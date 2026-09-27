<!--
study_buddy/CLAUDE.md (nested / folder level) — WHY: demonstrates SCOPED instructions.
Claude Code loads nested CLAUDE.md files on demand when it works with files in this folder,
so these rules cost no context in unrelated work (topic 2: storage levels + scoping;
compare with Cursor's `globs:` in .cursor/rules/*.mdc — see docs/other-tools.md).
-->

# Rules for `study_buddy/`

- Keep BM25 **pure Python**: no numpy, scipy, rank_bm25 or any other library.
  The point is that the algorithm is short enough to explain line by line.
- Keep `retrieve.py` under ~100 lines.
- Every chunk must keep its metadata: `source`, `heading`, `chunk_id`. Citations are
  always formatted `source#heading`.
- Chunking parameters (`chunk_size`, `overlap`) are function arguments with defaults,
  never hard-coded inside the loop.
- After changing chunking or retrieval, run the eval: `.venv\Scripts\python.exe -m pytest tests/test_rag_eval.py`
  and log any parameter change in `memory-bank/decision-log.md`.
