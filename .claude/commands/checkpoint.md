---
description: Save the current working state to memory-bank/active-context.md (run before /compact or /clear)
argument-hint: "[optional note]"
---
<!--
.claude/commands/checkpoint.md — WHY: explicit, controlled summarization (topic 5; topic 8).
/compact summarizes the chat automatically and loses detail; /clear forgets everything. This
command first writes the important state to a FILE (external memory) that the next session
reads. Different from Claude Code's built-in checkpoints (Esc Esc, /rewind), which undo edits.
(Custom commands still work in .claude/commands/; Claude Code now treats them like skills.)
-->

Update the memory bank so the working state survives /compact or /clear.

Extra note from the user (may be empty): $ARGUMENTS

1. Read `memory-bank/active-context.md` and `memory-bank/progress.md`.
2. Look at the current state: `git status` and `git diff --stat`.
3. Rewrite `memory-bank/active-context.md`, keeping its header comment, with these sections:
   - `_Last updated: <today's date>_`
   - **Current focus:** what we are doing right now (1–2 lines)
   - **Done this session:** bullets, including test results you actually ran
   - **Next step:** the single next concrete action
   - **Open questions / blockers**
   - **Watch out:** gotchas a fresh session must know
   Keep it under 25 lines. Facts only; write "not verified" for anything you didn't run.
4. If a milestone was completed, update its row in `memory-bank/progress.md`.
5. If a non-obvious decision was made, append an ADR entry to `memory-bank/decision-log.md`.
6. Reply with a 3-line summary and suggest: "/compact keep the decisions and next step" or /clear.
