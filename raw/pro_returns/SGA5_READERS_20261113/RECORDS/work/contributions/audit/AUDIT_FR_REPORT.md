# French fix-inheritance audit

## Result and scope

Both prepared French layers are reproduced **byte for byte** from their manifest-verified attached source layers by the complete edit list in `SOURCE_TO_PREPARED_FR.tsv`. There are 32 edits in the diplomatic layer and 35 in the current layer. There are no unaccounted differences. This proves that the source state containing the earlier applied fixes is inherited, except for the explicitly enumerated new decisions.

The 32 common edits implement the inspected Exposé XV RΓ decisions. Three additional current-layer edits implement H75 at folio 433 (`F'` to `f'` in the indicated quotient endomorphism), SOL-EN-084 at folio 472 (`F` to `F_\nu` in the annihilation clause), and GLOBAL-98b at folio 441. The last retains the recorded single-underlined, double-struck-F reading of Fr at the unresolved glyph question, following the source task's instruction to keep the printed reading while the scan is needed. The diplomatic layer keeps its supplied readings at those three places. Exact before/after strings and original character offsets are recorded for every edit.

This audit reaches the prepared layers. The reader build extends the proof by checking that the diplomatic and corrected branch projections of its annotated master reproduce those layers, with any presentation-only extraction explicitly specified. Compiling alone does not establish that relation. The audit does not independently reproduce the historical scan-check sequence or recheck judgments against scans unavailable in the attached material.

## Verified source identities

| ZIP-relative source | Source SHA-256 | Prepared SHA-256 | Enumerated edits |
|---|---|---|---:|
| `fr/sga5/diplomatic/s5.tex` | `3d1ed77591eab498a705c25f3f68658d62701d647fcfe1619decd8e723f1777a` | `3c5f1529288fdca8718280d2fd653e1c0066cc103226181a9038e0abadae03a4` | 32 |
| `fr/sga5/current/s5.tex` | `e789ad80e0862d61ab2d5a9503874883283b03d3fe3526ee74a816cd25b08800` | `de944d630421fda55862f8f9079d87ddb92f86ae9e02bbdc67f7db9970f06e3e` | 35 |

The byte lengths and SHA-256 values of all 15 audited fix/status input files also match `MANIFEST.tsv`. `AUDIT_FR.json` records each check by its path inside `SGA5_FR.zip`; source-machine paths are omitted.

## Record coverage

| Collection | Source records | Audit treatment |
|---|---:|---|
| `fixes/FIXLOG_5.jsonl` | 4,173 | One diplomatic inheritance row per original record |
| `fixes/FIXLOG_5_CURRENT.jsonl` | 3,770 | One current inheritance row per original record, including all 29 `misprint_correction` records |
| `fixes/HANDFIX_5.jsonl` | 88 | Original one-based record numbers preserved; layer read from each record |
| `fixes/REPLAY_MANUAL_5.json` | 36 | All 36 have a `resolved` field; later conventions and hand edits are checked |
| `fixes/REPLAY_MANUAL_5_DONE.json` | 1 | Earlier replay sidecar audited separately |
| Seven `fixes/MANUAL_5_findings_*.json` files | 8 findings | Both layers checked, giving 16 rows |
| `fixes/RECONCILE_CODEX_5.json` | 117 entries | Supplied status and reason retained in a separate table |
| `fixes/MISPRINTS_5.json` | 590 entries | Printed/corrected strings and notes retained; presence evidence recorded separately |

`FIX_INHERITANCE_FR.tsv` contains **8,084 rows**: 4,173 + 3,770 + 88 + 36 + 1 + 16. Each row has the source file and its original one-based record number, source scope, before/after strings, observed terminal evidence, observed folios and match counts, any identified superseding record, and qualifications. The source's own `id` is retained separately where supplied. The two extra tables contain all 117 reconciliation entries and all 590 misprint entries.

The reconciliation statuses are 56 `present`, 49 `applied`, 11 `rejected`, and 1 `superseded`. These are preserved decisions from the source record, with exact-source inheritance establishing that this build retains the supplied final layer state.

## What the terminal checks establish

Direct active-source literal witnesses were found for 4,046 of the 4,173 diplomatic fix-log records and 3,655 of the 3,770 current fix-log records. These searches allow an adjacent folio because later hand work moved markers. The remaining log rows have explicitly reported evidence: later overlapping edits, recorded conventions, named superseding records, descriptive or structural witnesses, deletions, R98 substitutions, or the documented title-stop discrepancy below. No fix-log row remains with the generic unresolved terminal-search status. All 88 hand records and all 36 replay records have terminal or explicitly described structural evidence. `AUDIT_FR.json` gives the complete evidence-category counts, including those for the 29 current-layer misprint corrections.

