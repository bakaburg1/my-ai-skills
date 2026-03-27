# Store Layout, Experiments, and Git Worktrees

Read this file when deciding where the `targets` store should live, how
to run experiments safely, or how to work from git worktrees.

## Core Rules

- Keep the main long-lived store outside the repository when the repo is
  synced, shared, or frequently cloned into worktrees. This reduces
  invalidation noise and keeps large mutable state out of git.
- Parameterize the store location via environment or config rather than
  hardcoding `_targets/` assumptions into every workflow.
- If the repo uses `.Rprofile` or `.Renviron` to set store roots or
  package paths, source that project config before the first `targets`
  command in a fresh session. In a worktree, if a local config file is
  absent, resolve the main checkout's config from the common git dir
  instead of assuming the worktree has its own copy.
- Before any `targets` command, check the active store explicitly with
  `targets::tar_config_get("store")`.
`active_store <- targets::tar_config_get("store")`
- Treat production or shared stores as protected. Do not run mutating
  operations against them casually.
- For experiments and especially for git worktrees, create an isolated
  experiment store in a local temp or other non-repo path, and point the
  session to it with `targets::tar_config_set(store = exp_store)`.
`exp_store <- file.path(tempdir(), "targets-exp-store")`
- If you need fast incremental experiments, seed the experimental store
  from the production store deliberately rather than mutating the
  production store directly.
- Keep only small pointers or metadata in the repo. Do not check in
  active experimental stores.
- When a worktree needs gitignored runtime inputs from the main repo,
  copy them non-destructively with `rsync -a --ignore-existing`, then
  confirm they remain ignored with `git check-ignore -v`.
- Diagnose failures through `tar_meta()` and related `targets` APIs, not
  by poking store internals directly.
- For temporary scripted experiments, use `targets::tar_dir()` around
  `targets::tar_script()` so temporary scripts do not overwrite repo
  files.
```r
  targets::tar_dir({
    targets::tar_script(list(targets::tar_target(x, 1)))
  })
  ```

## Avoid

- assuming `_targets/` in the current checkout is the active store
- mutating shared stores without first verifying the path and intent
- keeping experiment stores inside worktrees or synced folders
- copying runtime inputs in a way that overwrites files already present
  in the worktree
- debugging by manually editing store internals
