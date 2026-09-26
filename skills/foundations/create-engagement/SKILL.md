---
name: create-engagement
description: Create an engagement record from an engagement name and audit objective statement, or update its assignment facts. Use when an auditor starts a new engagement, asks to set up or register an audit, or changes an engagement's contacts, team, period, or target dates.
---

# Create Engagement

Establish one engagement in the auditor workspace and record its assignment facts in the engagement record, `engagements/<year>/<name>/ENGAGEMENT.md`. Every later engagement skill starts from this record. Scope, risk assessment, criteria, resource planning, and refined objectives belong to planning; this skill records the assignment as given.

Read the workspace glossary and the relevant methodology and organization context when present, and use the glossary's terms in the record; documented methodology governs. Proceed silently when they are absent. Call `audit-context` when a term is missing or contested, or when the conversation settles a fact useful across engagements.

## 1. Establish the objective

Require an engagement name and an auditor-supplied **audit objective statement**: what the engagement is about and what it is intended to accomplish, in the auditor's words.

When the statement is missing, or so unclear that planning could read it several ways, call the Skill tool with "shared-understanding" to establish it. Ask what the engagement is about and what it is intended to accomplish; recommend wording built only from what the auditor and the supplied material say; record the statement the auditor settles. The name, the annual plan, and general knowledge of the subject never supply the statement. Write nothing to the workspace until the statement is settled.

This step is complete when the record could quote both the name and the objective statement as the auditor's own.

## 2. Gather assignment facts

Take facts from the conversation and supplied material first, then request the remaining optional facts in one message:

- engagement identifier, when the annual plan or an audit management system assigns one
- subject: the activity, process, function, or system under audit
- responsible business area
- management contact
- engagement lead
- team
- period under examination: the period the audit covers
- annual-plan reference or the rationale for the assignment
- target dates: the planned dates for planning, fieldwork, and reporting

Record supplied facts as given and mark each remaining fact `Unspecified`. Keep the period under examination apart from the target dates: one is what the audit examines, the other is when the work happens. Recording known team members and dates is not resource planning; hours, budgets, and estimates stay out of the record.

This step is complete when every fact is recorded or marked unspecified and the auditor has been asked at most once.

## 3. Place the record

The engagement folder is `engagements/<year>/<name>/` under the auditor workspace root that the workspace instructions locate. The year is the annual-plan year; when it is unknown, ask for the intended year and suggest the current one. Work continuing into a later year stays in its original folder.

The folder name is the engagement name as the auditor writes it, spaces and capitals kept, with only the characters a file system rejects removed, and without the identifier unless the auditor wants it there. Create only the year folder, the engagement folder, and the record; later skills create `sources/`, `planning/`, and their own deliverables.

When `ENGAGEMENT.md` already exists at the target, ask whether the auditor wants to update that engagement or create a separate one under another name, and follow that answer. Preserve any other files already in the folder.

This step is complete when the target path is unambiguous and holds no record that would be overwritten as a new engagement.

## 4. Write or update the record

For a new engagement, copy [ENGAGEMENT-TEMPLATE.md](ENGAGEMENT-TEMPLATE.md) and fill every field. The record holds identity, the objective statement, and assignment facts only.

For an update, change the administrative facts the auditor supplies (contacts, team, period, plan reference, target dates) in place, replace `Unspecified` with newly known values, and add a dated line under Changes. Leave the audit objective statement as recorded: refined objectives belong in planning deliverables. When the auditor states that the assignment itself changed, add the new statement under the original with its date and basis so the original stays visible.

This step is complete when the record reads as the auditor's assignment, with the objective statement unchanged on an update.

## 5. Report

State the record's path and list the facts recorded and those left unspecified. Tell the auditor to name this engagement in a conversation before engagement work so later skills start from its record.

Creation is complete when the engagement is identifiable and its assignment objective is recorded. Stop there: no planning deliverable, folder, or next-stage draft.
