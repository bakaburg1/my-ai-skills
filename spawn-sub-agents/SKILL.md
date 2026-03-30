---
name: spawn-sub-agents
description: Spawn one-shot opencode sub-agents in noninteractive mode for shell-only experimentation, quick probes, or batchable tasks where intermediate steps would waste context. Use when parallelizing lightweight terminal checks, dry-run commands, or information gathering, and when the main agent should keep the full editing context while sub-agents return concise results.
---

# Spawn Sub Agents

## 1. Overview

1. Use this skill to dispatch one-shot, noninteractive opencode runs for terminal-only experimentation, then collect concise results back into the main agent's context.

## 2. Use Cases

1. Run quick shell probes that would otherwise eat context (e.g., `rg` searches, listing files, quick command outputs).
2. Parallelize independent checks (e.g., inspecting different directories or running small read-only commands).
3. Produce compact summaries from command outputs that do not require file edits.

## 3. Workflow

1. Decide if a sub-agent is appropriate.
   a. Use sub-agents only for terminal experimentation, never for editing files.
   b. Keep main-agent edits centralized to avoid conflicts.
   c. Do not ask sub-agents to spawn other sub-agents.
2. Build a minimal context for each sub-agent.
   a. Provide just enough paths, commands, and constraints.
   b. Avoid pasting full conversation history unless essential.
3. Define the task list.
   a. Keep each task single-purpose and one-shot.
   b. If more than 5 tasks are needed, ask the user to confirm before spawning.
4. Run sub-agents in noninteractive mode.
   a. Use `opencode run` which supports specifying `--model` and reasoning `--variant`.
   b. The default wrapper script uses `--model=opencode/mimo-v2-pro-free` and `--reasoning=high`. If the free model is unavailable and no alternative is provided, the script will error out indicating this skill must be updated.
   c. The wrapper automatically checks for and attaches the `AGENTS.md` file from the repository root on startup.
5. Collect results and integrate.
   a. Summarize outputs into actionable findings.
   b. If a sub-agent fails, craft a clearer retry prompt.
   c. If repeated failures occur, stop spawning and handle in the main agent.

## 4. Prompt Template (One-Shot)

1. Use a concise, explicit prompt structure.
2. **Detailed implementation specs** must be provided by the parent model. You cannot assume the sub-agent is smart and knowledgeable; it must be hand-driven to completion with exact instructions.
3. Include the task, constraints, and required output format.

```text
You are a one-shot sub-agent. Do not edit files.
Task: <single, specific task>
Constraints:
1) Terminal-only experimentation.
2) Do not create or ask other sub-agents.
3) No file edits; if a complex script is needed, write it under .agents/tmp and delete it on success.
4) Keep output concise and actionable.
Return:
1) Commands run.
2) Key outputs (summarized).
3) Any errors and suggested fixes.
```

## 5. Guardrails

1. Do not edit or generate patches in sub-agents.
2. Do not create or ask other sub-agents.
3. Do not assume interactive follow-ups; each run is one-shot.
4. If a script is unavoidable, place it in `.agents/tmp/` and remove it after success.
5. Keep sub-agent prompts narrowly scoped.

## 6. Failure Handling

1. If a sub-agent returns unusable output, retry with a clearer, more constrained prompt.
2. If a sub-agent fails twice, stop retrying and do the work in the main agent.

## 7. Scripted Orchestration

1. Use `scripts/spawn_subagents.py` to run multiple noninteractive jobs with timeouts and concurrency control.
2. Use `--confirm-large` only after the user approves running more than 5 tasks.
3. Use `--output-dir` if you need per-task stdout/stderr logs.
4. Use `--prepend` to enforce mandatory constraints (e.g., no sub-agent spawning) in every task.
5. Output is printed by default; use `--no-print-output` to suppress it.

## 8. References

1. For noninteractive opencode usage patterns, see `references/noninteractive.md`.
