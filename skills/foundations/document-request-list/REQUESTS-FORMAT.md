# REQUESTS.md Format

## Structure

```markdown
# Document Request List

The engagement's document request list. Each row represents one request. Other skills read it; only `document-request-list` edits it.

## Table

| ID | Request | Owner | Due Date | Status |
| --- | --- | --- | --- | --- |
```

## Rules

- **Keep one request per row.** Use exactly the five columns shown above. An empty list contains only the table header, with no placeholder rows.
- **Preserve request IDs.** Assign the next sequential ID after the highest existing number: RQ-01, RQ-02, and so on. Never reuse an existing ID.
- **Describe the requested material.** Write each request clearly and specifically enough to identify what should be provided, including the relevant period or scope when known. Request is the only field that must be known when creating a new row.
- **Identify the provider.** Owner is the business stakeholder responsible for providing the requested material. Leave it blank when unknown.
- **Use consistent dates.** Write known due dates as `MM/DD/YYYY` and leave unknown dates blank.
- **Use three statuses.** Open means the request remains outstanding and is the default for new requests. Closed means the request has been fulfilled. Withdrawn means the material is no longer being requested.
- **Keep partial responses open.** A request remains Open until the received material fully satisfies it or the auditor directs otherwise.
