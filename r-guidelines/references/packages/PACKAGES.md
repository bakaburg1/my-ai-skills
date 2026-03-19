# Package Development and Testing

Read this file for package code, roxygen, dependency choices, testing,
developer workflows, and user-facing errors or messages.

## Default Rules

- Use `cli` for user-facing alerts, warnings, and aborts.
- Keep dependencies deliberate and minimal.
- Never edit `NAMESPACE` manually; regenerate it.
- Test frequently during iteration and add focused coverage for edge
  cases.
- For nontrivial changes, start with a small console repro to test your
  assumptions before editing, then back the change with focused tests.
- Before changing a package function, inspect its source and roxygen
  docs so the current contract is explicit.
- When you need to inspect a package function body, use
  `devtools::load_all()` and then `print(function_name)` so the source
  comes from the loaded package rather than the installed copy.

## Topic Tree

- Dependencies, docs, and developer workflow
  Read [dependencies-docs.md](dependencies-docs.md)

- Errors, checks, and tests
  Read [errors-testing.md](errors-testing.md)
