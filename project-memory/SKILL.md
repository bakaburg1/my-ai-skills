---
name: project-memory
description: Manages `.agents/memory/` for durable project context, including initialization and selective retrieval. Use when reading or updating project memory.
metadata:
  author: Angelo D'Ambrosio
  license: EUPL-1.2
---

# Project Memory

## Overview

Use this skill to maintain `.agents/memory/` as a durable, selective-retrieval memory layer for a project. It stores context that matters across sessions without turning memory into a diary or duplicating the rest of the project state.

## What This Skill Owns

- `.agents/memory/MEMORY.json`
- child `MEMORY.json` files in branch folders
- root tags and tag index
- branch routing and selective traversal
- durable memory record content and promotion rules

## What This Skill Does Not Own

- backlog files
- plans or specs
- issue trackers
- PR workflow
- routine project status outside memory

Other artifacts may reference memory IDs when that helps preserve context, but those artifacts remain external to this skill.

## Memory Model

1. The root file is the entry point.
2. Branch files store narrower, topic-scoped learnings.
3. Tags connect related items across branches.
4. Root metadata routes retrieval; it is not a place for full history.
5. Lower branches stay specific; higher branches only keep generalized lessons.

## Read Workflow

1. Read `.agents/memory/MEMORY.json` first.
2. Inspect `branches` and `tag_index`.
3. Open only the child memories needed for the task.
4. Stop once you have enough context to continue.

## Write Workflow

1. Write only durable learnings.
2. Store specific details in the lowest useful branch.
3. Promote only generalized lessons upward.
4. Keep routine chatter, raw logs, and ephemeral notes out of memory.
5. If a memory item depends on an external plan, backlog item, or other project file, note that source in the record instead of copying the file's content.

## Record Contract

Each `MEMORY.json` file uses:

```text
version
scope
summary
updated_at
memories
branches
local_tags (optional)
```

The root file also includes:

```text
canonical_tags
tag_index
```

Each memory record should include:

```text
id
kind
title
summary
details
tags
source
last_verified_at
promote_to_parent
```

Allowed `kind` values:

```text
decision
constraint
preference
question
risk
test-result
error
resolution
```

## Example Structures

### Root `MEMORY.json`

```json
{
  "version": 1,
  "scope": "project-root",
  "summary": "Root memory for the project.",
  "updated_at": "2026-03-19T12:00:00Z",
  "memories": [
    {
      "id": "mem-root-001",
      "kind": "decision",
      "title": "Default branch convention",
      "summary": "Use `main` as the default branch.",
      "details": "This is the stable baseline for the project.",
      "tags": ["workflow", "branching"],
      "source": {
        "type": "user-instruction",
        "detail": "Project branch policy",
        "captured_at": "2026-03-19T12:00:00Z"
      },
      "last_verified_at": "2026-03-19T12:00:00Z",
      "promote_to_parent": false
    }
  ],
  "branches": [
    {
      "slug": "workflow",
      "path": ".agents/memory/workflow",
      "description": "Workflow rules and coordination notes.",
      "tags": ["workflow", "repo-ops"]
    }
  ],
  "canonical_tags": {
    "domains": ["workflow", "architecture", "product"],
    "record_kinds": ["decision", "constraint", "preference", "question", "risk", "test-result", "error", "resolution"]
  },
  "tag_index": {
    "workflow": [".agents/memory/workflow/MEMORY.json#mem-workflow-001"]
  }
}
```

### Branch `MEMORY.json`

```json
{
  "version": 1,
  "scope": "workflow",
  "summary": "Workflow memory branch.",
  "updated_at": "2026-03-19T12:00:00Z",
  "memories": [
    {
      "id": "mem-workflow-001",
      "kind": "question",
      "title": "Where should backlog references live?",
      "summary": "Track them externally, but link them from memory when needed.",
      "details": "If a backlog item helps explain a memory record, include its identifier in `source.detail` or `details`.",
      "tags": ["workflow", "cross-reference"],
      "source": {
        "type": "user-correction",
        "detail": "Memory can reference external backlog items for context",
        "captured_at": "2026-03-19T12:00:00Z"
      },
      "last_verified_at": "2026-03-19T12:00:00Z",
      "promote_to_parent": false
    }
  ],
  "branches": [],
  "local_tags": ["workflow", "cross-reference"]
}
```

### Single memory record

```json
{
  "id": "mem-architecture-004",
  "kind": "constraint",
  "title": "Selective traversal only",
  "summary": "Do not scan the full tree by default.",
  "details": "Open only the branch files needed for the current task.",
  "tags": ["retrieval", "constraint"],
  "source": {
    "type": "repo-contract",
    "detail": "Memory system rules",
    "captured_at": "2026-03-19T12:00:00Z"
  },
  "last_verified_at": "2026-03-19T12:00:00Z",
  "promote_to_parent": true
}
```

## Guardrails

- Do not use memory as a diary.
- Do not scan the full tree by default.
- Do not duplicate plans or task trackers in memory.
- Do not let open questions disappear.
- Do not promote branch-local specifics too early.
