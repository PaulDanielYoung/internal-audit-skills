# Markdown RCM contract

This renderer is the implementation for issue #34. The planning stage skill ships separately in #40; this folder is not yet a listed skill. That skill should read this contract before writing or regenerating the preliminary RCM.

Run with Python 3.10+ (standard library only):

```text
python "<skill directory>/scripts/render_rcm.py" "<engagement>/planning/risk-and-control-matrix.md"
```

The script validates the whole document, atomically replaces the sibling `risk-and-control-matrix.html`, and opens it using `Start-Process` on Windows, `open` on macOS, or `xdg-open` on Linux, following exploratory-data-analysis. `--no-open` writes without launching a browser. Validation errors name their category and location, return exit code 1, and leave any existing HTML unchanged. A browser launch failure returns exit code 2 and reports the saved HTML path. Screenshot verification is outside this renderer's contract.

Markdown governs. Edit it and regenerate; the offline HTML is a viewer. Keep these two artifacts in `planning/`. There is no JSON record or entity register. Structural validation does not establish substantive readiness for walkthroughs; the stage skill owns that judgement.

## One matrix

Use exactly one pipe table, with a header, a separator row, and at least one data row. Copy the column headings and order from [the fixture](scripts/fixtures/matrix.md). All 18 columns are required. Every physical table line starts and ends with `|`; every separator cell is at least three hyphens, optionally with alignment colons. Blank lines end the table. Additional tables, missing cells, and extra cells are errors.

Each row is one process–risk–control combination. IDs use `P-` (process), `R-` (risk), or `C-` (control) followed by digits. Repeated IDs across different combinations are valid. For each shared ID, repeat its entity fields identically, including citations and gap markers; control fields include Planned Procedures. Leading/trailing cell whitespace is ignored, but wording and within-cell spacing are significant. A risk can belong to several processes and a control to several risks. Duplicate combinations fail validation.

For a risk without an identified control, leave Control ID and all control attributes empty except Control Title, which must be `Control not yet identified`, and Planned Procedures, which holds risk-gap procedures. Repeat these procedures identically for each occurrence of that Risk ID without a control. Such a row is valid alongside identified controls for that risk. The renderer accepts empty procedures as a visible gap; the stage skill checks whether the work program is usable.

## Supported text

- Keep a table row on one physical line. Use `<br>` or `<br/>` for within-cell line breaks. Write numbered procedures as `1. First step<br>2. Second step`; the renderer preserves the numbers as a list.
- Escape a literal pipe as `\|` and a literal backslash as `\\`. Other backslashes remain literal. Pipes inside links also need escaping.
- Use inline source links as `[label](destination)`. Destinations contain no whitespace or parentheses; percent-encode these characters in filenames. HTTP(S), mailto, fragments, and relative paths are supported. Other schemes and protocol-relative URLs display as text, never executable links. Labels contain no square brackets. Raw HTML is escaped; only the specified line breaks are interpreted.
- Explicit internal entity references use `[label](#P-01)`, `[label](#R-01)`, or `[label](#C-01)`. Every such target must occur in the matrix. Plain ID mentions are text, so retirement history may name old IDs. RQ references are external: use a relative request-list link such as `[RQ-01](../request-list.md#RQ-01)`; they are not resolved against matrix entities.
- Outside the matrix, use plain paragraphs, `#` through `######` headings, and `- ` bullets or numbered lines. These are rendered in document order. Other Markdown constructs display literally. Put upstream snapshot references/versions and methodology basis before the table, and Information gaps (including RQ references) and Flags after it. They remain prose, never extra matrix columns or tables.
- Empty non-ID cells display `[Unknown]`, except the absent Control ID and attributes in a missing-control row, which stay empty. Explicit unknowns are `Unknown`, `TBD`, `?`, or a descriptive bracketed marker such as `[Owner pending]`. They remain visible. Process/Risk IDs always require real IDs; a blank Control ID is allowed only in the missing-control row.

## Methodology replacements

Document the governing methodology and glossary basis in surrounding prose. Defaults are likelihood and impact 1–5, score = likelihood × impact, bands Low 1–4 / Moderate 5–9 / High 10–16 / Critical 17–25, Type preventive / detective / corrective / directive / compensating / recovery, and Nature manual / automated / IT-dependent.

When documented methodology or glossary replaces these, put any applicable directive below on its own line **outside the table**. Directives are visible prose in both artifacts. Omitted directives retain defaults; a changed scale usually needs changed bands too. Directives may appear only once per key. Preserve spelling for display; band, Type, and Nature comparisons ignore case.

```text
RCM likelihood: 1, 2, 3
RCM impact: 1, 2, 3
RCM bands: Low=1..3; High=4..9
RCM types: preventive, detective, corrective
RCM natures: manual, automated, hybrid
```

Scales are nonempty lists of distinct positive integers. Bands are named, ascending, contiguous integer intervals covering exactly the minimum through maximum product of the scales. Classification lists contain distinct nonempty names. The script rejects malformed or unknown directives. Known ratings must belong to their scale, a supplied score must be in the possible score range, and supplied likelihood/impact/score must agree. A supplied band must match the score (or the product when both ratings are known). Unknowns are never inferred into the output.

Rows sort by Process ID (lexically), descending band then score, and Control ID (lexically). Rows with any unknown rating, score, or band follow fully rated rows within their process, ordered by Control ID; source order breaks ties. All shared content remains repeated.

## Validation

Named failures are `TableStructure`, `MissingID`, `InvalidID`, `MissingControl`, `ConflictingEntity`, `DuplicateCombination`, `DanglingReference`, `InvalidMethodology`, `InvalidRating`, `InconsistentScore`, `InconsistentBand`, and `InvalidClassification`. The first failure stops generation. File read/write failures report `FileError`.

From this folder run `python -m unittest`. Tests exercise Markdown input through HTML or named errors, preserving existing output on failure, and platform opener dispatch without opening a real browser.
