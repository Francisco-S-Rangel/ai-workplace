# .claude/hooks/guard_paths.py — WHY: event-based access control (topic 10).
# Registered as a PreToolUse hook in .claude/settings.json. Claude Code runs it BEFORE every
# matching tool call and passes the call as JSON on stdin. Exit code 2 BLOCKS the call and the
# stderr text is shown to Claude as the reason. The harness runs this, not the model, so it
# holds even if the model is confused or prompt-injected (topic 9: hooks are deterministic).
#
# Blocks:
#   - any file tool or shell command touching `secrets/` or `.env`
#   - writes to `data/index.json` (regenerate it with `python -m study_buddy.cli ingest` instead)
# This is defense in depth on top of `permissions.deny`: deny rules cover the built-in file
# tools and recognized commands like `cat`, but not e.g. `grep -r KEY .` or a Python one-liner.
# Standard library only, so it runs with any Python on Windows / macOS / Linux.
"""PreToolUse guard for secrets and the protected index."""

import json
import os
import re
import sys
from pathlib import Path

SECRET_PATH_RE = re.compile(r"(^|/)(secrets(/|$)|\.env$)")
SECRET_CMD_RE = re.compile(r"(?<![\w.-])(secrets([/\\]|\b)|\.env\b)", re.IGNORECASE)
INDEX_WRITE_CMD_RE = re.compile(
    r"(>\s*|tee\s+|out-file\s+|set-content\s+)\S*data[/\\]index\.json", re.IGNORECASE
)
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def relative_to_project(raw: str, cwd: str) -> str:
    """Project-relative POSIX path (lowercase) or the absolute path if outside the project."""
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or cwd).resolve()
    path = Path(raw)
    if not path.is_absolute():
        path = Path(cwd) / path
    path = path.resolve()
    try:
        return path.relative_to(project).as_posix().lower()
    except ValueError:
        return path.as_posix().lower()


def check(event: dict) -> str | None:
    """Return a block reason, or None to allow."""
    tool = event.get("tool_name", "")
    tool_input = event.get("tool_input") or {}
    cwd = event.get("cwd") or os.getcwd()

    for key in ("file_path", "path", "notebook_path"):
        if tool_input.get(key):
            rel = relative_to_project(str(tool_input[key]), cwd)
            if SECRET_PATH_RE.search(rel):
                return f"{tool} on '{rel}' is blocked: secrets/ and .env are off-limits."
            if tool in WRITE_TOOLS and rel == "data/index.json":
                return (
                    "Writing data/index.json by hand is blocked. "
                    "Rebuild it with: python -m study_buddy.cli ingest"
                )

    command = str(tool_input.get("command", ""))
    if command:
        if SECRET_CMD_RE.search(command):
            return f"{tool} command blocked: it references secrets/ or .env."
        if INDEX_WRITE_CMD_RE.search(command):
            return (
                "Shell writes to data/index.json are blocked. Use: python -m study_buddy.cli ingest"
            )
    return None


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # never break the session on malformed input
    reason = check(event)
    if reason:
        print(f"[guard_paths hook] {reason}", file=sys.stderr)
        sys.exit(2)  # exit 2 = block the tool call; stderr goes to Claude
    sys.exit(0)


if __name__ == "__main__":
    main()
