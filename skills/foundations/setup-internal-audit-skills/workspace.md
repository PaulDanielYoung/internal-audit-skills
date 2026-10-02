# Workspace Docs

How the internal audit skills should consume workspace documentation when performing audit work.

## Before working, read these files in `context/`

- `INDEX.md`
- `GLOSSARY.md`
- `METHODOLOGY.md`
- `ORGANIZATION.md`

If any of these files are absent or contain only a blank template, **proceed silently**. Do not flag their absence or blank content alone; don't suggest populating them upfront.

Everything in `context/` is an approved reference maintained by the internal audit department. Agents read it without making edits, with one exception: `GLOSSARY.md`, which only the `audit-terminology` skill edits.

## File Structure

The full workspace layout is shown below. Files and directories are created as needed by the relevant skills.

```text
/
├── CLAUDE.md
├── context/
│   ├── INDEX.md
│   ├── GLOSSARY.md
│   ├── METHODOLOGY.md
│   ├── ORGANIZATION.md
│   ├── policies/
│   └── regulations/
├── docs/
│   └── agents/
│       └── workspace.md
└── engagements/
    └── <year>/
        └── <name>/
            ├── ENGAGEMENT.md
            ├── document-requests/
            │   ├── REQUESTS.md
            │   └── received/
            ├── fieldwork/
            ├── planning/
            │   ├── risk-assessment.md
            │   ├── risk-and-control-matrix.md
            │   ├── preliminary-survey.md
            │   ├── planning-memo.md
            ├── reporting/
            └── walkthroughs/
```

## Resolve material ambiguity with the auditor

When ambiguity about context, assumptions, preferences, or decisions could materially change the work, call the `shared-understanding` skill and resolve it with the auditor before producing the affected part. Continue work the ambiguity doesn't affect.

Clarification through `shared-understanding` settles the current work only; it does not approve changes to `context/METHODOLOGY.md` or `context/ORGANIZATION.md`.

## Use the glossary's vocabulary

When your output names an audit concept, use the term as defined in `context/GLOSSARY.md`. Don't drift to synonyms the glossary explicitly avoids.

If a needed concept is not in the glossary, first consider whether you're introducing language the auditors don't use. Route it through `audit-terminology` when its meaning needs agreement or consistency across engagements. Otherwise, use the established meaning and continue the work.

## Follow the documented methodology

When the work involves something addressed by the audit methodology, follow the relevant guidance and requirements in `context/METHODOLOGY.md`. Apply what is documented rather than inventing a different procedure or convention.

If the methodology does not address something needed for the work, don't treat the absence as permission to invent it. Note the genuine methodology gap and resolve uncertainty with the auditor by calling the `shared-understanding` skill.

## Reference organizational facts

When the work depends on organization-specific facts, use the relevant context in `context/ORGANIZATION.md`. Treat the facts as context for the work rather than replacing them with generic assumptions.

If needed organizational context is not documented, don't treat the absence as permission to invent it. Note the genuine organizational context gap and resolve uncertainty with the auditor by calling the `shared-understanding` skill.

## Consult context documents on demand

When the work depends on a policy or regulation, find it through the context index and read only the documents that bear on the work. `context/policies/` holds management's own criteria and `context/regulations/` the laws and regulations the organization must comply with.

Each context document opens with front matter giving its title, description, and effective date; cite it with those.

## Engagements

Engagements live in `engagements/<year>/<name>/`. Before producing engagement work, resolve the engagement named by the auditor and read its `ENGAGEMENT.md`. Ask if the selection is ambiguous. Keep engagement-specific outputs within that engagement's folder.

## Cite sources

Support factual statements with inline citations giving the source, its relevant location, and its known date or version. Keep unknown provenance and conflicting accounts visible.

## Request missing material

When work reveals missing material, call the `document-request-list` skill and record the information gap. When material arrives, assess whether its contents resolve the gap.
