<!--
docs/concepts/non-determinism.md — WHY: study page for topic 12 (model non-determinism) and why
this repo relies on tests/evals instead of trusting a single run (topic 11).
-->

# Model non-determinism

## Why the same prompt gives different answers
| Cause | Explanation |
|---|---|
| **Sampling** | With temperature > 0 the next token is *sampled* from a probability distribution. Two runs can pick different tokens, and the answers diverge from there. |
| **Floating point + batching** | GPU arithmetic isn't perfectly associative. Your request is batched with others, and a different batch changes the tiny rounding, which can flip a near-tie between tokens. So even temperature 0 isn't guaranteed identical. |
| **Backend routing** | Requests can go to different hardware, regions, or model snapshots or versions. |
| **Different context** | A slightly different history, file read, tool result, time, or retrieved chunk is a *different input*, so the output differs. Agents amplify this, because each step feeds the next. |

## What to do about it
- **Verify with deterministic checks:** tests, linters, evals (`pytest`, `ruff`, hit@3). The
  code under test is deterministic even if the model isn't.
- **Pin what you can:** model version, low temperature for extraction tasks, fixed instructions.
- **Structure the output:** JSON or templates make runs comparable.
- **Evaluate on a set, not one example:** `tests/eval/eval_set.jsonl` has 10 questions.
- **Keep decisions on disk:** the decision log, so the next run doesn't re-decide differently.

In this repo the *retrieval* is deterministic (BM25, sorted files). Only Claude's wording
varies, which is why `/ask-notes` demands citations you can check.
