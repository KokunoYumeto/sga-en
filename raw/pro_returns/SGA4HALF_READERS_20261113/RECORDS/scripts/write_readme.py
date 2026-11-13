"""Write the final report from verified machine-readable build evidence."""
from pathlib import Path
import collections,csv,json,re
from edition_catalog import ROOT,COMPONENTS,all_rows

OUT=ROOT/'work/records'
def read(name):return json.loads((ROOT/name).read_text())
def rows(name):
    with (OUT/name).open(newline='') as f:return list(csv.DictReader(f,delimiter='\t'))

counts=read('work/records/RECORDS_VALIDATION.json')
verification=read('work/verification/FINAL_VERIFICATION.json')
glossary=read('work/glossary/STATUS.json')
occurrences=read('work/records/VARIANT_OCCURRENCES.json')
sol=all_rows('decisions')
reader_rows=verification['readers']

lines=[r'''# SGA 4½: scan-checked French and English readers

## Deliverable and scope

This edition contains six complete reader forms and two annotated masters, each as a single flattened LaTeX file and a compiled PDF. The French and English archives contain four source/PDF pairs apiece. The records archive contains the adjudications, page ledger, correction register, complete source-comparison logs and diffs, glossary, build scripts, machine-check outputs, and checkpoint reconciliation. Extract the three archives into the same project directory; their `deliverables/FR`, `deliverables/EN`, `scripts`, and `work` paths are complementary.

The controlling witness is the attached scan of Pierre Deligne’s *Cohomologie étale* (SGA 4½; Lecture Notes in Mathematics 569, Springer, 1977), with the collaboration of J.-F. Boutot, A. Grothendieck, L. Illusie and J.-L. Verdier. All 314 required printed text pages—III–IV and 1–312—were compared directly with the scan. The unnumbered general contents at PDF page 5 was also read and restored. The first scanned copy of the Rapport is used. For printed pages 1–109, the PDF page number is the printed page number plus 5; from p. 110 onward it is the printed page number plus 39. Introduction pages III and IV correspond to PDF pages 3 and 4.

The photographed title and copyright pages are not reproduced: the readers supply their bibliographic information and the requested current credit/rights statements instead. The second scanned copy of the Rapport is a duplicate witness, not additional authorial text, and is not repeated. No required text page, original summary, part contents, local bibliography, or authorial note is deliberately omitted. Miller’s separately identified typesetter’s note is present in diplomatic and apparatus forms, with its address removed, and omitted in the plain reading forms as their prefaces state.

## Counts and completion gates
''']
lines.append(f"- Required scanned text pages checked: **{counts['pages']} / 314**; unnumbered original contents checked additionally.\n- Sol findings decided: **{counts['sol_findings']:,} / 1,247**—**{counts['sol_verdicts']['accepted']:,} accepted**, **{counts['sol_verdicts']['accepted with a corrected reading']} accepted with a corrected reading**, **{counts['sol_verdicts']['rejected']} rejected**.\n- Independent findings: **{counts['own_findings']}**, each with an explicit reason.\n- Original-print variant occurrences and register rows: **312 French**; corresponding English variants: **218**.\n- Combined Sol/own implementation coverage: **{verification['coverage_rows']:,} two-language evidence rows**, covering every finding in each language. A no-change decision has an explicit preservation or unchanged-translation witness.\n- Final independent verification: **{verification['result']}**, **{verification['counts'].get('pass',0)} checks passed**, **{verification['counts'].get('fail',0)} failed**, **{verification['counts'].get('pending',0)} pending**.\n- Every reader PDF has **314 original-page destinations**. Corrected/master PDFs have 312 French or 218 English apparatus destinations; diplomatic and reading PDFs have none.\n")
lines+=['| Part | Printed pages | Sol rows | FR variants | EN variants |','|---|---:|---:|---:|---:|']
for c in COMPONENTS:
    pset=set(c['pages']);n=sum(d['printed_page'] in pset for d in sol)
    v=[sum(x['component']==c['key'] and x['language']==lang for x in occurrences) for lang in ['fr','en']]
    lines.append(f"| {c['name']} | {len(pset)} | {n} | {v[0]} | {v[1]} |")
