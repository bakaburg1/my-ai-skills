---
name: apply-clearance-comments
description: Reviews Word DOCX clearance comments and tracked changes against source text and marks decisions in the review target. Use when editing clearance or peer-review DOCX files.
metadata:
  author: Angelo D'Ambrosio
  license: EUPL-1.2
---

# Apply Clearance Comments

## Purpose

Use this skill to reconcile a Word review document with tracked changes or
comments against editable source text files.

- Treat the Word `.docx` as the review source.
- Treat repository text files as the editable source of record.
- The user must provide, point to, or clearly identify the Word `.docx`.
- Source text files may be one file or several files. They can be `.md`, `.qmd`,
  `.rmd`, `.html`, `.tex`, `.txt`, or another plain-text format.
- If the user does not name the source file(s), infer candidates from the
  repository and verify matches with distinctive Word text fragments.
- Do not edit any source file until the user explicitly approves the proposed
  item.
- Mark Word review decisions in the user's chosen Word review target: either
  the original `.docx` or a parallel `<old_name>.reviewed.docx` copy.

## Word Review Target

Before writing review markers or response comments, decide which Word file is
the review target.

- Default to a parallel review copy named `<old_name>.reviewed.docx` next to
  the original Word file.
- If the user explicitly asks to work in the same Word file, use the original
  `.docx` as the review target and do not create a parallel reviewed copy.
- If the user has not made a preference clear, state the default target before
  the first write. Ask only when in-place editing seems intended but ambiguous.
- Never write to both targets for the same review pass unless the user asks.
- All `mark` and `feedback` commands must operate on the chosen review target.

## Source File Discovery

If the user names source files, use those files first. Otherwise, infer the
editable source files before proposing edits.

1. Inspect the repository shape with `rg --files`.
2. Prioritize likely source formats: `.md`, `.qmd`, `.rmd`, `.html`, `.htm`,
   `.tex`, `.txt`, `.rst`, `.adoc`, `.yml`, `.yaml`, `.csv`, and related
   project text files.
3. Use headings, table labels, variable names, citations, and unusual phrases
   from the Word document as targeted `rg` search fragments.
4. Check project configuration when relevant, such as `_quarto.yml`, front
   matter, include directives, render scripts, Makefiles, or pipeline files.
5. Exclude generated outputs, dependency folders, caches, and vendored files by
   default unless the user or project context identifies them as editable
   sources.
6. If more than one source file matches, map each Word paragraph or comment to
   the narrowest source file and section. If the mapping remains ambiguous, ask
   before editing.

Do not assume there is a single source file.

## Fast DOCX Access

Do not rely on rendered text alone. Open the `.docx` as a ZIP package and inspect
OOXML directly.

Prefer the bundled helper script instead of retyping OOXML parsing snippets.
Resolve `scripts/docx_review.py` relative to this `SKILL.md`.

```bash
python3 scripts/docx_review.py headings "<target.docx>"
python3 scripts/docx_review.py edits "<target.docx>" --paragraphs 342:462 --unmarked-only
python3 scripts/docx_review.py comments "<target.docx>" --paragraphs 342:462
python3 scripts/docx_review.py comments "<target.docx>" --paragraphs 342:462 --author "Reviewer Name"
python3 scripts/docx_review.py mark "<target.docx>" --kind revision --paragraphs 354 --marker R+ --text "also being"
python3 scripts/docx_review.py mark "<target.docx>" --kind comment --comment-id 372 --marker R+
python3 scripts/docx_review.py feedback "<target.docx>" --comment-id 372 --author "Name" --text "Accepted in amended form. ..."
python3 scripts/docx_review.py feedback "<target.docx>" --paragraphs 354 --author "Name" --text "Not accepted. ..."
```

Use `headings` first to identify Word paragraph ranges for the relevant chapter
or section. Use `edits --unmarked-only` for normal review lists. Use `comments
--author <name>` when the user asks for one reviewer's comments. Use
`comments --exclude-author <name>` only when the user, repo instructions, or
review context clearly says to ignore that author. The `comments` command
highlights the actual comment range with `==...==` when Word exposes the range.
Use `mark` only after the approval rules below are satisfied.

Use `feedback` when an item is refused (`_ R-`) or amended (`_ R~`). With
`--comment-id`, it adds a threaded reply to the original Word comment. With
`--paragraphs`, it adds a standalone feedback comment for a tracked change that
has no comment thread. It does not alter the reviewer's original comment text.
Threaded replies need both normal document comment anchors and a
`word/commentsExtended.xml` parent link.
After writing a reviewed DOCX, verify more than ZIP integrity when possible:
Word must open it without a repair prompt.

