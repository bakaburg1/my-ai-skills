# Package Development with `targets`

Read this file when a package under development is consumed by a
`targets` pipeline in the same session.

## Core Rules

- If the session depends on local package source, load it with
  `devtools::load_all()` before running pipeline helpers.
- When `targets` helper commands must see the loaded dev package, run
  them in-process with `callr_function = NULL`; otherwise they may use
  the installed package in a subprocess.
- If the loaded package must be visible during pipeline execution, keep
  execution in the main process or otherwise ensure the worker sees the
  same code.
- Run `targets` reads and loads from the project whose store and root
  the pipeline expects. Do not assume a separate package repo has the
  right working directory for `tar_read()` or `tar_load()`.
- Use simple stage markers or similar metadata only when they make a
  repeated pipeline step idempotent and easier to reason about.

## Avoid

- calling `tar_outdated()` or similar helpers in a way that silently
  switches from loaded source to installed package code
- mixing package development and pipeline execution without being
  explicit about the working directory and active store
