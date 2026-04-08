---
name: spawn-sub-agents
description: Spawn one-shot opencode sub-agents in noninteractive mode for repository exploration, targeted test execution, or bounded implementation work. Use when delegating a clearly planned task to one sub-agent or parallelizing multiple independent sub-agents while the main agent keeps the broader context.
---

# Spawn Sub Agents

## 1. Overview

1. Use this skill to launch one-shot, noninteractive `opencode run` helper agents.
2. This skill fits read-only investigation, focused test execution, and bounded repository edits.
3. The main agent decides whether delegation is safe, writes the prompt, integrates the result, and communicates with the user.
4. The main agent may spawn multiple sub-agents in parallel only when tasks are independent; parallel edit tasks require clearly separated writable ownership and no realistic chance of overlap.

## 2. When To Use It

1. Offload repository exploration, searches, documentation review, environment probes, or test runs that would waste main-agent context.
2. Delegate a bounded implementation task when the main agent can provide a full detailed plan.
3. Split independent work across multiple sub-agents when their scopes, files, commands, or tests can be kept separate.
4. Keep orchestration, synthesis, and broad architectural judgment in the main agent.

## 3. Main-Agent Rules

1. Delegate only one-shot tasks that can succeed without interactive clarification.
2. If the delegated task edits files, provide a full and detailed plan. Do not delegate vague requests like "fix this" or "refactor that".
3. If the delegated task does not edit files, choose the instruction detail level you think is appropriate.
4. Always state the goal, working directory, relevant files or paths, constraints, expected deliverable, and whether edits are allowed.
5. For edit tasks, include concrete implementation steps, coding conventions, architecture notes, and verification commands whenever available.
6. Provide enough repo-specific context that the sub-agent does not need to guess intended behavior.
7. Prefer several focused sub-agents over one overloaded prompt when tasks are independent.
8. When using multiple sub-agents, assign each one explicit ownership boundaries such as files, directories, commands, or tests.
9. For parallel edit tasks, specify exactly which files or paths each sub-agent may modify and which paths are off-limits.
10. Do not ask a sub-agent to spawn other sub-agents.
11. Avoid delegating destructive or irreversible work unless the user explicitly requested it and the prompt states the boundaries precisely.

## 3A. Launch Modes

1. Use `repo mode` by default.
2. `repo mode` assumes the normal repository contract, including `AGENTS.md` and the relevant coordination files when the task needs them.
3. Use `fast mode` only for small, self-contained tasks where repository coordination files are not needed to do correct work.
4. Good `fast mode` candidates include:
   - narrow read-only searches
   - targeted command execution
   - tiny mechanical edits in one clearly bounded file
   - simple environment probes
5. Do not use `fast mode` for:
   - architecture-sensitive work
   - backlog or planning decisions
   - coordination-file updates
   - broad refactors
   - tasks where repo conventions materially affect correctness
6. If there is any doubt, use `repo mode`.
7. In `fast mode`, state explicitly that the sub-agent should not read repo coordination files unless the prompt references them directly.

## 4. Sub-Agent Rules

1. Treat every run as one-shot and self-contained.
2. Follow the provided task and plan before expanding scope.
3. If you are unsure how the code works, inspect nearby code, documentation, configuration, and tests before deciding what to do.
4. If uncertainty remains, run relevant tests or targeted validation commands to confirm your understanding before making or finalizing changes.
5. Keep edits bounded to the delegated scope and report any uncertainty that remains.
6. If you are part of a parallel batch, do not edit files outside your assigned ownership boundary.
7. Do not spawn or request other sub-agents.

## 5. Running `opencode` Noninteractively

1. Basic form:

```bash
opencode run "Your task prompt"
```

1. Preferred default for this skill:

```bash
opencode run --model github-copilot/gpt-5.4-mini --variant high "Your task prompt"
```

1. Important options:
   - `--model <provider/model>` selects the model.
   - `--variant <level>` selects reasoning effort such as `high`, `max`, or `minimal`.
   - `--dir <path>` runs the task in a specific directory.
   - `-f, --file <path>` attaches one or more files as context.
   - `--print-logs` sends internal runner logs to stderr and should be reserved for debugging runs.
   - `--log-level` controls internal runner verbosity when `--print-logs` is enabled.
   - `--thinking` shows thinking blocks when supported and useful.
   - `-c, --continue` continues the last session.
   - `-s, --session <id>` continues a specific session.
   - `--fork` forks a continued session before proceeding.
   - `--agent <name>` selects a different agent profile when needed.
2. Reliable startup pattern for long or multiline prompts:
   - Write the full prompt to a repo-local task file and pass that file path as the sole positional message.
   - Put that prompt file under `.agents/tmp/sub_agents/<pid>-<timestamp>/task.txt` or a similarly named repo-local run directory.
   - Keep the prompt file inside the workspace or repo. Do not place it under `/tmp` or another external directory unless you have already confirmed the runner can read it.
   - Prefer a blocking, single-shot launch instead of shell quoting a multiline prompt inline.
   - If you need extra context files, list them explicitly in the prompt or attach them with `-f`; do not worry about a large context set when the task truly needs it.
   - In this environment, the most reliable shape was: `opencode run --model github-copilot/gpt-5.4-mini --variant high <repo-local-task-file>`.
3. Output behavior:
   - The user-facing transcript and final response are printed to stdout.
   - Internal runner logs are printed to stderr only when `--print-logs` is enabled.
   - The default skill workflow should treat stdout as the primary run artifact and keep stderr separate.
