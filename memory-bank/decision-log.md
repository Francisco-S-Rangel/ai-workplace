<!--
memory-bank/decision-log.md — WHY: ADR-style log of non-obvious choices (date, decision,
alternatives, why). Lets a future session (or a teammate, or the assessor) understand WHY
the code looks like this without re-deriving it — topic 8 (memory bank) and topic 11
(grounding: decisions are written down, not remembered by the model).
-->

# Decision log

## 2026-09-27 — Pin `mcp>=1.2,<2`
- **Decision:** use MCP Python SDK 1.x (installed 1.30.0).
- **Alternatives:** SDK 2.x (2.2.0), where `FastMCP` was renamed to
  `MCPServer` (`from mcp.server.mcpserver import MCPServer`).
- **Why:** the plan specifies `FastMCP`, and most tutorials and docs still show the 1.x API.
  Migrating later is a documented rename.

## 2026-09-27 — Local virtual env `.venv/`
- **Decision:** dependencies go into `.venv/`, and all commands use `.venv\Scripts\python.exe`.
- **Alternatives:** global pip install; uv.
- **Why:** reproducible, keeps the system Python clean, and needs no extra tool.

## 2026-09-27 — BM25 instead of embeddings
- **Decision:** pure-Python BM25 lexical retrieval, index saved as JSON.
- **Alternatives:** embeddings + Chroma/FAISS/Qdrant; hybrid BM25 + dense + reranker.
- **Why:** zero dependencies, about 50 lines you can explain, and good enough for a corpus
  of about 7 notes. Production would use hybrid retrieval.

## 2026-09-27 — Commit `data/index.json`
- **Decision:** the index is committed, not gitignored.
- **Why:** it's a "protected artifact" in the hook demo, so it must exist. It is regenerated
  only by `study_buddy.cli ingest` (Python writes it; the agent's Write tool is blocked).

## 2026-09-27 — Header comments in JSON files
- **Decision:** JSON can't contain comments. `.claude/settings.json` and `.mcp.json` are
  explained in `docs/` (`docs/mcp.md`, `docs/storage-levels.md`) instead of adding
  unknown keys that a strict schema might reject.

## 2026-09-27 — Chunking defaults: 120 words, 20 overlap, split by heading first
- **Decision:** split on markdown headings, then use word windows (`chunk_size=120`, `overlap=20`).
  The heading is indexed along with the body.
- **Alternatives:** fixed character windows; sentence splitting; token-based sizes.
- **Why:** headings mark topic boundaries in these notes. Words are easy to explain. The
  result is 37 chunks averaging about 72 words, with hit@3 = 1.00 on the 10-question eval.

## 2026-09-27 — The eval builds the index fresh
- **Decision:** `tests/test_rag_eval.py` rebuilds from `docs/knowledge/` instead of reading
  `data/index.json`, with a threshold of hit@3 >= 0.8.
- **Why:** the eval should measure the current code, not a stale committed index.
  (`eval_set.jsonl` has no header comment because JSONL can't hold comments; the test file
  documents it.)

## 2026-09-27 — `.mcp.json` uses a relative venv command
- **Decision:** `"command": ".venv/Scripts/python.exe"` (relative to the repo root, where
  Claude Code starts project servers). The package is installed editable (`pip install -e .`),
  so `-m mcp_server.server` imports from any working directory.
- **Alternatives:** `"command": "python"` (would pick the system Python, which doesn't have `mcp`);
  an absolute path (breaks on other machines).
- **Verified:** `claude mcp get study-notes` reads it as project scope and "Pending approval".
  Connecting after approval has to be checked interactively with `/mcp`.

## 2026-09-27 — `/agents` wizard removed in Claude Code 2.1.283
- **Observation:** running `/agents` prints "The /agents wizard has been removed … edit
  `.claude/agents/`". Sub-agents are still defined as `.claude/agents/*.md`.
- **Impact:** the demo shows the agent files, plus asking Claude "which sub-agents are available?",
  instead of relying on the `/agents` UI.
