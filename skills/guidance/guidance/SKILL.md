---
name: guidance
description: Answers methodology, policy, and regulation questions through the relevant ask skills.
disable-model-invocation: true
---

# Guidance

Answer the auditor's question from the context folder by routing it to the right source, as a reply in the conversation.

## 1. Classify the question

Match each part of the question by subject to every relevant source category:

| Source | Answers questions about | Answered by |
|---|---|---|
| Methodology | how the internal audit function performs and documents its work | `ask-methodology` |
| Policies | management's own criteria: what the organization requires of itself | `ask-policy` |
| Regulations | what the law requires of the organization | `ask-regulation` |

Read `context/INDEX.md` to locate the available sources. A missing index, document, or empty table is an evidence gap; keep the question assigned to its relevant source category.

Handle these cases as they arise:

- **A task, not a question**: name the skill whose description fits the task, in one line, and stop.
- **Genuinely ambiguous**: missing facts or unclear intent would materially change which sources apply or how the question is answered. Call `shared-understanding` to resolve that uncertainty, then resume classification. Continue with unaffected parts.
- **Outside scope**: a clear question falls outside all three source categories. State that boundary for that part and continue with any in-scope parts.

Classification is done when every part has all relevant source categories identified, is outside scope, or is pending a specific clarification. Multiple applicable sources, including a request to compare them, proceed to gathering answers.

## 2. Gather the answers

Invoke the ask skill for each matched source category with its assigned question parts and the full question as context. Ask it to answer only the assigned parts, using its existing labels and citations.

Where sources are unavailable, report which assigned parts cannot be assessed from the available context. Use **Not addressed** for the ask skills' documented empty-source cases or when the available sources do not cover a part; distinguish those from a listed document that could not be read.

## 3. Reply

**One source**: return its answer unchanged, appending any outside-scope parts or pending clarifications.

**Two or more sources**: synthesize. Preserve every applicable requirement that can be satisfied together. Where requirements are incompatible, show the conflicting provisions and identify what remains unresolved. Gather and compare the sources before deciding whether missing facts or unclear intent require `shared-understanding`.

In the combined **Answer** and **Recommendation**, preserve each source's uncertainty and distinguish stated requirements, inferences, and general practice. Keep evidence gaps, outside-scope parts, pending clarifications, and unresolved conflicts visible.

The reply is complete when every question part has a supported answer or an explicit limitation. If no part can be answered, return those limitations and what would resolve them. Otherwise, format a multi-source reply as shown below, with only the blocks the answer uses:

```
💬 **Answer**

{one direct answer to the auditor's question, drawing on every source consulted}

---
🛠️ **Methodology**

{that skill's answer, minus its Answer and Recommendation blocks}
---
📋 **Policy**

{that skill's answer, minus its Answer and Recommendation blocks}
---
⚖️ **Regulation**

{that skill's answer, minus its Answer and Recommendation blocks}
---
➡️ **Recommendation**

{what the auditor should do next, reconciling each source's recommendation}
```
