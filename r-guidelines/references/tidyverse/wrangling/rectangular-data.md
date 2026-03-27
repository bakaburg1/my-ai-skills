# Rectangular Data Manipulation

Read this file when the task is about joins, summaries, reshaping,
grouping, selecting columns, or converting between tidy and legacy data
shapes.

## Core Rules

- Prefer `.by` for single-operation grouping.
`summarise(data, mean_value = mean(value), .by = group)`
- Use `group_by()` only when multiple grouped steps must share state or
  the grouping logic is genuinely complex.
`data |> group_by(group) |> mutate(rank = min_rank(value)) |> summarise(top = max(rank))`
- In column-aware verbs such as `mutate()`, `summarise()`, `filter()`,
  and `group_by()`, use `.data$col` or `.data[["col"]]` for individual
  variables.
`mutate(data, ratio = .data$numerator / .data$denominator)`
- Use `join_by()` instead of character-vector join specs.
`left_join(x, y, by = join_by(id == record_id))`
- Use `multiple` and `unmatched` when match quality matters.
`left_join(x, y, by = join_by(id), multiple = "error", unmatched = "error")`
- Use `pick()` inside data-masking verbs to work with subsets of
  columns.
`mutate(data, total = rowSums(pick(starts_with("score_"))))`
- Use `across()` when applying a function to several columns.
`summarise(data, across(where(is.numeric), mean), .by = group)`
- Use `reframe()` for multi-row summaries.
`reframe(data, top_two = head(sort(value, decreasing = TRUE), 2), .by = group)`
- Use `case_when(..., .default = ...)` for default branches rather than
  `TRUE ~ ...`.
`case_when(score >= 90 ~ "A", score >= 80 ~ "B", .default = "C")`
- In base subsetting, keep `drop = FALSE` when the result must remain a
  data frame or matrix, but do not treat it as universally necessary;
  it is redundant for many multi-column subsets.
`mat[, 1, drop = FALSE]`
- When list-level attributes matter, preserve them deliberately; if a
  full-list mapping would drop outer attributes, use `x[] <- ...` rather
  than rebinding the whole object.
`x[] <- lapply(x, as.character)`
- In selection verbs and tidyselect arguments such as `select()`,
  `rename()`, and `.by`, use tidyselect helpers or quoted column names,
  not `.data$col`.
`select(data, starts_with("score"), all_of(extra_cols))`

## Avoid

- `group_by() |> summarise() |> ungroup()` when `.by` is enough
- `by = c("a" = "b")` joins
- superseded `gather()` and `spread()`
- manually deduplicating already set-like operations
