# Dependencies, Documentation, and Workflow

Read this file when editing package metadata, roxygen docs, imports, or
 development workflows.

## Dependencies

- Add dependencies only when they provide material value in correctness,
  maintainability, or user experience.
- Use base R for straightforward utilities when an extra dependency would
  be disproportionate.
- Add package dependencies with
  `usethis::use_package("pkg", type = "Imports", min_version = TRUE)` rather
  than manually pinning package versions in `DESCRIPTION`.
- Put optional packages in `Suggests:` and gate them with
  `rlang::check_installed()` when needed.
- Prefer built-in R functions or well-maintained tidyverse equivalents
  over unnecessary dependencies.
- For data import/export, prefer `rio` or similar tidyverse-friendly
  packages when they materially improve safety or clarity.
- Declare dependencies in `DESCRIPTION` under `Imports:` or `Suggests:`
  and namespace calls with `pkg::fun()`.

## Documentation

- Document exported functions and any complex public behavior.
- Use backticks instead of `\\code{}` in roxygen.
- Include precise tags for data-masked, tidy-select, and dynamic-dots
  parameters where relevant.
- Use `devtools::document()` to refresh docs and `NAMESPACE`.
- Avoid `@importFrom` when functions are already namespaced in code.
- For repeatedly used packages inside a function, `@importFrom` can be
  appropriate, but do not duplicate imports when you already call
  `pkg::fun()`.

## Iteration Workflow

- Use `devtools::load_all()` during development.
- Use `Rscript -e '...'` for quick checks, taking care to avoid shell
  expansion issues.
- Allow long timeouts for `devtools::check()` from the shell.
- When full R help text is required, use
  `utils:::.getHelpFile(help("fn", package = "pkg"))`.
- Do not call `library(pkg)` inside functions.
