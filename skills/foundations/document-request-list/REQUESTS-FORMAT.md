# REQUESTS.md Format

## Structure

```
# Document Request List

The audit engagement's document request list. One row corresponds to one request. Every skill reads it; only `document-request-list` edits it.

## Table

| ID | Request | Owner | Due Date | Status |
| --- | --- | --- | --- | --- |
```

## Rules

- **Keep one request per row.** Use exactly the five columns shown above. An empty list has the table header without placeholder rows.
- **Preserve request IDs.** Allocate `RQ-01`, `RQ-02`, and so on above the highest existing number.
- **Describe the requested material.** Request text is the only required input for a new row.
- **Identify the provider.** Owner is the business stakeholder responsible for providing the requested material. Leave the cell blank when unknown.
- **Use consistent dates.** Write known due dates as `MM/DD/YYYY` and leave unknown dates blank.
- **Use three statuses.** Open means outstanding and is the default for new requests. Closed means the auditor considers the request fulfilled. Withdrawn means the material is no longer being requested.
- **Follow the auditor's status decisions.** Change status only on the auditor's instruction. Partial responses remain Open.
