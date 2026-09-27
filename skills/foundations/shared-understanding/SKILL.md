---
name: shared-understanding
description: Resolve material ambiguity with the user before making a judgment or producing work. Use when missing context, assumptions, preferences, or decisions could materially change the result.
---

# Shared Understanding

Reach a shared understanding before proceeding with work that depends on unresolved decisions or assumptions.

Find the **facts** yourself first. Read the available files, tools, policies, procedures, prior work, and other evidence before asking the user for anything you can determine on your own. The **decisions** are the user's; put each material decision to them.

If additional material the user can provide would improve the answer, name the specific kind that would help (for example policies, procedures, audit reports, prior workpapers, meeting notes, etc.).

## Work the decision tree

Map the unresolved **questions** as a **decision tree**. A question may depend on facts or on other decisions that must be settled first.

The **frontier** is the set of material unresolved questions whose prerequisites are already settled: the questions that can be answered now without guessing about another unresolved fact or decision.

Ask the frontier in **rounds**.

If the frontier is reasonably small, ask all of its questions in the same round. If it is large, ask the highest-leverage questions first in a manageable group while preserving dependency order.

Do not ask a question whose answer depends on another unresolved question in the same round.

For each decision question, give a recommended answer and briefly explain the reasoning. Make the recommendation specific enough that the user can accept it, modify it, or choose another option. For missing facts, ask for the fact or supporting evidence; suggest how to establish it when useful.

Format each question as shown below for its type, numbering questions in order within the round:

```
❓ **Q1** - **{decision question title}**

{question body, including choices where useful}

➡️ **Recommended answer**

{recommended answer and brief reasoning}
---
❓ **Q2** - **{factual question title}**

{question asking for the missing fact or supporting evidence}

➡️ **Suggested source**

{where or how to establish the fact, when useful; otherwise omit this section}
```

After each round, reassess the decision tree. The user's answers may settle other questions, introduce new ones, change assumptions, or move the frontier.

## Know when to stop

Shared understanding is complete when no **material** unresolved question, decision, or assumption remains that could change the work. Summarize the resulting shared understanding when this criterion is met.

If material questions remain but none can be answered until unavailable evidence or a prerequisite decision is supplied, report the blocked questions and what would unblock them. Keep dependent work pending and continue unaffected work.

If this skill was invoked by another skill, return the settled understanding and any blockers so the invoking skill can continue supported work.

If this skill was invoked directly as part of work the user already requested, continue supported work after presenting the settled understanding and any blockers.
