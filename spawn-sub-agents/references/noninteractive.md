# Noninteractive Codex Notes (Condensed)

## 1. Basic Usage
1. Run a one-shot task with `codex exec "<prompt>"`.
2. Progress streams to stderr; the final message prints to stdout.
3. Use `-o` or `--output-last-message <path>` to write the final message to a file.

## 2. Permissions
1. Default is a read-only sandbox.
2. Allow edits with `--full-auto`.
3. Allow broader access with `--sandbox danger-full-access` only in controlled environments.

## 3. Machine-Readable Output
1. Use `--json` for JSONL event output, suitable for piping into tools like `jq`.
2. Use `--output-schema <schema.json>` to request structured final output.

## 4. Resume
1. Use `codex exec resume --last "<prompt>"` to continue the last session.
2. Use `codex exec resume <SESSION_ID>` to target a specific session.

## 5. CI Authentication
1. `codex exec` can use saved CLI auth.
2. In CI, set `CODEX_API_KEY` for noninteractive runs.

## 6. Git Repository Requirement
1. `codex exec` expects a Git repo.
2. Use `--skip-git-repo-check` only if the environment is safe.
