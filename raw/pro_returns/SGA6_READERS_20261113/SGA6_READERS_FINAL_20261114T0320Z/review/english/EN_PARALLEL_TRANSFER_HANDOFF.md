> Historical contributor interface. All assigned English intervals and final aggregate gates are complete. The authoritative completed handoff is final/HANDOFF.md, with exact hashes and scope in final/RELEASE_STATUS.json. The earlier progress statements below are retained as the working interface history.

# English transfer handoff

This handoff supports separate later-exposé contributions while the English
assembly continues in `review/english`. The latest compiled prefix is folios
1–296, with all four forms passing twice and the new corrected IV body/apparatus
region visually checked. The source comparison covers9,621 mathematical units
with zero unexpected differences,68 accepted passage records and201 variants.
Frozen checkpoints remain untouched. Later disjoint contributions remain in
their assigned directories until contiguous assembly.

## Assigned intervals

| Owner | French source folios | Contribution directory |
|---|---|---|
| English assembly owner | Contiguous1–296 complete; VII416–465 sealed; XIII616–666 in progress | `review/english/contributions/expose_vii` and `review/english/contributions/expose_xiii` |
| V reviewer | V–VI297–415 | `review/english/contributions/exposes_v_vi` |
| VIII reviewer | VIII–X466–594 | `review/english/contributions/exposes_viii_x` |
| Coordinator | XII595–615 sealed; XIV667–700 and front/rear matter | `review/english/contributions/exposes_xii_xiv` and a separate front/rear packet |

These assignments follow the actual supplied sequence: there is no ExposéXI
body to create. Each contributor may deliver successive coherent chunks before
the whole assigned range is complete. Keep later chunks inside their assigned
directory until assembly, even when a local branch check passes. The aggregate
reader only advertises its contiguous registered prefix. Final variant numbers,
the glossary, global registries and full-document builds remain with assembly.

## Ownership

Each contributing reviewer writes in a separately assigned directory, for
example `review/english/contributions/expose_iv`. Keep drafts there until the
English assembly owner integrates them. Do not edit shared
`EN_TRANSLATION_PATCHES.jsonl`, `EN_VARIANTS.jsonl`,
`EN_APPROVED_LEXICAL_MATH_PAIRS.json`, `EN_AUTHOR_NOTE_MARKS.tsv`, generated
readers, build status, glossary files or original `en/` and `fr/` sources.
The assembly owner assigns final variant numbers, composes adjacent exact
replacement spans, runs full builds and maintains the glossary. Source-reading
decisions stay with the French coordinator/reviewer. A translation contribution
does not alter those source records.

## Exact French reference

From the `sga6_work` directory:

```python
import sys
sys.path.insert(0, "review/english")
from reviewed_french import load_reviewed_pages
current, current_record = load_reviewed_pages(last_folio, "current", start=first_folio)
diplomatic, diplomatic_record = load_reviewed_pages(last_folio, "diplomatic", start=first_folio)
```

The loader uses `build/page_packets/<folio>/<layer>.tex` after folio77 and
applies recorded patch streams in order. Later streams follow the French
assembler's late/middle-then-alphabetical order. It fails on an unexpected
anchor count; it accepts an already-applied patch only when that exact old/new
pair was already applied in the same composition. Do not suppress a failure or
blindly replay old `add_*.py` scripts. Retain the returned page hashes, patch-line
hashes and baseline differences for the contribution's scope. The loader's
success does not establish scan coverage: inspect the assigned exposé's
`page_status.jsonl`, decisions and frozen handoff separately.
The optional `start` argument limits the comparison to the assigned interval;
its default remains1 for the existing aggregate scripts. Returned `bases` are
ordered from that supplied start, so use the `page` field when looking up a
reference record. The contribution checker supplies its first chunk page as
`start`, avoiding a dependency on unrelated live French review intervals.

II178's post-checkpoint05 locator amendment is a separate stream. Author-claim
packets on II206, III244–245 and IV295 retain the source body; they do not supply
replacement assertions. Follow the coordinator's exact disposition when these
passages occur in the assigned text.

IV287/289 also have a separate `review/expose_iv_amendments` stream: current
repairs the analytic locator5.9(b) to5.8(b), identified by its identical
adjunction-defined projection map; the diplomatic locator stays5.9(b).

Later specific packets include VI385's retained section-equality defect, VI411's
approved all-degree cohomology index, and VI415's approved r-factor product.
Use the coordinator's exact current/diplomatic patches and proof records. The
additional `review/expose_v_rendering/patches.jsonl` stream contains V314's
literal `\inN`→`\in N` transport repair and is consumed by the ordered loader.
Do not replay historical incremental `add_*.py` files to reconstruct source.

## Files to return

1. **Raw corrected English chunks**, named
   `EN_EXPOSE_IV_P274_278.tex` or the analogous range. Translate every paragraph,
   formula, original note and bibliography entry against the reviewed French.
   Preserve each source boundary with its exact comment and one
   `\SGAPrintPage{274}` command. The raw chunk contains current readings; it does
   not contain editorial `\var` calls. Retain mathematical TeX literally,
   including whitespace, local glyph commands, arguments and displayed labels.
   Preserve observed lexical underline spans and separately marked math; do not
   apply an inferred volume-wide font rule. Include original native
   `\sgaStableTarget{...}` anchors in their actual corresponding passages.

