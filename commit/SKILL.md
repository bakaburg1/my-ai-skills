---
name: commit
description: Guide for drafting and applying git commits in a repository. Use when the user asks to write or apply commits, stage changes, or organize commits by mode (E/I/G) for current changes.
---

# Commit

## Overview

Use this skill to draft and apply commits for the current git repository while matching the project's commit style and following explicit user mode instructions.

## Workflow

- Read `references/commit.md` for the full procedure and rules.
- Ensure you are inside a git repo and detect the requested mode (E/I/G or ad hoc).
- Collect diffs (prefer staged; otherwise include tracked and untracked changes).
- Inspect recent commit messages to mirror tone and format.
- Draft one commit at a time, ask for confirmation, then apply the commit.

## Resources

- `references/commit.md`: authoritative commit workflow and formatting rules.
