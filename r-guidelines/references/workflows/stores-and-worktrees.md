# Store Layout, Experiments, and Git Worktrees

Read this file when deciding where the `targets` store should live, how
to run experiments safely, or how to work from git worktrees.

## Core Rules

- Keep the main long-lived store outside the repository when the repo is
  synced, shared, or frequently cloned into worktrees. This reduces
  invalidation noise and keeps large mutable state out of git.
- Parameterize the store location via environment or config rather than
  hardcoding `_targets/` assumptions into every workflow.
- Before any `targets` command, check the active store explicitly with
  `targets::tar_config_get("store")`.
- Treat production or shared stores as protected. Do not run mutating
  operations against them casually.
- For experiments and especially for git worktrees, create an isolated
  experiment store in a local temp or other non-repo path, and point the
  session to it with `targets::tar_config_set(store = exp_store)`.
- If you need fast incremental experiments, seed the experimental store
  from the production store deliberately rather than mutating the
  production store directly.
- Keep only small pointers or metadata in the repo. Do not check in
  active experimental stores.
- When a worktree needs gitignored runtime inputs from the main repo,
  copy them non-destructively and confirm they remain ignored.
- Diagnose failures through `tar_meta()` and related `targets` APIs, not
  by poking store internals directly.
- For temporary scripted experiments, use `targets::tar_dir()` around
  `targets::tar_script()` so temporary scripts do not overwrite repo
  files.

## Avoid

- assuming `_targets/` in the current checkout is the active store
- mutating shared stores without first verifying the path and intent
- keeping experiment stores inside worktrees or synced folders
- debugging by manually editing store internals
