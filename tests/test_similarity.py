import pytest
from docsim.similarity import compute_similarity

def test_compute_similarity():
    text = "This is a test document about machine learning."
    result = compute_similarity(("file1", "file2", text, text, 0.5))
    assert result is not None
    assert result[2] == pytest.approx(1.0, 0.01)
    
    text1 = "This is about dogs"
    text2 = "This is about cats"
    result = compute_similarity(("file1", "file2", text1, text2, 0.5))
    assert result is not None
    assert result[2] < 1.0
    
    assert compute_similarity(("file1", "file2", "", "text", 0.5)) is None
    assert compute_similarity(("file1", "file2", "text", "", 0.5)) is None
