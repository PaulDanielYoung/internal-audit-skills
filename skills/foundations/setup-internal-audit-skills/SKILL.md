---
name: setup-internal-audit-skills
description: Prepare an auditor workspace in local Claude Code with shared context documents, an engagements folder, and project instructions.
disable-model-invocation: true
---

# Setup Internal Audit Skills

Prepare a new or existing auditor workspace. The skills must already be installed; this skill configures a workspace, not the user's skill installation.

## 1. Establish the workspace

The current directory is used as the default workspace if no target folder is supplied by the user.

Inspect existing workspace files relevant to setup before making changes. Preserve existing content and reuse existing configuration where possible. If existing context or instructions conflict with the new setup, resolve the conflict before writing.

Confirm that `audit-context` is available; setup cannot continue without it.

## 2. Initialize context and folders

Invoke `audit-context` with the absolute workspace root to initialize any missing `GLOSSARY.md`, `METHODOLOGY.md`, and `ORGANIZATION.md` files from its templates. Pass any supplied sources or established decisions.

Ensure `engagements/` exists. Leave individual engagement folders to `create-engagement` and other engagement artifacts to the skills that create them.

Preserve existing files and configuration. Rerunning setup should add missing components rather than reset the workspace.

## 3. Add project instructions

Read [WORKSPACE-INSTRUCTIONS.md](WORKSPACE-INSTRUCTIONS.md).

Add its `## Internal audit skills` block to the workspace's `CLAUDE.md`, creating the file if it does not exist.

If an `## Internal audit skills` block already exists, update it in place with any necessary changes. Preserve user additions and all unrelated instructions.

Use paths relative to the workspace. Do not add absolute or machine-specific paths to `CLAUDE.md`.

## 4. Done

Tell the user setup is complete and summarize the files created or updated.

Mention that they can edit the context files directly or use `audit-context` to maintain them.

Suggest `audit-context` as the next step for adding organization, methodology, glossary, or other shared context to the workspace.
