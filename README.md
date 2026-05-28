# agent-skills

Personal agent skills collection by Angelo D'Ambrosio — a shared source tree for skills used across multiple AI agent harnesses. Published on GitHub for backup and to share with others.

## How it syncs across harnesses

This folder is **symlinked** from each harness's skills location (Codex, Cursor, OpenCode, Claude, and similar) so the same files appear everywhere. Edit once here; all linked harnesses see the same skills. One general repository instead of maintaining separate copies per tool.

## What is in this repo

### Original skills (EUPL-1.2)

Written and maintained by Angelo D'Ambrosio. Each skill directory includes a `LICENSE.txt` and may declare `metadata.license: EUPL-1.2` in `SKILL.md`.

Examples: `r-guidelines`, `acc-memory-control`, `commit`, `docx-assistant`, `binary-docs-diff`, `apply-clearance-comments`, `project-init`, `sidecar-agent`, and others in this repository.

### Third-party skills (attributed)

Vendored or adapted from upstream projects. Each has a `NOTICE.txt` with upstream terms. These skills are **not** licensed under the EUPL.

Examples: `firecrawl`, `browser-use-cli`, `quarto-authoring`, `code-review`.

## Attribution and licenses

- **EUPL-1.2** applies only to original skills (see root [`LICENSE`](LICENSE) and each skill's `LICENSE.txt`).
- **Upstream skills**: read that skill's `NOTICE.txt` and any license declared in its `SKILL.md`.

## History rewrite note

If you clone an older revision or add a remote later, be aware this repository may have been cleaned with `git filter-repo` to remove machine-local paths and generated test artifacts. After such a rewrite, use `git push --force-with-lease` when publishing to an existing remote.
