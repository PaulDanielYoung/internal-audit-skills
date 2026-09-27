---
name: preliminary-survey
description: Draft or refresh a preliminary survey to understand the activity under audit or the auditee's environment. Use also to summarize prior reports and sources for planning. Owns the process list and flags matters for risk assessment.
---

# Preliminary Survey

Describe the activity under audit in a sourced internal workpaper at `planning/preliminary-survey.md` in the selected engagement. Own the process list and Process IDs inherited by later planning artifacts. Describe and flag matters; risk wording and rating belong to `risk-assessment` and `risk-statements`. Scope, criteria, and topical requirement applicability belong to `planning-memo`.

## Establish the basis

Follow the workspace instructions for engagement selection, read its `ENGAGEMENT.md`, and state the selected engagement and output path. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Use `audit-terminology` for missing, ambiguous, or contested terms and settled definitions.

Documented methodology governs the work. For structure, use a supplied organization template, then methodology, then relevant prior workpapers, then the defaults below. Read any longer retained source the methodology points to. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names and file paths fixed. State the methodology or default basis in the workpaper. Resolve unclear or conflicting methodology with the auditor through `shared-understanding`. List requirements outside this skill's remit as outstanding, with their methodology source.

Inspect available material before asking for more. Gather only what the survey needs: activity descriptions, organization charts, procedures, framework documents, prior assurance, management or entrance meeting notes, and equivalent auditor-supplied material. Accept an equivalent survey produced elsewhere, having `engagement-sources` preserve a received copy before adopting a working copy at the survey path. When entering before notification, recommend `engagement-notification`; if the auditor declines, continue with a provisional survey. Neither notification-sent status nor an existing request list is a prerequisite.

Use `shared-understanding` for material ambiguity that could change the survey, including unclear activity objectives or process boundaries; pause only the affected portion. Ask the material questions directly if that skill is unavailable. Preserve the assignment's audit objective statement verbatim and leave the engagement record unchanged. Minor gaps get descriptive bracketed markers in place and entries in Information gaps without interrupting the work.

## Retain and ground the sources

Delegate source retention and provenance updates to `engagement-sources`, passing supplied material and known original locations and receipt dates. Use its returned retained-source links. If unavailable, continue supported work from already-retained material and give a concrete handoff for outstanding retention or provenance updates; do not write sources or their index as a fallback. Settle which version governs with the auditor when unresolved.

Every factual statement carries an inline citation at the end of its sentence or paragraph to its retained copy and relevant location, or an explicit basis such as a dated auditor statement. `ORGANIZATION.md` also counts as a source. Label meeting notes as such. Accept dictated notes as auditor statements; invoke `engagement-sources` for a dated note when requested or when using a verbal answer as a request receipt. Taking minutes is outside this skill's work.

Use only facts supported by supplied material or the auditor. General subject context, if helpful, belongs in a clearly labelled note and supplies no facts about this activity. Use summary figures already stated in sources. For raw CSV or XLSX extracts, recommend `exploratory-data-analysis`; have `engagement-sources` retain its resulting report and cite the returned link when used, rather than profiling the extract here.

Use retained local framework documents; a missing document or undated edition is an information gap for the auditor, not a reason to fetch an external reference. Use plain concept terms and attribute rules to documented methodology without quoting, citing, or numbering IIA or ISACA text. Describe the subject from sources without classifying the engagement by type.

## Draft the survey

Use these default sections in order. Keep an unsourced section with a bracketed gap and list the missing information under Information gaps.

1. **Engagement context:** why the engagement is in the plan, the audit objective statement quoted unchanged from the engagement record, and changes since the plan was set.
2. **Activity overview:** the activity's purpose and objectives, mandate, and scale, including sourced volumes, spend, headcount, and locations. Distinguish activity objectives from the assignment's audit objective statement.
3. **Governance and organization:** owners, reporting lines, key roles, committees, and oversight.
4. **Processes:** a table with **Process ID**, **Process Title**, and **Process Description**, following the ownership rules below.
5. **Systems and data:** applications, interfaces, data held, and ownership.
6. **Policy, regulatory, and contractual framework:** the documented framework as fact, with factual topic links such as the use of third-party processors. Leave criteria selection and applicability decisions to `planning-memo`.
7. **Recent changes and developments:** sourced reorganizations and changes in systems, regulation, or volume.
8. **Prior assurance:** earlier engagement results, open findings and their reported remediation status, and other assurance providers and their coverage.
9. **Management's perspective:** attributed concerns and changes raised by management.
10. **Matters for risk assessment:** candidate areas, each pointing to the source fact it came from, such as “Vendor onboarding system change in March.” Keep risk event chains and ratings for the assessment. The list may be explicitly empty when sources reveal no matters; missing coverage remains a gap.
11. **Information gaps:** each in-place gap, its affected section, whether it could change the process list or activity objectives, and its returned RQ ID or question put to the auditor. Include outstanding methodology requirements and unresolved handoffs.
12. **Sources:** links to the retained copies used and other stated bases, preserving provenance and prior-content labels.

