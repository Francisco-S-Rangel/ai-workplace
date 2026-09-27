<!--
docs/knowledge/context-management.md — WHY: corpus note for the RAG demo (topic 7) that also
teaches topic 5 (context management, compaction, checkpoints) and topic 8 (memory bank).
-->

# Monitoring the Context

In Claude Code the `/context` command shows how the context window is being used: system
prompt, tools, MCP tool definitions, memory files and messages. `/cost` shows token usage
and spend for the session. Watching these numbers tells you when a session is getting
heavy and when many MCP servers are eating context with tool definitions nobody uses.

# Compaction and Summarization Types

When a conversation grows too large, something has to give. Common strategies:

- **Auto-compaction:** the tool summarizes the older conversation automatically when the
  window is nearly full. Claude Code does this and also offers manual `/compact`, which
  accepts instructions such as `/compact keep the decisions about chunking`.
- **Truncation / sliding window:** drop the oldest turns and keep the most recent ones.
  Cheap, but it silently forgets early decisions.
- **Selective or hierarchical summarization:** summarize old parts in layers, keeping more
  detail for recent or important parts and less for the rest.
- **External memory:** write the important state to files (a memory bank, a progress log,
  a decision log) and reload it when needed. This survives any compaction because it lives
  on disk, not in the chat.

Summaries lose detail. That is why you write decisions to files before compacting.

# Checkpoints

Claude Code takes checkpoints of file edits as it works. Pressing Esc twice or running
`/rewind` lets you go back to an earlier point in the conversation, the code, or both.
Checkpoints are a local undo for agent edits; they do not replace git. Commit after each
working step so you have a durable safety net.

# Chat Management versus Export

Chat management means `/clear` to start fresh, `/compact` to shrink, and `/resume` to
continue an earlier session. Export (`/export`) writes the conversation to a file or the
clipboard so a human can read or share it. Exported chats are records; the memory bank is
the curated state that the agent is meant to reload.

# Memory Bank

A memory bank is a small folder of markdown files the agent reads at the start of a
session and updates at the end: a project brief, the active context, progress, and a
decision log. It turns the agent from stateless into stateful across sessions without any
special infrastructure. Claude Code also has built-in memory: CLAUDE.md files at several
levels and the `/memory` command to edit them.
