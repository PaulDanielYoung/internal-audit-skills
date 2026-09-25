---
name: audit-context
description: Maintain shared audit context in GLOSSARY.md, METHODOLOGY.md, and ORGANIZATION.md. Use when establishing or updating this context, resolving missing or contested terms, clarifying documented methodology, or capturing organizational facts useful across engagements.
---

# Audit Context

Maintain the context other audit skills use. Capture existing terminology, documented methodology, and organizational facts; methodology design and engagement planning are separate work.

## Workspace and ownership

Use the auditor's explicitly chosen workspace root. Otherwise, when working beneath `engagements/`, use its parent; outside an engagement, use the working directory. Resolve an ambiguous workspace with the user before writing. Keep these files at that root, separate from the installed skill:

- `GLOSSARY.md`: the organization's own definitions.
- `METHODOLOGY.md`: a concise, source-linked account of documented audit requirements.
- `ORGANIZATION.md`: an organizational overview useful across engagements.

This skill owns edits to all three files. Other skills read the glossary and relevant methodology and organizational context when present, and proceed without absent files unless missing information materially affects their work. They call this skill when persistent context needs to change, passing the specific fact, term, or conflict and its evidence. Update only the relevant file or files, then return to the calling task.

Engagement scope, process and control detail, evidence, findings, and planning artifacts belong under `engagements/`.

## Initialize a workspace

When the user requests workspace setup, directly or through `setup-internal-audit-skills`, initialize all three context files. Read the guides below and create only missing files from their corresponding templates. Preserve existing files, including partial documents, and report which were retained.

Populate the documents only when the evidence and decisions required by their guides are available; setup can finish with the files otherwise as created. Outside explicit setup, create a missing file when there is settled content to record.

## 1. Read and resolve

Read the existing context files and the supplied source material relevant to the update. Establish what is new, changed, or conflicting before asking questions. During setup, record what the available material supports and leave the rest for later sessions. During maintenance, request only the missing sources or answers needed for the requested update.

Read the guide for each document being created or changed:

- [GLOSSARY-GUIDE.md](GLOSSARY-GUIDE.md): definitions, user decisions, and entry format.
- [METHODOLOGY-GUIDE.md](METHODOLOGY-GUIDE.md): documented requirements and source references.
- [ORGANIZATION-GUIDE.md](ORGANIZATION-GUIDE.md): shared organizational facts and their evidence.

Ask about material ambiguity; when it spans several decisions, use `shared-understanding` if available.

This step is complete when each proposed update has the basis required by its guide and material conflicts are resolved or identified as open questions. Continue with settled updates while dependent work waits for unresolved answers.

## 2. Record settled context

Update resolved content during the session rather than collecting it for a later review. Preserve unrelated content and replace superseded wording in place. Explicit requests and relevant discoveries during audit work trigger maintenance.

Where a material methodology or organizational gap will affect future work, keep a short, clearly labeled open question in the relevant file. State what needs to be established and which work depends on it. Remove the question when resolved.

This step is complete when each settled update is in its proper file, its basis is traceable, and unresolved matters remain distinct from definitions, facts, and requirements.

## 3. Check and return

Read the edited passages against their sources and the other context files. Check for conflicting definitions, changed requirement strength, unsupported facts, duplicated content, and engagement detail stored as shared context. Keep definitions in the glossary and use its terms in the other files.

Return the changed file paths, a short account of what changed, and any open question that affects the calling task. If there is nothing new to record, leave the files unchanged. Finish when the context is consistent with the available evidence and the calling task can distinguish settled context from what still needs an answer.
