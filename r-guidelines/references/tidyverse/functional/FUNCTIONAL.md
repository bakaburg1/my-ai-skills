# Functional Programming and Iteration

Read this file when the task involves repeated work over collections,
loop replacement, batching, side effects, or parallel execution.

If the work is mostly repeated transformations, read the purrr subtopic.
If the work is CPU-heavy or I/O-heavy enough to justify concurrency,
also read the parallelism subtopic.

## Topic Tree

- Purrr workflows, list binding, and side effects
  Read [purrr-workflows.md](purrr-workflows.md)

- Parallel execution
  Read [parallelism.md](parallelism.md)

## Defaults

- Prefer type-stable purrr functions when they improve clarity over base
  `sapply()` / `lapply()`.
`paths |> purrr::map_chr(fs::path_ext)`
- Use loops when they are clearer; use `purrr` when it makes the data
  flow more obvious or the result type more stable.
