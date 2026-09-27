---
name: document-request-list
description: Create and maintain audit engagement information requests across all phases. Use when an auditor asks to create a document request list, add requests, or update existing requests.
---

# Document Request List

Maintain a document requests for an audit engagement with one row per request. Work from auditor-supplied information and instructions, including those passed by another skill.

## Locate the list

Resolve the engagement from the auditor's request and workspace context, then read its `ENGAGEMENT.md`. Ask when the engagement is ambiguous. Use:

`engagements/<year>/<name>/document-requests/REQUESTS.md`

Read the existing list before editing. If absent, create it when list creation or adding requests is requested; create the parent directory if needed. For an empty list, write the heading and table header without placeholder rows.

## Maintain the table

Use [REQUESTS-FORMAT.md](REQUESTS-FORMAT.md) for the heading and five-column table in `REQUESTS.md`.

- **ID:** Allocate `RQ-01`, `RQ-02`, and so on above the highest existing number. Keep IDs stable through edits and retain Closed and Withdrawn rows so IDs remain available for reference.
- **Request:** The material requested, including period or version when supplied. This is the only required input for a new row.
- **Owner:** The person responsible for providing the material. Leave blank when unknown.
- **Due Date:** Use `MM/DD/YYYY` for known dates; leave blank when unknown. Resolve an ambiguous date with the auditor rather than guessing.
- **Status:** Use only Open, Closed, or Withdrawn, with the meanings below.

New requests default to **Open**, meaning outstanding; this does not imply a request has been sent. **Closed** means the auditor considers the request fulfilled. **Withdrawn** means the material is no longer being requested. Partial responses remain Open on the same row.

Apply the auditor's requested changes to the identified row, preserving its ID and all fields outside the requested change. Use the ID or an unambiguous request description to identify the row; ask only when ambiguity prevents adding or updating the correct request. Change status only on the auditor's instruction. Receipt of a file alone does not close a request or create another row.

## Finish

Verify that the saved list has the five columns, unique stable IDs, allowed statuses, and correctly formatted known dates, with unrelated rows preserved. Return the file path and a concise summary of added or updated IDs and any unresolved ambiguity. When another skill called this one, return the same information; substantive audit gaps remain with that skill.
