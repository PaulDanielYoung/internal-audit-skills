---
name: planning-memo
description: Write or update an engagement planning memo, set engagement objectives or scope, decide exclusions, define criteria, or set the engagement's team, budget, or timeline.
---

# Planning Memo

Own the internal workpaper at `planning/planning-memo.md` in the selected engagement: engagement objectives, process and risk scope, criteria, summary approach, team, budget, and timeline. Draft nothing for management. Preserve the survey's process list and the assessment's risks, wording, ratings, and IDs; flag needed changes to their owning skills. Detailed Planned Procedures and sample sizes belong in the preliminary RCM maintained by `risk-and-control-matrix`, using `planned-procedures` for wording.

## Establish the basis

Follow the workspace instructions for engagement selection, read its `ENGAGEMENT.md`, and state the selected engagement and output path. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Use `audit-terminology` when a term's meaning needs agreement or consistency across engagements.

Documented methodology overrides defaults. For structure, use a supplied organization template, then methodology, then relevant prior workpapers, then the defaults below. Read longer retained sources the methodology points to. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names, paths, and ID prefixes fixed. State the methodology or default basis in the workpaper. Resolve unclear or conflicting methodology with the auditor through `shared-understanding`. List requirements outside this skill's remit as outstanding with their methodology source.

Inspect available material before asking for more. Gather only what the memo needs: the survey, assessment, recorded framework, prior findings and assurance coverage, assignment facts, and any organization template or earlier memo. Accept equivalent auditor-supplied documents, preserving originals as described below. Quote the assignment's audit objective statement verbatim and leave the engagement record unchanged.

Use `shared-understanding` for material ambiguity that could change scope or objectives, pausing only the affected portion; ask directly if unavailable. Minor gaps get descriptive bracketed markers in place and entries in Information gaps. Use available local framework documents only. A missing reference or unknown edition/date is a gap for the auditor; dependent criteria and applicability decisions stay open until the source and its governing version are established. Use plain concept terms and attribute rules to documented methodology without quoting, citing, or numbering IIA or ISACA text. Describe the activity without classifying the engagement by subject type.

### Sources and provenance

Read source files in place and leave originals unchanged. The auditor places client-provided files in `document-requests/received/`; cite those files, other available local references, and upstream workpapers directly. Record known source dates or versions and relevant locations; leave unknown provenance explicit. Settle conflicting versions with the auditor. When adopting an external draft, create the working copy at this skill's output path only after a separate unchanged original is available.

Every factual statement and scoping consideration carries an inline citation to the retained copy and relevant location, or an explicit basis such as a dated auditor statement. Cite upstream workpapers and their underlying sources when carrying content. `ORGANIZATION.md` also counts as a source. Label meeting notes and prior-content bases. General context may appear only as a labelled note, never as an inferred fact about this activity.

### Entry without an assessment or with a prior memo

Accept an equivalent assessment supplied by the auditor. Without one, recommend `risk-assessment`; if declined, scope at process level only and mark the risk table “pending the risk assessment”. Use established Process IDs and leave unavailable risk and activity Objective ID links pending. Refer a missing or incomplete process list to `preliminary-survey`; this skill creates no processes or IDs. Pause the whole memo through `shared-understanding` only when neither processes nor the assignment's audit objective statement can be established; otherwise draft the supported portions. An absent request list or notification-sent status is no prerequisite.

Offer an earlier engagement's memo as a reference and cite it in place. Write the current engagement's memo separately, leaving the earlier memo unchanged. Its approach, team, budget, and dates may inform labelled prior content. Its scope decisions appear only as sourced considerations, with current decisions left undecided until the auditor decides.

## Present the scope judgement point

Carry the assessment's active risks into a scoping table in its ranked order, citing the assessment version. Include Risk ID, Risk Title, Process IDs, Band, sourced scoping considerations, In/Out, auditor's reason, and decision date. Cite Risk IDs without repeating Risk Descriptions. Consider prior findings, other assurance coverage, budget pressure, and prior scope decisions where supported. Present no proposed In/Out decisions.

Alongside that table, account for every process by Process ID with sourced considerations and its own In/Out, reason, and date, including processes with no risks. Present the period under examination, entities and locations, and systems for the auditor's scope decision, keeping unknown boundaries visible.

Ask the auditor for decisions and record their reasons and dates. Leave undecided entries blank; mark missing decision details as gaps rather than supplying them. Excluding a process excludes only risks linked solely to that process: list them under the exclusion and record the process decision as their basis, with its reason and date. Shared risks keep their own decision, even when one linked process is Out. Resolve contradictory risk/process decisions with the auditor rather than silently altering either. Every exclusion, including an excluded area outside the risk list, needs a reason. List risk exclusions in the assessment's ranked order, followed by other exclusions and their affected references; this preserves priority when methodology uses different band names.

## Agree objectives, criteria, and applicability

Draft a short numbered list of what the engagement will conclude on for the auditor to agree. Distinguish these engagement objectives from the activity objectives in the assessment and the assignment's audit objective statement. Each links the activity Objective IDs and in-scope Risk IDs it covers. Use plain list numbers, not stable IDs; preserve upstream IDs without allocating or reusing them. Record the auditor's agreement with date and stated reason, leaving unresolved wording visible. Check that every in-scope risk is covered by at least one agreed engagement objective.

