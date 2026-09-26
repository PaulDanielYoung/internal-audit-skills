# List and lifecycle rules

## Persistent format

Keep one persistent artifact: title `# Request list: <engagement name>`, one purpose line, and one Markdown table. Use these nine columns in this order:

| ID | Request | Addressee | Needed by | Requested | Due | Status | Received | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

**Request** stands alone for pasting, including period/version where relevant. **Addressee** is an external role or name. **Needed by** names one or more artifacts and sections or workstreams, not a deadline. **Requested** is the actual sent date. **Due** contains only an auditor-supplied date; leave it blank otherwise. **Received** links retained copies or dated notes. **Notes** preserves explanations, follow-ups, and history. Mark unknown request details visibly rather than inventing them.

Order rows by the numeric part of their RQ ID, never by phase or addressee. Allocate `RQ-01`, `RQ-02`, and so on above the highest existing ID. Keep every row, including discarded unsent proposals; never delete, renumber, or reuse an ID. No separate allocation field or hand-maintained counts are needed.

## Reconcile before adding

Check both retained engagement sources and existing rows for each supplied need:

- Clearly sufficient retained material: cite it instead of requesting it. A possible match with uncertain entity, period, version, or substantive sufficiency goes to the caller or auditor for decision; keep the need unresolved meanwhile.
- Matching **Proposed** or **Requested** row: reuse its ID and append the needing artifact/section or workstream to Needed by. Preserve request wording unless the auditor explicitly settles a change to an unsent proposal. Preserve sent wording; a changed deliverable becomes a linked new item. A different period or a different/narrower deliverable is a separate item.
- Matching **Received** row: use its retained material where sufficient; where insufficient, create a Proposed follow-up for the unmet need and link both rows in Notes.
- Matching **Not available** or **Withdrawn** row: put the prior outcome to the auditor before requesting it again. If the auditor decides to pursue it again, retain the closed row and create a linked Proposed item.
- No match: create one Proposed row per external deliverable, carrying the supplied Needed by references and known details.

An existing open row is not implicitly closed because sufficient material is discovered; receipt still follows the confirmation rules below.

## Status and history

| Status | Evidence and action |
| --- | --- |
| Proposed | Drafted and unsent. Leave Requested blank. |
| Requested | Auditor confirms actual sending and its date. Record that date in Requested. A draft or elapsed time is not confirmation. |
| Received | Auditor confirms the proposed match to retained material. Link it in Received; follow RECEIPT.md for full and partial responses. |
| Not available | Information cannot be supplied. Record who said so and when in Notes. |
| Withdrawn | No longer pursued, including a discarded unsent proposal. Record the reason in Notes. Leave Requested blank for an unsent row and preserve it for a sent row. |

Proposed and Requested are open; the other statuses close only the row. Preserve sent wording, original Requested dates, existing source links, and Notes history on every update. Record confirmed changes without erasing earlier events. Never infer receipt, unavailability, or withdrawal from time passing or a drafted message.