lines.append('''
The independent findings comprise 44 Introduction/Ariane/Arcata findings, 59 in Rapport through Dualité, 74 in Sommes trigonométriques, 45 in Finitude/Verdier/Erratum, and one volume-wide terminology decision. Some findings cover several original pages. `PAGES_CHECKED.tsv` counts those findings on every explicitly associated page; pagewise totals are therefore not a distinct-finding total. One finding concerns the unnumbered general contents and is outside the 314-row page table.

The original Sol kind counts remain recoverable in `original_kind`: 409 word, 273 proposed print misprints, 159 symbol, 143 missing, 129 formula, 44 number, 33 accent, 24 extra, 15 punctuation, 10 font, 4 other, and 4 page-cut findings. The reviewed classification is separate; a proposal’s original label does not determine whether an apparatus entry is warranted.

## How the forms are made

Each language is assembled once into a common annotated template. Every genuine difference between the printed and corrected readings has a source-bearing variant. The only differences among that language’s four flattened files are the two mode-selection declarations, `EditionMode` and `EditionIsMaster`; this identity is independently verified after normalizing those flags.

| Form | Selected text | Apparatus | Miller note | Original page marks |
|---|---|---|---|---|
| Diplomatic | Printed reading, including established print errors | None | Retained, identified, address removed | Margin labels with original page number |
| Corrected with apparatus | Corrected reading | One entry and body mark per variant occurrence | Retained, identified, address removed | Same original boundaries |
| Reading text | Same corrected reading | None; no editorial notes in the body | Omitted and disclosed in preface | Bare original page numbers in the margin |
| Annotated master PDF | Corrected reading | Same as corrected reader | Retained | Same original boundaries |

The masters retain both readings in their TeX. The master PDF’s preface identifies its function. Transcription repairs, restored passages, translation repairs, and permitted presentation choices are common to all forms; they do not create apparatus entries. French spelling errors that do not change the English have no artificial English variant.

The apparatus gives the printed reading, corrected reading and source identifier at every occurrence. It uses ordinary typeset text/math when the fragment is self-contained. For context-dependent TeX fragments, alignment cells, or a complete diagram-bearing span that cannot safely be typeset in isolation, it gives exact, line-wrapped literal TeX. This preserves the precise reading without changing its source span. Full reasons and source context remain in `MISPRINTS_45.tsv`, the decision tables and variant records. The apparatus register is per occurrence: a repeated source identifier can legitimately have more than one separately marked site.

The original page boundaries are retained in both languages. Where a boundary is at a heading or an item label, the visible marker is placed immediately after that heading/label to avoid a detached margin mark or a page-break artifact. `PAGES_CHECKED.tsv` records the scan-established boundary, component location, actual flattened-master line and marker context, and the placement explanation. `FINAL_PAGE_MARKERS.tsv` additionally records each PDF destination and coordinates. A source-page boundary does not force a new page in the recomposed books.

## Source authority and consequential decisions

Daniel Miller’s human LaTeX rendition is the foundation of every layer. Its original repository is `github.com/dkmiller/sga4.5`; the supplied provenance records it as no longer online. The surviving copy is `github.com/NomiL/sga4.5`, commit `d5266b27ed05c1486b958f43157e27cf0723639c`. The supplied `fr/miller_src` is the comparison baseline. The two Codex trees are separate comparison witnesses. Their 475 historical decision rows are retained in `CODEX_475_CROSSWALK.tsv`; that crosswalk is not a new adjudication of every historical decision. Where the present scan review disagrees with a historical decision, the current verdict records the reason.

The prompt’s assertion that the Codex text after printed p. 65 equals Miller’s except for one box does **not** match the attached trees. They contain later content repairs. The build therefore uses and compares their actual contents throughout, and the change logs identify the before witness explicitly. The retained box around `cas` in the complex-base sentence of component 7 is a layout choice at printed p. 256, common to the French forms, with no English content difference or apparatus entry.

The historical Codex identifier `SGA45-CORR-0011` occurs twice. The first row’s proposed singular imperative is rejected where two objects are introduced; the norm-subscript correction represented by the second row is disambiguated as `SGA45-CORR-0011B`. The alias and original row are preserved in the provenance records. Other stylistic Codex changes are not promoted to print errors merely because they occur in the corrected tree.

`NOTE_45.txt` governs the distinction between content and presentation. Miller’s displays, diagram style, stable labels, equivalent macros, script sheaves, and ordinary/sheaf Hom distinctions are retained unless the print itself makes a distinction they would erase. Four Sol label-renaming proposals—`S45-SOL-0199`, `S45-SOL-0201`, `S45-SOL-0204`, and `S45-SOL-0205`—are rejected as presentation-only. The existing labels remain, and their scan-established visible numbering is shared by every form. Normal comma spacing and modern capital accents are likewise shared typography.

The review restores the missing authorial matter, including *Un fil d’Ariane*, Arcata’s foreword and contents, its comparison paragraph on p. 41, the p. 19 item, Fonctions L §4.4, the adjunction identity on p. 155, the paragraph and formula (4.14.2) on p. 203, Verdier’s subtitle and historical note, and original summaries and bibliographies. Their new English passages are marked AI-translated in the change log. On p. 216, the corrected Sommes argument now says that places of degree 1 have density 1 and that the other places may be disregarded. The diplomatic English retains the printed density error. This restores the complete argument instead of retaining the incompatible paraphrase in the supplied English.

One reference correction remains expressly **conjectural**: `S45-ASTRA-A-0034`, printed p. 70, restores the problematic “3.2.4” as references to Dualité 3.2 and 3.4. The register explains the mathematical support and the inferred separator; the apparatus labels it as a conjectural restoration. The diplomatic forms retain “3.2.4.” Other damaged or ambiguous printed strokes are resolved in their individual reasons from the neighboring text and mathematics, rather than silently guessed.

Bibliographic corrections on pp. 74–75 were independently checked against the digitized publication records: Artin’s article is from 1969, pp. 23–58; Serre’s GAGA paper occupies pp. 1–42; Giraud’s *Analysis situs* is Bourbaki exposé 256. The corresponding findings retain the printed errors in the diplomatic text and correct them in the other forms. Full source references appear below and in the findings.

## Change logs and audit files

The root-level copies of the principal tables are convenience copies of their retained `work/records` or `work/glossary` originals. Relative paths inside the project records remain valid after extracting the three archives together.

| File | Meaning |
|---|---|
| `PAGES_CHECKED.tsv` | 314 scan-reviewed pages, finding counts and French/English master locations |
| `SOL_FINDINGS_DECIDED.tsv` | 1,247 original finding identities, scan readings, image/region, verdicts, changes, affected forms and reasons |
| `CHECK_FINDINGS.tsv` | 223 independent findings, including rejected normalizations and terminology decisions |
| `MISPRINTS_45.tsv` | 312 original-print difference sites, corrections, sources and reasons |
| `VARIANT_OCCURRENCES.json` | 530 French/English component-level variant occurrences |
| `CHANGES_FR.tsv` | Corrected French differences against both Miller and Codex corrected witnesses |
| `CHANGES_EN.tsv` | Corrected English differences against the English released on 12 November 2026, including new translations |
| `work/records/diffs/` | Full, reconstructible component and paratext source comparisons |
| `CODEX_475_CROSSWALK.tsv` | Navigation from all 475 historical Codex decisions to current evidence and recorded adjudications |
| `DECISIONS.tsv` | Original page boundaries, four cut reports, notation decisions, provenance discrepancy and presentation policy |
| `APPARATUS_COUNTS.md` | Entry counts per part, language, form and recorded kind |
| `GLOSSARY_SGA4HALF_FR_EN.tsv` | French terms/notation, English renderings, reproducible counts and first places |
| `GLOSSARY_INCONSISTENCIES.md` | Every multiple rendering in the glossary, contextual decisions and documented repairs |
| `GLOSSARY_ATTESTATIONS.tsv` | Occurrence-level evidence for the glossary’s paired-page counts |
| `work/*/` | Retained review ledgers, patch arrays, restored source material, component outputs and component verification results |
| `work/build/` | Shared prepared sources, assembly records and sanitized three-pass compile logs |
| `work/verification/` | Independent final structure, variant, page-marker, coverage, privacy and targeted visual reports |
| `CHECKPOINT_INDEX.tsv` | Immutable checkpoint names, hashes, publication status and milestones |
| `CHECKPOINT_RECONCILIATION.tsv` | Every earlier checkpoint member mapped to a retained, superseding or explicitly excluded final item |
| `scripts/` | Assembly, export, compile, privacy, reproducibility and packaging programs |

Exact before/after component hunks are checked by reconstructing each compared final component. Source identifiers attached to a hunk include source-page-associated decisions; that association is evidence of the relevant review context, not a claim that every listed finding caused every character in the hunk. `CODEX_475_CROSSWALK.tsv` and the change-coverage report document the limits of that attribution. Editorial front matter, style/preamble replacement, the original contents, and typesetter-note handling are separately represented so that the component comparison is not mistaken for the whole reader diff.

## Glossary

@GLOSSARY_SUMMARY@

Counts are exact English surface-form occurrences on an aligned original page that also contains the French expression, following the supplied SGA 4 glossary’s convention. They are **paired-page attestations**, not independently aligned one-to-one translation tokens. Nested expressions can overlap, and a page may contain more than one sense. These counts must not be added as a word total or interpreted as proof that every French token received every co-attested English rendering. The retained attestation table makes the scope inspectable.

Seven Arcata noun/heading instances of unwinding(s) are changed to dévissage(s), consistently with the supplied reference glossaries and the rest of this volume. Two verbal instances of unwound are retained in their explanatory contexts. Five Rapport uses of lisse describe adic sheaves and are retained after contextual review; smooth remains the usual rendering for geometric objects. Established British/American spelling differences and context-dependent mathematical synonyms are documented instead of globally normalized.

## Compilation and final PDF checks

All eight deliverable sources are standalone flattened files using the standard `book` class and an inlined adaptation of Miller’s style. They require no sibling `.sty`, component `\\input`, external bibliography run, or scan image. The supplied build used three pdfLaTeX passes per reader. The final PDF/source SHA-256 values are captured at compile time and independently matched to the delivered artifacts.

| Reader basename | PDF pages | Errors | Warnings | Overfull boxes | Largest overflow, pt | Underfull boxes |
|---|---:|---:|---:|---:|---:|---:|''')
for item in reader_rows:
    d=read('work/build/'+item['reader']+'.compile.json')['final']
    maximum=max([float(re.search(r'[0-9.]+',x).group()) for x in d['overfull']],default=0)
    lines.append(f"| `{item['reader']}` | {item['pdf_pages']} | {len(d['errors'])} | {len(d['warnings'])} | {len(d['overfull'])} | {maximum:.5f} | {d['underfull_count']} |")
