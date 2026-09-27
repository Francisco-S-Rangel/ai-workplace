<!--
memory-bank/progress.md — WHY: durable milestone log (what is done / what is left).
Survives /compact and /clear because it lives on disk, not in the chat — this is
"external memory" as a compaction strategy (topic 5) and part of the Memory Bank (topic 8).
-->

# Progress

| Phase | Content | Status |
|---|---|---|
| 1 | Scaffold, pyproject, CLAUDE.md (root + nested), memory bank, git | done |
| 2 | study_buddy core + knowledge notes + tests + eval | done |
| 3 | MCP server + .mcp.json + list_mcp_tools.py + docs/mcp.md | done |
| 4 | Settings/permissions, hooks, skills, sub-agents, commands | done |
| 5 | storage-levels.md + other-tools.md | done |
| 6 | ASSESSMENT-MAP, DEMO-SCRIPT, concepts, levels, value case | done |
| 7 | Final verification | done (see below) |

## Final verification checklist (2026-09-27)

| # | Check (spec §5) | Result | How it was verified |
|---|---|---|---|
| 1 | No AGENTS.md, .cursor/, QWEN.md or other tools' config | ✅ | `find` over the repo (excluding .venv): none |
| 2 | `pytest` green incl. RAG eval | ✅ | 34 passed; hit@3 = 1.00 (threshold 0.8) |
| — | `ruff check` + `ruff format --check` | ✅ | clean, 56 files |
| 3 | `cli ask "what is lost in the middle?"` returns cited chunks | ✅ | top result `context-window.md#Lost in the Middle` |
| 4a | `scripts/list_mcp_tools.py` prints the tools | ✅ | 3 tools + 1 resource |
| 4b | Claude Code can start and call `study-notes` | ✅ | headless `claude -p --mcp-config .mcp.json` called `search_notes` |
| 4c | `/mcp` lists `study-notes` in an interactive session | ⏳ user | `claude mcp get` shows it as project scope, "Pending approval"; approve once in `/mcp` |
| 5 | Reading the fake key is blocked | ✅ | live: the deny rule blocked Read; the hook blocked `grep -r`; plus 21 hook test cases |
| 6 | Editing a `.py` file auto-formats | ✅ | live: PostToolUse ran ruff right after Write/Edit |
| 7a | The 3 sub-agents are discoverable | ✅ | the session announced code-reviewer, rag-evaluator, test-writer (the `/agents` UI is removed in 2.1.283) |
| 7b | `/review-parallel` produces `.agent-handoff/summary.md` | ⏳ user | needs an interactive run (it launches 3 sub-agents) |
| 8 | Both skills discoverable and work | ✅ / ⏳ | discovered live; `inspect_chunks.py` runs; a full `/rag-debug` run is left to the user |
| 9 | `/ask-notes` cites, and says "not found" off-topic | ✅ (headless equivalent) / ⏳ | same MCP tool + rules via `claude -p`: a cited answer, and "Not found in notes." for "capital of France" |
| 10 | ASSESSMENT-MAP covers every topic; DEMO-SCRIPT runs end to end | ✅ / ⏳ | 34 questions over all 14 topics; the full demo rehearsal is left to the user |
| 11 | Memory bank updated; one commit per phase | ✅ | 7 commits, one per phase |
| — | Committed `data/index.json` matches the notes | ✅ | re-ran ingest: no git diff |
