# `AGENTS.md` Scaffold

Use `AGENTS.md` as the repo orchestrator. Start with a short project description, then define how agents must work in this repository.

Keep it horizontal and stateless: repo-wide working rules only, with time-varying state in `BACKLOG.md` and memory, and feature-specific design in `PLAN.md` or `ARCHITECTURE.md` as appropriate.

`AGENTS.md` should make it obvious how an agent is supposed to work in the repo without reading a long conversation first.

Here's a recommended structure, which can be adapted to the specific needs of the project. The general instructions should be imported as-is unless the user explicitly asks for a different workflow. The project-specific instructions should be added after the general instructions.

## Project Description

Here you should put a short description of the project, what it is, what it does, and what its goals are. This description should be kept stable and should not be updated frequently.

## Agent operative system

This repository is governed by the canonical coordination files: `AGENTS.md`, `PLAN.md`, `ARCHITECTURE.md`, `BACKLOG.md`, and `.agents/memory/`. Use them as the repo's operating system for coordination, planning, execution, and durable memory.

### Canonical coordination files

- `AGENTS.md` is the repo-wide operating manual. It defines stable, horizontal working rules for agents and contributors, explains how to navigate the other coordination files, and sets the expectations for repo hygiene, workflow discipline, and communication. It's stateless and horizontal: do not use it for live task status, implementation backlog detail, or feature-specific design.
- `PLAN.md` describes the intended end state, roadmap, and major project contracts. Update it only when the target state changes.
- `ARCHITECTURE.md` describes implemented reality only. Update it when landed code, data layout, or tooling actually changes.
- `BACKLOG.md` is the canonical execution tracker. Work to do is listed here and the work status should be updated as the project progresses. Items/milestones may be added or edited but only with the user permission.
- `.agents/memory/` stores durable decisions, constraints, risks, questions, learning points, solved issues and errors, and resolutions that should survive across sessions. It must not become a diary or duplicate the plan or backlog.

The gap between `PLAN.md` and `ARCHITECTURE.md` is expected. `BACKLOG.md` should make that gap actionable and show progress as it closes.

### Execution loop

1. Read the canonical coordination files in order:
   1. `AGENTS.md`
   2. `PLAN.md`
   3. `ARCHITECTURE.md`
   4. `BACKLOG.md`
   5. `.agents/memory/MEMORY.json`
   6. Only the child memory files needed for the task
2. Pick the next unblocked backlog item unless the user redirects the work.
3. Read `.agents/memory/MEMORY.json` first, then retrieve only the relevant child memory branches useful for the current task.
4. Perform the task.
5. Update `BACKLOG.md` to reflect status changes and any newly discovered work.
6. Update `ARCHITECTURE.md` if implemented reality changed.
7. Update `.agents/memory/` with `$project-memory` rules if durable learning was produced.
8. Update `PLAN.md` only if the target state or roadmap changed.

## Backlog discipline

- Use stable task IDs.
- Keep tasks atomic and finishable in one focused implementation effort.
- Record explicit dependencies when they matter for sequencing or parallel work.
- Keep decision gates visible as explicit backlog items.
- Reference architecture sections and memory IDs where useful.
- If a backlog item is not self-explanatory, add a short rationale or link it to the relevant memory record or architecture detail.
- When new work appears, ask user permission to add a task instead of burying it in prose.
- Expand tasks into subtasks if the need arise during implementation.

## Memory usage

Use `$project-memory` for initialization and maintenance of `.agents/memory/`.

Practical rules:

- Read `.agents/memory/MEMORY.json` first.
- Use the root `branches` list and `tag_index` to decide which child memory to open.
- Traverse selectively; do not scan the full memory tree by default.
- Use the traverse memory script described in the project-memory skill for efficient traversing.
- When tests fail, runtime behavior regresses, or a repeated issue appears, inspect relevant memory before assuming the problem is new.
- Store only durable learnings: decisions, constraints, preferences, risks, questions, test outcomes, errors, and resolutions.
- Do not store routine progress notes, raw logs, or copies of `PLAN.md`, `ARCHITECTURE.md`, or `BACKLOG.md`.
- Keep traceability by linking backlog task IDs and source files in memory records when useful.

## Git rules

- Treat `main` as the baseline branch unless the user asks for a different workflow.
[Some users may prefer to use a main-dev-branch workflow instead. Ask the user.]
- Use conventional-style commit messages. Always add the task ID as a prefix to the commit message. Always add a commit body in list form ending with a Why: element explaining the changes rationale briefly. e.g.:

```
<type>(<scope>): <backlog task id> commit title

- done 1
- done 2
Why: rationale
```

- Create a new branch for each milestone and, if necessary a sub branch for particularly invasive tasks requiring deep changes to split in many commits.
- Use conventional commits also for branch naming e.g. <type>/<milestone id>.branch-title for milestone branches or <type>/<milestone id>-<task id>.branch-title for task branches.
- !!!ALWAYS, ALWAYS, ALWAYS ask the user before commit, merge or other distructive git actions!!!
- Preserve user changes; never revert or discard work you did not create unless without asking permission.
- Snapshot meaningful baselines before major refactors.
- Keep tags human-readable and tied to actual repository milestones.

## Repo-Specific Rules

- General implementation instructions
- Production and test environment setup and management
- Coding/writing guidelines
- Testing workflow
- Branching model
- Communication format
- Code readability or documentation preferences
