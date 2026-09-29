# risk-and-control-matrix.md Format

## Structure

```markdown
# Risk and Control Matrix: <Engagement name>

## Engagement context

> <Audit objective statement, unchanged from ENGAGEMENT.md>

<Engagement objectives, numbered as in the memo. Survey, assessment, and memo
versions this matrix is built on, with dates. Methodology or default basis.>

## Matrix

| Process ID | Risk ID | Risk Title | Band | Control ID | Control Title | Owner | Frequency | Type | Nature | Key | Planned work |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Risks

### <Risk ID>: <Risk Title>

<Risk Description and Band, copied unchanged from the assessment. Process IDs
and engagement objectives it links to. Its key controls, or the auditor's
reason for a gap assessment or direct examination instead.>

## Controls

### <Control ID>: <Control Title>

<Control Description with inline sources. Owner, Frequency, Type, and Nature
with their bases. Risk IDs and Process IDs it addresses.>

**Design considerations:** <Sourced considerations, and where a walkthrough is
needed to settle the design.>

**Key control:** <Key or not key, with the auditor's date and reason, or
undecided.>

**Contrary practice:** <Attributed accounts that differ from the intended
design, or none known.>

#### Design and implementation procedures

<Engagement objectives and criteria served, techniques and tools, and the
assigned auditor.>

1. <Procedure step>

#### Operating-effectiveness procedures

<Population and source, period, sampling method, sample size, and projection
basis, each with its source.>

1. <Procedure step>

## Gap assessments

### <Risk ID>: <Risk Title>

<Why no control is identified. Engagement objectives served and the assigned
auditor.>

1. <Procedure step>

## Direct examination

1. <Procedure, linked to its Risk ID and engagement objective.>

## Objective coverage

| Engagement objective | Criteria | Risk IDs | Planned work |
| --- | --- | --- | --- |

## History

<Retired Control IDs with replacements or "no replacement", and combinations
no longer in scope with their earlier links and planned work, dated.>

## Flags

<Affected workpapers or pending handoffs, naming the affected IDs.>

## Information gaps

<Affected ID or section, whether the gap could materially change planned
work, and the returned RQ ID or question put to the auditor.>

## Sources

<Retained copies used and other stated bases, preserving provenance and
prior-content labels.>
```

## Use of the format

- Keep one matrix row per process–risk–control combination, ordered by the assessment's ranking, then Process ID, then Control ID.
- For a risk with no identified control, write `—` for Control ID and every attribute, and `Control not yet identified` as its Control Title.
- Mark Key as `Key`, `Not key`, or blank while undecided.
- Mark Planned work as `Design`, `Design + OE`, `Gap assessment`, `Direct examination`, or `Context only`.
- Give each control one section, however many rows it appears in. Rows repeat only its matrix fields.
- Omit the operating-effectiveness procedures heading for controls the approach does not test for operating effectiveness.
- Use plain ID mentions for retired IDs in History.
