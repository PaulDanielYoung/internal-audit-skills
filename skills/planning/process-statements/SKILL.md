---
name: process-statements
description: Write a clear process title and description that says what the process achieves, where it starts and ends, and who does what with which systems. Use when writing, reviewing, improving, or diagnosing process descriptions.
---

A process is one coherent flow from a start trigger to an end point. Write or review its **Process Title** and **Process Description**, returning wording to the auditor or calling skill. This planning writing skill owns no artifact, process list, or IDs.

## Starting pattern and completeness

The **Process Title** is a noun phrase of two to five words naming the flow by what it does, such as "Vendor onboarding". It is unique within the activity and contains no organization unit, system, or control.

A useful starting point for the **Process Description** is:

> [Roles] [main activities] in [systems], starting when [trigger] and ending when [end point], so that [purpose].

Adapt the wording to the context. Write one present-tense paragraph, roughly two to five sentences, stating facts. A description is complete when a reader can point to:

- **Purpose:** what the process achieves.
- **Start trigger and end point:** where the flow begins and ends.
- **Main activities:** what happens in sequence, at summary level.
- **Roles:** who performs the activities, by role rather than person.
- **Systems:** what systems the roles use.
- **Key inputs and outputs:** what enters and leaves the flow, where these clarify the boundaries.

Describe operation as the sources show it. When a source describes intended design and another shows divergent practice, state both and attribute each to its source without resolving between them. Describe approvals, reconciliations, and reviews as plain activities, without labelling them controls or adding adequacy, risk, or weakness judgements. Control wording belongs to `control-statements`; risk wording belongs to `risk-statements`.

## Shared context and gaps

Read the workspace glossary for process, activity, and role names, and relevant methodology and organization context for canonical role and system names, if present. Proceed silently when absent. Documented methodology governs the wording; the pattern above is a starting point.

Use `audit-context` when a needed term is missing from an existing glossary, terminology is contested or unclear, or persistent methodology or organization context needs updating or clarification. Pass the specific question and available evidence.

Use `shared-understanding` for material ambiguity that could change the wording, particularly a process boundary or whether two flows are one process. Mark missing facts in place with bracketed gaps, such as `[system not identified]` or `[end point not established]`; never invent an actor, system, step, or boundary. Preserve the caller's gap markers, source links, and basis labels. Source retention and artifact sourcing rules stay with the calling stage skill.

## Single process layer

Keep one process layer. Summarize related parts of a flow as activities. If distinct flows need separate descriptions, recommend sibling processes. Adding, splitting, merging, or retiring processes belongs to `preliminary-survey`; recommend splits or merges and leave the process list and IDs unchanged.

## Faults

Use these when reviewing, improving, or diagnosing. Each fault names what sound wording has instead.

- **A title that names a department, system, or control rather than the flow.** Name the flow with a short, unique noun phrase.
- **A description that restates the title.** Explain the purpose and the activities that achieve it, with roles, systems, and key inputs and outputs.
- **A missing start or end boundary.** State a concrete trigger and end point, including a clear handoff to the next process where supported.
- **Overlap with a sibling process.** Give each flow distinct boundaries and activities; recommend a boundary clarification or merge where the sources support it.
- **A subprocess nested inside the description.** Summarize it as an activity or recommend a separate sibling process, keeping one process layer.
- **Procedure-level detail, such as keystrokes or field-by-field steps.** Describe the main activities in sequence at summary level.
- **An embedded control or risk judgement.** State the activity as fact, leaving adequacy and risk judgements to their owning work.
- **Intended design presented as observed practice.** Attribute intended design and actual practice to their respective sources, stating both when they diverge.
- **Invented or guessed actors or systems.** Use supported roles and systems, with bracketed gaps for unknowns.
- **Several distinct flows combined under one title.** Describe one coherent flow from trigger to end point; recommend a split when separate flows need separate boundaries.

## Review output

Check the title, description form, and every completeness element as well as the faults. For several processes, also compare pairs for overlap and handoff gaps between one process's end and the next one's start. Report a handoff gap explicitly; whether the list covers the whole activity remains the survey's responsibility.

Name each fault found using the names above, explain any other unmet requirement, and propose a revised title and description for affected wording. Preserve gap markers, source links, and basis labels in the revisions. Keep any split or merge as a recommendation for the survey rather than applying it. Confirm sound wording and leave it unchanged, without rewriting for style.
