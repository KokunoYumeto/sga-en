# SGA 4: six complete readers

Build by GPT-6 Astra (OpenAI, ChatGPT Pro mode), 12 November 2026.

Validation state: 6 of six reader PDFs have a recorded successful compile matching the current TeX source. This file is regenerated from the build records; pending checks remain visible until they pass.

Final combined verification: 81 of 81 checks passed. VERIFICATION.json contains the evidence for each gate.

## Deliverables

| Archive | Contents |
|---|---|
| SGA4_READERS_FR.zip | Three French single-file readers, the annotated French master, PDFs and this README. |
| SGA4_READERS_EN.zip | Three English single-file readers, the annotated English master, PDFs and this README. |
| SGA4_READERS_RECORDS.zip | Change logs, decisions, complete item ledgers, glossary, apparatus counts, compile diagnostics, reviewed pair data and build scripts. |

| Language | Diplomatic | Corrected with apparatus | Reading text |
|---|---|---|---|
| French | SGA4_FR_diplomatique.tex | SGA4_FR_corrige_apparat.tex | SGA4_FR_texte_de_lecture.tex |
| English | SGA4_EN_diplomatic.tex | SGA4_EN_corrected_apparatus.tex | SGA4_EN_reading.tex |

Every reader contains all three tomes and all twenty transcribed exposés, including V bis. The French master is SGA4_FR_master_annote.tex; the English master is SGA4_EN_annotated_master.tex.

Each master defaults to the corrected form with apparatus. Its accompanying PDF reuses that verified rendering; MASTER_PDF_RENDERINGS.json records the exact selector correspondence and source/PDF hashes.

## Source authority and construction

All 1,938 source-manifest entries were checked against their recorded byte counts and SHA-256 hashes before extraction. SOURCE_MANIFEST.json retains archive-relative names, roles, sizes and hashes. The source archives remain read-only.

The French diplomatic source is fr/D_diplomatic_after_scan_check; the corrected source is fr/E_corrected_after_scan_check. The untouched Orgogozo snapshot 71766d9 supplies the earlier comparison. The English baseline is en/C_release_20261112/04_SGA4_EN_COMPLETE_READER.tex, checked against the 271 native translation fragments at commit 4a4cbac and the 12 November port records.

Each language has one annotated master. The French form switch is SGAForm; the English form switch is SGAform: 0 selects diplomatic, 1 selects corrected with apparatus, and 2 selects reading text. Generated forms differ only in that selector. The corrected and reading forms select the same mathematical body. Reading forms suppress the correction apparatus, unresolved-reading appendices and Orgogozo editorial notes.

Marginal labels have the form tome:original-page; the reader’s own page numbers identify the physical book pagination. In the corrected forms, linked variant marks lead to the entry containing the printed reading, corrected reading and source ID. French uses compact numbered marks; English uses linked daggers, with the full EN-V identifiers retained in the apparatus. Disputed-place marks lead to the unresolved item record. The human editorial dossiers and original-source supplements have their own headings and provenance.

The reviewed pair files give the complete printed and corrected spans, source IDs and exact location evidence. Replacements use explicit character/token correspondences and retain source notation. Page markers that intersect a replacement follow their mapped unchanged-character boundary. APPARATUS_PROJECTION.md records the limited macro expansions used to avoid entries for invisible label changes.

## Item counts and audit files