Read these parts first:

- `word/document.xml`: paragraphs, tracked insertions/deletions, comment anchors.
- `word/comments.xml`: comment text, author, date, and comment IDs.

Use namespace-aware XML parsing, preferably Python with `zipfile` and
`xml.etree.ElementTree` or another structured XML parser. Avoid plain grep for
interpreting tracked changes because Word revision markup is nested inside
paragraph runs.

Useful XPath concepts:

- Paragraphs: `.//w:p`
- Insertions: `.//w:ins`
- Deletions: `.//w:del`
- Comment anchors: `.//w:commentRangeStart`, `.//w:commentRangeEnd`,
  `.//w:commentReference`
- Text nodes: `.//w:t`
- Deleted text nodes may appear as `.//w:delText`

For each changed paragraph, derive three text views:

- Word visible/current text: all visible `w:t` text in paragraph order.
- Accepted-change text: include inserted text, exclude deleted text.
- Original/rejected-change text: include deleted text, exclude inserted text.

The accepted-change text is usually the candidate to compare against source
text. For deletion-only changes, also verify that the deleted text is absent
from the matching source context. A deletion is already implemented when the
surrounding accepted paragraph is reflected in source text and the deleted
phrase is not present there.

## Comment Rules

- Do not hard-code author exclusions. Apply exclusions only from user
  instructions, repo instructions, or clear review context.
- Still consider actual tracked insertions/deletions, including changes by an
  otherwise excluded comment author, unless the user explicitly says otherwise.
- For review comments, propose a source change only when the comment calls for a
  text change that is not already reflected in the source.
- If a comment is a question or expert judgement call, recommend `needs expert
  decision` and propose the smallest text change that would resolve it, if one
  is clear.
- Be careful with comments that describe a possible change but do not change the
  Word paragraph. If the visible Word text and source text already match, do not
  propose an edit unless the comment clearly requires a new textual resolution.

## Comparison Workflow

1. Select the Word review target. Create `<old_name>.reviewed.docx` next to the
   original only when using the default parallel-copy mode.
2. Read tracked changes and comments from the chosen review target, using the
   original only as a fallback reference when the target is a parallel copy.
3. List changed Word paragraphs and comments from OOXML.
4. Infer and verify the source text file(s) if the user did not provide them.
5. For each item, locate the matching source section with targeted `rg` searches
   using distinctive fragments.
6. Compare the accepted Word text and the current source text. Check insertions,
   replacements, and deletions separately when needed.
7. When an unmarked item already matches the accepted Word text or the comment's
   resolution, do not propose it to the user; mark the relevant Word item in the
   review target with `_ R+` and continue. For deletion-only items, mark `_ R+`
   only when the deleted text is absent from the matching source context and the
   surrounding accepted text matches the source.
8. If an item is already marked `_ R+`, verify in the background that the
   accepted Word text, comment resolution, or deletion is still reflected in the
   source. Do not list or discuss these `_ R+` items unless the user explicitly
   asks for an audit of accepted/marked changes or they are not actually
   reflected in the source. Warn the user in the second case.
9. Propose only unreviewed and unresolved changes.
10. Work paragraph by paragraph or one comment at a time unless the user asks
    for a batch.
11. Wait for user approval before editing any source file.

Do not autonomously mark `_ R~` or `_ R-`. These markers require the user's
explicit decision. If the source differs from the accepted Word text, treat it
as an unreviewed change proposal, not as an edited resolution. Present the Word
wording and the current source wording to the user for a decision.

## Response Comments

When the user refuses or amends a reviewer change, add feedback to the clearer
inside the chosen Word review target.

- Draft the exact response comment text in the chat first and ask the user to
  confirm or edit it before writing it into the DOCX.
- For `_ R-`, add a short response comment explaining why the proposed change
  was not applied.
- For `_ R~`, add a short response comment explaining that the point was
  accepted in amended form and summarize or quote the final source wording.
- For an existing Word comment, add the response as a threaded reply to the
  original comment ID. Ignore existing response replies during normal
  unresolved-comment scans unless auditing prior responses.
- For a tracked change without an existing comment, anchor the response to the
  changed paragraph.
- Never edit the original reviewer comment text.
- Keep feedback neutral, concise, and suitable for the clearer to read.
- Do not prefix every reply with a boilerplate label such as `Clearance
  response:`. Write a natural sentence that starts with the decision only when
  it helps readability, such as `Accepted in amended form.` or `Not accepted.`
