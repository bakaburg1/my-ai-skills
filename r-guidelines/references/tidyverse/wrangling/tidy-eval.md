# Programmable Data-Masking and Tidy Evaluation

Read this file when writing package APIs or any interface where users can
pass columns, column sets, or expressions into data-masking verbs.

## Preferred Patterns

- Use `{{}}` to forward a user-supplied column expression.
`summarise(data, mean = mean({{ var }}))`
- Use `.data[[var]]` when `var` is a character vector.
`summarise(data, mean = mean(.data[[var]]))`
- Use `.env$var` for environment values that might collide with columns.
`filter(data, .data$value > .env$threshold)`
- Use `!!` to inject one expression or value.
`summarise(data, !!name := mean(value))`
- Use `!!!` to splice several expressions or arguments.
`summarise(data, !!!summary_exprs)`
- Use `list2()` when collecting dynamic dots.
`args <- rlang::list2(...)`

## Programming Guidance

- Prefer explicit pronouns to avoid `R CMD check` notes and masking bugs.
`mutate(data, z = .data$x + .env$offset)`
- For `ggplot2` aesthetics, use the same pronouns to avoid global
  variable notes.
`ggplot(data, aes(x = .data$time, y = .data$value)) + geom_line()`
- Avoid `utils::globalVariables()` unless pronouns cannot solve the
  problem, and document the rationale in comments.
`utils::globalVariables("..density..")  # only for legacy ggplot code`
- If a helper accepts filter-style condition strings, split comma-
  separated clauses before parsing them; `rlang::parse_exprs()` does not
  interpret commas as implicit conjunctions.
```r
  clauses <- strsplit(filters, "\\s*,\\s*")[[1]]
  exprs <- rlang::parse_exprs(clauses)
  ```
- Use `sym()`, `syms()`, `data_sym()`, and `data_syms()` only when
  symbol construction is actually needed.
`cols_syms <- rlang::syms(cols)`
- Document programmable arguments with roxygen tags for data masking,
  tidy selection, and dynamic dots.
`#' @param var <[`data-masking`][rlang::args_data_masking]> Column to summarise.`

## Avoid

- `eval(parse(...))`
- `get()` inside data-masking code
- mixing embrace and defuse/inject patterns without a reason