| Corpus | Count | Evidence |
|---|---:|---|
| Printed page identities | 1,557 | PAGES.json; EN_PAGE_MARKERS.tsv; reader verification |
| Agreed transcription fixes | 898 | AGREED_TRANSCRIPTION_FIXES_AUDIT.json and .tsv |
| Agreed misprints | 930 | AGREED_MISPRINTS_PLACEMENT.json; reviewed pairs; language coverage audit |
| French agreed misprint placements marked represented | 930 | French placement ledger; final branch checks |
| English agreed misprints represented or explicitly assessed as unchanged English | 930 | EN_SOURCE_AUDIT.json, by unique MP ID |
| English agreed misprints with variants / unchanged English | 775 / 155 | EN_FINAL_DISPOSITIONS.json, with per-part evidence or common-reading context |
| French / English correction-apparatus entries | 2207 / 1956 | FR_VARIANTS.json; EN_VARIANTS.json; one entry per registered difference |
| One-model misprint judgments | 1,601 | ONE_MODEL_MISPRINTS_JUDGED.tsv: 258 Opus and 1,343 Sol |
| Accept / possible / reject | 550 / 1043 / 8 | One reason per item; possible items in the corrected-form appendix |
| Disputed items / printed pages | 643 / 443 | DISPUTED_PLACES.tsv |
| By-hand replay records | 56 | HAND_REPLAYS_PLACED.tsv |
| Held changes touching human apparatus | 18 | DECISIONS.tsv; held_apparatus_decisions.json |
| English port decisions | 583 | EN_PORT_AUDIT.tsv |
| Deferred French C records in the English port | 293 | EN_DEFERRED_FRENCH_FIXES.tsv |

The glossary contains 1,326 rows covering 1,087 distinct recorded French terms or notations; 217 have more than one observed English rendering. Its source census contains 1,769 emphasis spans and 1,753 alignment records. The extraction scope and counting rules are stated in GLOSSARY_INCONSISTENCIES.md.

The 930 agreed records are identified MP0001–MP0930 in their supplied order. AF0001–AF0898 identify the one-based lines of FIXLOG_4.jsonl. H identifiers retain the zero-based positions in REPLAY_MANUAL_4.json. OM-OPUS and OM-SOL identifiers retain each model list’s order.

By-hand replay statuses: already-present-in-corrected-reading: 30; held-disputed-page: 22; placed: 1; placed-adapted-to-existing-correction: 3.

Accepted nonhuman one-model placement statuses in French: held-disputed-page: 159; represented: 148; represented-manual: 190. Of the 550 accepted judgments, 53 concern existing human records; the remaining 497 include 338 undisputed items and 159 whose application is held on disputed pages.

The historical English port has 159 apply decisions: 157 C fixes and H33/H39. Its other decisions are 155 already and 269 not-applicable. FINAL_4.json accounts for all 898 French fixes with 549 final, 293 app_check and 56 not_in_current rows. The page-in-appcheck flag covers the 293 deferred C records plus 22 by-hand replays.

## Editorial decisions

No disputed reading was selected from an unavailable scan. The 643 records retain their item IDs, both available model readings, locations and kinds: 154 conflicts, 4 doubts, 347 one-model fixes, 84 batch cuts, 50 held agreed fixes and 4 unplaced fixes. Accepted one-model judgments on those pages remain held for application.

Orgogozo’s paired readings and N.D.E. notes are attributed as human editorial work. They remain in the diplomatic and corrected forms and are omitted from the reading forms. The 18 held apparatus changes are listed without applying them to his notes.

HUMAN_ORIGINAL_SOURCE_RECORDS.json inventories all 1,261 original active sisi records and their exact arguments, hashes and source-fragment correspondences. The transmitted D dossier has 1,258 records: three original commands were flattened before D, and 41 surviving pairs have changed raw arguments. A 44-pair original-source supplement preserves those originals in both French documentary forms. The released-English dossier has 1,171 records including its dedicated V bis rewrite; 315 original French pairs are also reproduced where a corresponding English record does not contain both original arguments verbatim. Each language separately preserves the exact original V bis p.138 printed proof and editorial rewrite.

All 129 original French editorial-note arguments are reproduced exactly in a separate attributed dossier in both diplomatic and corrected forms. Visible body-note counts are 121 diplomatic and 129 corrected in each language. Five human English notes hidden by archive-only wrappers in the release are restored unchanged to the documentary forms. The IV p.465 inline note keeps its released wording and is omitted in reading form by the same editorial selector. The two release-generated VIII reference notices remain archive-only. HUMAN_EDITORIAL_PRESERVATION_AUDIT.json records the exact source correspondence and form visibility.

Five French note arguments already differ between the supplied D and E trees. The final bodies retain the argument selected from their respective source trees; the preservation audit records the complete D/E pairs and source positions. The separate 129-note dossier retains the untouched A arguments, so these transmitted-source differences do not replace the original documentary evidence.

