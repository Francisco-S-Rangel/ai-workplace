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

## 2026-09-27 — Claude Code formats checked against the official docs
- **Hooks** (code.claude.com/docs/en/hooks): `hooks.<Event>[].matcher` + `hooks[].type: command`.
  PreToolUse exit 2 blocks the call and stderr goes to Claude. Stop exit 2 would keep Claude
  working, so the reminder uses exit 0 plus a JSON `systemMessage`. On Windows, hook commands
  run through Git Bash if it's installed, so `${CLAUDE_PROJECT_DIR}` expands.
- **Permissions** (docs/en/permissions): the Bash prefix form is now `Bash(cmd *)`, and the
  spec's `Bash(cmd:*)` is an equivalent legacy form. I used the space form. Path rules work
  only for `Read(...)`/`Edit(...)`, and `Write(path)` is never consulted, so writes to the index
  are denied with `Edit(./data/index.json)`. Read deny rules also cover `cat`/`head` in Bash but
  not `grep -r`, which is why the hook exists. The PowerShell tool needs its own rules
  (`PowerShell(Remove-Item *)`), because `Bash(rm *)` doesn't cover it.
- **Sub-agents** (docs/en/sub-agents): frontmatter `name`, `description`, `tools`, `model`,
  plus an optional per-agent `hooks:`. The `/agents` wizard is gone; list agents by asking
  Claude, typing `@`, or `/tasks`.
- **Skills / commands** (docs/en/skills): skills use `name` + `description` (+ `argument-hint`).
  `.claude/commands/*.md` still works and is treated like a skill (skills are recommended for new
  work). The commands are kept as the spec asks.

## 2026-09-27 — Read-only reviewer that can still hand off
- **Decision:** `code-reviewer` has `Read, Grep, Glob, Write`, and an agent-scoped PreToolUse
  hook (`restrict_writes.py .agent-handoff/`) limits Write to the hand-off folder. `test-writer`
  is limited to `tests/` + `.agent-handoff/`.
- **Alternatives:** no Write at all (then it can't hand off through a file); the parent copies the
  summary into a file (loses detail).
- **Why:** frontmatter tool lists are all-or-nothing, and a hook adds path-level least privilege.
  The orchestrator writes `diff.patch` because the reviewer has no Bash to run `git diff`.

## 2026-09-27 — `inspect_chunks.py` lives inside the skill folder
- **Decision:** `.claude/skills/rag-debug/scripts/inspect_chunks.py` instead of `scripts/`.
- **Why:** it shows that a skill ships its own tooling. The spec allowed either location.

## 2026-09-27 — Hooks verified live in the build session
- The deny rule blocked Read of the fake key ("denied by your permission settings").
- The hook blocked `grep -r FAKE` on the protected folder (`[guard_paths hook] …`).
- The PostToolUse hook reformatted an ugly `.py` file right after Write.
- Also covered by `tests/test_hooks.py` (21 cases).

## 2026-09-27 — The guard hook matches command TEXT (known false positive)
- **Observation:** the hook blocked a Bash heredoc that only *wrote documentation mentioning*
  the protected folder name. The regex can't tell intent from text.
- **Decision:** keep it strict (fail closed) for the demo. Write docs with the Write/Edit tools,
  which the hook checks by path, not content.
- **Talking point:** text-matching guards trade false positives for safety. OS-level sandboxing
  enforces by actual file access instead of by command text.

## 2026-09-27 — Agents and skills discovered live
- After Phase 4, the running session announced the 3 sub-agents (`code-reviewer`,
  `rag-evaluator`, `test-writer`) and 5 skills/commands (`add-knowledge-note`, `rag-debug`,
  `ask-notes`, `checkpoint`, `review-parallel`) with no restart, which confirms the frontmatter is valid.

## 2026-09-27 — The other-tools comparison is sourced, gaps marked
- **Decision:** every cell in `docs/other-tools.md` comes from a docs page fetched on 2026-09-27,
  or is marked "verify in docs".
- **Notable:** `MoonshotAI/kimi-cli` was archived on 2026-09-23 in favor of "Kimi Code CLI"
  (whose repo URL returned 404), so most Kimi cells stay unverified. Qwen Code's custom
  commands moved from `.toml` to `.md`.
