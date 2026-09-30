---
name: audit-terminology
description: Maintain the workspace's glossary. Use when audit terminology is missing, ambiguous, or contested, or when the auditor settles a definition useful across engagements.
---

# Audit Terminology

Actively build and sharpen the organization's audit vocabulary as you work. Challenge unclear terminology, test the boundaries between concepts, and record settled definitions as they emerge.

## File Structure

The workspace contains a single glossary file, in the context folder:

```text
/
└── context/
    └── GLOSSARY.md
```

Create `context/GLOSSARY.md` when the first term’s meaning is settled, using the structure in [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md). If the file already exists, update it in place.

## During the session

### Challenge and resolve meanings

- **Challenge against the glossary.** When usage conflicts with an existing definition, surface the specific difference immediately. Ask which meaning holds.
- **Sharpen fuzzy language.** When a word is ambiguous or vague, propose a precise canonical term. Distinguish separate concepts before treating their names as synonyms.
- **Test boundaries with scenarios.** Use concrete scenarios to clarify where one concept ends and another begins. Use them when it helps resolve a distinction.
- **Check against sources.** Compare the proposed meaning with relevant methodology, organizational context, and supplied materials. If they conflict, surface them for resolution with the auditor.

### Record settled definitions inline

Before adding a new term, check whether the glossary already defines the same or a closely related concept. Reconcile with the existing term rather than creating duplicate, overlapping, or competing definitions.

When a term is resolved, update `context/GLOSSARY.md` immediately rather than batching updates at the end. Use the format specified in [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md).

`GLOSSARY.md` should contain one consistent term and meaning for every concept. Keep it limited to audit terminology and definitions.
