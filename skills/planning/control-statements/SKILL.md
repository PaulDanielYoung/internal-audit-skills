---
name: control-statements
description: Write a clear control title and description that says who does what, when, how precisely, and what happens to exceptions. Use when writing, reviewing, improving, or diagnosing control descriptions.
---

A control is an activity that prevents or detects something going wrong. Write or review its **title** and **description**, returning wording to the auditor or calling skill. This planning writing skill owns no artifact, control list, IDs, In Scope flag, or Test Steps.

## Starting pattern and completeness

The **title** is a short noun phrase naming the action and its object, such as "Vendor master change review". It is unique within the engagement and contains no owner or ID. Include frequency or system only when needed to distinguish two controls.

A useful starting point for the **description** is:

> [Owner role] [action] [object] [frequency/timing], using [information or system], [precision: what is checked against what, any threshold]. Exceptions are [followed up how, by whom]. This [prevents/detects] [what goes wrong].

Adapt the wording to the context. A description is complete when a reader can point to:

- **Owner role:** who performs the control, by role rather than person or department.
- **Action and object:** the checkable activity and what it acts on.
- **Frequency or timing:** how often the activity happens or what triggers it.
- **Information or system:** what the performer uses.
- **Precision:** what is checked against what, including any applicable threshold.
- **Exception handling:** how exceptions are followed up and by whom.
- **Purpose:** what the control itself prevents or detects, without a Risk ID or risk-specific wording, so a shared control reads correctly on every row where it appears.

Evidence of performance is optional; include it only when a source states it. Evidence examination belongs to `test-steps`.

## Shared context and gaps

Read the workspace glossary, if present, and use its definitions for control and role; without one, the meanings above apply. Read the relevant methodology and organization context too, using their canonical role and system names, and proceed silently when absent. Documented methodology governs the wording; the pattern above is a starting point.

Use `audit-context` when a needed term is missing from an existing glossary, terminology is contested or unclear, or persistent methodology or organization context needs updating or clarification. Pass the specific question and available evidence.

Call the Skill tool with `shared-understanding` when material ambiguity about the control activity, its status, or whether activities form one control could change the wording. Mark missing facts in place with bracketed gaps, such as `[frequency not identified]` or `[exception handling not established]`; use only details supported by local material or the auditor. Preserve the caller's gap markers, source links, and basis labels. Source retention and artifact sourcing rules stay with the calling stage skill.

## Status and boundaries

Describe sourced controls as the sources show them. When intended design and observed practice differ, state both and attribute each to its source.

Write an expected control only on the auditor's explicit request. Open its description with **Expected control (auditor-added; not confirmed):** and use conditional voice, such as "would review" and "exceptions would be followed up". Keep proposed details visibly conditional and unknown elements marked as gaps. Never propose an expected control unprompted. For a not-yet-identified control, write no title or description; the row marker and clarification question belong to `risk-and-control-matrix`.

Judge clarity, completeness, and testability. Design adequacy, recommended improvements, and control scope stay with walkthroughs and the auditor. Owner, Frequency, Type, and Nature fields belong to the caller; flag any supplied attribute that contradicts the description and leave the fields unchanged.

## Faults

Use these when reviewing, improving, or diagnosing. Each fault names what sound wording has instead.

- **A title that names an owner, department, or system rather than the control activity.** Name the action and object with a short, unique noun phrase.
- **A description that restates the title.** Explain who performs the activity, when and how, its exception handling, and its purpose.
- **An owner missing or named as a person or department.** Identify the performing role, marking a gap when it is unknown.
- **Vague timing where a frequency or trigger is known.** Replace "periodically", "as needed", or "regularly" with the supported frequency or trigger.
- **A vague action with no checkable activity.** Explain what "monitors", "oversees", or "ensures" means in observable terms supported by the sources.
- **Missing precision.** State what is checked against what and any applicable threshold, marking unsupported details as gaps.
- **Missing exception handling.** State how exceptions are followed up and by whom, with gaps for unknowns.
- **A purpose missing or tied to one risk.** State what the control itself prevents or detects in wording that works across every linked risk and process.
- **A policy, requirement, or objective stated as a control.** Describe the activity that implements it when supported; a requirement such as "All payments must be approved" alone does not establish a control.
- **Several controls combined in one description.** Describe one control activity and recommend a split where separate activities need their own descriptions.
- **An expected control presented as established, or intended design presented as operating practice.** Carry the expected-not-confirmed marker and conditional voice for requested expected controls; attribute design and practice separately when they differ.
- **Invented or guessed details.** Use supported facts for sourced controls and bracketed gaps for unknowns; keep requested expected wording explicitly conditional.
- **An adequacy judgement or recommended improvement in the description.** State what the control does, leaving adequacy and improvements to walkthroughs and the auditor.
- **Test procedure or evidence-examination detail in the description.** Describe control performance; leave planned examination to `test-steps`.
- **A description that contradicts a supplied attribute field.** Flag the conflict and propose source-supported wording or a gap while leaving the attribute unchanged; use `shared-understanding` when the governing fact is materially ambiguous.

## Review output

Check the title, status, and every completeness element as well as the faults. For several controls, also compare pairs for duplicates (the same activity under different titles or Control IDs) and combined controls.

Name each fault found using the names above, explicitly identify duplicates, explain any other unmet requirement, and propose a revised title and description for affected wording. Preserve gap markers, source links, and basis labels in the revisions. Keep any split or merge as a recommendation for the caller rather than changing the control list or IDs. Confirm sound wording and leave it unchanged, without rewriting for style.
