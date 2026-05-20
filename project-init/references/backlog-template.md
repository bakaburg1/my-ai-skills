# `BACKLOG.md` Scaffold

Use `BACKLOG.md` as the canonical execution tracker derived from `PLAN.md`.

## Recommended Structure

### 1. Legend

Define status markers such as:

- `[ ]` pending
- `[-]` in progress
- `[x]` done
- `[!]` blocked
- `[a]` aborted/deprecated

### 2. Current Next Unblocked Task

Optionally name the next task to reduce ambiguity at session start.

### 3. Milestones

Group work into milestones or phases. Each milestone should have a short goal statement.

### 4. Atomic Tasks

Each task should have:

- a stable ID such as `P1-01`
- one finishable unit of work
- a status marker
- explicit dependency declarations on prerequisite tasks or milestones when applicable
- architecture references by numeric section such as `3.2` or `5.1`
- memory references by memory ID such as `mem-workflow-001`

If a task is not self-explanatory, add a short rationale or point to the relevant memory record or architecture section.

When a task has no prerequisite, say so only when that improves clarity.

Use `[a]` for items that were intentionally removed temporarily or definitively but should remain visible for traceability. Include a compact reason when marking an item aborted/deprecated.

### 5. Decision Gates

When the user defers a choice, create a decision-gate item and keep it visible. Use this for choices that will become actionable later.

### 6. Completion Traceability

When a task is completed, add a compact trace note if the repo workflow uses PRs, merges, or other durable references.

## Suggested Task Shape

```text
- [ ] `P2-03` Add undo and redo history. Depends on: `P2-02`. Arch: `3.2`, `5.1`. Memory: `mem-architecture-004`
```

Use milestone dependencies when the dependency is broader than one task.

## Quality Bar

If someone reads only `BACKLOG.md`, they should know what work exists, what comes next, and which open choices are intentionally deferred rather than forgotten.
