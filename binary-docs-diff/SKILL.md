---
name: binary-docs-diff
description: Inspects diffs for binary documents (`.docx`, `.xlsx`, `.pptx`, `.pdf`) when normal `git diff` is not useful, especially during review.
metadata:
  author: Angelo D'Ambrosio
  license: EUPL-1.2
---

# Binary Docs Diff

## Overview
Use this skill to inspect binary document diffs without unpacking Office files or reconstructing PDF evidence by hand.
The bundled helper emits three tiers of evidence in order: extracted-text diff, package or metadata diff, and rendered visual diff.

## Skill Root

Resolve the skill root from the location of this `SKILL.md`.
Do not hardcode any host-specific skill path.

Use the bundled helper via:

```bash
python3 <SKILL_ROOT>/scripts/inspect_diff.py ...
```

## Prerequisites

Expect these local tools:

- `markitdown` for the first-pass text extraction.
- `git` when comparing the working tree file against a committed revision.
- `pdfinfo`, `pdffonts`, and `pdfimages` for PDF internals.
- `soffice` and `pdftoppm` for rendered visual diffs.
- Python packages `lxml` and `Pillow` for XML normalization and image comparison.

If a tool is missing, say which tier is unavailable and continue with the remaining evidence instead of improvising a new workflow.

## Workflow

1. Compare the committed and working versions.

   For a tracked file, prefer git mode so the helper materializes the baseline for you:

   ```bash
   python3 <SKILL_ROOT>/scripts/inspect_diff.py \
     --git-path path/to/file.docx
   ```

   To compare arbitrary files instead:

   ```bash
   python3 <SKILL_ROOT>/scripts/inspect_diff.py \
     --old /tmp/baseline.docx \
     --new ./path/to/file.docx
   ```

2. Read the helper output in this order.

   - Tier 1 `markitdown`: treat this as the primary signal for user-visible content changes.
   - Tier 2 package or metadata diff: use this when Tier 1 is empty or suspicious.
   - Tier 3 visual diff: use rendered page diffs when the change may be layout-only, image-only, or formatting-heavy.

3. Inspect the artifact directory called out by the helper.

   The top-level `report.json` summarizes every tier.
   Relevant artifacts usually include:

   - `markitdown/old.md`, `markitdown/new.md`, `markitdown/text.diff`
   - `package/` normalized OOXML parts and XML diffs for `.docx`, `.xlsx`, `.pptx`
   - `pdf/` metadata, font, and image inventory diffs for `.pdf`
   - `visual/` rendered pages and per-page diff masks

## Interpretation Rules

- If Tier 1 shows a text diff, lead with that in the review. Mention structural or visual evidence only when it changes the meaning of the diff.
- If Tier 1 is unchanged but Tier 2 changed, report style, metadata, relationship, media, or packaging changes and cite the specific parts or reports.
- If Tier 1 and Tier 2 are unchanged but Tier 3 changed, report a layout or image-only change and inspect the saved page masks before summarizing it.
- If the file type is legacy binary Office (`.doc`, `.xls`, `.ppt`), expect Tier 2 to be skipped. Use Tier 1 plus Tier 3.

## Visual Fallback

The visual tier is the extra check that catches the main blind spot you identified: layout or image-only changes that are not obvious in text extraction or XML metadata.

The helper renders both versions to page images and compares them pixel-by-pixel:

- For PDFs, it renders pages directly.
- For OOXML files, it converts the file to PDF with LibreOffice first, then renders pages.

This catches:

- moved or resized objects
- changed charts or embedded images
- font fallback or spacing regressions
- slide or worksheet layout drift that keeps the same text

It can still miss semantically important changes that render identically, such as hidden metadata, alternate text, or structurally different but visually equivalent XML.
It can also report very small rendering noise, so check the per-page percentages before escalating minor differences.
