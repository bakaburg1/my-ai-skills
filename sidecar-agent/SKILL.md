---
name: sidecar-agent
description: "Orchestrate work through sidecar subagents while the main agent stays the driver: inspect ~/.codex/config.toml for sidecar concurrency, decide what is worth delegating, run simple local commands or edits directly when cheaper, spawn gpt-5.4-mini medium sidecars by default, adjust reasoning level when needed, evaluate their work, and report only validated outcomes. Use when the user wants the main agent to coordinate execution through subagents rather than perform all work inline."
---

# Sidecar Agent

## Driver Role

Keep the main agent as the driver. The driver assesses the request, decides what to delegate, writes sidecar prompts, reviews sidecar evidence, resolves conflicts, and reports the validated result to the user.

The driver may still run simple commands, inspect files, or make small code edits directly when delegation would cost more than it saves, especially before any sidecar has been spawned or when a task is too small to justify a new thread.

## Capacity Check

Before planning sidecar work, inspect `~/.codex/config.toml` and determine the available concurrent sidecar capacity. Look for settings such as `multi_agent`, `agents.max_threads`, `agents.max_depth`, and configured agent roles. Treat that capacity as the maximum number of sidecars to run at once unless the user explicitly narrows it.

If the config is unavailable or ambiguous, use the visible multi-agent tool limits conservatively and state the assumption in the final report.

## Delegation Workflow

1. Assess the request and split it into driver-owned judgment plus sidecar-owned execution.
2. Run trivial discovery or edits directly when that is faster than spawning.
3. Spawn sidecars as `gpt-5.4-mini` with `medium` reasoning by default.
4. Let the user-requested reasoning level override the default when the tool supports it.
5. Give each sidecar a narrow task, clear ownership boundaries, success criteria, and expected evidence.
6. Keep sidecar write scopes disjoint when multiple sidecars run concurrently.
7. Evaluate each sidecar result against the request, workspace state, tests, and constraints.
8. Ask follow-up sidecar prompts when context continuity matters; spawn a new sidecar when a clean review or independent verification is more useful.
9. Report only validated outcomes, including tests run, caveats, and any unresolved risk.

## Reasoning Level Adjustment

If a sidecar is not thinking deeply enough, first check whether the available API can raise that existing sidecar's reasoning level. If supported, raise it and explain the reason in the follow-up prompt.

If the API does not support changing reasoning level for an existing sidecar, spawn a new sidecar at a higher reasoning level and give it the relevant context plus the specific concern with the previous attempt. Do not present the weaker result as final until the higher-reasoning pass has been evaluated.

## Prompting Rules

- Include enough local context for the sidecar to work without assuming prior conversation history.
- Tell coding sidecars that they are not alone in the codebase and must not revert unrelated changes.
- Ask for concrete files changed, commands run, outputs, screenshots, or other evidence.
- Do not leak desired conclusions to verification sidecars; ask them to assess the artifact or diff directly.
- Prefer reusing a sidecar when retained context is valuable and spawning a new one when independence is more valuable.

## Driver Final Report

Summarize what the driver validated, not just what sidecars claimed. Include sidecar caveats only when they affect confidence or next steps.
