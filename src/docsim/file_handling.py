import os
import re
import fitz
from pdf2image import convert_from_path
import pytesseract
from docx import Document
from collections import defaultdict
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    text = ''
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text().strip()

        if not text.strip():  # Fallback to OCR if no text found
            print(f"🔍 OCR in corso per: {pdf_path}")
            images = convert_from_path(pdf_path)
            for img in images:
                text += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def extract_text_from_docx(docx_path):
    text = ''
    try:
        doc = Document(docx_path)
        paragraphs = [p.text for p in doc.paragraphs]
        text = '\n'.join(paragraphs)
    except Exception as e:
        print(f"Error reading {docx_path}: {e}")
    return text

def find_files(root_dir):
    files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            ext = file.lower().split('.')[-1]
            if ext in ['pdf', 'docx']:
                full_path = os.path.join(dirpath, file)
                files.append(full_path)
    return files

def get_author_name_from_path(file_path, root_dir):
    abs_root = os.path.abspath(root_dir)
    abs_file = os.path.abspath(file_path)

    try:
        rel_path = os.path.relpath(abs_file, abs_root)
        parts = rel_path.split(os.sep)
        if parts and parts[0] != '..':
            folder_name = parts[0]
            if '_' in folder_name:
                author_name = folder_name.split('_')[0]
                if author_name:
                    return author_name
            return folder_name
    except ValueError:
        pass

    folder_name_from_file = os.path.basename(os.path.dirname(abs_file))
    if '_' in folder_name_from_file:
        author_name = folder_name_from_file.split('_')[0]
        if author_name:
            return author_name
    return folder_name_from_file

def remove_author_name(text, author_name):
    if not author_name:
        return text
    name_variants = re.split(r'[-_\s]', author_name)
    patterns = [re.escape(name) for name in name_variants if name]
    if not patterns:
        return text
    pattern = r'\b(?:' + '|'.join(patterns) + r')\b'
    return re.sub(pattern, '', text, flags=re.IGNORECASE)

def group_files_by_subfolder(files, root_dir):
    grouped = defaultdict(list)
    for f in files:
        rel_path = os.path.relpath(f, root_dir)
        parts = rel_path.split(os.sep)
        if len(parts) > 1 and parts[0] != '..':
            folder = parts[0]
        else:
            folder = os.path.basename(os.path.dirname(f))
        if not folder:
            folder = "Uncategorized_Root"
        grouped[folder].append(f)
    return grouped

def merge_and_clean_text(file_group, root_dir):
    merged_text = ''
    file_group.sort()
    
    for f in file_group:
        ext = f.lower().split('.')[-1]
        if ext == 'pdf':
            text = extract_text_from_pdf(f).strip()
        elif ext == 'docx':
            text = extract_text_from_docx(f).strip()
        else:
            text = ''
        author = get_author_name_from_path(f, root_dir)
        clean = remove_author_name(text, author)
        merged_text += '\n' + clean
    return merged_text.strip(), file_group[0]
