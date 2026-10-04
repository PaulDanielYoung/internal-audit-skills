# Internal Audit Skills

A collection of AI agent skills for internal auditors, built for Claude Code.

The skills are designed to work together across the internal audit lifecycle—from planning and walkthroughs through fieldwork, reporting, and follow-up. They are grounded in established internal audit practices and principles, while remaining flexible enough to adapt to your organization’s methodology, terminology, and way of working.

Use them as a starting point. Change the wording, add or remove skills, modify the workflows, and experiment with new ideas. Make them your own and adapt them to the way you and your team actually work.

If you’re using these skills, have feedback, or have ideas for improving or expanding them, I’d love to hear from you. Feel free to reach out at pauldanielyoung@outlook.com.

## How it works

Create a new folder on your computer and open it in Claude Code. Download the skills, then run the `setup-internal-audit-skills` to initialize the workspace. It configures `CLAUDE.md`, adds the workspace instructions the skills follow, and creates the `context/` structure for your organization’s context.

Populate `context/METHODOLOGY.md` and `context/ORGANIZATION.md`. Add relevant policies as Markdown files to `context/policies/`.

When you’re ready to begin an audit, run the `create-engagement` skill. It creates the engagement workspace and records the basic context for the audit, including its name and objective statement.

From there, the skills work together within the engagement, using both the organization and engagement level context to help you do your work.

## Installation

Run the following command in your terminal and desired workspace folder:

```sh
npx skills add PaulDanielYoung/internal-audit-skills
```

## Setup

Run `/setup-internal-audit-skills` once for each project. It initializes the workspace and creates the files and folders the skills rely on.

When you’re ready to begin an individual audit, run `/create-engagement`. It creates a dedicated engagement workspace and the supporting structure for that audit.

## Reference

### [Foundations](skills/foundations/README.md)

- [setup-internal-audit-skills](skills/foundations/setup-internal-audit-skills/SKILL.md) — Sets up your workspace, context folder, and instructions for Claude.
- [shared-understanding](skills/foundations/shared-understanding/SKILL.md) — Clarifies questions and assumptions that could materially change the work.
- [ask-context](skills/foundations/ask-context/SKILL.md) — Answers questions from your audit methodology and your organization’s policies, citing the relevant provisions.
- [create-engagement](skills/foundations/create-engagement/SKILL.md) — Creates an engagement record and folders from its name, objective, and year.
- [document-request-list](skills/foundations/document-request-list/SKILL.md) — Proposes document requests for your approval, matches received files to requests, and tracks what is still outstanding.

### [Writing](skills/writing/README.md)

- [process-statements](skills/writing/process-statements/SKILL.md) — Writes and reviews process titles and descriptions.
- [risk-statements](skills/writing/risk-statements/SKILL.md) — Writes and reviews risk titles and descriptions.
- [control-statements](skills/writing/control-statements/SKILL.md) — Writes and reviews control titles and descriptions.
- [design-adequacy-procedures](skills/writing/design-adequacy-procedures/SKILL.md) — Writes and reviews procedures for assessing whether controls are designed adequately.
- [operating-effectiveness-procedures](skills/writing/operating-effectiveness-procedures/SKILL.md) — Writes and reviews procedures for testing whether controls operated effectively.

### [Planning](skills/planning/README.md)

- [preliminary-survey](skills/planning/preliminary-survey/SKILL.md) — Gathers sufficient background information and understanding the activities operations. 
- [risk-assessment](skills/planning/risk-assessment/SKILL.md) — Identifies, evaluates, and prioritizes risks.
- [planning-memo](skills/planning/planning-memo/SKILL.md) — Records agreed objectives, scope, criteria, approach, team, budget, and timeline.
- [risk-and-control-matrix](skills/planning/risk-and-control-matrix/SKILL.md) — Links risks to controls and plans the engagement’s work program.

### [Fieldwork](skills/fieldwork/README.md)

- [exploratory-data-analysis](skills/fieldwork/exploratory-data-analysis/SKILL.md) — Explores a CSV or supported XLSX table and opens a temporary HTML report.

## Feedback and contributions

Found a problem or have an idea for a skill? [Open an issue](https://github.com/PaulDanielYoung/internal-audit-skills/issues). Feedback, suggestions, and contributions are welcome.

## Acknowledgments

Inspired by [Matt Pocock’s skills repository](https://github.com/mattpocock/skills).

## License

[MIT](LICENSE).
