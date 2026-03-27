# Profiling and Benchmarking

Read this file when code is slow or you are considering a performance
rewrite.

## Tool Selection

- Use `profvis` for complex or unknown bottlenecks.
`profvis::profvis({ slow_pipeline(input) })`
- Use `bench::mark()` to compare alternative implementations.
`bench::mark(old = old_impl(data), new = new_impl(data))`
- Use `system.time()` only for quick directional checks.
`system.time(readr::read_csv(path))`
- Use `Rprof()` only when base-R-only tooling is required.

## Workflow

1. Profile the real workflow on realistic input sizes.
2. Identify the dominant bottleneck.
3. Benchmark only the hotspot alternatives.
4. Check both runtime and memory behavior.
5. Keep the simpler implementation unless the gain is meaningful.

## Avoid

- optimizing without measurement
- assuming loops, base R, or tidyverse are always slower or faster
- introducing complex code for marginal gains
