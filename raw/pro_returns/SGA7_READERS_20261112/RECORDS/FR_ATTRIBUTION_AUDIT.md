# French source-attribution audit

This is a correction of citation metadata. All 2,824 apparatus entries, their 1,112 variant-group identifiers, every diplomatic and corrected body reading, and the order and before/after text of all 7,977 change-log rows are preserved. The original ADOPT review remains exactly 531 entries: 197 in Volume I and 334 in Volume II.

## Results

| Record set | Rows checked | Rows with changed citation metadata | New WITNESS fallbacks |
|---|---:|---:|---:|
| French apparatus | 2824 | 806 | 529 |
| CHANGES_FR | 7977 | 1891 | 1053 |

The complete old-to-verified attribution changes are in `FR_ATTRIBUTION_CHANGES.tsv`. `FR_ATTRIBUTION_AUDIT.json` includes every checked row, exact witness offsets, selected source-record quotes and changed spans, record orientation, and hashes of the parsed source rows. `FR_ATTRIBUTION_BASELINE.json` freezes the earlier citation metadata and reading-identity hashes; it does not validate the earlier claims. `FR_ADOPT_COHORT.json` freezes the already reviewed textual cohort.

## Decision rules

Same volume, file where recorded, and folio. Exact full quotations must place the hunk inside their actual old/new changed spans; alternatively an identical recorded changed atom must be unique among actual same-page hunks and have a surviving full-quotation anchor at that exact span. Every surviving quote must be consistent with the hunk. No nearby-context or quote-length scoring and no unanchored atom inference.

Records using paraphrase, composite quotations, or surrounding text changed independently may fail this conservative exact check. A WITNESS identifier records that the paired designated witnesses support the existing reading, while the earlier individual historical citation is not established. It is a metadata fallback, not an emendation or a new ADOPT decision.

Existing genuine ADOPT and COLLATION witness decisions are retained even when an additional exact historical link can be found; those optional links appear separately in the audit. Supported historical citations are retained. Unsupported co-citations are removed. A historical claim with no supported citation receives a WITNESS identifier, whose explanation is explicitly about attribution and does not enlarge the textual-review scope.

## Targeted regressions

- F7I-IX-212.1, Reguliers → Réguliers at I:525, now cites 7I:800 at FIXLOG_7I_CURRENT.jsonl record 1005. The neighboring Ferrier correction at record 1006 is rejected because its changed span does not support this hunk.
- F7II-XVIII-013.2–.5 no longer cite ED-G52-notée: that decision changes notées → notée and does not support these quotation, spacing, and mathematical-accent changes. Each receives its own verified historical or paired-witness attribution.
- F7I-VII-046.1 retains ED-7I-356. The three current-layer CHANGES_FR rows retain ED-7I-356, ED-G52-notée, and ED-7II-1018, with exact changed-span evidence.

## Reproduction and indexing

Running `python build/french.py` regenerates both the apparatus and CHANGES_FR through the same matcher; `--data-only` omits reader construction. The two frozen input JSON files above must accompany the supplied source witnesses, correction logs, and editorial decisions. The rebuild checks the frozen identities and stops if body readings, entries, groups, or change-log order differ.

FIXLOG references count JSONL records from 1; MISPRINTS references use the existing zero-based array indices. Editorial patches are identified by their exact decision ID.

Zero-based half-open character spans in the exact cleaned witness projections used by french.py (source comments removed; folio furniture replaced by SGApage anchors).
