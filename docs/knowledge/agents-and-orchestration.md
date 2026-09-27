<!--
docs/knowledge/agents-and-orchestration.md — WHY: corpus note for the RAG demo that also
teaches topic 4 (agent vs LLM, sub-agents, hand-off via files) and topic 14 (multi-agent
orchestration, value and ROI).
-->

# Agent versus LLM

An LLM is a model that maps text in to text out. It does nothing on its own. An agent is a
loop around an LLM: it receives a goal, decides on an action, calls a tool (read a file,
run a command, query an MCP server), observes the result, and repeats until the goal is
met. The agent adds tools, memory, permissions and a stopping condition around the model.

# Agent versus Sub-agent

A sub-agent is an agent launched by another agent for a focused task. In Claude Code a
sub-agent has its own context window, its own system prompt and a restricted tool list.
Built-in limitations: the sub-agent does not see the parent conversation, it returns only a
final summary to the parent, and there is no shared memory between sub-agents. Details that
do not fit in the summary are lost.

# Hand-off via Files

The fix is to hand off through files. Each sub-agent writes its full result to a known file,
such as `.agent-handoff/review.md`, and returns only a short summary. The orchestrator then
reads the files, compares results and writes a combined summary. Files are durable,
reviewable, and can be read by the next agent or by a human.

# Multi-agent Orchestration

An orchestrator splits work into independent tasks and runs sub-agents in parallel, such as
a reviewer, a test writer and an evaluator. Good orchestration defines for each worker: the
input, the allowed tools, the output file, and what to do on failure (retry once, then
escalate to a human). Afterwards the orchestrator reconciles conflicts, for example when the
reviewer asks for a change that would break a test the test writer just added. Parallel
execution saves wall-clock time but costs more tokens, so use it when tasks are truly
independent.

# Value and ROI

AI adoption should be justified with numbers, not enthusiasm. A simple value case records
the task, the time before and after, the token cost, a quality metric such as defects or
eval score, and the risks. AI-assisted work means a human drives and the AI helps with steps.
AI-first work means the process is designed around the agent from the start, with
instructions, evaluations and guardrails, and the human reviews and steers.
