# Complete changes through the corrected readers

The root CHANGES_FR.tsv and CHANGES_EN.tsv include the full source comparisons, the exact body-extraction steps, all body-representation changes, and the complete assembly into the delivered corrected reader source. The five required columns are preserved. No before/after cell is abbreviated.

The stage label at the beginning of `place` identifies the source against which its byte ranges apply. These are consecutive maps, not one flat set of offsets. Start from the named original, apply its source-comparison group, then `extract`, `representation`, and `assemble` in the recorded order. Each stage and every complete chain was replayed from the written TSV with exact SHA-256 agreement.

| Language | Source changes | Body extraction | Representation | Reader assembly | Total rows |
|---|---:|---:|---:|---:|---:|
| FR | 18,023 | 3 | 1,163 | 1,188 | 20,377 |
| EN | 2,055 | 2 | 798 | 1,350 | 4,205 |

The French table has four alternative starting branches: August `o`, `c5`, `c4`, and final supplied `current`. They share the later extraction, representation and assembly stages. The English table begins with the released source. Assembly includes the new front matter, exact rights and credits, generated contents, margin folios, variant macros, apparatus and document support code. These source-code assembly differences are not counted as new mathematical corrections.

Read these tables with a TSV parser that preserves embedded newlines, for example Python `csv.DictReader(..., delimiter="\t")` on a file opened with `newline=""`. The original CRLF bytes inside quoted cells remain significant.

`COMPLETE_READER_CHANGELOG_RECONSTRUCTION.json` gives every chain, stage hash and final reader hash. `READER_ASSEMBLY_DECISIONS.tsv` gives each added extraction/assembly row an explicit decision and reason. The original stage reports and patches remain under the contributions directories.
