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

## Relationships

- A **Driver** builds exactly one **Report**
- Each **Context template** supplies the starting structure for one document in **Shared context**
- An **Auditor workspace** holds **Shared context**, including one **Working glossary**
