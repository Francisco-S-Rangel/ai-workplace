---
name: add-knowledge-note
description: Add a new markdown note to the Study Buddy knowledge base (docs/knowledge/), rebuild the index, add an eval question for it, and run the tests. Use when the user wants to add, write, or import a study note or topic.
argument-hint: "[topic of the note]"
---
<!--
.claude/skills/add-knowledge-note/SKILL.md — WHY: a SKILL = a repeatable procedure (topic 9).
Only the name + description above sit in context all the time; this body loads only when the
task matches or the user types /add-knowledge-note (progressive disclosure = cheap context).
Compare: a CLAUDE.md rule is always loaded; a hook always runs; a sub-agent gets its own context.
-->

# Add a knowledge note

Topic: $ARGUMENTS

## Steps
1. **Check for overlap.** Use the `search_notes` MCP tool (or
   `.venv/Scripts/python.exe -m study_buddy.cli ask "<topic>"`). If an existing note already
   covers the topic, propose extending that note instead and ask the user.
2. **Write the note** at `docs/knowledge/<kebab-case-topic>.md`:
   - first an HTML header comment: `<!-- docs/knowledge/<file> — WHY: ... topic N -->`
   - 300–600 words, plain English
   - 3–6 `#` headings; each heading is a self-contained sub-topic, because chunking splits on
     headings and the heading becomes the citation (`file.md#Heading`)
   - facts only; if you're not sure of something, leave it out
3. **Rebuild the index:** `.venv/Scripts/python.exe -m study_buddy.cli ingest`
   (never edit `data/index.json` by hand; a hook blocks that anyway).
4. **Add one eval question** to `tests/eval/eval_set.jsonl`:
   `{"question": "...", "expected_source": "<file>.md"}`. Phrase it the way a user would ask,
   not by copying the heading.
5. **Run the tests:** `.venv/Scripts/python.exe -m pytest -q`. If the eval drops below the
   threshold, use the `rag-debug` skill; don't weaken the threshold.
6. Report: the file created, the chunk count from ingest, the new eval question, and the pytest result.
