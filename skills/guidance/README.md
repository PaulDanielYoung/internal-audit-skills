# Guidance

Skills that answer an auditor's question from the context folder without producing a workspace file.

- [`guidance`](guidance/SKILL.md) is the one entry point for any question about methodology, policies, or regulations. It routes the question to the right ask skill and combines the answers when more than one source applies. Invoke it explicitly.
- [`ask-methodology`](ask-methodology/SKILL.md) answers an auditor's question from the workspace's `context/METHODOLOGY.md`, separating what it documents from what it leaves unaddressed.
- [`ask-policy`](ask-policy/SKILL.md) answers an auditor's question from the policies in `context/policies/`, citing each policy, section, and effective date relied on.
- [`ask-regulation`](ask-regulation/SKILL.md) answers an auditor's question from the regulations in `context/regulations/`, citing each instrument, provision, and effective date relied on.
