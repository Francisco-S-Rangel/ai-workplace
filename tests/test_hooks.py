# tests/test_hooks.py — WHY: hooks are code, so they get tests (topic 10: access control;
# topic 11: verify, don't trust). Runs each hook script exactly like Claude Code does:
# JSON on stdin, then checks the exit code (2 = blocked) and the message.
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HOOKS = ROOT / ".claude" / "hooks"


def run_hook(name: str, event: dict) -> subprocess.CompletedProcess:
    event = {"cwd": str(ROOT), **event}
    return subprocess.run(
        [sys.executable, str(HOOKS / name)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env={"CLAUDE_PROJECT_DIR": str(ROOT), "PATH": ""},
    )


@pytest.mark.parametrize(
    "tool, tool_input",
    [
        ("Read", {"file_path": str(ROOT / "secrets" / "api_key.txt")}),
        ("Read", {"file_path": "secrets/api_key.txt"}),
        ("Read", {"file_path": ".env"}),
        ("Grep", {"pattern": "KEY", "path": "secrets"}),
        ("Bash", {"command": "cat secrets/api_key.txt"}),
        ("Bash", {"command": "grep -r FAKE secrets"}),
        ("PowerShell", {"command": r"Get-Content .\secrets\api_key.txt"}),
        ("Write", {"file_path": "data/index.json", "content": "{}"}),
        ("Edit", {"file_path": str(ROOT / "data" / "index.json")}),
        ("Bash", {"command": "echo {} > data/index.json"}),
    ],
)
def test_guard_blocks(tool, tool_input):
    result = run_hook("guard_paths.py", {"tool_name": tool, "tool_input": tool_input})
    assert result.returncode == 2
    assert "[guard_paths hook]" in result.stderr


@pytest.mark.parametrize(
    "tool, tool_input",
    [
        ("Read", {"file_path": "docs/knowledge/rag-basics.md"}),
        ("Read", {"file_path": "data/index.json"}),  # reading the index is fine
        ("Bash", {"command": ".venv/Scripts/python.exe -m study_buddy.cli ingest"}),
        ("Bash", {"command": "git status"}),
        ("Edit", {"file_path": "study_buddy/retrieve.py"}),
    ],
)
def test_guard_allows(tool, tool_input):
    result = run_hook("guard_paths.py", {"tool_name": tool, "tool_input": tool_input})
    assert result.returncode == 0, result.stderr


def test_format_hook_ignores_non_python_files():
    result = run_hook(
        "format_python.py", {"tool_name": "Write", "tool_input": {"file_path": "x.md"}}
    )
    assert result.returncode == 0 and result.stdout == ""


def test_format_hook_formats_python_file(tmp_path):
    ugly = tmp_path / "ugly.py"
    ugly.write_text("x=  1\n", encoding="utf-8")
    result = run_hook(
        "format_python.py", {"tool_name": "Edit", "tool_input": {"file_path": str(ugly)}}
    )
    assert result.returncode == 0
    assert ugly.read_text(encoding="utf-8") == "x = 1\n"
    assert "format_python hook" in json.loads(result.stdout)["systemMessage"]


@pytest.mark.parametrize(
    "file_path, allowed, expected_code",
    [
        (".agent-handoff/review.md", [".agent-handoff/"], 0),
        ("study_buddy/retrieve.py", [".agent-handoff/"], 2),
        ("tests/test_new.py", ["tests/", ".agent-handoff/"], 0),
        ("study_buddy/ingest.py", ["tests/", ".agent-handoff/"], 2),
    ],
)
def test_restrict_writes(file_path, allowed, expected_code):
    event = {"cwd": str(ROOT), "tool_name": "Write", "tool_input": {"file_path": file_path}}
    result = subprocess.run(
        [sys.executable, str(HOOKS / "restrict_writes.py"), *allowed],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env={"CLAUDE_PROJECT_DIR": str(ROOT)},
    )
    assert result.returncode == expected_code, result.stderr
