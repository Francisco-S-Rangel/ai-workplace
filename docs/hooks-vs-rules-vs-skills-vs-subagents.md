<!--
docs/hooks-vs-rules-vs-skills-vs-subagents.md — WHY: the decision table for topic 9
("when do you use a rule vs a skill vs a sub-agent vs a hook?") and topic 10 (access control),
with a real example from this repo for every cell.
-->

# Rules vs Skills vs Sub-agents vs Hooks (vs Commands, MCP)

In Claude Code terms, **"Rules" = `CLAUDE.md` files + `permissions` in `settings.json`**.
(Cursor calls its equivalent `.cursor/rules/*.mdc`; see `docs/other-tools.md`.)

## Decision table

| | Rules (`CLAUDE.md`) | Permissions (`settings.json`) | Skill (`.claude/skills/*/SKILL.md`) | Sub-agent (`.claude/agents/*.md`) | Hook (`settings.json` → script) | Slash command (`.claude/commands/*.md`) |
|---|---|---|---|---|---|---|
| **Trigger** | always loaded at session start (nested files load when their folder is used) | every tool call is checked | Claude matches the description to the task, or you type `/name` | Claude delegates (description match) or you ask for it | an event: PreToolUse, PostToolUse, Stop, … | you type `/name` |
| **Who decides** | the model interprets them | the harness | the model (or you) | the model (or you) | **the harness: always runs** | you |
| **Deterministic?** | no: guidance can be ignored or forgotten | yes: allow/ask/deny | no | no | **yes** | the prompt is fixed; the result isn't |
| **Context cost** | every turn, full text | ~0 | description always; body only when used | its own separate context window; the parent pays only for the summary | 0 (runs outside the model); only its output is added | only when invoked |
| **Scope** | managed / user / project / local / nested folder | managed / user / project / local | user / project | user / project / CLI | managed / user / project / local / per agent | user / project |
| **Best for** | conventions, commands, definition of done, "don't touch" lists | hard allow/deny of tools and paths | repeatable multi-step procedures, plus bundled scripts | isolating noisy work, least privilege, parallelism | things that MUST happen or MUST NOT: blocking, formatting, reminders | your own shortcuts for prompts you reuse |
| **Example here** | `CLAUDE.md`, `study_buddy/CLAUDE.md` (pure-Python BM25) | deny `Read(./secrets/**)`, `Edit(./data/index.json)`, `Bash(git push *)` | `add-knowledge-note`, `rag-debug` (+ `scripts/inspect_chunks.py`) | `code-reviewer` (read-only), `test-writer` (writes only under `tests/`), `rag-evaluator` (haiku) | `guard_paths.py`, `format_python.py`, `remind_memory_bank.py`, `restrict_writes.py` | `/checkpoint`, `/review-parallel`, `/ask-notes` |

## Rules of thumb
- If it **must** happen every time → **hook**, not a CLAUDE.md sentence.
  ("Format Python after edits" is a hook; "prefer small functions" is a rule.)
- If it's a **hard boundary** on a tool or path → a **permission deny**, backed by a **hook** for
  cases the rule can't see (e.g. `grep -r KEY .`).
- If it's a **procedure** with steps you repeat → **skill**. It costs almost no context until used.
- If the work is **noisy, parallel, or needs fewer privileges** → **sub-agent**, with results
  handed off through files, because it returns only a summary.
- If it's **knowledge everyone needs every time** → **CLAUDE.md**, kept short (lost in the middle).
- If it's **external data or tools** → **MCP server**, read-only if possible.

## Access control in this repo: defense in depth

| Layer | What it does | Demo |
|---|---|---|
| Permission deny | blocks `Read`/`Edit` on `secrets/**` and `.env`, recognized `cat`-style Bash reads, and `Edit` of `data/index.json` | "read secrets/api_key.txt" → *denied by your permission settings* |
| PreToolUse hook | inspects the full command text and paths, including PowerShell and `grep -r` | `grep -r FAKE secrets` → `[guard_paths hook] … blocked`, exit 2 |
| Agent-scoped hook | narrows Write for sub-agents | `code-reviewer` writing `study_buddy/x.py` → `[restrict_writes hook]` |
| Sandbox (optional) | OS-level limits on files and network for Bash/PowerShell commands | not enabled here (verify Windows support in the sandboxing docs) |
| Human review | permission prompts, plan mode, `/review-parallel` summary | — |

## Verified facts (checked against the docs on 2026-09-27; see memory-bank/decision-log.md)
- PreToolUse **exit code 2 blocks** the call, and stderr is shown to Claude. On PostToolUse,
  exit 2 can't undo the call. On Stop, exit 2 keeps Claude working.
- Path rules only work for `Read(...)` and `Edit(...)`. A `Write(path)` rule is accepted but
  **never consulted**, so `Edit(./data/index.json)` also covers writes.
- Deny, then ask, then allow: the first match in that order wins.
- On Windows, hook commands run through Git Bash when it's installed, otherwise PowerShell.
