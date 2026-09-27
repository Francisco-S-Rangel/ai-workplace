# tests/test_chunking.py — WHY: pins down chunking behavior (topic 7: chunking) so a change to
# chunk_size / overlap / heading logic that breaks citations is caught by a test, not by a
# wrong answer later (topic 11: tests as a hallucination guard).
import pytest

from study_buddy.ingest import chunk_document, split_by_heading, split_by_size

DOC = """<!-- header comment that must not be indexed -->
# Alpha
one two three

## Beta
four five six
"""


def test_split_by_size_overlap():
    words = [str(i) for i in range(10)]
    windows = split_by_size(words, chunk_size=4, overlap=2)
    assert windows[0] == ["0", "1", "2", "3"]
    assert windows[1][:2] == windows[0][-2:]  # consecutive windows share `overlap` words
    assert windows[-1][-1] == "9"  # nothing is dropped at the end


def test_split_by_size_rejects_bad_params():
    with pytest.raises(ValueError):
        split_by_size(["a"], chunk_size=3, overlap=3)


def test_heading_preserved_and_comment_dropped():
    sections = split_by_heading(DOC)
    assert [h for h, _ in sections] == ["Alpha", "Beta"]
    assert all("header comment" not in body for _, body in sections)


def test_chunks_have_metadata_and_no_empty_text():
    long_doc = "# Long\n" + " ".join(f"w{i}" for i in range(50))
    chunks = chunk_document("long.md", long_doc, chunk_size=20, overlap=5)
    assert len(chunks) > 1
    for c in chunks:
        assert c["text"].strip()
        assert c["source"] == "long.md" and c["heading"] == "Long"
    assert len({c["chunk_id"] for c in chunks}) == len(chunks)  # ids are unique
