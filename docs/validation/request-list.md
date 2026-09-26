# Request-list validation

Behavioral dry runs for [issue #45](https://github.com/PaulDanielYoung/internal-audit-skills/issues/45), performed 2026-09-26.

An independent agent interpreted the skill against an isolated temporary auditor workspace with workspace instructions, shared context, an engagement record, retained sources, and planning and fieldwork artifacts. It enacted 24 scenarios, saved list mutations and replies, and checked the resulting artifacts. This is a model-enacted dry run, not execution through an installed Claude skill runtime or a repeated-run reliability evaluation.

## Observed outcomes

| Scenarios | Outcome |
| --- | --- |
| Cold entry before notification; initial message | Created root list with nine columns and Proposed deliverables; drafting selected only Proposed rows and changed no state. Notification prompted a brief workflow note without blocking. |
| Cross-phase reuse | Reused RQ-01 and appended fieldwork references without changing the request wording. |
| Highest unsent withdrawal; subsequent allocation | Preserved RQ-02 as Withdrawn with Requested blank; allocated RQ-03 next. |
| Missing sent date; confirmed sending; sent withdrawal | Missing date left rows Proposed. Confirmation recorded 2026-09-20; withdrawal preserved the date and wording. |
| Reminder draft and confirmed follow-up | Draft selected only outstanding Requested rows and changed no state; confirmation added 2026-09-24 to Notes while preserving the original sent date. |
| Confirmed partial response; reference search and provenance handoff | RQ-01 became Received with a retained April-May source; new Proposed RQ-04 requested June, carrying both phase references and reciprocal Notes references. Handoff returned the remaining gap and provenance ID without editing workpapers or source index. |
| Uncertain retained-source period | Left source sufficiency unresolved for the caller/auditor without silently suppressing the need. |
| Matching Withdrawn and Not available items | Preserved closed rows and surfaced prior outcomes for auditor decision; no duplicate or reopened row. Unavailability recorded who said so and when. |
| Unretained attachment; undocumented verbal response; missing receipt confirmation | Left receipt outstanding until retention, dated notes, and the relevant auditor confirmation were available. |
| Unrequested material | Returned normal retention handoff without changing the request list. |
| Legacy planning-only list | Appended RQ-08 in place without creating an engagement-root list. |
| Both list locations present | Changed neither list pending auditor reconciliation. |
| Clearly sufficient retained material | Cited the vendor master without allocating a request. |
| Different period | Allocated separate Proposed RQ-06 for July. |
| Auditor-only question | Kept sample-size decision in the owning artifact's information gaps, off the external request list. |

No behavioral failures or instruction ambiguities emerged in these scenarios. Final main-fixture IDs were RQ-01 through RQ-06 in numeric order, with withdrawn rows preserved and June still an explicit gap.

## Packaging checks

- `claude plugin validate . --strict`: passed (the CLI selected the marketplace manifest).
- Skill creator's `quick_validate.py skills/foundations/request-list`: passed.
- All 11 shipped skill directories are listed in the plugin manifest; the new category and top-level README links resolve.
- `git diff --check`: passed.
- Maintainer skill links refreshed successfully for all 11 skills.

Additional direct validation of `.claude-plugin/plugin.json --strict` reported the existing root `CLAUDE.md` warning: plugin-root project instructions are not loaded into installed projects. This repository file was unchanged by the issue; the additional strict check did not pass.
