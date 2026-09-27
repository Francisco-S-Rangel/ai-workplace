<!--
memory-bank/active-context.md — WHY: "what am I doing right now" — short-lived working state.
Written by `/checkpoint` before /compact or /clear so nothing important is lost when the
conversation is summarized (topic 5: context management; topic 8: memory bank).
-->

# Active context

_Last updated: 2026-09-27_

- **Current focus:** all 7 phases are done; the repo is ready for the demo.
- **Done this session:** built and verified everything; see the checklist in `progress.md`.
- **Next step (user):** in a fresh `claude` session, approve `study-notes` in `/mcp`, then rehearse
  `docs/DEMO-SCRIPT.md`, including `/review-parallel`, `/rag-debug` and `/ask-notes`.
- **Open questions:** official assessment wording (the map uses reconstructed questions);
  "verify in docs" cells in `docs/other-tools.md` (mostly Kimi, whose CLI repo is archived).
- **Watch out:** the guard hook blocks any shell command whose text names the protected folder
  or `.env`. `/agents` is removed; ask "which sub-agents are available?". The MCP SDK is pinned `<2`.
