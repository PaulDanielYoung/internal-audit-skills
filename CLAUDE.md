Skills live one folder each under `skills/`. Every skill has an entry in the top-level `README.md`, with its name linked to its `SKILL.md`. `.claude-plugin/plugin.json` ships every folder under `skills/`; there is no curated list to keep in sync.

`CONTEXT.md` at the repo root defines the repo's own vocabulary (seed glossary, working glossary, driver, report). Use its terms in skills and docs.

The working glossary is `GLOSSARY.md` in the user's working directory. Skills read it if it exists and proceed without it otherwise. Only the `glossary` skill edits it; other skills call that skill when a term is missing or contested. The seed glossary lives inside the glossary skill at `skills/glossary/SEED-GLOSSARY.md`, so it travels with the skill under every install route; nothing outside that folder should link to it by a relative path.

For local testing, `.claude/skills` is a gitignored junction onto `skills/`, so the skills load in this repo without copying. Recreate it on a fresh clone with `New-Item -ItemType Junction -Path .claude\skills -Target skills`.
