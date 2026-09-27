---
name: document-request-list
description: Proactively maintain audit engagement document requests. Use when missing materials warrant a request, received files may change a request's status, or the auditor asks to create or update the list.
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

Create `document-requests/`, `document-requests/received/`, and `REQUESTS.md` when the first request is approved or the auditor asks to create a request list. Format `REQUESTS.md` according to [REQUESTS-FORMAT.md](REQUESTS-FORMAT.md). If any already exist, update them in place.

## Suggest and add requests

When audit work identifies missing material, check `REQUESTS.md` and the received files for existing coverage. If a new request is warranted, propose it in the conversation, explain why it is needed, and ask the auditor to approve adding it.

Add the request only after approval. An explicit instruction to add a request counts as approval. Keep unapproved suggestions in the conversation.

## Maintain requests

Update `REQUESTS.md` as relevant information and received files become available. Maintain request statuses without separate approval, using the status rules in [REQUESTS-FORMAT.md](REQUESTS-FORMAT.md).

Ask the user for clarification if the status of a request is unclear.

## Done

If `REQUESTS.md` changed, briefly summarize the changes to the user, including the affected requests. Surface any unresolved questions that require the user's input.
