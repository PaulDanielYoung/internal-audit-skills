# Internal Audit Skills

Open-source AI skills for internal auditors.

## Installation

As a Claude Code plugin, from a session:

```
/plugin marketplace add PaulDanielYoung/internal-audit-skills
/plugin install internal-audit-skills@internal-audit-skills
```

Or copy editable skill files into your project with [skills.sh](https://skills.sh), on any agent:

```bash
npx skills@latest add PaulDanielYoung/internal-audit-skills
```

## Skills

Skills are organized by where an auditor would first reach for them. Their invocation names stay the same.

### [Foundations](skills/foundations/README.md)

- [`glossary`](skills/foundations/glossary/SKILL.md) builds and sharpens the project's `GLOSSARY.md`, the definitions the other skills read, starting from the [seed glossary](skills/foundations/glossary/SEED-GLOSSARY.md).
- [`shared-understanding`](skills/foundations/shared-understanding/SKILL.md) resolves ambiguity with the user before a judgment is made or work is produced.

### [Planning](skills/planning/README.md)

- [`risk-statements`](skills/planning/risk-statements/SKILL.md) turns a risk, concern, or vague topic into a clear risk statement.

### [Walkthroughs](skills/walkthroughs/README.md)

Skills for walkthroughs will be listed here as they are added.

### [Fieldwork](skills/fieldwork/README.md)

- [`exploratory-data-analysis`](skills/fieldwork/exploratory-data-analysis/SKILL.md) explores one CSV or one selected values-only XLSX table and opens a temporary offline HTML report of it.

### [Reporting](skills/reporting/README.md)

Skills for reporting will be listed here as they are added.

## License

[MIT](LICENSE)
