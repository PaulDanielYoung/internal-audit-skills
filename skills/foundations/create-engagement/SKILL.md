---
name: create-engagement
description: Create an engagement record from an engagement name and audit objective statement. Use when an auditor starts a new engagement or asks to set up or register an audit.
---

# Create Engagement

Establish one engagement in the auditor workspace by recording its name and audit objective statement in the engagement record, `engagements/<year>/<name>/ENGAGEMENT.md`. Every later engagement skill starts from this record.

Read the workspace glossary and the relevant methodology and organization context when present, and use the glossary's terms; documented methodology governs. Proceed silently when they are absent. Call `audit-context` when a term is missing or contested, or when the conversation settles a fact useful across engagements.

## 1. Establish the objective

Require an engagement name and an auditor-supplied **audit objective statement**: what the engagement is about and what it is intended to accomplish, in the auditor's words.

When the statement is missing, or so unclear that planning could read it several ways, call the Skill tool with "shared-understanding" to establish it. Ask what the engagement is about and what it is intended to accomplish; recommend wording built only from what the auditor and the supplied material say; record the statement the auditor settles. The name, the annual plan, and general knowledge of the subject never supply the statement. Write nothing to the workspace until the statement is settled.

This step is complete when the record could quote both the name and the objective statement as the auditor's own.

## 2. Place the record

The engagement folder is `engagements/<year>/<name>/` under the auditor workspace root that the workspace instructions locate. The year is the annual-plan year; when it is unknown, ask for the intended year and suggest the current one. Work continuing into a later year stays in its original folder.

The folder name is the engagement name in kebab-case: lowercase words joined by hyphens, so "Procurement Card Spend" becomes `procurement-card-spend`. Create only the year folder, the engagement folder, and the record.

When `ENGAGEMENT.md` already exists at the target, leave it as it is and ask whether the auditor means that engagement or a separate one under another name. Its objective statement stays as recorded; refined objectives belong in planning deliverables.

This step is complete when the target path is unambiguous and holds no record that would be overwritten as a new engagement.

## 3. Write and report

Copy [ENGAGEMENT-TEMPLATE.md](ENGAGEMENT-TEMPLATE.md), fill in the name and the statement as the auditor gave them, and state the record's path. Tell the auditor to name this engagement in a conversation before engagement work so later skills start from its record.

Creation is complete when the engagement is identifiable and its objective statement is recorded. Stop there: no planning deliverable, folder, or next-stage draft.
