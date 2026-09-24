# Internal Audit Skills

A set of agent skills for internal auditors. This file defines the vocabulary the skills and their docs use about themselves; the organization's audit vocabulary lives in its working glossary.

## Language

**Auditor workspace**:
The user's working folder for one organization's audit work. Its root holds shared context; individual audit material lives under `engagements/`.

**Shared context**:
The working glossary, documented methodology captured in `METHODOLOGY.md`, and organizational overview in `ORGANIZATION.md` at the auditor workspace root. The `audit-context` skill maintains these files for other skills to read.

**Context template**:
An unpopulated starting structure shipped inside `audit-context` for one shared context document. It supplies headings and prompts, not definitions, requirements, or facts.

**Working glossary**:
The `GLOSSARY.md` at the auditor workspace root, holding the organization's own definitions. Every skill reads it when present; only the `audit-context` skill edits it.
_Avoid_: project glossary, engagement glossary

**Driver**:
The throwaway Python script the `exploratory-data-analysis` skill writes to the OS temporary directory for one selected source table. It holds the source selection, interpretation choices, and every calculation behind the report, and builds the report through the **Report** module.
_Avoid_: analysis script, notebook

**Report**:
The `Report` module in `exploratory-data-analysis/scripts/report.py`. It takes the driver's content (framing, data quality conditions, overview items, observations, limitations) and owns section order, section titles, omission of empty sections, validation, and escaping when it writes the offline HTML file.
_Avoid_: helpers, template

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

- A **Driver** builds exactly one **Report**
- A **Report** derives every **Mechanical condition** and date-field **Coverage span** from the profile, and the **Driver** explains each one
- Each **Context template** supplies the starting structure for one document in **Shared context**
- An **Auditor workspace** holds **Shared context**, including one **Working glossary**
