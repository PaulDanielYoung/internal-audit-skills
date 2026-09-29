---
name: preliminary-survey
description: Develop or refresh an engagement's preliminary survey and its process list. Use when starting engagement planning or building an understanding of the activity under review.
---

# Preliminary Survey

Build a sourced understanding of the activity under review: what it aims to achieve, how it is organized, how its processes are intended to work, and what has changed. The survey owns the engagement's process list and Process IDs; later workpapers inherit them.

## File Structure

```text
/
└── engagements/
    └── <year>/
        └── <name>/
            └── planning/
                └── preliminary-survey.md
```

Create `planning/preliminary-survey.md` using the structure in [SURVEY-FORMAT.md](SURVEY-FORMAT.md). If the file already exists, update it in place.

## 1. Establish the starting point

Establish why the engagement was commissioned, the initial expectations, and the known boundaries. Prior workpapers can inform the structure and content without establishing current facts.

## 2. Gather and describe the activity

Inspect available material before identifying additional information needs. Useful sources include org charts, policies, procedures, process maps, system documentation, management risk assessments, prior audit reports, and meeting notes.

Explain the activity's objectives, process boundaries, responsibilities, dependencies, and operating environment. Capture management's performance measures and established risk tolerance. Describe governance, risk management, and known control arrangements at a level that supports risk assessment. Record the frameworks and requirements evidenced by the sources, with their known editions.

Label each fact's **basis**: documented, reported, or observed. Preserve differences between bases with their sources; a procedure document shows documented design, not what happens in practice. When a material uncertainty needs a focused discussion or observation, state what it must resolve; walkthroughs can come later.

Record **leads** for risk assessment as the facts emerge: significant changes, dependencies, incidents, management concerns, or unresolved prior findings. Link each lead to its source and to Process IDs when known.

Continue until every section of the format has sourced content, a stated absence or non-applicability, or a named information gap.

## 3. Establish the process list

Draft and review each Process Title and Process Description through `process-statements`, keeping its source references and basis labels.

Preserve Process IDs already established in this engagement, including provisional IDs in downstream workpapers, and resolve conflicting identities before allocating new ones. Allocate new IDs as `P-01`, `P-02`, and so on.

## 4. Report readiness for risk assessment

A portion of the survey is ready for risk assessment when:

- The activity's objectives are sourced and distinguished from the audit objective statement.
- The process list covers the activity as far as current sources show, with boundaries and handoffs clear enough to identify risks.
- Every section of the format has sourced content, a stated absence or non-applicability, or a named information gap.
- Each lead is linked to its supporting facts, or the survey states that none were identified from the material reviewed.
- No open gap prevents understanding the objectives, processes, scale, or material dependencies of that portion.

Report which portions are ready, and which gaps hold back the rest and why. Minor gaps can stay open. Readiness is the basis for risk assessment only; control design and effectiveness are assessed later.

## Refreshing an existing survey

Use an earlier engagement's survey of the same activity as a reference and leave it unchanged. Label carried content without current support as "prior engagement; not reconfirmed" and account for it in readiness. Reconcile Process IDs with those already established for the current engagement.

When processes, objectives, or other material facts change, search the engagement's workpapers for affected references. Record the change in Readiness and handoff and flag the affected risk assessment, planning memo, RCM, or later workpapers for review by their owning skills. Edit only the survey; downstream decisions stand until their owners reconsider them.

## Done

Reply with a brief account of the activity and significant leads, readiness, remaining gaps, and any downstream workpapers flagged for review.
