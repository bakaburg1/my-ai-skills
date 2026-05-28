---
name: markdown-section-index
description: Indexes and extracts sections from Markdown-like documents (.md, .qmd, .rmd). Use when navigating long docs or retrieving sections by heading.
metadata:
  author: Angelo D'Ambrosio
  license: EUPL-1.2
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
