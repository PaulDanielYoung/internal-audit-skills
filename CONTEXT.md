# Internal Audit Skills

A set of agent skills for internal auditors. This file defines the vocabulary the skills and their docs use about themselves; the organization's audit vocabulary lives in its glossary.

## Language

**Planning stage skill and planning writing skill**:
A planning stage skill owns a planning artifact and carries the engagement through that stage under the auditor's judgement. A planning writing skill supplies reusable wording guidance to the auditor or a calling skill, owning no artifact or IDs.

**Auditor workspace**:
The user's working folder for one organization's audit work. Its root holds shared context; individual audit material lives under `engagements/`.

**Planning artifact**:
A persistent work product owned by a planning stage skill for one engagement, such as the engagement notification. On-demand agendas are not persistent artifacts; the shared engagement request list is a separate cross-phase artifact owned by `request-list`.

**Engagement notification**:
The initial communication from internal audit to management about an engagement, preserving the audit objective statement and presenting preliminary scope, period, timing, and next steps.

**Preliminary RCM**:
The planning artifact that maps the engagement's scoped processes and risks to intended controls and planned audit procedures. It carries the engagement work program, including procedures to investigate risks without identified controls, for the handoff to walkthroughs.

**Engagement sources**:
The retained supplied material and its provenance shared across an engagement's phases, maintained by `engagement-sources` and distinct from the work products derived from it.

**Receipt event**:
One occasion on which supplied material is received, with its original location and receipt date. Identical material can have several receipt events sharing one retained copy; recording an event does not confirm a request match or establish source sufficiency.

**Shared engagement request list**:
The cross-phase artifact owned by `request-list` that records external information requests and their lifecycle for one engagement. It is distinct from planning artifacts and from the information gaps those requests may help resolve.

**Request item**:
One deliverable requested from a party outside the engagement team, with its own stable RQ ID and history. Closing an item does not necessarily resolve the underlying information gap.

**Stable ID**:
A persistent reference to an item whose identity survives updates. An allocated ID is never renumbered or reused, including when the item is withdrawn.

**Information gap**:
Missing or unresolved information relevant to an engagement's work. In a communication draft, a minor gap appears as a visible placeholder with its explanation outside the communication.

**Stated readiness**:
The skill's report of whether its work meets its completion criteria and which gaps remain. Readiness is distinct from approval or sending a communication.

**Judgement point**:
A decision reserved for the auditor, presented with sourced considerations and recorded with its date and stated reason. The drafting skill supplies no proposed decision.

**Flag**:
A notice that a change may require an artifact's owning skill and the auditor to revisit earlier work or decisions. A flag identifies affected references without changing the downstream artifact.

**Engagement**:
One planned piece of internal audit work on a defined subject, carried from assignment through reporting, with its material in `engagements/<year>/<name>/`. "Audit" is an acceptable informal synonym in conversation; skills and docs say engagement.
_Avoid_: project, review

**Audit objective statement**:
The auditor-supplied statement of what an engagement is about and what it is intended to accomplish, as assigned. `create-engagement` records it and never invents it; planning refines objectives in its own deliverables and leaves this one unchanged.
_Avoid_: engagement objective, audit purpose, scope statement

**Engagement record**:
The `ENGAGEMENT.md` at the root of an engagement's folder, holding its name and audit objective statement. `create-engagement` creates it; every other engagement skill reads it to find the selected engagement and its output path.
_Avoid_: engagement file, engagement charter

**Shared context**:
The glossary, documented methodology captured in `METHODOLOGY.md`, and organizational overview in `ORGANIZATION.md` at the auditor workspace root. The `audit-terminology` skill maintains the glossary; the internal audit department maintains the other two as approved references for skills to read.

**Workspace instructions**:
The `## Internal audit skills` block in the auditor workspace's `CLAUDE.md` and the `docs/agents/workspace.md` it points to, established by `setup-internal-audit-skills`. Together they locate shared context, set its reading, use, and maintenance boundaries, carry engagement selection rules, and mark the workspace as set up.
_Avoid_: setup block, instruction block

**Glossary**:
The `GLOSSARY.md` at the auditor workspace root, holding the organization's own definitions. Every skill reads it when present; only the `audit-terminology` skill edits it.
_Avoid_: working glossary, project glossary, engagement glossary

**Source table**:
The one selected table the `exploratory-data-analysis` skill reads in place, with its values, error cells, locations, and reader disclosures. CSV and XLSX differ behind it; the profile, the **Driver**, and the **Report** never ask which they hold.
_Avoid_: source file, workbook, input

**Choices**:
The selection and interpretation overrides one profiling run applied: worksheet, Table or range, field roles, date formats, and encoding. The profile records them and the **Driver** repeats them unchanged.
_Avoid_: options, settings, overrides

**Driver**:
The throwaway Python script the `exploratory-data-analysis` skill writes to the OS temporary directory for one selected source table. It holds the source selection, interpretation choices, and every calculation behind the report, and builds the report through the **Report** module.
_Avoid_: analysis script, notebook

**Report**:
The `Report` module in `exploratory-data-analysis/scripts/report.py`. It takes the driver's content (framing, data quality conditions, overview items, observations, limitations) and owns section order, section titles, omission of empty sections, validation, and escaping when it writes the offline HTML file.
_Avoid_: helpers, template

**Visual**:
One chart or table the **Driver** hands to the **Report**: a value from the charts module that knows its kind, what it drew, and any groups it folded into Other. The Report accepts nothing else as a chart or table.
_Avoid_: markup, SVG string, figure

**Condition**:
One row of the report's data quality assessment: a field, what was observed in it, how many records it affects, and why it matters to a reader of the data.
_Avoid_: finding, issue, data quality row

**Mechanical condition**:
A **Condition** the **Report** derives from the profile without judgment, such as blank cells or unparsed values. The **Driver** explains why it matters; it never records or omits one.
_Avoid_: automatic condition, computed condition

**Coverage span**:
The reach of one date or period field: its earliest and latest valid values and how many records carry one. Spans for date fields are mechanical; spans for period labels come from the **Driver**.
_Avoid_: date range, period coverage

## Relationships

- A **Planning stage skill** uses **Planning writing skills** to word content in its artifact
- A **Planning stage skill** owns a **Planning artifact** for one **Engagement**
- An **Engagement notification** is a **Planning artifact** that preserves the **Audit objective statement**
- A **Preliminary RCM** is a **Planning artifact** that carries planned procedures for one **Engagement**
- **Engagement sources** support work across one **Engagement**; **Stated readiness** identifies remaining **Information gaps**
- **Engagement sources** preserve **Receipt events** independently of confirmed **Request item** matches
- A **Shared engagement request list** holds **Request items** across one **Engagement**; each item has a **Stable ID**
- A **Request item** can support several artifacts or workstreams, and several items can address one **Information gap**
- A **Driver** profiles exactly one **Source table** with the **Choices** its profiling run recorded
- A **Driver** builds exactly one **Report**
- A **Driver** builds every **Visual** through the charts module and passes it to its **Report**
- A **Report** derives every **Mechanical condition** and date-field **Coverage span** from the profile, and the **Driver** explains each one
- Each **Context template** is the starting structure for one document in **Shared context**
- An **Auditor workspace** holds **Shared context**, including one **Glossary**
- An **Auditor workspace** holds many **Engagements**, each in its own folder under `engagements/<year>/`
- An **Engagement** has exactly one **Engagement record**, which records exactly one **Audit objective statement**
- **Workspace instructions** locate the **Shared context** of one **Auditor workspace** and say how a conversation selects one of its **Engagements**