The commented printed diagram at I p.34 is restored. The original V bis p.138 argument appears in the diplomatic form; the existing editorial rewrite remains in the corrected body, with its source recorded. Exposés II and III use the supplied printed-page identities.

DECISIONS.tsv records the printed plain P, raised-dot and capital-label conventions; the bounded cardinal pi decision in I §§8–9; the script-C notation in V pp.65–80; Exposé IV reference prefixes; and the held phi/empty-set and equation-parenthesis questions. Every notation replacement has a bounded scope and occurrence evidence.

C293 is reconciled with MP0355. C293 repairs the site-symbol spelling; MP0355 gives V as the printed erroneous denominator and U as the correction. The induced inverse-image functor sends (W→U) to (V×_{p*U}p*W→V), so the corresponding morphism of sites goes from T/V to S/U. The diplomatic English therefore has S/V; both corrected languages have S/U.

## Change logs and terminology

CHANGES_FR.tsv contains separate comparisons against Orgogozo 71766d9 and against corrected source E. Its rows identify the page, place, before and after readings, source authority and comparison. CHANGES_EN.tsv records changes from the released English. The variant inventories preserve the full branch readings and sources.

FR_CHANGE_AUDIT.json verifies 42 complete comparisons: each of the twenty exposés against both French baselines, plus each complete source bundle against the generated corrected TeX. Forward and inverse reconstruction also pass after reading the serialized TSV. The baseline bundles preserve their source line endings and record any required privacy filtering explicitly. EN_CHANGE_AUDIT.json verifies exact reconstruction of the selected English corrected body and of the complete generated corrected source.

GLOSSARY_SGA4_FR_EN.tsv records observed French terminology or notation, English rendering, count and first place. GLOSSARY_EVIDENCE.tsv supplies paired source excerpts. GLOSSARY_INCONSISTENCIES.md lists observed multiple renderings and states the extraction scope and counting method. Existing valid technical renderings remain unless a documented slip requires a correction.

## Missing source material

The following printed summary pages were not transcribed in the supplied corpus: V p.1; V bis p.83; VI pp.163–164; VII p.341; VIII p.366; XVI p.206; XVII pp.250–251. Each tome’s original front matter and indexes are also absent. They have not been invented or reconstructed. Reader title pages, source notices, prefaces and tables of contents are newly generated and identified as this edition’s material.

## Compilation and diagnostics

The single-file readers use the system amsbook class and XeLaTeX. On a standard complete TeX Live installation, run xelatex on a reader until its table of contents and cross-references settle (the build uses repeated passes). The font setup uses the TeX Live Libertine and XITS families. Every exposé and the required local macro/style material are embedded in the reader; no companion source file is needed.

| Reader | Current source compiled | PDF pages | Errors | Warnings | Overfull boxes | Underfull boxes | Missing glyph reports |
|---|---|---:|---:|---:|---:|---:|---:|
| SGA4_FR_diplomatique | yes | 1050 | 0 | 66 | 15 | 90 | 0 |
| SGA4_FR_corrige_apparat | yes | 1684 | 0 | 66 | 29 | 412 | 0 |
| SGA4_FR_texte_de_lecture | yes | 877 | 0 | 66 | 21 | 87 | 0 |
| SGA4_EN_diplomatic | yes | 1008 | 0 | 57 | 152 | 20 | 0 |
| SGA4_EN_corrected_apparatus | yes | 1413 | 0 | 57 | 159 | 345 | 0 |
| SGA4_EN_reading | yes | 863 | 0 | 57 | 156 | 27 | 0 |

COMPILE_STATUS.json records the source/PDF hashes, pass return codes and diagnostic lists. Complete sanitized engine logs accompany it. Box warnings are reported separately from compilation errors. A PDF is considered current only when its recorded source hash matches the delivered TeX, its pass succeeds, and it has no errors, missing characters, or unresolved-reference/rerun warnings.

