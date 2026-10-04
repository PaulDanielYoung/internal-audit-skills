---
name: setup-internal-audit-skills
description: Configure the project for internal audit skills by setting up the workspace. Run once before first use of the other internal audit skills.
disable-model-invocation: true
---

# Setup Internal Audit Skills

Prepare the workspace with the necessary configuration that the internal audit skills assume exist.

## 1. Establish the workspace

The current directory is used as the default workspace if no target folder is supplied by the user.

Inspect the existing files relevant to setup before making changes. If existing content conflict with the new setup, resolve the conflict with the user before writing.

## 2. Create or Update CLAUDE.md

Create `CLAUDE.md` if it doesn't exist. Otherwise, edit it.

If an `## Internal audit skills` block already exists in `CLAUDE.md`, update its contents in-place rather than appending a duplicate.

````markdown
## Internal audit skills

How the internal audit skills should consume workspace documentation when performing audit work.

### Before working, read these files in `context/`

- `GLOSSARY.md`
- `METHODOLOGY.md`
- `ORGANIZATION.md`

If any of these files are absent or contain only a blank template, **proceed silently**. Do not flag their absence or blank content alone; don't suggest populating them upfront.

Everything in `context/` is an approved reference maintained by the internal audit department. Agents read it without making edits, with one exception: `GLOSSARY.md`, which only the `audit-terminology` skill edits.

### File structure

The full workspace layout is shown below. Files and directories are created as needed by the relevant skills.

```text
/
├── CLAUDE.md
├── context/
│   ├── GLOSSARY.md
│   ├── METHODOLOGY.md
│   ├── ORGANIZATION.md
│   └── policies/
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
            │   └── planning-memo.md
            ├── reporting/
            └── walkthroughs/
```

### Resolve material ambiguity with the auditor

When ambiguity about context, assumptions, preferences, or decisions could materially change the work, call the `shared-understanding` skill and resolve it with the auditor before producing the affected part. Continue work the ambiguity doesn't affect.

Clarification through `shared-understanding` settles the current work only; it does not approve changes to `context/METHODOLOGY.md` or `context/ORGANIZATION.md`.

### Use the glossary's vocabulary

When your output names an audit concept, use the term as defined in `context/GLOSSARY.md`.

If a term or concept arises that would be useful to define in the glossary, suggest it to the auditor.

### Follow the documented methodology

When the work involves something addressed by the audit methodology, follow the relevant guidance and requirements in `context/METHODOLOGY.md`. Apply what is documented rather than inventing a different procedure or convention.

If the methodology does not address something needed for the work, don't treat the absence as permission to invent it. Note the genuine methodology gap and resolve uncertainty with the auditor by calling the `shared-understanding` skill.

### Tailor work to the organization

Use the organization's name, description, and industry to tailor your work to the organization.

Use the organization's name when it is natural and useful.

### Consult context documents on demand

When the work depends on a policy, find it at `context/policies/` and read only the documents that bear on the work.

Each context document opens with front matter giving its title, description, and effective date; cite it with those.

### Engagements

Engagements live in `engagements/<year>/<name>/`. Before producing engagement work, resolve the engagement named by the auditor and read its `ENGAGEMENT.md`. Ask if the selection is ambiguous. Keep engagement-specific outputs within that engagement's folder.

### Request missing material

When work reveals missing material, call the `document-request-list` skill and record the information gap. When material arrives, assess whether its contents resolve the gap.
````

## 3. Create the context folder

Create `context/` and its subfolder `policies/`, if they do not exist. Leave existing folders and their contents unchanged.

## 4. Create files from templates

Copy each template from this skill's folder to its destination. If the file already exists, skip it and leave it unchanged.

| Template | Destination |
|---|---|
| [GLOSSARY.md](GLOSSARY.md) | `context/GLOSSARY.md` |
| [METHODOLOGY.md](METHODOLOGY.md) | `context/METHODOLOGY.md` |
| [ORGANIZATION.md](ORGANIZATION.md) | `context/ORGANIZATION.md` |

## 5. Report

Tell the user setup is complete and the internal audit skills will now read from the files in `context/`.

Explain that `context/GLOSSARY.md`, `context/METHODOLOGY.md`, and `context/ORGANIZATION.md` are blank templates for the user to complete and maintain. The user is responsible for keeping the information in these files accurate and up to date.

Explain that organizational policies converted to Markdown should be added to `context/policies/`.
