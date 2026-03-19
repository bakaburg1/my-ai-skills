# Errors, Checks, and Tests

Read this file when changing user-facing behavior, runtime validation, or
test coverage.

## Errors and Messages

- Use `cli::cli_abort()` instead of `stop()` for user-facing fatal errors.
- Use `cli::cli_warn()` instead of `warning()` for user-facing runtime
  problems.
- Use `cli::cli_alert()` for neutral step headings.
- Use `cli::cli_alert_info()` for informational status updates that do
  not imply action.
- Use `cli::cli_alert_success()` for confirmations after a relevant or
  difficult step completes.
- Use `cli::cli_alert_warning()` for non-code cautions when results need
  careful interpretation; use `cli::cli_warn()` for runtime logical
  issues that would have used `warning()`.
- Use `cli::cli_alert_danger()` when circumstances make results highly
  unreliable but the code path itself is sound.
- Avoid `message()` and `cat()` for user-facing messaging.
- Let `cli` format vectors rather than collapsing them manually.

## Checks and Tidy-Eval Notes

- Prefer `.data`, `.env`, and tidyselect helpers over
  `utils::globalVariables()`.
- Use `utils::globalVariables()` only when pronouns cannot address the
  check note and comment the reason.
- Avoid “no visible binding for global variable” notes from
  non-standard evaluation in `dplyr`, `ggplot2`, and `data.table`.

## Testing

- Test small units during development.
- Add focused tests for edge cases, metaprogramming, and class behavior.
- For tidy-eval interfaces, test both simple column inputs and injected or
  expression-based inputs.
- For package workflows, cover integration paths as well as unit behavior.
- For targeted test runs, prefer `Rscript -e 'devtools::test(filter = "...")'`
  rather than `testthat::test_file()`.
- Use `devtools::load_all()` for small console repros, not as the default
  way to run the test suite.
