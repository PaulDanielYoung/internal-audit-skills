---
name: create-engagement
description: Create an engagement record from an engagement name and audit objective statement. Use when an auditor starts a new engagement or asks to create or set up an audit.
---

# Create Engagement

Establish an engagement in the auditor workspace by recording its name and audit objective statement in the engagement record, `engagements/<year>/<name>/ENGAGEMENT.md`.

## 1. Establish the engagement name, objective, and year

Require a name, an objective statement, and a year: what the engagement is called, what it intends to accomplish, and the year it is planned for.

Use the engagement name, objective statement, and year already clearly established in context or conversation. If any are missing or ambiguous, propose them and ask the auditor to confirm or revise.

## 2. Create the engagement record

Use the engagement year and the engagement name in kebab-case (lowercase words joined by hyphens) to form the engagement folder path:

`engagements/<year>/<name-with-hyphens>/`

Create the year and engagement folders if they do not exist. Otherwise, use the existing folders.

Create `ENGAGEMENT.md` within the corresponding engagement folder using the structure in [ENGAGEMENT-FORMAT.md](ENGAGEMENT-FORMAT.md). If the file already exists, leave it unchanged and report the conflict to the user.
