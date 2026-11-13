# SGA 5 — French and English readers

Eight complete single-file LaTeX sources and eight PDFs are supplied: three readers and one annotated master per language. The edition was built from the three attached source archives, with all 270 manifest-listed files verified by size and SHA-256. No PDF has been omitted.

## Files

`SGA5_READERS_FR.zip` contains `SGA5_FR_diplomatique`, `SGA5_FR_corrige_apparat`, `SGA5_FR_texte_de_lecture`, and `SGA5_FR_master_annotated`, each as `.tex` and `.pdf`.

`SGA5_READERS_EN.zip` contains `SGA5_EN_diplomatic`, `SGA5_EN_corrected_apparatus`, `SGA5_EN_reading`, and `SGA5_EN_master_annotated`, each as `.tex` and `.pdf`.

`SGA5_READERS_RECORDS.zip` contains this README, the required decision/change/glossary/count tables, compilation logs and summaries, the complete prepared layers and variant catalogues, exact reconstruction proofs, scan evidence, and build scripts with their outputs. The `work/` layout is retained for the rebuild driver. Its root `MANIFEST.tsv` records package paths, bytes and hashes.

## One master for each language

Every body difference is a balanced `\SGAvar{printed}{corrected}{id}` call in the language's annotated master. `SGAform=0` selects the diplomatic argument; `SGAform=1` selects the corrected argument and a linked apparatus call; `SGAform=2` selects the corrected argument without editorial calls or apparatus. The three reader sources have identical content after the two-line form header. Each master defaults to form 1. The extracted master PDF and corrected-reader PDF texts agree exactly.

There are **1,061 French** and **879 English** variant calls. Every call has a source and both complete TeX readings; PDF extraction verifies every apparatus ID, its order, and its printed number. The plain readers preserve the complete corrected authorial body, original footnotes, proofs, references and both indexes. Thirty readings requiring unavailable scans are recorded separately in each corrected volume, with both alternatives and a reason; they contribute no variant call because the retained body readings agree. English has one additional inherited editorial note from I 4.6, folio 43, moved verbatim out of all reader bodies into the corrected-only unresolved appendix. The original removed-reader-prose record and the exact deletion/reinsertion ledger document this relocation; there are therefore 31 English unresolved notes.

The English independent audit proves byte-exact projection of both bodies and preserves all 875 original input variants through 843 exact edit components. The French audit enumerates every raw serialization discrepancy: initial empty lines, the discarded display-math endline on p. 52, redundant paragraph-ending lines at pp. 73 and 204, and the comment/argument boundary on p. 248. Each has a specific TeX token or mode proof. There is no blanket whitespace equivalence rule in this audit. A reproducible pdfTeX token probe is included for p. 248. The final reader-body assembly is also reversed explicitly and compared with the master.

## Folios and missing front matter

French retains all **483** source folio markers, in their supplied order, with scan index = folio + 11. The print repeats 434 in the place of 435; the next marker is 436. The prefaces and a margin notice at that jump explain the repetition.

English has **793** source-supported section, paragraph or formula anchors on **479** distinct folios. Folios **94, 399, 411 and 413** have no safe independent English marker at the exact source boundary, so no interpolated marker is invented. The alignment table records every anchor and its method. Repeated anchors for the same printed folio are intentional. The English change log uses surrounding validated anchor bounds when a change has no uniquely exact folio.

The original title page, L. Illusie's Introduction (iii–viii), the Liste des SGA and the original Table des matières were not transcribed in the supplied sources. Their missing text is not reconstructed. New title/credit/preface pages are identified as this reader edition, and each table of contents is generated from the headings actually present. The supplied body from Exposé I through XV and both indexes is retained in full.

## Scan decisions and other editorial decisions

All **32** specified RΓ places on printed pp. 457–474 were read in the supplied scan strips and crops. Each has an upright R with two underlines. The diplomatic branches use `\underline{\underline{\mathrm{R}}}\Gamma`; the corrected branches use `\mathrm{R}\Gamma` under GLOBAL_ISSUES 98. Attached scripts are kept inside each complete variant so they remain attached to Γ. R98-18 on p. 460 also has the double underline. The separate plain-RΓ occurrence on p. 461 lies outside this list and remains plain. `PLACES_98_DECIDED.tsv` gives images, regions, readings and reasons; the evidence directory includes all 32 crops and overview sheets.

