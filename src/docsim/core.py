import os
import csv
from itertools import product, combinations
from tqdm import tqdm
from collections import defaultdict
from .file_handling import (find_files, group_files_by_subfolder,
                           merge_and_clean_text, get_author_name_from_path)
from .similarity import compute_similarities
from .visualization import generate_html_dashboard

def compare_folders(folder1, folder2, similarity_threshold=0.85,
                   output_csv="similarity_results.csv",
                   output_html="similarity_dashboard.html",
                   max_workers=None):
    
    files1 = find_files(folder1)
    files2 = find_files(folder2)

    print(f"📁 Folder 1: Found {len(files1)} files (PDF & DOCX)")
    print(f"📁 Folder 2: Found {len(files2)} files (PDF & DOCX)")

    grouped1 = group_files_by_subfolder(files1, folder1)
    grouped2 = group_files_by_subfolder(files2, folder2)

    texts1 = {}
    representative_files1 = []
    print("🧹 Extracting and merging texts for folder 1...")
    for folder_name, file_group in tqdm(grouped1.items()):
        merged_text, repr_file = merge_and_clean_text(file_group, folder1)
        if not merged_text:
            print(f"⚠️ Empty or unreadable text in group: {folder_name} (from folder 1)")
            continue
        texts1[repr_file] = merged_text
        representative_files1.append(repr_file)

    texts2 = {}
    representative_files2 = []
    print("🧹 Extracting and merging texts for folder 2...")
    for folder_name, file_group in tqdm(grouped2.items()):
        merged_text, repr_file = merge_and_clean_text(file_group, folder2)
        if not merged_text:
            print(f"⚠️ Empty or unreadable text in group: {folder_name} (from folder 2)")
            continue
        texts2[repr_file] = merged_text
        representative_files2.append(repr_file)

    pairs = []
    processed_pairs_for_computation = set()

    # Comparisons within Folder 1
    for file1_repr_a, file1_repr_b in combinations(representative_files1, 2):
        sorted_repr_files = tuple(sorted((file1_repr_a, file1_repr_b)))
        if sorted_repr_files not in processed_pairs_for_computation:
            processed_pairs_for_computation.add(sorted_repr_files)
            if file1_repr_a in texts1 and file1_repr_b in texts1:
                pairs.append((file1_repr_a, file1_repr_b, texts1[file1_repr_a], texts1[file1_repr_b], similarity_threshold))

    # Comparisons within Folder 2 (only if different folders)
    if os.path.abspath(folder1) != os.path.abspath(folder2):
        for file2_repr_a, file2_repr_b in combinations(representative_files2, 2):
            sorted_repr_files = tuple(sorted((file2_repr_a, file2_repr_b)))
            if sorted_repr_files not in processed_pairs_for_computation:
                processed_pairs_for_computation.add(sorted_repr_files)
                if file2_repr_a in texts2 and file2_repr_b in texts2:
                    pairs.append((file2_repr_a, file2_repr_b, texts2[file2_repr_a], texts2[file2_repr_b], similarity_threshold))

    # Cross-folder comparisons
    for file1_repr in representative_files1:
        for file2_repr in representative_files2:
            if os.path.abspath(file1_repr) == os.path.abspath(file2_repr):
                continue
            
            sorted_repr_files = tuple(sorted((file1_repr, file2_repr)))
            if sorted_repr_files not in processed_pairs_for_computation:
                processed_pairs_for_computation.add(sorted_repr_files)
                if file1_repr in texts1 and file2_repr in texts2:
                    pairs.append((file1_repr, file2_repr, texts1[file1_repr], texts2[file2_repr], similarity_threshold))

    print(f"🔄 Comparing {len(pairs)} document group pairs...")

    raw_results = compute_similarities(pairs, max_workers)

    if not raw_results:
        print("❌ No pairs exceeded the similarity threshold.")
        generate_html_dashboard([], folder1, folder2, output_html=output_html)
        return

    best_similarity_per_author_pair = {}
    for file1_repr, file2_repr, sim in raw_results:
        author1 = get_author_name_from_path(file1_repr, folder1)
        author2 = get_author_name_from_path(file2_repr, folder2)
        author_pair_key = tuple(sorted((author1, author2)))

        if author_pair_key not in best_similarity_per_author_pair or \
           sim > best_similarity_per_author_pair[author_pair_key][2]:
            best_similarity_per_author_pair[author_pair_key] = (file1_repr, file2_repr, sim)
            
    final_results = list(best_similarity_per_author_pair.values())
    final_results.sort(key=lambda x: x[2], reverse=True)

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Author1_Folder", "Author2_Folder", "Similarity", "Representative_File1", "Representative_File2"])
        for file1_repr, file2_repr, sim in final_results:
            author1_folder_name = os.path.basename(os.path.dirname(file1_repr))
            author2_folder_name = os.path.basename(os.path.dirname(file2_repr))
            writer.writerow([author1_folder_name, author2_folder_name, sim, file1_repr, file2_repr])

    print(f"💾 CSV saved at: {output_csv}")
    generate_html_dashboard(final_results, folder1, folder2, output_html=output_html)
