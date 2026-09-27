<!--
docs/ASSESSMENT-MAP.md — WHY: the main study sheet. Each assessment question → a short answer
(plain words) → the file in this repo that proves it → what to show live.
NOTE: the questions are RECONSTRUCTED from the 14 assessment topics in the build plan; the
official wording may differ. Replace or extend them as needed.
-->

# Assessment map

Legend: **Proof** = a file to open · **Live** = what to do in Claude Code or the terminal.
`py` = `.venv\Scripts\python.exe`

## A1 — Foundations

| # | Question | Short answer | Proof | Live |
|---|---|---|---|---|
| 1 | What is the context / context window? | Everything the model sees on a turn (system prompt, instructions, tools, history, files, tool results). The window is its max size in tokens. There's no other memory. | `docs/concepts/context-and-lost-in-the-middle.md` | `/context` |
| 2 | What is "lost in the middle"? | Info in the middle of a long prompt is used less reliably than at the start or end. Keep instructions short, retrieve instead of dumping, restate the task last. | `docs/knowledge/context-window.md` | `py -m study_buddy.cli ask "what is lost in the middle?"` |
| 3 | Which prompting techniques do you use? | Goal + constraints · context first, question last · examples · plan first · fixed output format · grounding with citations · definition of done. | `docs/concepts/context-and-lost-in-the-middle.md`, `docs/prompt-log.md` | show prompt #1 in the prompt log |
| 4 | Agent vs LLM? | An LLM maps text to text. An agent is a loop around an LLM: goal → pick a tool → observe → repeat, with tools, permissions, memory and a stop condition. | `docs/knowledge/agents-and-orchestration.md` | watch Claude read, run and fix in a loop |
| 5 | Why is the same prompt answered differently? | Sampling · floating-point and batching effects · backend routing · a slightly different context. So verify with tests and evals. | `docs/concepts/non-determinism.md` | run a question twice |
| 6 | Why is a follow-up prompt almost free? | Prompt caching: the unchanged prefix (system, tools, CLAUDE.md, history) is read from cache cheaply; only the new message and output cost full price. Editing early context breaks the cache. | `docs/concepts/prompt-caching.md` | `/cost` before and after a short follow-up |

## A2 — Using the agent well

| # | Question | Short answer | Proof | Live |
|---|---|---|---|---|
| 7 | What is AGENTS.md / the project instructions file in your tool? | In Claude Code it's `CLAUDE.md`: loaded every session; purpose, commands, conventions, don't-touch list, definition of done. It supports `@imports` and nested files. | `CLAUDE.md`, `study_buddy/CLAUDE.md` | `/memory` |
| 8 | Where can instructions and settings be stored, and which wins? | Managed > CLI > local > project > user for settings. Permissions: deny → ask → allow. CLAUDE.md files are additive. | `docs/storage-levels.md` | `/status`, `/permissions` |
| 9 | How do you keep instructions modular without duplication? | `@path` imports and nested `CLAUDE.md` scoped to a folder; details in skills that load on demand. | `CLAUDE.md` (line `@memory-bank/project-brief.md`) | `/memory` |
| 10 | When do you use plan mode, and when not? | Use it for multi-file features, unfamiliar code, risky changes. Skip it for typos, one-liners, questions. It reads but can't edit until you approve. | `CLAUDE.md` → "Plan mode policy" | Shift+Tab, then ask for a small feature |
| 11 | How do you monitor the context? | `/context` (by category), `/cost`. Watch for tool-output bloat and many MCP tools. | `docs/concepts/compaction.md` | `/context` |
| 12 | What compaction / summarization types exist? | Auto-compaction · manual `/compact <what to keep>` · truncation / sliding window · hierarchical summaries · external memory (files). Summaries lose detail, so save to files first. | `docs/concepts/compaction.md` | `/checkpoint`, then `/compact keep decisions` |
| 13 | What are checkpoints? | Automatic snapshots of edits. `Esc Esc` or `/rewind` restores the conversation and/or code. Local undo, not a replacement for git. | `docs/concepts/compaction.md` | make an edit, then `/rewind` |
| 14 | Chat management vs export? | `/clear`, `/compact`, `/resume` manage the working context. `/export` writes a record for humans. The memory bank is curated state for the agent. | `docs/concepts/compaction.md` | `/export` |

