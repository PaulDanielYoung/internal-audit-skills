Skills live one folder each under `skills/<category>/`. Keep each skill in one category. Every skill has an entry in its category's `README.md` and the top-level `README.md`, with its name linked to its `SKILL.md`. List each shipped skill path in `.claude-plugin/plugin.json`.

`CONTEXT.md` at the repo root defines the repo's own vocabulary. Use its terms in skills and docs.

Validate plugin packaging with `claude plugin validate . --strict`. Users install through the plugin or `npx skills add`, as the README documents. For maintainers only, `./scripts/link-skills.ps1` in PowerShell links every skill into `~/.claude/skills/` so edits are live in the next session without reinstalling; re-run it after adding, moving, or removing a skill, and remove the links before testing an npx or plugin install.

## Agent skills

### Issue tracker

Issues are tracked in this repo's GitHub Issues via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles use their default label names. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
