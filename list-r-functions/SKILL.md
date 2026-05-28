---
name: list-r-functions
description: Lists R function names and signatures with matching .Rd text from man/. Use when cataloging functions defined in selected R source files.
metadata:
  author: Angelo D'Ambrosio
  license: EUPL-1.2
---

# List R Functions

## Quick start

1. Run from the repo root (the working directory is used to find files).
2. Source the helper script.
3. Call `list_r_functions()` with one or more file regex patterns.

```r
source("list-r-functions/scripts/list_r_functions.R")
rd_texts <- list_r_functions(file_regex = c("R/utils.*\\.R$"))
```

## Escaping in `Rscript -e`

When running from the shell, you must escape backslashes for both the shell and R.
Prefer one of these safe patterns:

```sh
Rscript -e 'source("list-r-functions/scripts/list_r_functions.R"); list_r_functions(file_regex = c("R/utils.*\\\\.R$"))'
```

```sh
Rscript -e 'source("list-r-functions/scripts/list_r_functions.R"); list_r_functions(file_regex = c("R/utils.*[.]R$"))'
```

Note: in an R string you need `\\.` (written as `\\\\.` in the shell), i.e. escape with `\\\.` to mean a literal dot.


## Output

- Prints signatures as `name(arg1, arg2 = ...)`.
- Returns a named list where each element is the full .Rd text for that function.
- If a .Rd is missing, the list element is `"function documentation not found"`.

If a .Rd is missing for a function that starts with a dot (e.g. `.foo`), check for a `dot-foo.Rd` file in `man/` because dot-prefixed functions are documented with `dot-` filenames. If it is still missing, inspect the source file or read the body with `print(function_name)`.
