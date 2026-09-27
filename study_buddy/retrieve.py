# study_buddy/retrieve.py — WHY: pure-Python BM25 retrieval with citations.
# Assessment topic 7 (retrieval quality, citations) + topic 11 (grounding): the answer is built
# from retrieved chunks, and each carries `source#heading` so a human can verify it.
# No numpy / rank_bm25 on purpose (see study_buddy/CLAUDE.md): short enough to explain.
"""BM25 ranking over chunks."""

import math
import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = set(
    "a an and are as at be by can do does for from how in is it of on or so that the this to "
    "what when where which who why with you your".split()
)


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens without stopwords."""
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


def citation(chunk: dict) -> str:
    return f"{chunk['source']}#{chunk['heading']}"


class BM25:
    """Okapi BM25.

    score(q, d) = sum over query terms t of
        idf(t) * tf(t, d) * (k1 + 1) / (tf(t, d) + k1 * (1 - b + b * len(d) / avgdl))
    idf(t) = ln(1 + (N - df(t) + 0.5) / (df(t) + 0.5))
    k1 controls term-frequency saturation, b controls length normalization.
    """

    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1, self.b = k1, b
        # The heading is indexed together with the body: it is a strong topic signal.
        self.doc_tf = [Counter(tokenize(c["heading"] + " " + c["text"])) for c in chunks]
        self.doc_len = [sum(tf.values()) for tf in self.doc_tf]
        self.avgdl = sum(self.doc_len) / len(chunks) if chunks else 0.0
        df = Counter(term for tf in self.doc_tf for term in tf)
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def score(self, query_terms: list[str], i: int) -> float:
        tf, dl, total = self.doc_tf[i], self.doc_len[i], 0.0
        for t in query_terms:
            if t in tf:
                norm = tf[t] + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                total += self.idf[t] * tf[t] * (self.k1 + 1) / norm
        return total

    def search(self, query: str, top_k: int = 3, source: str | None = None) -> list[dict]:
        """Top-k chunks (score > 0), optionally filtered by source file, with citations."""
        terms = tokenize(query)
        results = []
        for i, chunk in enumerate(self.chunks):
            if source and chunk["source"] != source:
                continue
            s = self.score(terms, i)
            if s > 0:
                results.append({**chunk, "score": round(s, 4), "citation": citation(chunk)})
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]
