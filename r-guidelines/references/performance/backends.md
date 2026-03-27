# Backend and Scaling Choices

Read this file when choosing between base R, tidyverse, `data.table`,
parallel purrr, or `vctrs`.

## Data Backend Rules

- Use `dplyr` when readability, maintainability, and modern joins or
  window logic matter most.
`data |> dplyr::summarise(mean_value = mean(value), .by = group)`
- Use `data.table` when datasets are very large, reference semantics are
  beneficial, or maximum throughput is critical.
```r
  data.table::as.data.table(data)[, .(mean_value = mean(value)), by = group]
  ```
- Use base R when the task is simple or dependencies must stay minimal.
`mean_value <- mean(data$value)`

## Parallelism

- Use `in_parallel()` only for expensive, independent work.
- Avoid parallelism for cheap vectorized operations or small workloads.

## vctrs

- Use `vctrs` when type stability, consistent coercion, and robust vector
  behavior matter more than minimal overhead.
`count <- vctrs::vec_cast(count, integer())`
- Prefer base primitives for very simple hot loops when the safety
  features are not needed.

## Avoid

- parallelizing fast operations
- switching backends for style alone
- adding `vctrs` complexity to one-off scripts without a concrete benefit
