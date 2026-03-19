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
- Prefer the base pipe `|>` for chaining. Use `_` only as a named
  placeholder argument or as the head of an extraction chain; otherwise
  use an anonymous function.
  Example: `data |> lm(formula = y ~ x, data = _)`
- Do not deduplicate set operations manually; for example,
  `unique(intersect(...))` is unnecessary.
- Use `case_when(..., .default = ...)` for default branches rather than
  `TRUE ~ ...`.
- Use `%||%` when optional inputs may be `NULL` and an inline fallback is
  clearer than a separate branch.
- Prefer `fs` for nontrivial filesystem work such as path composition or
  directory creation when it makes the intent clearer than base helpers.

## Function Structure

- Keep functions focused and type-stable where possible.
- Use up to two arguments on one line; put longer signatures one argument
  per line.
- For package-local helpers tied to a parent function, prefer a leading
  `.` naming convention.
- Use a single-line function signature only for short argument lists.
- For longer signatures, put one argument per line.

## Comments and Documentation

- Explain what the code is doing and why, not the edit history.
- Put comments above the code they describe, not inline at the end.
- Start comments with a capital letter.
- Use roxygen for package functions that should have help pages. Mark
  internal-only helpers with `@keywords internal`, avoid `@noRd`, and
  prefix conventional internal helpers with `.`.
- End roxygen sentences with a full stop, except for the title line.
- Use backticks for code formatting in roxygen.
- Avoid `@importFrom` when calls are already namespaced in code.
- Wrap roxygen at roughly 80 columns.
- Use `# Section Name ----` for section headers in scripts and helpers.

## Namespacing

- Namespace all functions except those from `dplyr`, `stringr`, and base
  R.
- Never call `library()` inside functions.

## Interactive Debugging

- When exploring data interactively, use `print()`, `str()`, or
  `glimpse()` to inspect objects.

## Read Next

- For grouped data work, joins, tidyselect, or metaprogramming:
  [../tidyverse/wrangling/WRANGLING.md](../tidyverse/wrangling/WRANGLING.md)
- For package docs, imports, errors, and tests:
  [../packages/PACKAGES.md](../packages/PACKAGES.md)
