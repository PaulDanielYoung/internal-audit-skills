---
name: risk-assessment
description: Assess or rate an engagement's inherent risks, identify risks from a preliminary survey, rank risks for scoping, or reassess after an upstream or RCM flag. Single-risk wording goes to risk-statements.
---

# Risk Assessment

Own the engagement risk assessment at `planning/risk-assessment.md` in the selected engagement, including Risk IDs and activity Objective IDs. Identify, word, and present inherent risks for the auditor to rate. Rank risks for `planning-memo`; scope decisions belong there. List no controls; those belong to the RCM.

## Establish the basis

Follow the workspace instructions for engagement selection, read its `ENGAGEMENT.md`, and state the selected engagement and output path. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Use `audit-context` for missing or contested terms and settled changes to persistent shared context.

Documented methodology overrides defaults. For structure, use a supplied organization template, then methodology, then relevant prior workpapers, then the defaults below. Read longer retained sources the methodology points to. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names, paths, and ID prefixes fixed. State the methodology or default basis in the workpaper. Surface unclear or conflicting methodology and propose an `audit-context` update rather than guess. List requirements outside this skill's remit as outstanding with their methodology source.

Inspect available material before asking for more. Gather only what this assessment needs: the survey, prior assessments and findings, incidents, management concerns, and equivalent auditor-supplied material. Accept an equivalent assessment produced elsewhere, retaining a received copy and adopting a working copy at the assessment path. Preserve the assignment's audit objective statement verbatim and leave the engagement record unchanged.

Use `shared-understanding` for material ambiguity that could change the assessment, pausing only the affected portion; ask directly if unavailable. Minor gaps get descriptive bracketed markers in place and entries in Information gaps. Use retained local framework documents; a missing document or undated edition is a gap for the auditor, not a reason to fetch an external reference. Use plain concept terms and attribute rules to documented methodology without quoting, citing, or numbering IIA or ISACA text. Describe the activity without classifying the engagement by subject type.

### Sources and provenance

Retain supplied material in the engagement's shared `sources/` folder, preserving originals. Reuse identical copies, keep changed versions separately, and record original location and receipt date in `sources/README.md`. Ask which version governs when unsettled.

Every factual statement, including each rating consideration, carries an inline citation to the retained copy and relevant location, or an explicit basis such as a dated auditor statement. Cite the survey and its underlying sources when carrying its content. `ORGANIZATION.md` also counts as a source. Label meeting notes and prior-content bases. General knowledge supplies labelled candidates, never facts about this activity.

## Establish processes and activity objectives

Inherit the survey's Process IDs and process list unchanged. Carry its activity objectives once, with their wording and sources, into Activity objectives; distinguish them from the assignment's audit objective statement. Allocate short Objective IDs (`O-01`, `O-02`, and so on) and preserve established identities on updates. These IDs are owned inside the assessment; downstream references may cite them, but they add no objective layer to the RCM. Include a process-level objective only when a source states one. Missing objectives remain gaps rather than being inferred from process names.

Without a survey, recommend `preliminary-survey`. If declined, use equivalent material and establish any missing process list provisionally inside this assessment, with Process ID, Process Title, and Process Description. Use `process-statements` for that wording; if unavailable, mark its review outstanding. Preserve existing engagement Process IDs, allocate new provisional `P-nn` IDs above the highest allocated number, and flag the list for the survey to adopt. An absent request list or notification-sent status is no prerequisite. Pause the whole assessment through `shared-understanding` only when neither objectives nor processes can be established; otherwise draft what is supported, keeping missing links visible and the affected work pending.

## Identify and word risks

Consider candidates in this order: methodology and organization context; sourced facts from survey matters, prior findings, incidents, and management concerns; the auditor; then labelled general-knowledge candidates. Retain a general-knowledge candidate only when the auditor accepts it or a source supports it, recording that dated acceptance or source as its basis. Ask about unsupported candidates before adding them to the assessment. Omit rejected candidates and survey matters that do not become risks.

Give each retained risk one Risk ID (`R-01`, `R-02`, and so on), linked to every Process ID it affects and at least one Objective ID. A risk affecting several processes remains one risk. Draft and review every new or edited Risk Description through `risk-statements`, passing its linked objectives as context and preserving citations, basis labels, and gap markers. Write the short Risk Title here. Compare descriptions for duplicate event chains; split only where `risk-statements` identifies distinct chains that would be assessed or managed differently. A rating-only change keeps the existing wording review. If `risk-statements` is unavailable, keep the description provisional and explicitly report the required review as outstanding.

### Stable IDs and flags

Allocate Risk IDs above the highest allocated number, including retired IDs. Rewording or re-rating keeps the ID. Splits and merges give each resulting risk a new ID; retire old entries with their replacement IDs. A dropped risk keeps a retired entry, with “no replacement” when applicable. Keep retirement history visible below the active risks. Never renumber or reuse IDs; preserve Objective IDs likewise and reconcile identity conflicts with the auditor before allocating replacements.

For a new, changed, or retired risk, record the change and affected references in its entry or retirement history, and flag `planning-memo` and the RCM for re-decision in the reply. Search existing engagement artifacts for affected Risk IDs, Process IDs, and objectives; name pending handoffs when an artifact does not yet exist. Refresh only this assessment. Downstream decisions remain visible in their owners' artifacts until re-decided.