2. **`variants.jsonl`**, with one explicit source difference per row. Use local
   provisional identifiers such as `EN-CONTRIB-IV-001`; the assembler will assign
   final numbers. Required fields are `id`, `page`, `old`, `printed`, `corrected`,
   `mode`, `source`, `reason`, `scope_start`, `scope_end`, `scan_image` and
   `scan_region`. `old` is the exact unique current-text anchor; `corrected`
   normally equals it. Scope strings are the folio comments. `mode` is `math`
   for an inner formula, `text` for prose or mixed inline text, and `display`
   for a complete display/diagram. Use the reviewed source identifiers and
   attributed scan evidence. Do not claim a new image reading from a text check.
   Explain a mathematical repair with its actual map or calculation. French
   spelling/agreement changes that leave the English unchanged belong in the
   transfer ledger without an invented English error. Retained French/German
   titles can carry their literal source spelling variants.

3. **`lexical_math_pairs.json`**, an array of individually reviewed complete
   mathematical units whose internal words require translation. Each entry has
   `page`, `layer` (`both`, `current` or `diplomatic`), `French_literal_unit`,
   `English_literal_unit`, `expected_multiplicity`, `status` and `scope`.
   Translate only the lexical text. Preserve every other character; do not
   normalize commands, spacing or notation to pass the comparison.

4. **`transfer.jsonl`** records each applicable French patch identifier and
   patch-line hash, its English variant or unchanged-rendering reason, both
   reviewed page hashes, exact glyph/author-note inventories, and substantive
   restorations of prose, formulas or references. Explain every current-only
   source difference, including those already present in the baseline packets.
   Include independent proof audits as separate attributed packets when the
   source body is retained. Record native and reviewed continuation macro blocks
   and their hashes at exposé boundaries; do not move their definitions earlier.

5. **Original-note and terminology candidates**: `author_notes.tsv` records
   inspected label, call position, full-text location and source ID. The shared
   commands are `\SGAAuthorFootnote{label}{text}` and split
   `\SGAAuthorFootMark{label}` / `\SGAAuthorFootText{label}{text}`. Supported
   observed labels include numerical digits, `*`, `raisedstar` and `unmarked`;
   do not guess labels from sequence order. `terms.tsv` gives French term,
   English rendering, exact passage and any unresolved choice. The assembler
   handles shared glossary counts and cross-volume decisions.

6. **`translation_spans.jsonl`** gives each proposed replacement's exact native
   `old` string, translated `new` string, native span hash, first/last stable
   targets and covered folios. Read the original flattening
   `SGA6_EN_native_flattened_UNVERIFIED.tex`; retain complete native continuation
   definitions. The assembler reconciles neighboring partial-paragraph spans.
   **`STATUS.md`** states completed source comparison, remaining questions and
   whether any PDF was actually compiled or viewed.

## Independent contribution check

The supplied checker writes only into the contribution directory:

```bash
python review/english/check_contribution.py review/english/contributions/expose_iv
```

It materializes both local variant branches and compares every complete TeX
mathematical unit with the two reviewed French forms, recording exact hashes
and differences in `literal_math_verification.json`. A zero unexpected count
is required. It does not certify prose fidelity or PDF typography. The raw
formula comparison permits prose word-order changes through multiset matching;
it does not prove that formulas occupy the right paragraph. That is part of
the manual passage comparison and transfer ledger.

## Assembly commands (assembly owner only)

Run the registration scripts after any accepted raw-chunk change; the builder
reads their stored `new` strings, not the chunk files directly. Exact accepted
anchors must occur once. Then, from `sga6_work`:

```bash
python review/english/verify_reviewed_english.py
python review/english/verify_expose_i_forms.py
python review/english/verify_expose_ii_forms.py
python review/english/build_english_candidates.py
python review/english/compile_candidates.py
python review/english/make_alignment_hints.py
python review/english/refresh_work_summary.py
```

The later-exposé branch checks are added as those contributions are integrated.
Do not run summary refresh while compilation is replacing PDFs. Each build
uses the isolated `scripts/tex_environment.py` wrapper, two passes per form and
path-free diagnostic logs. The annotated master selects all three forms with
`SGAReaderForm`; its apparatus captures the actual local source macro meanings
before later redefinitions. Whole TikZ displays use explicit mode branches to
preserve ampersand parsing. Rendering-only fixes belong in
`EN_RENDERING_REPAIRS.jsonl` with a proved identity of the unchanged content.

Inspect new body pages, original note call/text placement, changed diagrams and
all new apparatus readings. Preserve honest distinctions between prepared,
registered, generated, compiled and visually inspected scope. Source/PDF hashes
and the visible unfinished-volume notices remain part of every checkpoint.

## Final paragraph-continuity assembly audit

Every source-folio join must be checked against its exact reviewed French paragraph continuation. A maker must not add a blank TeX line solely because a folio ends; retain only explicitly translated paragraph boundaries. A source word split can be mapped to an intact English word at an adjacent lexical boundary, with the exact transport recorded. Existing sealed contributions remain immutable and receive any needed join-only repair in the aggregate integration ledger. The already recorded VIII–X continuation list is preserved in `EN_CONTRIBUTION_RECEIPTS.json`; it is a review aid, not an exhaustive certification. The certified blank690 will be consumed from the coordinator’s explicit blank-page packet, with its marker retained.
