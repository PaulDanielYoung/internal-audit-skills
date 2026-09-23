---
name: glossary
description: Build and sharpen the project's GLOSSARY.md, the definitions every other skill reads. Use when a term is missing, unclear, or used inconsistently, when writing or editing GLOSSARY.md, or when a project has none yet.
---

# Glossary

`GLOSSARY.md` at the root of the working directory holds the project's definitions. Every skill in this set reads it before judging or writing; this skill is the only one that edits it. Other skills call this skill when a term is missing or contested.

## Creating one

Create the file only when there is a definition to record. Offer to start from the seed glossary in [SEED-GLOSSARY.md](SEED-GLOSSARY.md), which holds the general internal audit definitions the skills assume, and adapt its wording to the organization's own terminology.

## During the session

- **Challenge against the glossary.** When the user's material uses a term in a way that conflicts with its definition, say so at once and ask which meaning holds.
- **Sharpen fuzzy language.** When a word carries more than one meaning, propose a precise canonical term. The organization's established term wins over the seed's.
- **Put each definition to the user.** Definitions are the user's decision. Give a recommended wording and write it once they accept or amend it.
- **Update inline.** Record a resolved term immediately, in the session where it was settled. A task-specific exception or temporary interpretation stays in the conversation.
- **Glossary and nothing else.** No procedures, findings, engagement detail, or notes. Anything that is not a definition belongs elsewhere.

## Format

```md
**Term**
One or two sentences stating what it is, not what it does.
_Avoid_: synonyms the project does not use
```

- **Be opinionated.** When several words exist for one concept, pick one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences.
- **Only terms specific to audit practice or this organization.** General English and general business terms stay out.
- **Group terms under headings** when natural clusters emerge. A flat list is fine until then.
