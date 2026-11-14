# SGA6 checkpoint15 — completed English and combined release gates

This numbered archive is an exact delta over SGA6_READERS_checkpoint_14.zip. Extract checkpoint14 first, then checkpoint15 into the same directory. The overlay supplies every file needed by the completed release plan. Both archives and their manifests are immutable. The final three release ZIPs are also delivered separately.

The following shared release documentation describes the completed books and their evidence.

# SGA 6 — French and English readers

The release contains six readers and two annotated masters, with all eight standalone LaTeX sources and all eight compiled PDFs. All 720 original scan leaves have completed review dispositions. All historical decision queues are decided. The limitations of retained source passages and the attributed publisher-notice restitution are stated below and in the reader prefaces.

## Archives and opening the books

- SGA6_READERS_FR.zip: readers/fr/final/, containing the French diplomatic, corrected-apparatus and reading forms, plus their common annotated master; each has a PDF.
- SGA6_READERS_EN.zip: review/english/final/, containing the corresponding English forms and annotated master; each has a PDF. It also carries the entire unchanged manifest closure of the ten sealed English reconstruction/evidence packets at their recorded paths.
- SGA6_READERS_RECORDS.zip: the decision tables, complete change logs, glossary, source-transfer evidence, captured glossary inputs, build scripts and sanitized build diagnostics.

Extract all three archives into the same directory to retain the recorded relative paths. Each archive has a MANIFEST.tsv with path, source, bytes, SHA-256 and role. Each also carries this README. All eight requested PDFs are included; none is omitted for size.

## Completed page and decision review

| Record class | Completed | Pending |
|---|---:|---:|
| Original scan leaves |720|0|
| Checker findings |3751|0|
| FIXLOG rows, both French branches |5513|0|
| Historical misprint-register records |724|0|
| Replay records, including four already resolved historically |20|0|
| Hand-placed findings |7|0|
| Rejected Codex records |141|0|
| HOLD-tree differences |119|0|

The scan comprises 14 front leaves, folios 1–700, and 6 rear leaves. PAGES_CHECKED.tsv has 720 rows, with image/region evidence, finding counts and an exact line location in both final annotated masters. Its numbered-page relation is original PDF page = folio+14. The source comments preserve scan indices 0–719 in order. The missing folio 690 marker has been restored. Source-certified blank leaves keep their marker comments; they add no empty visible margin label.

The aggregate tables contain 9,264 FINDINGS_DECIDED rows, 966 MISPRINTS_6_DECIDED rows, 1,923 own findings and 226 convention/boundary decisions. The misprint table includes 724 historical records and 242 additional explicit source-error dispositions. These are record counts; their grouping in the apparatus is separately recorded.

OPEN_ITEMS_DECIDED.tsv contains the 16 originally open replay items plus 7 manual findings. PRIOR_RESOLVED_REPLAY_REVIEW.tsv preserves the four already-resolved replay items and their second review. CODEX_DECIDED.tsv contains 141 rejected Codex records and 119 HOLD differences. Every imported duplicate has an explicit merge resolution. No verdict is left pending.

## Construction and correspondence of forms

The French builder applies the exact reviewed patches to both attached French layers. There are 4,992 applied branch patches, four already-present applications and zero blocked anchors. The final typography applications include 930 applications from the completed convention pass and 98 applications for 49 numeric-only headings in both branches. All patches retain their old/new strings, expected counts, source IDs and reasons.

Each language has one annotated master. Its literal diplomatic and corrected alternatives determine all three forms through a form switch. The diplomatic form selects the source reading; the corrected-apparatus form selects the corrected reading and prints the corresponding source-linked entry; the reading form selects that same corrected text while omitting the new apparatus. The Introduction, original author/editor notes, tables, indexes and transcribed publisher matter remain in all three forms.

