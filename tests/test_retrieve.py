# tests/test_retrieve.py — WHY: sanity checks for the BM25 ranking (topic 7: retrieval
# quality) and the citation format (topic 11: citations make claims verifiable).
from study_buddy.retrieve import BM25, tokenize

CHUNKS = [
    {"chunk_id": "a-00", "source": "a.md", "heading": "Cats", "text": "cats purr and cats nap"},
    {"chunk_id": "b-00", "source": "b.md", "heading": "Dogs", "text": "dogs bark loudly"},
    {"chunk_id": "c-00", "source": "c.md", "heading": "Pets", "text": "cats and dogs are pets"},
]


def test_tokenize_drops_stopwords_and_case():
    assert tokenize("What IS the Context?") == ["context"]


def test_most_relevant_chunk_ranks_first():
    results = BM25(CHUNKS).search("cats purr", top_k=3)
    assert results[0]["chunk_id"] == "a-00"
    assert all(r["score"] > 0 for r in results)
    assert results == sorted(results, key=lambda r: r["score"], reverse=True)


def test_citation_and_source_filter():
    results = BM25(CHUNKS).search("cats", source="c.md")
    assert [r["citation"] for r in results] == ["c.md#Pets"]


def test_no_match_returns_empty():
    assert BM25(CHUNKS).search("quantum physics") == []
