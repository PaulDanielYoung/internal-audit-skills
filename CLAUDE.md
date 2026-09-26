Skills live one folder each under `skills/<category>/`. Keep each skill in one category. Every skill has an entry in its category's `README.md` and the top-level `README.md`, with its name linked to its `SKILL.md`. List each shipped skill path in `.claude-plugin/plugin.json`.

`CONTEXT.md` at the repo root defines the repo's own vocabulary. Use its terms in skills and docs.

Shared context lives at the auditor workspace root: `GLOSSARY.md`, `METHODOLOGY.md`, and `ORGANIZATION.md`. The workspace instructions that setup writes locate that root and carry the reading and capture rules and the engagement selection rules, so skills don't resolve the root or the selected engagement themselves. Only `audit-context` edits these files, and it depends on the workspace instructions: when they are missing it tells the user to run `setup-internal-audit-skills`. Other skills refer to the workspace glossary and relevant methodology and organization context in brief prose, read them if present, proceed silently if not, and call `audit-context` when a term is missing or contested or persistent context needs updating. Don't add setup pointers or root-resolution rules to skills whose output only becomes less sharp without shared context. Documented methodology governs audit work.

Context templates and their guides live inside `skills/foundations/audit-context/` so they travel with the skill under every install route. Other skills delegate context creation and maintenance to `audit-context` rather than duplicating its document rules.

`engagement-sources` owns retained engagement material and its provenance index. Other skills delegate retention and provenance updates to it, keeping substantive interpretation and artifact sourcing with the artifact owner. `request-list` delegates retention before matching and confirmed RQ backlinks afterward. If `engagement-sources` is unavailable, continue supported work from retained material and report outstanding source work rather than writing sources or their index as a fallback.

Validate plugin packaging with `claude plugin validate . --strict`. Users install through the plugin or `npx skills add`, as the README documents. For maintainers only, `./scripts/link-skills.ps1` in PowerShell links every skill into `~/.claude/skills/` so edits are live in the next session without reinstalling; re-run it after adding, moving, or removing a skill, and remove the links before testing an npx or plugin install.

`setup-internal-audit-skills` prepares an auditor workspace and its project instructions; it delegates context initialization to `audit-context`. Explicit setup creates missing glossary, methodology, and organization documents from the context templates. Ordinary maintenance records settled content and preserves existing workspace files.

## Agent skills

### Issue tracker

Issues are tracked in this repo's GitHub Issues via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles use their default label names. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