The new corrected French source has exactly 35 declared changes from the supplied current layer: the 32 scan readings; OPEN-H75 on p. 433 (`F'/G` → `f'/G`, by the explicitly defined induced endomorphism); SOL-EN-084 on p. 472 (`F` → `F_ν`, by the immediately preceding component formula, with the scan confirming printed F); and GLOBAL-98b on p. 441, where the supplied printed Frobenius glyph is retained pending its unavailable scan. The last is a retained reading in both branches, with the alternative in the unresolved notes. The diplomatic French source has exactly the 32 scan changes.

`OPEN_ITEMS_DECIDED.tsv` has **157** explicit dispositions, covering all six REVIEW questions, the 89 English SOL observations, open merge/report items and relevant global issues. Eighteen Spanish-only observations are explicitly recorded as outside these French/English readers. Every decision gives its reason and affected forms. Stale “open” wording and superseded port decisions are reconciled to the later named evidence.

## Applied-fix inheritance

The French audit checks **4,173 diplomatic fix-log records**, **3,770 corrected fix-log records**, including **29** `misprint_correction` records, **88 hand records**, **36 resolved replay items**, and **8 findings in seven manual files**. The resulting inheritance table has **8,084 rows**. It verifies the manifest identities of the supplied final layers, replays every additional build edit, and records literal, contextual, scope or supersession evidence for every fix record. The independent master projections extend that proof into the readers. The audit also records all **117 reconciliation dispositions**.

The 590-item misprint register has no uniform status field. It provides 512 literal/projection witnesses in current and 78 entries requiring descriptive or supersession context. These figures do not mean that every proposed registry correction was inserted. Two historical p. 109 fix-log records cite an intermediate title with a final stop; the supplied final source omits that stop. Both discrepancies are documented, and the authoritative final text is retained.

The English port audit accounts for **1,856** records: 735 exact retained readings, one verified later port operation, 42 covered records, 67 readings with named later repairs, and 1,011 recorded not-applicable items; no port record remains unresolved. Exact replay applies 398 common operations at 515 occurrences, followed by the 95 input variants that change corrected source, to reproduce the frozen corrected English. Source-to-final links and all original port row IDs remain available.

## Change logs and glossary

`CHANGES_FR.tsv` contains **20,377** complete rows and `CHANGES_EN.tsv` contains **4,205**. These tables include source changes, exact body extraction, representation changes and final reader assembly. The French starting branches are August `o`, `c5`, `c4` and supplied current; the English starting branch is the released source. All five complete chains reconstruct the delivered corrected-reader `.tex` bytes exactly. `COMPLETE_READER_CHANGELOG_REPORT.md` explains the stages, and the reconstruction JSON records every source/final hash. Original CRLF bytes are preserved inside quoted TSV cells; read with a TSV parser opened using `newline=''`.

The glossary contains **320 rows**, including all **108 paired term/notation index entries** and the observed forms in **131 audited body phrase families**. `GLOSSARY_INCONSISTENCIES.md` lists the **65** families with multiple observed English forms and distinguishes contextual constructions from slips by their cited occurrences. Five documented lexical repair operations make 13 replacements. Counts are literal occurrence counts under each recorded phrase pattern; index rows retain their exact paired TeX. The coverage audit and contexts make the vocabulary scope explicit.

## Compilation and visual checks

Every file was compiled in three pdfLaTeX passes with a fixed build epoch. All eight compilations finished with **zero LaTeX errors**, **zero missing-character diagnostics**, and no undefined-reference warning. Remaining diagnostics are retained in full in `build_outputs/`.

