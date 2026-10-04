# REQUESTS.md Format

## Structure

```markdown
# Document Request List

The engagement's internal document request list, written for the audit team. Each row represents one request. Other skills read it; only `document-request-list` edits it.

## Table

| ID | Request | Purpose | Owner | Requested | Due | Status | Received | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

## Rules

- **Keep one request per row.** Use exactly the nine columns shown above. An empty list contains only the table header, with no placeholder rows.
- **Preserve request IDs.** Assign the next sequential ID after the highest existing number: RQ-01, RQ-02, and so on. Proposed requests receive IDs too. Other workpapers cite these IDs, so keep every row; retire a request by withdrawing it. Never reuse an existing ID.
- **Describe the requested material.** Write each request clearly and specifically enough to identify what should be provided, including the relevant period or scope when known. Request and Purpose are the only fields that must be known when creating a new row.
- **State the purpose bluntly.** Purpose says why the engagement needs the material, in plain internal language, citing the Process, Risk, or Control IDs it supports when known. Reconciliation judges received files against it.
- **Identify the provider.** Owner is the business stakeholder responsible for providing the requested material. Leave it blank when unknown.
- **Use consistent dates.** Write Requested and Due as `MM/DD/YYYY`. Requested is the date the auditor approved the request; leave it blank while Proposed. Leave unknown dates blank.
- **Use four statuses.** Proposed means the request awaits the auditor's approval and has not been requested. Open means the request remains outstanding. Closed means the request has been fulfilled. Withdrawn means the material is no longer being requested.
- **List received files.** Received lists each file that answers the request, as a path relative to `received/`, separated by `; `. Leave it blank until a file arrives.
- **Keep partial responses open.** A request remains Open until the received material fully satisfies it or the auditor directs otherwise. Notes records what is still missing.
- **Write blunt notes.** Notes records partial-response gaps, follow-ups, the auditor's direction to close, and withdrawal reasons. Leave it blank when there is nothing to note.
