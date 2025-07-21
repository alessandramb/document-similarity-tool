from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def compute_similarity(pair):
    file1_repr, file2_repr, text1, text2, threshold = pair
    if not text1 or not text2:
        return None
    try:
        vec = TfidfVectorizer().fit_transform([text1, text2])
        sim = cosine_similarity(vec[0:1], vec[1:2])[0][0]
        if sim >= threshold:
            return (file1_repr, file2_repr, sim)
    except Exception:
        return None
    return None

def compute_similarities(pairs, max_workers=None):
    max_workers = max_workers or (multiprocessing.cpu_count() - 1)
    raw_results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for res in tqdm(executor.map(compute_similarity, pairs), total=len(pairs)):
            if res:
                raw_results.append(res)
    return raw_results