### Refresh an earlier assessment

When an earlier assessment of the same activity exists, offer to refresh it. On acceptance, retain an unchanged received copy in `sources/` and work at the current assessment path, reconciling identities with this engagement's established IDs. Label carried risks “prior engagement; not reconfirmed” until a current source or the auditor reconfirms them. Show prior ratings only as sourced likelihood or impact considerations; leave current ratings, score, and band blank until the auditor rates. For reassessment after a flag, move the affected risks' previous ratings into considerations and reopen their current ratings, preserving unaffected current decisions. Treat unresolved currency or upstream changes as gaps against readiness.

## Present the rating judgement point

For each risk, lay out sourced **likelihood considerations** (such as frequency, volumes, complexity, change, findings, and incidents) and **impact considerations** (such as financial size, regulatory exposure, customers, operations, and the linked objective). Describe the activity before controls. Show methodology's scale and calibration; absent methodology, show only the bare integer scale 1 to 5 for each dimension, without invented calibration labels. Present no proposed likelihood, impact, score, or band.

Ask the auditor to rate likelihood and impact and give the date and reason. Record the auditor's ratings, date, and reason; mark missing decision details visibly and ask for them rather than inventing a rationale. An undecided dimension stays blank, with score and band blank too. Check supplied values against the scale and resolve out-of-range values with the auditor.

Compute Score as Likelihood × Impact and derive Band from the computed score using an executable calculation, never manual entry. Default bands are Low 1–4, Moderate 5–9, High 10–16, Critical 17–25; methodology overrides the rating method and bands. Resolve an incomplete or conflicting method before computing affected results. Recompute after a rating or method change and use the same results in the summary and risk entries.

Rank rated risks by band from highest to lowest, then score descending. Use Risk ID order for ties; place unrated risks last in Risk ID order. This mechanical sort is the entire ranking, with no additional priority or scope judgement.

## Check coverage and assemble the assessment

Before handoff, consider fraud, IT and systems, compliance, and third-party risks, or methodology's replacement list. For each topic, link the retained risks or state a sourced reason none applies. Where coverage raises a candidate, take it through identification, wording, and the rating judgement point. Unresolved coverage remains a gap. This is a coverage check, not a taxonomy or risk field.

Use these default sections in order, retaining missing content with bracketed gaps:

1. **Engagement context:** the audit objective statement quoted unchanged and a link to the survey, or the provisional entry basis and process list.
2. **Activity objectives:** Objective IDs, carried wording, and sources.
3. **Rating method:** scale, calibration if supplied, formula, bands, and methodology or default basis.
4. **Risk summary:** ranked table with Risk ID, Risk Title, Process IDs, Objective IDs, Likelihood, Impact, Score, and Band.
5. **Risks:** entries in the same ranked order, each with description, basis, linked processes and objectives, likelihood and impact considerations, and recorded rating with date and reason. Include wording-review status, changes, flags, and retirement history where applicable.
6. **Coverage check:** topics considered, linked risks or reasons none applies, and outstanding questions.
7. **Information gaps:** affected risk or section, whether the gap could add, remove, or re-rate a risk, and its returned RQ ID or question put to the auditor. Include outstanding methodology requirements and unresolved handoffs.
8. **Sources:** retained copies used and other stated bases, preserving provenance and prior-content labels.

## Route information needs and responses

This skill decides what information the assessment needs. For each external deliverable, invoke `request-list` for authorized creation or updates, including cold entry with no list. Pass the deliverable, period/version, addressee if known, needing artifact/section, and candidate retained-source links or proposed matches. Preserve unknown details as gaps. Let `request-list` reconcile existing material and open matches and return IDs; record those IDs in Information gaps. Decide uncertain substantive source sufficiency here or with the auditor, keeping the gap visible until settled. Auditor-only questions stay in the assessment.

For supplied responses, retain and index material first, then pass its retained link and proposed RQ matches to `request-list`. Add returned RQ IDs to the source's provenance in `sources/README.md` after auditor-confirmed matching. For partial responses, use returned remainder IDs and applicable Needed by references to update this assessment's remaining gaps, preserving the link to the supplied portion. Search engagement artifacts across phases for affected RQ references and combine them with the returned affected references; flag other owners' work in the reply and refresh only this assessment. A closed request, including Not available or Withdrawn, does not resolve a substantive gap by itself.

Route request messages and reminders to `request-list` as well. Invoke it for authorized changes and requested messages; recommend it for optional next steps. Request IDs, states, lifecycle, and table edits belong only to that skill. When unavailable, keep gaps visible and return a concrete handoff with the need, known details, candidate sources, and affected references. Explicitly state that the list has not been updated; never edit the request table as a fallback.

## Report readiness

Save the assessment in Markdown. It is ready for `planning-memo` when every active risk links to a process and an objective, every description has gone through `risk-statements`, every risk is rated by the auditor, the coverage check is done, and no open gap would add, remove, or re-rate a risk. Resolve such a gap through `shared-understanding`, pausing that risk meanwhile.

In the reply, give the output path, stated readiness against each criterion, named undecided risks, remaining gaps and RQ references, outstanding methodology requirements, and downstream flags. Recommend `planning-memo`, with blockers clear when not ready. Readiness is distinct from approval: neither request nor record approval, and send no communications.
