---
name: commit
description: Guide for drafting and applying git commits in a repository. Use when the user asks to write or apply commits, stage changes, or organize commits by mode (E/I/G) for current changes.
---

# Commit

## Overview

Use this skill to draft and apply commits for the current git repository while matching the project's commit style and following explicit user mode instructions.

## Modes

- **E**: commit everything in one commit
- **I**: commit each file individually
- **G**: group files smartly into ordered commits (default)
- Or follow ad hoc instructions the user provides

## Workflow

1. **Check Environment**: Ensure you are inside a git repo (`git rev-parse --show-toplevel`); if not, state the error and stop.
2. **Detect Changes**: List changed/staged files. If mode is not provided, use G by default. If no changes, report and stop.
3. **Collect Diffs**:
    - Prefer staged: `git diff --cached`.
    - If empty, use tracked changes (`git diff`) plus untracked files via `git status --porcelain`.
    - For untracked files, use `git diff --no-index /dev/null "<file>"` or `cat`.
    - When inspecting a diff, **check all of it**, not just the first 50 lines.
4. **Optional Context**: Check the contents of `DESCRIPTION`, `README.r?md` (prefer Rmd), and any obviously relevant files to help understand the project.
5. **Identify Backlog**: Check if a backlog exists (e.g., `BACKLOG.md` or `.agents/memory/backlog.md`). If it exists, try to identify the relevant `<backlog id>` for the current task.
6. **Group and Stage**:
    - **Mode E**: Stage all changes.
    - **Mode I/G**: Stage only the target file(s) per commit. Order from least dependent to most dependent (utilities/config/docs first, then core logic, then tests/integration).
7. **Learn Style and History**:
    - **Commit Style**: Inspect recent commits (`git log -n 10 --format='%h%n%s%n%b%n---'`) to mirror tone and formatting. Ensure the whole commit body is visible (do not use `--oneline`).
    - **Commit Content**: For each modified file, inspect that file’s commit history (`git log -n 10 --follow --format='%h%n%s%n%b%n---' -- <file>`) to align with prior intent and patterns (increase N if the file changes rarely).
    - **Consistency**: Be careful to note commit labels/types/scopes in the file’s history and keep new labels consistent. You may also inspect a short repo-level log, but do not rely on it alone for style or labeling.
8. **Draft and Propose**:
    - **List Files**: Always list the files included in the proposed commit.
        - If <= 10 files: List them explicitly.
        - If > 10 files: Describe the group generally without listing every file (e.g., "Updating 15 CSS components in root-relative/path/to/folder").
    - **Format Message**:
        Follow the Conventional Commits style guidelines:

        ```
        <type>(<scope>): <backlog id> commit title

        - item 1
        - item 2
        Why: rationale behind the changes
        ```

        - **Title**: Short, imperative, and concise.

        - `<type>`: The category of change. Standard types include `feat` (new features), `fix` (bug fixes), `docs` (documentation), `style` (formatting), `refactor` (restructuring), `test` (adding tests), and `chore` (maintenance).
        - `<scope>`: The specific part of the codebase affected (e.g., `ui`, `core`, `api`, or a subject name like `commit` for this skill, or a function name/group). Mirror existing scope patterns found in history.
        - `<backlog id>`: Only include if a backlog (e.g. BACKLOG.md or similar) exists and an ID is identifiable (e.g., `AC-123` or `P1-01`).
        - `Why: rationale`: A brief explanation of the "why" behind the changes at the bottom of the body.
9. **Confirm and Apply**:
    - Present the drafted message and the list/description within the proposal for review.
    - Explicitly ask for confirmation before applying.
    - Execute the commit via `git commit -F -` by piping the message.
10. **Post-Commit**: Show `git status -sb` and the commit hash/message text after finishing.

## Rules

- Do not list all future commits at once; focus on the current one and proceed only after it is committed.
- If a commit fails, report the error and stop.
- If you cannot generate or apply a commit, explain why.