The French exact branch reconstruction, actual final-master body comparison and all 720 original markers pass. The English checks likewise reconstruct both source branches and show that the three rendered sources differ by the master switch. Original author-note commands and their 111 label/geometry keys agree with the reviewed source in both English branches. Captured macro states at each variant preserve the locally active meanings when alternatives are printed in the apparatus.

Generated layout transports have explicit inverses: heading boxes retain their literal contents; source-folio labels attach to their opening headings; each of the fourteen written exposés begins on a fresh output page; and the English presentation-only line breaks retain formula payloads. Exposé XI has no body and creates no opening or apparatus entry.

### Apparatus totals

| Kind | French | English |
|---|---:|---:|
| source misprint correction |755|510|
| mathematical source correction |47|45|
| explicit notation convention |131|128|
| adjudicated source correction |37|8|
| **All groups** |**970**|**691**|

APPARATUS_COUNTS.md and its complete TSV give the counts by exposé, form and kind. Every group has different literal readings and adjudicated source links. The French independent provenance audit checks all 970 groups, including repeated short-pair contexts and 90 manual full-context mappings. The English classification preserves every source ID and explicit related source.

### English transfer and terminology

The English reconstruction uses 142 exact reviewed native-source spans covering all 720 original leaves. TRANSFER_LEDGER.jsonl retains 6,060 attributed correction/typography/aggregate rows. The two complete mathematical branches have zero unexpected literal-unit differences after the 156 explicitly recorded lexical translation pairs and exact wrapper transports. The check includes starred equation environments and the complete equation crossing 526/527. All 699 numeric folio joins have recorded separator comparisons and inverse-checked whitespace transports.

The glossary contains 1,346 rows; all 234 printed terminology/notation index rows are paired and adjudicated. GLOSSARY_INCONSISTENCIES.md records 46 admitted groups with more than one English rendering. CROSS_VOLUME_TERMS.tsv and CROSS_VOLUME_DECISIONS.tsv record 111 decisions against the supplied SGA 4, 4½, 5 and 7 glossaries and notation records. The two reviewed générisation passages on 648–649 use generization in both English branches.

Glossary counts retain an explicit scope for each row: surface-form occurrences on a leaf that co-attests the complete French phrase, exact paired index rows, or literal macro/token uses in the declared folios. The audit accounts for every supplied inventory row and every printed index row. It does not present these different count scopes as a single word total. Detailed source and semantic attestations remain in review/english/terminology_final/.

### Literal change logs

CHANGES_FR.tsv contains 9,314 literal hunks across four independently reconstructing streams: each of the two specified before sources (Codex HOLD and the attached corrected layer) to the reviewed author-text projection, and each to the exact final corrected-reader TeX including generated editorial/apparatus material. Scope and source columns identify each stream.

CHANGES_EN.tsv contains 8,443 exact released-reader-to-final-reader hunks, including 4,222 reversible line-ending hunks and 4,221 other literal source hunks. Forward and reverse reconstruction both pass. The 142 native-to-reviewed translation spans and the separately recorded English-only corrections are additionally labelled by their own scope and baseline. Their before/after text is complete.

## Source passages retained after adjudication

The decisions on 431, 443 and 590–592 include explicit counterexamples to the examined printed assertions. A unique authorial textual repair was not established, so those passages remain verbatim in the French author text and faithfully translated in English, in all forms. The source blanks for references on 464 and the integral-group memberships on 465 are also retained. The 465 record supplies the rational construction and states exactly what the available argument establishes. These are completed retention dispositions; unchanged passages create no diplomatic/corrected variant.

The full calculations, source images/regions and reasons are preserved in review/final_dispositions/ and the underlying decisions. The prefaces make these limitations visible to readers. This release does not claim a replacement theorem for any of those passages.

## Notation conventions and exact identifications

The complete source policy is review/global_conventions/CONVENTIONS_SGA6.md, supplemented by review/global_numeric_headings/. Required GLOBAL_ISSUES 76, 81, 82, 84, 86, 87, 88 and six NOTE_6 supplements are decided. Each scope is tied to observed occurrences; no blanket glyph substitution is inferred from a mathematical role.