PDF_PAGE_MARKER_AUDIT.json checks the rendered marginal page labels against all 1,557 supplied page identities, in order, in each reader. PDF_ORIGINAL_PAGE_LOCATIONS.tsv maps every original page to its physical PDF page and label coordinates. Per-reader PDF_QA records check full text bounds, contents entries, and representative rendered pages; the bounds check includes text beyond the page crop.

The isolated execution environment required a local TeX format/font-map repair. The optional tex_environment.py helper detects those prepared repair assets; a normal TeX Live installation uses its ordinary environment. No system class or system files were modified.

## Rebuilding from the attached sources

Use Python 3 and a complete TeX Live installation. The rendered-PDF audits also require PyMuPDF (imported as fitz) and Poppler’s pdffonts command. Place only the three original source ZIP archives in upload beside build_scripts: extract_sources.py expects a root MANIFEST.tsv in every upload/*.zip. No scan images are required or assumed.

Restore SGA4_READERS_RECORDS.zip into the rebuild workspace using this mapping:

| Archive member | Rebuild location |
|---|---|
| build_scripts/... | build_scripts/... |
| shared/... | output/shared/... |
| Every other member, preserving its relative path | output/records/... |

The complete records directory is a required reconstruction input. In particular, retain EN_MISPRINT_LANGUAGE_ASSESSMENT.json, HUMAN_ORIGINAL_SOURCE_RECORDS.json and OM_1326_SCOPE_DECISION.json, together with all reviewed pair files and human-source supplements in output/shared. These contain the recorded editorial decisions.

```sh
python build_scripts/extract_sources.py
python build_scripts/judge_misprints.py
python build_scripts/shared_records.py
python build_scripts/build_fr.py
python build_scripts/build_en.py
python build_scripts/en_manual_pairs.py
python build_scripts/en_composed_reviews.py
python build_scripts/en_dispositions.py
python build_scripts/en_glossary.py
python build_scripts/finish_records.py
python build_scripts/audit_fr_t3.py
python build_scripts/audit_transcription_fixes.py
python build_scripts/audit_en_reviewed_pairs.py
python build_scripts/audit_en_auto_t3.py
python build_scripts/audit_en_om_branches.py
python build_scripts/human_preservation_final.py
```

Ordinary reconstruction uses the included reviewed pair files and documentary inputs. Their generators and audit scripts are supplied with the recorded outputs. Some research-stage generators require the specific intermediate snapshots named in their code; the ordinary rebuild recipe reuses their reviewed outputs. build_fr.py automatically runs the full French change-register audit, build_en.py regenerates the English change comparisons, and en_glossary.py regenerates the glossary source-span records.

Compile all six generated TeX files, then regenerate the PDF QA, reports, master renderings and page lookup before the final verification and packaging:

```sh
python build_scripts/fr_compile.py SGA4_FR_diplomatique 3
python build_scripts/fr_compile.py SGA4_FR_corrige_apparat 3
python build_scripts/fr_compile.py SGA4_FR_texte_de_lecture 3
python build_scripts/en_compile.py diplomatic --passes 3
python build_scripts/en_compile.py corrected_apparatus --passes 3
python build_scripts/en_compile.py reading --passes 3
python build_scripts/fr_pdf_qa.py
python build_scripts/en_pdfqa.py
python build_scripts/build_reports.py
python build_scripts/finalize_master_pdfs.py
python build_scripts/audit_pdf_markers.py
python build_scripts/verify_readers.py
python build_scripts/package_outputs.py --final
```

## Credits, rights and privacy

The readers credit M. Artin, A. Grothendieck and J.-L. Verdier, the contributors named in the supplied records, and Fabrice Orgogozo for the LaTeX edition at commit 71766d9. They identify the later layers as AI-transcribed, AI-translated and AI-produced corrections, and credit this build to GPT-6 Astra (OpenAI, ChatGPT Pro mode).

The rights in the original work belong to its author or the author's representatives or heirs. Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, they are dedicated to the public domain under CC0 1.0. This edition is published for educational, non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and object to its publication here, please open a GitHub issue and we will take it down.

Source references in these deliverables use archive-relative paths. Personal filesystem paths and email addresses are omitted. CHECKPOINTS.json records the completed-reader checkpoints and artifact hashes.
