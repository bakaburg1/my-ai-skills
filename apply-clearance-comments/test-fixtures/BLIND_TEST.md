# Blind Test Protocol

Use this file only from the main orchestrating agent. Do not include it in the prompt to the blind tester.

## Purpose

Validate `apply-clearance-comments` by asking a cheaper sidecar to perform what looks like a normal clearance-review job. The sidecar should not be told it is testing the skill.

## Main-agent setup

1. Remove generated review artifacts from `test-fixtures/sidecar-validation/`:
   - `fixture-review.reviewed.docx`
   - any `~$...` Word lock files
2. Restore `fixture-source.md` to the baseline text:
   - `The protocol uses weekly summaries for analysis.`
   - `The pilot phase remains in the document for continuity.`
3. Verify the helper loads:
   - `python3 scripts/docx_review.py --help`
   - `python3 scripts/docx_review.py feedback --help`

## Blind tester prompt shape

Tell the sidecar this is an actual clearance-review job. Give it only:

- the skill path,
- `test-fixtures/sidecar-validation/fixture-review.docx`,
- `test-fixtures/sidecar-validation/fixture-source.md`,
- the review decisions to apply.

Required decisions for this fixture:

- Amend Alice Reviewer’s comment about reporting cadence by changing `weekly summaries` to `weekly surveillance summaries`. Mark the comment `_ R~` and add a threaded reply explaining the amendment.
- Reject Bob Reviewer’s tracked deletion of `for continuity`. Keep the Markdown source unchanged for that phrase, mark the tracked deletion `_ R-`, and add a reviewer-facing feedback comment explaining why it was retained.

When validating the current skill behavior, the sidecar should first show the
planned response comment wording and wait for approval before it writes feedback
comments into the DOCX. If the sidecar is given the response wording explicitly
in the prompt, that wording counts as approved.

## Main-agent validation

After the sidecar finishes, inspect the generated DOCX package directly. Acceptance criteria:

- `fixture-source.md` only changes `weekly summaries` to `weekly surveillance summaries`.
- `fixture-review.reviewed.docx` exists and `fixture-review.docx` remains untouched.
- Alice’s original comment author has `_ R~`.
- Bob’s tracked deletion author has `_ R-`.
- The sidecar exposed the planned response comment wording before writing it,
  unless the wording was explicitly provided in the prompt.
- The response to Alice is a threaded reply, proven by `word/commentsExtended.xml` containing a `w15:commentEx` for the reply with `w15:paraIdParent` equal to Alice’s comment paragraph ID.
  `word/document.xml` should also anchor the reply over the same text as the parent comment, with starts grouped before text and range ends grouped before comment references.
- The tracked-deletion response is present as feedback in `word/comments.xml`.
- `unzip -t fixture-review.reviewed.docx` passes.
- Open XML SDK validation passes with zero errors when `.NET` and
  `DocumentFormat.OpenXml` are available.
- No Word repair prompt appears when opened manually, if manual Word verification is available.
