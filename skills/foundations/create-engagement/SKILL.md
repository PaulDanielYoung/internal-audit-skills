---
name: create-engagement
description: Create an engagement record from an engagement name and audit objective statement. Use when an auditor starts a new engagement or asks to create or set up an audit.
---

# Create Engagement

Create the workspace structure and engagement record for an audit engagement. 

## Engagement Structure

Each engagement uses the following structure:

```
/
├── ENGAGEMENT.md
├── document-requests/received/
├── fieldwork/
├── planning/
├── reporting/
├── walkthroughs/
```

## 1. Establish the engagement name, objective, and year

Require a name, an objective statement, and a year: what the engagement is called, what it intends to accomplish, and the year it is planned for.

Use the engagement name, objective statement, and year already clearly established in the context or conversation. If any are missing or ambiguous, propose them and ask the auditor to confirm or revise.

## 2. Create the engagement workspace

Use the engagement year and the engagement name in kebab-case (lowercase words joined by hyphens) to form the engagement folder path:

`engagements/<year>/<name-with-hyphens>/`

Create the year and engagement folders if they do not exist. Otherwise, use the existing folders.

Within the engagement folder:

- Create `ENGAGEMENT.md` using the structure in [ENGAGEMENT-FORMAT.md](ENGAGEMENT-FORMAT.md). If the file already exists, leave it unchanged and report the conflict to the user.
- Create any missing directories from the Engagement Structure above. Leave existing directories unchanged.
