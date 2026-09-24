# Internal Audit Skills

A set of agent skills for internal auditors. This file defines the vocabulary the skills and their docs use about themselves; the audit vocabulary the skills hand to auditors lives in the seed glossary.

## Language

**Seed glossary**:
The general internal audit definitions the skills assume, shipped inside the `glossary` skill as `SEED-GLOSSARY.md`. The starting point offered when a project has no working glossary yet.
_Avoid_: default glossary, template glossary

**Working glossary**:
The `GLOSSARY.md` in the user's working directory, holding the organization's own definitions. Every skill reads it; only the `glossary` skill edits it.
_Avoid_: project glossary, engagement glossary

**Driver**:
The throwaway Python script the `exploratory-data-analysis` skill writes to the OS temporary directory for one selected source table. It holds the source selection, interpretation choices, and every calculation behind the report, and builds the report through the **Report** module.
_Avoid_: analysis script, notebook

**Report**:
The `Report` module in `exploratory-data-analysis/scripts/report.py`. It takes the driver's content (framing, data quality conditions, overview items, observations, limitations) and owns section order, section titles, omission of empty sections, validation, and escaping when it writes the offline HTML file.
_Avoid_: helpers, template

## Relationships

- A **Driver** builds exactly one **Report**
- The **Seed glossary** is the offered starting point for a **Working glossary**
