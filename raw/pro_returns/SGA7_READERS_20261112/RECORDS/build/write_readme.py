#!/usr/bin/env python3
"""Write the delivery README from the actual edition records and build statuses."""
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'output' / 'records'
csv.field_size_limit(20000000)


def data(name, default=None):
    p = R / name
    return json.loads(p.read_text()) if p.exists() else default


def rows(name):
    with (R / name).open(newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def main():
    fr = data('FR_APPARATUS.json', [])
    en = data('EN_APPARATUS.json', [])
    ed = data('editorial_decisions.json', {})
    glossary = data('GLOSSARY_AUDIT.json', {})
    enstatus = data('EN_BUILD_STATUS.json', {})
    fc = collections.Counter(x['comparison'] for x in rows('CHANGES_FR.tsv'))
    ec = len(rows('CHANGES_EN.tsv'))
    notes = ed.get('unresolved_notes', [])
    needs = sum(n['status'] == 'needs the scan' for n in notes)
    selections = data('FR_SOURCE_SELECTION_DECISIONS.json', [])
    apparatus_selections = sum(x['id'].startswith('ADOPT-F') for x in selections)
    baseline_selections = sum(x['id'].startswith('COLLATION-') for x in selections)
    attribution = data('FR_ATTRIBUTION_AUDIT.json', {}).get('summary', {})
    apparatus_attribution = attribution.get('apparatus', {})
    changes_attribution = attribution.get('changes', {})
    en_attribution = data('EN_ATTRIBUTION_UPDATE.json', {})
    statusfiles = sorted((R / 'compile').glob('*.json'))
    statuses = [json.loads(p.read_text()) for p in statusfiles]
    def current_complete(s):
        lang='fr' if s['reader'].startswith('SGA7_FR') else 'en'
        source=ROOT/'output'/lang/s['reader']
        pdf=source.with_suffix('.pdf')
        return (s['success'] and len(s['passes'])>=3 and all(x['exit_code']==0 for x in s['passes'])
                and source.exists() and pdf.exists()
                and hashlib.sha256(source.read_bytes()).hexdigest()==s['source_sha256']
                and hashlib.sha256(pdf.read_bytes()).hexdigest()==s['pdf_sha256'])
    ok = len(statuses) == 6 and all(current_complete(s) for s in statuses)
    state = ('All six readers compile without errors.' if ok else
             'This is a source-only rebuild; PDFs have not been compiled in this directory.' if not statuses else
             'Compilation is incomplete; the status table below is authoritative.')
    pdf_contents = 'all four corresponding PDFs; ' if ok else ''
    master_pdf_note = (
        "The masters default to the corrected-apparatus form. Each master source is byte-identical to its corresponding corrected-reader source; its supplied PDF is a byte-identical copy of that source's verified three-pass PDF. `FR_MASTER_PDF_EQUIVALENCE.json` and `EN_MASTER_PDF_EQUIVALENCE.json` record the source and PDF hashes. All eight source files have corresponding PDFs; none is omitted for size."
        if ok else
        "The masters default to the corrected-apparatus form. In a compiled build, `build/master_pdfs.py` verifies source and compile-hash identity before supplying each master PDF from the corresponding corrected-reader PDF. Run the rebuild with `--compile` to produce all eight PDFs.")
    text = f'''# SGA 7 I and II: French and English readers

Edition of 12 November 2026. Build credited to **GPT-6 Astra (OpenAI, ChatGPT Pro mode)**.

{state} Each reader contains both published volumes in one standalone LaTeX file. The delivery contains two annotated masters and six form files, with PDFs in a compiled build as listed below. The original three source archives are the immutable inputs; this delivery does not redistribute those archives.

## Deliverables

| Archive | Contents |
| --- | --- |
| `SGA7_READERS_FR.zip` | `SGA7_FR_master_annote.tex`; `SGA7_FR_diplomatique.tex`; `SGA7_FR_corrige_apparat.tex`; `SGA7_FR_texte_de_lecture.tex`; {pdf_contents}this README. |
| `SGA7_READERS_EN.zip` | `SGA7_EN_annotated_master.tex`; `SGA7_EN_diplomatic.tex`; `SGA7_EN_corrected_apparatus.tex`; `SGA7_EN_reading.tex`; {pdf_contents}this README. |
| `SGA7_READERS_RECORDS.zip` | Change logs, apparatus registers and counts, glossary and attestations, decisions, provenance, source verification, compilation records, build scripts, and frozen build/intermediate data. |

{master_pdf_note}

## Witnesses and construction

The French diplomatic and current witnesses are the designated files in ZIP 1, under `fr/sga7i/` and `fr/sga7ii/`. The August witnesses in ZIP 3 are used only on the before side of the French change log. Every one of the **626 manifest entries** in the three archives passed its byte-count and SHA-256 check before extraction. `INPUT_VERIFICATION.json` contains the archive-internal member names, roles and verified hashes; private original-location fields were excluded.

Each language has one annotated master. A marked passage uses `\\SGAvar{{printed}}{{corrected}}{{group-id}}`. Form 0 selects the diplomatic branch, form 1 selects the corrected branch and its linked apparatus marker, and form 2 selects the corrected branch without apparatus. The three form files differ from their master only in this selector. The source-level form/guard checks in `APPARATUS_COUNTS.json` verify that the diplomatic and reading forms display no critical apparatus or editorial notes.

Apparatus passages are grouped at safe paragraph or mathematical-environment boundaries so that TeX constructs remain intact. Each group can contain several individually identified token changes. The apparatus gives the exact TeX spelling of the printed and corrected fragments, the original folio and the source reference. Context and exact offsets are retained in the JSON registers. A single marker therefore does not mean that several changes have been counted as one. Source-log records, source issues, variant entries, and marked blocks are separate quantities.

The French projection audit reconstructs both cleaned witnesses exactly from the annotated master, before the documented typesetting transport. It also checks the complete, ordered **528 + 438 Arabic folios**, with the transcribed Volume I introduction V–VII separately preserved. The original folios appear in the margin; the new PDF pagination is independent of them. Exposé XIII begins at II:82: its title, author and local contents were stored at the end of the supplied Exposé XII component and are placed with XIII in the readers without losing any text.

The English base is the supplied release `v2026-11-12-english-edition`, repository commit `4a4cbac`, flattened from its native components. Its corrected wording is retained except for the explicit source-backed decisions and repairs in `CHANGES_EN.tsv`. Printed mathematical and linguistic readings are reconstructed from the final paired French witnesses and the correction-port evidence. Historical intermediate replacements are not treated as the print when the final diplomatic witness gives a different reading. Formula transfer candidates received individual structural review; explicit overrides prevent changes to exponent scope, subscript scope, font arguments, delimiter placement, or TeX control-word boundaries. The paired-source reviews and dispositions are included in the records.

**Exposé VI was originally written in English.** Both language readers use the same exact diplomatic/current source pair for VI, including its {sum(e['expose']=='VI' for e in fr)} variant entries. The separately reworded released English VI is not substituted for that original English. Every difference introduced by restoring the original corrected English is recorded in `CHANGES_EN.tsv` under `ED-VI-AUTHOR`. The publisher catalogue at I:525–528, omitted from the released English reader but supplied as a native component, is restored and logged. Its multilingual titles remain as supplied.

English folios are based on unique numbered items and shared mathematical anchors. Exact source starts and catalogue boundaries are marked directly; interpolated positions are explicitly marked with an approximation sign. `EN_ALIGNMENT.tsv` distinguishes the anchor quality. These locations support navigation and do not claim a facsimile alignment to scans that were not supplied. VI retains the exact French-source folio sequence.

## Editorial and audit counts

| Quantity | Count |
| --- | ---: |
| French numbered variant entries | {len(fr)} |
| French marked variant blocks | {len({e['group_id'] for e in fr})} |
| English numbered variant entries | {len(en)} |
| English marked variant blocks | {len({e['group_id'] for e in en})} |
| French changes against August diplomatic | {fc['August diplomatic']} |
| French changes against August corrected | {fc['August corrected']} |
| French changes against supplied current | {fc['current']} |
| English change-log rows against release | {ec} |
| Explicit open-item decisions | {len(ed.get('decisions',[]))} |
| Separate retained/unresolved notes per corrected reader | {len(notes)} |
| Of those notes, marked “needs the scan” | {needs} |
| Inherited English editorial notes retained separately | {enstatus.get('inherited_editorial_notes',0)} |
| Attested French–English glossary pairs | {glossary.get('pairs',0)} |
| Distinct attested French terms/notations | {glossary.get('terms_attested',0)} |
| Paired glossary occurrences | {glossary.get('occurrence_pairs',0)} |
| French entries with multiple English renderings | {glossary.get('multiple_rendering_terms',0)} |

The **3,434 French fix-log records** are audited individually: 719 diplomatic and 1,036 current records for Volume I; 773 diplomatic and 906 current records for Volume II. `FR_FIX_AUDIT.tsv`, `FR_VERIFICATION.json`, and `FR_FIX_EXCEPTIONS.json` distinguish exact surviving replacements, later successor edits, and bulk/transformed effects. The final evidence accounts for 3,361 exact new readings, 56 successor-chain readings, and 17 transformed or bulk effects. A superseded intermediate string is not reinserted merely to make a literal search pass. The supplied historical logs are not a complete serialized history of every baseline-to-final edit; the exception record makes those limits explicit.

The corrected French differs from the supplied current layer in exactly three editorial changes: the context-specific agreement repair at I:179; restoration of the omitted quotient equality at II:353; and reversal of the unsupported pluralization at II:265 while preserving the separate mathematical correction. Their decisions and reasons are in `OPEN_ITEMS_DECIDED.tsv`.

Some genuine diplomatic/current differences cannot be assigned mechanically to one earlier fix identifier. The original {apparatus_selections} explicit apparatus source-selection decisions identify the two designated witnesses and explain the adoption of the current reading. `FR_SOURCE_SELECTION_DECISIONS.json` also preserves {baseline_selections} original baseline-collation decisions. Their scope is frozen independently of later citation repairs, and none claims a new scan inspection.

Every French apparatus attribution and change-log attribution has a separate exact-span check in `FR_ATTRIBUTION_AUDIT.json`. A historical citation must support the actual changed span on the same folio; nearby unchanged wording is insufficient. The audit repaired citation metadata for {apparatus_attribution.get('metadata_changed',0)} apparatus entries and {changes_attribution.get('metadata_changed',0)} change-log rows, without changing any body reading, entry/group identifier, or change-log ordering. Where the conservative historical match cannot be established, {sum(apparatus_attribution.get('witness_fallbacks_by_volume',{}).values())} apparatus entries and {sum(changes_attribution.get('witness_fallbacks_by_volume',{}).values())} change-log rows carry separate `WITNESS-` attributions to their exact paired sources. Their explanations are included in `FR_SOURCE_SELECTION_DECISIONS.json`; these metadata fallbacks do not enlarge the original textual ADOPT review. The audit retains the previous claims for comparison and explicitly labels unsupported citations. `FR_ATTRIBUTION_CHANGES.tsv` lists every repaired attribution. Historical fix IDs and later register indices can differ, so the audit gives the exact ZIP-internal filename and row reference for each change-log row: FIXLOG JSONL records are counted from 1, and MISPRINTS array indices from 0.

TeX-ignored whitespace changes are kept in the change and nonprinting-difference records but do not create fictitious printed variants. Genuine word-space or paragraph changes remain visible differences where applicable.

The English fix audit separates applied port operations, already-correct decisions, source-authoritative VI replacement, and later source-witness adjudications. `EN_FIX_AUDIT.json` and its companion tables report the evidence against the released components and final reader. All frozen reconstruction decisions, supersession/conflict records, and source-pair audits are supplied so that accepted and rejected heuristic proposals remain reviewable.

The final French attribution repairs propagate to {en_attribution.get('metadata_changed_entries',0)} English apparatus entries through shared VI and explicitly traced nonmath-source dependencies. `EN_ATTRIBUTION_UPDATE.json` verifies exact identity of all {en_attribution.get('parts_verified',0)} diplomatic, corrected and annotated English component bodies, every apparatus identifier and reading, and all {en_attribution.get('changes_en_rows_verified',0)} released-body change-log rows across that update. Frozen reconstruction proposals and their reviewed operation readings remain unchanged.

`APPARATUS_COUNTS.md` provides per-exposé, per-form and per-kind counts. Diplomatic and reading forms have zero visible apparatus entries. Unresolved alternatives and inherited editorial notes have their own sections in the corrected reader; they are not added to the variant count when the two body readings are identical. The plain-reading preface states these omissions.

## Open items and glossary

Every requested specific open item and the applicable low-confidence/review items in `GLOBAL_ISSUES_SGA.md` has a decision, reason, source and affected forms. `GLOBAL_ISSUES_SELECTION_AUDIT.json` records the selection. Where the supplied material cannot decide a physical reading, the body retains the attached diplomatic reading and a separate corrected-reader note gives both alternatives. The {needs} scan-dependent notes are not claimed as resolved by mathematical plausibility. The other {len(notes)-needs} retained notes concern interpretive or missing-authorial-information questions.

The glossary is an attested technical lexicon, not a count of every French word in running prose. Its counts are paired occurrences in the supplied current French and native released English source corpus, constrained by source alignment; they are not whole-book word frequencies or a recount of the final edited readers. `GLOSSARY_ATTESTATIONS.tsv` provides every counted occurrence and its source; all counts and first places are checked. The {glossary.get('multiple_rendering_terms',0)} entries with more than one attested English rendering appear in `GLOSSARY_INCONSISTENCIES.md`. Variation with a plausible mathematical, grammatical or contextual explanation is retained; no global terminology replacement is silently imposed.

The audit also inventories {glossary.get('underlined_inventory',0)} underlined source phrases and reviews {glossary.get('underlined_candidates',0)} residual compositional, grammatical or proper-name spans. The candidate and inventory tables expose the glossary's scope instead of pretending that all highlighted prose is a single technical term. Original-English VI is treated as original English, not as evidence of a nonexistent French translation.

## Missing source material and limits

The printed Volume I title/publication leaves and its separate volume contents are not transcribed in the supplied French layers. Its general introduction V–VII is present; V is inferred from the adjoining visible VI and VII. The Volume II source begins at Exposé X, folio 1, and supplies no preceding printed volume title/publication/contents leaves. Their precise wording and leaf structure cannot be reconstructed without scans. The new title pages and tables of contents are explicitly editorial. `FRONT_MATTER_INVENTORY.tsv` documents what is present and absent.

The numbering jump from Exposé II to VI is historical: there are no separately written published Exposés III–V to invent or recover from these inputs. The local exposé titles, authors, local contents, bibliographies, terminal matter and publisher catalogue supplied in the body files are preserved. No scanned pages were attached, and this build makes no claim of a new visual comparison with the original printing. Earlier provenance statements retain their own stated audit limits.

## Compilation and visual checks

The six `.tex` readers are self-contained with respect to source content: they require standard TeX Live packages, not companion source components, images or custom external style files. They use pdfLaTeX, Latin Modern, AMS mathematics, Babel French/English, TikZ/tikz-cd, ulem, adjustbox, marginnote, xurl and hyperref. The delivered builds used pdfLaTeX from the installed TeX Live 2025 development/Debian environment, with compatible standard language/font packages configured locally. No system TeX files were modified.

| Reader | PDF pages | Successful passes | Errors | Package/LaTeX warnings | Overfull boxes | Underfull boxes | Largest overflow (pt) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
'''
    for s in statuses:
        text += f"| `{s['reader']}` | {s.get('pages') or '—'} | {sum(x['exit_code']==0 for x in s['passes'])} | {len(s['errors']) if s['success'] else 'BUILD FAILED'} | {len(s['warnings'])} | {s['overfull_boxes']} | {s['underfull_boxes']} | {s['largest_overfull_pt']:.3f} |\n"
    text += '\n### Diagnostic messages by reader\n\nRepeated identical warning messages are shown once here; the counts above and complete logs retain their occurrences.\n'
    for s in statuses:
        text += '\n**'+s['reader']+'**\n\n'
        messages = list(dict.fromkeys(s['errors'] + s['warnings']))
        text += ('```text\n'+'\n'.join(messages)+'\n```\n') if messages else 'No LaTeX errors or package warnings.\n'
    text += '''
The corresponding sanitized `.log` and `.json` files in `compile/` contain the exact warnings and source/PDF hashes. An overfull-box warning is reported rather than suppressed; it is not a compilation error. The inherited footnotesize-in-math and atopwithdelims warnings arise from the supplied notation/typesetting. Missing-glyph and unresolved-reference checks, PDF geometry checks, and representative visual inspections are recorded separately. Title/contents pages, mathematical body pages, apparatus pages, and terminal pages were inspected. No claim of a pixel-level review of every page is made.

`TYPESETTING_TRANSFORMS.tsv` records the nonauthorial transport: source page comments become marginal folios; TikZ matrix ampersands receive macro-safe catcodes; blank lines inside mathematical displays are prevented from becoming paragraph tokens; wide diagrams are fitted to the text width; generated navigation and source-boundary handling are added. These transformations do not silently replace mathematical notation. Broken or uncertain printed readings are retained in diplomatic branches even where they are mathematically defective.

## Rebuilding

To compile one delivered standalone reader on an ordinary TeX Live installation, run pdfLaTeX three times on its `.tex` filename. No source archive is needed for this operation. The corrected reader's exact-text apparatus is deliberately substantial; the plain reading form is the compact corrected text.

To recreate the annotated masters and records, unpack the records archive into a directory, put the **three original source ZIPs** in a subdirectory named `upload`, and run:

```sh
python build/rebuild.py --compile
```

The script verifies and extracts the original archives, regenerates the decisions and French master, rebuilds English alignment/variants using the frozen editorial resolutions, generates the glossary and reports, compiles all six readers through the ordinary installed TeX configuration, and recreates the three delivery archives. Python build stages use the standard library; optional PDF geometry/inspection uses PyMuPDF, and compile-page counting uses `pdfinfo`. The packaged `work/*.json` files preserve the explicit reviewed decisions and intermediate evidence. They are not unexplained substitutes for the source archives.

Omit `--compile` to rebuild sources and records only. `--local-tex` is for an already prepared workspace TeX configuration, not needed on an ordinary complete TeX Live installation. `build/compile_reader.py --system-tex` can also compile any one generated reader and write a sanitized diagnostic record. The build scripts use paths relative to their own directory; source references in the records are ZIP-internal paths.

## Record guide

| Files | Purpose |
| --- | --- |
| `CHANGES_FR.tsv`, `CHANGES_EN.tsv` | Exact before/after changes with place and source. TSV fields can contain quoted tabs/newlines; use a TSV parser rather than counting physical lines. French comparisons have an additional comparison column. |
| `FR_APPARATUS.json`, `EN_APPARATUS.json`, `APPARATUS_COUNTS.*` | Individual printed/corrected entries, contexts, sources, group IDs and per-form visibility/count checks. |
| `OPEN_ITEMS_DECIDED.tsv`, `editorial_decisions.json`, `GLOBAL_ISSUES_SELECTION_AUDIT.json` | Explicit adjudications, exact body patches, retained alternatives and review-item scope. |
| `FR_VERIFICATION.json`, `FR_FIX_AUDIT.tsv`, `FR_FIX_EXCEPTIONS.json`, `FR_PAGE_MARKERS.tsv` | Exact witness projection, historical-fix evidence and full French folio coverage. |
| `FR_SOURCE_SELECTION_DECISIONS.json`, `FR_NONPRINTING_DIFFERENCES.tsv` | Witness-based source decisions and nonprinting TeX differences excluded from critical counts. |
| `FR_ATTRIBUTION_AUDIT.*`, `FR_ATTRIBUTION_CHANGES.tsv`, `FR_ATTRIBUTION_BASELINE.json`, `FR_ADOPT_COHORT.json` | Exact changed-span citation evidence, transparent attribution repairs, frozen reading/identifier scope, and the original textual-review cohort. |
| `EN_BUILD_STATUS.json`, `EN_ALIGNMENT.tsv`, `EN_FIX_AUDIT*`, `EN_*AUDIT*`, `EN_*REVIEW*`, `EN_RECONSTRUCTION_DECISIONS.json` | English release/fix verification, exact versus approximate source anchors, formula/port review and reconstruction decisions. |
| `EN_INHERITED_EDITORIAL_NOTES.json` | Complete extracted inherited editorial notes, kept separately in the corrected reader rather than mistaken for authorial text. |
| `EN_ATTRIBUTION_UPDATE.json`, `EN_PDF_TEXT_QA.json` | Body/identifier invariance across the final attribution update and compiled English text checks. |
| `FR_PDF_VISUAL_QA.json` | Inspected final French apparatus pages, including the corrected historical links and long paired-witness references. |
| `GLOSSARY_SGA7_FR_EN.tsv`, `GLOSSARY_INCONSISTENCIES.md`, `GLOSSARY_ATTESTATIONS.tsv`, `GLOSSARY_AUDIT.json` | Technical pairs, multiple renderings, exact attestation counts and validation. |
| `GLOSSARY_CANDIDATES.tsv`, `GLOSSARY_UNDERLINED_INVENTORY.tsv` | Reviewed residual candidate phrases and complete underlined-phrase inventory. |
| `PROVENANCE.md`, `FRONT_MATTER_INVENTORY.tsv`, `FRONT_MATTER_AUDIT.json` | Source credits, rights, exact provenance excerpts, absent leaves and credit/wording checks. |
| `INPUT_VERIFICATION.json`, `TYPESETTING_TRANSFORMS.tsv`, `FINAL_AUDIT.json`, `compile/` | Manifest verification, render transport, delivery checks and compilation diagnostics. |
| `FR_MASTER_PDF_EQUIVALENCE.json`, `EN_MASTER_PDF_EQUIVALENCE.json` | Byte identity of each master with its compiled default form, including source and PDF hashes. |
| `build/`, `work/` | Reproducible scripts, curated lexicon, frozen editorial decisions and intermediate build outputs. |

## Credits, rights and privacy

The bibliographic credits, every named human contribution in the supplied attribution records, and source-specific provenance are retained in each reader. The wording is **AI-transcribed**, **AI-translated**, and **AI-produced corrections**, with the original-English exception for VI clearly stated. Wider SGA-project credits are identified as wider-project credits rather than misrepresented as SGA 7 contributions. `PROVENANCE.md` preserves the source excerpts and their original qualifications.

The rights in the original work belong to its author or the author's representatives or heirs. Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, they are dedicated to the public domain under CC0 1.0. This edition is published for educational, non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and object to its publication here, please open a GitHub issue and we will take it down.

The French readers carry the corresponding French statement. The rights wording does not enlarge any third-party license or erase inherited human attribution. Private local provenance paths and email addresses are omitted; references identify members inside the supplied ZIPs. Compiled logs replace local resource paths with generic resource basenames. Intermediate completion checkpoints and the three final archives were saved as requested.
'''
    R.mkdir(parents=True, exist_ok=True)
    (R / 'README.md').write_text(text)
    print('README written from current records; six-reader compilation complete:', ok)


if __name__ == '__main__':
    main()
