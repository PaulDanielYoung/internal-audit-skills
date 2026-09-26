# Internal Audit Skills

Open-source AI skills for internal auditors using local Claude Code.

## Installation

As a Claude Code plugin, from a session:

```
/plugin marketplace add PaulDanielYoung/internal-audit-skills
/plugin install internal-audit-skills@internal-audit-skills
```

Or with the skills CLI, from a terminal:

```
npx skills add PaulDanielYoung/internal-audit-skills -g
```

The plugin prefixes each skill name with `internal-audit-skills:`; the CLI installs the plain names. Reinstall to pick up a new version.

## Skills

Skills are organized by where an auditor would first reach for them. Their invocation names stay the same.

### [Foundations](skills/foundations/README.md)

- [`setup-internal-audit-skills`](skills/foundations/setup-internal-audit-skills/SKILL.md) prepares a new or existing auditor workspace and its project instructions. Invoke it explicitly for setup.
- [`audit-context`](skills/foundations/audit-context/SKILL.md) maintains the glossary, documented methodology, and organizational context shared across engagements. It includes a guide and template for each document.
- [`shared-understanding`](skills/foundations/shared-understanding/SKILL.md) resolves ambiguity with the user before a judgment is made or work is produced.
- [`create-engagement`](skills/foundations/create-engagement/SKILL.md) creates the engagement record from an engagement name and audit objective statement. Every later engagement skill starts from it.
- [`request-list`](skills/foundations/request-list/SKILL.md) maintains the shared engagement information-request list across audit phases and drafts request messages and reminders on demand.

### [Planning](skills/planning/README.md)

- [`engagement-notification`](skills/planning/engagement-notification/SKILL.md) drafts the initial communication to management and, on demand, an entrance meeting agenda; request work routes to `request-list` when available.
- [`preliminary-survey`](skills/planning/preliminary-survey/SKILL.md) describes the activity from retained sources, owns the process list and stable Process IDs, and flags matters for risk assessment.
- [`risk-assessment`](skills/planning/risk-assessment/SKILL.md) develops sourced inherent risks, presents ratings for the auditor's judgement, and ranks the assessment for planning.
- [`planning-memo`](skills/planning/planning-memo/SKILL.md) records auditor-agreed objectives and scope, sourced criteria and approach, and the team, budget, and timeline for the RCM handoff.
- [`risk-statements`](skills/planning/risk-statements/SKILL.md) turns a risk, concern, or vague topic into a clear risk statement.
- [`process-statements`](skills/planning/process-statements/SKILL.md) writes and reviews process titles and descriptions, including purpose, boundaries, roles, and systems.
- [`control-statements`](skills/planning/control-statements/SKILL.md) writes and reviews intended-design control titles and descriptions, preserving inline sources and separately referring contrary practice.
- [`planned-procedures`](skills/planning/planned-procedures/SKILL.md) writes and reviews planned design, walkthrough, operating-effectiveness, risk-gap, and auditor-selected direct examination procedures.

### [Walkthroughs](skills/walkthroughs/README.md)

Skills for walkthroughs will be listed here as they are added.

### [Fieldwork](skills/fieldwork/README.md)

- [`exploratory-data-analysis`](skills/fieldwork/exploratory-data-analysis/SKILL.md) explores one CSV or one selected values-only XLSX table and opens a temporary offline HTML report of it.

### [Reporting](skills/reporting/README.md)

Skills for reporting will be listed here as they are added.

## Auditor workspace

Keep shared context at the root of your audit workspace, separate from the installed skills:

```text
CLAUDE.md
GLOSSARY.md
METHODOLOGY.md
ORGANIZATION.md
engagements/
  <year>/
    <engagement-name>/
      ENGAGEMENT.md
```

Create a folder for audit work, start Claude Code there, and run setup once:

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Projects\audit-workspace" -Force
Set-Location "$env:USERPROFILE\Projects\audit-workspace"
claude
```

```text
/internal-audit-skills:setup-internal-audit-skills
```

With the CLI install, the command is `/setup-internal-audit-skills`. You can also supply a target folder to the setup skill from an existing session; it creates a missing folder and preserves existing workspace content. Then start a session in that workspace so its project instructions load.

Setup delegates the context documents to `audit-context`, which creates any that are missing from its templates, and adds `engagements/` and the project instructions in `CLAUDE.md`. Existing files are preserved. Then capture context, for example:

> Use audit-context to capture the organizational material at the path I provide.

Definitions are agreed with you, methodology comes from documented sources, and organizational facts come from your material or explicit statements. As you work, Claude offers to record terms, methodology points, and organizational facts that get settled, and writes each one when you accept. Other skills read the context when present; `audit-context` needs setup to have run and asks you to run it if not.

Individual audit material belongs under `engagements/`. Start an engagement with `create-engagement`, giving its name and audit objective statement; it writes the engagement record under the annual-plan year. In later conversations, name the engagement you are working on and the engagement skills use its record and folder. Use `engagement-notification` to draft the initial communication to management.

## License

[MIT](LICENSE)
