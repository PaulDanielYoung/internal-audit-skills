---
name: control-statements
description: Guidance for concise control titles and intended-design descriptions. Use when drafting or reviewing control statements, either directly for the user or within another skill's workflow.
---

A control is any action taken by management, the board, and other parties to manage risk and increase the likelihood that established goals are achieved. Write or review its **title** and **description**, returning wording to the auditor or calling skill.

## Starting pattern and completeness

The **title** is a short noun phrase naming the action and its object. It is unique within the process and matches the description’s boundaries. Include frequency or system when needed to distinguish the control from others in the process.

A useful starting point for the **description** is:

> [Role or automated system] [control action and scope] [frequency or trigger], using [relevant information, system, or configured rule], to [specific control purpose]. [Applicable criteria, exception follow-up, and supported records or outputs].

Adapt the wording to the context. Write one present-tense paragraph, roughly one to three sentences, stating the supported intended design. A description is complete when a reader can point to:

- **Performer or automated system:** which roles or systems perform the control. Name people by role and distinguish the accountable owner from the performer where relevant.
- **Action and scope:** the observable activity or mechanism and the population or other scope it covers.
- **Frequency or timing:** how often the activity occurs, what triggers it, or when it applies continuously, including relevant deadlines.
- **Information or system:** the relevant information, systems, or configurations used, where applicable.
- **Precision:** the operating rule or criteria that make the mechanism specific, such as the comparison performed, authorization condition, configured restriction, or recovery action. Include relevant granularity and supported thresholds; qualitative criteria may be sufficient.
- **Exception handling:** how applicable exceptions are resolved or escalated, by whom, and within any supported time limit.
- **Purpose:** the specific risk or undesired outcome addressed, or objective supported, through prevention, detection, correction, or recovery as applicable. Make the purpose understandable without consulting a linked risk statement and accurate wherever the shared control appears.

Include supported records or outputs where they explain the activity or how its performance is recorded. Distinguish inapplicable elements from material unknowns, and mark the latter as gaps.

## Sources and gaps

Base descriptions on supported intended design and distinguish documented design, reported practice, and direct observation. Preserve differences between sources with their attribution.

Mark missing facts with descriptive bracketed gaps. When revising supplied wording, retain its source references, visible information gaps, and distinctions between documented, reported, and observed practice. When drafting directly for the user, identify the material or attributed statements used. When another skill requests the wording, return this supporting information with the draft for inclusion in its workpaper.

## Control boundaries

Describe one coherent control mechanism per statement, with a clear purpose and scope. Keep connected steps together when they explain how the control works, including applicable review, investigation, resolution, and sign-off. Different roles, actions, or frequencies alone do not establish separate controls. When wording combines distinct controls, explain the distinction and propose separate statements.

When reviewing multiple statements, compare their mechanisms and scope for duplicated coverage. Clarify shared activities and recommend combining statements that describe the same control.

## Faults

When reviewing control statements, check for the following problems and apply the corresponding guidance.

- **A title that names an owner, department, or system rather than the control activity.** Name the action and object with a short, unique noun phrase.
- **A description that restates the title.** Explain the mechanism, its scope, performers, timing, applicable follow-up, and purpose.
- **A missing performer or ownership confused with performance.** Identify the performing role or automated system, marking a gap when unknown. Distinguish accountability from execution.
- **Vague timing where a frequency or trigger is known.** Replace "periodically", "as needed", or "regularly" with the supported frequency or trigger.
- **A vague action with no checkable activity.** Explain what "monitors", "oversees", or "ensures" means in observable terms supported by the sources.
- **Missing precision.** State the relevant operating rule or review criteria at the supported level of detail, marking material unknowns as gaps.
- **Missing applicable exception handling.** State how exceptions are resolved or escalated and by whom, with gaps for unknowns.
- **A missing, generic, or row-dependent purpose.** State the specific risk, undesired outcome, or objective addressed in wording that works across every linked risk and process.
- **A requirement or objective without a described control mechanism.** Describe the supported mechanism; "All payments must be approved" alone leaves its implementation unclear. For policy-based or directive controls, explain the supported activities for establishing, communicating, or enforcing the policy.
- **Several controls combined, or one control fragmented across descriptions.** Apply the coherent-mechanism boundary and recommend a split or combination where warranted.
- **Operating practice substituted for intended design.** Keep the supported design and intended frequency in the description, with contrary practice separately attributed and linked to the control.
- **Design or reported practice presented as observed operation.** Preserve the source attribution and what each source establishes.
- **Invented or guessed details.** Use supported intended-design facts and bracketed gaps for unknowns, including records or outputs.
- **An adequacy judgment or recommended improvement in the description.** Describe intended design and keep assessments and control improvements with their owning audit work.
- **Procedure or evidence-examination detail in the description.** Describe intended control activity; leave planned examination to `planned-procedures`.
- **A description that contradicts a supplied attribute field.** Flag the conflict and propose source-supported wording or a gap while leaving the attribute unchanged.

## Output

Check that the statements adhere to the guidance above, including every applicable completeness element, source attribution, and any separate handoff of contrary practice.

Return the drafted or revised titles and descriptions to the user or calling skill, with a brief summary of what was created or changed and an explanation of each substantive issue found.

Distinguish changes made from proposed changes, including any recommendations to combine or separate statements. Identify duplicates explicitly. Keep changes to the control list and IDs with the caller.

For each unresolved question or information gap, state which statement it affects and what clarification or source material is needed to resolve it.

If no changes are needed, confirm that the statements meet the guidance and leave sound wording unchanged.
