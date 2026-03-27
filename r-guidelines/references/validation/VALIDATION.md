# Input Validation and Defensive Interfaces

Read this file when designing or reviewing user-facing function
interfaces, argument validation, scalar checks, coercion, or defensive
error handling. If the inputs are paths or directories, also read
[../filesystem/FILESYSTEM.md](../filesystem/FILESYSTEM.md). If the
inputs are tidyselect or data-masked expressions, also read
[../tidyverse/wrangling/tidy-eval.md](../tidyverse/wrangling/tidy-eval.md).

## Topic Tree

- Scalar and argument validation
  Read [scalar-validation.md](scalar-validation.md)

- Selector contracts
  Read [selector-contracts.md](selector-contracts.md)

## Defaults

- Validate early, close to the public interface.
- Prefer clear reusable validators over scattered ad hoc checks when the
  same contract appears repeatedly.
- Keep validation messages actionable and specific about the offending
  argument or value.
`cli::cli_abort("{.arg cols} must select at least one column.")`
- Test surprising edge cases directly in the console before settling on
  a validation pattern.
