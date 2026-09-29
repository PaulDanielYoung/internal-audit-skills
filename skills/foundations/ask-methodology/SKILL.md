---
name: ask-methodology
description: Answer the user's question using audit methodology, citing the sections relied on.
disable-model-invocation: true
---

# Ask Methodology

Answer the auditor's question from `METHODOLOGY.md`, as a reply in the conversation.

## Find every section that bears on the question

Search the methodology for every section that bears on the question, including sections that apply indirectly, such as documentation standards, approvals, or definitions governing the activity asked about. The search is done when each part of the question is matched to a section or found **silent**.

## Classify each statement

Every statement in the answer belongs to one of three classes, and the answer makes the class visible:

- **Stated**: what the methodology says. Cite the section by heading and keep its force: a "must" stays a requirement, a "should" stays guidance. Quote prescribed values word for word, such as thresholds, sample sizes, required fields, and approvals.
- **Inferred**: what reasonably follows from applying a stated section to the auditor's situation. Name the section reasoned from and mark the inference as yours.
- **Silent**: what the methodology leaves unaddressed. Report the part as silent; that report completes the answer for that part. Offer general audit practice where it helps, labelled as general practice.

A blank or absent `METHODOLOGY.md` makes the whole question silent. Say so in the first line of the answer.

## Shape the answer

Lead with the direct answer, then the methodology supporting it, then what the auditor should do next. When more than one approach is consistent with the methodology, lay out the approaches and recommend one for the circumstances.
