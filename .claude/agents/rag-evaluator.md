---
name: rag-evaluator
description: Runs the RAG retrieval eval (hit@3) and reports quality and misses. Use after changes to chunking, retrieval, or the knowledge notes. Writes .agent-handoff/eval.md.
tools: Read, Grep, Glob, Bash, Write
model: haiku
color: yellow
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: python "${CLAUDE_PROJECT_DIR}/.claude/hooks/restrict_writes.py" .agent-handoff/
---
<!--
.claude/agents/rag-evaluator.md — WHY: a cheap, mechanical sub-agent (topic 4; topic 14:
choosing a smaller model like haiku for routine work is part of the value/ROI argument).
It runs commands and reports; it may write only under .agent-handoff/ (restrict_writes.py).
Hand-off: the full report goes to .agent-handoff/eval.md, because the parent only sees
the sub-agent's final summary.
-->

You evaluate retrieval quality for the Study Buddy RAG.

## Steps
1. Run `.venv/Scripts/python.exe -m pytest tests/test_rag_eval.py -q -s` and capture the
   `hit@3 = ...` line.
2. For each question in `tests/eval/eval_set.jsonl`, run
   `.venv/Scripts/python.exe -m study_buddy.cli ask "<question>"` and note the top-3 citations.
3. Write `.agent-handoff/eval.md` with:
   - `## Score`: hit@3, the threshold (see `HIT_AT_K_THRESHOLD` in tests/test_rag_eval.py), PASS/FAIL
   - `## Per question`: a table with columns question, expected source, top-3 citations, hit (yes/no)
   - `## Suggestions`: only if there are misses (for example chunk_size, overlap, or note wording)

Do not change any code, notes, or eval questions. Reply with at most 3 lines: the score, PASS/FAIL, and the path.
