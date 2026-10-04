---
name: ask-context
description: Answer the auditor's question from the audit methodology and the organization's policies, citing the sections relied on. Use when the auditor asks what the methodology or a policy, procedure, or standard the organization has approved says or requires.
---

# Ask Context

Answer the auditor's question from the sources in `context/`, as a reply in the conversation.

## Sources

| Source | Location | Governs | Citation |
|---|---|---|---|
| Methodology | `context/METHODOLOGY.md` | How internal audit does its work | Methodology, {section heading} |
| Policy | Each document in `context/policies/` | What the organization holds itself to | {policy title}, {section heading}, effective {effective_date} |

## Find every section that bears on the question

Search the methodology for every section that bears on the question. Read the front matter of every document in `context/policies/`, select each policy whose title or description bears on the question, and read each selected policy in full.

Include sections that apply indirectly, such as definitions, exceptions, approvals, documentation standards, and review cycles. The search is done when each part of the question is matched to a section of a source or confirmed as **not addressed** by both.

A blank or absent methodology, or an empty `context/policies/`, contributes nothing; the parts it would have answered are not addressed.

## Label each part of the answer

Each part of the answer carries one of three labels:

- **Stated**: a source says it. Cite it as its row in the Sources table shows and keep its force: a "must" stays a requirement, a "should" stays guidance. Quote prescribed values word for word, such as thresholds, sample sizes, frequencies, required approvals, and retention periods.
- **Inferred**: it reasonably follows from applying a stated section to the auditor's situation. Cite the section reasoned from and mark the inference as yours.
- **Not addressed**: neither source covers this part of the question. Say so plainly; that completes the answer for that part. When useful, supplement it with general practice from authoritative external sources, clearly identified as separate from the organization's own sources.

When the methodology and a policy both bear on the same part, give each its own block so the auditor sees which source says what.

## Shape the answer

Format the answer as shown below, with one block per part and only the labels the answer uses:

```
💬 **Answer**

{direct answer to the auditor's question}

---
📖 **Stated** - **{title}**

{what the source says}

📍 {citation}
---
🧩 **Inferred** - **{title}**

{what follows for the auditor's situation}

📍 Reasoned from {citation}
---
⚠️ **Not addressed** - **{title}**

Neither the methodology nor the policies address {part of the question}.

💡 **General practice**: {general practice that helps; otherwise omit this line}
---
➡️ **Recommendation**

{what the auditor should do next}
```
