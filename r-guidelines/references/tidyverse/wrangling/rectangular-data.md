# Rectangular Data Manipulation

Read this file when the task is about joins, summaries, reshaping,
grouping, selecting columns, or converting between tidy and legacy data
shapes.

## Core Rules

- Prefer `.by` for single-operation grouping.
- Use `group_by()` only when multiple grouped steps must share state or
  the grouping logic is genuinely complex.
- In column-aware verbs such as `mutate()`, `summarise()`, `filter()`,
  and `group_by()`, use `.data$col` or `.data[["col"]]` for individual
  variables.
- Use `join_by()` instead of character-vector join specs.
- Use `multiple` and `unmatched` when match quality matters.
- Use `pick()` inside data-masking verbs to work with subsets of
  columns.
- Use `across()` when applying a function to several columns.
- Use `reframe()` for multi-row summaries.
- Use `case_when(..., .default = ...)` for default branches rather than
  `TRUE ~ ...`.
- When list-level attributes matter, preserve them deliberately; if a
  full-list mapping would drop outer attributes, use `x[] <- ...` rather
  than rebinding the whole object.
- In selection verbs and tidyselect arguments such as `select()`,
  `rename()`, and `.by`, use tidyselect helpers or quoted column names,
  not `.data$col`.

## Example Patterns

```r
data |>
  summarise(mean_value = mean(value), .by = category)

transactions |>
  inner_join(companies, by = join_by(company == id))

transactions |>
  inner_join(
    companies,
    by = join_by(company == id),
    multiple = "error",
    unmatched = "error"
  )

data |>
  summarise(
    across(where(is.numeric), mean, .names = "mean_{.col}"),
    .by = group
  )
```

## Avoid

- `group_by() |> summarise() |> ungroup()` when `.by` is enough
- `by = c("a" = "b")` joins
- superseded `gather()` and `spread()`
- manually deduplicating already set-like operations