- Do not mark `_ R-` or `_ R~`, and do not run `feedback`, until the user has
  seen and approved the exact response wording.

Example response comments:

```text
Not accepted. The existing source wording is retained because it matches the
agreed scope and avoids introducing a broader definition.
```

```text
Accepted in amended form. The final wording was narrowed for consistency with
the surrounding section: "..."
```

Plain `@Name` text in a Word comment can be used as a visible cue only. Do not
promise that it will email or notify the clearer. Real Word mention
notifications depend on Microsoft 365 identity, cloud storage, and modern
threaded comments; ordinary OOXML comments may not trigger them.

Sign response comments with the user's preferred review name. If the user has
not specified one, infer a candidate from `CLEARANCE_RESPONSE_AUTHOR`,
`git config user.name`, `id -F`, or the local username. Ask before using it when
the signer is unclear or the document is external-facing. The helper script
accepts `--author`; without it, it tries those local defaults.

## Proposal Format

Keep each proposal short and readable.

Include:

- Enough location context to understand where the edit sits, such as file path,
  section heading, subsection heading, table/variable name, and a short nearby
  phrase.
- A concise description of the change.
- A recommendation: `accept`, `reject`, or `needs expert decision`.
- A wrapped git-style diff with short lines.
- For comments, always show the paragraph where the comment is anchored.
  Highlight the actual commented span inside that paragraph when
  `w:commentRangeStart`/`w:commentRangeEnd` make it identifiable. Use
  `==commented text==` for the highlighted span, and wrap the paragraph to short
  readable lines. If Word only exposes a point comment or the exact range cannot
  be reconstructed safely, state that the exact span is unavailable and show the
  nearest anchor paragraph.

Do not print `Source` and `Target` labels when the location is obvious from the
file path, heading, or shown text. Still provide enough context before the diff
so the user can orient themselves without opening the file.

Use inline word-level markers inside changed lines:

- `[-deleted words-]` for removed text.
- `{+added words+}` for added text.

Example:

```diff
@@ path/to/source.qmd :: Objectives
- to describe the microbiological and molecular epidemiology, including
  antibiotic susceptibility, [-strain identification-], toxin genes, and
  detection of emerging types;
+ to describe the microbiological and molecular epidemiology, including
  antibiotic susceptibility, {+strain typing (genotype and ribotype)+},
  toxin genes, and detection of emerging types;
```

If using a full patch header, explain only once that `a/...` means current
source text and `b/...` means proposed source text. Usually omit the full header
for individual review proposals.

## Marking Reviewed Items In Word

Record review decisions in the chosen Word review target: the parallel
`<old_name>.reviewed.docx` copy by default, or the original Word file when the
user explicitly selected in-place review.

Mark decisions by appending a suffix to the existing Word author metadata for
the relevant tracked change or comment:

- `_ R+`: accepted and applied to source, including inserted/replaced text
  already found in source and deleted text already absent from source.
- `_ R-`: reviewed and rejected.
- `_ R~`: user rejected the initial Word-vs-source proposal during assisted
  review and approved a third wording that was not exactly the original Word
  text or the current source text.

Preserve the original author name and append the marker, for example:

- `Reviewer Name _ R+`
- `Reviewer Name _ R-`
- `Reviewer Name _ R~`

For tracked changes, update the `w:author` attribute on the relevant `w:ins`
and/or `w:del` elements in `word/document.xml`. For comments, update the
`w:author` attribute on the relevant `w:comment` elements in
`word/comments.xml`.

This keeps provenance readable while allowing Word filtering by review decision.
For `_ R-` and `_ R~`, also add a response comment as described above. For
`_ R+`, add a response comment only when the user asks for one.

## Approval And Editing

After approval, apply only the approved item to the mapped source file and mark
the relevant Word item in the chosen review target with `_ R+` when the Word
wording is accepted. Use `_ R~` only when the user explicitly approves a third
wording created during assisted review, different from both the Word text and
current source text; show the planned response comment to the user, then add it
only after the user approves that wording.

If an item is discovered to match the source exactly enough to be already
implemented, mark it `_ R+` immediately and move on without presenting it as a
proposal. This includes deletion-only changes where the deleted wording is
already absent from the matching source text.

If the user rejects an item, do not edit the source and mark the relevant Word
item with `_ R-` only after that explicit rejection and after adding the
reviewer-facing response comment approved by the user. Preserve unrelated user
edits and comments. If multiple items are approved together, apply only those
items and then continue the review from the next unresolved Word item.
