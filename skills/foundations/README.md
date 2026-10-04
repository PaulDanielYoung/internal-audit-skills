# Foundations

Skills used across audit phases.

- [`setup-internal-audit-skills`](setup-internal-audit-skills/SKILL.md) prepares a new or existing auditor workspace and its `context/` folder in local Claude Code. Invoke it explicitly for project setup.
- [`shared-understanding`](shared-understanding/SKILL.md) resolves material ambiguity with the user before work depends on an assumption.
- [`ask-context`](ask-context/SKILL.md) answers an auditor's question from `context/METHODOLOGY.md` and the policies in `context/policies/`, separating what they state from what is inferred and what they leave unaddressed.
- [`create-engagement`](create-engagement/SKILL.md) creates the engagement record and folders from an engagement name and audit objective statement. Every later engagement skill starts from it.
- [`document-request-list`](document-request-list/SKILL.md) proactively proposes requests for auditor approval, reconciles received files against them, and maintains one internal Markdown document request list per engagement.
