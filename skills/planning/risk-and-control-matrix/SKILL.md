---
name: risk-and-control-matrix
description: Build or update an engagement's preliminary RCM or work program, document controls for engagement risks, plan procedures, or re-render and open the RCM. Single-control wording belongs to control-statements; standalone procedure wording belongs to planned-procedures.
---

# Risk and Control Matrix

Own the preliminary RCM and stable Control IDs for the selected engagement. Keep the authoritative work program in `planning/risk-and-control-matrix.md` and generate `planning/risk-and-control-matrix.html` from it. The planning memo owns process/risk scope; the survey and assessment own their respective fields and IDs. This skill plans work; execution, results, and final findings belong to later phases.

## Establish the basis

Follow the workspace instructions for engagement selection, read its `ENGAGEMENT.md`, and state the selected engagement and output paths. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Use `audit-terminology` when a term's meaning needs agreement or consistency across engagements.

Documented methodology governs. For structure, prefer a supplied organization template, then methodology, then relevant prior workpapers, then the defaults here, retaining the single-table rendering contract. Read longer retained sources the methodology points to. State the methodology or default basis in the RCM; resolve conflicts with the auditor through `shared-understanding`. Requirements outside this skill's remit remain outstanding with their methodology source. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names, paths, and ID prefixes fixed. Use plain concept terms and attribute rules to methodology without quoting, citing, or numbering IIA or ISACA text. Describe the activity without a subject-type classification.

Inspect available material before asking for more: the survey, assessment, memo, existing RCM, applicable local policies and procedures, attributed management/auditor accounts, and relevant prior work. Accept equivalent auditor-supplied documents. When adopting an external current-engagement RCM, create the working copy at the RCM path only after a separate unchanged original is available. Use an earlier engagement's RCM as a sourced reference, preserving that engagement's artifact and establishing current support for each carried control.

Read source files in place and leave originals unchanged. The auditor places client-provided files in `document-requests/received/`; cite those files, other available local references, and upstream workpapers directly. Record known source dates or versions and relevant locations; leave unknown provenance explicit. Settle conflicting versions with the auditor. Cite factual statements inline and record relevant verbal facts as dated, attributed statements in the workpaper. General knowledge supplies only labelled context, never facts about this activity.

Use `shared-understanding` for ambiguity that could materially change planned work, or ask directly if unavailable; pause only the affected portion. Mark minor unknowns with descriptive bracketed gaps in place and list them in Information gaps.

For a render/open-only request, use the existing Markdown and proceed to rendering. Report any identified upstream changes as pending refresh, keeping the saved work program unchanged. Creating or updating the work program follows the content steps below.

## Establish the included risks

Read [RENDERER.md](RENDERER.md) before creating, updating, or rendering the matrix. It owns the 18-column contract, supported Markdown, missing-control encoding, classification defaults, methodology directives, and validation rules. Keep exactly one table with one row per process–risk–control combination; use surrounding prose for all supporting sections. Markdown is authoritative; maintain no JSON record, separate entity registers, or browser edits.

Include the memo's in-scope risks with their applicable in-scope processes. Resolve contradictory or undecided process/risk scope with the auditor through `planning-memo`, retaining a visible gap for the affected portion. Copy Process ID, Title, and Description from the survey, or the assessment's provisional process list when no survey exists, and all risk fields from the assessment without rewording or rating them. Keep provisional process status visible until the survey adopts the list. Record source links and identifiable versions/dates for each upstream workpaper used above the matrix. Route new risks and risk wording/rating problems to `risk-assessment`, and process problems to `preliminary-survey`; those owners settle changes before the RCM inherits them.

Without a memo, recommend `planning-memo`; if declined, draft for all assessed risks with process/risk scope pending. Without an assessment or equivalent, recommend `risk-assessment` and retain established process material and information needs in prose while risk rows await their owner. Pause the whole artifact only when neither a process nor risk list can be established; otherwise save supported portions. If no valid process–risk row can be formed, explain that HTML generation awaits those IDs rather than inventing a row. An absent request list or notification-sent status is no prerequisite.

## Describe intended controls and plan the work

For each included risk, identify supported intended control activities from applicable local policy/procedure. Where policy is silent, use supported procedures or an attributed management/auditor account with its basis clear. A requirement alone does not establish a control activity. Use `control-statements` to draft and review Control Title and Description, preserving short inline links to retained sources in the description cell. Populate Owner, intended Frequency, Type, and Nature from supported material, using the contract's lists unless methodology/glossary replaces them; leave unsupported attributes visibly unknown.

Use one sourced intended-design pattern for every control. Keep known contrary practice in separately attributed prose below the matrix, linked by Control ID and retained source for walkthroughs/fieldwork. Preserve the intended baseline and treat the departure as material for examination, not an automatic final finding. Controls have no selection or confirmation-status workflow: no control-level scope field, decisions, history, procedure gate, or expected/unconfirmed/prior-control statuses or prefixes.

Allocate `C-01`, `C-02`, and so on above the highest Control ID in the current engagement's RCM and retirement history. Keep one ID for a shared activity across risks and processes; repeat every field and its Planned Procedures identically. Ask `control-statements` to review duplicates and combined activities. Settle genuine splits/merges with the auditor, allocate new IDs, and retire old IDs with replacements or “no replacement” in history/Flags. Never renumber or reuse IDs. A risk-specific assessment alone does not split a control.

