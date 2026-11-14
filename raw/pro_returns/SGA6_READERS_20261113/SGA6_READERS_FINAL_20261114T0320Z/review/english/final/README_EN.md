# Final English release handoff

The complete English edition is ready for archival. Exact artifact hashes, source hashes, audit links and the bounded gate definitions are in RELEASE_STATUS.json.

## Books and diagnostics

| Form | Pages | Compiler exits | Remaining underfull paragraphs | Other final diagnostics |
|---|---:|---|---:|---:|
| annotated_master | 561 | 0 / 0 | 5 | 0 |
| diplomatic | 388 | 0 / 0 | 4 | 0 |
| corrected_apparatus | 561 | 0 / 0 | 5 | 0 |
| reading | 387 | 0 / 0 | 4 | 0 |


All four standalone TeX files contain no external input/include/graphics commands. Standard TeX packages remain runtime dependencies. The annotated-master and corrected-apparatus TeX files have identical bytes; the diplomatic and reading forms differ only by the one master form switch. Original Introduction, authors' and editors' notes, additions, indexes and original front/rear matter remain in every form.

The full two-pass compiler receipts are in final/EN_CANDIDATE_BUILD_STATUS.json; the four diagnostic logs are sanitized. Final passes have zero errors, zero overfull boxes and no other compiler warnings. The five distinct underfull paragraphs were individually viewed and remain legible without clipping or overlap. First-pass rerun warnings are preserved in the receipt and disappear in the second pass.

## Complete source transfer

The edition contains all 700 numbered folios and all 20 original front/rear leaves, with 720 unique source comments and generated-marker calls in original order. Six certified blank labels are suppressed while their comments/calls remain. The original notice that Exposé XI was not written up is retained; no XI body is supplied.

The 142 exact translated spans are backed by manually compared passage records and sealed contributions. The aggregate ledger contains 6060 attributed rows. Every original author-note command has the same folio and label key as the reviewed French in both branches:111 commands per branch. That count includes repeated calls and split call/text helpers.

There are zero unexpected mathematical units in either branch. Exact disjoint counts follow:

| Branch | Within numbered folios | Cross-folio equation | Original front/rear | Total of these scopes |
|---|---:|---:|---:|---:|
| current | 22414 | 1 | 10 | 22425 |
| diplomatic | 22411 | 1 | 10 | 22422 |


The cross-folio unit is equation 1.3.9 across 526/527; its nonprinting-comment projection has an exact inverse. The 156 complete lexical pairs and 532 approved difference-side units record translated words or the explicit wrapper transports inside formulas. They are not counts of independent mathematical corrections.

All 699 numbered-folio joins are recorded. The 192 repaired separator boundaries plus the special visible 527 marker preserve every nonwhitespace token and pass forward/reverse reconstruction. The sealed front/rear packet separately records 18 internal joins.

The typography pass maps 387 outer source groups,77 ordinary numeric labels and 49 numeric-only structural headings. It preserves the six plain nested terms, eight plain resp. tokens,21 corrected/20 diplomatic plain locator occurrences, and the two explicitly ruled resp. tokens at 567. No nested underline wrapper remains.

The static macro audit records 1306 equal page/command groups and 11 approved lexical groups:20 red invocations, two longg invocations and four naif invocations. MACRO_EXPANSION_CLOSURE.json supplies the precise object-preserving or lexical disposition of every unequal group. The restored Gl and double-struck coefficient expansions now compare equal to the source. Actual local TeX state capture for all 691 variants is a separate recorded mechanism. The static parser is not presented as a complete TeX interpreter.

## Apparatus and exhaustive change log

The 691 genuine printed/current variant groups are classified as 510 source-misprint corrections,45 mathematical-source corrections,128 explicit notation conventions and 8 adjudicated source corrections. APPARATUS_COUNTS_EN.json links the independently resolved primary and related source IDs and per-exposé matrix. Complete diagrams or indivisible formulas may carry several source differences within one group. Unchanged-English French spelling repairs and unchanged author assertions have ledger dispositions and create no variant entry.

CHANGES_EN.tsv includes every literal difference between the exact released 07_SGA6_EN_CURRENT_LAYERED_READER.tex and the final corrected-apparatus TeX, including generated preface, credits, preamble, typography, source markers and apparatus. Its 8443 raw hunks contain 4222 line-ending-only hunks and 4221 literal-source-change hunks. Actual CRLF/LF bytes are retained; the alignment-only newline projection has its own exact inverse. Full forward and reverse file reconstruction pass. The additional 142 native-to-English span rows and 3 English-only correction rows have distinct scope labels.

## Closed glossary

