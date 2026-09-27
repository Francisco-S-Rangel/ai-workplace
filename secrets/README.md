<!--
secrets/README.md — WHY: explains the fake key used to demo access control (topic 10).
`api_key.txt` contains only `FAKE-DEMO-KEY`. Reads of this folder are blocked twice:
by a `permissions.deny` rule in `.claude/settings.json` and by the PreToolUse hook
`.claude/hooks/guard_paths.py` (defense in depth). Never put real secrets in a repo.
-->
# secrets/ (demo only)
