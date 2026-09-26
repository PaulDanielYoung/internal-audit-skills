# Receipt and source handoff

`engagement-sources` owns source retention and provenance. A receiving substantive skill may invoke it before passing retained-source links and proposed RQ matches here. Use those retained links when supplied.

When invoked directly with unretained material, invoke `engagement-sources` with the material and known original location and receipt date. For a verbal answer, have it retain a dated, attributed note of the supplied account. Keep receipt outstanding until it confirms retention and returns the source link; an unretained attachment is not a received-source link. Route unrequested material through the same skill without creating or changing a request row.

If `engagement-sources` is unavailable, continue supported work using already-retained material. Return a concrete handoff for new retention or provenance updates with the material or retained links, known receipt details, and affected RQ references, explicitly stating what was not performed. Keep that work outstanding; do not write retained sources or their index as a fallback.

Propose the retained-source match and obtain auditor confirmation before marking a row Received. An auditor's explicit confirmation already supplied in the conversation is sufficient. Put uncertain entity, period, version, or substantive sufficiency to the caller or auditor rather than treating a possible match as satisfaction.

For a confirmed full response, mark the row Received and link the retained source in Received. For a confirmed partial response:

1. Mark the original Received and link the retained response.
2. Create a new Proposed row for the remainder under LIST-RULES.md, carrying applicable Needed by references. Link both IDs reciprocally in Notes and describe the supplied portion and remaining need.
3. Return the remaining information gap, new ID, retained-source link, and affected references. Receipt of the original is not satisfaction of all its needs.

After recording a confirmed response, invoke `engagement-sources` with the retained-source link, actual request-list path, RQ ID, and auditor-confirmed match to add the provenance backlink. Include the receipt details identifying the supplied portion where needed. It owns that index update; the receiving substantive skill consumes the result.

If the backlink update fails or its skill is unavailable, preserve the valid Received state and any existing remainder item. Report the unfinished provenance update and retry only that update, without creating another receipt or remainder item. Keep the overall handoff incomplete until the required provenance update succeeds, while reporting saved list changes separately. Include remaining gaps, provenance limitations, and affected references in the handoff required by SKILL.md; the owning skills update their own artifacts.
