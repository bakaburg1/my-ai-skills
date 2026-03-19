# Performance and Backend Choices

Read this file when speed, memory use, scale, or backend selection is a
real concern. Do not optimize first and justify later.

## Default Rules

- Profile before optimizing.
- Prefer algorithmic improvements over micro-optimizations.
- Keep the readable version unless measurement justifies extra
  complexity.
- Benchmark realistic workloads, not toy examples.
- Use `profvis` to find unknown bottlenecks, `bench::mark()` to compare
  alternatives, `system.time()` for quick checks, and `Rprof()` only
  when base-R profiling is required.

## Topic Tree

- Profiling and benchmarking workflow
  Read [profiling.md](profiling.md)

- Backend and scaling choices
  Read [backends.md](backends.md)
