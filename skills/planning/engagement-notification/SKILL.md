---
name: engagement-notification
description: Draft or refresh the initial engagement notification to management, or prepare an entrance meeting agenda. Use when asked to notify or announce an engagement. Information requests and request emails route to document-request-list.
---

# Engagement Notification

Draft the auditor's initial communication to management. The only persistent work product this skill owns is `planning/engagement-notification.md` in the selected engagement. An entrance meeting agenda is an on-demand reply.

## Establish the basis

Follow the workspace instructions for engagement selection, read its `ENGAGEMENT.md`, and state the selected engagement and output path. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Use `audit-terminology` for missing, ambiguous, or contested terms and settled definitions.

Documented methodology governs the work. For structure, use a supplied organization template, then methodology, then relevant prior workpapers, then the defaults below. Read any longer retained source the methodology points to. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names and file paths fixed. If methodology is unclear or conflicts with sources, resolve the uncertainty with the auditor through `shared-understanding`. Keep requirements outside this skill's remit outstanding in the reply, with their methodology source.

Inspect the record and available material before asking for more. Intake is limited to the communication: an assignment note, organization notification template, or prior notification may help; accept equivalent auditor-supplied material. Ground activity facts in supplied material or dated auditor statements, never general knowledge. Record only auditor-supplied scope decisions; do not propose them.

Delegate source retention and provenance updates to `engagement-sources`, passing supplied material and known original locations and receipt dates. Use its returned retained-source links. If unavailable, continue supported work from already-retained material and give a concrete handoff for outstanding retention or provenance updates; do not write sources or their index as a fallback. Before adopting an external draft at the notification path, have `engagement-sources` preserve an unchanged received copy. Engagement sources are intake records, not additional planning work products.

Use `shared-understanding` only for material ambiguity that could change the communication, including a missing identifiable management addressee or a missing/materially unclear audit objective statement. Pause only the affected portion. If that skill is unavailable in an independent install, ask the material questions directly. Never invent or reword the assignment objective, or edit the engagement record to refine it. Mark non-material missing facts with descriptive bracketed placeholders and continue without interruption.

## Draft or refresh the notification

Write from the engagement lead to the management addressee in the internal audit function's voice ("we"); use another sender when specified by methodology or the auditor. An identifiable management role is sufficient even if the person's name is unknown.

The default content is:

- **To, From, Date, Subject.** Use placeholders for unknown non-material details, including the lead's name or proposed notification date.
- **Purpose of the engagement.** Ground the introduction in the assignment.
- **Audit objective statement.** Copy the statement verbatim from the engagement record, or the auditor's settled statement if it was missing or unclear. Introduce it with preliminary planning framing outside the statement itself, for example: "For preliminary planning, the assigned audit objective statement is:" followed by the unchanged statement.
- **Preliminary scope and period under examination.** Use supplied boundaries and period, or visible placeholders; distinguish the period examined from the dates when work will occur.
- **Proposed timing.** Clearly identify it as preliminary.
- **Entrance meeting and next steps.** Explain the proposed coordination at a high level, with placeholders for unsettled arrangements.

Keep document and information requests, risks, criteria, controls, work program, and budget hours outside the notification. "Why in the plan" and a separate team/contacts section are not default requirements. Route any methodology requirement for excluded content to the appropriate work rather than silently inserting it here.

Save the requested draft to `planning/engagement-notification.md`. On refresh, use the current supplied facts and retain the assignment objective verbatim. Keep internal Information gaps, Sources sections, inline source bookkeeping, and methodology-basis statements out of the communication; explain them separately in the reply.

## Entrance meeting agenda, when requested

Produce the agenda in the reply only, separate from internal explanations. An agenda-only request does not create or refresh the notification file. Use these default topics:

- Purpose and preliminary objective, preserving the assignment statement verbatim if quoted.
- Preliminary scope, period under examination, and proposed timing.
- How the engagement will run, grounded in methodology or supplied arrangements.
- Information needs as a discussion topic, without deriving an information-needs program.
- Management's view of recent changes and concerns.
- Next steps.

Leave attendees to the auditor. Keep walkthrough and detailed control-design content out of the agenda. Apply the same visible-placeholder and separate-source-explanation rules as for the notification.

## Route request work

`document-request-list` owns the shared engagement request list and all request emails, including the initial message. Route information-request work there even if no list exists or the notification has not been sent. This skill owns no request IDs, statuses, lifecycle rules, or request-table edits, and saves no request messages.

For a combined request, pass auditor-supplied needs to `document-request-list` with the item, period/version, addressee, relevant artifact/section or workstream, and candidate retained sources. Preserve unknown details as gaps. Invoke it for authorized list creation or updates and requested message drafting; recommend it when request work is only an optional next step. Additional substantive needs belong to the appropriate planning skill, normally `preliminary-survey`; do not derive them from organization context while drafting a notification.

When `document-request-list` is unavailable, finish the notification work and give a concrete handoff in the reply containing those supplied needs and context. Explicitly state that the list was not updated. Never edit the request table as a fallback. If supplied material responds to an existing request, invoke `engagement-sources` for retention and pass its returned link and proposed match to `document-request-list`. That skill arranges confirmed RQ backlinks through `engagement-sources`; report unfinished retention or provenance updates. Unrequested material does not change the list.

## Report completion

Notification drafting is complete when the requested draft exists, material ambiguities are resolved, and minor gaps are visibly marked and listed in the reply. For an agenda-only request, apply those criteria to the agenda in the reply. Completion means drafted, not sent or approved, and requires neither an agenda nor a request list. Do not send communications or ask for approval as a readiness gate.

In the reply, give the output path (or the on-demand agenda), state whether drafting is complete, and list remaining placeholders, material gaps, and outstanding methodology requirements. Explain the methodology or default basis and link supporting retained sources or identify dated auditor statements so the communication's factual claims are traceable without citations inside it. Keep assumptions explicit. Recommend the next appropriate planning stage, normally `preliminary-survey`, without making it a prerequisite for this draft.
