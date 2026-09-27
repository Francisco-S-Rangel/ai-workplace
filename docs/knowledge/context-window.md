<!--
docs/knowledge/context-window.md — WHY: corpus note for the RAG demo (topic 7) that also
teaches topic 1: prompting techniques, context, context window, lost in the middle.
-->

# Context and the Context Window

The context is everything the model sees on a turn: the system prompt, project
instructions such as CLAUDE.md, tool definitions, the conversation history, file contents
that were read, and tool results. The model has no other memory. If a fact is not in the
context, the model either does not know it or it guesses.

The context window is the maximum number of tokens the model can take in at once. A token
is roughly three quarters of an English word. Every token in the window costs money and
latency on every turn. Large windows are useful, but a full window is not a free lunch:
the more text you add, the harder it becomes for the model to focus on the parts that
matter.

# Lost in the Middle

Lost in the middle is a documented effect in long-context models: information placed at
the beginning or the end of a long prompt is used more reliably than information buried in
the middle. Accuracy on retrieval-style questions drops when the relevant passage sits in
the center of a very long input.

Practical consequences:

- Put the most important instructions at the start (system prompt, CLAUDE.md) and restate
  the concrete task at the end, right before the model answers.
- Do not paste a whole 200-page document into the prompt. Retrieve the few relevant chunks
  instead (this is why RAG beats dumping a big document).
- Keep project instructions short; every extra rule dilutes the important ones.
- Compact or clear long conversations so old, irrelevant turns stop crowding the middle.

# Prompting Techniques

Good prompts are specific about the goal, the constraints, and the definition of done.
Useful techniques:

- **Role and goal:** say who the model is acting as and what outcome you want.
- **Context first, question last:** give the material, then ask the precise question.
- **Few-shot examples:** show one or two examples of the desired input and output format.
- **Step-by-step / plan first:** ask for a plan before code for multi-file changes
  (plan mode in Claude Code).
- **Constraints and negatives:** "do not add dependencies", "only edit files under tests/".
- **Output format:** ask for a table, JSON, or a fixed template so results are checkable.
- **Grounding:** "answer only from the provided sources and cite them; otherwise say not
  found" reduces hallucination.

A vague prompt produces a plausible but generic answer. A precise prompt with context,
constraints and a verification step produces an answer you can check.
