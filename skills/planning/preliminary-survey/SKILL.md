---
name: preliminary-survey
description: Draft or refresh a preliminary survey to understand the activity under audit or the auditee's environment. Use also to summarize prior reports and sources for planning. Owns the process list and flags matters for risk assessment.
---

# Preliminary Survey

Describe the activity under audit in a sourced internal workpaper at `planning/preliminary-survey.md` in the selected engagement. Own the process list and Process IDs inherited by later planning artifacts. Describe and flag matters; risk wording and rating belong to `risk-assessment` and `risk-statements`. Scope, criteria, and topical requirement applicability belong to `planning-memo`.

## Establish the basis

Follow the workspace instructions for engagement selection, read its `ENGAGEMENT.md`, and state the selected engagement and output path. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Use `audit-terminology` when a term's meaning needs agreement or consistency across engagements.

Documented methodology governs the work. For structure, use a supplied organization template, then methodology, then relevant prior workpapers, then the defaults below. Read any longer retained source the methodology points to. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names and file paths fixed. State the methodology or default basis in the workpaper. Resolve unclear or conflicting methodology with the auditor through `shared-understanding`. List requirements outside this skill's remit as outstanding, with their methodology source.

Inspect available material before asking for more. Gather only what the survey needs: activity descriptions, organization charts, procedures, framework documents, prior assurance, management or entrance meeting notes, and equivalent auditor-supplied material. Accept an equivalent survey produced elsewhere, preserving its original as described below. Neither notification-sent status nor an existing request list is a prerequisite; assess readiness using the criteria below.

Use `shared-understanding` for material ambiguity that could change the survey, including unclear activity objectives or process boundaries; pause only the affected portion. Ask the material questions directly if that skill is unavailable. Preserve the assignment's audit objective statement verbatim and leave the engagement record unchanged. Minor gaps get descriptive bracketed markers in place and entries in Information gaps without interrupting the work.

## Ground the work in sources

Read source files in place and leave originals unchanged. The auditor places client-provided files in `document-requests/received/`; cite those files, other available local references, and upstream workpapers directly. Record known source dates or versions and relevant locations; leave unknown provenance explicit. Settle conflicting versions with the auditor. When adopting an external draft, create the working copy at this skill's output path only after a separate unchanged original is available.

Every factual statement carries an inline citation at the end of its sentence or paragraph to the source file and relevant location, or an explicit basis such as a dated auditor statement. `ORGANIZATION.md` also counts as a source. Label meeting notes as such. Record relevant verbal facts as dated, attributed statements in the workpaper; keep unconfirmed accounts visibly unresolved.

Use only facts supported by supplied material or the auditor. General subject context, if helpful, belongs in a clearly labelled note and supplies no facts about this activity. Use summary figures already stated in sources. For raw CSV or XLSX extracts, recommend `exploratory-data-analysis` rather than profiling the extract here. Its report is temporary: before using its observations in the survey, record the source file, selected table, run date, relevant results, and limitations in the workpaper so the survey does not depend on a temporary report link. Treat exploratory observations as leads for follow-up.

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

When an earlier survey of the same activity exists, offer to use it as the starting point for the current survey. If accepted, leave the earlier artifact unchanged and work at the current survey path. Label carried content not reconfirmed by a current source or the auditor as “prior engagement; not reconfirmed,” with its citation. Reconcile earlier processes with this engagement's established identities and allocate IDs under the ownership rules above. Reassess currency gaps against readiness; prior coverage alone does not establish current completeness.

Compare a refresh with the existing survey and any upstream flags. Record changes and affected downstream references in a note within Processes or the relevant section, and flag them in the reply for re-decision. A process-list change flags `risk-assessment` and the RCM, plus any affected planning memo references. Search existing engagement artifacts for affected Process IDs and objectives; identify pending handoffs when an artifact does not yet exist. Refresh only the survey, leaving downstream content and prior decisions for their owning skills.

## Route information needs and responses

Record missing information and its effect on the work in Information gaps. Invoke `document-request-list` when missing material warrants a document request, relevant information or received files may change an existing request, or the auditor asks to create or update the list. Pass the selected engagement, the material needed and why, known period/version, request owner and due date, relevant files, and any existing request ID or auditor instruction. Let that skill manage approval of new requests and maintain the list; record returned RQ IDs beside the corresponding gaps. Questions requiring the auditor's judgement stay in this workpaper.

Cite received material when updating the workpaper and assess whether it resolves each affected gap. A request's status alone does not establish that the workpaper's information need is satisfied.

If `document-request-list` is unavailable, continue supported work, keep gaps visible, and return proposed requests or status changes as a handoff, explicitly stating that the list was not updated. Request table edits belong to that skill.

## Report readiness

Save the survey in Markdown. It is ready for `risk-assessment` when all of these hold:

- The activity's objectives are stated.
- The process list covers the activity described by the assignment, as far as current sources show.
- Every section is sourced or has its gap named.
- No open gap would change the process list or activity objectives. Resolve such a gap through `shared-understanding`, pausing the affected work meanwhile.
- The Matters for risk assessment list exists, even if explicitly empty.

In the reply, give the output path, stated readiness against these criteria, remaining gaps and RQ references, outstanding methodology requirements, and downstream flags. Recommend `risk-assessment`, with blockers clear when the survey is not ready. Report readiness separately from the auditor decisions and document-request approvals required above; add no final approval gate and send no communications.
