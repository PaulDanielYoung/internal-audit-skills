Skills live one folder each under `skills/<category>/`. Keep each skill in one category. Every skill has an entry in its category's `README.md` and the top-level `README.md`, with its name linked to its `SKILL.md`. List each shipped skill path in `.claude-plugin/plugin.json`.

`CONTEXT.md` at the repo root defines the repo's own vocabulary (seed glossary, working glossary, driver, report). Use its terms in skills and docs.

The working glossary is `GLOSSARY.md` in the user's working directory. Skills read it if it exists and proceed without it otherwise. Only the `glossary` skill edits it; other skills call that skill when a term is missing or contested. The seed glossary lives inside the glossary skill at `skills/glossary/SEED-GLOSSARY.md`, so it travels with the skill under every install route; nothing outside that folder should link to it by a relative path.

For local testing on Windows, run `./scripts/link-skills.ps1` in PowerShell. It creates gitignored, flat junctions under `.claude/skills/` for the categorized skill folders, so their slash names stay unchanged. Re-run it after adding, moving, or removing a skill. Validate plugin packaging with `claude plugin validate . --strict`.
