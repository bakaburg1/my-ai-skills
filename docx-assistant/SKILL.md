---
name: docx-assistant
description: Skill for cross-platform .docx reader/editor. Summarize and navigate large documents, detect/retain tracked changes, generate new tracked changes, read/add/reply to comments (threaded when possible). Use when asked to edit or read Word documents.
---

# Word DOCX Assistant

## Interaction-start reminder (MANDATORY)

At the start of every interaction where this skill is activated **and the task includes writing edits, comments, or tracked changes**, explicitly remind the user:

* “Default author for comments and tracked changes is **AI helper**, unless you specify otherwise.”

## Default authorship

* Unless user states otherwise, all new comments and tracked changes MUST be authored as:

  * Author: `AI helper`
  * (If tool supports it) Initials: `AI`
* If the user specifies another author, use it consistently for **both** comments and revisions.

## Portability and paths (MANDATORY)

This skill must remain portable across different agent hosts; always locate scripts and resources relative to the skill root (the folder containing this SKILL.md).

* NEVER hardcode `.codex/...` or any app-specific skill path.
* ALWAYS reference scripts/resources using paths **relative to the skill root** (the folder containing this SKILL.md).
* All scripts MUST resolve the skill root via their own location (works even when the skill folder is symlinked).

## Tooling (deterministic)

Use the bundled .NET tool `docxctl` (invoked via wrapper scripts) for all DOCX operations:

* Fast navigation of long documents (outline + search + targeted extracts)
* Reading comments + threaded reply metadata (best effort)
* Detecting existing tracked changes
* Adding new tracked changes while preserving existing ones (default)
* Compare-based redlining (only when safe/explicit)

**Wrapper entrypoints (preferred)**

* macOS/Linux: `./scripts/docxctl.sh <command> [args...]`
* Windows: `./scripts/docxctl.ps1 <command> [args...]`

Note: the `docxctl.sh` wrapper lives inside the `scripts/` folder. If the executable bit isn't set, invoke it via `bash <SKILL_ROOT>/scripts/docxctl.sh`.

## One-time setup (from ANY working directory)

Use the bootstrap script from the skill root.

* macOS/Linux: `bash <SKILL_ROOT>/scripts/bootstrap.sh`
* Windows: `powershell -ExecutionPolicy Bypass -File <SKILL_ROOT>\scripts\bootstrap.ps1`

Bootstrap must:

* Ensure `dotnet` is available (use Homebrew on macOS if `brew` exists)
* Restore/build `tools/docxctl`
  If bootstrap cannot install prerequisites, STOP and tell the user the exact manual steps needed.

## Core workflow (efficient + safe)

### 0) Always detect document state first

Run:

* `docxctl status --in <file.docx>`

This must return (at minimum):

* `hasTrackedChanges: true/false`
* `hasComments: true/false`
* `commentModel: "legacy" | "modern" | "unknown"`
* `estimatedLength: { paragraphs, headings }`

### 1) Long-document navigation (MANDATORY for big docs)

Do NOT full-dump long documents.
Use progressive disclosure:

1. Outline first:

* `docxctl outline --in <file.docx> --out outline.json`

2. Locate relevant areas by search:

* `docxctl find --in <file.docx> --query "<text|regex>" --max 50 --out hits.json`

**Search semantics (IMPORTANT):** `find` searches on a *normalized plain-text view* of the document, not raw XML nodes. Formatting boundaries (e.g., bold/italics split across runs) are ignored by concatenating text across runs within each paragraph before matching. `find` SHOULD support case-insensitive matching and regex, and MUST return match offsets that can be mapped back to a stable anchor (paragraph id + start/end character offsets in the normalized paragraph text).

3. Pull only the needed context:

* `docxctl extract --in <file.docx> --anchor <anchor.json> --before 2 --after 2 --out excerpt.json`

Only if the doc is small (or the user explicitly asks for full inspection), run:

* `docxctl inspect --in <file.docx> --out inspect.json`

### 2) Editing WITHOUT destroying existing tracked changes (DEFAULT)

If `hasTrackedChanges == true`, apply edits by directly creating revision markup in-place:

* `docxctl apply-tracked --in <file.docx> --ops <ops.json> --out <tracked.docx> --author "AI helper"`

This mode MUST:

* Preserve all existing `<w:ins>`, `<w:del>`, comment anchors, and comment IDs
* Add new revisions by inserting proper revision elements (`<w:ins>`, `<w:del>`, etc.) with new IDs and metadata
* Touch only the minimal necessary runs/paragraphs

