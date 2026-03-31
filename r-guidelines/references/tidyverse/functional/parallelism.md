# Parallel Execution

Read this file when repeated work is expensive enough to justify
parallel overhead.

## Core Rules

- Use `in_parallel()` only for expensive, independent work.
- Avoid parallelism for cheap vectorized operations or small workloads.
- Profile first; parallelism is usually a scaling decision, not a style
  choice.

## Mirai Backends

- Use `mirai` when you need daemon-backed parallel mapping for repeated
  independent work and can keep the worker state serializable.
- If `mirai` and `carrier` are guaranteed dependencies for the package
  or project, `purrr::in_parallel()` is a good default when you want one
  map call that automatically falls back to sequential execution without
  extra branching.
- In `mirai::mirai_map()`, use `...` for objects that must exist in the
  worker environment and `.args` for arguments that should be passed to
  `.f`.
- Prefer one worker function shared by the sequential and `mirai`
  branches, then pass the shared state explicitly once instead of
  duplicating the worker body.
- Capture package-local helper functions in the outer scope before you
  hand the worker to `mirai`. If the remote body re-resolves an internal
  helper by name, it may miss mocked bindings or fail to see the same
  function object that the parent session used.
- If a worker depends on several sibling values, bundle them into a
  local closure or a single args object and reuse that capture. Do not
  rebuild the execution state inside the remote body unless you need
  remote-specific state.
- Test both the sequential fallback and the daemon-backed branch with a
  small reprex before you widen the implementation. The worker closure
  should behave identically in both paths.
- Use the project convention for collection when available, such as
  `jobs[mirai::.progress]`, so progress reporting and promise resolution
  stay in one place.

### Do

```r
# Pass the helper through `...` so the daemon can see it, then pass the
# worker arguments through `.args`.
run_mirai <- function(xs) {
  helper <- function(x, multiplier) {
    x * multiplier
  }

  jobs <- mirai::mirai_map(
    xs,
    function(x, multiplier) {
      helper(x, multiplier)
    },
    helper = helper,
    .args = list(
      multiplier = 2
    )
  )

  jobs[mirai::.progress]
}

run_mirai(1:4)
```

```r
# Use `in_parallel()` when mirai is guaranteed and the worker can receive
# the needed state as explicit arguments.
run_parallel <- function(xs) {
  helper <- function(x, multiplier) {
    x * multiplier
  }

  worker <- purrr::in_parallel(
    function(x, multiplier, helper) {
      helper(x, multiplier)
    },
    helper = helper,
    multiplier = 2
  )

  purrr::map_int(xs, worker)
}

run_parallel(1:4)
```

### Don't

```r
# This looks up `helper()` from the worker's parent scope instead of
# passing it through `...`, which is fragile once the work is serialized.
run_mirai_bad <- function(xs) {
  helper <- function(x, multiplier) {
    x * multiplier
  }

  jobs <- mirai::mirai_map(xs, function(x) {
    helper(x, 2)
  })

  jobs[mirai::.progress]
}

run_mirai_bad(1:4)
```

```r
# This worker depends on `helper` from the outer function, but it is not
# declared inside the worker body or passed through `...`.
run_parallel_bad <- function(xs) {
  helper <- function(x, multiplier) {
    x * multiplier
  }

  worker <- purrr::in_parallel(
    function(x) {
      helper(x, 2)
    }
  )

  purrr::map_int(xs, worker)
}

run_parallel_bad(1:4)
```

## Avoid

- parallelizing fast operations
- using parallelism to compensate for an inefficient algorithm
- reselecting internal helpers inside the remote worker when the helper
  was already selected in the parent scope
- assuming a remote worker can discover parent-scope bindings unless you
  have explicitly captured them in the worker closure or `.args`
