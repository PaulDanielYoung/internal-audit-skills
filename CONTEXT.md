# Internal Audit Skills

A set of agent skills for internal auditors. This file defines the vocabulary the skills and their docs use about themselves; the organization's audit vocabulary lives in its glossary.

## Language

**Planning stage skill and planning writing skill**:
A planning stage skill owns a planning artifact and carries the engagement through that stage under the auditor's judgement. A planning writing skill supplies reusable wording guidance to the auditor or a calling skill, owning no artifact or IDs.

**Auditor workspace**:
The user's working folder for one organization's audit work. Its root holds shared context; individual audit material lives under `engagements/`.

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
The glossary, documented methodology captured in `METHODOLOGY.md`, and organizational overview in `ORGANIZATION.md` at the auditor workspace root. The `audit-context` skill maintains these files for other skills to read.

**Workspace instructions**:
The `## Internal audit skills` block that `setup-internal-audit-skills` adds to the auditor workspace's `CLAUDE.md`. It locates the shared context files, sets the reading and capture rules, carries the engagement selection rules, and marks the workspace as set up.
_Avoid_: setup block, instruction block

**Context template**:
The starting file shipped inside `audit-context` for one shared context document: a title, a one-sentence description, and any fixed heading.

**Glossary**:
The `GLOSSARY.md` at the auditor workspace root, holding the organization's own definitions. Every skill reads it when present; only the `audit-context` skill edits it.
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
- A **Driver** profiles exactly one **Source table** with the **Choices** its profiling run recorded
- A **Driver** builds exactly one **Report**
- A **Driver** builds every **Visual** through the charts module and passes it to its **Report**
- A **Report** derives every **Mechanical condition** and date-field **Coverage span** from the profile, and the **Driver** explains each one
- Each **Context template** is the starting file for one document in **Shared context**
- An **Auditor workspace** holds **Shared context**, including one **Glossary**
- An **Auditor workspace** holds many **Engagements**, each in its own folder under `engagements/<year>/`
- An **Engagement** has exactly one **Engagement record**, which records exactly one **Audit objective statement**
- **Workspace instructions** locate the **Shared context** of one **Auditor workspace** and say how a conversation selects one of its **Engagements**
