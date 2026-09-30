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

## Skills

Skills are organized into shared capabilities (Foundations, Guidance, and Writing) and engagement stages (Planning, Walkthroughs, Fieldwork, and Reporting). Their invocation names stay the same.

### [Foundations](skills/foundations/README.md)

- [`setup-internal-audit-skills`](skills/foundations/setup-internal-audit-skills/SKILL.md) prepares a new or existing auditor workspace, its `context/` folder, and its project instructions. Invoke it explicitly for setup.
- [`audit-terminology`](skills/foundations/audit-terminology/SKILL.md) sharpens audit terminology and maintains agreed definitions in the workspace's `context/GLOSSARY.md`, creating it when the first definition is settled.
- [`shared-understanding`](skills/foundations/shared-understanding/SKILL.md) resolves ambiguity with the user before a judgment is made or work is produced.
- [`create-engagement`](skills/foundations/create-engagement/SKILL.md) creates the engagement record and folders from an engagement name and audit objective statement. Every later engagement skill starts from it.
- [`document-request-list`](skills/foundations/document-request-list/SKILL.md) proactively suggests requests for auditor approval and maintains one Markdown document request list per engagement as information and received files become available.

### [Guidance](skills/guidance/README.md)

Skills that answer an auditor's question from the context folder without producing a workspace file.

- [`guidance`](skills/guidance/guidance/SKILL.md) is the one entry point for any question about methodology, policies, or regulations. It routes the question to the right ask skill and combines the answers when more than one source applies. Invoke it explicitly.
- [`ask-methodology`](skills/guidance/ask-methodology/SKILL.md) answers an auditor's question from the workspace's `context/METHODOLOGY.md`, separating what it documents from what it leaves unaddressed.
- [`ask-policy`](skills/guidance/ask-policy/SKILL.md) answers an auditor's question from the policies in `context/policies/`, citing each policy, section, and effective date relied on.
- [`ask-regulation`](skills/guidance/ask-regulation/SKILL.md) answers an auditor's question from the regulations in `context/regulations/`, citing each instrument, provision, and effective date relied on.

### [Writing](skills/writing/README.md)

Skills for writing and reviewing reusable audit statements and procedures, used across engagement stages.

- [`process-statements`](skills/writing/process-statements/SKILL.md) writes and reviews process titles and descriptions, including purpose, boundaries, roles, and systems.
- [`risk-statements`](skills/writing/risk-statements/SKILL.md) writes and reviews risk titles and descriptions, connecting events, causes, and consequences to objectives.
- [`control-statements`](skills/writing/control-statements/SKILL.md) writes and reviews intended-design control titles and descriptions, preserving inline sources and separately referring contrary practice.
- [`design-adequacy-procedures`](skills/writing/design-adequacy-procedures/SKILL.md) writes and reviews procedures for assessing whether control design addresses the relevant risk, with implementation checks when requested.
- [`operating-effectiveness-procedures`](skills/writing/operating-effectiveness-procedures/SKILL.md) writes and reviews operating-effectiveness test steps, including evidence, evaluation criteria, population, period, and selection details.

### [Planning](skills/planning/README.md)

- [`preliminary-survey`](skills/planning/preliminary-survey/SKILL.md) establishes a sourced understanding of the activity, maintains its process list and stable Process IDs, and identifies leads and information gaps for risk assessment.
- [`risk-assessment`](skills/planning/risk-assessment/SKILL.md) develops sourced inherent risks, presents ratings for the auditor's judgement, and ranks the assessment for planning.
- [`planning-memo`](skills/planning/planning-memo/SKILL.md) records auditor-agreed objectives and scope, sourced criteria and approach, and the team, budget, and timeline for the RCM handoff.
- [`risk-and-control-matrix`](skills/planning/risk-and-control-matrix/SKILL.md) owns the preliminary RCM and Control IDs, plans procedures for controls and risk gaps, and generates its HTML view from Markdown.

### [Walkthroughs](skills/walkthroughs/README.md)



### [Fieldwork](skills/fieldwork/README.md)

- [`exploratory-data-analysis`](skills/fieldwork/exploratory-data-analysis/SKILL.md) explores one CSV or one selected values-only XLSX table and opens a temporary offline HTML report of it.

### [Reporting](skills/reporting/README.md)


