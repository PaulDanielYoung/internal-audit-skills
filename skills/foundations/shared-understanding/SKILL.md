---
name: shared-understanding
description: Resolve material ambiguity with the user before making a judgment or producing work. Use when missing context, assumptions, preferences, or decisions could materially change the result.
---

# Shared Understanding

Reach a shared understanding before proceeding with work that depends on unresolved decisions or assumptions.

Use the auditor's chosen workspace root, otherwise the parent of `engagements/` when working beneath it, otherwise the working directory. Read the working glossary (`GLOSSARY.md`) and relevant requirements in `METHODOLOGY.md` and facts in `ORGANIZATION.md` there when present. Documented methodology governs audit work; consult its sources when needed. Absent context files only need attention when the missing information is material. Use `audit-context` to record settled changes to shared context or resolve missing or contested terms; only that skill edits these files. If `audit-context` called this skill, return the resolved decisions to it for recording.

Find the **facts** yourself first. Read the available files, tools, policies, procedures, prior work, and other evidence before asking the user for anything you can determine on your own. The **decisions** are the user's; put each material decision to them.

If additional material only the user can provide would materially improve the answer, name the specific kind that would help—for example a methodology, policy, procedure, spreadsheet, report, prior workpaper, or meeting notes. Let the user answer the underlying question directly instead if they prefer.

## Work the decision tree

Map the unresolved **questions** as a **decision tree**. A question may depend on facts or on other decisions that must be settled first.

The **frontier** is the set of material unresolved questions whose prerequisites are already settled: the questions that can be answered now without guessing about another unresolved fact or decision.

Ask the frontier in **rounds**.

If the frontier is reasonably small, ask all of its questions in the same round. If it is large, ask the highest-leverage questions first in a manageable group while preserving dependency order.

Do not ask a question whose answer depends on another unresolved question in the same round.

For each question, give a recommended answer and briefly explain the reasoning. Make the recommendation specific enough that the user can accept it, modify it, or choose another option.

Format each round and question like so:

```
❓ **Q1** - **{question title}**

{question body, including choices where useful}

➡️ **Recommended answer**

{recommended answer and brief reasoning}
---
❓ Q2 - {question title}

{question body, including choices where useful}

➡️ Recommended answer

{recommended answer and brief reasoning}
```

After each round, reassess the decision tree. The user's answers may settle other questions, introduce new ones, change assumptions, or move the frontier.

## Know when to stop

Continue until no **material** unresolved question, decision, or assumption remains that could change the work.

When the frontier is empty, summarize the resulting shared understanding in the two-column table above.

Do **not** ask for a separate confirmation by default. Reaching an empty frontier means the shared understanding has been established from the user's answers and the available evidence.

If this skill was invoked by another skill, return the shared understanding and allow the invoking skill to continue.

If this skill was invoked directly as part of work the user already requested, continue with that work after presenting the shared understanding.
