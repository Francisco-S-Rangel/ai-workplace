# .claude/hooks/remind_memory_bank.py — WHY: keeps the Memory Bank honest (topics 8 and 9).
# Registered as a Stop hook: runs every time Claude finishes a turn. If there are uncommitted
# changes but memory-bank/active-context.md was not touched, it shows a reminder to run
# /checkpoint. It exits 0 (non-blocking); exit 2 would force Claude to keep working, which is
# too aggressive for a reminder. Quiet when there is nothing to remind about, so it doesn't nag.
"""Stop hook: remind to update memory-bank/active-context.md."""

import json
import os
import subprocess
import sys


def main() -> None:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass
    project = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=project, capture_output=True, text=True
        ).stdout
    except OSError:
        sys.exit(0)
    changed = [line[3:] for line in status.splitlines() if line.strip()]
    if changed and not any("memory-bank/active-context.md" in path for path in changed):
        message = (
            f"[memory bank] {len(changed)} uncommitted change(s) but "
            "memory-bank/active-context.md is unchanged - "
            "run /checkpoint before /compact or /clear."
        )
        print(json.dumps({"systemMessage": message}))
    sys.exit(0)


if __name__ == "__main__":
    main()
