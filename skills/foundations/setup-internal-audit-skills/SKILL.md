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

### Shared Understanding

When unresolved ambiguity about context, assumptions, preferences, or decisions could materially change the work, call the `shared-understanding` skill and resolve with the user before proceeding.
```

## 3. Create files from templates

Copy each template from this skill's folder to its destination. If the file already exists, skip it and leave it unchanged.

| Template | Destination |
|---|---|
| [workspace.md](workspace.md) | `docs/agents/workspace.md` |
| [METHODOLOGY.md](METHODOLOGY.md) | `METHODOLOGY.md` (workspace root) |
| [ORGANIZATION.md](ORGANIZATION.md) | `ORGANIZATION.md` (workspace root) |

## 4. Report

Tell the user setup is complete and the internal audit skills will now read from these files.

Explain that newly created `METHODOLOGY.md` and `ORGANIZATION.md` files are blank templates for the auditor to populate manually with approved content.

Mention that they can edit docs/agents/workspace.md directly to update workspace instructions.
