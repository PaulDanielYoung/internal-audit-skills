# Workspace Docs

How the internal audit skills should consume workspace documentation when performing audit work.

## Before working, read these files located at the root

- `GLOSSARY.md`
- `METHODOLOGY.md`
- `ORGANIZATION.md`

If any of these files are absent or contain only a blank template, **proceed silently**. Don't flag their absence or blank content; don't suggest populating them upfront.

## File structure

```text
/
├── CLAUDE.md
├── docs/
│   └── agents/
│       └── workspace.md
└── engagements/
    └── <year>/
        └── <name>/
            └── ENGAGEMENT.md
├── GLOSSARY.md
├── METHODOLOGY.md
├── ORGANIZATION.md
```

## Use the glossary's vocabulary

When your output names a workspace concept, use the term as defined in `GLOSSARY.md`. Don't drift to synonyms the glossary explicity avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the auditors don't use (reconsider) or there's a real gap (note it for `audit-context`).

## Follow the documented methodology

When the work involves something addressed by the audit methodology, follow the relevant guidance and requirements in `METHODOLOGY.md`. Apply what is documented rather than inventing a different procedure or convention.

If the methodology does not address something needed for the work, don't treat the absence as permission to invent it. Note the genuine methodology gap and resolve uncertainty with the auditor by calling the `shared-understanding` skill.

## Reference organizational facts

When the work depends on organization-specific facts, use the relevant context in `ORGANIZATION.md`. Treat the facts as context for the work rather than replacing them with generic assumptions.

If needed organizational context is not documented, don't treat the absence as permission to invent it. Note the genuine organiztional context gap and resolve uncertainty with the auditor by calling the `shared-understanding` skill.
