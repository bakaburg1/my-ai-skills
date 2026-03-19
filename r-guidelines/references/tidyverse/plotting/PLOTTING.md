# Plotting and Visualization

Read this file when creating, modifying, or reviewing `ggplot2` output.
Use it for decisions about geoms, aesthetics, scales, guides, themes,
facets, labels, and annotations.

## Core Rules

- Build plots in layers so the data, geometry, and styling choices are
  easy to inspect separately.
- Keep the visual encoding explicit: map data to aesthetics on purpose,
  not by accident.
- Prefer scales and themes that communicate intent instead of relying on
  defaults.
- Use faceting when comparison is the actual task and separate plots
  when the comparisons are genuinely different.

## Read Next

- For theme-heavy or reusable plot styling decisions:
  inspect [themes.md](themes.md)
- For axis, legend, and annotation adjustments:
  inspect [guides-and-labels.md](guides-and-labels.md)
- For plot object replacement, layer inspection, or ggplot internals:
  inspect [ggplot-internals.md](ggplot-internals.md)
