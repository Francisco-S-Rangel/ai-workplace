<!--
docs/knowledge/claude-code-building-blocks.md — WHY: corpus note for the RAG demo that also
teaches topic 2 (project instructions, storage levels), topic 9 (rules vs skills vs
sub-agents vs hooks) and topic 10 (permissions, sandbox).
-->

# Project Instructions

In Claude Code, project instructions live in `CLAUDE.md`. It is loaded into every session,
so it should hold the purpose, commands, conventions, definition of done and a list of
things not to touch. It can import other files with `@path`. Nested `CLAUDE.md` files in
subfolders load when Claude works in those folders, which scopes rules to one area.

# Storage Levels and Priority

Settings and instructions exist at several levels: managed (enterprise policy set by IT),
user (`~/.claude/`), project (`.claude/` and `CLAUDE.md`, committed) and local
(`.claude/settings.local.json` and `CLAUDE.local.md`, not committed). For settings, managed
wins over everything, then command-line arguments, then local, then project, then user.
For permissions, a deny rule beats an allow rule.

# Rules versus Skills versus Sub-agents versus Hooks

- **Rules** (CLAUDE.md plus permissions) are always-on guidance. They cost context every
  turn and the model interprets them, so they are not guaranteed.
- **Skills** are folders with a `SKILL.md` that describe a repeatable procedure. Only the
  short description is loaded up front; the full body loads when the task matches. Use a
  skill for a workflow you repeat, like adding a note or debugging retrieval.
- **Sub-agents** are specialized agents with their own context window, system prompt and
  restricted tools. Use them to isolate a noisy task or to enforce least privilege, such as
  a read-only reviewer.
- **Hooks** are shell commands that run on events such as PreToolUse, PostToolUse and Stop.
  They are deterministic: the harness runs them, the model does not decide. Use hooks for
  things that must always happen, such as blocking access to secrets or formatting code.

# Permissions and Sandbox

Permissions in `settings.json` allow, ask or deny specific tools and patterns, such as
allowing `Bash(pytest:*)` and denying `Read(./secrets/**)`. Permission modes range from
asking every time to auto-accepting edits. A sandbox restricts file system and network
access for commands at the operating system level. Together with hooks, these are the
event-based access controls for repository resources.

# Plan Mode

Plan mode (Shift+Tab) lets the agent read and research but not edit. It produces a plan
for approval. Use it for multi-file features, unfamiliar code or risky changes. Skip it for
typo fixes, single-line changes and quick questions, where planning costs more than it saves.
