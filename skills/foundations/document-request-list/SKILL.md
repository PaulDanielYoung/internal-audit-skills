---
name: document-request-list
description: Proactively maintain audit engagement document requests. Use when missing material warrants a request, received files need reconciling, a scope change affects a request, or the auditor asks to create or update the list.
---

# Document Request List

Proactively maintain the engagement's document request list in `REQUESTS.md`. The agent proposes requests and keeps them current; the auditor approves requests and places client-provided files in `document-requests/received/`.

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

Create `document-requests/`, `document-requests/received/`, and `REQUESTS.md` when the first request is proposed or the auditor asks to create a request list. Format `REQUESTS.md` according to [REQUESTS-FORMAT.md](REQUESTS-FORMAT.md). If any already exist, update them in place.

## 1. Reconcile received files

Start every run by reconciling `received/`, including subfolders, against `REQUESTS.md`. For each file not yet listed in any request's Received column, read its contents and judge which requests it answers against each request's Request and Purpose.

- **Matches a request**: add the file to that request's Received column. A file may answer more than one request. Close the request when the received material fully satisfies it; otherwise keep it Open and record in Notes what is still missing.
- **Matches no request**: flag it to the auditor.

Reconciliation is done when every file in `received/` is listed against a request or flagged to the auditor. Status changes from reconciliation need no separate approval.

## 2. Propose requests

When work reveals missing material, check `REQUESTS.md` and the received files for existing coverage. If a request already covers the need, return its RQ ID. Otherwise, add a Proposed row with its Purpose and return the new RQ ID to the calling work.

Gather the proposals from a piece of work and present them to the auditor together at the end, each with its purpose, for approval. On approval, set the request Open and its Requested date to today. A declined proposal becomes Withdrawn, with the auditor's reason in Notes.

An explicit instruction from the auditor to add a request counts as approval: add it directly as Open.

## 3. Keep requests current

- Record owners, due dates, follow-ups, and partial-response gaps as information becomes available.
- When a scope change leaves a request without a purpose, such as a planning memo exclusion or a removed risk or control, flag the request to the auditor as a withdrawal candidate. Withdraw it on the auditor's direction, with the reason in Notes.
- Flag Open requests past their due date.
- When a request's status is unclear, call the `shared-understanding` skill.

## Done

If `REQUESTS.md` changed or reconciliation flagged anything, summarize for the auditor:

- Proposed requests awaiting approval, with their purposes.
- Status changes, with the received files behind them.
- Unmatched received files.
- Overdue requests and withdrawal candidates.
- Unresolved questions that require the auditor's input.
