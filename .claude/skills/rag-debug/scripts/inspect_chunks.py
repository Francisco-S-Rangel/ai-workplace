# .claude/skills/rag-debug/scripts/inspect_chunks.py — WHY: helper bundled with the `rag-debug`
# skill (topic 9: skills can ship scripts; topic 7: chunking and retrieval quality).
# Shows how a note is chunked (optionally with different parameters) and how a query's tokens
# match the chunks, without modifying data/index.json.
# Usage:
#   python .claude/skills/rag-debug/scripts/inspect_chunks.py --source rag-basics.md
#   python .claude/skills/rag-debug/scripts/inspect_chunks.py --chunk-size 80 --overlap 10
#   python .claude/skills/rag-debug/scripts/inspect_chunks.py --query "lost in the middle"
"""Inspect chunks and query-token matches."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))  # so it runs from anywhere, even without `pip install -e .`

from study_buddy.index import build_index, index_stats  # noqa: E402
from study_buddy.retrieve import BM25, tokenize  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="only show chunks from this file")
    parser.add_argument("--chunk-size", type=int, default=120)
    parser.add_argument("--overlap", type=int, default=20)
    parser.add_argument("--query", help="show per-token idf and matching chunks")
    args = parser.parse_args()

    index = build_index(chunk_size=args.chunk_size, overlap=args.overlap)
    print(f"Stats: {index_stats(index)}\n")
    chunks = [c for c in index["chunks"] if not args.source or c["source"] == args.source]
    for c in chunks:
        words = len(c["text"].split())
        print(f"{c['chunk_id']:<32} {words:>4}w  {c['source']}#{c['heading']}")
        print(f"    {c['text'][:110]}...")

    if args.query:
        bm25 = BM25(index["chunks"])
        print(f"\nQuery tokens for {args.query!r} (stopwords removed):")
        for token in tokenize(args.query):
            hits = [
                c["chunk_id"]
                for c, tf in zip(index["chunks"], bm25.doc_tf, strict=True)
                if token in tf
            ]
            idf = bm25.idf.get(token, 0.0)
            print(f"  {token:<15} idf={idf:.2f}  in {len(hits)} chunks: {hits[:5]}")
        print("\nTop 5:")
        for r in bm25.search(args.query, top_k=5):
            print(f"  {r['score']:>7}  {r['citation']}  ({r['chunk_id']})")


if __name__ == "__main__":
    main()
