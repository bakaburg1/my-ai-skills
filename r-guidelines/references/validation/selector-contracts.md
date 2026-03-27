# Selector Contracts

Read this file when validating column selectors, quoted column names,
or other selector-backed inputs.

## Core Rules

- When a helper accepts column selectors, resolve them with one
  consistent path rather than branching on string-vs-symbol forms unless
  the missing-column behavior truly differs.
- If the helper only needs resolved column names, `names(dplyr::select(data,
  ...))` is often enough. Use `tidyselect::eval_select()` when you need
  positions or more control over selection resolution.
`resolved <- names(dplyr::select(data, tidyselect::all_of(cols)))`
- For quoted names, validate them with `all_of()`/`any_of()` instead of
  treating them as bare symbols.
`select(data, all_of(cols))`
- If a user-facing filter expression is supplied as a string, split
  comma-separated clauses before parsing; `rlang::parse_exprs()` does
  not treat commas as clause separators.
```r
  clauses <- strsplit(filters, "\\s*,\\s*")[[1]]
  exprs <- rlang::parse_exprs(clauses)
  ```

## Avoid

- accepting selector strings without a single, explicit resolution path
- feeding comma-separated filter clauses directly to `parse_exprs()`
