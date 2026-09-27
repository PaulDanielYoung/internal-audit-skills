---
name: document-request-list
description: Create and maintain audit engagement information requests across all phases. Use when an auditor asks to create a document request list, add requests, or update existing requests.
---

# Document Request List

Maintain a document requests for an audit engagement with one row per request. Work from auditor-supplied information and instructions, including those passed by another skill.

## Locate the list

Resolve the engagement from the auditor's request and workspace context, then read its `ENGAGEMENT.md`. Ask when the engagement is ambiguous. Use:

`engagements/<year>/<name>/document-requests/REQUESTS.md`

Read the existing list before editing. If absent, create it when list creation or adding requests is requested; create the parent directory if needed.

## Maintain the table

Read [REQUESTS-FORMAT.md](REQUESTS-FORMAT.md) before creating or updating `REQUESTS.md`; it defines the document structure and rules for request IDs, fields, dates, and statuses.

Apply the auditor's requested changes to the identified row, preserving its ID and all fields outside the requested change. Use the ID or an unambiguous request description to identify the row; ask only when ambiguity prevents adding or updating the correct request.

## Finish

Verify that the saved list has the five columns, unique stable IDs, allowed statuses, and correctly formatted known dates, with unrelated rows preserved. Return the file path and a concise summary of added or updated IDs and any unresolved ambiguity. When another skill called this one, return the same information; substantive audit gaps remain with that skill.
