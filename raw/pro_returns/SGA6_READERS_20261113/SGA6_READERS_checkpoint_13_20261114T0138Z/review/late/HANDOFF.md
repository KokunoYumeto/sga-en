# Late review: complete handoff

The direct page comparison is complete for printed folios **667–700**, including all of Exposé XIV, the bibliography, the editorial notes, the blank verso690, and both indices. The main image source is `scan/SGA6_scan_360dpi.pdf`, PDF page=folio+14. The witness is `scan/SGA6_witness_300dpi.djvu`, page=folio+11; this offset was checked against the visible folio on the first witness read. Weak or omitted strokes were checked against actual witness images. Codex's `fr/codex/sga6_fr_r1_fr.tex` was compared as the second reading for672–689.

## Files to merge

| File | Rows | Purpose |
|---|---:|---|
| `review/late/page_status.jsonl` | 34 | Fully inspected page certification,667–700 |
| `review/late/decisions.jsonl` | 801 |279checker,386FIXLOG,86misprint,40Codex,9HOLD,1replay decisions |
| `review/late/patches.jsonl` |154| Exact replacements with page, layer, source ID, and expected occurrence count |
| `review/late/own_findings.jsonl` |107| New readings, local notation decisions, damaged-print resolution, and page-marker decisions |
| `review/late/write_reviews.py` |1script| Regenerates the four JSONL files without changing either source master |

Every applicable checker, FIXLOG, MISPRINT, rejected or applied Codex record, HOLD difference111–119, and open replay item20 has an explicit decision. An independent ID-coverage audit found no missing applicable records and no duplicate decision IDs. All154patches were simulated sequentially against both frozen source layers; every expected-count assertion passed. The decision files contain no local absolute paths or email addresses.

## Marker actions requiring the coordinator

- **690 is entirely blank**, mainPDF704/witness701. Insert `%%%%%%%%%%  scan idx 703  |  folio 690  %%%%%%%%%%` after the final p.689 paragraph ending `pour conclure la même relation dans le cas général.` and before the final-index setup. No missing body text needs transcription.
- The670/671break is `essentielle-` / `ment`; preserve `essentiellement` as one extracted word with an internal zero-width page boundary.
- The672/673break is `dis-` / `pose`; preserve `dispose` as one extracted word with an internal zero-width page boundary.
- Previously moved669,670,688,696–700markers now agree with the images. The decisions record their actual boundaries.

## Material adjudications

Accepted current-only mathematical corrections include:676degree exponent `dim Y` by the explicit codimension calculation;676ambient `Gr_top(Y)` for `f^*f_*`;679the second filtration's duplicated `top`;680positive-degree index `i>0`;683virtual relative dimension “de f”;689note reference `(4.6)` in place of `(9.6)`;699Adams superscript `psi^k` verified against V7.1.

Reverted or rejected editorial expansions include:674the added `(X)` after `Gr_top`;669an added grading dot where `Gr(Y)` is unambiguous;679`A^0(X)`→`A^0(G)` because pullback identifies the degree-zero groups;681`c^i(E)`→`c_i(E)` because V6.7.1 explicitly defines the superscript notation;691deletion of `C_0` because I4.8 expressly identifies that category;bare citation brackets and abbreviation punctuation;699`par.amp`→`parf.amp`.

The bibliography's `U. Mausin` is corrected to **U. Manin**, retaining the printed initial rather than adding `Yu. I.`. Replay20is closed by removing emphasis around the already corrected SGA4title. The unanchored footnote on675remains unanchored in both forms; the printed orphan mark on677must remain explicit. The coordinator owns printed footnote-mark rendering.

All inspected complex L dots in667–669and685are lower dots; K/Gr/gdots are raised where printed. The cohomology placeholders in XIV are typed asterisks, distinct from those dots. Current H2* on681requires8replacements while diplomatic requires7; ASTRA-LATE-0044is already split into those layer-specific counts. The right K in670's regularity isomorphism has **no dot in either image**: the diplomatic patch restores that omission, while current retains the coherent-group lower dot.

Local underlines are explicitly recorded: structure sheaves, bundle letters, category C and site/category S in the indices, and M beneath Hom. The plain C in696's `cl_C` has no underline; preserve that local exception. Global notation work should deduplicate these exact patches rather than replace their observed distinctions.

## Boundaries of certification

The cross-reference images on122,353,360and651were read only to settle specific late-page decisions; these are not certified as full-page checks. All page-status rows in this review belong only to667–700. No source masters were edited.

This directory is frozen after the handoff. Subsequent Exposé XIII work belongs to `review/xiii/`.
