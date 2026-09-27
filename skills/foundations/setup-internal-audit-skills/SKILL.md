---
name: setup-internal-audit-skills
description: Configure the project for internal audit skills by setting up the workspace. Run once before first use of the other internal audit skills.
disable-model-invocation: true
---

# Setup Internal Audit Skills

Scaffold the workspace with the necessary configuration that the internal audit skills assume:

- **Workspace**: where the internal audit skills are set up and configured.

This is a prompt-driven skill, not a deterministic script.

## 1. Establish the workspace

The current directory is used as the default workspace if no target folder is supplied by the user.

Inspect existing workspace files relevant to setup before making changes. Preserve existing content and reuse existing configuration where possible. If existing context or instructions conflict with the new setup, resolve the conflict before writing.

## 2. Initialize context and folders

If `CLAUDE.md` does not exist, create it. If `CLAUDE.md` exists, edit it.

If an `## Internal audit skills` block already exists in `CLAUDE.md`, update its contents in-place rather than appending a duplicate.

The `## Internal audit skills` block:

```
## Internal audit skills

### Workspace Instructions

[one-line summary of where the internal audit skills are set up]. See 'docs/agents/workspace.md'.
```

Then read [workspace.md](workspace.md) and write it to `docs/agents/workspace.md`.

## 3. Done

Tell the user setup is complete and the internal audit skills will now read from these files.

Mention that they can edit docs/agents/workspace.md directly to update workspace instructions.
