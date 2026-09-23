---
name: shared-understanding
description: Resolve ambiguity with the user before making a judgment or producing work. Use when missing context, assumptions, preferences, or decisions could change the result.
---

Interview the user until you reach a shared understanding.

Find the facts yourself first: read the available files, tools, policies, and other evidence before asking the user for anything you can determine on your own. The **decisions** are the user's; put each to them.

Identify the unresolved questions and ask them one at a time. Ask **foundational** questions first: a question whose answer depends on another still-open question waits until that one is settled.

For each question, give a recommended answer and briefly explain your reasoning. Make the recommendation specific enough that the user can accept it, modify it, or choose another option.

Format each question like so:

❓ **Q1** - **{question title}**

{question body, might be multiple paragraphs, including multiple choices}

➡️ **Recommended answer**

{your recommended answer, keep it brief and explain your reasoning}

After each answer, reassess what remains unresolved. The user's answer may settle other questions, introduce new ones, or change which question should come next.

When supporting material would settle a question or remove an important assumption, name the specific kind that would help (a methodology, policy, procedure, spreadsheet, report, prior workpaper, meeting notes) and invite the user to share it. Let them answer the underlying question directly instead if they prefer.

The session is done when every row of the following table is either stated by the user or written down as an assumption they have confirmed. Then summarize the shared understanding in this two-column Markdown table:

| Area                | Shared understanding |
| ------------------- | -------------------- |
| **Objective**       | {the objective of the work} |
| **Context**         | {the relevant context} |
| **Decisions**       | {the key decisions} |
| **Assumptions**     | {the assumptions you are relying on} |
| **Constraints**     | {the constraints} |
| **Expected output** | {the expected output} |

Keep each cell concise but specific enough to capture what was agreed. Separate multiple items in a cell with semicolons. After the table, ask the user to confirm the shared understanding before proceeding.
