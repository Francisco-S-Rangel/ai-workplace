<!--
docs/other-tools.md — WHY: topic 13 ("same concepts, different templates"). The assessment was
written with Cursor / Kimi / Qwen in mind; this page maps each concept to the file or command
each tool uses, so I can explain the differences. DOCUMENTATION ONLY: this repo deliberately
contains no .cursor/, AGENTS.md, QWEN.md, .qwen/ or .kimi/ files.
Sources (fetched 2026-09-27): cursor.com/docs (rules, hooks, MCP), qwenlm.github.io/qwen-code-docs
(settings, commands), github.com/MoonshotAI/kimi-cli (archived 2026-09-23 in favor of "Kimi Code CLI").
Cells marked "verify in docs" were NOT confirmed; don't quote them as fact.
-->

# Same concepts, different templates

| Concept | **Claude Code (this repo)** | **Cursor** | **Kimi CLI** | **Qwen Code** |
|---|---|---|---|---|
| Project instructions | `CLAUDE.md` (root + nested), `@path` imports | `.cursor/rules/*.mdc` **or** `AGENTS.md` (root + nested) | `AGENTS.md` | `QWEN.md` by default (configurable via `context.fileName`, which can also point to `AGENTS.md`) — verify the default name in docs |
| Rules with scoping | nested `CLAUDE.md`; permissions in `settings.json` | `.mdc` frontmatter: `description`, `globs`, `alwaysApply` → Always / Apply Intelligently / Apply to Specific Files / Manual (@-mention). User Rules (settings) and Team Rules (dashboard) | verify in docs | context files per folder — verify in docs |
| Legacy format | — | `.cursorrules` (legacy; superseded by `.cursor/rules`) — verify current status | — | commands in `.toml` (deprecated → `.md`) |
| Skills | `.claude/skills/<name>/SKILL.md` | verify in docs | a `.agents/skills/` folder exists in the repo — verify it's the user-facing format | `.qwen/skills/<name>/SKILL.md` |
| Sub-agents | `.claude/agents/*.md` (frontmatter `name`, `description`, `tools`, `model`, `hooks`) | verify in docs (hooks list `subagentStart/Stop` events) | verify in docs | supported (`/agents manage`, `/coordinator`); file location: verify in docs |
| Custom slash commands | `.claude/commands/*.md` (now treated like skills), `$ARGUMENTS` | `.cursor/commands/` — verify in docs | verify in docs | `.qwen/commands/*.md` (project) and `~/.qwen/commands/`; `{{args}}`, `!{cmd}`, `@{path}`; subfolders → `/git:commit` |
| Hooks | `settings.json` → `hooks` (PreToolUse, PostToolUse, Stop, …); exit 2 blocks | `.cursor/hooks.json` (project), `~/.cursor/hooks.json`, enterprise path; events such as `beforeShellExecution`, `beforeReadFile`, `afterFileEdit`, `preToolUse`, `stop`; **exit 2 blocks** | verify in docs | supported (`/hooks`); config format: verify in docs |
| MCP config file | `.mcp.json` (project) + `claude mcp add --scope local/project/user` | `.cursor/mcp.json` (project), `~/.cursor/mcp.json` (global), key `mcpServers` | `kimi mcp add / list / remove / auth`; `--mcp-config-file` (standard JSON format) | `mcpServers` key in `settings.json` |
| See MCP capabilities | `/mcp`, `claude mcp list` | "Available Tools" in the MCP settings | `kimi mcp list` | `/mcp` |
| Plan mode | Shift+Tab → plan mode | Plan Mode | verify in docs | approval mode `plan` (`/approval-mode`); others `default`, `auto-edit`, `auto`, `yolo` |
| Checkpoints / rewind | automatic checkpoints; `Esc Esc` / `/rewind` | checkpoints — verify in docs | verify in docs | `/restore` (file checkpoints before a tool call); the old `checkpointing` setting is deprecated |
| Context commands | `/context`, `/compact [instr]`, `/clear`, `/resume`, `/export`, `/cost` | verify in docs | verify in docs | `/context`, `/compress` (`/summarize`), `/summary`, `/resume`, `/memory`, `/remember` |
| Settings levels | managed > CLI > local > project > user (`.claude/settings*.json`, `~/.claude/settings.json`) | Team Rules > project rules; user rules in settings; enterprise hooks path | `~/.kimi/` (config format: verify in docs) | lowest→highest: defaults, system-defaults, user `~/.qwen/settings.json`, project `.qwen/settings.json`, system settings, env vars, CLI args |

## Can I just copy `.cursor/` into a Claude Code project?

**No.** Each tool reads only its own file names, formats and frontmatter. Claude Code ignores
`.cursor/rules/*.mdc`; Cursor ignores `CLAUDE.md` and `.claude/`. Copying the folder does nothing
at best, and at worst creates two sets of instructions that silently drift apart.

Instead: **copy the intent, translate the format, then validate the behavior.**

| Cursor artifact | Claude Code translation | How to validate |
|---|---|---|
| `.mdc` with `alwaysApply: true` | a section in the root `CLAUDE.md` (keep it short) | `/memory` shows it; ask a question the rule should change |
| `.mdc` with `globs: src/api/**` | a nested `src/api/CLAUDE.md` (loads when working there), or a skill whose `description` names the area | edit a file in that folder and check the rule is applied |
| `.mdc` "Apply Intelligently" (description only) | a **skill** (`SKILL.md` with a good `description`) | ask for the task in natural language; the skill should trigger |
| `.mdc` "Manual" (@-mention) | a slash command / skill you invoke with `/name` | run `/name` |
| `.cursor/mcp.json` | `.mcp.json` (the same `mcpServers` shape; check `type`, command paths, env vars) | `/mcp` shows it connected; `scripts/list_mcp_tools.py`-style listing |
| `.cursor/hooks.json` (`beforeShellExecution`, exit 2) | `settings.json` → `hooks.PreToolUse` with matcher `Bash` (exit 2 blocks); the stdin JSON shape differs | feed sample JSON to the script (see `tests/test_hooks.py`), then try it live |
| `AGENTS.md` | `CLAUDE.md` (or a `CLAUDE.md` that imports it with `@AGENTS.md` if the team shares one file across tools — verify import behavior) | `/memory` |

Checklist after any migration:
1. The same task gives the same *kind* of result in both tools (don't expect identical text, because of non-determinism).
2. Tests and evals still pass (`pytest`, hit@3).
3. Hooks and permissions really block what they should: try it, don't assume.
4. Remove the old files, or document which tool owns which file, to avoid drift.