### Process ownership

Use `process-statements` to draft and review every process title and description. Check its completeness elements: purpose, start trigger and end point, main activities, roles, systems, and key inputs and outputs where they clarify boundaries. Carry its source links, basis labels, and bracketed gaps into the table. If unavailable in an independent install, apply these elements directly and report that the wording review remains outstanding. Compare the flows with all available activity sources for coverage, overlap, and handoff gaps; ask through `shared-understanding` when an ambiguity could change the list.

Allocate `P-01`, `P-02`, and so on above the highest allocated Process ID, including retired IDs. Preserve IDs already established for the engagement, including provisional IDs in later artifacts; reconcile conflicting identities with the auditor before allocation. Wording updates keep the ID. A split or merge gives each resulting process a new ID; mark the old IDs retired with a note naming their replacements. A dropped process keeps its old ID as retired, with “no replacement” when applicable; any replacement gets a new ID. Keep retired entries and their history visible below the active process table. Never renumber or reuse an ID.

### Refresh and downstream flags

When an earlier survey of the same activity exists, offer to refresh it. If accepted, have `engagement-sources` retain an unchanged received copy and work at the current survey path. Label carried content not reconfirmed by a current source or the auditor as “prior engagement; not reconfirmed,” with its citation. Preserve the current engagement's established IDs when reconciling the earlier list. Reassess currency gaps against readiness; prior coverage alone does not establish current completeness.

Compare a refresh with the existing survey and any upstream flags. Record changes and affected downstream references in a note within Processes or the relevant section, and flag them in the reply for re-decision. A process-list change flags `risk-assessment` and the RCM, plus any affected planning memo references. Search existing engagement artifacts for affected Process IDs and objectives; identify pending handoffs when an artifact does not yet exist. Refresh only the survey, leaving downstream content and prior decisions for their owning skills.

## Route information needs and responses

This skill decides what information the survey needs. For each external deliverable, invoke `request-list` for authorized creation or updates, including cold entry with no list. Pass the deliverable, period/version, addressee if known, needing artifact/section, and candidate retained-source links or proposed matches. Preserve unknown details as gaps. Let `request-list` reconcile existing material and open matches and return IDs; record those IDs in Information gaps. Decide uncertain substantive source sufficiency here or with the auditor, keeping the gap visible until settled. Auditor-only questions stay in the survey.

For supplied responses, invoke `engagement-sources` for retention first, then pass its returned links and proposed RQ matches to `request-list`. That skill arranges confirmed RQ backlinks through `engagement-sources`; carry any unfinished retention or provenance updates into the handoff. For partial responses, use the returned remainder IDs and applicable Needed by references to update the survey's remaining gaps, preserving the link to the supplied portion. A closed request, including Not available or Withdrawn, does not resolve a substantive gap by itself.

Use `request-list`'s returned affected references without repeating its RQ search. Add any substantive impacts identified here, flag other owners' work in the reply, and refresh only this survey. Carry forward search limitations, continuing supported work while keeping potentially affected work unresolved.

Route request messages and reminders to `request-list` as well. Invoke it for authorized changes and requested messages; recommend it for optional next steps. Request IDs, states, lifecycle, and table edits belong only to that skill. When it is unavailable, keep the survey's gaps visible and return a concrete handoff with the need, known details, candidate sources, and affected references. Explicitly state that the list has not been updated; never edit the request table as a fallback.

## Report readiness

Save the survey in Markdown. It is ready for `risk-assessment` when all of these hold:

- The activity's objectives are stated.
- The process list covers the activity described by the assignment, as far as current sources show.
- Every section is sourced or has its gap named.
- No open gap would change the process list or activity objectives. Resolve such a gap through `shared-understanding`, pausing the affected work meanwhile.
- The Matters for risk assessment list exists, even if explicitly empty.

In the reply, give the output path, stated readiness against these criteria, remaining gaps and RQ references, outstanding methodology requirements, and downstream flags. Recommend `risk-assessment`, with blockers clear when the survey is not ready. Readiness is distinct from approval: neither request nor record approval, and send no communications.
