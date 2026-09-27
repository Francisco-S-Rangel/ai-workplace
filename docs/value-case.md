<!--
docs/value-case.md — WHY: topic 14 / level A5, value and ROI thinking. A reusable template plus
ONE ILLUSTRATIVE EXAMPLE. The example numbers are made up to show the method; they are not
measurements.
-->

# Value case template (ROI)

| Field | What to record |
|---|---|
| **Task** | a concrete, repeated task (not "coding in general") |
| **Frequency** | how often it happens (per week or month) |
| **Time before** | median human time per task, measured (not guessed) |
| **Time after** | human time with the agent: prompting + reviewing + fixing |
| **Token cost** | from `/cost` (tokens × price), per task |
| **Quality metric** | defects, review comments, eval score, rework rate, before vs after |
| **Risk** | what can go wrong (security, wrong output, over-reliance) + mitigations |
| **Setup cost** | one-time effort (instructions, skills, hooks, evals) |
| **Decision** | adopt / pilot / reject, and the review date |

**Monthly value** ≈ frequency × (time before − time after) × hourly cost − token cost.
**Payback** ≈ setup cost ÷ monthly value.

---

## Example (ILLUSTRATIVE — numbers invented to show the method)

**Task:** add a new knowledge note to a RAG corpus, with an eval question and passing tests
(the `add-knowledge-note` skill).

| Field | Value |
|---|---|
| Frequency | 20 notes / month |
| Time before | 45 min (write, chunk-check, add eval, run tests) |
| Time after | 15 min (prompt + review the draft + check citations) |
| Token cost | ~$0.30 per note → $6 / month |
| Quality | eval hit@3 must stay ≥ 0.8 (a gate, automated); review comments per note: track |
| Risk | factual errors in generated notes → mitigated by human review + "facts only" rule + eval |
| Setup cost | 3 h (skill + eval + hooks) |

Monthly time saved: 20 × 30 min = 10 h. At €50/h that's €500 − €6 tokens ≈ **€494/month**.
Payback: 3 h × €50 = €150 → **under one week**.

**Decision (example):** adopt, re-check in 1 month with *measured* times.

## Caveats to say out loud
- Measure the "after" time **including review and fixes**, not just generation.
- Quality can drop silently; that's why the eval gate exists.
- Savings on rare tasks rarely cover the setup cost. Start with frequent, well-specified tasks.
