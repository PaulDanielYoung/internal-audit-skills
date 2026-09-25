---
name: setup-internal-audit-skills
description: Prepare an auditor workspace in local Claude Code with shared context documents, an engagements folder, and project instructions.
disable-model-invocation: true
---

# Setup Internal Audit Skills

Prepare a new or existing auditor workspace. The skills must already be installed; this skill configures a workspace, not the user's skill installation.

## 1. Establish the workspace

Use the target folder supplied by the user, resolving a relative path from the current working directory. If no target was supplied, use the current directory when it is clearly an auditor workspace or an empty folder, apart from Claude Code configuration in `.claude/`. Otherwise, ask for the intended folder. In the skills source repository, ask for a separate auditor workspace path rather than treating the source repository as an organization.

Inspect existing `CLAUDE.md`, `AGENTS.md`, shared context files, and `engagements/` in the target. Preserve existing content. If the folder already describes a different organization or has conflicting workspace instructions, resolve that conflict before making changes. Create the target directory if needed.

Locate the available `audit-context` skill, including its plugin-qualified name when installed through a plugin. If it is unavailable, explain that setup requires it and stop before writing workspace files. Do not substitute a copy of its document rules.

This step is complete when the target is unambiguous, existing workspace conventions have been inspected, and `audit-context` is available.

## 2. Initialize context and folders

Invoke `audit-context` with the absolute workspace root and an explicit request to initialize missing context files using its glossary, methodology, and organization templates. Pass any supplied sources and established decisions. That skill owns all edits to `GLOSSARY.md`, `METHODOLOGY.md`, and `ORGANIZATION.md`.

Ensure `engagements/` exists. Leave individual engagement folders and planning artifacts for the audit work that needs them. Keep existing files intact; rerunning setup fills missing pieces rather than resetting the workspace.

This step is complete when all three context documents and `engagements/` exist. Sources and definitions come later through `audit-context`.

## 3. Add project instructions

Read [WORKSPACE-INSTRUCTIONS.md](WORKSPACE-INSTRUCTIONS.md). Add its block to the target's `CLAUDE.md`, creating the file if absent. When a block headed `## Internal audit skills` already exists, merge necessary changes into that block, preserving user additions and all unrelated instructions. Respect any existing `CLAUDE.md` pointer to `AGENTS.md`; add the block to the referenced project instruction file rather than replacing the pointer. Resolve conflicting instructions with the user.

The block's root is the selected auditor workspace. If the instruction file is outside that root, adjust the root sentence to name the actual workspace path. Use the installed skill's callable name in the block, including a plugin prefix when needed. Avoid machine-specific source-repository paths in ordinary workspace instructions.

This step is complete when Claude Code can find the workspace root, context ownership, and reading rules from its project instructions without duplicate or conflicting setup blocks.

## 4. Verify and hand off

Check that the context documents are readable, `engagements/` exists, and the project instructions point to the correct workspace and skill. Report the absolute workspace path and the files created or retained.

Tell the user to start a local Claude Code session in the workspace. Give one next prompt of the form "Use audit-context to capture <material>", with organizational material as the example. Setup is complete without generating an engagement plan or requiring another confirmation.
