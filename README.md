# Internal Audit Skills

Open-source AI skills for internal auditors using local Claude Code.

## Installation

As a Claude Code plugin, from a session:

```
/plugin marketplace add PaulDanielYoung/internal-audit-skills
/plugin install internal-audit-skills@internal-audit-skills
```

Then open an auditor workspace in Claude Code and run:

```text
/internal-audit-skills:setup-internal-audit-skills
```

For development from this repository, use the local links below instead of installing a second plugin copy.

## Skills

Skills are organized by where an auditor would first reach for them. Their invocation names stay the same.

### [Foundations](skills/foundations/README.md)

- [`setup-internal-audit-skills`](skills/foundations/setup-internal-audit-skills/SKILL.md) prepares a new or existing auditor workspace and its project instructions. Invoke it explicitly for setup.
- [`audit-context`](skills/foundations/audit-context/SKILL.md) maintains the working glossary, documented methodology, and organizational context shared across engagements. It replaces `glossary` and includes a guide and unpopulated template for each document.
- [`shared-understanding`](skills/foundations/shared-understanding/SKILL.md) resolves ambiguity with the user before a judgment is made or work is produced.

### [Planning](skills/planning/README.md)

- [`risk-statements`](skills/planning/risk-statements/SKILL.md) turns a risk, concern, or vague topic into a clear risk statement.

### [Walkthroughs](skills/walkthroughs/README.md)

Skills for walkthroughs will be listed here as they are added.

### [Fieldwork](skills/fieldwork/README.md)

- [`exploratory-data-analysis`](skills/fieldwork/exploratory-data-analysis/SKILL.md) explores one CSV or one selected values-only XLSX table and opens a temporary offline HTML report of it.

### [Reporting](skills/reporting/README.md)

Skills for reporting will be listed here as they are added.

## Auditor workspace

Keep shared context at the root of your audit workspace, separate from these installed skills:

```text
CLAUDE.md
GLOSSARY.md
METHODOLOGY.md
ORGANIZATION.md
engagements/
```

Run `setup-internal-audit-skills` once per auditor workspace. It delegates the context documents to `audit-context`: all three start from clearly marked, unpopulated templates. Definitions are agreed with you, methodology comes from documented sources, and organizational facts come from your material or explicit statements. Existing documents are preserved. Use `audit-context` afterward to capture or update context. Other skills read it and call `audit-context` when it needs updating. Individual audit material belongs under `engagements/`; an engagement planning skill is not yet included.

Existing root-level working glossaries stay in place when switching from `glossary` to `audit-context`.

## Develop and try the skills locally

From this repository in PowerShell, run:

```powershell
./scripts/link-skills.ps1
```

This links each skill into your personal `~/.claude/skills/` directory. The links point directly to this repository, so source edits are available without copying or reinstalling. The script preserves unrelated skills and stops if an existing skill name belongs to another installation. Re-run it when adding, moving, or removing a skill.

Create a folder for audit work, start local Claude Code there, and run setup:

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Projects\audit-workspace" -Force
Set-Location "$env:USERPROFILE\Projects\audit-workspace"
claude
```

```text
/setup-internal-audit-skills
```

You can also supply a target folder to the setup skill from an existing session. It creates a missing folder and preserves existing workspace content. Then start a session in that workspace so its project instructions load.

Try a real task, for example:

> Use audit-context to read my audit manual at the path I provide and populate METHODOLOGY.md. Ask about material gaps or conflicts.

Inspect the changes, give feedback, and revise the skill source in this repository. Start a fresh session in the auditor workspace to retry with the revised instructions. Keep your workspace documents between runs; use a new folder when you want to test first-time setup. The local links are for Claude Code on this machine; they do not upload skills to Claude chat or Cowork.

## License

[MIT](LICENSE)
