# Backend and Scaling Choices

Read this file when choosing between base R, tidyverse, `data.table`,
parallel purrr, or `vctrs`.

## Data Backend Rules

- Use `dplyr` when readability, maintainability, and modern joins or
  window logic matter most.
- Use `data.table` when datasets are very large, reference semantics are
  beneficial, or maximum throughput is critical.
- Use base R when the task is simple or dependencies must stay minimal.

## Parallelism

- Use `in_parallel()` only for expensive, independent work.
- Avoid parallelism for cheap vectorized operations or small workloads.

## vctrs

- Use `vctrs` when type stability, consistent coercion, and robust vector
  behavior matter more than minimal overhead.
- Prefer base primitives for very simple hot loops when the safety
  features are not needed.

## Avoid

- parallelizing fast operations
- switching backends for style alone
- adding `vctrs` complexity to one-off scripts without a concrete benefit
