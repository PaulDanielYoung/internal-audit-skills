---
name: ask-regulation
description: Answer the user's question from the laws and regulations the organization must comply with, citing the instruments and provisions relied on. Use when the auditor asks a question about a regulatory requirement.
---

# Ask Regulation

Answer the auditor's question from the regulations in `context/regulations/`, as a reply in the conversation.

## Find every regulation and provision that bears on the question

Open `context/INDEX.md` and select every row in the Regulations table whose title or description bears on the question. Read each selected document in full, including provisions that apply indirectly, such as definitions, scope and applicability, exemptions, record-keeping, and reporting duties. The search is done when each part of the question is matched to a provision or confirmed as **not addressed**.

## Label each part of the answer

Each part of the answer carries one of three labels:

- **Stated**: the regulation says it. Cite the regulation by title and the provision by its section, article, or clause, and keep its force: a "shall" or "must" stays an obligation, a "may" stays a permission. Quote prescribed values word for word, such as deadlines, thresholds, retention periods, and required disclosures.
- **Inferred**: it reasonably follows from applying a stated provision to the auditor's situation. Name the regulation and provision reasoned from and mark the inference as yours.
- **Not addressed**: no regulation in the context folder covers this part of the question. Say so plainly; that completes the regulatory answer for that part. When useful, supplement the answer with general practice from authoritative external sources, clearly identified as separate from the regulations in the context folder.

An empty Regulations table leaves the whole question not addressed.

## Shape the answer

Format the answer as shown below, with one block per part and only the labels the answer uses:

```
💬 **Answer**

{direct answer to the auditor's question}

---
📖 **Stated** - **{title}**

{what the regulation says}

📍 {regulation title}, {provision}, effective {effective_date}
---
🧩 **Inferred** - **{title}**

{what follows for the auditor's situation}

📍 Reasoned from {regulation title}, {provision}, effective {effective_date}
---
⚠️ **Not addressed** - **{title}**

No regulation in the context folder addresses {part of the question}.

💡 **General practice**: {general practice that helps; otherwise omit this line}
---
➡️ **Recommendation**

{what the auditor should do next}
```
