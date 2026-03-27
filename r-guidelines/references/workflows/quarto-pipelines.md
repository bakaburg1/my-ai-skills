# Quarto and Report Pipelines

Read this file when `targets` is used to render Quarto reports or other
multi-format document outputs.

## Core Rules

- Keep render helpers and shared logic out of `_targets.R`; place
  reusable functions in `R/` or sourced helper files.
- For Quarto project pipelines, treat Quarto inspect metadata as the
  source of truth for expected outputs. Do not assume runtime overrides
  alone control what `tar_quarto()` tracks.
- In project mode, remember that Quarto `--output-dir` paths are
  interpreted relative to the project root.
`"output"` means `project_root/output`, not the current subdirectory
- Keep heavyweight computation out of authoring documents when pipeline
  outputs can be read instead.

## Avoid

- inline helper definitions in report documents or `_targets.R`
- output-path assumptions that ignore Quarto project semantics