lines.append(r'''
Each final log has the same two `pdfTeX warning (font expansion): font should be expanded before its first use` notices. They concern font-expansion initialization. There are no final undefined references or citations, missing glyph warnings, duplicate PDF destinations, or rerun notices. The small residual overfull boxes are below 5 pt; they are reported rather than hidden. Underfull boxes are also counted. Earlier-pass and trial warnings are historical diagnostics, not the final compile status.

The runtime did not supply the Calligra font metric or the `stmaryrd` double-bracket package. The guarded style therefore uses script H/E/T with italic suffixes for the affected named sheaf-functor typography, and composed double brackets. The mathematical commands and distinctions remain unchanged; the fallback is explicit in `work/common/font_fallbacks.json`. A full TeX Live installation with those fonts uses them through the same guarded source. The compile driver initialized a local pdfLaTeX format and font map and set the TeX search paths for this runtime. Those generated operational files are not required inputs or distributed artifacts.

All original-page and apparatus named destinations are verified. Automatic equation destinations are unique even where the author’s visible numbers repeat. Internal link targets are resolved. Targeted visual review of 16 pages across the eight final PDFs checks covers, credits/rights, mode differences, margin page numbers, long formulas, late-category notation and final apparatus entries; additional layout trials check the difficult diagrams and displays. This targeted output inspection is separate from the complete 314-page review of the source scan. The report does not claim that every recomposed PDF page was visually inspected.

## Reproduction and retained evidence

The four original input ZIPs are needed to rebuild the source comparisons and component repairs from their witnesses. They are not duplicated in the final archives. All 1,775 input-manifest entries were checked for byte size and SHA-256 before review; `work/manifest_verification.json` records that result without private source-machine paths.

For a quick standalone build, run pdfLaTeX three times on any delivered `.tex` from its own directory. For the complete source reconstruction, put the four original archives in `upload`, extract these final archives into a common directory, and follow `work/reproducibility/REBUILD.md` and `python3 scripts/rebuild_all.py --help`. The safe unpacker verifies archive names, manifest byte sizes and hashes before extraction. The rebuild driver uses final retained ledgers and idempotent component builders, not the historical append-only recording scripts. Frozen, reviewed transcriptions and translations are explicit build inputs where applicable. Two isolated component replays reproduced all 22 component files byte for byte and left all 54 frozen inputs unchanged; see `work/reproducibility/COMPONENT_REPLAY_VALIDATION.json`. Safe extraction tests are recorded in `work/reproducibility/UNPACK_VALIDATION.json`.

Run `python3 work/verification/verify_arcata_own.py` before `python3 work/verification/verify_final.py --strict`; the rebuild driver performs both checks in that order. Add `--privacy-root` with the project-relative staging directory to include its files in the final privacy scan. The driver documentation lists the preceding component, glossary, assembly, compilation, and export steps. Scripts use their project-relative locations and do not embed the original user’s paths. Retained compile logs have absolute runtime paths and addresses removed, including line-wrapped embedded-font tokens. Final archive preflight checks safe member names, ZIP integrity, all distributable text, and PDF text/metadata.

The final records retain the current versions of checkpointed project files. `CHECKPOINT_RECONCILIATION.tsv` accounts for every earlier member by hash: unchanged, superseded by the named current artifact, or excluded with a specific reason. Superseded text files have retained unified diffs where appropriate. Temporary full-book layout trials are not additional editions; their validation reports and reusable repair module are retained. Regenerable scan rasters, local format/font caches and transfer helpers are operational material. Checkpoint candidates 07 and 08 were not published: preflight found wrapped runtime paths in 07, and residual layout-log paths and interpreter shebangs in 08. Neither candidate was uploaded, overwritten, or deleted. Candidate 09 passed preflight before archive creation. The reconciliation accounts for the earlier candidates without reproducing private path text.

## Credits and rights

Miller’s typesetting remains credited to him. Codex’s August 2026 corrections and GPT-6.1 Sol’s 12 November 2026 scan-check proposals are AI-produced corrections. The English is AI-translated. Newly restored French matter is AI-transcribed; its English is AI-translated. The second check, adjudication, reconstruction, bilingual alignment and this build are credited to GPT-6 Astra (OpenAI, ChatGPT Pro mode). The readers preserve the source-specific human credits, the supplied project’s collection-wide AI credits, and the exact requested rights statement in their respective languages. The three original English repository credit documents are preserved in `work/records/source_credits` for exact provenance.

The original work’s rights remain with its author or the author’s representatives or heirs. The supplied statement dedicates rights held in the new transcription, translation, corrections and typesetting to CC0 1.0, gives the educational/non-profit purpose and GitHub takedown route, and makes no claim to rights not held. See each reader’s full statement.

## References

Artin, M. F. (1969). Algebraic approximation of structures over complete local rings. *Publications Mathématiques de l’IHÉS, 36*, 23–58. https://doi.org/10.1007/BF02684596. Digitized publication record: https://www.numdam.org/item/PMIHES_1969__36__23_0/

Deligne, P. (1977). *Cohomologie étale* (with the collaboration of J.-F. Boutot, A. Grothendieck, L. Illusie, & J.-L. Verdier; Séminaire de Géométrie Algébrique du Bois-Marie SGA 4½; Lecture Notes in Mathematics 569). Springer. Controlling witness: attached `scan/Number32.pdf`.

Giraud, J. (1964). Analysis situs. In *Séminaire Bourbaki: Années 1962/63–1963/64, exposés 241–276* (Exposé 256, pp. 189–199; talk delivered May 1963). Société mathématique de France. https://www.numdam.org/item/SB_1962-1964__8__189_0/

Miller, D. (n.d.). *SGA 4½: LaTeX rendition* [LaTeX source]. Surviving repository snapshot `d5266b27ed05c1486b958f43157e27cf0723639c`: https://github.com/NomiL/sga4.5. Original repository recorded in the supplied provenance: https://github.com/dkmiller/sga4.5.

Serre, J.-P. (1956). Géométrie algébrique et géométrie analytique. *Annales de l’Institut Fourier, 6*, 1–42. https://doi.org/10.5802/aif.59. Digitized publication record: https://www.numdam.org/item/AIF_1956__6__1_0/
''')
glossary_summary=(f"The glossary contains {glossary['glossary_rows']:,} rows: {glossary['term_rows']:,} term/rendering pairs for {glossary['unique_french_terms']:,} normalized French expressions, plus {glossary['notation_rows']:,} named mathematical commands. "
                  f"It records {glossary['english_attestations']:,} paired-page lexical attestations and all {glossary['multi_rendering_terms']} expressions with multiple attested renderings. "
                  f"The supplementary census retains {glossary['emphasis_spans']} emphasis spans, and all {glossary['reviewed_emphasis_candidates']} residual short-expression candidates have reviewed dispositions.")
text='\n'.join(lines).replace('@GLOSSARY_SUMMARY@',glossary_summary)+'\n'
(OUT/'README.md').write_text(text)
print(json.dumps({'readme':'work/records/README.md','bytes':len(text.encode()),'verification_result':verification['result']}))
