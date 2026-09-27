# Workspace Docs

How the skills should consume workspace context when performing audit work.

## Before working, read these files in the folder root

- `GLOSSARY.md`
- `METHODOLOGY.md`
- `ORGANIZATION.md`

If any of these file are absent, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `audit-context` skill creates them lazily when terms or decision actually get resolved.

## Use shared context

- **Use the glossary's vocabulary.** Use the organization's agreed terms and meanings in audit work, including its preferred names over synonyms it avoids.
- **Follow documented methodology.** Apply the requirements relevant to the work, preserving required versus recommended steps, applicability conditions, scales, thresholds, and exceptions. Consult the linked governing sources when the summary directs it or does not settle a material question. The governing source takes precedence over the summary; a missing rule does not establish that no requirement applies.
- **Use relevant organizational facts.** Consider the overview's sources and effective dates when applying facts to an engagement. Keep engagement-specific assumptions distinct from shared facts.
- **Surface material conflicts.** Identify conflicts between the current work, shared context, and supplied sources. Resolve the governing meaning, requirement, or fact with the auditor before dependent work proceeds; continue unaffected work.

## Capture shared context

Route agent-made changes to shared context through `audit-context`. Call it when a term is missing or contested, or when audit work establishes a term, methodology point, or organizational fact useful across engagements. Pass the specific term, fact, or conflict and its evidence; that skill handles clarification and accepted updates.

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

## Engagements

Engagements live in `engagements/<year>/<name>/` and are identified by their `ENGAGEMENT.md`. Keep engagement-specific outputs within the engagement folder.

Before producing work for an engagement, resolve the engagement named by the auditor and read its `ENGAGEMENT.md`. Ask when the selection is ambiguous rather than inferring it from the files being read.
