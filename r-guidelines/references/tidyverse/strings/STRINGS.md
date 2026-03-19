# String Manipulation and Text Processing

Read this file when the task involves normalizing, extracting,
replacing, splitting, or formatting text.

## Core Rules

- Prefer `stringr` for consistent, pipe-friendly string handling.
- Use `fixed()`, `regex()`, and `coll()` when match semantics matter.
- Prefer string-first APIs when they make chained transformations easier
  to read.

```r
text |>
  str_to_lower() |>
  str_trim() |>
  str_replace_all("pattern", "replacement") |>
  str_extract("\\d+")
```

## Avoid

- inconsistent base string helpers when `stringr` is clearer
- hidden regex semantics when a literal or locale-aware match is needed
