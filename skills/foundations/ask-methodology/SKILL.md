---
name: ask-methodology
description: Answer the user's question using audit methodology, citing the sections relied on.
disable-model-invocation: true
---

# Ask Methodology

Answer the auditor's question from `METHODOLOGY.md`, as a reply in the conversation.

## Find every section that bears on the question

Search the methodology for every section that bears on the question, including sections that apply indirectly, such as documentation standards, approvals, or definitions governing the activity asked about. The search is done when each part of the question is matched to a section or confirmed as **not addressed**.

## Label each part of the answer

Each part of the answer carries one of three labels:

- **Stated**: the methodology says it. Cite the section by heading and keep its force: a "must" stays a requirement, a "should" stays guidance. Quote prescribed values word for word, such as thresholds, sample sizes, required fields, and approvals.
- **Inferred**: it reasonably follows from applying a stated section to the auditor's situation. Name the section reasoned from and mark the inference as yours.
- **Not addressed**: the methodology does not cover this part of the question. Say so plainly; that completes the methodology answer for that part. When useful, supplement the answer with general audit practice from authoritative external sources, clearly identified as separate from the methodology.
A blank or absent METHODOLOGY.md leaves the whole question not addressed.

## Shape the answer

Format the answer as shown below, with one block per part and only the labels the answer uses:

```
💬 **Answer**

{direct answer to the auditor's question}

---
📖 **Stated** - **{title}**

{what the methodology says}

📍 {section heading}
---
🧩 **Inferred** - **{title}**

{what follows for the auditor's situation}

📍 Reasoned from {section heading}
---
⚠️ **Not addressed** - **{title}**

The methodology does not address {part of the question}.

💡 **General practice**: {general audit practice that helps; otherwise omit this line}
---
➡️ **Recommendation**

{what the auditor should do next}
```

When more than one approach is consistent with the methodology, lay out the approaches in the recommendation and recommend one for the circumstances.
