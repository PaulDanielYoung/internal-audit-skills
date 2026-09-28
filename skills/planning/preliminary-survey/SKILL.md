---
name: preliminary-survey
description: Develop or refresh a preliminary survey at the start of engagement planning. Establish a sourced understanding of the activity, maintain its process list, and identify matters and information gaps for risk assessment.
---

# Preliminary Survey

Build an initial understanding of the activity under review: what it aims to achieve, how it is organized, how its processes are intended to work, and what has changed. Save the survey at `planning/preliminary-survey.md` in the selected engagement.

The survey owns the process list and Process IDs used by later workpapers. Describe known controls and concerns where they help explain the activity. Risk assessment, engagement scope decisions, criteria selection, and conclusions about control design or effectiveness belong to subsequent work.

## 1. Establish the starting point

Read the selected engagement's `ENGAGEMENT.md`. Preserve its audit objective statement verbatim in the survey and leave the engagement record unchanged. Distinguish that assignment from the activity's own business objectives.

Establish why the engagement was commissioned, the initial expectations and known boundaries, and relevant changes since the assignment was made. Review the risk assessment supporting the audit plan, when available, alongside prior engagement material and management's concerns. Treat initial boundaries as context for understanding the activity; later scope decisions belong to `planning-memo`.

Use the organization's supplied template when consistent with its methodology. Otherwise, read and follow [SURVEY-FORMAT.md](SURVEY-FORMAT.md), adapting the detail to the activity and the assignment. Record the basis used. Relevant prior workpapers can inform the structure and content without establishing current facts.

## 2. Gather and describe the activity

Inspect available material before identifying additional information needs. Useful sources include activity plans and objectives, performance reports, organization charts, policies, procedures, process maps, system documentation, management risk assessments, prior assurance reports, and attributed meeting notes.

Develop enough understanding to explain the activity's objectives, process boundaries, responsibilities, dependencies, and operating environment. Capture established risk tolerance and the measures management uses to judge performance. Describe governance, risk management, and known control arrangements at a level that supports risk assessment.

Distinguish documented design, reported practice, and direct observation. Preserve differences between them with their sources; a procedure document alone does not establish what happens in practice. If a focused discussion or process observation is needed to understand a material uncertainty, identify what it must resolve. Detailed walkthroughs will corroborate and deepen the understanding; they need not be completed before every survey can support risk assessment.

Identify matters for risk assessment from the facts gathered, such as significant changes, dependencies, incidents, management concerns, or unresolved prior findings. Link each matter to its source and relevant process when known. Leave formal risk statements, ratings, and prioritization to `risk-assessment`.

### Sources and evidence

Read source files in place and preserve originals. Cite client material in `document-requests/received/`, other available references, and relevant workpapers. When adopting an externally prepared survey, retain an unchanged original before creating the engagement's working copy.

Support factual statements with inline citations at the end of the sentence or paragraph, including the relevant source location and known date or version. Record verbal information as dated, attributed statements. Keep unknown provenance and conflicting accounts visible. General subject knowledge may supply labelled background or questions; it does not establish facts about this activity.

Record the frameworks and requirements evidenced by the sources, including their known editions. Missing or uncertain references remain information gaps. Evaluation criteria and topical requirement applicability decisions belong to `planning-memo`; this survey records the factual basis for those decisions.

Use sourced summary figures. When raw CSV or XLSX extracts need exploration, use `exploratory-data-analysis` if available. Before relying on its temporary report, retain the source file reference, selected table, run date, relevant observations, and limitations in the survey. Treat those observations as leads for follow-up.

## 3. Establish the process list

Maintain a table with **Process ID**, **Process Title**, and **Process Description**. Use `process-statements` to draft or review titles and descriptions, retaining its source references and distinctions between documented, reported, and observed practice. If unavailable, describe each process's purpose, boundaries, main activities, roles, systems, and relevant inputs and outputs, and report the unavailable wording guidance.

Compare the list with the activity sources for missing coverage, overlapping processes, and unclear handoffs. A system or department alone does not define a process. Keep unresolved boundaries visible rather than presenting an incomplete list as settled.

Preserve Process IDs already established in this engagement, including provisional IDs in downstream workpapers. Resolve conflicting identities before assigning IDs. Allocate new IDs as `P-01`, `P-02`, and so on above the highest allocated number, including retired IDs. Never renumber or reuse an ID.

Wording changes retain the ID. A split or merge gives each resulting process a new ID; retire the old IDs and name their replacements. A dropped process retains a retirement entry with its replacement or "no replacement". Keep this history below the active process table.

## 4. Address information gaps

Mark missing information where it belongs and maintain an Information gaps section. For each gap, state what is missing, the affected process or section, its effect on the survey, and the question or material needed to resolve it. Distinguish an unknown fact from a confirmed absence or an item that does not apply.

Use `document-request-list` when missing material warrants a document request or received material may affect an existing request. Pass the engagement, the material needed and why, known period or version, request owner and due date, relevant files, and any existing request ID. That skill maintains the list and handles approval of new requests. Record returned RQ IDs against the corresponding gaps. Keep questions requiring auditor judgment in the survey.

When material arrives, assess whether its contents resolve the gap and update the survey with citations. A request's status alone does not resolve the information need. If `document-request-list` is unavailable, report the proposed handoff and leave request-list edits pending.

## 5. Refresh existing work

Update the current engagement's survey in place. Use earlier engagement surveys as references, leaving their originals unchanged. Label carried content without current support as "prior engagement; not reconfirmed" and assess its effect on readiness. Reconcile process identities with those already established for the current engagement.

For changes to processes, objectives, or other material facts, search existing engagement workpapers for affected references. Record the changes and flag the affected risk assessment, planning memo, RCM, or later workpapers for review by their owning skills. Update only the survey; preserve downstream decisions until they are reconsidered.

## 6. Report readiness for risk assessment

Check that:

- The activity's objectives are supported and distinguished from the assignment's audit objective statement.
- The process list covers the activity described by the assignment, as far as current sources show, with boundaries and handoffs sufficiently clear to identify risks.
- Relevant survey topics have sourced content, an explained absence or non-applicability, or a named information gap.
- Matters for risk assessment are linked to their supporting facts, or the section explicitly states that none were identified from the material reviewed.
- No unresolved gap prevents meaningful risk assessment of the portion being handed over, including understanding its objectives, processes, scale, and material dependencies.

Report readiness for the supported portions and identify what remains pending. Minor gaps need not stop risk assessment; explain which gaps prevent the affected portion from being ready and why. Readiness here concerns the basis for risk assessment, not completion of planning or confirmation that controls work.

Return the saved path, a concise account of the activity and significant matters, readiness, remaining gaps and RQ references, and affected downstream workpapers. Recommend `risk-assessment` as the next step where ready, identifying the information needed elsewhere. This skill produces an internal workpaper; communications and professional approvals follow the engagement's established workflow.