**Note:** Direct tracked edits are constrained (by design) to operations that can be precisely anchored (see “Ops schema”).

### 3) Compare-based redlining (ONLY when safe/explicit)

Compare-based redlining is excellent for generating Word-native revisions, but it can scramble/duplicate diffs if the input already contains revisions.

`docxctl redline` may be used ONLY if one is true:

* `hasTrackedChanges == false`, or
* the user explicitly requests “rebase” (accept/reject all existing changes first), or
* the operation is performed on a copy where existing revisions were first flattened intentionally.

Workflow:

1. Make a clean edited copy (no new tracked changes):

* `docxctl apply --in <file.docx> --ops <ops.json> --out <edited.docx>`

2. Redline:

* `docxctl redline --original <file.docx> --edited <edited.docx> --out <tracked.docx> --author "AI helper"`

### 4) Comments: read, add, reply (threaded when possible)

* List comments:

  * `docxctl comments list --in <file.docx> --out comments.json`
* Add a comment:

  * `docxctl comments add --in <file.docx> --anchor <anchor.json> --text "<...>" --out <out.docx> --author "AI helper"`
* Reply to a comment (TRY THREADED FIRST):

  * `docxctl comments reply --in <file.docx> --commentId <id> --text "<...>" --out <out.docx> --author "AI helper" --threaded auto`

Threading policy:

* If the document supports modern comment threading metadata, emit the appropriate `commentsExtended` (`w15:commentsEx` / `commentEx`) structures.
* If true threading cannot be represented/validated, fallback to a non-threaded reply anchored to the same range, but include an explicit linkage in the text: “Reply to comment : …”.

## Ops schema (minimal, deterministic)

`ops.json` must be a JSON object with:

* `author` (optional; default “AI helper”)
* `ops`: array of operations

Each op:

* `op`: `"insert" | "delete" | "replace" | "set-style"`
* `target`: either:

  * `anchor`: explicit anchor `{ "paraId": "...", "start": <int>, "end": <int> }`, OR
  * `locator`: text-based locator `{ "query": "...", "scope": "heading:<text>|doc", "occurrence": 1 }`
* `text` / `replacement` / `style` depending on op
* `mode`: `"tracked" | "plain"` (plain allowed only in `apply`; tracked required in `apply-tracked`)

Anchors:

* `paraId` is the Word paragraph id if present, else a stable synthetic id emitted by `outline/find/extract`.

## Command reference (docxctl)

* `status --in file.docx`
* `outline --in file.docx --out outline.json`
* `find --in file.docx --query "..." --max N --out hits.json`
* `extract --in file.docx --anchor anchor.json --before k --after k --out excerpt.json`
* `inspect --in file.docx --out inspect.json` (avoid for big docs)
* `apply --in file.docx --ops ops.json --out edited.docx`
* `apply-tracked --in file.docx --ops ops.json --out tracked.docx --author "AI helper"`
* `redline --original a.docx --edited b.docx --out tracked.docx --author "AI helper"`
* `comments list|add|reply ...`
* `review --in <file.docx> [--kind comments|changes|both] [--author <text>] [--authorRegex true|false] [--text <text>] [--textRegex true|false] [--from N] [--limit N] [--threaded true|false] [--before N] [--after N] [--out <file.json>]`
  - Filtered review of comments and/or tracked changes with context and markers.
  - Markers: tracked change uses `<< >>`, comment range uses `[[[ ]]]`.
  - If a review by author returns nothing, run `authors` to check exact names and possible misspellings.
* `authors --in <file.docx> [--kind comments|changes|both] [--out <file.json>]`
  - Lists distinct authors for comments and/or tracked changes.

## Examples that should trigger this skill

* “Revise this DOCX with tracked changes and reply to reviewer comments.”
* “Find where the protocol defines X and update that paragraph with track changes.”
* “Summarize outstanding tracked changes and propose accept/reject decisions.”

**review output schema**
- `changes[]`: { type, author, date, text, paraId, paraIndex, before, current, after }
- `comments[]`: { id, author, initials, date, text, attachedText, paraId, paraIndex, before, current, after, thread[] }
- `thread[]`: { id, author, initials, date, text, replyToId }
- `page`: { from, limit, totalComments, totalChanges }

**authors output schema**
- `changes[]`: list of distinct change authors
- `comments[]`: list of distinct comment authors
