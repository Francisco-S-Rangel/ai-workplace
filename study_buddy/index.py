# study_buddy/index.py — WHY: builds and stores the searchable index (`data/index.json`).
# Assessment topic 7 (local RAG): this JSON file is the stand-in for a vector store.
# In production you would embed chunks and store them in Chroma / FAISS / Qdrant, often with
# hybrid retrieval (BM25 + dense vectors) and a reranker on top. Here BM25 statistics are
# recomputed on load: cheap for a few dozen chunks, and the index stays human-readable.
"""Build, save and load the chunk index."""

import json
from pathlib import Path

from study_buddy.ingest import chunk_folder
from study_buddy.retrieve import BM25

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "docs" / "knowledge"
INDEX_PATH = ROOT / "data" / "index.json"


def build_index(
    knowledge_dir: Path = KNOWLEDGE_DIR, chunk_size: int = 120, overlap: int = 20
) -> dict:
    chunks = chunk_folder(knowledge_dir, chunk_size, overlap)
    return {"params": {"chunk_size": chunk_size, "overlap": overlap}, "chunks": chunks}


def save_index(index: dict, path: Path = INDEX_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_index(path: Path = INDEX_PATH) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"{path} not found - run: python -m study_buddy.cli ingest")
    return json.loads(path.read_text(encoding="utf-8"))


def load_retriever(path: Path = INDEX_PATH) -> BM25:
    return BM25(load_index(path)["chunks"])


def index_stats(index: dict) -> dict:
    chunks = index["chunks"]
    sizes = [len(c["text"].split()) for c in chunks]
    return {
        "chunk_count": len(chunks),
        "source_count": len({c["source"] for c in chunks}),
        "avg_chunk_words": round(sum(sizes) / len(sizes), 1) if sizes else 0,
        **index["params"],
    }