## A3 — Configuring the agent

| # | Question | Short answer | Proof | Live |
|---|---|---|---|---|
| 15 | Rules vs skills vs sub-agents vs hooks? | Rules = always-on guidance (interpreted). Skills = procedures loaded on demand. Sub-agents = separate context and restricted tools. Hooks = deterministic scripts on events. | `docs/hooks-vs-rules-vs-skills-vs-subagents.md` | open the table |
| 16 | Show a skill. | `SKILL.md` with `name` + `description`. Only the description is in context until it triggers. It can ship scripts. | `.claude/skills/rag-debug/` (+ `scripts/inspect_chunks.py`) | `/rag-debug "chunking overlap"` |
| 17 | Agent vs sub-agent; what are the built-in limitations? | A sub-agent has its own context window, doesn't see the parent chat, returns only a summary, and has no shared memory. | `.claude/agents/*.md` (header comments) | "Which sub-agents are available?" |
| 18 | How do you overcome them? | Hand-off via files: inputs go in via `.agent-handoff/diff.patch`, full results come out via `.agent-handoff/*.md`, and the parent reads the files. | `.claude/commands/review-parallel.md` | `/review-parallel`, then open `.agent-handoff/` |
| 19 | How do you control access to repo resources? | Defense in depth: permission deny rules + a PreToolUse hook (exit 2) + agent-scoped write limits + optional sandbox + human review. | `.claude/settings.json`, `.claude/hooks/guard_paths.py` | "read secrets/api_key.txt" → blocked |
| 20 | Why a hook if you already have deny rules? | Deny rules don't see everything (e.g. `grep -r`, PowerShell variants). A hook inspects the full command. Hooks always run; the model doesn't decide. | `tests/test_hooks.py`, the decision log | "grep -r FAKE in the secrets folder" → hook message |
| 21 | What is MCP, and how is it configured? | A protocol exposing tools, resources and prompts from a server. Configured in `.mcp.json` (project) or with `claude mcp add --scope`. | `.mcp.json`, `mcp_server/server.py`, `docs/mcp.md` | `/mcp` |
| 22 | How do you retrieve the full list of capabilities of an MCP server? | `/mcp` · `claude mcp list` · ask the agent · protocol `tools/list` via an SDK `list_tools()`. | `scripts/list_mcp_tools.py` | `py scripts/list_mcp_tools.py` |
| 23 | MCP risks and mitigations? | Over-permissioned servers · prompt injection via output · secrets in config · context bloat · stale data → read-only tools, allow/deny `mcp__…`, tool output = data, env vars, few servers. | `docs/mcp.md`, `docs/knowledge/mcp-overview.md` (injection line) | `/ask-notes what does the prompt injection example say?` |
| 24 | What is RAG, and why not dump the whole doc? | Retrieve the top-k relevant chunks, then answer from them with citations. Cheaper, fits the window, avoids lost-in-the-middle, verifiable. | `docs/knowledge/rag-basics.md`, `study_buddy/` | `py -m study_buddy.cli ask "why is RAG better…"` |
| 25 | How do you chunk? | Split by heading, then by size with overlap. Keep metadata (source, heading, id). Tune size and overlap with evals. | `study_buddy/ingest.py`, `tests/test_chunking.py` | `py .claude/skills/rag-debug/scripts/inspect_chunks.py --source rag-basics.md` |
| 26 | How do you measure retrieval quality? | An eval set of question → expected source; hit@k / recall; a threshold in CI. BM25 here; hybrid + reranker in production. | `tests/test_rag_eval.py`, `tests/eval/eval_set.jsonl` | `py -m pytest tests/test_rag_eval.py -s` |
| 27 | What is a Memory Bank? | Markdown files the agent reads at start and updates at the end: brief, active context, progress, decision log. External memory that survives compaction. | `memory-bank/`, the CLAUDE.md protocol | `/checkpoint` |
| 28 | How do you reduce hallucinations? | Individually: grounding, citations, "not found", run it, check the docs. As a team: tests and evals in CI, reviewer agents, shared instructions, decision logs, guardrails. | `docs/concepts/hallucination-reduction.md`, `.claude/commands/ask-notes.md` | `/ask-notes what is the capital of France?` → "Not found in notes." |

