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

- [`glossary`](skills/glossary/SKILL.md) builds and sharpens the project's `GLOSSARY.md`, the definitions the other skills read, starting from the [seed glossary](skills/glossary/SEED-GLOSSARY.md).
- [`shared-understanding`](skills/shared-understanding/SKILL.md) resolves ambiguity with the user before a judgment is made or work is produced.
- [`risk-statements`](skills/risk-statements/SKILL.md) turns a risk, concern, or vague topic into a clear risk statement.
- [`exploratory-data-analysis`](skills/exploratory-data-analysis/SKILL.md) explores one CSV or one selected values-only XLSX table and opens a temporary offline HTML report of it.

## License

[MIT](LICENSE)