The glossary has 1346 rows for 1296 French headword keys,46 admitted multiple-rendering groups and 111 cross-volume decisions. All 234 printed index rows are paired:129 terminology and 105 notation rows, including both repeated-label cases. All 5134 declared TSV input rows and 26 manual entries have dispositions. The 648/649 generization repairs are applied; no known terminology slip remains pending in this inventory.

Each glossary row declares whether its count concerns a co-attesting leaf, a paired index entry or a literal command/token use. Those measures are not added as word totals or represented as one-to-one semantic translation frequencies. Completeness applies to the declared inventories and printed indexes; arbitrary phrase extraction is not claimed to enumerate every possible technical expression.

## Rendered evidence and retained source limits

The English assembler individually viewed 28 final images:23 corrected-apparatus images and 5 reading-form images. They include original and editorial front matter, original note labels, formula/title repairs, every distinct underfull paragraph, the Introduction and four exposé starts, and three apparatus pages testing local macro states. The independent late reviewer viewed 8 further images at 7 source loci. Exact PDF/image hashes and observations are in visual_qa_final/VISUAL_QA.json and visual_qa_late/VISUAL_QA.json. No clipping or overlap was observed in these bounded checks; every output page is not claimed visually inspected.

Original-image collation is attributed to the coordinator's records/PAGES_CHECKED.tsv. Author assertions without a uniquely supported textual emendation remain in both forms, with exact counterexamples or computations in the source dossier. The final preface identifies this handling. Human credits and AI attribution are retained. Masked publisher-notice restitution is explicitly attributed to the matching 1971 LNM228 template, without claiming recovery of hidden physical strokes.

## Authoritative files

All paths below are under review/english unless otherwise stated.

| Evidence | Path |
|---|---|
| Final hashes and gate definitions | final/RELEASE_STATUS.json |
| Complete compiler receipts | final/EN_CANDIDATE_BUILD_STATUS.json |
| Every final-reader difference | final/CHANGES_EN.tsv; final/CHANGES_EN_RECONSTRUCTION.json |
| Source-linked variants and transfer | final/VARIANTS.jsonl; final/TRANSFER_LEDGER.jsonl |
| Source-span, marker and hyperlink completeness | aggregate/SOURCE_SPAN_COMPLETENESS.json |
| Literal math and crossing equation | aggregate/LITERAL_MATH_VERIFICATION.json; aggregate/CROSS_FOLIO_MATH_AUDIT.json |
| Exact single-master branches | aggregate/SINGLE_MASTER_BRANCH_AUDIT.json |
| Original note geometry | aggregate/ORIGINAL_NOTE_LABEL_AUDIT.json |
| Paragraph boundaries | aggregate/FOLIO_JOIN_AUDIT.json |
| Source-specific typography | aggregate/TYPOGRAPHY_TRANSPORT.json; EN_FONT_RENDERING_RECORD.json |
| Macro dispositions and captures | aggregate/MACRO_EXPANSION_CLOSURE.json; aggregate/APPARATUS_MACRO_STATES.json |
| Actual output observations | visual_qa_final/VISUAL_QA.json; visual_qa_late/VISUAL_QA.json |
| Glossary deliverables | final/GLOSSARY_SGA6_FR_EN.tsv; final/CROSS_VOLUME_TERMS.tsv; final/GLOSSARY_INCONSISTENCIES.md |
| Glossary evidence and seal | terminology_final/HANDOFF.json; terminology_final/FINAL_VERIFICATION.json; terminology_final/MANIFEST.json |

## Exact reproduction order

Extract all records and all ten unchanged packet closures into the common project directory, preserving their exact catalog paths and original manifest members. The native flattened source, accepted prefix span records, released baseline, reviewed French page packets and ordered amendment streams are required. All packet manifests are named in aggregate/INPUT_CATALOG.json and RELEASE_STATUS.json. There is no delivery projection or relaxed manifest check.

Run from the common directory containing en/,fr/,scripts/,build/,review/:

    python review/english/collect_english_aggregate.py
    python review/english/verify_english_aggregate.py
    python review/english/build_english_aggregate.py --final
    python review/english/audit_english_aggregate.py
    python review/english/audit_english_macro_expansions.py
    python review/english/compile_candidates.py --directory review/english/final --prefix SGA6_EN_
    python review/english/finalize_english_records.py


The supplied scripts/tex_environment.py wrapper requires its standard TeXLive environment. Do not replay historical incremental add_*.py files. finish_english_qa_records.py serializes observations already made against the listed images; it does not automatically inspect them. A different PDF hash requires renewed output inspection before a new visual receipt. Ordinary PDF builds carry generated metadata, so exact TeX reconstruction and exact archived-PDF hashes are separate recorded facts.

Original source files, old checkpoints and sealed contribution inputs remain unchanged. This English handoff is stable for final coordinator packaging.
