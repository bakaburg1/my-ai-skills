# Profiling and Benchmarking

Read this file when code is slow or you are considering a performance
rewrite.

## Tool Selection

- Use `profvis` for complex or unknown bottlenecks.
- Use `bench::mark()` to compare alternative implementations.
- Use `system.time()` only for quick directional checks.
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
