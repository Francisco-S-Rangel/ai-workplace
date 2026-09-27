---
name: rag-debug
description: Diagnose bad or missing retrieval results in the Study Buddy RAG - inspect chunks, tune chunk_size / overlap / top_k, re-run the eval, and log the decision. Use when a question returns the wrong source, "Not found in notes", or when the RAG eval (hit@3) fails.
argument-hint: "[the question that retrieves badly]"
---
<!--
.claude/skills/rag-debug/SKILL.md — WHY: a skill that SHIPS A SCRIPT (topic 9) and teaches
retrieval-quality debugging (topic 7). The helper scripts/inspect_chunks.py lives inside the
skill folder, so the procedure and its tooling travel together.
-->

# Debug retrieval

Problem question: $ARGUMENTS

## 1. Reproduce
- `.venv/Scripts/python.exe -m study_buddy.cli ask "$ARGUMENTS" --top-k 5`
- Note the citations and scores. Which source did you expect?

## 2. Inspect the chunks
Run the bundled helper:
`.venv/Scripts/python.exe .claude/skills/rag-debug/scripts/inspect_chunks.py --source <expected-file.md>`
Optional: `--chunk-size 80 --overlap 10` previews other parameters without touching the index,
and `--query "..."` shows how each query token matches (idf, and which chunks contain it).

Typical causes:
| Symptom | Likely cause | Fix |
|---|---|---|
| Right file, wrong section | chunks too large, diluted | smaller `chunk_size` |
| Answer split across two chunks | cut at a boundary | more `overlap` |
| Query words not in the note | vocabulary mismatch (BM25 is lexical) | reword the note / add synonyms to it; note that production would use hybrid dense retrieval |
| Right chunk at rank 4–5 | `top_k` too small | raise `top_k` (costs context) |

## 3. Change one thing, then measure
- Try the new parameters: `.venv/Scripts/python.exe -m study_buddy.cli ingest --chunk-size N --overlap M`
- Run the eval: `.venv/Scripts/python.exe -m pytest tests/test_rag_eval.py -q -s`
- Keep the change only if hit@3 stays >= the threshold AND the problem question improves.
  If you change the defaults, change them in `study_buddy/index.py` and `cli.py` together.

## 4. Record it
- Add an ADR entry to `memory-bank/decision-log.md` (date, decision, alternatives, why, hit@3 before/after).
- Add the problem question to `tests/eval/eval_set.jsonl` so it can't regress silently.
