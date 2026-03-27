# String Manipulation and Text Processing

Read this file when the task involves normalizing, extracting,
replacing, splitting, or formatting text.

## Core Rules

- Prefer `stringr` for consistent, pipe-friendly string handling.
`text |> stringr::str_to_lower() |> stringr::str_trim()`
- Use `fixed()`, `regex()`, and `coll()` when match semantics matter.
`str_detect(name, fixed("RStudio"))`
- Prefer string-first APIs when they make chained transformations easier
  to read.
`str_replace_all(text, regex("\\s+"), " ")`

## Avoid

- inconsistent base string helpers when `stringr` is clearer
- hidden regex semantics when a literal or locale-aware match is needed
