---
description: Orchestrate code-reviewer, test-writer and rag-evaluator in parallel, reconcile their hand-off files into .agent-handoff/summary.md
---
<!--
.claude/commands/review-parallel.md — WHY: multi-agent orchestration demo (topic 14, level A4)
and the fix for sub-agent limitations (topic 4). Three sub-agents run IN PARALLEL, each with
its own context window and least-privilege tools. They share nothing but files: the diff goes
in via .agent-handoff/diff.patch, and the results come out via .agent-handoff/*.md. The
orchestrator (this session) reconciles conflicts and handles failures.
-->

You are the orchestrator. Follow these steps exactly.

## 1. Prepare the inputs (you, not the sub-agents)
- Use the Write tool to reset `.agent-handoff/review.md`, `tests.md` and `eval.md` to the single
  line `PENDING`. This creates the folder and clears stale results; `rm` is denied in
  `.claude/settings.json`.
- Write the diff to review: `git diff HEAD > .agent-handoff/diff.patch`. If it's empty, use
  `git diff HEAD~1 HEAD > .agent-handoff/diff.patch` (the last commit) and say so.

## 2. Launch the sub-agents in parallel (a single message with three Agent calls)
| Agent | Prompt | Expected output |
|---|---|---|
| `code-reviewer` | "Review .agent-handoff/diff.patch against CLAUDE.md." | `.agent-handoff/review.md` |
| `test-writer` | "Add or extend tests for the code changed in .agent-handoff/diff.patch; run pytest." | `.agent-handoff/tests.md` |
| `rag-evaluator` | "Run the RAG eval and report." | `.agent-handoff/eval.md` |

## 3. Handle failures
- When all three have finished, check that each expected file no longer says `PENDING`.
- If one is missing or the agent reported an error: **retry that agent once** with the same
  prompt plus the error text.
- If it fails again: **stop and escalate to the user**: say which agent failed, the error, and
  what you have from the others. Don't invent the missing result.

## 4. Reconcile
Read all three hand-off files and look for conflicts, for example:
- the reviewer flags a bug that the test-writer's new test "confirms" (the test locks in the bug), or
- the reviewer asks for a change that would lower hit@3, or
- tests pass but the eval fails (or the other way round).

## 5. Write `.agent-handoff/summary.md`
- `## Result`: overall GO / NO-GO
- `## Review`: verdict and the top findings (with links to review.md)
- `## Tests`: tests added and the pytest result line
- `## Eval`: hit@3 and PASS/FAIL
- `## Conflicts and decisions`: how you resolved each conflict, or "none"
- `## Retries / escalations`: which agent was retried, if any

Reply with the Result line and the path to the summary. Don't apply any code changes yourself.
