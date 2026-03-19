# Purrr Workflows

Read this file when mapping, walking, reducing, or binding list outputs.

## Core Rules

- Prefer `map()` plus `list_rbind()` over superseded `map_dfr()`.
- Prefer `map()` plus `list_cbind()` over superseded `map_dfc()`.
- Use `walk()` and `walk2()` for side effects.
- Prefer `map_*()` variants when the result type should be enforced.

```r
models <- data_splits |>
  map(\(split) train_model(split)) |>
  list_rbind()

walk2(data_list, plot_names, \(df, name) {
  p <- ggplot(df, aes(x, y)) + geom_point()
  ggsave(name, p)
})
```

## Avoid

- `map_dfr()` and `map_dfc()`
- `sapply()` when a type-stable result is expected
- using `purrr` when a straightforward loop is easier to read
