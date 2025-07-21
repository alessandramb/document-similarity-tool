import pytest
import os
import tempfile
from docsim.file_handling import (
    extract_text_from_pdf,
    extract_text_from_docx,
    find_files,
    group_files_by_subfolder,
    merge_and_clean_text
)

@pytest.fixture
def sample_docx_path():
    from docx import Document
    doc = Document()
    doc.add_paragraph("This is a test document.")
    
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
        doc.save(tmp.name)
        yield tmp.name
    os.unlink(tmp.name)

@pytest.fixture
def sample_pdf_path():
    import fitz
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        doc = fitz.open()
        doc.insert_page(0)
        doc.save(tmp.name)
        yield tmp.name
    os.unlink(tmp.name)

def test_extract_text_from_docx(sample_docx_path):
    text = extract_text_from_docx(sample_docx_path)
    assert "This is a test document." in text

def test_find_files(tmp_path):
    subdir = tmp_path / "subfolder"
    subdir.mkdir()
    
    pdf_file = tmp_path / "test.pdf"
    pdf_file.touch()
    docx_file = subdir / "test.docx"
    docx_file.touch()
    
    files = find_files(str(tmp_path))
    assert len(files) == 2
    assert str(pdf_file) in files
    assert str(docx_file) in files

def test_group_files_by_subfolder(tmp_path):
    sub1 = tmp_path / "author1"
    sub1.mkdir()
    sub2 = tmp_path / "author2"
    sub2.mkdir()
    
    file1 = sub1 / "doc1.pdf"
    file1.touch()
    file2 = sub2 / "doc2.docx"
    file2.touch()
    
    groups = group_files_by_subfolder([str(file1), str(file2)], str(tmp_path))
    assert len(groups) == 2
    assert "author1" in groups
    assert "author2" in groups
