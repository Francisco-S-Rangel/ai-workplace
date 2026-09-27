<!--
docs/storage-levels.md — WHY: topic 2 (project instructions + storage levels + priority).
Answers "where can instructions/settings live, who sees them, and which one wins?" for Claude
Code, using the files in this repo as examples. Also documents .claude/settings.json, which
can't carry a header comment because it's JSON.
Facts checked against code.claude.com/docs (settings, permissions, sub-agents, skills) on
2026-09-27; anything not confirmed is marked "verify in docs".
-->

# Claude Code storage levels

## The four levels

| Level | Settings | Instructions (memory) | Agents / skills / commands | MCP servers | Shared? | In this repo |
|---|---|---|---|---|---|---|
| **Managed** (organization / IT policy) | `managed-settings.json` in a system directory, MDM policy, or server-managed settings from the claude.ai admin console | a managed `CLAUDE.md` in the system directory (verify in docs) | managed agents have the highest priority | managed MCP config (verify in docs) | everyone the org deploys it to; **can't be overridden** | — (none on this machine) |
| **User** (you, every project) | `~/.claude/settings.json` | `~/.claude/CLAUDE.md` | `~/.claude/agents/`, `~/.claude/skills/`, `~/.claude/commands/` | `claude mcp add --scope user` | only you | — |
| **Project** (team, committed to git) | `.claude/settings.json` | `CLAUDE.md` (root) + nested `study_buddy/CLAUDE.md`; `@path` imports | `.claude/agents/`, `.claude/skills/`, `.claude/commands/` | `.mcp.json` (`--scope project`) | everyone who clones the repo | ✅ all of these |
| **Local** (you, this project, NOT committed) | `.claude/settings.local.json` | `CLAUDE.local.md` | — | `claude mcp add --scope local` (the default scope; stored in your user config) | only you, only here | `*.example` files; real ones are gitignored |

Plus two session-only sources: **command-line** flags (`claude --settings …`, `--model`,
`--agents '{json}'`) and, for sub-agents, the `--agents` flag.

## Which one wins?

**Settings precedence (highest first):**

```
1. Managed      managed-settings.json / MDM / claude.ai console   (nothing overrides it)
2. Command line claude --settings …, --model …                     (this session only)
3. Local        .claude/settings.local.json                        (you, this project)
4. Project      .claude/settings.json                              (the team)
5. User         ~/.claude/settings.json                            (you, every project)
```

- A **scalar** key (e.g. `model`) comes from the highest level that sets it.
- **Array** keys such as `permissions.allow` / `permissions.deny` are **merged** across levels.
- **Permissions:** rules are evaluated **deny → ask → allow**. The first match in that order
  wins, so a deny anywhere beats an allow anywhere. A project can't "un-deny" something that
  a managed policy denies.
- A few security-sensitive keys keep the *stricter* value from any level (see "exceptions to
  managed settings precedence" in the settings docs).

**Instructions (`CLAUDE.md`) are additive, not "winner takes all":** managed, user, project,
nested and local files are all loaded into context together. If two files contradict each
other the model has to reconcile them, so avoid contradictions. The exact order in which
they're loaded is: verify in docs (memory page).

**Sub-agent priority when names collide:** managed > `--agents` CLI flag > project
`.claude/agents/` > user `~/.claude/agents/` > plugin agents.

## How to see what's active
- `/status` lists the setting sources in effect (including a managed policy, if one applies).
- `/permissions` shows the allow/ask/deny rules and where each comes from.
- `/memory` opens the loaded `CLAUDE.md` files.
- `/hooks` shows the registered hooks. `/mcp` shows the servers.
- Sub-agents: ask "which sub-agents are available?" or type `@`; `/tasks` shows running
  ones. (The `/agents` wizard was removed in recent versions.)

## What each file in this repo is for

| File | Level | Purpose |
|---|---|---|
| `CLAUDE.md` | project | always-loaded instructions; imports `@memory-bank/project-brief.md` |
| `study_buddy/CLAUDE.md` | project (nested) | loads when working in `study_buddy/` (pure-Python BM25 rule) |
| `CLAUDE.local.md.example` | local (template) | copy to `CLAUDE.local.md` for personal notes (gitignored) |
| `.claude/settings.json` | project | permissions (allow test/lint/CLI/`mcp__study-notes__*`; deny the protected folder, `.env`, index edits, `git push`, `rm`) and hook registrations |
| `.claude/settings.local.json.example` | local (template) | personal extras, e.g. `enabledMcpjsonServers: ["study-notes"]` to auto-approve the project MCP server |
| `.mcp.json` | project | the `study-notes` MCP server |
| `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`, `.claude/commands/*.md` | project | sub-agents, skills, commands |

## MCP scopes (a separate axis)
| Scope | Stored in | Visible to |
|---|---|---|
| `local` (default) | your user config, keyed to this project | you, this project |
| `project` | `.mcp.json` | everyone who clones the repo, after they approve it |
| `user` | your user config | you, all projects |
