# Errors, Checks, and Tests

Read this file when changing user-facing behavior, runtime validation, or
test coverage.

## Errors and Messages

- Use `cli::cli_abort()` instead of `stop()` for user-facing fatal errors.
`cli::cli_abort("{.arg path} must be a single existing directory.")`
- Use `cli::cli_warn()` instead of `warning()` for user-facing runtime
  problems.
`cli::cli_warn("Some rows were dropped because {.field id} was missing.")`
- Use `cli::cli_alert()` for neutral step headings.
`cli::cli_alert("Rendering quarterly report")`
- Use `cli::cli_alert_info()` for informational status updates that do
  not imply action.
`cli::cli_alert_info("Using cached input files.")`
- Use `cli::cli_alert_success()` for confirmations after a relevant or
  difficult step completes.
`cli::cli_alert_success("Model fit completed.")`
- Use `cli::cli_alert_warning()` for non-code cautions when results need
  careful interpretation; use `cli::cli_warn()` for runtime logical
  issues that would have used `warning()`.
`cli::cli_alert_warning("Interpret this trend carefully because the sample is small.")`
- Use `cli::cli_alert_danger()` when circumstances make results highly
  unreliable but the code path itself is sound.
`cli::cli_alert_danger("The input file is stale; results may be misleading.")`
- Avoid `message()` and `cat()` for user-facing messaging.
- Let `cli` format vectors rather than collapsing them manually.
`cli::cli_abort("Unknown columns: {bad_cols}.")`

## Checks and Tidy-Eval Notes

- Prefer `.data`, `.env`, and tidyselect helpers over
  `utils::globalVariables()`.
`summarise(data, mean = mean(.data[[var]]))`
- Use `utils::globalVariables()` only when pronouns cannot address the
  check note and comment the reason.
`utils::globalVariables("..density..")  # old ggplot stat interface`
- Avoid “no visible binding for global variable” notes from
  non-standard evaluation in `dplyr`, `ggplot2`, and `data.table`.

## Testing

- Test small units during development.
- Add focused tests for edge cases, metaprogramming, and class behavior.
- For tidy-eval interfaces, test both simple column inputs and injected or
  expression-based inputs.
- For package workflows, cover integration paths as well as unit behavior.
- For whole-package inspections, prefer `devtools::check()` over a full
  `devtools::test()` run, and run `devtools::document()` before checking.
- For targeted test runs, prefer `Rscript -e 'devtools::test(filter = "...")'`
  rather than `testthat::test_file()`.
`Rscript -e 'devtools::test(filter = "validate_path")'`
- Use targeted `devtools::test(filter = "...")` runs only for scoped
  iteration after an issue is found; once fixed, rerun
  `devtools::document()` and `devtools::check()`.
- Use `devtools::load_all()` for small console repros, not as the default
  way to run the test suite.
