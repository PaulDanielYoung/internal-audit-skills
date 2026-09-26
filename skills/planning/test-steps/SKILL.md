---
name: test-steps
description: "Write clear, executable test steps for a control: what to examine, what to do, and what counts as a satisfactory result, with population, period, and sampling. Use when writing, reviewing, improving, or diagnosing planned control tests."
---

Write or review planned **operating effectiveness** procedures for one control or several, returning wording to the auditor or calling skill. This planning writing skill owns no artifact, IDs, In Scope flag, or control selection. Performing tests and recording results, deviations found, or conclusions belong to fieldwork.

## Starting pattern and completeness

A useful starting point is:

> **Population:** [items and source] · **Period:** [dates] · **Sample:** [approach and size, or a bracketed gap]
>
> 1. [Technique] [evidence or object] for [attribute], **satisfactory when** [criterion].
> 2. …
>
> **Deviation:** [what counts as a failure of the control].

Use numbered steps, one executable action per step, each naming its technique, evidence, attribute, and satisfactory-when criterion. Techniques are **inquire**, **observe**, **inspect**, **reperform**, and **recalculate**; the glossary or methodology may rename or extend them. The deviation definition describes failure, not a tolerable rate or an effectiveness conclusion. Any tolerable rate or rule for drawing a conclusion comes only from methodology or the auditor; keep the output as a plan.

The procedure is complete when every element of the control description is covered by a step or its omission is stated:

- **Who:** evidence that the specified role performed the control.
- **What:** evidence of the action on the stated object, linked to what the control prevents or detects.
- **When:** timing checked against the description and any supplied Frequency.
- **How:** the information or system used and reperformance of the comparison or threshold at the described precision.
- **Exceptions:** evidence of follow-up by the specified role.

Where the control relies on system-generated information, include a step addressing its completeness and accuracy. Mark an unidentified report or extract as a bracketed gap. For automated controls, add a one-line note that reliance depends on general IT controls tested elsewhere; selection and design of those tests stay with the caller.

## Shared context, sampling, and gaps

Read the workspace glossary, if present, for control, test, sample, deviation, and technique names. Read relevant methodology and organization context too, using their system and report names, and proceed silently when absent. Documented methodology governs the pattern and testing conventions; follow any relevant longer source it points to.

Use `audit-context` when a needed term is missing from an existing glossary, terminology is contested or unclear, or persistent methodology or organization context needs updating or clarification. Pass the specific question and available evidence.

Record the sampling approach and size supplied by the auditor. Otherwise, apply a methodology frequency-to-sample-size table when the control's frequency is known, labelling the size as coming from methodology. Leave any unsupported approach or size as a bracketed gap, such as `[sample size not yet determined]`; there is no default sample-size table. For automated controls, use a single-instance or baseline approach only when methodology provides it; otherwise leave the sample as a bracketed gap.

Call the Skill tool with `shared-understanding` when material ambiguity about the control, its status, evidence, population, or sampling could change the procedure. Use only local material and auditor-supplied facts. Mark unknown populations, periods, evidence, and reports in place, such as `[evidence of review not identified]`, rather than substituting generic evidence. Carry each gap in the control description into the matching step. Preserve the caller's gap markers, source links, and basis labels; source retention and artifact sourcing rules stay with the calling stage skill.

## Shared, expected, and missing controls

Keep one risk-neutral set of steps per Control ID, identical on every row of a shared control. A risk needing a different test suggests a control split: flag it for the caller rather than changing the control list or IDs. Combined sampling across controls is a strategy decision for the auditor or fieldwork.

Write steps for an expected control only when the auditor asks and the control is in scope. Open with **Planned for an expected control; confirm at walkthrough.** Use conditional wording and leave evidence as bracketed gaps. For a control not yet identified, write no procedure.

## Faults

Use these when reviewing, improving, or diagnosing. Each fault names what a sound procedure has instead.

1. **Unnumbered steps or several actions merged into one.** Number the steps and give each one an executable action.
2. **A missing technique or vague verb.** Name the technique and the action on an object, replacing bare "review", "check", "ensure", or "verify".
3. **Unnamed or invented evidence.** Name the supported object or evidence and mark unknowns as gaps.
4. **A missing satisfactory-when criterion.** Give each step its own observable criterion for the attribute tested.
5. **A missing deviation definition.** State what counts as failure of the control.
6. **A missing or guessed population, period, or sample.** Supply a supported header and mark unknown elements as gaps.
7. **A step unrelated to the control or an unexplained coverage gap.** Tie each step to a control element or required information-reliability check, and cover every description element or state its omission.
8. **Unaddressed completeness and accuracy of system-generated information.** Include a step for both when the control relies on a report or extract.
9. **Reliance only on inquiry or observation.** Flag the evidence limitation and propose corroboration supported by the available material, marking missing evidence as a gap. Leave the decision to the auditor and continue the review.
10. **Design, walkthrough, or substantive procedures mixed into the test.** Keep the procedure focused on operating effectiveness; route design and walkthrough work to walkthroughs and leave substantive or data-analytic work outside this skill.
11. **Results, conclusions, or deviations found recorded as if testing occurred.** Return planned actions and criteria, leaving execution and its record to fieldwork.
12. **An unsourced sample size or tolerable rate.** Attribute the value to the auditor or applicable methodology; replace an unsupported value with a gap.
13. **Risk-specific steps for a shared control.** Use one risk-neutral procedure per Control ID and recommend a split when the tests differ by risk.
14. **An expected control treated as confirmed.** Apply the expected-control conditions and opening marker, conditional wording, and evidence gaps.
15. **A procedure contradicting the control description, Frequency, or Nature.** Flag the conflict and propose supported wording or gaps, leaving supplied attributes unchanged; resolve material ambiguity through `shared-understanding`.

## Review output

Check the header, every step, deviation definition, every completeness element, sampling basis, control status, and the faults. For automated controls, also check the general IT controls note and the methodology basis for any single-instance or baseline approach. For several controls, flag the same procedure under two Control IDs as a possible duplicate and refer it to `control-statements`' duplicate check.

Name each fault found using the names above, explain any other unmet requirement, and propose revised procedures for affected wording. Preserve gap markers, source links, and basis labels in the revisions. Keep splits or merges as recommendations for the caller. Confirm sound procedures and leave them unchanged, without rewriting for style.
