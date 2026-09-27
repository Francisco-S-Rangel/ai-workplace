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

## Template for new entries
- **Prompt:** what I asked (keep the key constraints verbatim).
- **Context given:** files/@mentions, plan mode on/off.
- **Result:** what changed, and whether tests passed.
- **Lesson:** what I would phrase differently next time.
