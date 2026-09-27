<!--
docs/levels.md — WHY: self-assessment against levels A0–A5, with evidence from this repo.
NOTE: the one-line level descriptions are MY INTERPRETATION of the assessment's scale, reconstructed
from the topics it covers. Replace them with the official wording if you have it.
-->

# Levels A0–A5: where this repo puts me

| Level | One line (my interpretation) |
|---|---|
| **A0** | Doesn't use AI tools for work. |
| **A1** | Uses chat assistants ad hoc: asks questions, copies answers. Knows basic prompting. |
| **A2** | Uses an agent in the IDE/CLI deliberately: gives context, uses project instructions, plan mode, understands the context window and lost in the middle. |
| **A3** | Configures the agent for the team: instruction files at the right storage level, skills, sub-agents, hooks, permissions, MCP, RAG, memory bank; reduces hallucinations with grounding and tests. |
| **A4** | Orchestrates: multiple agents in parallel with hand-offs and failure handling; automated evals that detect regressions; AI-first workflows others can reuse. |
| **A5** | Drives adoption: measures value/ROI, sets guardrails and standards across teams, decides where AI should *not* be used. |

## Where I am: solid A3, with A4 evidence
**A2 evidence**
- `CLAUDE.md` with commands, conventions, definition of done, plan-mode policy.
- Built the repo in plan mode, phase by phase (`docs/prompt-log.md`).
- `docs/concepts/context-and-lost-in-the-middle.md`; I use `/context`, `/compact`, `/rewind`.

**A3 evidence**
- Storage levels in practice: project + nested + local templates (`docs/storage-levels.md`).
- 2 skills (one ships a script), 3 least-privilege sub-agents, 4 hooks, 3 commands.
- A custom MCP server with read-only tools + a script that lists its capabilities.
- Local RAG with chunking, BM25, citations; hallucination-reduction practices.
- Access control that I tested: deny rules + a PreToolUse hook, verified live and in `tests/test_hooks.py`.

**A4 evidence**
- `/review-parallel`: 3 sub-agents in parallel, hand-off via `.agent-handoff/*.md`, retry once,
  then escalate, and conflict reconciliation.
- `tests/test_rag_eval.py`: an automated eval with a threshold; a regression fails the build.
- The model is chosen per agent (haiku for the mechanical evaluator), a cost-aware design.

## A5 (one paragraph)
A5 is about organizational value, not tooling. It means picking the workflows where agents pay
off, measuring them (time, cost, quality, risk; see `docs/value-case.md`), and standardizing what
works as shared templates (like this repo's `.claude/` folder), with guardrails that security
signs off on (managed settings, deny rules, hooks). It also means saying **no** where the risk
or verification cost exceeds the gain. My next step toward A5 would be running the value-case
template on 2–3 real team tasks and turning this repo's config into a team template.
