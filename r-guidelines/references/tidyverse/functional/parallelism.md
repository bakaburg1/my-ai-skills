# Parallel Execution

Read this file when repeated work is expensive enough to justify
parallel overhead.

## Core Rules

- Use `in_parallel()` only for expensive, independent work.
- Avoid parallelism for cheap vectorized operations or small workloads.
- Profile first; parallelism is usually a scaling decision, not a style
  choice.

## Avoid

- parallelizing fast operations
- using parallelism to compensate for an inefficient algorithm
