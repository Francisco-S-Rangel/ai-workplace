<!--
docs/knowledge/reliability.md — WHY: corpus note for the RAG demo that also teaches topic 11
(hallucination reduction) and topic 12 (non-determinism, prompt caching).
-->

# Hallucination Reduction

A hallucination is a fluent answer that is not supported by facts. Techniques that reduce
it, at the individual level:

- **Grounding:** give the model the source material (RAG, files, tool results) and ask it
  to answer only from that material.
- **Citations:** require a source for every claim so unsupported claims stand out.
- **Allow "I don't know":** explicitly permit "not found in the notes".
- **Verification:** run tests, linters and type checks; never accept "it works" without a
  run.
- **Small steps:** plan first, change little, check often.

At the team and process level: automated evaluation sets that catch regressions in CI,
code review (human or a reviewer sub-agent), shared project instructions, decision logs,
and treating model output as a draft that must pass the same gates as human code.

# Model Non-determinism

The same prompt can give different answers. Reasons:

- **Sampling:** with temperature above zero the model samples among likely tokens.
- **Floating point and batching:** GPU arithmetic is not perfectly associative; the batch
  your request shares with others can change tiny numbers and flip a token choice.
- **Backend routing:** requests may be served by different hardware or model versions.
- **Different context:** a slightly different history, file read or tool result changes the
  input, so the output changes too.

Because of this, you rely on tests and evaluations, not on one lucky run.

# Prompt Caching

Providers cache the processed prefix of a prompt: system prompt, tool definitions, project
instructions and earlier conversation turns. When the next request starts with the same
prefix, those tokens are read from cache at a fraction of the normal price and with lower
latency. That is why a follow-up prompt in the same session is almost free: only the new
message and the new output are processed at full cost. Changing something early in the
prompt, such as editing CLAUDE.md or switching models, breaks the cache for everything
after it. Caches also expire after a period of inactivity.
