# Planning-memo validation

Dry runs for [issue #39](https://github.com/PaulDanielYoung/internal-audit-skills/issues/39), performed 2026-09-26 against the new [skill](../../skills/planning/planning-memo/SKILL.md) and the existing request-list contract.

These are manual, model-enacted walkthroughs by the implementing agent. The inputs and resulting workpaper/handoff excerpts are recorded below. They are not independent agent tests, installed Claude runtime executions, or repeated-run reliability measurements. No real engagement or request list was changed.

## Scope and readiness walkthrough

The fictional engagement record supplies the audit objective statement “Assess purchasing authorization.” The survey supplies P-01 Purchasing, P-02 Payments, and P-03 Reporting (no risks), with activity objective O-01 linked through the assessment. The assessment supplies this ranked input:

| Risk ID | Risk Title | Process IDs | Band | Score |
| --- | --- | --- | --- | --- |
| R-02 | Unauthorized payments | P-01, P-02 | Critical | 20 |
| R-01 | Unauthorized purchasing | P-01 | High | 12 |
| R-03 | Duplicate payments | P-02 | Moderate | 6 |

Retained `sources/prior-findings.md` records an authorization exception; `sources/assurance.md` records purchasing coverage by another engagement; `sources/policy.md` contains dated authorization criteria. These filenames are fictional fixture references, not shipped source documents.

The first scope draft preserved R-02, R-01, R-03 order, their titles, links, and bands. It cited the authorization exception and other assurance coverage as considerations. All risk and process In/Out cells remained blank. P-03 had its own undecided process row. No risk description, rating, or process was rewritten. Readiness was **not ready**: scope and objective agreement were outstanding.

The next input supplied these auditor decisions dated 2026-09-26: P-01 Out because the other engagement covers purchasing; P-02 In because payments are the focus; P-03 Out because reporting is outside the assignment; R-02 Out because the other engagement covers the shared authorization risk; R-03 In because duplicate payments remain within the assignment. The resulting scope excerpt was:

| Risk ID | In/Out | Recorded basis |
| --- | --- | --- |
| R-02 | Out | Auditor's separate shared-risk decision, other engagement coverage, 2026-09-26 |
| R-01 | Out | Solely linked to excluded P-01; purchasing coverage reason and process decision date retained |
| R-03 | In | Auditor's duplicate-payments decision and reason, 2026-09-26 |

Before the separate R-02 decision arrived, excluding P-01 left R-02 undecided. Exclusions listed R-02 (Critical) and R-01 (High) first, then the remaining process exclusions, including P-03. This checked both the shared-risk boundary and explicit treatment of a process with no risks.

The auditor then agreed objective 1, “Conclude whether duplicate payments are prevented or detected,” linking O-01 and R-03, with agreement date and basis. Criteria cited the supplied policy; the summary approach named inspection and data analytics without procedures or sample sizes. Period, entities, and systems were supplied and decided. With topical applicability settled and no scope-changing gaps, readiness became **ready for the RCM**, even though the team, budget, and timeline remained bracketed gaps. The assignment statement remained unchanged.

## Additional branches

Each row is a separate variation of the preceding fixture, so a gap introduced in one row does not carry into another.

| Scenario and input | Result of walkthrough |
| --- | --- |
| No assessment; auditor declines the recommendation | Recommended `risk-assessment`, then produced process scope using P-01 through P-03 only. Risk table said “pending the risk assessment”; risk and Objective ID links stayed pending. Reported not ready without inventing risks or processes. |
| Prior engagement memo with decided scope and a 100-hour budget | Retained the earlier memo as a reference, kept current scope blank, and cited prior scope only as considerations. Prior budget stayed labelled as prior; the earlier memo was not refreshed. |
| Methodology supplies two topical requirements with retained sources | Presented survey topic links and in-scope risks for each, leaving applicability undecided. After auditor input, recorded one as covered here with objective 1 and one as covered elsewhere with its engagement reference and decision date. |
| Methodology has no list | Asked the auditor once and offered `audit-context`. An unanswered question stayed a gap. An explicit “we do not apply a list” became a one-line statement; a later memo update reused that recorded answer. No catalog was introduced. |
| Listed requirement excluded; criterion source has no edition date | Recorded the auditor's exclusion rationale and date. Kept the dependent criterion open with an auditor-only “obtain dated edition” gap, without an external fetch or request-list item. Readiness depended on whether that gap could change scope or objectives. |
| No budget from any allowed source | Budget remained `[Budget not supplied]`, with an Information gaps entry. It did not block an otherwise decided RCM handoff. |
| Budget 100 hours; phases 20, 50, 20; milestones 2026-11-05 then 2026-10-20 | Calculated 90 phase hours, reported the 10-hour discrepancy and reversed milestones, and preserved the supplied values. Resource inconsistencies remained visible without independently blocking RCM readiness. |
| Methodology requires independence declaration, materiality, and audit risk model | Listed the declaration outstanding with its methodology source; did not draft it. Presented the latter two as undecided judgement points with no proposed values. With no such methodology, all three were omitted. |
| R-03 re-rated; new R-04; R-01 retired and replaced by R-05 | R-03 said “needs re-decision”, with its prior In, reason, and date retained as history. New R-04 and R-05 were undecided; retired R-01 showed replacement R-05. Unaffected R-02 retained its current decision. Readiness became not ready, with an RCM flag and no downstream edit. |
| RCM flags an in-scope risk with no in-scope control | Returned the affected risk's scope to the auditor and kept control scope with the RCM. No proposed exclusion or control decision was supplied. |

## Request-list handoff walkthroughs

The external need was “Other assurance coverage report for purchasing, April–June 2026”, addressed to the assurance lead, needed by `planning/planning-memo.md / Scope`. The candidate retained source was `sources/coverage-undated.md`, whose period was uncertain.

1. **Existing open match:** supplied the deliverable, period, addressee, needing section, and candidate source to `request-list`. Under its contract, existing Requested RQ-07 gained the memo's Needed by reference; wording and state stayed unchanged and no duplicate row was created. The memo recorded returned RQ-07.
2. **Uncertain sufficiency:** inspection could not establish the candidate source's period. The memo retained the gap and asked the auditor whether it covered April–June rather than treating it as satisfaction. The scope decision dependent on that coverage remained pending.
3. **Cold entry:** with no list and no notification sent, the same authorized need went to `request-list`, which could create its root list and return RQ-01. The memo recorded that return without requiring notification or inventing its own RQ ID.
4. **Confirmed partial response:** retained and indexed `sources/coverage-apr-may.md` before passing its link and proposed match to RQ-07. With auditor confirmation, the request-list contract returned RQ-07 for the received portion and Proposed RQ-08 for June. The memo's remaining gap became “June coverage outstanding — RQ-08”, keeping the received portion linked. Source provenance gained RQ-07. A fieldwork reference to RQ-07 was flagged in the reply, with its workpaper unchanged.
5. **Closed remainder:** changing RQ-08 to Not available or Withdrawn did not resolve the June coverage gap or a dependent scope decision.
6. **Unavailable dependency:** returned the concrete deliverable, April–June period, assurance lead, memo Scope reference, and candidate retained link with “The request list has not been updated.” Kept the gap visible and made no table edit. Requested messages and reminders were routed to the same dependency rather than drafted by the memo skill.

## Packaging and vocabulary

- `claude plugin validate . --strict`: passed; the CLI selected the marketplace manifest.
- Skill creator's `quick_validate.py skills/planning/planning-memo`: passed with `python -X utf8` and PyYAML installed in an OS temporary directory. The existing Python environments lacked PyYAML; the validator also needed explicit UTF-8 on Windows.
- All 14 shipped skill directories match the plugin manifest; both new README links resolve.
- Maintainer skill links refreshed successfully for all 14 skills.
- `git diff --check`: passed.
- `CONTEXT.md` reviewed: the skill uses the existing planning artifact, judgement point, information gap, stable ID, and flag constructs. Organization-owned terms remain in the workspace glossary; no new repo construct required an entry.
- The additional direct check `claude plugin validate .claude-plugin/plugin.json --strict` reports the existing plugin-root `CLAUDE.md` warning and fails strict mode. That unchanged maintainer-instructions file is not loaded into installed projects; the required directory-level command passes.
