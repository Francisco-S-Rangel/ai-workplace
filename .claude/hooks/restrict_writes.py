# .claude/hooks/restrict_writes.py — WHY: least privilege for sub-agents (topics 4 and 10).
# Tool lists in agent frontmatter are all-or-nothing ("Write" or no Write). This hook narrows
# Write/Edit to specific folders. It is registered in the `hooks:` frontmatter of an agent,
# e.g. code-reviewer may write ONLY under .agent-handoff/, test-writer only under tests/.
# Usage (in agent frontmatter):  python restrict_writes.py .agent-handoff/ tests/
# Exit 2 blocks the call and tells the sub-agent why.
"""PreToolUse: allow Write/Edit only under the folders given as arguments."""

import json
import os
import sys
from pathlib import Path


def main() -> None:
    allowed = [a.replace("\\", "/").lower().rstrip("/") + "/" for a in sys.argv[1:]]
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    raw = (event.get("tool_input") or {}).get("file_path")
    if not raw:
        sys.exit(0)
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".").resolve()
    path = Path(raw) if Path(raw).is_absolute() else Path(event.get("cwd") or project) / raw
    try:
        rel = path.resolve().relative_to(project).as_posix().lower()
    except ValueError:
        rel = path.resolve().as_posix().lower()
    if not any(rel.startswith(prefix) for prefix in allowed):
        print(
            f"[restrict_writes hook] this agent may only write under {allowed}; got '{rel}'.",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
