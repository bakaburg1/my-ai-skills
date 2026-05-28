---
name: r-guidelines
description: R coding and review guidelines with task-specific references. Use when writing, editing, or reviewing R code, packages, dplyr/tidyr/ggplot2, targets, or tests.
metadata:
  author: Angelo D'Ambrosio
  license: EUPL-1.2
---

# R Guidelines

Use this skill when writing, reviewing, refactoring, or testing R code.
The default stance is modern, readable, package-quality R with current
tidyverse conventions where they materially improve clarity or safety.

## Core Instructions

- Prefer readable, idiomatic R first. Optimize only after profiling.
- Use the native pipe `|>` rather than `%>%`.
- Prefer modern tidyverse APIs, especially `dplyr` 1.1+ features such as
  `.by`, `join_by()`, `pick()`, `across()`, and `reframe()`.
- In data-masking code, use `.data` and `.env` deliberately; for
  programmable interfaces, use modern `rlang` patterns.
- Use `cli` for user-facing messages and actionable errors.
- Keep code package-safe: namespace functions deliberately, avoid hidden
  dependencies, and avoid patterns that trigger unnecessary `R CMD check`
  notes.
- Prefer `snake_case`; keep functions small enough to reason about; add
  helpers only when reuse, testing, or complexity justifies them.
- Use type-stable outputs and modern purrr/vctrs patterns when that
  improves correctness.
- Validate inputs deliberately, especially user-facing scalars, selectors,
  and filesystem paths.
- Prefer `fs` for nontrivial path and directory work.
- Treat `targets` stores as deliberate infrastructure, not incidental
  repo state.
- When an external assistant would benefit from exact R context,
  optionally use `btw::btw(..., clipboard = FALSE)` to gather prompt-ready
  descriptions of functions, packages, data frames, or environments.
- When applied to a function, `btw::btw()` gives the function body and
  surrounding context, not the full Rd help page.
- When you need the full Rd help text for a function, use
  `help("<fn>", package = "<package>") |> utils:::.getHelpFile() |>
  tools::Rd2txt()`.
`btw::btw(dplyr::mutate, mtcars, clipboard = FALSE)`

## Workflow

1. Read this file for the default rules.
2. Read the most relevant topic references below before changing code.
3. If the task touches multiple areas, read multiple topic files.
4. If you are unsure whether a topic applies, be slightly loose and read
   one more reference file rather than one fewer.
5. If you need to hand R context to an LLM, prefer `btw` over ad hoc
   paraphrases or partial copies.
6. Apply the guidance directly while implementing or reviewing code.

## Topic Map

- Style and structure
  Use when deciding naming, spacing, comments, helper boundaries,
  function layout, namespacing, or general code shape.
  Read [references/style/STYLE.md](references/style/STYLE.md)

- Input validation and defensive interfaces
  Use when validating user-facing arguments, scalar inputs, selectors,
  coercion, missing values, path-like inputs, or when deciding whether
  `rlang` helpers are safer than ad hoc checks.
  Read [references/validation/VALIDATION.md](references/validation/VALIDATION.md)

- File systems and paths
  Use when creating directories, handling relative paths, validating
  file or directory inputs, writing temporary artifacts, or working in
  synced folders and git worktrees.
  Read [references/filesystem/FILESYSTEM.md](references/filesystem/FILESYSTEM.md)

- Pipelines and `targets`
  Use when creating or editing `_targets.R`, target helpers, store
  layout, dev-mode workflows, Quarto/report pipelines, or experimental
  runs in git worktrees.
  Read [references/workflows/TARGETS.md](references/workflows/TARGETS.md)

- Data wrangling and manipulation
  Use when cleaning, reshaping, joining, summarizing, filtering,
  grouping, selecting columns, or maintaining legacy rectangular-data
  pipelines with `dplyr`, `tidyr`, `tibble`, `plyr`, or base R.
  Read [references/tidyverse/wrangling/WRANGLING.md](references/tidyverse/wrangling/WRANGLING.md)

- Functional programming and iteration
  Use when mapping, reducing, walking, batching, parallelizing repeated
  work, or deciding between loops and `purrr` pipelines.
  Read [references/tidyverse/functional/FUNCTIONAL.md](references/tidyverse/functional/FUNCTIONAL.md)

- String manipulation and text processing
  Use when normalizing, extracting, replacing, or formatting text, or
  deciding between `stringr` and base R string helpers.
  Read [references/tidyverse/strings/STRINGS.md](references/tidyverse/strings/STRINGS.md)

- Plotting and visualization
  Use when building, modifying, or reviewing `ggplot2` charts, layers,
  aesthetics, scales, guides, themes, facets, labels, or annotations.
  Read [references/tidyverse/plotting/PLOTTING.md](references/tidyverse/plotting/PLOTTING.md)

- Performance and backend choices
  Use when code may be slow, memory-heavy, parallelizable, or when
  deciding between base R, tidyverse, `data.table`, `vctrs`, or lower
  level approaches.
  Read [references/performance/PERFORMANCE.md](references/performance/PERFORMANCE.md)

- Package development and testing
  Use when editing package code, roxygen docs, dependencies, errors,
  `R CMD check` issues, `devtools` workflows, or tests.
  Read [references/packages/PACKAGES.md](references/packages/PACKAGES.md)

- Object systems and class design
  Use when designing classes or choosing between S3, S7, S4, and `vctrs`.
  Read [references/oop/OOP.md](references/oop/OOP.md)

## Default Review Lens

When reviewing R code, check for:

- outdated tidyverse patterns where modern replacements are clearer
- unsafe tidy evaluation or ambiguous data-masking
- weak dependency hygiene or avoidable namespace leakage
- avoidable performance work done without profiling evidence
- missing tests around metaprogramming, edge cases, and class behavior
