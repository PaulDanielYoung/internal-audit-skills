---
name: exploratory-data-analysis
description: Explore a dataset an auditor has received and show what is in it as an HTML page with charts. Use when the user shares or names a data file (CSV, Excel, JSON) and wants to understand, summarize, profile, or sanity-check it.
---

Show the auditor what is in a dataset: its shape, its quality, how values are distributed, and what stands out. The page is for looking, not for testing: it describes the data and draws no conclusion about any control.

## Process

### 1. Settle what the data is

Find the facts yourself first: open the file, read the header and a few rows, list the sheets. Then call the Skill tool with "shared-understanding" when any of these is unclear:

- what one row represents (an invoice, a journal line, a user, a change)
- which file, sheet, or header row holds the data when there are several
- the period the data is meant to cover
- which date says when things happened, and which amount matters, when the file offers several and the obvious choice is wrong

A single sheet with a clear header and obvious date and amount fields needs no questions.

### 2. Profile

Run `scripts/profile.py <file>` from this skill's directory (`--help` lists the options for sheet, delimiter, encoding, and row limit). It uses only the Python standard library; XLSX needs `openpyxl`. It writes `<stem>-eda/profile.json` beside the file and prints a summary.

Read the summary, then the JSON. Every number on the page comes from the JSON: aggregates, at most five sample values per field, personal-looking fields masked. Raw rows stay in the source file.

### 3. Render

Write `<stem>-eda/report.html` following [HTML-REPORT.md](HTML-REPORT.md). Open it for the user (`xdg-open` on Linux, `open` on macOS, `start` on Windows) and tell them the absolute path.

The page is complete when every field has a card, every chart has its data table, and the flag list matches the JSON.

### 4. Point at what stands out

In the conversation, name the three to five things most worth the auditor's attention: a spike month, a dominant counterparty, weekend activity, a gap in a sequence, blank-heavy fields, values that differ only by case. Each is an observation about the data. Then ask which they want to look into.
