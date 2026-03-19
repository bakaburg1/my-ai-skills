# Themes

Read this file when the task is mostly about plot appearance rather than
data encoding.

## Core Rules

- Keep theme changes intentional and reusable.
- Prefer a small, consistent theme layer over ad hoc styling at each
  plot call.
- Make typography, spacing, and background choices coherent with the
  plot's purpose.

## Avoid

- scattering the same `theme()` tweaks across many plots
- style changes that obscure the data
