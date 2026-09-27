<!--
docs/prompt-log.md — WHY: evidence of an AI-First workflow (topics 1 and 14, levels A3–A5).
Records the key prompts that built this repo, what mode they were run in, and what came out,
so the process can be reviewed and repeated, not just the result.
-->

# Prompt log

| # | Date | Mode | Prompt (summary) | Outcome |
|---|---|---|---|---|
| 1 | 2026-09-27 | Plan mode | Pasted the full build plan (`AI-Workplace-Plan.md`): goal, hard constraints, the 14 assessment topics, the "Study Buddy" app, the Claude Code config, docs, 7 phases, and a verification checklist. | Claude explored the (empty) folder, checked the Python/git/Claude versions, wrote an execution plan (venv, doc-verified formats, commit per phase), and got it approved. |
| 2 | 2026-09-27 | Execute | Phase 1 — scaffold. | Found that `mcp` 2.x renamed FastMCP → pinned `<2` (see decision log). |
| 3 | 2026-09-27 | Execute | Phase 2 — RAG core ("go"). | 7 notes, heading+size chunking, BM25, CLI, 10 tests, hit@3 = 1.00. |
| 4 | 2026-09-27 | Execute | Phase 3 — MCP ("go"). | FastMCP server (3 read-only tools + 1 resource), SDK list script, `claude mcp get` shows it pending approval. |
| 5 | 2026-09-27 | Execute | Phase 4 — Claude Code controls ("go"). | Checked formats against the official docs first. Deny rule + hook blocked the fake key live, the format hook fired live, 34 tests. The hook also blocked one of my own heredocs (false positive, logged). |
| 6 | 2026-09-27 | Execute | Phase 5 — comparison docs ("go"). | Fetched the Cursor, Qwen Code and Kimi docs; built the storage-levels + other-tools tables; unconfirmed cells marked "verify in docs". |
| 7 | 2026-09-27 | Execute | Phase 6 — study docs ("go"). | 34-question map, demo script, 6 concept pages, levels, value case. Measured that chunk size cannot break the eval, so the regression demo uses a code bug instead. |
| 8 | 2026-09-27 | Execute | Phase 7 — final verification ("go"). | All automatable checks green. Headless `claude -p --mcp-config` proved the MCP server launches and grounding works; interactive-only checks left to the user. |

## Template for new entries
- **Prompt:** what I asked (keep the key constraints verbatim).
- **Context given:** files/@mentions, plan mode on/off.
- **Result:** what changed, and whether tests passed.
- **Lesson:** what I would phrase differently next time.
