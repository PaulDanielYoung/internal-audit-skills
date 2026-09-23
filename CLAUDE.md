Skills live one folder each under `skills/`. Every skill has an entry in the top-level `README.md`, with its name linked to its `SKILL.md`.

`GLOSSARY.md` at the repo root is the seed glossary: the general internal audit definitions the skills assume. Skills read the working directory's `GLOSSARY.md` if it exists and proceed without it otherwise. Only the `glossary` skill edits it; other skills call that skill when a term is missing or contested. Refer to the seed as `${CLAUDE_PLUGIN_ROOT}/GLOSSARY.md`, never by a relative path out of a skill folder, since installed skill folders are detached from the repo layout.

For local testing, `.claude/skills` is a gitignored junction onto `skills/`, so the skills load in this repo without copying. Recreate it on a fresh clone with `New-Item -ItemType Junction -Path .claude\skills -Target skills`.
