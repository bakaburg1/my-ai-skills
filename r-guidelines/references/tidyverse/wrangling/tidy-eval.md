# Programmable Data-Masking and Tidy Evaluation

Read this file when writing package APIs or any interface where users can
pass columns, column sets, or expressions into data-masking verbs.

## Preferred Patterns

- Use `{{}}` to forward a user-supplied column expression.
- Use `.data[[var]]` when `var` is a character vector.
- Use `.env$var` for environment values that might collide with columns.
- Use `!!` to inject one expression or value.
- Use `!!!` to splice several expressions or arguments.
- Use `list2()` when collecting dynamic dots.

```r
my_summary <- function(data, group_var, summary_var) {
  data |>
    group_by({{ group_var }}) |>
    summarise(mean_val = mean({{ summary_var }}))
}

my_mean <- function(data, var) {
  data |>
    summarise(mean = mean(.data[[var]]))
}

my_group_by <- function(.data, vars) {
  .data |>
    group_by(across(all_of(vars)))
}
```

## Programming Guidance

- Prefer explicit pronouns to avoid `R CMD check` notes and masking bugs.
- For `ggplot2` aesthetics, use the same pronouns to avoid global
  variable notes.
- Avoid `utils::globalVariables()` unless pronouns cannot solve the
  problem, and document the rationale in comments.
- If a helper accepts filter-style condition strings, split comma-
  separated clauses before parsing them; `rlang::parse_exprs()` does not
  interpret commas as implicit conjunctions.
- Use `sym()`, `syms()`, `data_sym()`, and `data_syms()` only when
  symbol construction is actually needed.
- Document programmable arguments with roxygen tags for data masking,
  tidy selection, and dynamic dots.

## Avoid

- `eval(parse(...))`
- `get()` inside data-masking code
- mixing embrace and defuse/inject patterns without a reason
