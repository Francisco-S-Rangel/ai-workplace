<!--
memory-bank/project-brief.md — WHY: the stable "what and why" of the project, rarely changes.
Imported into CLAUDE.md with `@memory-bank/project-brief.md` to show modular instructions
without duplication (topic 2) and part of the Memory Bank pattern (topic 8).
-->

# Project brief

- **What:** "Study Buddy" — local RAG over markdown notes in `docs/knowledge/`, served to
  Claude Code by a custom read-only MCP server.
- **Why:** a working demo repo for the internal AI Assessment (levels A0–A5). Every concept
  in the assessment maps to a real file here (see `docs/ASSESSMENT-MAP.md`).
- **Scope limits:** ~4 hours of work, no external services, 3 dependencies (`mcp`, `pytest`, `ruff`).
- **Audience:** me (studying) and the assessor (live demo, see `docs/DEMO-SCRIPT.md`).
