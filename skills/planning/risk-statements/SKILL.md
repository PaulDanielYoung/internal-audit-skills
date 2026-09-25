---
name: risk-statements
description: Turn a risk, concern, issue, or vague topic into a clear risk statement that explains what could happen, why it could happen, and why it matters. Use when writing, reviewing, improving, or diagnosing risk statements.
---

A risk statement connects an **event** to its **cause** and **consequence** in relation to an **objective**. It answers three questions: what could happen, why could it happen, and why do we care. The **objective** is the thing at stake; it is usually stated as context alongside the statement rather than inside it, and the consequence should make clear how that objective is affected.

A useful starting point is:

> [Event] caused by [cause/s] resulting in [consequence/s].

Split it into two sentences when it runs long:

> [Event] caused by [cause/s]. This may result in [consequence/s].

Adapt the wording to the context. The statement is complete when a reader can point to the event, the cause, and the consequence, and can name the objective the consequence affects.

## Shared context

Use the auditor's chosen workspace root, otherwise the parent of `engagements/` when working beneath it, otherwise the working directory. Read `GLOSSARY.md` there if present and use its definitions for **risk**, **objective**, **event**, **cause**, and **consequence**. Without one, the meanings in the opening paragraph apply.

Read relevant requirements in `METHODOLOGY.md` and relevant facts in `ORGANIZATION.md` when present, consulting referenced sources when needed. Documented methodology governs the wording; the pattern above is a starting point. Proceed without absent context files unless a material question needs resolving.

## When to pause

Before drafting, use `audit-context` when a needed term is missing from an existing glossary, the user's material uses conflicting terminology, or its intended meaning is unclear. Also use it when methodology or organizational context needs updating or clarification; only that skill edits the shared context files. Pass the specific question and available evidence.

Call the Skill tool with "shared-understanding" when material ambiguity about the objective, event, causes, consequences, or intended use of the statement could meaningfully change what you write.

## Faults

Use this section when reviewing, improving, or diagnosing a statement. Each fault names what a sound statement has instead.

* **A cause or control weakness stated as the risk.** A condition such as inadequate staffing, weak access controls, or insufficient monitoring may explain why an event could occur; it is not the whole risk. State the uncertain event and its consequence.

* **A consequence stated as the event.** Financial loss, service disruption, regulatory action, reputational harm, and similar effects are consequences when they arise from an event. Identify what happens first.

* **An issue stated as a risk.** If something has already happened or is certain to occur, it is an issue or existing condition rather than the uncertain event. Use it as context or a cause and identify any remaining uncertain event and consequence.

* **The objective merely negated.** Statements such as "failure to achieve the objective" or "inability to meet requirements" do not explain what could cause that failure. Name the event that would affect the objective.

* **A topic, category, or overly general condition stated as the risk.** Labels such as "cyber risk," "staffing risk," "human error," or "poor controls" do not describe a specific causal chain. State what could happen, why, and with what consequence.

* **Multiple distinct risks combined into one statement.** A statement may have multiple related causes or consequences, but separate distinct event chains when they would be understood, assessed, or managed differently.

* **A cause too vague to explain the event.** Replace generic labels with the specific condition that could give rise to the event when the available information supports it. Do not invent a root cause that is not known.

* **A consequence too vague or disconnected from the objective.** State a plausible effect that explains why the event matters and how an objective would be affected. Prefer specific consequences over generic phrases such as "reputational damage" when greater precision is supported.

* **A broken or circular causal chain.** Each cause should plausibly give rise to the event, and each consequence should plausibly follow from the event. Do not simply restate the same condition in different words.

* **An overloaded statement.** Include the causes and consequences needed to understand the material risk, not every conceivable driver or downstream effect. Split or move supporting detail to context when it obscures the core statement.
