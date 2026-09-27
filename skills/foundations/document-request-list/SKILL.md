---
name: document-request-list
description: Create, seed, reconcile, or maintain engagement information requests across audit phases, including receipt, withdrawal, and follow-up. Use also to draft initial or additional request messages and reminders.
---

# Request List

Own the engagement's shared information-request list and its lifecycle across planning, walkthroughs, fieldwork, and later phases. Record information needs supplied by the auditor or a substantive skill; deriving an information-needs program belongs to that substantive work. Each row represents one deliverable requested from a party outside the engagement team. Auditor-only questions stay in the owning artifact's Information gaps.

## Establish the basis

Follow the workspace instructions for engagement selection and read its `ENGAGEMENT.md`. Read the workspace glossary and relevant methodology and organization context when present; proceed silently when absent. Documented methodology governs. Use `audit-terminology` for missing, ambiguous, or contested terms and settled definitions. Use the glossary's artifact name in prose and headings, noting the repo term once; keep skill names, paths, columns, and ID prefixes fixed. Surface conflicting methodology requirements for resolution with the auditor.

The list lives at `document-requests/document-request-list.md` in the engagement folder. If an older `request-list.md` exists at the engagement root or in `planning/`, ask the auditor before moving it or creating another. State the selected engagement and list path once settled.

Read [LIST-RULES.md](LIST-RULES.md) before interpreting or changing rows. Accept the supplied deliverable, period/version, addressee if known, needing artifact/section or workstream, and candidate source links. Preserve unknown details as visible gaps; use `shared-understanding` only for material ambiguity, or ask directly if unavailable. Pause only the affected work until the request or decision is clear.

## Perform the requested work

- **Create, seed, add, or reconcile:** check retained engagement sources and existing rows using the matching rules in LIST-RULES.md before allocating an ID. Resolve each need to sufficient retained material, a matching row, a new Proposed row, or an explicit unresolved decision.
- **Update, withdraw, or record sending:** apply the lifecycle rules in LIST-RULES.md while preserving wording and history. Report missing confirmations or dates as outstanding, without inferring a state change.
- **Receive material or finish receipt provenance:** read [RECEIPT.md](RECEIPT.md) for delegation to `engagement-sources`, auditor-confirmed matching, partial responses, and recovery of unfinished provenance updates.
- **Draft an initial/additional request or reminder, or record a reminder sent:** read [MESSAGES.md](MESSAGES.md). Produce messages on demand in the reply only.

For combined requests, complete authorized list changes before rendering messages from those rows. Management notification is a workflow default: when management has not been notified, briefly note that initial requests normally follow or accompany notification, then proceed. Request preparation and use of this skill are independent of `engagement-notification`.

## Return the handoff

Own discovery of explicit RQ references for the handoff. Search engagement artifacts across all phases for the relevant RQ IDs and combine those locations with Needed by, including references found outside the listed needs. Return matched or created IDs, retained-source links, unresolved matches, remaining information gaps, and affected artifact/section or workstream references.

If any artifacts cannot be inspected, return the known references and identify what could not be inspected and why. Distinguish an incomplete search from a completed search with no references found; keep these limitations visible in the handoff.

The substantive skill uses the returned references without repeating the RQ search, interprets the information for additional substantive impacts, flags other owners' work, and refreshes only its own artifact. It can continue supported work while keeping potentially affected work unresolved where search limitations remain. This skill neither edits another skill's workpaper nor decides its readiness. Closing a row does not establish that its substantive information gap is resolved.

Completion means each supplied need or requested change has an accounted-for outcome under the rules, the authorized changes and required receipt provenance updates are saved, and outstanding decisions or confirmations are explicit. State the list path, changes made (or that none were made), and what remains unresolved, including unfinished retention or provenance updates. Keep internal assumptions, sources, methodology basis, and gaps outside any communication.

## Contract for calling skills

The auditor or substantive skill decides needs and passes the deliverable, period/version, addressee if known, needing artifact/section or workstream, and candidate source links. Invoke `document-request-list` for authorized creation, changes, or requested message drafting; recommend it for an optional next step. The caller or auditor decides uncertain substantive source sufficiency.

In a single-skill install where `document-request-list` is unavailable, the caller returns those precise needs and affected references as a handoff, explicitly states that the list has not been updated, and keeps the information gap visible. The caller never edits the request table as a fallback.
