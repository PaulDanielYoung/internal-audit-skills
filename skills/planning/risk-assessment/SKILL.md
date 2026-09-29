---
name: risk-assessment
description: Assess or rate an engagement's inherent risks, identify risks from a preliminary survey, and rank risks for scoping. Use when starting risk assessment after the preliminary survey, or when upstream changes require reassessment.
---

# Risk Assessment

Own the engagement risk assessment at `planning/risk-assessment.md` in the selected engagement, including Risk IDs and activity Objective IDs. Identify, word, and present inherent risks for the auditor to rate. Rank risks for `planning-memo`; scope decisions belong there. List no controls; those belong to the RCM.

## File Structure

```text
/
└── engagements/
    └── <year>/
        └── <name>/
            └── planning/
                └── risk-assessment.md
```

Create `planning/risk-assessment.md` using the structure in [ASSESSMENT-FORMAT.md](ASSESSMENT-FORMAT.md). If the file already exists, update it in place.

## 1. Establish the starting point

Start from the survey and its readiness report. Inspect prior assessments and findings, incidents, management's risk assessments, and auditor-supplied equivalents before asking for more. Prior workpapers can inform structure and candidate risks without establishing current facts.

Cite every factual statement and rating consideration to its source, with its location and known date or version, or give an explicit basis such as a dated auditor statement. Carry the survey's basis labels with its content. General knowledge supplies labelled candidates, never facts about this activity. Minor gaps get bracketed markers in place and Information gaps entries.


## 2. Establish processes and activity objectives

Inherit the survey's Process IDs and process list unchanged. Carry its activity objectives, with their wording, performance measures and targets, and sources, into Activity objectives; distinguish them from the audit objective statement. Carry management's established risk tolerance, or the survey's statement of its absence. Allocate Objective IDs as `O-01`, `O-02`, and so on, and preserve established identities on updates. The assessment owns these IDs; downstream workpapers may cite them, but they add no objective layer to the RCM. Include a process-level objective only when a source states one. Missing objectives remain gaps rather than being inferred from process names.

Without a survey, recommend `preliminary-survey`. If the auditor declines, establish a provisional process list inside this assessment from equivalent material, wording each process through `process-statements`. Preserve existing engagement Process IDs, allocate new provisional `P-nn` IDs above the highest allocated number, and flag the list for the survey to adopt. Pause the whole assessment only when neither objectives nor processes can be established; otherwise draft what is supported, keeping missing links visible and the affected work pending.

## 3. Identify and word risks

Consider candidates in this order: methodology and organization context; the internal audit plan's risk rationale and changes since the plan was approved; survey leads, prior findings, incidents, and management concerns; management's own risk assessments; the auditor; then labelled general-knowledge candidates. Retain a general-knowledge candidate only when a source supports it or the auditor accepts it, recording that source or dated acceptance as its basis. Omit rejected candidates and survey leads that do not become risks.

Give each retained risk one Risk ID (`R-01`, `R-02`, and so on), linked to every Process ID it affects and at least one Objective ID. Draft and review each new or edited Risk Title and Risk Description through `risk-statements`, passing its linked objectives as context and keeping citations, basis labels, and gap markers. Compare descriptions for duplicate event chains; split only where `risk-statements` identifies distinct chains that would be assessed or managed differently. A rating-only change keeps the existing wording review.

### Consider fraud

Consider fraud in every assessment, starting from the survey's fraud indicators. Work through each **fraud scheme**: misappropriation of assets, corruption, fraudulent reporting, and management override of controls. Take each supported scheme through identification, wording, and the rating judgement point like any other risk. Close each scheme with its linked Risk IDs or with the auditor's dated reason that no fraud risk is retained for it.

## 4. Present the rating judgement point

Ratings are **inherent**: consider the activity before controls. For each risk, lay out sourced **likelihood considerations** (such as frequency, volumes, complexity, change, findings, and incidents) and **impact considerations** (such as financial size, regulatory exposure, customers, operations, the linked objective and its performance measures, and management's risk tolerance where established). Include management's own view of likelihood or impact as an attributed consideration, noting where the evidence differs. Show methodology's scale and calibration; absent methodology, show only the bare integer scale 1 to 5 for each dimension, without invented calibration labels. Present no proposed likelihood, impact, score, or band.

Ask the auditor to rate likelihood and impact, and record each rating with its date and reason. Mark a missing date or reason visibly and ask for it rather than inventing a rationale. An undecided dimension stays blank, with score and band blank too. Resolve values outside the scale with the auditor.

Compute Score as Likelihood × Impact and derive Band from the computed score using an executable calculation, never manual entry. Default bands are Low 1–4, Moderate 5–9, High 10–16, Critical 17–25; methodology overrides the rating method and bands. Resolve an incomplete or conflicting method before computing affected results. Recompute after a rating or method change and use the same results in the summary, heat map, and risk entries.

Rank rated risks by band from highest to lowest, then score descending. Use Risk ID order for ties; place unrated risks last in Risk ID order. This mechanical sort is the entire ranking, with no additional priority or scope judgement.

## 5. Check coverage and reconcile with management

Consider compliance, financial reporting, operations and performance, IT and systems, strategy, and third-party risks, or methodology's replacement list. For each topic, link the retained risks or state a sourced reason none applies. This is a coverage check, not a taxonomy or risk field.

Compare the retained risks with management's risk registers, self-assessments, and stated concerns. Record each management-identified risk not retained, with the reason, and each retained risk management has not identified. When management's view is unavailable, record that as a gap.

Where coverage or reconciliation raises a candidate, take it through identification, wording, and the rating judgement point. Unresolved coverage or reconciliation remains a gap.

## 6. Report readiness for the planning memo

The assessment is ready when:

- Every active risk links to a process and an objective.
- Every Risk Title and Risk Description has been through `risk-statements`.
- The auditor has rated every active risk.
- Every fraud scheme is closed.
- The coverage check and management reconciliation are done.
- No open gap could add, remove, or re-rate a risk.

Record each gap's effect in Information gaps, with the returned RQ ID or the question put to the auditor. Questions requiring the auditor's judgement stay in this workpaper. Pause a risk affected by a gap that could add, remove, or re-rate it until the auditor resolves the gap.

## Refreshing an existing assessment

When an earlier assessment of the same activity exists, offer to use it as the starting point. On acceptance, leave the earlier workpaper unchanged and work at the current assessment path, reconciling identities with this engagement's established IDs. Label carried risks "prior engagement; not reconfirmed" until a current source or the auditor reconfirms them. Show prior ratings only as sourced likelihood or impact considerations; leave current ratings, score, and band blank until the auditor rates.

For reassessment after an upstream or RCM flag, move the affected risks' previous ratings into considerations and reopen their current ratings, preserving unaffected current decisions. Treat unresolved currency or upstream changes as gaps against readiness.

## Done

Reply with the output path, readiness against each criterion, undecided risks, remaining gaps and RQ IDs, outstanding methodology requirements, and downstream flags. Recommend `planning-memo`, naming the blockers when not ready. Send no communications.
