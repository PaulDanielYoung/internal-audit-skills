---
name: ask-policy
description: Answer the user's question from the organization's policies, citing the documents and sections relied on. Use when the auditor asks a question about a policy, procedure, or standard the organization has approved.
---

# Ask Policy

Answer the auditor's question from the policies in `context/policies/`, as a reply in the conversation.

## Find every policy and section that bears on the question

Open `context/INDEX.md` and select every row in the Policies table whose title or description bears on the question. Read each selected document in full, including sections that apply indirectly, such as definitions, exceptions, approvals, and review cycles. The search is done when each part of the question is matched to a section of a policy or confirmed as **not addressed**.

## Label each part of the answer

Each part of the answer carries one of three labels:

- **Stated**: the policy says it. Cite the policy by title and the section by heading, and keep its force: a "must" stays a requirement, a "should" stays guidance. Quote prescribed values word for word, such as thresholds, frequencies, required approvals, and retention periods.
- **Inferred**: it reasonably follows from applying a stated section to the auditor's situation. Name the policy and section reasoned from and mark the inference as yours.
- **Not addressed**: no policy covers this part of the question. Say so plainly; that completes the policy answer for that part. When useful, supplement the answer with general practice from authoritative external sources, clearly identified as separate from the organization's policies.

An empty Policies table leaves the whole question not addressed.

## Shape the answer

Format the answer as shown below, with one block per part and only the labels the answer uses:

```
💬 **Answer**

{direct answer to the auditor's question}

---
📖 **Stated** - **{title}**

{what the policy says}

📍 {policy title}, {section heading}, effective {effective_date}
---
🧩 **Inferred** - **{title}**

{what follows for the auditor's situation}

📍 Reasoned from {policy title}, {section heading}, effective {effective_date}
---
⚠️ **Not addressed** - **{title}**

No policy addresses {part of the question}.

💡 **General practice**: {general practice that helps; otherwise omit this line}
---
➡️ **Recommendation**

{what the auditor should do next}
```
