<!--
docs/concepts/compaction.md — WHY: study page for topic 5 (context management: monitoring,
compaction/summarization types, checkpoints, chat management vs export).
-->

# Context management and compaction

## Monitor
- `/context`: what's using the window (system, tools, MCP, memory files, messages).
- `/cost`: tokens and spend for the session.
- Signals that it's time to act: the conversation changes topic; long tool outputs pile up;
  the model starts forgetting early decisions.

## Compaction and summarization types
| Type | How it works | Pro | Con | In Claude Code |
|---|---|---|---|---|
| **Auto-compaction** | the tool summarizes older turns when the window is nearly full | hands-off | you don't choose what's kept | automatic (buffer shown in `/context`) |
| **Manual compaction with instructions** | you trigger the summary and say what to keep | control | still lossy | `/compact keep the chunking decisions and next step` |
| **Truncation / sliding window** | drop the oldest turns | cheap and predictable | silently forgets early decisions | (used by many simple chat systems) |
| **Selective / hierarchical summarization** | summarize in layers, with more detail for recent or important parts | keeps structure | more complex | (a pattern; partly what `/compact` does) |
| **External memory** | write state to files and reload it | survives everything; reviewable; shareable | needs discipline | memory bank + `/checkpoint` + Stop hook reminder |

**Rule:** summaries lose detail, so write decisions to a file **before** compacting.
This repo: `/checkpoint` → `memory-bank/active-context.md`, and the `remind_memory_bank.py`
Stop hook nudges you when you forget.

## Checkpoints (undo) vs checkpoint (save state)
- **Claude Code checkpoints:** automatic snapshots of file edits. `Esc Esc` or `/rewind` goes back
  in the conversation, the code, or both. They're local and short-lived; **git is still the
  real safety net** (this repo commits after every phase).
- **`/checkpoint` (this repo's command):** saves the *working state* (focus, next step,
  gotchas) to the memory bank.

## Chat management vs export
| Action | What it does | Use when |
|---|---|---|
| `/clear` | new empty context (the memory bank on disk stays) | switching tasks |
| `/compact [instructions]` | replaces history with a summary | same task, window getting full |
| `/resume` | reopen an earlier session | continue yesterday's work |
| `/export` | write the conversation to a file or the clipboard | share or audit a session (a record, not memory) |
| Memory bank | curated state the agent reloads | continuity across sessions and people |
