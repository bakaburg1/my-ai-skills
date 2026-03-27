# Scalar and Argument Validation

Read this file when validating scalar strings, numbers, integer-like
indices, optional arguments, or caller-supplied expressions.

## Core Rules

- Prefer `rlang` scalar helpers over manual type-and-length checks when
  they materially reduce edge cases.
- Use `rlang::is_string(x)` for scalar strings, and pair it with
  `!rlang::is_named(x)` when you must reject named strings.
```r
  if (!rlang::is_string(path) || rlang::is_named(path)) {
    cli::cli_abort("{.arg path} must be a single unnamed string.")
  }
  ```
- Use `rlang::is_scalar_double(x)` for numeric scalar validation.
`if (!rlang::is_scalar_double(alpha)) cli::cli_abort("{.arg alpha} must be one number.")`
- Use `rlang::is_scalar_integerish(x, finite = TRUE)` for scalar integer
  validation instead of hand-rolled `is.numeric()` plus rounding logic.
```r
  if (!rlang::is_scalar_integerish(index, finite = TRUE)) {
    cli::cli_abort("{.arg index} must be one finite integer-like value.")
  }
  ```
- Use `rlang::is_empty(x)` when the contract is “empty or not” instead
  of open-coded `!is.null(x) && length(x) > 0` checks.
`if (rlang::is_empty(items)) cli::cli_abort("{.arg items} must not be empty.")`
- Do not rely on `rlang::is_scalar_character()` for path-like inputs if
  `NULL`, `NA`, or blank strings need special handling; use a dedicated
  path validator instead.
- Use base `missing()` when you need to know whether an argument with a
  default was supplied. `rlang::is_missing()` does not answer that
  question reliably for defaulted arguments.
`if (missing(value)) cli::cli_abort("{.arg value} must be supplied explicitly.")`
- When you need the caller expression for messages, capture it with
  `enquo()` and report it with `rlang::as_label()`. Do not assume
  `enexpr()` preserves the right expression in all cases.
```r
  var_quo <- rlang::enquo(var)
  var_label <- rlang::as_label(var_quo)
  ```
- For tidyselect-like inputs, prefer one consistent resolution path
  rather than multiple branches unless missing-column semantics truly
  differ.

## Avoid

- repeating handwritten `is.character(x) && length(x) == 1` checks
- spelling emptiness checks as layered `NULL` plus `length()` conditions
- assuming unnamedness from `rlang::is_string()`
- using `enexpr()` when the error message depends on the caller label
- broad coercion before checking whether the original input was valid
