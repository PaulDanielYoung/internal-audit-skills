---
name: risk-and-control-matrix
description: Build or update an engagement's risk and control matrix (RCM) and work program for its in-scope risks. Use when the planning memo has set scope, when linking controls to a testing approach, or when upstream changes require an update.
---

# Risk and Control Matrix (RCM)

Link each in-scope risk to the controls that address it and plan how each control will be assessed, so the engagement tests what matters most. Assessing control design during planning identifies the key controls to carry into operating-effectiveness testing. The matrix is the engagement's work program. It owns the engagement's Control IDs, and leaves risks and scope to the risk assessment and planning memo.

## File Structure

```text
/
└── engagements/
    └── <year>/
        └── <name>/
            └── planning/
                └── risk-and-control-matrix.md
```
Create `planning/risk-and-control-matrix.md` using the structure in [MATRIX-FORMAT.md](MATRIX-FORMAT.md). If the file already exists, update it in place.

## 1. Establish the starting point

Start from the planning memo and its readiness report, with the risk assessment and survey behind it. Inspect applicable policies and procedures, attributed management and auditor accounts, and any prior RCM before asking for more. Prior workpapers can inform structure and candidate controls without establishing current facts.

Cite every factual statement to its source, with its location and known date or version, or give an explicit basis such as a dated auditor statement. Carry upstream basis labels with their content. General knowledge supplies labelled context, never facts about this activity. Minor gaps get bracketed markers in place and Information gaps entries.

## 2. Establish the included risks

Include the memo's in-scope risks with their in-scope processes. Copy Process ID, Title, and Description from the survey and all risk fields from the assessment without rewording or rating them, recording each upstream workpaper's version. Refer scope conflicts to the planning memo, new risks and risk wording or ratings to the risk assessment, and process problems to the survey; the matrix inherits their changes once settled.

Without a memo, recommend `planning-memo`. If the auditor declines, draft for all assessed risks with scope pending. Pause the whole matrix only when neither processes nor risks can be established; otherwise draft what is supported.

## 3. Identify and describe controls

For each included risk, identify the intended control activities supported by policy, procedure, or an attributed management or auditor account. A requirement alone does not establish a control. Draft and review each Control Title and Control Description through `control-statements`. Record Owner, Frequency, Type (preventive, detective, directive, or corrective), and Nature (manual, automated, or IT-dependent) from supported material, leaving unsupported attributes visibly unknown.

Record the intended design. Keep known contrary practice in attributed prose linked by Control ID, as material for walkthroughs rather than a finding.

When a risk has no identified control, add a "Control not yet identified" row with no invented Control ID, description, or attributes. Missing information is not a design deficiency.

### Stable Control IDs

Allocate `C-01`, `C-02`, and so on above the highest allocated number, including retired IDs. A control shared across risks and processes keeps one ID and one section, with identical matrix fields wherever it repeats. Settle splits and merges with the auditor; each resulting control gets a new ID, and old IDs are retired with their replacements or "no replacement". Never renumber or reuse IDs.

## 4. Assess design and identify key controls

For each control, present sourced **design** considerations from its intended design: how it addresses the risk, its precision and timing, its coverage of the population, and its dependencies on information, systems, or other controls. Note where documentation alone cannot settle the design and a walkthrough is needed. Present no proposed conclusion.

Ask the auditor to designate the **key controls** relied on to address each in-scope risk, and record each designation with its date and reason. Check that every in-scope risk has at least one key control, a planned gap assessment, or the auditor's reason for direct examination instead. Other controls stay in the matrix as context.

## 5. Plan the work program

For each key control, draft design and implementation procedures through `design-adequacy-procedures`. Where the memo's approach calls for operating-effectiveness conclusions, add procedures through `operating-effectiveness-procedures`, with population, period, sampling method, sample size, and projection basis from the auditor or methodology. For each risk without an identified control, plan gap-assessment procedures attached to its Risk ID. Keep auditor-selected direct examination of transactions or outcomes in a numbered section linked to its Risk ID and engagement objective.

Link each procedure set to the engagement objectives and criteria it serves, and name its techniques, tools or analytical procedures, and the assigned auditor where known. Check that every engagement objective has planned work.

## 6. Report readiness for walkthroughs

The matrix is ready for walkthroughs when:

- Every included risk has a key control, a planned gap assessment, or direct examination with the auditor's reason.
- Every control description has been through `control-statements`.
- Every key control has reviewed design and implementation procedures, and operating-effectiveness procedures with a sampling basis where the approach requires them.
- Every engagement objective has planned work.
- Shared controls are consistent wherever they repeat.
- No open gap would materially change planned work.

Record each gap's effect in Information gaps, with the returned RQ ID or the question put to the auditor.

## Updating the matrix

On updates, compare current survey, assessment, and memo versions with those recorded in the matrix. Refresh inherited fields consistently across every row. Add newly included risks with "Control not yet identified" rows until controls are supported. Move combinations no longer in scope to dated history, preserving their links and planned work. Search engagement workpapers across phases for affected IDs and flag them. Edit only this matrix; upstream wording, ratings, objectives, and scope stay with their owners.

## Done

Reply with the output path, readiness against each criterion, undecided key-control designations, remaining gaps and RQ IDs, outstanding methodology requirements, and flags. Recommend walkthroughs, naming the blockers when not ready.
