# Exposé 0 and appendix: completed scan collation

Printed folios **1–77** have been compared in order against the main scan, word by word and symbol by symbol. Each complete page was viewed in four overlapping image strips. The review includes body text, displayed formulas, diagrams, headings, author and copyist notes, punctuation, and the exact printed folio boundaries.

The main scan is `scan/SGA6_scan_360dpi.pdf`, physical PDF page = folio + 14. The witness is `scan/SGA6_witness_300dpi.djvu`, physical page = folio + 11. Its offset was confirmed. Witness use is regional: the inspected detail is stated in the evidence and page notes. The witness was used on folios 3, 4, 5, 8, 16, 31, 35, 37, 41, 42, 49, 50, 53, 57, 60, 64, 68, 70, and 75. No claim of complete second-scan collation is made.

## Files to merge

- `review/early/decisions.jsonl`: 1,152 source-linked decisions.
- `review/early/patches.jsonl`: 121 occurrence-specific patches against the attached page extracts: 61 current-only, 59 both-layer, and 1 diplomatic-only.
- `review/early/page_status.jsonl`: exactly 77 complete page records, in folio order.
- `review/early/coverage_audit.json`: the expected source IDs, their coverage, the actual page mapping exception, and the aggregate counts.
- `review/early/frozen_manifest.tsv`: sizes and SHA-256 digests of the frozen records, supporting data, and scripts.

These files are review inputs for the coordinator's annotated masters and reader builds. This handoff does not certify the coordinator's final typesetting or the as-yet-unreviewed remainder of the volume.

## Source coverage

| Source family | Decisions in folios 1–77 |
|---|---:|
| Checker findings | 411 |
| Diplomatic FIXLOG rows | 266 |
| Current FIXLOG rows | 246 |
| MISPRINT register records | 115 |
| Manual replay items | 2 |
| Hand-placed findings | 0 applicable |
| Exposé 0 Codex queue entries | 14 |
| Corresponding tagged-source records | 3 |
| HOLD differences at actual early passages | 31 |

Every expected ID in these groups has a decision. The source audit found no missing early record. The three tagged-source records are reconciliation entries 314–316, explicitly cross-linked to queue entries 165–167 and to their already-inspected passages. All five rejected Exposé 0 queue claims are adjudicated, including the two different occurrences addressed by queue entry 164.

HOLD entry 35 was filed in a nominal folio-75 packet but concerns Exposé I §1.1.5 at actual folio 85. It was referred to the Exposé I reviewer, who has reported its independent decision. It is excluded from this handoff's page and source coverage. HOLD entries 1–3 concern the front matter; entries 4–34 are the 31 early differences decided here.

## Material decisions

The new findings include corrected mathematical indices, missing symbols, wrong references, and page-boundary syllables. Each exact change and its reason is in the JSONL records. Examples include the coefficient index in formula (1.37), the positive range needed by the factorial formula (1.38), the missing tilde on the target of the total Chern map, the reversed filtration inequality on folio 57, and the direct-image lower shriek in the folio-69 Riemann–Roch formula. Their reasons give the specific identities, maps, or neighboring definitions that establish the correction.

The proposed replacement of the locally introduced factors `C_j` by `G_j` on folio 62 was rejected. The explicit renaming `G_j := C_j` leaves the projections and their pulled-back bundles identical; the passage therefore supplies no correction to the printed local names. The duplicate printed lemma number 2.15 on folios 61 and 62 is also retained. The associated-graded notation `G(A)` was retained with its explicit degree-component identification recorded.

The final batch restores the omitted check on `F` in the folio-76 Riemann–Roch triple in the corrected layer (MISPRINT 116), corrects `obtenu` to `obtenue` there (MISPRINT 117), and preserves the observed raised and lowered copyist stars (ASTRA-EARLY-TYPE-019). Folio 77 required no new change.

## Typography and note conventions

Occurrence-specific patches preserve the inspected double-struck category C, underlined structure-sheaf O, and primes outside the underline of L. No global category or structure-sheaf macro is redefined by this review. Script Todd T and every inspected lower-shriek/star distinction are recorded by scope or occurrence. Existing emphasis groups were compared with the printed underlining; the coordinator's word-group underline formatter supplies their rendering, with the accepted statement/heading conventions of NOTE_6 retained.

Author notes use the shared explicit helpers `SGAAuthorFootnote`, `SGAAuthorFootMark`, and `SGAAuthorFootText`. Literal label keys preserve the different observed forms: `1` for the raised numerical note on folio 25; `raisedstar` for the high stars on folios 8 and 15; `*` for the inspected central starred notes; and `unmarked` for the copyist explanation on folio 71. Repeated calls, display-positioned calls, and the absence of a call after the folio-71 heading are preserved. The separately observed copyist interpolation stars retain their raised, lowered, or normal-height positions.

The diplomatic spelling `KÜnneth` on folios 70 and 75 is retained explicitly, with `Künneth` in the corrected form. Main-scan and native witness details support the tall U form. The change has its own source ID and is not treated as a silent typeface substitution.

Layout-only observations on folios 27 and 30 retain the attached displayed formulas. The evidence states the token-by-token identity between each printed inline formula and its displayed transcription. The earlier tentative layout patches were removed from both the current patch registry and their historical one-shot scripts.

## Validation and reproduction

`record_review.py` regenerates the three primary JSONL files from the explicit image-evidence dictionaries, extra records, and overrides. `validate_review.py` verifies unique source IDs and every patch's expected anchor count against the unmodified attached page extracts. `freeze_audit.py` verifies source coverage, folios 1–77, reference privacy, and hashes. The latest run reports **zero validation or coverage errors** and **no unresolved in-scope item**.

The `add_batch_*.py` and `add_author_labels_001_060.py` files document the incremental entry of evidence; they are one-shot scripts and must not be replayed against already-populated data. Rendering and crop helpers are saved. The canonical frozen records and their hashes, rather than rerunning those one-shot entry scripts, are the merge authority.

The English reviewer received each batch's material decisions and the explicit author-note and copyist-mark geometry. The English reconstruction and its compilation are owned and certified separately by that reviewer.
