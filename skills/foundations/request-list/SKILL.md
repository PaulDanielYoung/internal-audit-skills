---
name: request-list
description: Create, seed, reconcile, or maintain engagement information requests across audit phases, including receipt, withdrawal, and follow-up. Use also to draft initial or additional request messages and reminders.
---

# Request List

Own the engagement's shared information-request list and its lifecycle across planning, walkthroughs, fieldwork, and later phases. Record information needs supplied by the auditor or a substantive skill; deriving an information-needs program belongs to that substantive work. Each row represents one deliverable requested from a party outside the engagement team. Auditor-only questions stay in the owning artifact's Information gaps.

## Establish the basis

Follow the workspace instructions for engagement selection and read its `ENGAGEMENT.md`. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Documented methodology governs. Use `audit-context` for missing or contested terms and persistent context changes. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names, paths, columns, and ID prefixes fixed. Surface conflicting methodology requirements for resolution with the auditor.

Inspect both engagement-root `request-list.md` and `planning/request-list.md`. Continue the planning-level list in place if it is the only existing list; create new lists at the engagement root. If both exist, reconcile them with the auditor before changing either or creating another. State the selected engagement and list path once settled.

Read [LIST-RULES.md](LIST-RULES.md) before interpreting or changing rows. Accept the supplied deliverable, period/version, addressee if known, needing artifact/section or workstream, and candidate source links. Preserve unknown details as visible gaps; use `shared-understanding` only for material ambiguity, or ask directly if unavailable. Pause only the affected work until the request or decision is clear.

## Perform the requested work

- **Create, seed, add, or reconcile:** check retained engagement sources and existing rows using the matching rules in LIST-RULES.md before allocating an ID. Resolve each need to sufficient retained material, a matching row, a new Proposed row, or an explicit unresolved decision.
- **Update, withdraw, or record sending:** apply the lifecycle rules in LIST-RULES.md while preserving wording and history. Report missing confirmations or dates as outstanding, without inferring a state change.
- **Receive material:** read [RECEIPT.md](RECEIPT.md) for retention, auditor-confirmed matching, partial responses, and provenance handoff.
- **Draft an initial/additional request or reminder, or record a reminder sent:** read [MESSAGES.md](MESSAGES.md). Produce messages on demand in the reply only.

For combined requests, complete authorized list changes before rendering messages from those rows. Management notification is a workflow default: when management has not been notified, briefly note that initial requests normally follow or accompany notification, then proceed. Request preparation and use of this skill are independent of `engagement-notification`.

## Return the handoff

Search affected engagement artifacts across all phases for the relevant RQ references and combine those locations with Needed by. Return matched or created IDs, retained-source links, unresolved matches, remaining information gaps, and affected artifact/section or workstream references. The substantive skill refreshes only its own artifact; this skill neither edits another skill's workpaper nor decides its readiness. Closing a row does not establish that its substantive information gap is resolved.

Completion means each supplied need or requested change has an accounted-for outcome under the rules, the authorized changes are saved, and outstanding decisions or confirmations are explicit. State the list path, changes made (or that none were made), and what remains unresolved. Keep internal assumptions, sources, methodology basis, and gaps outside any communication.

## Contract for calling skills

The auditor or substantive skill decides needs and passes the deliverable, period/version, addressee if known, needing artifact/section or workstream, and candidate source links. Invoke `request-list` for authorized creation, changes, or requested message drafting; recommend it for an optional next step. The caller or auditor decides uncertain substantive source sufficiency.

In a single-skill install where `request-list` is unavailable, the caller returns those precise needs and affected references as a handoff, explicitly states that the list has not been updated, and keeps the information gap visible. The caller never edits the request table as a fallback.
