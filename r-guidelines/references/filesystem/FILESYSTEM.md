# File Systems and Paths

Read this file when code creates directories, validates file or
directory inputs, writes artifacts, works with temp files, or must
behave safely in synced folders or git worktrees. If the main issue is
argument validation, also read
[../validation/VALIDATION.md](../validation/VALIDATION.md).

## Topic Tree

- Path validation and creation
  Read [paths-and-tempfiles.md](paths-and-tempfiles.md)

## Defaults

- Prefer `fs` for nontrivial path handling and directory creation.
`scratch_dir <- fs::path(tempdir(), "my-run")`
- Separate path validation from existence checks from creation.
- Keep path semantics explicit: either relative to the working directory,
  relative to a project root, or absolute by contract.
`report_path <- here::here("reports", "draft.qmd")`
- Do not leave temporary artifacts in the repository root.
- Keep heavy mutable runtime state out of synced directories and out of
  the git worktree unless there is a clear reason not to.
