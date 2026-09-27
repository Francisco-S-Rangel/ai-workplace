<!--
docs/concepts/hallucination-reduction.md — WHY: study page for topic 11 (hallucination
reduction: grounding, citations, tests, evals) at the individual AND team/process level.
-->

# Hallucination reduction

A hallucination is a **fluent, confident answer not supported by facts**: an invented API, a
wrong flag, a "tests pass" that was never run.

## Individual level (you + the agent)
| Technique | How | In this repo |
|---|---|---|
| Grounding | give sources; answer only from them | RAG + `search_notes` MCP tool |
| Citations | every claim → `source#heading` | `/ask-notes`, `cli ask` |
| Permission to say "I don't know" | explicit fallback text | "Not found in notes." |
| Verify, don't trust | run it | CLAUDE.md: "never claim something works without running it" |
| Check the docs, not memory | read official docs for formats | Phase 4: hook, permission and agent formats fetched from the docs; see the decision log |
| Small steps + plan | plan mode, one phase at a time | 7 phases, a commit each |
| Mark uncertainty | "verify in docs" instead of guessing | `docs/other-tools.md` |

## Team / process level
| Technique | In this repo |
|---|---|
| Automated tests in the definition of done | `pytest` (34 tests) |
| **Evals that catch regressions** | `tests/test_rag_eval.py`: hit@3 ≥ 0.8 or the build fails |
| Review by a second agent or a human | `code-reviewer` sub-agent, `/review-parallel` |
| Shared, versioned instructions | `CLAUDE.md`, skills, commands in git |
| Decision records | `memory-bank/decision-log.md` |
| Deterministic guardrails | hooks + permissions: even a hallucinated command can't read the protected folder |
| Treat tool output as data | the prompt-injection line in `mcp-overview.md` is quoted, not obeyed |

## Real examples from building this repo
- The MCP SDK 2.x had renamed `FastMCP`. An import test caught it and I pinned `<2`, instead of
  writing code for an API that no longer existed.
- The spec used `Bash(cmd:*)`; the docs show `Bash(cmd *)` as the current form. I checked instead of assuming.
- The Kimi CLI repo turned out to be archived, so its cells are marked "verify in docs" rather than invented.
