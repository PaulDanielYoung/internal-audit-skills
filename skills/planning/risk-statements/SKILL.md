---
name: risk-statements
description: Turn a risk, concern, issue, or vague topic into a clear risk statement that explains what could happen, why it could happen, and why it matters. Use when writing, reviewing, improving, or diagnosing risk statements.
---

A risk statement connects an **event** to its **cause** and **consequence** in relation to an **objective**: what could happen, why it could happen, and why we care. The objective is the thing at stake, usually stated as context beside the statement rather than inside it. Write or review the statement, returning wording to the auditor or calling skill.

## Starting pattern and completeness

A useful starting point is:

> [Event] caused by [cause/s] resulting in [consequence/s].

Split it into two sentences when it runs long:

> [Event] caused by [cause/s]. This may result in [consequence/s].

Adapt the wording to the context. A statement is complete when a reader can point to:

- **Event:** the uncertain thing that could happen.
- **Cause:** the specific condition that could give rise to it.
- **Consequence:** the plausible effect that shows how the objective is affected.
- **Objective:** what is at stake, named in the statement or its context.

## Shared context and gaps

Read the workspace glossary, if present, and use its definitions for risk, objective, event, cause, and consequence; without one, the meanings above apply. Read the relevant methodology and organization context too, and proceed silently when absent. Documented methodology governs the wording; the pattern above is a starting point.

Use `audit-context` when a needed term is missing from an existing glossary, terminology is contested or unclear, or persistent methodology or organization context needs updating or clarification. Pass the specific question and available evidence.

Call the Skill tool with `shared-understanding` when material ambiguity about the objective, event, causes, consequences, or intended use of the statement could change the wording. Mark missing facts in place with bracketed gaps, such as `[cause not established]` or `[objective not identified]`; use only causes, events, and consequences the available information supports. Preserve the caller's gap markers, source links, and basis labels.

## Faults

Use these when reviewing, improving, or diagnosing. Each fault names what sound wording has instead.

- **A cause or control weakness stated as the risk.** Conditions such as weak access controls or insufficient monitoring explain why an event could occur; state the uncertain event and its consequence.
- **A consequence stated as the event.** Financial loss, service disruption, regulatory action, and reputational harm are effects; identify the event they follow from.
- **An issue stated as a risk.** Something that has happened or is certain to occur is an existing condition; use it as context or a cause and state the remaining uncertain event and consequence.
- **The objective merely negated.** "Failure to achieve the objective" names no cause; name the event that would affect the objective.
- **A topic or category stated as the risk.** Labels such as "cyber risk" or "human error" describe no causal chain; state what could happen, why, and with what consequence.
- **Multiple distinct risks combined into one statement.** Related causes or consequences may share a statement; separate event chains that would be understood, assessed, or managed differently.
- **A cause too vague to explain the event.** Replace generic labels with the specific condition the available information supports, marking a gap when it supports none.
- **A consequence too vague or disconnected from the objective.** State the plausible effect that shows why the event matters and how the objective is affected, preferring specifics over generic phrases where supported.
- **A broken or circular causal chain.** Each cause plausibly gives rise to the event and each consequence plausibly follows from it, with each link adding a distinct condition.
- **An overloaded statement.** Include the causes and consequences needed to understand the material risk; split or move supporting detail to context when it obscures the core.

## Review output

Check the pattern and every completeness element as well as the faults. For several statements, also compare pairs for the same event chain stated twice or one risk split across statements.

Name each fault found using the names above, explain any other unmet requirement, and propose a revised statement for affected wording. Preserve gap markers, source links, and basis labels in the revisions. Confirm sound wording and leave it unchanged, without rewriting for style.