- Raised K/Gr dots, lower complex/coherent-group dots, genuine primes, Tate/cohomological asterisks, baseline series dots and completion placeholders retain their observed positions and local scope.
- Source word rules use upright underlined lexical groups. Individually ruled mathematical letters, double rules and primes outside the rules retain their own commands. Plain defined terms, reference numerals and resp. tokens follow the documented exclusions. Ordinary item and paragraph labels use ordinary weight; NOTE_6 statement-label styling remains explicit.
- Category/site glyph transports fix the already-bound objects and morphisms. The named filtered category fixes its groups, filtration subgroups and filtration-preserving maps. For the graded category in V, the degree-filtration functor j and associated graded Gr are recorded; the map B→Gr(jB) sends each homogeneous element to its class of the same degree, with the inverse taking that class back to the element.
- The small exterior wedge fixes each elementary exterior tensor in the same alternating quotient, including degree and Module argument. The wedge-shaped algebra name in V 356–360 fixes the named augmented lambda-ring, its multiplication, augmentation and lambda operations. The source-specific choice of ordinary atom versus operator is retained.
- For derived tensor notation the documented fixed representative P gives the identity chain map on P⊗F; for a derived image a fixed injective representative I gives the identity on f_*I and its cohomology. Locally declared double-rule/double-struck representations preserve those same objects and maps. Symmetric-algebra letter transports fix the graded algebra and therefore the degree-zero affine charts and the projective bundle obtained by gluing them.
- Hom, Isom, Proj and Pic rules follow the source occurrences. Wavy Picard-functor rules and neighboring scheme-letter rules remain visible. Their representability relation is the recorded natural identification of T-points with the functor values. The structure-sheaf O, XIV phi, c-ell/cl, n°, Ob/ob, Ab.fil. punctuation and macro resets follow their source-scoped decisions.
- The explicitly admitted coefficient-field spelling sends every rational number to itself and preserves addition and multiplication. Double-struck coefficient letters, plain/script exceptions, Gro and all later macro states have their local source declarations and exact English transports recorded.

## Original front/rear matter and attributed restitution

The original cover, title/colophon, preface, Introduction and contents are transcribed. The rear leaves retain 188 catalogue entries and the two ISBN lines; the two blank rear leaves keep their source markers. Bibliographic data identify Lecture Notes in Mathematics 225, Springer, 1971, and all named volume authors and collaborators.

The inside-cover publisher notice is partly hidden by an attached label in the scanned copy and has no matching witness leaf. Its obscured wording is an explicitly attributed restitution from the corresponding 1971 Springer Lecture Notes in Mathematics 228 notice, whose 17 visible comparison points agree. The covered physical strokes of the SGA 6 copy have not been recovered. Evidence, comparison tables and the source PDFs are retained in review/publisher_notice_recovery/.

Institutional stamps, barcodes, handwritten prices, attached labels and other copy-specific marks are omitted as documented; nontextual publisher logos are omitted. No printed author/editor text, original note, Introduction, index entry, catalogue entry or ISBN is intentionally removed from the reading form.

## Credits and rights

Each reader preserves the human contributions and source attributions specified in the supplied English repository records and SOURCES.md, including the named original authors/editors and credited transcription, typesetting and English-source contributions. Source attribution remains attached to inherited English formulations.

The edition uses the required wording AI-transcribed, AI-translated and AI-produced corrections. It credits Codex’s August 2026 layers/corrections, Claude Opus 5.5 at effort max for the 10–13 November 2026 numbered-page review, and this build to GPT-6 Astra (OpenAI, ChatGPT Pro mode). Both languages carry the exact requested rights statement in their respective prefaces, including the conditional dedication of rights actually held under CC0 1.0 and the requested GitHub-issue takedown contact.

## Compilation and rendered checks

