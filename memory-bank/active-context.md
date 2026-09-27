<!--
memory-bank/active-context.md — WHY: "what am I doing right now" — short-lived working state.
Written by `/checkpoint` before /compact or /clear so nothing important is lost when the
conversation is summarized (topic 5: context management; topic 8: memory bank).
-->

# Active context

_Last updated: 2026-09-27_

- **Current focus:** Phase 4 is done (settings, 4 hooks, 2 skills, 3 agents, 3 commands; 34 tests green).
- **Next step:** Phase 5 — `docs/storage-levels.md` + `docs/other-tools.md`.
- **Open questions:** the user still has to check `/mcp` approval, `/review-parallel` and `/ask-notes` in a fresh session.
- **Watch out:** the guard hook blocks ANY shell command whose text names the protected folder or
  `.env`, including heredocs and commit messages. Use Write/Edit for docs that mention them.