## A4 — Orchestration and quality at scale

| # | Question | Short answer | Proof | Live |
|---|---|---|---|---|
| 29 | How do you orchestrate multiple agents in parallel? | Split into independent tasks; one agent per task with least-privilege tools; launch them in parallel; each writes a hand-off file; the orchestrator reconciles. | `.claude/commands/review-parallel.md`, `.claude/agents/` | `/review-parallel` → `.agent-handoff/summary.md` |
| 30 | How do you handle failures and conflicts between agents? | Check outputs exist; retry once with the error, then escalate to a human; never invent the missing result. Resolve conflicts explicitly (e.g. a test that locks in a bug) and log them in the summary. | `.claude/commands/review-parallel.md` §3–4 | read the summary's "Conflicts" section |
| 31 | How do automated evals detect regressions? | A fixed eval set plus a metric plus a threshold in the test suite: a change to chunking or BM25 that drops hit@3 below 0.8 fails `pytest`. | `tests/test_rag_eval.py` | ask Claude to change `reverse=True` → `reverse=False` in `study_buddy/retrieve.py`, run pytest (hit@3 drops from 1.0 to 0.6 → FAIL), then `Esc Esc` / `/rewind` to undo. (BM25 is robust to chunk size on this small corpus: hit@3 stays at 0.9–1.0 from 4 to 2000 words, so a parameter tweak won't show a failure.) |
| 32 | Same concepts in Cursor / Kimi / Qwen: can you copy `.cursor/` over? | No. Copy the intent, translate the format (`.mdc` → CLAUDE.md or a skill; `.cursor/mcp.json` → `.mcp.json`; `hooks.json` → settings hooks), then validate the behavior. | `docs/other-tools.md` | open the translation table |
| 33 | AI-Assisted vs AI-First? | Assisted: the human drives, AI helps with steps. First: the process is designed around the agent (instructions, evals, guardrails) and the human specifies and reviews. | `docs/concepts/ai-assisted-vs-ai-first.md` | show `docs/prompt-log.md` + git log |

## A5 — Value

| # | Question | Short answer | Proof | Live |
|---|---|---|---|---|
| 34 | How do you justify AI adoption? | Per task: frequency, time before and after (including review), token cost, a quality metric, risk, setup cost → payback. Start with frequent, well-specified tasks. | `docs/value-case.md`, `docs/levels.md` | walk through the example (it's marked illustrative) |

---

## Claude Code commands to know

| Command / key | What it does |
|---|---|
| `Shift+Tab` | cycle permission modes, including **plan mode** |
| `/context` | context window usage by category |
| `/compact [instructions]` | summarize history, keeping what you specify |
| `/clear` | start a fresh context |
| `/rewind` or `Esc Esc` | restore a checkpoint (conversation and/or code) |
| `/resume` | continue a previous session |
| `/export` | export the conversation |
| `/mcp` | MCP servers, status, tools; approve project servers |
| `/agents` | **removed in recent versions**: ask "which sub-agents are available?", type `@`, or use `/tasks` |
| `/hooks` | view the registered hooks |
| `/memory` | open or edit the loaded CLAUDE.md files |
| `/permissions` | view or edit allow/ask/deny rules |
| `/status` | version, model, setting sources |
| `/cost` | token usage and cost |
| `/model` | switch model |
| `/init` | generate a starter CLAUDE.md for a repo |
| `/skills` | list skills |
| `claude mcp list / add / get` | manage MCP servers from the terminal |
