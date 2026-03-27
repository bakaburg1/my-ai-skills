# Path Validation and Temp Files

Read this file when validating paths, choosing output directories, or
deciding where runtime artifacts and temporary files should live.

## Core Rules

- Prefer `fs::path_*()`, `fs::dir_create()`, `fs::file_exists()`, and
  related helpers over ad hoc string concatenation or base path code when
  the `fs` version is clearer.
`output_dir <- fs::path(tempdir(), "my-experiment")`
- Centralize path validation in reusable helpers when the codebase has
  more than one public path-taking interface.
`validate_path <- function(path) { ... }`
- Distinguish:
  validation: is this a syntactically acceptable path input?
  existence: does a file or directory already exist there?
  creation: should the code create the directory now?
- Trim whitespace and reject `NULL`, `NA`, and empty strings explicitly
  for user-facing path inputs.
```r
  if (!rlang::is_string(path) || is.na(path) || !nzchar(trimws(path))) {
    cli::cli_abort("{.arg path} must be a non-empty string.")
  }
  ```
- For relative-path APIs, document clearly what the base is. If the
  contract is “relative to the working directory”, do not add a second
  hidden root argument.
- For project-root-relative paths in packages, reports, or pipelines,
  prefer `here::here()` when the project already uses `here` and the root
  semantics are part of the workflow contract.
`report_path <- here::here("reports", "draft.qmd")`
- Make output directories configurable instead of hardcoding machine- or
  user-specific absolute paths.
- Write exploratory or temporary artifacts to `tempdir()` or another
  explicit temp location, not to the repository root.
`fs::path(tempdir(), "plot-preview.png")`
- In synced folders such as OneDrive or similar, keep large mutable
  caches and pipeline stores outside the synced tree when possible to
  avoid invalidations and noise.

## Avoid

- ad hoc `paste0()` path building for complex paths
- mixing validation, existence checks, and creation in scattered inline
  conditions
- mixing working-directory-relative paths and project-root-relative paths
  without documenting which convention the function expects
- hard-coded absolute paths in portable code
- writing files like `Rplots.pdf` or scratch outputs into the repo root
