# .claude/hooks/format_python.py — WHY: deterministic formatting (topics 9 and 10).
# Registered as a PostToolUse hook on Edit|Write. After Claude edits a .py file, the harness
# runs `ruff format` on it. "Hooks always run, the agent doesn't decide": compare with a
# CLAUDE.md rule saying "please format your code", which the model may forget.
# Standard library only; finds ruff in the project venv first, then on PATH.
"""PostToolUse: run `ruff format` on the edited Python file."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_ruff(project: Path) -> str | None:
    for candidate in (
        project / ".venv" / "Scripts" / "ruff.exe",
        project / ".venv" / "bin" / "ruff",
    ):
        if candidate.exists():
            return str(candidate)
    return shutil.which("ruff")


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    file_path = (event.get("tool_input") or {}).get("file_path", "")
    if not file_path.endswith(".py"):
        sys.exit(0)

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".")
    ruff = find_ruff(project)
    if not ruff:
        sys.exit(0)  # formatting is a convenience: never fail the session if ruff is missing
    result = subprocess.run([ruff, "format", file_path], capture_output=True, text=True)
    status = (result.stdout or result.stderr).strip()
    # systemMessage is shown in the UI, so the demo can SEE the hook fire.
    print(
        json.dumps(
            {"systemMessage": f"[format_python hook] ruff format {Path(file_path).name}: {status}"}
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
