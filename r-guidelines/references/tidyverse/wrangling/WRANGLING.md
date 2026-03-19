# Data Wrangling and Manipulation

Read this file when the task is about rectangular data pipelines:
filtering, joining, reshaping, summarizing, grouping, selecting columns,
or making package-safe data-masking code.

If the task is purely about column manipulation or joins, read the
rectangular-data subtopic. If it is programmable or package-facing, also
read the tidy-eval subtopic.

## Topic Tree

- Rectangular data manipulation, joins, and column operations
  Read [rectangular-data.md](rectangular-data.md)

- Programmable data-masking and tidy evaluation
  Read [tidy-eval.md](tidy-eval.md)

## Defaults

- Prefer modern `dplyr` and `tidyr` patterns over legacy `plyr` or base
  workarounds when readability and correctness improve.
- Use `.by`, `join_by()`, `pick()`, `across()`, and `reframe()` where
  they make the code simpler and safer.
- Use `.data` and `.env` deliberately in programmatic code.
