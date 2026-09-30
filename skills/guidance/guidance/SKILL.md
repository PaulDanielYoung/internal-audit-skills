---
name: guidance
description: One entry point for any question about methodology, policies, or regulations. Routes the question to the right ask skill and combines the answers.
disable-model-invocation: true
---

# Guidance

Answer the auditor's question from the context folder by routing it to the right source, as a reply in the conversation.

## 1. Classify the question

Read `context/INDEX.md` to see which sources the workspace holds. Match each part of the question to the sources that bear on it:

| Source | Answers questions about | Answered by |
|---|---|---|
| Methodology | how the internal audit function performs and documents its work | `ask-methodology` |
| Policies | management's own criteria: what the organization requires of itself | `ask-policy` |
| Regulations | what the law requires of the organization | `ask-regulation` |

Classification is done when every part of the question has at least one source, or the question is recognized as one of the two cases below.

- **A task, not a question**: name the skill whose description fits the task, in one line, and stop.
- **Genuinely ambiguous**: two sources plausibly apply and their answers could conflict, or the question can't be matched to any source. Call `shared-understanding` to settle the intent with the auditor before answering.

## 2. Gather the answers

Invoke the ask skill for each matched source with the auditor's question.

## 3. Reply

**One source**: return its answer unchanged.

**Two or more sources**: synthesize. Sources rank by precedence when they bear on the same point: a regulation over a policy; the methodology governs the auditor's own work rather than the auditee's, so it doesn't compete with either. Format the reply as shown below, with only the blocks the answer uses:

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
