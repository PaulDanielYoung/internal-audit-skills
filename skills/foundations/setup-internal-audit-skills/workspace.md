# Workspace Docs

How the skills should consume workspace context when performing audit work.

## Before working, read these

Shared context lives at the workspace root in `GLOSSARY.md`, `METHODOLOGY.md`, and `ORGANIZATION.md`. At the start of each new chat session, read these files once before doing audit work.

Route agent-made changes to shared context through `audit-context`. When audit work establishes a term, methodology point, or organizational fact useful across engagements, use that skill to capture it.

## File structure

```text
/
├── CLAUDE.md
├── GLOSSARY.md
├── METHODOLOGY.md
├── ORGANIZATION.md
└── engagements/
    └── <year>/
        └── <name>/
            └── ENGAGEMENT.md
```

## Engagements

Engagements live in `engagements/<year>/<name>/` and are identified by their `ENGAGEMENT.md`. Keep engagement-specific outputs within the engagement folder.

Before producing work for an engagement, resolve the engagement named by the auditor and read its `ENGAGEMENT.md`. Ask when the selection is ambiguous rather than inferring it from the files being read.
