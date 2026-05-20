---
name: markdown-section-index
description: Index and extract sections from Markdown-like documents, including .md, .qmd, .rmd, and other files that use # heading structure. Use when Codex needs to navigate a long Markdown/Quarto/R Markdown file, list its section hierarchy, locate headings, or retrieve one or more sections by exact or fuzzy heading title.
---

# Markdown Section Index

Use this skill to navigate long Markdown-like files without loading the whole file into context.

## CLI

Run the bundled Python command:

```bash
python scripts/md_section_index.py path/to/file.md
```

Common options:

```bash
# Print a heading index with line numbers and hierarchy.
python scripts/md_section_index.py file.md

# Return sections by exact heading title.
python scripts/md_section_index.py file.md --section "Section title"

# Return multiple sections.
python scripts/md_section_index.py file.md --section "Section 1 title" --section "Section 1.1 title"

# Allow fuzzy matching on heading titles.
python scripts/md_section_index.py file.md --section "section tit" --fuzzy

# Emit JSON for downstream parsing.
python scripts/md_section_index.py file.md --json
```

## Workflow

1. Run the command without `--section` first to see the document index.
2. Use exact section names when possible.
3. Add `--fuzzy` when the requested title is approximate, misspelled, or shortened.
4. Prefer `--json` when another script or agent step needs stable structured output.

The script treats ATX headings (`#`, `##`, etc.) as section boundaries, skips headings inside fenced code blocks, and returns each requested section through the start of the next heading at the same or higher level.
