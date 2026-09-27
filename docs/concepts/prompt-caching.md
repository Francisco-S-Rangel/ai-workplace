<!--
docs/concepts/prompt-caching.md — WHY: study page for topic 12 (prompt caching: why a follow-up
prompt is almost free).
-->

# Prompt caching

## How it works
Every request re-sends the whole context: system prompt, tool definitions, CLAUDE.md, and
the chat history. The provider **caches the processed prefix**. If the next request starts with
the same bytes, those tokens are read from cache at a small fraction of the normal input price,
and faster. Only the **new** part (your new message and the model's output) is paid at full price.

```
Turn 1: [system][tools][CLAUDE.md][msg1]              → all written to cache
Turn 2: [system][tools][CLAUDE.md][msg1][reply1][msg2] → prefix read from cache, only msg2 + output are new
```

## Why a follow-up prompt is almost free
The 50–100k tokens of setup (tools, instructions, history) are a cache **hit** on the follow-up.
You pay full price for a few hundred new tokens plus the cheap cache reads.

## What breaks the cache
- Changing something **early** in the prompt: editing CLAUDE.md, adding or removing an MCP server
  or tool, switching model. Everything after the change is reprocessed.
- **Time:** caches expire after a period of inactivity (the TTL; commonly minutes, sometimes an
  hour; it depends on the provider and settings).
- `/clear` or a new session: a new prefix.

## Practical consequences
- Keep stable things (instructions, tools) **first** and stable; put changing things last.
- Don't fiddle with CLAUDE.md mid-task; batch edits.
- Many small follow-ups in one session are cheap; restarting sessions often isn't.
- Compaction rewrites the history, so the next turn re-caches the new summary (a one-time cost).