| File | PDF pages | Passes | Errors | Warnings |
|---|---:|---:|---:|---:|
| SGA6_FR_master_annote.tex |553|2|0|0|
| SGA6_FR_diplomatique.tex |390|2|0|1|
| SGA6_FR_corrige_apparat.tex |553|2|0|0|
| SGA6_FR_texte_de_lecture.tex |390|2|0|1|
| SGA6_EN_annotated_master.tex |561|2|0|5|
| SGA6_EN_diplomatic.tex |388|2|0|4|
| SGA6_EN_corrected_apparatus.tex |561|2|0|5|
| SGA6_EN_reading.tex |387|2|0|4|

All eight final sources compiled in two passes with zero errors and unchanged source hashes during compilation. The French diplomatic and reading forms each report one 2.18752 pt vertical-box warning at output 346. Both pages were viewed: original note, bottom formula and page number remain separate with no observed clipping or overlap. The French apparatus and master have no warnings. The English receipts retain every actual remaining paragraph/box diagnostic; final targeted layout observations are supplied separately.

French final rendered QA covers 19 directly viewed pages and confirms identical extracted page text for all 553 apparatus/master pages. The English bounded late audit directly views eight output pages at seven source loci; the English owner’s final report adds front matter, title/folio alignment, original notes, macro-sensitive formulas, apparatus and remaining layout checks. These output checks supplement the recorded source collation; they do not substitute for it.

Exact path-free diagnostics are in records/COMPILE_SGA6_FR_*.json and review/english/final/EN_CANDIDATE_BUILD_STATUS.json. RELEASE_VALIDATION.json records the final 16 source/PDF hashes and the aggregate gates. Local filesystem paths and email addresses are excluded from the exported text records and readers.

## Rebuilding

1. Extract the four originally supplied input archives into a common work directory, retaining their distinct original manifests. Extract the three release archives over that directory.
2. Run python3 scripts/intake.py --archives followed by the four original archive filenames to verify the supplied manifests and regenerate the input registry.
3. Run python3 scripts/build_french.py --final. The saved review records are the authoritative exact patch inputs. Earlier observation scripts document completed image reads and do not create automatic source verdicts.
4. Run python3 scripts/compile_readers.py with the four TeX paths under readers/fr/final/. A standard complete TeX Live installation provides the required packages; the optional isolated runtime wrapper falls back to the installed environment.
5. Follow review/english/final/HANDOFF.md for the exact English collection, aggregate verification, final build, compile and record commands. The exact sealed packet paths named in aggregate/INPUT_CATALOG.json are included in the English archive. Every original packet manifest and member is retained; the original collector verification remains unchanged.
6. Run python3 scripts/merge_records.py, then python3 scripts/finalize_french_records.py. Run the English final record writer specified in its handoff. Run python3 scripts/finalize_release.py after the completed English/glossary/provenance reports are present.

A rebuild may change PDF creation metadata and engine-dependent pagination; actual compile receipts bind the delivered PDFs to the delivered TeX hashes. The source reconstruction proofs and recorded decisions remain the reproducible content checks.

## Historical checkpoints and omissions

All previously created numbered checkpoint archives and frozen stages remain unchanged. Their manifests, README files and archive hashes are retained under records/checkpoint_history/. Current files at a repeated relative path carry the completed reviewed state; prior byte versions remain in their named immutable checkpoint archives.

RELEASE_PACKAGING_PLAN.json lists every omitted generated historical PDF and every historical checkpoint path absent from this release. The final eight PDFs are retained. The ten sealed English packets additionally retain their historical probe PDFs, images and sanitized diagnostic logs as exact original-manifest members. Outside those packets, original input archives, nested checkpoint ZIPs, runtime packages, caches, raw engine transcripts, auxiliary files and reproducible scan crops/contact sheets are omitted. Exact source-image page/region evidence, review scripts, sanitized diagnostics and reconstruction inputs are supplied.
