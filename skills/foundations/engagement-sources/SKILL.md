---
name: engagement-sources
description: Retain supplied material for an engagement, maintain its source provenance, save requested source notes, or add auditor-confirmed request references to retained sources. Interpretation and source sufficiency belong to the substantive skill; request matching and lifecycle belong to request-list.
---

# Engagement Sources

Own retained material in the selected engagement's `sources/` folder and its provenance in `sources/README.md` across audit phases. Preserve supplied originals and existing citations. Substantive skills decide what material they need, when a verbal account needs a retained note, which version governs, and whether a source supports their work. `request-list` owns RQ matching and lifecycle; `audit-terminology` owns glossary edits; the internal audit department maintains the methodology and organization references.

## Establish the basis

Follow the workspace instructions for engagement selection, read its `ENGAGEMENT.md`, and state the selected engagement and source paths. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Documented methodology governs. Use `audit-terminology` for missing, ambiguous, or contested terms and settled definitions; use `shared-understanding` for material uncertainty about methodology or organizational facts, including conflicting retention requirements.

Accept supplied material or accessible paths, its original location and receipt date when known, and the requested retention or provenance update. For a source note, accept the supplied account, attribution, and date. For an RQ backlink, require the retained-source link, request-list path, RQ ID, and auditor-confirmed match supplied by `request-list` or the auditor. Existing explicit confirmation suffices; a candidate match does not.

Inspect retained material and the index before writing. Preserve existing layout, paths, links, and provenance; fill missing details from supplied facts and keep unknown details visibly marked. Ask only when ambiguity affects a safe update, pausing that portion while continuing supported work.

## Retain material and receipt events

Use ordinary file tools to create missing `sources/` and index files and perform the requested work. Compare file contents to establish identical copies; a matching filename alone is insufficient. Reuse an identical retained copy within this engagement. Copy new or changed contents unchanged to a distinct path, verifying the retained bytes against the supplied original. Keep both versions and their provenance. Avoid filename collisions without overwriting, renaming, or deleting existing retained material, so earlier citations keep working.

Record each actual receipt's original location and date against the retained copy. Identical material received from another location or on another date shares the retained file but keeps its distinct receipt event. A rerun of the same intake or a later provenance-only update adds neither another copy nor another receipt event. Compare the supplied receipt details with the index; if it is unclear whether this is a new receipt or a retry, preserve established records and report the uncertainty rather than inventing an event. The processing date is not a substitute for an unknown receipt date.

When asked to retain a verbal account or dictated note, write a dated, attributed note from the supplied account, distinguishing paraphrase from quotation and preserving uncertainty. Keep missing attribution or date visible. Reuse an existing note for a repeated request; retain a changed account separately. The caller decides whether a note is required; this skill does not generate meeting minutes or turn an account into an established fact.

Retain material even when its governing version or substantive sufficiency is unsettled, and return that question to the caller or auditor. Unrequested material can be retained without creating a request item. Retention does not adopt an external workpaper as the engagement's working artifact or reconfirm prior-engagement content; those decisions stay with the artifact owner.

## Maintain provenance

For a new index, use the title `# Engagement sources`, a short purpose line, and a simple Markdown entry per retained file, with its link, original location and receipt date for each receipt event, and confirmed RQ references when present. Preserve an existing index's structure instead of migrating it. Use paths as references; allocate no source IDs or separate register. Preserve recorded history when correcting or completing provenance.

Add an RQ backlink only for the supplied auditor-confirmed match. Link to the actual request list and RQ ID, preserving existing matches and adding no duplicate link on a retry. This update does not represent another receipt. Report candidate or uncertain matches back to `request-list` or the auditor without recording them as confirmed. Edit neither the request list nor its statuses.

Use working relative Markdown links within the engagement, percent-encoding spaces and parentheses in link destinations so returned links can also be used in the RCM. Keep originals unchanged; any requested source note is a separately identified record of the account.

## Verify and return the handoff

Check that each reported retained file exists, copied bytes are unchanged, the index points to it, distinct receipt events are preserved, and requested confirmed RQ backlinks are present without duplication. Return retained paths and links, the index path, what was copied or reused, provenance changes, and outstanding details or failures. Name any unresolved governing-version or sufficiency questions for the caller; make no readiness decision for its artifact.

If an operation fails after part of the work succeeds, report the saved material and the exact unfinished update. On retry, inspect that state and finish only the outstanding work. A copied file with an unwritten index entry is incomplete retention, not a reason to make another copy. A failed RQ backlink does not undo a confirmed receipt recorded by `request-list`.

## Contract for calling skills

Call this skill for new retention, requested source notes, and provenance changes; use its returned links in the owning artifact. `request-list` can call it directly before matching unretained material and again after confirmation to add backlinks. Callers retain substantive interpretation, governing-version decisions, additional flags, and their own artifact updates.

If this skill is unavailable, callers continue supported work from already-retained material and return a concrete handoff with the supplied material, known receipt details, requested update, and affected artifact or request references. Keep new retention and provenance updates outstanding and state that they were not performed; callers do not write retained sources or their index as a fallback.
