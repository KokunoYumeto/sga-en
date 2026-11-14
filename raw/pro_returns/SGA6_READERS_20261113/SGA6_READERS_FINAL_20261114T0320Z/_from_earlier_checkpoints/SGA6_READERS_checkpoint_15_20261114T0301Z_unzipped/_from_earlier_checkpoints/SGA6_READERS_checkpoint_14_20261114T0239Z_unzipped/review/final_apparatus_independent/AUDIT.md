# Independent audit of French apparatus provenance

The captured apparatus contains **970 exact alternatives**. All 970 pass the independent ID, folio, text, SHA-256, TSV, resolved-source, and literal-correspondence checks; both body locations pass, giving 1,940 location checks. The audit identified seven occurrence-attribution or compound-source issues. All seven are resolved in the observed 90-row manual-link stream. The French alternatives and the underlying source decisions were not changed.

## Seven resolved issues

| Variant | Folio | Captured-report issue | Effective source |
|---|---:|---|---|
| FRV0061 | 15 | wrong occurrence of the same spelling correction | `fixes/MISPRINTS_6.json#62` |
| FRV0271 | 259 | wrong occurrence of the same reference-digit correction | `check/findings/findings_256_260.json#20` |
| FRV0426 | 372 | one wrapper component linked to a different mathematical-letter occurrence | `ASTRA-VI-ALGEBRA-RULE-372` |
| FRV0485 | 397 | notation locator linked to a different basis locator on the same page | `ASTRA-VI-FLAG-NOTATION-REFERENCE-397` |
| FRV0745 | 557 | two parts of one pivot-index correction split across different source occurrences | `ASTRA-X-0093` |
| FRV0768 | 580 | missing separately adjudicated component source in a compound variant | `ASTRA-X-REF-580-POSTFREEZE`; `fixes/MISPRINTS_6.json#501` |
| FRV0773 | 585 | localization bar linked to the following residue-field bar | `fixes/MISPRINTS_6.json#493` |


The page 397 notation/basis mismatch had already been identified by the coordinator and early reviewer and was present as an override in the initial manual snapshot. The other six required additional overrides during this audit. Complete exact alternatives, contexts, source reasons and the original versus corrected source lists are in `DISCREPANCIES.json`.

## Scope and evidence

The occurrence pass covers **419 distinct alternatives**. It includes all 41 variants with an automatically selected literal context shorter than six characters, all 48 variants with multiple short-pair candidate sources, all 35 repeated complete-pair groups (79 variants), every manual whole-alternative link, compound-source alternatives, the additional short-context/tiny-pair cases, and the listed explicit source-scope exclusions. `OCCURRENCE_AUDIT.json` retains an individual row with exact neighboring text and the attributed source records for each reviewed alternative.

The remaining 551 alternatives received the exact-text, hash, location, character-edit and resolved-provenance checks. This is a provenance-selection audit of existing reviewed evidence. It does not claim a fresh scan collation or a new mathematical proof for each of the 970 source corrections. No new source image was certified.

The repeated-pair checks confirm the two page 12 naif subscripts under M51; distinguish the two page 17 citations; confirm M252's explicit coverage of the display tag and both later references on 293; and retain the counted page-wide operator records where their scope really covers multiple occurrences. The page 89 and 93 category-C manual links remain distinct from the adjacent site-S records. Full group-by-group reasons appear in `REPEATED_PAIR_AUDIT.json`.

## Literal and positional checks

The saved French bodies were captured after the 49 numeric-heading font declarations had been added, whereas the 970 cached offsets preceded that supplement. The auditor inverted only those exact 49 declarations in each branch **in memory**. All 970 offsets then matched in both branches. No source file was rewritten; `context_alignment.json` records the body hashes and the 98 exact inversions.

The captured automatic proofs comprise 803 whole-pair reconstructions and 435 literal-component correspondences. All were independently replayed. Each character delta is covered. The manual stream is checked against the same exact alternatives and hashes. The source records retain accepted dispositions, matching folios, scan references and their own reasons. The TSV alternatives and source lists match the captured JSON exactly.

## Code assessment

The existing builder's exact cache/manual assertions are effective safeguards. Its automatic scores establish literal correspondence, but a minimal3-to 4 or one-brace hunk can come from another occurrence on the same page. A compound diff can also merge two independent changes into one character component. The seven explicit whole-alternative overrides address these observed cases without broadening source scope.

The component report stores the printed neighboring literal strings and a context length common to two separate branch comparisons. The independent validator checks each branch against its own source-pair strings; it does not assume neighboring text is identical between branches. The later code changes observed during this audit only add explicit source-error classification supplements; the literal-selection and manual-precedence logic is unchanged. `CODE_AUDIT.json` and the two saved code diffs document this.

## Handoff

`EXPECTED_REGENERATED_LINKS.json` fixes all 970 alternatives and their effective source IDs. Run `python review/final_apparatus_independent/verify_regenerated.py` after rebuilding the French apparatus. That read-only check compares the regenerated report and variants with this exact expectation and writes only its audit result here. The original capture remains unchanged under `input_snapshot/`.

No French source text, source decision, frozen review, contribution, or checkpoint was modified by the audit.


## Regenerated output verified

The coordinator's rebuilt report and variants have now passed `verify_regenerated.py`: all 970 exact alternatives, hashes, folios and effective source lists match the sealed expectation, with90 manual links and zero unresolved entries. `REGENERATED_VALIDATION.json` records the exact observed file hashes.
