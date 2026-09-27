<!--
docs/concepts/context-and-lost-in-the-middle.md — WHY: study page for topic 1 (prompting,
context, context window, lost in the middle). Short answers for the assessment and pointers to
where this repo applies each idea.
-->

# Context, context window, lost in the middle

## In one breath
**Context** = everything the model sees on a turn (system prompt, CLAUDE.md, tool definitions,
chat history, file contents, tool results). The **context window** is its maximum size in
tokens. The model has no other memory: if it's not in the context, it isn't known.

## What fills the window in Claude Code
Run `/context`. In this session it showed roughly: system prompt ~4k, system tools ~23k,
skills ~5k, messages ~63k of 1M tokens, with MCP tools "loaded on-demand" (deferred). The
auto-compact buffer is reserved at the end.

## Lost in the middle
Long-context models use information at the **start** and **end** of the prompt more reliably
than information in the **middle**. The more you add, the more likely the key fact is buried.

What to do (and where this repo does it):
| Practice | In this repo |
|---|---|
| Put important rules first, keep them short | `CLAUDE.md` ≲ 120 lines; details moved to `@imports` and a nested `study_buddy/CLAUDE.md` |
| Put only relevant text in the prompt (retrieve, don't dump) | RAG: `search_notes` returns the top 3 chunks, not whole files |
| Restate the concrete task at the end | slash commands end with the exact output format |
| Clear old turns | `/checkpoint` → `/compact` or `/clear` |
| Load detail only when needed | skills load their body only when triggered |

## Prompting techniques (checklist)
1. **Goal + role:** what outcome, from whose perspective.
2. **Context first, question last.**
3. **Constraints:** "no new dependencies", "only edit tests/".
4. **Examples (few-shot)** for format.
5. **Plan first** for multi-file work (plan mode).
6. **Output format** you can check (table, JSON, template).
7. **Grounding:** "answer only from the sources, cite them, else say not found" (`/ask-notes`).
8. **Definition of done:** "tests + ruff pass" (CLAUDE.md).

The prompt that built this repo is a worked example: `docs/prompt-log.md`, entry 1.
