---
name: risk-and-control-matrix
description: Build or update an engagement's preliminary RCM or work program, document controls for engagement risks, plan procedures, or re-render and open the RCM. Single-control wording belongs to control-statements; standalone procedure wording belongs to planned-procedures.
---

# Risk and Control Matrix

Own the preliminary RCM and stable Control IDs for the selected engagement. Keep the authoritative work program in `planning/risk-and-control-matrix.md` and generate `planning/risk-and-control-matrix.html` from it. The planning memo owns process/risk scope; the survey and assessment own their respective fields and IDs. This skill plans work; execution, results, and final findings belong to later phases.

## Establish the basis

Follow the workspace instructions for engagement selection, read its `ENGAGEMENT.md`, and state the selected engagement and output paths. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Use `audit-terminology` for missing, ambiguous, or contested terms and settled definitions.

Documented methodology governs. For structure, prefer a supplied organization template, then methodology, then relevant prior workpapers, then the defaults here, retaining the single-table rendering contract. Read longer retained sources the methodology points to. State the methodology or default basis in the RCM; resolve conflicts with the auditor through `shared-understanding`. Requirements outside this skill's remit remain outstanding with their methodology source. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names, paths, and ID prefixes fixed. Use plain concept terms and attribute rules to methodology without quoting, citing, or numbering IIA or ISACA text. Describe the activity without a subject-type classification.

Inspect available material before asking for more: the survey, assessment, memo, existing RCM, applicable local policies and procedures, retained management/auditor accounts, and relevant prior work. Accept equivalent auditor-supplied documents. Have `engagement-sources` preserve an unchanged received copy of an external current-engagement RCM before adopting its working copy at the RCM path. Use an earlier engagement's RCM as a sourced reference, preserving that engagement's artifact and establishing current support for each carried control.

Delegate source retention and provenance updates to `engagement-sources`, passing supplied material and known original locations and receipt dates. Use its returned retained-source links. If unavailable, continue supported work from already-retained material and give a concrete handoff for outstanding retention or provenance updates; do not write sources or their index as a fallback. Settle conflicting versions with the auditor. Cite factual statements inline to retained material and locations, including upstream workpapers and their underlying sources. Have `engagement-sources` retain verbal accounts as dated, attributed notes. General knowledge supplies only labelled context, never facts about this activity.

Use `shared-understanding` for ambiguity that could materially change planned work, or ask directly if unavailable; pause only the affected portion. Mark minor unknowns with descriptive bracketed gaps in place and list them in Information gaps.

## Establish the included risks

Read [RENDERER.md](RENDERER.md) before creating, updating, or rendering the matrix. It owns the 18-column contract, supported Markdown, missing-control encoding, classification defaults, methodology directives, and validation rules. Keep exactly one table with one row per process–risk–control combination; use surrounding prose for all supporting sections. Markdown is authoritative; maintain no JSON record, separate entity registers, or browser edits.

Include the memo's in-scope risks with their applicable in-scope processes. Resolve contradictory or undecided process/risk scope with the auditor through `planning-memo`, retaining a visible gap for the affected portion. Copy Process ID, Title, and Description from the survey and all risk fields from the assessment without rewording or rating them. Record source links and identifiable versions/dates for the survey, assessment, and memo above the matrix. Route new risks and risk wording/rating problems to `risk-assessment`, and process problems to `preliminary-survey`; those owners settle changes before the RCM inherits them.

Without a memo, recommend `planning-memo`; if declined, draft for all assessed risks with process/risk scope pending. Without an assessment or equivalent, recommend `risk-assessment` and retain established process material and information needs in prose while risk rows await their owner. Pause the whole artifact only when neither a process nor risk list can be established; otherwise save supported portions. If no valid process–risk row can be formed, explain that HTML generation awaits those IDs rather than inventing a row. An absent request list or notification-sent status is no prerequisite.

## Describe intended controls and plan the work

For each included risk, identify supported intended control activities from applicable local policy/procedure. Where policy is silent, use supported procedures or an attributed management/auditor account with its basis clear. A requirement alone does not establish a control activity. Use `control-statements` to draft and review Control Title and Description, preserving short inline links to retained sources in the description cell. Populate Owner, intended Frequency, Type, and Nature from supported material, using the contract's lists unless methodology/glossary replaces them; leave unsupported attributes visibly unknown.

Use one sourced intended-design pattern for every control. Keep known contrary practice in separately attributed prose below the matrix, linked by Control ID and retained source for walkthroughs/fieldwork. Preserve the intended baseline and treat the departure as material for examination, not an automatic final finding. Controls have no selection or confirmation-status workflow: no control-level scope field, decisions, history, procedure gate, or expected/unconfirmed/prior-control statuses or prefixes.

Allocate `C-01`, `C-02`, and so on above the highest Control ID in the current engagement's RCM and retirement history. Keep one ID for a shared activity across risks and processes; repeat every field and its Planned Procedures identically. Ask `control-statements` to review duplicates and combined activities. Settle genuine splits/merges with the auditor, allocate new IDs, and retire old IDs with replacements or “no replacement” in history/Flags. Never renumber or reuse IDs. A risk-specific assessment alone does not split a control.

