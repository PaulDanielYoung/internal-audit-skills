---
name: planning-memo
description: Write or update an engagement planning memo, set engagement objectives or scope, decide exclusions, define criteria, or set the engagement's team, budget, or timeline.
---

# Planning Memo

 Set the engagement's direction: what it will conclude on, which processes and risks it covers and why, the criteria it will be judged against, how the work will be approached, and the resources it needs. The memo is the internal record of these planning decisions. It builds on the survey and risk assessment without changing them, and leaves detailed procedures to the work program.

## File Structure

```text
/
└── engagements/
    └── <year>/
        └── <name>/
            └── planning/
                └── planning-memo.md
```

Create `planning/planning-memo.md` using the structure in [MEMO-FORMAT.md](MEMO-FORMAT.md). If the file already exists, update it in place.

## 1. Establish the starting point

Start from the assessment and its readiness report, and the survey. Inspect prior findings and assurance coverage, the engagement record, and any organization template or earlier memo before asking for more. Prior workpapers can inform structure and labelled prior content without establishing current decisions.

Establish whether the engagement provides **assurance** or **advisory** services from the engagement record or methodology; otherwise ask the auditor once and record the answer. Later steps note where advisory engagements differ.

Cite every factual statement and scoping consideration to its source, with its location and known date or version, or give an explicit basis such as a dated auditor statement. Carry upstream basis labels with their content. General context may appear only as a labelled note, never as an inferred fact about this activity. Minor gaps get bracketed markers in place and Information gaps entries.

Without an assessment, recommend `risk-assessment`. If the auditor declines, scope at process level only and mark the risk table "pending the risk assessment", leaving risk and Objective ID links pending. Refer a missing or incomplete process list to `preliminary-survey`; this skill creates no processes or IDs. Pause the whole memo only when neither processes nor the audit objective statement can be established; otherwise draft the supported portions.

## 2. Present the scope judgement point

Carry the assessment's active risks into a scoping table in its ranked order, citing the assessment version. Cite Risk IDs without repeating Risk Descriptions. Consider prior findings, other assurance coverage, budget pressure, and prior scope decisions where supported. Account for every process by Process ID the same way, including processes with no risks. Present the period under examination, entities and locations, and systems for the auditor's scope decision, keeping unknown boundaries visible. Present no proposed In/Out decisions.

Ask the auditor for decisions and record their reasons and dates. Leave undecided entries blank; mark missing decision details as gaps rather than supplying them. Excluding a process excludes only risks linked solely to that process: list them under the exclusion and record the process decision as their basis, with its reason and date. Shared risks keep their own decision, even when one linked process is Out. Resolve contradictory risk/process decisions with the auditor rather than silently altering either. Every exclusion, including an excluded area outside the risk list, needs a reason.

Classify each exclusion's basis as the auditor's judgement or a **scope limitation**: a condition imposed on the work, such as restricted access to people, data, systems, or facilities, insufficient resources, or a stakeholder's request to include, exclude, or shorten work. For each limitation, record its discussion with management and its resolution, or that escalation by the chief audit executive to the board is pending.

## 3. Agree objectives, criteria, and applicability

Draft a short numbered list of what the engagement will conclude on for the auditor to agree. Distinguish these engagement objectives from the activity objectives in the assessment and the audit objective statement. Include goals mandated by laws or regulations recorded in the survey. Each objective links the activity Objective IDs and in-scope Risk IDs it covers. Use plain list numbers, not stable IDs; preserve upstream IDs without allocating or reusing them. Record the auditor's agreement with date and stated reason, leaving unresolved wording visible. Check that every in-scope risk is covered by at least one agreed engagement objective. For advisory engagements, record the objectives and scope as agreed with the management that requested the service.

For each engagement objective, consider criteria in this order: management's own criteria (policies, procedures, performance measures and targets, and risk tolerance), external obligations (laws, regulations, and contracts), then authoritative frameworks, drawing on the survey's candidate evaluation criteria. Present sourced **adequacy** considerations for each: relevance, alignment with the organization's and the activity's objectives, and whether they support reliable comparison. Record the auditor's judgement. Use management's criteria where adequate. Where they are inadequate or absent, label replacement criteria as auditor-developed and record that they need discussion with management, or with senior management or the board. For advisory engagements, record whether formal criteria are needed, as agreed with the requesting stakeholders.