| File stem | PDF pages | LaTeX errors | Warnings | Overfull boxes | Underfull boxes | Missing glyphs |
|---|---:|---:|---:|---:|---:|---:|
| `SGA5_FR_diplomatique` | 318 | 0 | 59 | 5 | 2 | 0 |
| `SGA5_FR_corrige_apparat` | 594 | 0 | 60 | 7 | 1 | 0 |
| `SGA5_FR_texte_de_lecture` | 318 | 0 | 58 | 4 | 2 | 0 |
| `SGA5_FR_master_annotated` | 594 | 0 | 60 | 7 | 1 | 0 |
| `SGA5_EN_diplomatic` | 325 | 0 | 63 | 4 | 1 | 0 |
| `SGA5_EN_corrected_apparatus` | 557 | 0 | 66 | 6 | 2 | 0 |
| `SGA5_EN_reading` | 325 | 0 | 62 | 3 | 1 | 0 |
| `SGA5_EN_master_annotated` | 557 | 0 | 66 | 6 | 2 | 0 |

French files have 52 hyperref PDF-bookmark warnings about mathematical tokens; English files have 55. English also retains three source `scriptsize`-in-math font warnings. The remaining counts above are line-spacing/overfull-box diagnostics. They are reported rather than suppressed. Visual inspection covered title/credit pages, generated contents, ordinary mathematical pages, the folio gap, the RΓ passages and scripts, both indexes, apparatus opening/long entries/scan entries, and the separate unresolved notes. The final check verifies the complete printed apparatus ID sequence and matching master/reader text.

## Rebuild

For an individual reader, place its single `.tex` file in a directory with a standard TeX Live installation and run `pdflatex -interaction=nonstopmode -halt-on-error FILE.tex` three times. Its packages include the usual AMS packages, Babel French/English, Latin Modern, geometry, microtype, tikz-cd, hyperref, marginnote, fvextra, xparse and needspace; the English source also uses ulem. No external source inputs or images are needed to compile a reader.

For the full source build, extract the records archive, place the original three supplied archives in the directory documented by `REBUILD.md`, then run its included rebuild driver. The original private `source_path` fields are not republished. The driver verifies source manifests, uses the retained reviewed decision catalogues, regenerates the prepared layers and masters, audits the results, reconstructs the change logs, compiles all eight files, and rebuilds package manifests. Scan judgments are preserved as explicit inputs with their evidence and exact offsets. The scripts stop on a failed hash, range, count or reconstruction.

An isolated source rebuild started with only implementation scripts, the declared reviewed inputs and the original three archives. It verified all 270 manifest members and reproduced all eight reader/master LaTeX sources, both frozen English sources, the French prepared layers and the final glossary byte for byte. All five complete reader reconstruction chains passed again. The isolated run stopped after source reconstruction; the eight PDF compilations reported above were performed separately on these identical final sources. The full report is `work/contributions/packaging_audit/FINAL_SOURCE_REPRODUCTION.json`.

## Record path conventions

Paths beginning `fr/`, `fr_baseline_aug2026/`, `fixes/`, `conventions/`, `reports/` and the original corpus-record paths refer to members of `SGA5_FR.zip`. Paths beginning `en/` and `port/` refer to `SGA5_EN.zip`; original `scans/`, `checker_crops/` and `tex_pages/` refer to `SGA5_SCANS.zip`. In contribution reports, `prepared/` maps to `work/build/prepared/`, `scripts/` to `work/build/scripts/`, and `english/`, `audit/`, `decisions/`, `validation_fr/`, `validation_en/` to the corresponding `work/contributions/` directory. Root copies of `FR_SOURCE_WITNESSES.json` and `EN_variants_input.json` resolve the apparatus's short citation basenames; `SOURCE_IDENTIFIERS.md` specifies the record-number conventions. The standalone change utilities retain their own explicitly documented CLI layouts. Exact root delivery tables supersede the earlier source-only tables retained inside the contributions directories.

## Credits and rights

Each source and PDF carries the bibliographic and contributor credits from the supplied records, all 37 named human contributions, the required wording “AI-transcribed”, “AI-translated” and “AI-produced corrections”, and the requested rights statement in its language. This build is credited to GPT-6 Astra (OpenAI, ChatGPT Pro mode). The credits audit verifies the exact English rights statement and French translation across all eight source files. Original authors' rights and the stated CC0 dedication for rights actually held are preserved.

Only archive-relative paths appear in the published records. Temporary compiler files and source records containing private machine paths are excluded. Package integrity and privacy reports accompany the final delivery. Checkpoints preserve successive completed readers; these final three packages supersede them.
