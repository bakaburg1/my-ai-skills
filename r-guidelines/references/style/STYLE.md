# Style and Structure

Read this file when deciding how R code should look and how logic should
be split. If a task also involves package APIs, errors, or tests, also
read [../packages/PACKAGES.md](../packages/PACKAGES.md).

## Default Style

- Write easy-to-understand but efficient R code.
- Favor tidyverse functions when they improve readability, reliability,
  or safety, not by reflex.
- Avoid trivial helper functions. Split logic into helpers only when the
  code is reused, error-prone, or needs targeted tests.
- Use `snake_case` for variables and functions.
- Treat variable names as nouns and function names as verbs.
- Avoid dots except for S3 methods and conventional internal helpers.
- Keep lines under roughly 80 characters and break at logical boundaries.
- Use `\()` for short anonymous functions.
`paths |> purrr::map(\(path) fs::file_info(path))`
- Prefer the base pipe `|>` for chaining. Use `_` only as a named
  placeholder argument or as the head of an extraction chain; otherwise
  use an anonymous function.
`data |> lm(formula = y ~ x, data = _)`
- Do not deduplicate set operations manually; for example,
  `unique(intersect(...))` is unnecessary.
- Use `case_when(..., .default = ...)` for default branches rather than
  `TRUE ~ ...`.
`case_when(x < 0 ~ "neg", x == 0 ~ "zero", .default = "pos")`
- Use `%||%` when optional inputs may be `NULL` and an inline fallback is
  clearer than a separate branch.
`label <- label %||% "unknown"`
- Prefer `fs` for nontrivial filesystem work such as path composition or
  directory creation when it makes the intent clearer than base helpers.
`report_dir <- fs::path("reports", "draft")`

## Function Structure

- Keep functions focused and type-stable where possible.
- Use up to two arguments on one line; put longer signatures one argument
  per line.
```r
  fit_model <- function(
    data,
    response,
    predictors,
    family = stats::gaussian()
  ) {
  ```
- For package-local helpers tied to a parent function, prefer a leading
  `.` naming convention.
`.validate_inputs <- function(path, overwrite) { ... }`
- Use a single-line function signature only for short argument lists.
`add_flag <- function(data, flag) { ... }`
- For longer signatures, put one argument per line.
```r
  build_report <- function(
    data,
    title,
    output_dir,
    overwrite = FALSE
  ) {
  ```

## Comments and Documentation

- Explain what the code is doing and why, not the edit history.
- Put comments above the code they describe, not inline at the end.
```r
  # Reuse the cached file if it is still current.
  if (fs::file_exists(path)) return(path)
  ```
- Start comments with a capital letter.
- Use roxygen for package functions that should have help pages. Mark
  internal-only helpers with `@keywords internal`, avoid `@noRd`, and
  prefix conventional internal helpers with `.`.
```r
  #' Validate one path-like input
  #'
  #' @keywords internal
  .validate_path <- function(path) { ... }
  ```
- End roxygen sentences with a full stop, except for the title line.
- Use backticks for code formatting in roxygen.
``#' Return a `data.frame` with one row per file.``
- Avoid `@importFrom` when calls are already namespaced in code.
- Wrap roxygen at roughly 80 columns.
- Use `# Section Name ----` for section headers in scripts and helpers.
`# Data Preparation ----`

## Namespacing

- Namespace all functions except those from `dplyr`, `stringr`, and base
  R.
`fs::dir_create(path)` and `cli::cli_abort("Bad input.")`
- Never call `library()` inside functions.

## Interactive Debugging

- When exploring data interactively, use `print()`, `str()`, or
  `glimpse()` to inspect objects.
`dplyr::glimpse(df)`

## Read Next

- For grouped data work, joins, tidyselect, or metaprogramming:
  [../tidyverse/wrangling/WRANGLING.md](../tidyverse/wrangling/WRANGLING.md)
- For package docs, imports, errors, and tests:
  [../packages/PACKAGES.md](../packages/PACKAGES.md)