4. Prefer a repo-local task file plus `--dir` when you need repeatable noninteractive runs.
5. For multiple parallel sub-agents, launch separate `opencode run` commands with separate prompts rather than combining unrelated tasks into one run.
6. `AGENTS.md` is part of the repo contract and is already assumed by the workflow, so you do not need to attach it for normal launches.
7. Always capture the user-facing transcript and any internal debug output into separate files under the run directory:

```bash
run_id="$(date +%Y%m%dT%H%M%S)-$$"
run_dir="$PWD/.agents/tmp/sub_agents/$run_id"
mkdir -p "$run_dir"
task_file="$run_dir/task.txt"
run_log="$run_dir/run.log"
debug_log="$run_dir/debug.log"
opencode run --model github-copilot/gpt-5.4-mini --variant high "$task_file" \
  > >(tee "$run_log") \
  2> >(tee "$debug_log" >&2)
```

- `run.log` is the main artifact and should contain the user-facing transcript/final answer, not internal opencode service logs.
- `debug.log` should stay separate and is mainly for stderr, warnings, and optional debugging output.
- If the task needs more context files, put them in the same run directory or pass them with `-f`.
- Only add `--print-logs` for a debugging run, and when you do, also set `--log-level WARN` or `ERROR` so `debug.log` stays readable.

1. Clean up old run directories automatically on launch when it is safe to do so.
   - Prefer a best-effort pruning sweep for entries older than a short retention window, such as 7 days.
   - Treat the run directory like disposable temp storage, not a permanent archive.
2. Do not busy-poll a sub-agent run.
   - Start the process once, let it run to completion, and wait on that single process if your environment supports it.
   - If your tool stack cannot block while the sub-agent is running, stop after launch, report the PID and log file path, and tell the user you will resume when they wake you up.

## 6. Prompt Templates

1. Use an explicit prompt structure.
2. For edit tasks, the parent agent must provide detailed implementation instructions instead of relying on the sub-agent to invent the plan.
3. Include the task, constraints, verification expectations, and required return format.

```text
You are a one-shot sub-agent.
Task: <single, specific task>
Working directory: <repo or subdir>
Assigned scope: <files, directories, tests, or commands you own>
Constraints:
1) <state whether file edits are allowed>
2) Do not create or ask other sub-agents.
3) If uncertain how the code works, inspect code, docs, config, and tests first.
4) Run relevant tests or checks when needed to validate conclusions.
5) If this is part of a parallel batch, do not go outside your assigned scope.
6) Keep output concise and actionable.
Return:
1) What you did.
2) Files changed or commands run.
3) What you verified.
4) Remaining risks or open questions.
```

4. Use this template when the delegated task edits files:

```text
You are a one-shot sub-agent and you may edit files.
Goal: <precise implementation objective>
Working directory: <repo root or subdir>
Relevant files: <paths>
Owned writable files or paths: <exact paths this sub-agent may change>
Constraints:
1) Stay within the delegated scope.
2) Follow this plan exactly unless verification reveals a necessary adjustment.
3) If unsure how the current code works, inspect related code, docs, config, and tests before editing.
4) If this is part of a parallel batch, do not edit files outside the owned writable paths.
5) Run the required validation after changes.
Plan:
1) <step one>
2) <step two>
3) <step three>
Validation:
1) <test or command>
2) <test or command>
Return:
1) Changes made.
2) Validation performed and results.
3) Any deviations from the plan and why.
4) Remaining risks or follow-ups.
```

5. Use this template for `fast mode` tasks:

```text
You are a one-shot sub-agent in fast mode.
Task: <single, specific task>
Working directory: <repo or subdir>
Assigned scope: <files, directories, tests, or commands you own>
Constraints:
1) Do not read AGENTS.md, PLAN.md, ARCHITECTURE.md, BACKLOG.md, or project memory unless this prompt explicitly references them.
2) Stay within the assigned scope.
3) Do not create or ask other sub-agents.
4) If uncertain, inspect only the directly relevant code, docs, config, or tests needed for this task.
5) Keep output concise and actionable.
Return:
1) What you did.
2) Files changed or commands run.
3) What you verified.
4) Remaining risks or open questions.
```

## 7. Parallel Execution Guidance

1. Run multiple sub-agents only when their tasks are independent.
2. Parallel read-only exploration and test tasks are usually safe if they do not compete for exclusive resources.
3. Parallel edit tasks are safe only when writable ownership is clearly split and there is no realistic chance of overlapping changes.
4. Prefer one prompt per task instead of combining unrelated goals.
5. Give each parallel sub-agent explicit file, directory, command, or test ownership.
6. Capture outputs to files and keep the prompt file, log file, and any supporting context under `.agents/tmp/sub_agents/<pid>-<timestamp>/`.
7. Prefer a single blocking launch with console-plus-file log capture over repeated polling.
8. If the environment cannot wait on the sub-agent process directly, stop after launch and hand control back to the user rather than spinning on repeated status checks.
9. Be conservative with large batches; if delegation becomes hard to review, do more of the work in the main agent.

## 8. Guardrails And Failure Handling

1. Do not create or ask other sub-agents.
2. Do not assume interactive follow-ups; each run is one-shot.
3. Keep prompts narrowly scoped and explicit.
4. Do not let a sub-agent silently broaden the task beyond the delegated goal.
5. Do not assign overlapping writable ownership to multiple sub-agents.
6. Prefer the main agent to handle final synthesis, broad architectural judgment, and user communication.
7. If a sub-agent returns unusable output, retry with a clearer, more constrained prompt.
8. If a sub-agent fails twice, stop retrying and do the work in the main agent.
9. If a delegated edit task starts to require major replanning, take the work back into the main agent and produce a new plan before delegating again.
10. If parallel sub-agents uncover shared writable files, conflicting assumptions, or competing ownership, stop the parallel plan and re-scope the work in the main agent.
