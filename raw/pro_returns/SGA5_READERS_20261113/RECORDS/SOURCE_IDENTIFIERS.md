# Source identifiers

All source coordinates in the witness/reconstruction JSON files specify their unit and origin. `L` is a one-based physical source line; zero-based half-open character and byte ranges are explicitly labelled and retained separately.

| Citation | Exact destination |
|---|---|
| `FR_SOURCE_WITNESSES.json:FR-xxxx` or `:R98-xx` | The matching `id` in the root file's `variants` array; canonical copy under `work/contributions/validation_fr/` |
| `EN_variants_input.json:ID` | The matching original English input `id`; root file and canonical `work/build/prepared/EN_variants_input.json` |
| `FR-xxxx`, `EN-xxxx`, `R98-xx` in a reader | Matching balanced call and entry in `work/build/prepared/FR_variants_ordered.json` or `EN_variants_ordered.json` |
| `PLACES_98_DECIDED.tsv:R98-xx` | Exact ID row in the root scan-decision table |
| `OPEN_ITEMS_DECIDED.tsv:ID` | Exact item ID in the root open-item decision table |
| `MISPRINTS_5:NNNN` | One-based record NNNN in `SGA5_FR.zip` member `fixes/MISPRINTS_5.json` |
| `FIXLOG_5:NNNN`, `FIXLOG_5_CURRENT:NNNN`, `HANDFIX_5:NNNN` | One-based JSONL record NNNN in the corresponding member under `fixes/` in `SGA5_FR.zip` |
| `path#N` | One-based record N of the named original or generated table; the change-log report specifies its exact source archive |
| `conventions/GLOBAL_ISSUES_SGA.md:N` | Numbered issue N in the French source archive's conventions register |
| `READERS-FR-*`, `READERS-EN-*` | Root `READER_ASSEMBLY_DECISIONS.tsv` and complete reader change tables |
| `FRDIFF-*`, `ENDIFF-*` | Their decision tables under `work/contributions/changes/` and `work/contributions/changes_en/` |
| `EN-INHERITED-0046-P43` | Root open-item table, `work/build/prepared/EN_wrapper_editorial_extractions.json`, and original English removed-reader-prose record SGA5-READER-PROSE-002 |

The final French citations use exact source-layer witnesses. A legacy register citation remains only after both complete old/new record strings locate uniquely on the original source folios and a changed component overlaps both witnessed variant intervals. The English citations use independently replayed edit components, preserving every original input edit and the exact unchanged gaps.

Earlier heuristic citation strings remain solely as explicitly labelled prior evidence in resolver reports. The final ordered variant ledgers and printed apparatus carry the resolved citations.