Use available local framework documents only. A missing reference or unknown edition is a gap; dependent criteria and applicability decisions stay open until the source and its governing version are established.

Take the topical requirements list from methodology, with a source for every requirement. If methodology is silent, ask the auditor once for the list. Preserve that answer or pending question in the memo so updates do not repeat the intake. When the auditor confirms no list applies or declines to provide one, state that basis in one line; an unanswered question remains a gap. Embed no catalog.

For each listed requirement, present sourced considerations from the survey and in-scope risks, without proposing applicability. Record the auditor's decision and date: covered here (link objectives and scope), covered elsewhere (identify the engagement or source of coverage), or excluded with rationale. Keep unresolved decisions and missing references visible; assess whether each could change scope or objectives.

## 4. Develop the approach and resources

Describe the summary approach per engagement objective: techniques, any reliance on other assurance or prior work, and any planned use of `exploratory-data-analysis`. For planned reliance on another provider's work, record the basis for its competence, objectivity, and due care, or list that evaluation as outstanding.

Take team names, roles and supervisor, total budget and phase hours, and milestone dates only from the auditor, the engagement record, methodology defaults, or a labelled prior memo. Cite each basis; leave missing values as gaps without inventing estimates. Check phase hours sum to the stated budget and milestone dates run in order, reporting inconsistencies for resolution without changing sourced values.

Present sourced **sufficiency** considerations: whether the team's skills, the budget, the timeline, and the available tools suit the engagement's nature and complexity, including specialist needs such as IT, data analytics, or subject expertise raised by in-scope risks or the survey. Record the auditor's judgement. When resources are insufficient, record the concern's escalation to the chief audit executive and whether it could reduce scope.

Record each team member's objectivity confirmation, or mark it outstanding, noting known threats such as recent work in the activity. List methodology's required declarations as outstanding with their source rather than drafting them. Include materiality and the audit risk model only when methodology requires them, presenting sourced considerations for the auditor's judgement with no proposed values. Record the auditor's decision, date, and stated reason.

## 5. Report readiness for the RCM

The memo is ready for `risk-and-control-matrix` when:

- Every engagement objective is agreed.
- Every active risk and process has a current In/Out decision, with reasons for exclusions.
- Every in-scope risk is covered by an agreed engagement objective.
- Every engagement objective has criteria with an adequacy judgement, an agreed advisory basis for none, or a named gap.
- No unresolved scope limitation affects an engagement objective.
- No open gap would change scope or objectives.

A pending assessment or scoping re-decision prevents readiness. Team, budget, timeline, sufficiency, and objectivity items are reported as outstanding without blocking the RCM; any associated unresolved scope or objective decision still blocks. Record each gap's effect in Information gaps, with the returned RQ ID or the question put to the auditor.

## Updating the memo

On updates, compare current upstream processes, risks, ratings, objective links, and sources with the versions supporting the memo. Mark affected scoping rows "needs re-decision", retaining the old decision, reason, and date visibly as history. Keep unaffected current decisions. Add new risks undecided; show retired risks with replacement IDs or "no replacement", preserving history. Recheck affected engagement objectives, criteria, and coverage with the auditor; an old decision awaiting re-decision does not satisfy readiness.
Memo changes flag the RCM for revision, identifying affected scope, objectives, criteria, and other references. Search existing engagement workpapers for affected Process IDs, Risk IDs, and objective references; name pending handoffs when the downstream workpaper does not exist. Edit only this memo. A risk without an identified control remains available for planned assessment in the RCM under the agreed approach; the missing control alone does not require a new scope decision.

Offer an earlier engagement's memo as a reference and cite it in place, leaving it unchanged. Its approach, team, budget, and dates may inform labelled prior content. Its scope decisions appear only as sourced considerations, with current decisions left undecided until the auditor decides.

## Done

Reply with the output path, readiness against each criterion, undecided items, outstanding sufficiency and objectivity items, remaining gaps and RQ IDs, outstanding methodology requirements, and downstream flags. Recommend `risk-and-control-matrix`, naming the blockers when not ready.
