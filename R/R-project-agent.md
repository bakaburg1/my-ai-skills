For any requested change or task which is not trivial, you should always assess the situation, test your assumptions in the console (e.g., small repros or focused checks), make tests, and then present a detailed plan of action before ANY change to the code. Run relevant unit tests after the edit (not before), unless explicitly requested otherwise.
You'll enact your plan of action after the plan has been approved by the user.

**Exception:** The planning and wait for approval process is not needed when asked to add documentation.

## ⚠️ IMPORTANT: When In Doubt, Ask First

Do not blindly interpret and enact changes if:

- The requirements or desiderata are not clear.
- There are two or more drastically different approaches to solve an issue.
- Some evidence you found would lead you to take bold or significant choices.
- You noticed something else that seems to be wrong or not working as expected while trying to perform a requested task.

**Always ask to confirm the course of action before proceeding.** When in doubt, ask.

## R guidelines

Read and follow these guidelines:
https://raw.githubusercontent.com/bakaburg1/my-ai-skills/main/R/R-rules.md
https://raw.githubusercontent.com/bakaburg1/my-ai-skills/main/R/unit-testing.md

## Track learning points

Update progressively this document when you learn something about how to better perform your tasks related to this project. This could be coding best practices, implementation details, overall design decisions, corrections and remarks from the user, etc.

Update the list below with the new learning points:

```yaml
- name: cli alert level conventions
  description: Use cli_alert for action logs, cli_alert_info for supplemental details, cli_warn for runtime logical issues that would have used warning(), and cli_alert_warning for non-code cautions when results need careful interpretation (e.g., low-quality input, incomplete data).
  scope: logging/messages
- name: cli alert capture
  description: cli_alert* emits messages that expect_message() can capture in tests; expect_warning() will not.
  scope: testing
- name: roxygen generation only
  description: Never write .Rd or NAMESPACE manually; always run devtools::document() to update documentation and exports.
  scope: documentation
- name: git write confirmation
  description: Always ask for explicit user confirmation before performing any write operation to the git repository, such as commit, push, or other actions that modify git history.
  scope: git operations
- name: dependency additions via usethis
  description: Always add packages with usethis::use_package using min_version = TRUE when updating dependencies.
  scope: dependencies
- name: cli alert bullet handling
  description: cli_alert* functions do not support named bullet vectors; emit one cli_alert* call per bullet message instead of passing a named vector.
  scope: logging/messages
- name: devtools test filter usage
  description: Run tests with Rscript -e 'devtools::test(filter = \"...\")' (no testthat::test_file); use devtools::load_all() only for small console repros, not test runs.
  scope: testing
```

## Dependency Management (`renv`)

`renv` is turned off by default in this repository. The repo dependency status
(i.e. the `renv.lock` file) is brought up to date only when stable versions are
reached.
