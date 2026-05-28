---
name: compact-context
description: Creates long-form conversation summaries and handoff memos for the full thread. Use when summarizing a chat, handing off to another agent, or hitting token limits.
metadata:
  author: Angelo D'Ambrosio
  license: EUPL-1.2
---

# Compact Context

## Overview

Produce a detailed, structured summary of the full conversation, not just the recent turns. Prioritize information that enables another agent to continue immediately with minimal rereads.

## Core Requirements

Always include the following content:
- What was done and what is complete.
- What is currently being worked on.
- Which files were created/modified and where to look.
- What still needs to be done next.
- Key user requests, constraints, preferences, and non-obvious decisions (with rationale when available).
- Outstanding TODOs with file paths and line numbers when possible.
- Tests needed or gaps (edge cases, performance, integration, etc.).
- Open bugs, quirks, or setup steps that affect continuation.

If there was a recent `update_plan` call, repeat its steps verbatim in a dedicated section.

If the user requested a “memento” due to token limits or asked to “stop coding,” write the summary as a handoff memo and do not perform further edits.

## Output Format

Use the following sections in order. Keep them concise but complete, and cover the whole conversation. If a section has no items, write “None.”

**Summary**
A comprehensive narrative of the entire conversation, not just the end. Include goals, progress, and outcomes.

**Work Completed**
Concrete actions finished, including commands run or files created.

**In Progress**
What is actively being worked on or was last attempted.

**Files Modified**
List file paths (with line numbers when possible) and a brief note on the change.

**Decisions and Constraints**
Key choices, tradeoffs, preferences, and any constraints that must persist.

**Outstanding TODOs**
Actionable items with file paths and line numbers where possible.

**Tests and Gaps**
Missing tests, edge cases, performance, or integration concerns.

**Bugs, Quirks, Setup Notes**
Known issues, odd behavior, or setup steps that help the next agent continue.

**Plan Recap (if applicable)**
If an `update_plan` call occurred, repeat its steps verbatim here.

**Open Questions**
Clarifications needed from the user or uncertainties blocking progress.

## Style Rules

- Do not be short; cover the whole conversation.
- Prefer precise file paths and concrete identifiers.
- Keep the summary self-contained so another agent can resume without rereading the thread.
- Use clear, compact language; avoid filler.
