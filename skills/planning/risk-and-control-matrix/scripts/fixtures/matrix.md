# Preliminary RCM — purchasing

Upstream snapshots: [Survey v2](preliminary-survey.md), [Assessment v3](risk-assessment.md), and [Memo v1](planning-memo.md), received 2026-09-26. Methodology basis: default 1–5 inherent ratings and standard Type/Nature lists.

| Process ID | Process Title | Process Description | Risk ID | Risk Title | Risk Description | Inherent Risk Likelihood Rating | Inherent Risk Impact Rating | Inherent Risk Score | Risk Band | Control ID | Control Title | Control Description | Control Owner | Frequency | Control Type | Control Nature | Planned Procedures |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P-02 | Invoice payment | Pay approved invoices. | R-01 | Unauthorized purchase | Unauthorized purchases cause financial loss. | 4 | 5 | 20 | Critical | C-01 | Purchase approval | Manager checks A \| B & <limits> before approval per [Policy §2](../sources/policy.pdf#page=2). | Purchasing manager | Per purchase | preventive | manual | 1. Inspect the policy's approval criteria.<br>2. Trace a purchase through approval and compare its approver and amount to those criteria. |
| P-01 | Purchase ordering | Request and approve purchases. | R-02 | Duplicate order | Duplicate orders cause excess expenditure. | 2 | 3 | 6 | Moderate | C-02 | Duplicate check | System compares supplier and order reference before release per [Design](../sources/design.pdf). | [Owner pending] | Per order | detective | automated | 1. Inspect the matching configuration.<br>2. Walk through a duplicate order against the documented matching rules. |
| P-01 | Purchase ordering | Request and approve purchases. | R-01 | Unauthorized purchase | Unauthorized purchases cause financial loss. | 4 | 5 | 20 | Critical | C-01 | Purchase approval | Manager checks A \| B & <limits> before approval per [Policy §2](../sources/policy.pdf#page=2). | Purchasing manager | Per purchase | preventive | manual | 1. Inspect the policy's approval criteria.<br>2. Trace a purchase through approval and compare its approver and amount to those criteria. |
| P-01 | Purchase ordering | Request and approve purchases. | R-03 | Unrecorded order | Unrecorded orders prevent timely fulfillment. | [Rating pending] | Unknown | | TBD | | Control not yet identified | | | | | | 1. Ask the process owner how unrecorded orders are detected.<br>2. Inspect any supplied design evidence against the risk of unrecorded orders. |

## Information gaps

- [RQ-01](../request-list.md#RQ-01): confirm the owner of [the duplicate check](#C-02).
- Confirm gap-assessment evidence for [unrecorded orders](#R-03).

## Flags

- Refresh procedures for [purchase ordering](#P-01) when the policy changes. Retired R-99 has no replacement.
