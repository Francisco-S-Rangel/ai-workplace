# tests/test_rag_eval.py — WHY: automated RAG evaluation (topic 11: evals; topic 14 / A4:
# "automated evals detect regressions"). Each question in eval/eval_set.jsonl has an expected
# source file; hit@3 = share of questions whose expected source is in the top 3 results.
# If someone changes chunking or BM25 and quality drops below the threshold, this test fails.
import json
from pathlib import Path

from study_buddy.index import build_index
from study_buddy.retrieve import BM25

EVAL_SET = Path(__file__).parent / "eval" / "eval_set.jsonl"
HIT_AT_K_THRESHOLD = 0.8
K = 3


def hit_at_k(retriever: BM25, cases: list[dict], k: int = K) -> tuple[float, list[str]]:
    misses = []
    for case in cases:
        sources = [r["source"] for r in retriever.search(case["question"], top_k=k)]
        if case["expected_source"] not in sources:
            misses.append(f"{case['question']!r} -> got {sources}")
    return 1 - len(misses) / len(cases), misses


def test_hit_at_3_above_threshold():
    # Built fresh from docs/knowledge (not data/index.json) so the eval measures current code.
    retriever = BM25(build_index()["chunks"])
    cases = [json.loads(line) for line in EVAL_SET.read_text(encoding="utf-8").splitlines()]
    score, misses = hit_at_k(retriever, cases)
    print(f"hit@{K} = {score:.2f} ({len(cases)} questions)")
    assert score >= HIT_AT_K_THRESHOLD, f"hit@{K}={score:.2f} misses: {misses}"
