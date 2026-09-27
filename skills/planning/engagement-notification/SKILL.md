---
name: engagement-notification
description: Draft or refresh the initial engagement notification to management, or prepare an entrance meeting agenda. Use when asked to notify or announce an engagement or plan its entrance meeting.
---

# Engagement Notification

Draft the auditor's initial communication to management. The only persistent work product this skill owns is `planning/engagement-notification.md` in the selected engagement. An entrance meeting agenda is an on-demand reply.

## Establish the basis

Follow the workspace instructions for engagement selection, read its `ENGAGEMENT.md`, and state the selected engagement and output path. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Use `audit-terminology` when a term's meaning needs agreement or consistency across engagements.

Documented methodology governs the work. For structure, use a supplied organization template, then methodology, then relevant prior workpapers, then the defaults below. Read any longer retained source the methodology points to. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names and file paths fixed. If methodology is unclear or conflicts with sources, resolve the uncertainty with the auditor through `shared-understanding`. Keep requirements outside this skill's remit outstanding in the reply, with their methodology source.

Inspect the record and available material before asking for more. Intake is limited to the communication: an assignment note, organization notification template, or prior notification may help; accept equivalent auditor-supplied material. Ground activity facts in supplied material or dated auditor statements, never general knowledge. Record only auditor-supplied scope decisions; do not propose them.

Read source files in place and leave originals unchanged. The auditor places client-provided files in `document-requests/received/`; use those files and other available local references directly. When adopting an external draft, create the working copy at the notification path only after a separate unchanged original is available. Explain source dates or versions and relevant locations in the reply, leaving unknown provenance explicit.

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

`document-request-list` owns the engagement's document request list. Invoke it when drafting reveals missing material that warrants a document request, relevant information or received files may change an existing request, or the auditor asks to create or update the list. Neither an existing list nor a sent notification is a prerequisite. Request messages and reminders are outside that skill's scope. This skill saves only the notification.

Pass the selected engagement, the material needed and why, known period/version, request owner and due date, relevant files, and any existing request ID or auditor instruction. Let `document-request-list` manage approval of new requests and maintain the list. Keep requests separate from the notification; broader information-needs analysis belongs to `preliminary-survey`.

When `document-request-list` is unavailable, finish supported notification work and return proposed requests or status changes as a handoff, explicitly stating that the list was not updated. Request table edits belong to that skill.

## Report completion

Notification drafting is complete when the requested draft exists, material ambiguities are resolved, and minor gaps are visibly marked and listed in the reply. For an agenda-only request, apply those criteria to the agenda in the reply. Completion means drafted, not sent or approved, and requires neither an agenda nor a request list. Do not send communications or ask for approval as a readiness gate.

In the reply, give the output path (or the on-demand agenda), state whether drafting is complete, and list remaining placeholders, material gaps, and outstanding methodology requirements. Explain the methodology or default basis and link supporting retained sources or identify dated auditor statements so the communication's factual claims are traceable without citations inside it. Keep assumptions explicit. Recommend the next appropriate planning stage, normally `preliminary-survey`, without making it a prerequisite for this draft.