For each engagement objective, select criteria from the framework recorded in the survey or equivalent supplied material, citing retained sources and locations. Where authoritative criteria are absent, label auditor-developed criteria and obtain the auditor's agreement on suitability; keep missing criteria or agreement as named gaps.

Take the topical requirements list from methodology, with a source for every requirement. If methodology is silent, ask the auditor once for the list. Preserve that answer or pending question in the memo so updates do not repeat the intake. When the auditor confirms no list applies or declines to provide one, state that basis in one line; an unanswered question remains a gap. Embed no catalog.

For each listed requirement, present sourced considerations from the survey's factual topic links and in-scope risks, without proposing applicability. Record the auditor's decision and date: covered here (link objectives and scope), covered elsewhere (identify the engagement or source of coverage), or excluded with rationale. Keep unresolved decisions and missing references visible; assess whether each could change scope or objectives.

## Develop the approach and resource plan

Describe the summary approach per engagement objective: techniques, any reliance on other assurance or prior work, and any planned use of `exploratory-data-analysis`. Keep detailed procedures and sample sizes for the RCM.

Take team names, roles and supervisor, total budget and phase hours, and milestone dates only from the auditor, the engagement record, methodology defaults, or a labelled prior memo. Cite each basis; leave missing values as gaps without inventing estimates. Check phase hours sum to the stated budget and milestone dates run in order, reporting inconsistencies for resolution without changing sourced values.

Include independence or conflict declarations only when methodology requires them; list the required declaration and its source as outstanding rather than drafting it. Include materiality and the audit risk model only when methodology requires them, presenting sourced considerations for the auditor's judgement with no proposed values. Record the auditor's decision, date, and stated reason.

## Reconcile changes

On updates, compare current upstream processes, risks, ratings, objective links, and sources with the versions supporting the memo. Mark affected scoping rows “needs re-decision”, retaining the old decision, reason, and date visibly as history. Keep unaffected current decisions. Add new risks undecided; show retired risks with replacement IDs or “no replacement”, preserving history. Recheck affected engagement objectives, criteria, and coverage with the auditor; an old decision awaiting re-decision does not satisfy readiness.

Memo changes flag the RCM for revision, identifying affected scope, objectives, criteria, and other references. Search existing engagement artifacts for affected Process IDs, Risk IDs, and objective references; name pending handoffs when the downstream artifact does not exist. Refresh only this memo. A risk without an identified control remains available for planned assessment in the RCM under the agreed approach. Return material changes to engagement objectives or process/risk scope to the auditor here; the missing control alone does not require a new scope decision.

## Route information needs and responses

Record missing information and its effect on the work in Information gaps. Invoke `document-request-list` when missing material warrants a document request, relevant information or received files may change an existing request, or the auditor asks to create or update the list. Pass the selected engagement, the material needed and why, known period/version, request owner and due date, relevant files, and any existing request ID or auditor instruction. Let that skill manage approval of new requests and maintain the list; record returned RQ IDs beside the corresponding gaps. Questions requiring the auditor's judgement stay in this workpaper.

Cite received material when updating the workpaper and assess whether it resolves each affected gap. A request's status alone does not establish that the workpaper's information need is satisfied.

If `document-request-list` is unavailable, continue supported work, keep gaps visible, and return proposed requests or status changes as a handoff, explicitly stating that the list was not updated. Request table edits belong to that skill.

## Assemble the memo and report readiness

Use these default sections in order, retaining missing content with bracketed gaps:

1. **Engagement context:** unchanged audit objective statement, links to the survey and assessment, and methodology or default basis.
2. **Engagement objectives:** numbered wording, linked Objective IDs and Risk IDs, and auditor agreement.
3. **Scope:** period, entities and locations, systems, process decisions, and ranked risk scoping table.
4. **Exclusions:** reasons and affected references, with risk exclusions in the assessment's ranked order.
5. **Criteria:** per engagement objective, with sources, auditor-developed labels and agreement, or gaps.
6. **Topical requirements applicability:** sourced list, considerations, and auditor decisions, or the one-line basis for no list.
7. **Approach:** summary per engagement objective.
8. **Team:** sourced names, roles, and supervisor.
9. **Budget:** sourced total and hours by phase, with any inconsistency.
10. **Timeline:** sourced milestones, with any inconsistent ordering.
11. **Information gaps:** affected section, whether the gap could change scope or objectives, and returned RQ ID or question put to the auditor. Include outstanding methodology requirements and handoffs.
12. **Sources:** retained copies used and other stated bases, preserving provenance and prior-content labels.

Save the memo in Markdown. It is ready for `risk-and-control-matrix` when every engagement objective is agreed, every active risk and process has a current In/Out decision with reasons for exclusions, every in-scope risk is covered by an agreed objective, every objective has criteria or a named gap, and no open gap would change scope or objectives. A pending assessment or scoping re-decision prevents readiness. Team, budget, and timeline gaps or inconsistencies are listed without blocking the RCM; any associated unresolved scope or objective decision still blocks. Resolve scope-changing or objective-changing gaps through `shared-understanding`, pausing the affected portion meanwhile.

In the reply, give the output path, stated readiness against each criterion, undecided items, remaining gaps and RQ references, outstanding methodology requirements, and downstream flags. Recommend `risk-and-control-matrix`, with blockers clear when not ready. Report readiness separately from the auditor decisions and document-request approvals required above; add no final approval gate and send no communications.
