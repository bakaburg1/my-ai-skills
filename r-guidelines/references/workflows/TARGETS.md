# Pipelines and `targets`

Read this file when designing, editing, or debugging `_targets.R`,
target helpers, stores, or report pipelines built on `targets`. If the
pipeline renders Quarto outputs, also read
[quarto-pipelines.md](quarto-pipelines.md).

## Topic Tree

- Store layout, experiments, and git worktrees
  Read [stores-and-worktrees.md](stores-and-worktrees.md)

- Package development with `targets`
  Read [package-dev.md](package-dev.md)

- Quarto and report pipelines
  Read [quarto-pipelines.md](quarto-pipelines.md)

## Defaults

- Keep pipelines deterministic and side-effect aware.
- Put reusable pipeline helpers in `R/` or sourced helper files, not as
  inline helper function definitions inside `_targets.R`.
- Keep `_targets.R` focused on setup, configuration, and target
  assembly.
`_targets.R` should mostly hold `tar_option_set()` and `list(tar_target(...))`
- Treat the active store path as explicit state that must be checked
  before mutating operations.
`store <- targets::tar_config_get("store")`
