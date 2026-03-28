---
name: project-init
description: Bootstrap a new project around a coordinated operating system of `AGENTS.md`, `PLAN.md`, `ARCHITECTURE.md`, `BACKLOG.md`, and `.agents/memory/`. Use when Codex needs to initialize or re-initialize a repository's working contract, artifact choreography, backlog discipline, and project memory flow for a new product, tool, app, library, or internal project.
---

# Project Init

## Overview

Use this skill to create the initial project operating backbone before implementation starts. The goal is not only to scaffold files, but to make them work together: `AGENTS.md` orchestrates the workflow, `PLAN.md` defines the target, `ARCHITECTURE.md` records implemented reality, `BACKLOG.md` decomposes the work, and `project-memory` initializes durable memory without duplicating the other artifacts.

## Workflow

1. Establish the backbone information before writing files.
2. Create the canonical artifacts in a fixed order.
3. Initialize `.agents/memory/` through `$project-memory`.
4. Keep deferred choices explicit and avoid guessing.

## Step 1: Establish Backbone Information

Extract as much as possible from the user request and repo context first. Before writing the artifact set, make sure you understand enough of the project to give the scaffold a real backbone.

Use [bootstrap-discovery-checklist.md](references/bootstrap-discovery-checklist.md) to confirm the minimum inputs.

At minimum, try to establish:

- short project description
- project purpose and audience
- intended deliverable or product shape
- scope boundaries
- major technical direction
- initial milestone framing
- known open questions
- which choices the user wants to defer

Ask for missing high-impact information when the scaffold would otherwise become vague or misleading. The user may defer some or all decisions to later implementation time. When that happens:

- record strategic or cross-cutting deferrals in `PLAN.md`
- convert actionable deferrals into decision-gate backlog items in `BACKLOG.md`
- record only durable unresolved context in memory through `$project-memory`

Do not force premature specificity just to fill every heading.

## Step 2: Create the Artifact Set

Create artifacts in this order:

1. `AGENTS.md`
2. `PLAN.md`
3. `ARCHITECTURE.md`
4. `BACKLOG.md`
5. `.agents/memory/` via `$project-memory`

Use the reference files for structure:

- [agents-template.md](references/agents-template.md)
- [plan-template.md](references/plan-template.md)
- [architecture-template.md](references/architecture-template.md)
- [backlog-template.md](references/backlog-template.md)

These are scaffolding references, not rigid forms. Adapt the wording to the actual project, but preserve the artifact roles and their relationships.

## Step 3: Write `AGENTS.md` as the Orchestrator

Start `AGENTS.md` with a short project description.

`AGENTS.md` must be both horizontal and stateless:

- horizontal means it should contain repo-wide working rules, not implementation detail for one feature, subsystem, or experiment;
- stateless means it should not describe the current phase, temporary status, or time-bound project state.

State that changes over time belongs in `BACKLOG.md` and memory. Feature- or subsystem-specific target design belongs in `PLAN.md` and later in `ARCHITECTURE.md` once implemented.

Then define the working contract for the repo:

- required read order
- roles of `PLAN.md`, `ARCHITECTURE.md`, `BACKLOG.md`, and memory
- execution loop for day-to-day work
- update timing for each artifact
- backlog discipline and traceability rules
- how to use `.agents/memory/`
- canonical git rules unless the user explicitly asks for a different policy
- communication and testing rules if the project already has them

`AGENTS.md` should explain how memory is used, but should not restate or replace the full `project-memory` record contract. Instruct agents to use `$project-memory` for initialization and maintenance, then summarize the practical operating rules:

- read root memory first
- traverse selectively by branch and tags
- when tests fail or runtime behavior is unexpected, traverse memory or follow linked memory IDs before re-solving the problem because it may already be known
- store only durable learnings
- avoid duplicating `PLAN.md`, `ARCHITECTURE.md`, or `BACKLOG.md`
- keep open questions visible
- keep traceability between backlog items and durable memory records

If the `project-memory` skill provides a search or traversal helper, point agents to it explicitly in `AGENTS.md` for tag- and keyword-based lookup during debugging.

## Step 4: Differentiate the Other Artifacts Clearly

### `PLAN.md`

Use `PLAN.md` for the desired end state:

- product or project objective
- scope boundaries
- target architecture direction
- major implementation decisions that shape the final system
- roadmap or milestone framing
- strategic open questions

Keep it stable by default. Update it when direction changes, not for routine progress.

`PLAN.md` can stay more discursive than the other artifacts as long as the section boundaries remain clear.

### `ARCHITECTURE.md`

Use `ARCHITECTURE.md` for current implemented reality only:

- what exists now
- where it lives
- dependency and tooling shape
- implemented features
- active technical decisions that are already true

`ARCHITECTURE.md` must stay aligned with `PLAN.md`, but it is not a second copy of the plan. It should be a subset of the plan with more implementation detail and only for work that has actually landed.

Use nested numeric lists for the main architecture sections so backlog items can point to exact architecture locations without relying on prose references.

### `BACKLOG.md`

Use `BACKLOG.md` to translate the plan into milestone-based atomic work:

- stable task IDs
- explicit status markers
- short, finishable items
- explicit dependencies on other tasks or milestones so parallel work is visible
- decision-gate items when deferred choices become actionable
- references to architecture section numbers where useful
- memory IDs for memory references

If new work appears, add a task instead of hiding it in notes.
If a task needs extra context to be understandable, add a short rationale or point to the relevant memory record or architecture section.

## Step 5: Initialize Memory Through `$project-memory`

Do not create ad hoc memory files or invent a separate memory schema here. After the core artifacts exist, invoke `$project-memory` to initialize `.agents/memory/` for the repo.

Then make sure `AGENTS.md` tells future agents how to use that memory layer:

- root-first retrieval
- selective traversal
- search by tag or keyword when a bug, failed test, or repeated problem may already have memory coverage
- durable-learning write triggers
- promotion rules
- traceability with backlog work

Memory should store durable decisions, constraints, preferences, questions, risks, test results, errors, and resolutions. It should not become a diary, issue tracker, or duplicate backlog.

## Step 6: Leave Clean Deferrals

If the user does not want to decide something yet, leave a clean placeholder in the right artifact without inventing policy:

- `PLAN.md` for strategic or architectural open questions
- `BACKLOG.md` for future decision gates
- memory for durable unresolved context that should survive sessions

A good scaffold is specific where the user is decided and explicit where the user is not.

## References

- [bootstrap-discovery-checklist.md](references/bootstrap-discovery-checklist.md): minimum project information to extract or ask for before writing the scaffold
- [agents-template.md](references/agents-template.md): orchestrator structure for `AGENTS.md`
- [plan-template.md](references/plan-template.md): stable-target structure for `PLAN.md`
- [architecture-template.md](references/architecture-template.md): implemented-reality structure for `ARCHITECTURE.md`
- [backlog-template.md](references/backlog-template.md): milestone and task structure for `BACKLOG.md`

## Guardrails

- Do not collapse `PLAN.md`, `ARCHITECTURE.md`, and `BACKLOG.md` into paraphrases of each other.
- Keep `AGENTS.md` horizontal and stateless.
- Do not define memory JSON templates here; use `$project-memory`.
- Do not treat unresolved choices as settled just to make the scaffold look complete.
- Do not let `ARCHITECTURE.md` describe planned work as already implemented.
- Do not hide open questions in prose when they should be visible in the plan or backlog.