The proof of inheritance is the exact source reconstruction. The terminal searches supplement that proof with record-level witnesses; they do not assume that an intermediate `new` string must survive every later edit. For a recorded overlap, the script applies the later exact `old`/`new` replacement inside the earlier result and locates the resulting string. For a partial overlap, it identifies the exact shared prefix or suffix and transfers only changed intervals inside that shared text. The relevant record identifiers remain in the table. Explicit convention mappings, including derived tensor notation, script H, underlined Omega, and the R98 decisions, are similarly listed.

Some source records describe a global pattern or use ellipses. Their rows report the specified pattern or structural check and state that an individually unique historical occurrence was not established. A literal appearing more than once is reported with its match count. A raw-source-only match is distinguished from a match in the diagnostic active text. Deletion evidence reports the old string's absence in its scope; it does not manufacture a historical location for an unlocated deletion.

For the small number of whitespace-projection witnesses, the mapping is explicitly defined: delete each unescaped percent sign and the following text through its line ending, then delete Unicode whitespace. Equality after this mapping gives a string-location witness. It is not used as a proof that arbitrary TeX expressions have identical rendered output. No notation is rewritten in the source by this audit.

## Source-record details that require qualification

At folio 109, `FIXLOG_5.jsonl#710` and `FIXLOG_5_CURRENT.jsonl#665` record the title string `{Corollaire 4.7 - (Formule de Lefschetz-Verdier)}`. The authoritative final sources contain `{Corollaire 4.7 - (Formule de Lefschetz-Verdier).}`, with a final full stop before the closing brace. The audit reports `source_terminal_difference_documented` for these two rows. The title and its single hyphens are located; the final source's additional stop is inherited. No historical record for that added stop is invented.

`REPLAY_MANUAL_5.json#10` has a `resolved` field whose text still begins “open”. Its folio-184 wording was subsequently restored by `HANDFIX_5.jsonl#45`; that terminal text is present. The original status wording remains visible in the audit rather than being silently rewritten. Likewise, replay items 12–14 at folio 201 are read with the later restorations in hand records 46–48.

`fixes/MARKERS_5.json` is an earlier placement report: it lists 482 markers and missing folios 435 and 484 in both layers. Hand records 13 and 14 subsequently add folio 484. The final source layers and prepared layers each contain **483 markers**, with the same full ordered marker sequence, scan index equal to folio + 11, and only folio 435 absent. The source task explains that omission by the print's repeated page number 434; the build does not invent a folio-435 marker.

## Misprint-register status

All 590 entries contain `page`, `where`, `print`, `correct`, `tex_did`, `note`, and `source`. No entry contains a separate `status` or `decision` field. The decisions and qualifications therefore have to be read from the supplied fields and notes.

The final current layer supplies a literal or explicit projection witness for 512 corrected descriptions: 498 on the declared folio, 13 on an adjacent folio, and 1 under the stated whitespace projection. The remaining 78 descriptions require their prose, notation, supersession, or new-build-decision context; failure of this literal search is recorded explicitly. They include the folio-441 GLOBAL-98b decision to retain the printed glyph while its scan remains needed. The audit makes no blanket assertion that 590 proposed corrections were all inserted. The full register notes are retained in `MISPRINT_STATUS_FR.tsv`, while the manifest/source reconstruction separately proves preservation of the attached final layer except for the enumerated decisions.

## Reproduction and files

From the build workspace, run:

```sh
python work/contributions/audit/audit_fixes.py
```

The script also accepts `--fr`, `--prepared`, `--scans`, and `--output` to set the source directory, prepared-layer directory, R98 patch JSON, and audit output directory. `--additional-edits` accepts an explicit JSON list of further uniquely located before/after edits when a later build adds a recorded decision. The script checks source identities, expected record counts, exact reconstruction, marker inheritance, and unresolved terminal searches, and exits unsuccessfully when one of these required checks fails.

Outputs are `AUDIT_FR.json`, `FIX_INHERITANCE_FR.tsv`, `SOURCE_TO_PREPARED_FR.tsv`, `RECONCILE_INHERITANCE_FR.tsv`, `MISPRINT_STATUS_FR.tsv`, and this report. All source references in these outputs use paths inside the input ZIPs or record identifiers. Email addresses and source-machine paths are removed from copied free-text evidence.
