---
name: document-request-list
description: Maintain audit engagement document requests. Use when missing materials warrant a request, received files may change a request's status, or the auditor asks to create or update the list.
---

# Document Request List

Proactively suggest document requests as needs emerge. The agent maintains `REQUESTS.md`; the auditor approves new requests and places client-provided files in `document-requests/received/`.

## File Structure

```text
/
└── engagements/
    └── <year>/
        └── <name>/
            └── document-requests/
                ├── REQUESTS.md
                └── received/
```

## Locate the list

Resolve the engagement from the conversation and workspace context, then read its `ENGAGEMENT.md`. Ask when the engagement is ambiguous. Use:

`engagements/<year>/<name>/document-requests/REQUESTS.md`

Read the existing list before editing. When the first request is approved or the auditor asks to create a list, create any missing `document-requests/` and `document-requests/received/` directories, and create `REQUESTS.md` if it does not already exist.

Read [REQUESTS-FORMAT.md](REQUESTS-FORMAT.md) for the table structure, IDs, fields, and dates. The status rules below take precedence over that reference.

## Suggest and add requests

When needed material is missing, check the list and received files for existing coverage. Propose a specific request in the conversation, explain why it is needed, and ask the auditor to approve adding it. Add the request only after approval; an explicit instruction to add it already counts as approval. Keep unapproved suggestions in the conversation.

## Maintain requests

Update the list as relevant information and received files become available, preserving stable IDs and unrelated fields. Maintain statuses without separate approval:

- **Open:** Material remains outstanding or the response is partial.
- **Closed:** Review of the received material establishes that the request is fulfilled.
- **Withdrawn:** The auditor indicates the material is no longer needed.

Follow explicit auditor status decisions. When fulfillment or the matching request is unclear, retain the current status and ask for clarification.

## Finish

Verify the saved list follows the table format, with unique stable IDs and supported statuses. Briefly report added or updated IDs and any unresolved questions.