When a risk has no identified control, use the contract's `Control not yet identified` row with no invented Control ID, description, or attributes. Keep gap-assessment Planned Procedures attached to that Risk ID, identical wherever its missing-control row repeats. Use the same row alongside identified controls when a distinct unresolved control gap needs investigation. Missing information is not an established design deficiency. Where evidence establishes the absence of a necessary control, plan a supported response to the engagement objective; there is no operating effectiveness of an absent control to test.

Use `planned-procedures` to draft and review the work program against the memo's objectives, criteria, and agreed approach: design assessment, implementation/walkthrough, operating effectiveness, risk-gap assessment, and auditor-selected direct examination of transactions or outcomes as needed. Supply control descriptions and attributes, risk context, period, retained evidence/criteria, and applicable methodology. Apply that skill's sampling, information-reliability, automated-control, and deviation requirements where relevant; preserve unknown bases as gaps. One reviewed procedure set belongs to each Control ID. Risk-specific gap work belongs to its Risk ID. Complete the work program against the engagement objectives, without requiring operating-effectiveness testing on every control or treating a gap response as a scope change.

Keep risk-specific direct-examination procedures in a numbered prose section below the matrix, linked to the Risk ID and memo objective they address. This gives them a home without changing shared control procedures or implying a missing control. Include that section when checking work-program coverage and readiness.

If a writing skill is unavailable, preserve supported draft content, name the review handoff and affected IDs, and leave the required review outstanding in readiness.

## Refresh and preserve history

When creating or updating the work program, compare the upstream snapshots with current survey, assessment, memo, and source versions. Refresh inherited fields consistently across all occurrences, and identify affected controls and procedures for review. Add newly included risks with missing-control rows until controls are supported. Material unresolved changes block readiness for the affected portion; they do not create a control-selection decision.

Remove combinations no longer included by current upstream scope from the active matrix, preserving the earlier links and planned work in dated prose history. Preserve retired Process, Risk, and Control IDs with replacements or “no replacement”; use plain ID mentions for IDs absent from the active table, as the renderer requires. A control shared with remaining rows keeps its ID and identical procedure set. Keep contrary-practice/source links available for later phases.

Search engagement artifacts across phases for affected IDs and references. Record Flags naming affected artifacts/sections or pending handoffs, and refresh only the RCM. Return changes to upstream-owned wording, ratings, objectives, or scope to their owners and the auditor. Keep materially unresolved review work visible until settled.

## Route information needs and responses

Record missing information and its effect on the work in Information gaps. Invoke `document-request-list` when missing material warrants a document request, relevant information or received files may change an existing request, or the auditor asks to create or update the list. Pass the selected engagement, the material needed and why, known period/version, request owner and due date, relevant files, and any existing request ID or auditor instruction. Let that skill manage approval of new requests and maintain the list; record returned RQ IDs beside the corresponding gaps. Questions requiring the auditor's judgement stay in this workpaper.

Cite received material when updating the workpaper and assess whether it resolves each affected gap. A request's status alone does not establish that the workpaper's information need is satisfied.

If `document-request-list` is unavailable, continue supported work, keep gaps visible, and return proposed requests or status changes as a handoff, explicitly stating that the list was not updated. Request table edits belong to that skill.

## Render and report readiness

For content creation or updates, place engagement context, the unchanged audit objective statement, memo objectives/approach references, upstream snapshot versions, and methodology basis above the single table. Below it, retain any risk-specific direct-examination procedures, contrary practice, dated history, Information gaps with affected IDs and returned RQ IDs or auditor questions, Flags, and Sources. Use prose and lists, not supporting tables. Apply the contract's methodology directives when supported; if the renderer cannot represent the governing methodology, retain it unchanged and report the rendering limitation for resolution rather than alter upstream ratings to pass validation.

When a valid process–risk row exists, run the bundled script using its installed skill path and the engagement's absolute Markdown path:

```text
python "<skill-directory>/scripts/render_rcm.py" "<engagement-directory>/planning/risk-and-control-matrix.md"
```

It validates before writing HTML and opens the generated view. Use `--no-open` when browser opening is unwanted. During content updates, resolve validation failures in owned content and route upstream conflicts to their owners. For render/open-only requests, report validation failures and the required corrections. Failed validation leaves prior HTML unchanged, so identify it as stale and keep readiness pending. If only browser opening fails, report the saved HTML path separately. Inspect the resulting table and surrounding sections for preserved source links, visible gaps, consistent repeats, and usable numbered procedures. If no valid row exists, report HTML generation as pending and identify any earlier HTML as stale; for creation or updates, save the supported Markdown.

Report ready for walkthroughs only for portions where every included control has a sourced description and usable reviewed procedures, every risk without an identified control has gap-assessment procedures, any agreed direct-examination work has usable reviewed procedures, shared entries are consistent, Markdown validates and HTML has been regenerated, and no unresolved information would materially change planned work. Identify portions not ready and the blocking gaps/reviews, including pending upstream scope or objectives. A usable investigation plan can proceed with a suspected gap visible; a material unresolved planning basis cannot. Rendering alone establishes no new planning readiness. List outstanding methodology requirements separately.

In the reply, give the Markdown path and the HTML path if generated, readiness against these criteria, affected portions, remaining gaps/RQ references, and Flags. Recommend walkthroughs with limitations clear: planning Markdown/HTML stay in place, and walkthroughs start their own working copy carrying every Process, Risk, and Control ID. Report readiness separately from the auditor decisions and document-request approvals required above; add no final approval gate.