When a risk has no identified control, use the contract's `Control not yet identified` row with no invented Control ID, description, or attributes. Keep gap-assessment Planned Procedures attached to that Risk ID, identical wherever its missing-control row repeats. Use the same row alongside identified controls when a distinct unresolved control gap needs investigation. Missing information is not an established design deficiency. Where evidence establishes the absence of a necessary control, plan a supported response to the engagement objective; there is no operating effectiveness of an absent control to test.

Use `planned-procedures` to draft and review the work program against the memo's objectives, criteria, and agreed approach: design assessment, implementation/walkthrough, operating effectiveness, risk-gap assessment, and auditor-selected direct examination of transactions or outcomes as needed. Supply control descriptions and attributes, risk context, period, retained evidence/criteria, and applicable methodology. Apply that skill's sampling, information-reliability, automated-control, and deviation requirements where relevant; preserve unknown bases as gaps. One reviewed procedure set belongs to each Control ID. Risk-specific gap work belongs to its Risk ID. Complete the work program against the engagement objectives, without requiring operating-effectiveness testing on every control or treating a gap response as a scope change.

If a writing skill is unavailable, preserve supported draft content, name the review handoff and affected IDs, and leave the required review outstanding in readiness.

## Refresh and preserve history

On every invocation, compare the upstream snapshots with current survey, assessment, memo, and source versions, including when asked only to re-render/open. Refresh inherited fields consistently across all occurrences, and identify affected controls and procedures for review. Add newly included risks with missing-control rows until controls are supported. Material unresolved changes block readiness for the affected portion; they do not create a control-selection decision.

Remove combinations no longer included by current upstream scope from the active matrix, preserving the earlier links and planned work in dated prose history. Preserve retired Process, Risk, and Control IDs with replacements or “no replacement”; use plain ID mentions for IDs absent from the active table, as the renderer requires. A control shared with remaining rows keeps its ID and identical procedure set. Keep contrary-practice/source links available for later phases.

Search engagement artifacts across phases for affected IDs and references. Record Flags naming affected artifacts/sections or pending handoffs, and refresh only the RCM. Return changes to upstream-owned wording, ratings, objectives, or scope to their owners and the auditor. Keep materially unresolved review work visible until settled.

## Route information needs and responses

This skill owns the RCM's information needs. For external deliverables, invoke `document-request-list` for authorized creation or updates, including cold entry. Pass the deliverable, period/version, addressee if known, needing RCM section/IDs, and candidate retained-source links or proposed matches. Let that skill reconcile existing matches and preserve its Needed by behavior; record returned RQ IDs in Information gaps. Decide uncertain source sufficiency here or with the auditor, keeping the substantive gap visible meanwhile. Auditor-only questions stay in the RCM.

For responses, invoke `engagement-sources` for retention first, then pass its returned links and proposed RQ matches to `document-request-list`. That skill arranges confirmed RQ backlinks through `engagement-sources`; carry unfinished retention or provenance updates into the handoff. Unrequested material goes through `engagement-sources` without changing the list. For partial responses, carry returned remainder IDs and applicable Needed by references into remaining gaps, retaining links to the supplied portion. Received, Not available, or Withdrawn request states never silently resolve a substantive gap.

Use `document-request-list`'s returned affected references without repeating its RQ search. Add any substantive impacts identified here, flag other owners' work in the reply, and refresh only the RCM. Carry forward search limitations, continuing supported work while keeping potentially affected work unresolved.

Request messages/reminders belong to `document-request-list`; invoke it for requested messages or authorized changes and recommend optional next steps. When unavailable, preserve the gap and give a concrete handoff with the need, known details, candidate sources, and affected references, explicitly stating that the list was not updated. Request table edits and lifecycle belong only to that skill.

## Render and report readiness

Above the single table, state engagement context, the unchanged audit objective statement, memo objectives/approach references, upstream snapshot versions, and methodology basis. Below it, retain contrary practice, dated history, Information gaps with affected IDs and returned RQ IDs or auditor questions, Flags, and Sources. Use prose and lists, not supporting tables. Apply the contract's methodology directives when supported; if the renderer cannot represent the governing methodology, retain it unchanged and report the rendering limitation for resolution rather than alter upstream ratings to pass validation.

Run the bundled script using its installed skill path and the engagement's absolute Markdown path:

```text
python "<skill-directory>/scripts/render_rcm.py" "<engagement-directory>/planning/risk-and-control-matrix.md"
```

It validates before writing HTML and opens the generated view. Use `--no-open` when browser opening is unwanted. Resolve validation failures in owned content; route upstream conflicts to their owners. Failed validation leaves prior HTML unchanged, so identify it as stale and keep readiness pending. If only browser opening fails, report the saved HTML path separately. Inspect the resulting table and surrounding sections for preserved source links, visible gaps, consistent repeats, and usable numbered procedures.

Report ready for walkthroughs only for portions where every included control has a sourced description and usable reviewed procedures, every risk without an identified control has gap-assessment procedures, shared entries are consistent, Markdown validates and HTML has been regenerated, and no unresolved information would materially change planned work. Identify portions not ready and the blocking gaps/reviews, including pending upstream scope or objectives. A usable investigation plan can proceed with a suspected gap visible; a material unresolved planning basis cannot. List outstanding methodology requirements separately.

In the reply, give both paths, readiness against these criteria, affected portions, remaining gaps/RQ references, and Flags. Recommend walkthroughs with limitations clear: planning Markdown/HTML stay in place, and walkthroughs start their own working copy carrying every Process, Risk, and Control ID. Readiness is distinct from approval; neither request nor record approval.
