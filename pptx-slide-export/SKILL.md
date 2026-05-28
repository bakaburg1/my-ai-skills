---
name: pptx-slide-export
description: Exports PowerPoint slides to medium-resolution images via soffice and pdftoppm. Use when rendering slide previews or inspecting layout without native image export.
metadata:
  author: Angelo D'Ambrosio
  license: EUPL-1.2
---

# Pptx Slide Export

## Overview
Use this skill to convert a deck into review-ready PNG slides with consistent, moderate resolution.
Default output targets visual inspection speed, not print-quality rendering.

## Workflow
1. Confirm required tools exist: `soffice` and `pdftoppm`.
2. Run `scripts/export_slides.sh` with input deck and output folder.
3. Open a few exported images and check text wrapping, spacing, line breaks, and overlap.
4. Report issues slide-by-slide with concrete fixes.

## Quick Start
```bash
"$(pwd)/.agents/skills/pptx-slide-export/scripts/export_slides.sh" \
  "Presentations/01_workshop_overview.pptx" \
  "Presentations/01_workshop_overview_figures" \
  150
```

Arguments:
- `arg1`: input `.ppt` or `.pptx`
- `arg2`: output directory
- `arg3` (optional): DPI, default `150`
- `arg4` (optional): output prefix, default `slide`

Output:
- PNG files named like `slide_01.png`, `slide_02.png`, ...
- One intermediate PDF in a temp directory (auto-cleaned)

## Review Checklist
- Detect literal escaped newlines (`\\n`) shown as text.
- Detect title or bullet overflow/cropping.
- Detect inconsistent spacing or unexpected font fallback.
- Detect object overlap and off-canvas elements.

## Troubleshooting
- If `soffice` is missing, install LibreOffice.
- If `pdftoppm` is missing, install Poppler.
- If outputs are too heavy, lower DPI (for example `120`).
- If text is hard to read, raise DPI to `160-180`.
