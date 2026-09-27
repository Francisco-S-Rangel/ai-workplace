<!--
docs/DEMO-SCRIPT.md — WHY: a 10–15 minute live walkthrough for the assessor that touches every
topic with a real file or command. Each step: what I say, what I type, what should happen.
-->

# Demo script (10–15 min)

## Before the call (5 min, not shown)
- [ ] `cd` into the repo; `.venv\Scripts\python.exe -m pytest` → all green.
- [ ] `.venv\Scripts\python.exe -m study_buddy.cli ingest` (the index is up to date).
- [ ] Start `claude` in the repo; approve the `study-notes` MCP server once (`/mcp`).
- [ ] `git status` is clean (so the Stop-hook reminder stays quiet until step 8).
- [ ] Open in the editor: `CLAUDE.md`, `.claude/settings.json`, `docs/ASSESSMENT-MAP.md`.

---

### 1. Project instructions (1 min) — topics 2, 1
- **Say:** "In Claude Code the AGENTS.md equivalent is `CLAUDE.md`. It's loaded every session,
  so it's short: commands, conventions, definition of done, a don't-touch list. Details are imported
  with `@` or live in a nested file that only loads when I work in that folder."
- **Type:** `/memory`, then show `CLAUDE.md` and `study_buddy/CLAUDE.md`.
- **Expect:** both files listed; point at the `@memory-bank/project-brief.md` import.
- **Bonus:** `docs/storage-levels.md` for managed > CLI > local > project > user.

### 2. Plan mode on a small feature (2 min) — topic 3
- **Say:** "For a multi-file change I plan first; for a typo I wouldn't."
- **Type:** `Shift+Tab` (plan mode), then:
  `Add a --json flag to "study_buddy.cli ask" that prints results as JSON, with a test.`
- **Expect:** Claude reads `cli.py` and the tests and proposes a plan, **with no edits**.
- **Say:** "I can review and reject before anything changes." Reject or Esc (keep the demo clean).

### 3. Skill (1.5 min) — topic 9
- **Say:** "A skill is a procedure. Only its description sits in context; the body and its
  script load when needed."
- **Type:** `/rag-debug "chunking overlap"`
- **Expect:** Claude runs `cli ask` and the bundled `inspect_chunks.py`, showing chunks, per-token idf and the top 5.

### 4. MCP + grounded answers (2 min) — topics 6, 7, 11
- **Type:** `/mcp` → `study-notes` connected, 3 tools.
- **Say:** "To list capabilities at protocol level, I call `tools/list`:"
  `! .venv\Scripts\python.exe scripts/list_mcp_tools.py`
- **Type:** `/ask-notes what is lost in the middle?`
- **Expect:** a short answer, every sentence cited `[context-window.md#Lost in the Middle]`.
- **Type:** `/ask-notes what is the capital of France?`
- **Expect:** **"Not found in notes."** "That's the hallucination guard: permission to say no."

### 5. Hooks and permissions block the secrets folder (1.5 min) — topic 10
- **Type:** `read secrets/api_key.txt`
- **Expect:** blocked: *denied by your permission settings*.
- **Type:** `use grep -r to search for FAKE inside the secrets folder`
- **Expect:** `[guard_paths hook] Bash command blocked…` "The deny rule can't see this one; the
  hook can. Hooks are deterministic: the harness runs them, not the model."
- **Bonus:** `/ask-notes what does the prompt injection example say?` → Claude quotes the
  "IGNORE PREVIOUS INSTRUCTIONS" line as data and doesn't act on it.

### 6. Multi-agent orchestration (2.5 min) — topics 4, 14
- **Say:** "Sub-agents have their own context and return only a summary, so they hand off
  through files. Each one has least privilege: the reviewer can only write to `.agent-handoff/`."
- **Type:** `/review-parallel`
- **Expect:** three agents run in parallel, then `.agent-handoff/summary.md` with a GO/NO-GO
  verdict, the review, tests, eval and conflicts.
- **Show:** `.agent-handoff/review.md`, `eval.md`, `summary.md`.

### 7. Eval catches a regression (1.5 min) — topics 11, 14 (A4)
- **Type:** `In study_buddy/retrieve.py change reverse=True to reverse=False, then run pytest`
- **Expect:** ruff formats the file via the PostToolUse hook; pytest **fails** with hit@3 = 0.60 < 0.8.
- **Type:** `Esc Esc` → rewind to before the edit (checkpoints), then re-run pytest → green.

### 8. Context management (1.5 min) — topics 5, 8, 12
- **Type:** `/context` "Here's what fills the window; MCP tools are deferred."
- **Type:** `/checkpoint`: writes `memory-bank/active-context.md`.
- **Type:** `/compact keep the demo steps and results`
- **Say:** "Summaries lose detail, so state goes to files first. A follow-up after this is cheap
  because of prompt caching: the stable prefix is read from cache."

### 9. Wrap-up (30 s) — topics 13, 14
- **Say:** "Other tools express the same ideas differently (`docs/other-tools.md`). You don't copy
  `.cursor/`; you translate the intent and validate it. Value is measured per task
  (`docs/value-case.md`)."

---

## If something goes wrong
| Problem | Fix |
|---|---|
| `study-notes` not connected | `/mcp` → approve; check that `.venv\Scripts\python.exe` exists; `claude mcp get study-notes` |
| Hook not firing | `/hooks`; hooks run via Git Bash + `python` on PATH |
| A sub-agent fails in `/review-parallel` | that's the retry → escalate path; show the summary's "Retries" section |
| Eval flaky? | It can't be: BM25 is deterministic. The model's wording varies; the retrieval doesn't. |
