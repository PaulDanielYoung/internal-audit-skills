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

```
## Internal audit skills

### Workspace Instructions

Before performing work, read and follow 'docs/agents/workspace.md'.
```

## 3. Create the context folder

Create `context/` and its subfolders `policies/`, `regulations/`, and `frameworks/` if they do not exist. Leave existing folders and their contents unchanged.

## 4. Create files from templates

Copy each template from this skill's folder to its destination. If the file already exists, skip it and leave it unchanged.

| Template | Destination |
|---|---|
| [workspace.md](workspace.md) | `docs/agents/workspace.md` |
| [CONTEXT-INDEX.md](CONTEXT-INDEX.md) | `context/README.md` |
| [METHODOLOGY.md](METHODOLOGY.md) | `context/METHODOLOGY.md` |
| [ORGANIZATION.md](ORGANIZATION.md) | `context/ORGANIZATION.md` |

## 5. Report

Tell the user setup is complete and the internal audit skills will now read from these files.

Explain that newly created `context/METHODOLOGY.md` and `context/ORGANIZATION.md` files are blank templates for the auditor to populate manually with approved content, and that converted policies, regulations, and frameworks go in the matching `context/` subfolder with a row in `context/README.md`.

Mention that they can edit docs/agents/workspace.md directly to update workspace instructions.
