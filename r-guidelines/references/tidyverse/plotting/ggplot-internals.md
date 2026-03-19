# GGplot Internals and Replacement Semantics

Read this file when a task needs to inspect or replace existing plot
components, detect whether a `ggplot2` constructor supplied `mapping`
or `data` explicitly, or preserve layer/facet structure during edits.

## Core Rules

- When you need to know whether positional ggplot arguments were
  explicitly supplied, resolve the call with `rlang::call_match()`
  before inspecting the named formals.
- Use `layer$mapping` when preserving or replacing layer mappings; do
  not assume `layer$constructor$mapping` is populated.
- Treat `layer$data` carefully: it may be a `waiver()` object even when
  the constructor data is `NULL`, so do not assume it is always a data
  frame.
- For full replacement semantics of layers, scales, or facets, prefer
  direct object assignment over rebuilding calls when the object model
  already supports it.
- When mutating facet parameters, rebuild the facet with
  `facet_wrap()`/`facet_grid()` using the existing params merged with the
  edits so ggplot2 validates the current args. If the facet expression
  depends on local symbols, evaluate it in the plot environment.

## Patterns

```r
call <- rlang::call_match(ggplot2::geom_point(aes(x, y)))
mapping <- call$mapping
layer <- plot$layers[[1]]
mapping <- layer$mapping
```

## Avoid

- assuming constructor internals always hold the canonical layer state
- treating `layer$data` as a plain data frame without checking
- reconstructing a whole plot call when a direct object replacement is
  sufficient
