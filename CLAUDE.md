Skills live one folder each under `skills/<category>/`. Keep each skill in one category. Every skill has an entry in its category's `README.md` and the top-level `README.md`, with its name linked to its `SKILL.md`. List each shipped skill path in `.claude-plugin/plugin.json`.

`CONTEXT.md` at the repo root defines the repo's own vocabulary. Use its terms in skills and docs.

Shared context lives at the auditor workspace root: `GLOSSARY.md`, `METHODOLOGY.md`, and `ORGANIZATION.md`. Skills read the glossary and relevant methodology and organizational context when present; absent files do not block work unless the missing information is material. Only `audit-context` edits these files; other skills call it when a term is missing or contested or persistent context needs updating. Documented methodology governs audit work. Use the auditor's chosen root, otherwise the parent of `engagements/` when working beneath it, otherwise the working directory. Resolve an ambiguous root before writing.

Context templates and their guides live inside `skills/foundations/audit-context/` so they travel with the skill under every install route. Other skills delegate context creation and maintenance to `audit-context` rather than duplicating its document rules.

Validate plugin packaging with `claude plugin validate . --strict`. Users install through the plugin or `npx skills add`, as the README documents. For maintainers only, `./scripts/link-skills.ps1` in PowerShell links every skill into `~/.claude/skills/` so edits are live in the next session without reinstalling; re-run it after adding, moving, or removing a skill, and remove the links before testing an npx or plugin install.

`setup-internal-audit-skills` prepares an auditor workspace and its project instructions; it delegates context initialization to `audit-context`. Explicit setup creates missing glossary, methodology, and organization documents from the context templates. Ordinary maintenance records settled content and preserves existing workspace files.
