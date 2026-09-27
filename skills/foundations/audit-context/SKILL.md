---
name: audit-context
description: Maintain a workspace's context files. Use when audit terminology is discussed, when documented methodology needs clarifying, or when audit work settles a term or surfaces an organizational fact useful across engagements.
---

# Audit Context

Actively maintain the shared context other audit skills use. Challenge unclear terminology, reconcile conflicts against sources, and record settled definitions, documented methodology, and organizational facts as they emerge.

## File structure

```text
/
├── CLAUDE.md
├── GLOSSARY.md
├── METHODOLOGY.md
├── ORGANIZATION.md
├── docs/
│   └── agents/
│       └── workspace.md
└── engagements/
    └── <year>/
        └── <name>/
            └── ENGAGEMENT.md
```

## Workspace and ownership

Use the workspace root identified by the workspace instructions. When setup calls this skill, use the absolute root it passes; otherwise, if the workspace instructions are missing, tell the user to run `setup-internal-audit-skills` before maintaining shared context.

This skill owns edits to all three context files. Other skills read them when present and call this skill when persistent context needs to change, passing the specific fact, term, or conflict and its evidence. Update only the relevant file or files, then return to the calling task.

Engagement scope, process and control detail, evidence, findings, and planning artifacts belong under `engagements/`.

## Initialize a workspace

When the user requests workspace setup, directly or through `setup-internal-audit-skills`, initialize all three context files. Read the format files below and create only missing files using their starting structures. Preserve existing files, including partial documents, and report which were retained.

Populate the documents only when the evidence and decisions required by their format files are available. Otherwise, use only the title, description, and fixed headings, omitting illustrative entries and placeholders. Outside explicit setup, create a missing file when there is settled content to record.

## During the session

Read the existing context files and supplied source material relevant to the update. Establish what is new, changed, or conflicting before asking questions. Explicit requests and relevant discoveries during audit work trigger maintenance.

Read the format file for each document being created or changed:

- [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md): definitions and entry format.
- [METHODOLOGY-FORMAT.md](METHODOLOGY-FORMAT.md): documented requirements and source references.
- [ORGANIZATION-FORMAT.md](ORGANIZATION-FORMAT.md): shared organizational facts and their evidence.

- **Challenge terminology.** When usage conflicts with an existing definition, surface the conflict immediately and ask which meaning holds. When a word carries more than one meaning, propose a precise canonical term using supplied material and the organization's established terminology.
- **Test meanings with scenarios.** Use concrete audit examples to clarify the boundaries between concepts. Treat hypothetical scenarios as questions to test a definition, not as evidence about the organization.
- **Check against sources.** Reconcile methodology interpretations with governing documents. When sources disagree or their current status is unclear, establish which documented source governs before recording a requirement as settled. Resolve conflicting organizational facts against their evidence and effective dates before replacing settled context.
- **Clarify material gaps.** Ask focused questions for only the missing sources or answers needed for the current update. Continue with settled updates while dependent work waits for unresolved answers; during setup, record what the available material supports and leave the rest for later sessions.
- **Put proposed changes to the user.** New or revised definitions are the user's decision. Offer each proposed definition, source-supported methodology clarification, or supported organizational fact in one line during the work, then write it on acceptance. Don't hold proposals for later.
- **Record settled context immediately.** Write accepted updates to the appropriate document during the session. Preserve unrelated content and replace superseded wording in place. When governing documents or organizational facts change, update the summary and its source references or effective period.

Where a material methodology or organizational gap will affect future work, keep a short, clearly labeled open question in the relevant file. State what needs to be established and which work depends on it. Remove the question when resolved.

## Check and return

Read the edited passages against their sources and the other context files. Check for conflicting definitions, changed requirement strength, unsupported facts, duplicated content, and engagement detail stored as shared context. Keep definitions in the glossary and use its terms in the other files.

Return the changed file paths, a short account of what changed, and any open question that affects the calling task. Keep unresolved matters distinct from settled context. If there is nothing new to record, leave the files unchanged.
