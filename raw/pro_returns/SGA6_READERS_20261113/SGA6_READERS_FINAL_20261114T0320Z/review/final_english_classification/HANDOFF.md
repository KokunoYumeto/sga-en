# English apparatus classification handoff

**All 691 English variant groups are classified; zero unresolved source decisions or complete-pair attributions remain.** This is a read-only classification audit. It changes no English/French reader, final variant ledger, source decision or sealed audit.

Input: `review/english/final/VARIANTS.jsonl`  
SHA-256: `eba4605bc5b30336f87910e4d30feeccf88661ef8492a292eec0d17696462757`

The audit calls `fr_source_links.load_decisions()` and the unchanged `fr_readable_apparatus.classify()` function. It includes semicolon-separated decision IDs and the explicitly declared `related_sources`. File references and bibliographic verification descriptions are preserved separately and are not treated as decision IDs.

## Counts by kind

| Kind | English variant groups |
|---|---:|
| source misprint correction | 510 |
| mathematical source correction | 45 |
| explicit notation convention | 128 |
| adjudicated source correction | 8 |
| **Total** | **691** |

## Counts by exposé

| Exposé / matter | Misprint | Mathematical | Notation | Adjudicated | Total |
|---|---:|---:|---:|---:|---:|
| Front matter | 1 | 0 | 0 | 0 | 1 |
| 0 | 62 | 11 | 0 | 0 | 73 |
| I | 43 | 0 | 0 | 0 | 43 |
| II | 38 | 0 | 2 | 1 | 41 |
| III | 35 | 0 | 0 | 0 | 35 |
| IV | 15 | 0 | 0 | 0 | 15 |
| V | 57 | 2 | 8 | 3 | 70 |
| VI | 52 | 0 | 61 | 0 | 113 |
| VII | 32 | 9 | 40 | 0 | 81 |
| VIII | 16 | 1 | 17 | 0 | 34 |
| IX | 5 | 0 | 0 | 0 | 5 |
| X | 50 | 5 | 0 | 1 | 56 |
| XI | 0 | 0 | 0 | 0 | 0 |
| XII | 21 | 12 | 0 | 0 | 33 |
| XIII | 46 | 5 | 0 | 3 | 54 |
| XIV | 31 | 0 | 0 | 0 | 31 |
| Indexes | 6 | 0 | 0 | 0 | 6 |

XI is marked « Non rédigé » in the source and has no variant group. Bibliographies remain assigned to their exposé; the terminal indexes are listed separately.

## Attribution checks

- **690 distinct resolved source decisions** supply the classifications, including amendments and the explicit classification supplements.
- **623 groups** have exact final-ID, folio and complete printed/corrected pairs in the aggregate transfer ledger. **68 groups** match their complete original `EN_VARIANTS.jsonl` records; these are EN-VAR-001…067 and EN-VAR-068. The latter also has an ID-linked aggregate record that does not repeat the pair.
- **43 reused source IDs** were checked against their individually named complete transfer pairs. The only cross-folio source alias, ASTRA-EARLY-TYPE-016, explicitly covers both 70 and 75.
- All 27 groups with declared secondary sources include those decisions. In VI385-03 the E-rule source misprint takes precedence over the P notation convention; in VII077/461 the independent rational-coefficient mathematical correction takes precedence over the exponent misprint.
- **12 auxiliary reference strings (69 uses)** are retained separately. Every supporting file exists and has its hash recorded. The two bibliographic descriptions remain literal descriptions attached to an independently resolved source decision.
- **No actual missing provenance was found.** The eight entries classified as adjudicated source corrections use the unchanged classifier's fourth branch; their accepted image-backed decisions are complete, but their metadata does not assert one of its higher-precedence categories.

## Fourth-branch entries

| Variant | Folio | Explicit source decision(s) |
|---|---:|---|
| EN-VAR-136 | 186 | fixes/RECONCILE_CODEX_6.json#252; fixes/FIXLOG_6_CURRENT.jsonl#359 |
| EN-CONTRIB-V-335-01 | 335 | check/findings/findings_331_335.json#12 |
| EN-CONTRIB-V-356-02 | 356 | fixes/FIXLOG_6_CURRENT.jsonl#415 |
| EN-CONTRIB-V-362-03 | 362 | check/findings/findings_361_365.json#12 |
| EN-CONTRIB-X-003 | 524 | ASTRA-X-0015 |
| EN-CONTRIB-XIII-041 | 661 | ASTRA-XIII-0066 |
| EN-CONTRIB-XIII-052 | 666 | fixes/FIXLOG_6_CURRENT.jsonl#556 |
| EN-CONTRIB-XIII-053 | 666 | fixes/FIXLOG_6_CURRENT.jsonl#557 |

## Files

- `CLASSIFICATION.json`: summary, exact classifier, and all 691 entries with source IDs, complete alternative hashes, metadata predicates and transfer attribution.
- `RESOLVED_SOURCE_DECISIONS.json`: exact resolved/amended/supplemented source metadata used.
- `EXACT_TRANSFER_EVIDENCE.json`: full supporting English transfer records and row/file hashes.
- `BROAD_ALIAS_AUDIT.json`: occurrence-specific transfer checks for reused decision aliases.
- `INPUT_MANIFEST.json`: exact hashes of all loader and transfer inputs; rechecked unchanged at completion.
- `VALIDATION.json`: zero-unresolved release checks.

These are counts of English variant groups. A group can contain more than one sourced component and is counted once according to the shared classifier's precedence. This audit does not re-adjudicate the mathematics or assert a fresh scan reading.
