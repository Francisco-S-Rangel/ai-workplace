<!--
docs/concepts/ai-assisted-vs-ai-first.md — WHY: study page for the AI-Assisted vs AI-First
distinction (levels A3–A5, topic 14) with this repo as the example of an AI-First workflow.
-->

# AI-Assisted vs AI-First

| | AI-Assisted | AI-First |
|---|---|---|
| Who drives | the human; AI helps with steps (autocomplete, "explain this", one-off chat) | the process is designed around the agent; the human sets goals, reviews, steers |
| Unit of work | a snippet or answer | a task or feature (plan → implement → test → review) |
| Instructions | ad hoc prompts | versioned project instructions (`CLAUDE.md`), skills, commands |
| Quality control | the human reads the output | automated gates: tests, evals, hooks, reviewer agents, plus human review |
| Memory | in the human's head | on disk: memory bank, decision log, prompt log |
| Scaling | one chat at a time | sub-agents in parallel, repeatable workflows |
| Risk control | trust and eyeballing | permissions, hooks, least-privilege agents, sandbox |

## This repo as an AI-First example
1. **Planned first:** the build started in plan mode from a written spec (`docs/prompt-log.md` #1).
2. **Instructions as code:** `CLAUDE.md`, the nested rules, skills, and commands are in git.
3. **Gates:** 34 tests, including hook tests and the RAG eval. Ruff runs via a hook.
4. **Guardrails:** deny rules, the PreToolUse guard, and agents limited in where they can write.
5. **Memory:** memory bank + decision log; each phase committed.
6. **Orchestration:** `/review-parallel` runs 3 specialized agents and reconciles their results.

AI-First doesn't mean "no human". It means the human's time goes to **specifying,
reviewing, and deciding**, not typing.
