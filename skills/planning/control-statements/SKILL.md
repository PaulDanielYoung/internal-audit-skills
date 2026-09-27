---
name: control-statements
description: Write a control title and intended-design description with roles, timing, precision, exception handling, and inline sources. Use when writing, reviewing, improving, or diagnosing control descriptions.
---

A control is any action taken by management, the board, and other parties to manage risk and increase the likelihood that established goals are achieved. Write or review its **title** and **intended-design description**, returning wording to the auditor or calling skill.

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

Evidence of performance is optional; include it only when a source states it. Evidence examination belongs to `planned-procedures`.

## Shared context and gaps

Read the workspace glossary, if present, and use its definitions for control and role; without one, the meanings above apply. Read the relevant methodology and organization context too, using their canonical role and system names, and proceed silently when absent. Documented methodology governs the wording; the pattern above is a starting point.

Use `audit-terminology` for missing, ambiguous, or contested terms and settled definitions. Use `shared-understanding` for material uncertainty about methodology or organizational facts. Pass the specific question and available evidence.

Call the Skill tool with `shared-understanding` when material ambiguity about intended design, its governing source, or whether activities form one control could change the wording. Mark missing facts in place with bracketed gaps, such as `[frequency not identified]` or `[exception handling not established]`; use only details supported by local material or the auditor. Preserve the caller's gap markers, short inline retained-source references, and basis labels. The calling stage skill arranges retention through `engagement-sources` and owns artifact sourcing.

## Intended design and boundaries

Describe intended design and intended frequency from applicable policy or procedure, or an attributed management or auditor account when those documents are silent. Identify the supported activity rather than inferring one from a requirement alone. Keep short source references beside the details they support.

Keep known contrary practice outside the baseline description: return a separately attributed note and retained-source reference linked by Control ID for the caller to retain for walkthroughs or fieldwork. A monthly policy activity remains monthly when quarterly practice is reported. The departure is material for later examination, not an automatic final finding.

For a risk without an identified control, leave the title and description empty; return the gap to the caller and route gap-confirmation or assessment wording to `planned-procedures`.

Judge clarity, completeness, and testability. Design adequacy and recommended improvements stay with walkthroughs and the auditor. Owner, Frequency, Type, and Nature fields belong to the caller; flag any supplied attribute that contradicts intended design and leave the fields unchanged.

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
- **Operating practice substituted for intended design.** Keep the supported design and intended frequency in the description, with contrary practice separately attributed and linked by Control ID.
- **Invented or guessed details.** Use supported intended-design facts and bracketed gaps for unknowns; an account of design does not establish performance or evidence.
- **An adequacy judgement or recommended improvement in the description.** State what the control does, leaving adequacy and improvements to walkthroughs and the auditor.
- **Procedure or evidence-examination detail in the description.** Describe intended control activity; leave planned examination to `planned-procedures`.
- **A description that contradicts a supplied attribute field.** Flag the conflict and propose source-supported wording or a gap while leaving the attribute unchanged; use `shared-understanding` when the governing fact is materially ambiguous.

## Review output

Check the title, intended-design basis, inline references, and every completeness element as well as the faults. Check that any contrary practice has a separate attributed handoff linked by Control ID. For several controls, also compare pairs for duplicates (the same activity under different titles or Control IDs) and combined controls.

Name each fault found using the names above, explicitly identify duplicates, explain any other unmet requirement, and propose a revised title and description for affected wording. Preserve gap markers, source links, and basis labels in the revisions. Keep any split or merge as a recommendation for the caller rather than changing the control list or IDs. Confirm sound wording and leave it unchanged, without rewriting for style.
