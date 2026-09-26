---
name: planned-procedures
description: "Write or review executable planned procedures for design assessment, implementation or walkthroughs, operating effectiveness, risk gaps, or auditor-selected direct examination of transactions or outcomes."
---

Return procedure wording to the auditor or calling skill for the auditor's agreed approach. This planning writing skill owns no artifacts or IDs and makes no approach decisions. Executing procedures and recording results, deviations found, findings, or conclusions belong to the stage performing the work.

## Common writing rules

Use numbered steps with one executable action per step:

> 1. [Technique and action] [supported evidence or object] for [attribute], evaluated against [applicable criterion and source, or a bracketed gap].

Each step names what to examine, what to do, and the observable criterion for evaluating it. Techniques include **inquire**, **observe**, **inspect**, **reperform**, and **recalculate**; the glossary or methodology may rename or extend them. Replace bare "review", "check", "ensure", or "verify" with the actual action. Phrase criteria as planned comparisons or questions to resolve, preserving open outcomes.

Read the workspace glossary and relevant methodology and organization context when present, using their role, system, report, and technique names; proceed silently when absent. Documented methodology governs the procedures; follow relevant longer sources it points to. Use `audit-context` for a needed term missing from an existing glossary, contested terminology, or persistent context needing update or clarification, passing the question and available evidence.

Use only local material and auditor-supplied facts. Mark unsupported criteria, evidence, reports, periods, or other necessary details in place, carrying gaps in the control description into the matching steps. Preserve the caller's gap markers, short inline retained-source references, and basis labels. Source retention and artifact sourcing rules stay with the calling stage skill. Use `shared-understanding` when ambiguity about the agreed approach, control, evidence, criteria, or applicable sampling could materially change the procedure.

## Completeness by purpose

Apply the checks for each purpose the caller requests. A procedure may combine purposes when the agreed approach calls for them; make each step's purpose clear.

### Design assessment

Compare the intended control activity with the risk and applicable criteria. Address how its role, timing, information, precision, and exception handling would prevent or detect the risk, identifying unsupported design details as gaps. Draft assessment actions and evaluation criteria; leave adequacy conclusions for execution.

### Implementation and walkthroughs

Trace the described activity through its performer, systems, handoffs, and exception handling using a supported instance or `[walkthrough instance not identified]`. Include examination of available evidence to establish how the activity is implemented and compare it with intended design. Where contrary practice has been retained, reference it by Control ID and plan examination of the departure. Inquiry or one traced instance does not establish operation throughout a period.

### Operating effectiveness

State the population and its source, period, sampling approach and size (or full-population coverage), and what counts as a deviation from the control requirement. Cover every control-description element or explain its omission: performing role, action and object, timing against intended frequency, information and precision, and exception follow-up.

When the control relies on system-generated information, include completeness and accuracy checks; mark an unidentified report or extract as a gap. If only inquiry or observation is available, flag the evidence limitation and propose locally supported corroboration, with missing evidence left visible for the auditor's decision.

For automated controls, note that reliance depends on general IT controls tested elsewhere; selection and design of those tests stay with the caller. A single-instance or baseline approach requires a methodology basis; otherwise leave the sampling basis as a gap.

### Risk gaps

For a risk without an identified control, draft steps to confirm the gap and assess the risk against supplied criteria: inquire of a supported responsible role, inspect relevant retained material, and identify what evidence would establish whether a control exists or what exposure remains. Mark unknown roles, evidence, and criteria as gaps. Associate these procedures with the Risk ID, leaving the Control ID and control description empty. An unidentified control supports assessment work, not an invented control or evidence trail.

### Direct examination

When the auditor's agreed approach requires examining transactions or outcomes directly, name the population or objects, relevant period, examination action, and applicable transaction or outcome criteria. Use sampling rules below when selecting a sample; for a full-population examination, state its coverage and source. Address completeness and accuracy of data used and define departures against the examination criteria, without recasting them as control failures.

## Sampling and evaluation bases

Apply population, period, and selection detail when the planned work depends on them. Design and gap assessments need no routine sample header or control-failure definition. For sampled work, record the auditor-supplied approach and size; otherwise apply relevant documented methodology, including a frequency-to-sample-size table when applicable and frequency is known. Attribute each basis and leave unsupported details as bracketed gaps; there is no default sample-size table. Combined sampling across controls remains an auditor or fieldwork strategy decision.

A deviation definition describes a departure from the applicable requirement, not a tolerable rate or effectiveness conclusion. Any tolerable rate or conclusion rule must come from methodology or the auditor.

## Shared controls and review output

Keep one risk-neutral set of control procedures per Control ID, identical wherever that shared control appears. Keep additional risk-specific assessment linked to the Risk ID; that assessment alone is no reason to split a control. Refer genuinely different control activities to `control-statements` for a split recommendation, leaving control lists and IDs with the caller.

For each procedure, check the common writing rules and every applicable purpose's completeness checks, sampling and evaluation bases, and consistency with supplied control attributes. Flag conflicts without changing attributes; resolve material ambiguity through `shared-understanding`. For several controls, refer identical procedures under different Control IDs to `control-statements`' duplicate check.

Report unmet requirements and evidence limitations, and propose revised wording for affected procedures. Preserve sound wording unchanged. Return planned actions and criteria only, with gaps and source references intact; leave splits, merges, and approach decisions to the caller and auditor.
