# study_buddy/cli.py — WHY: human entry point to the RAG pipeline.
# Assessment topic 7 (RAG) + topic 11 (citations): `ask` prints the top chunks with their
# `source#heading` citation so every answer is traceable to a file.
# Usage:
#   python -m study_buddy.cli ingest [--chunk-size 120] [--overlap 20]
#   python -m study_buddy.cli ask "what is lost in the middle?" [--top-k 3] [--source file.md]
"""Command-line interface: ingest and ask."""

import argparse

from study_buddy.index import INDEX_PATH, build_index, index_stats, load_retriever, save_index


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="study_buddy")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="chunk docs/knowledge and write data/index.json")
    ingest.add_argument("--chunk-size", type=int, default=120)
    ingest.add_argument("--overlap", type=int, default=20)

    ask = sub.add_parser("ask", help="retrieve the top chunks for a question")
    ask.add_argument("question")
    ask.add_argument("--top-k", type=int, default=3)
    ask.add_argument("--source", help="only search this file, e.g. rag-basics.md")

    args = parser.parse_args(argv)
    if args.command == "ingest":
        index = build_index(chunk_size=args.chunk_size, overlap=args.overlap)
        save_index(index)
        print(f"Wrote {INDEX_PATH}: {index_stats(index)}")
    else:
        results = load_retriever().search(args.question, args.top_k, args.source)
        if not results:
            print("Not found in notes.")
        for rank, r in enumerate(results, 1):
            print(f"[{rank}] {r['citation']}  (score {r['score']}, id {r['chunk_id']})")
            print(f"    {r['text'][:300]}{'...' if len(r['text']) > 300 else ''}\n")


if __name__ == "__main__":
    main()
