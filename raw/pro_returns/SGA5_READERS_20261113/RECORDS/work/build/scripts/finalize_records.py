"""Write final counts, build verification and reader documentation."""
from __future__ import annotations
import collections,csv,json,re,subprocess
from pathlib import Path
from sga5_common import EXPOSES,expose_for,write_json,digest

ROOT=Path('deliverables')
CON=Path('work/contributions')
PREP=Path('work/build/prepared')
NAMES={
 'FR':['SGA5_FR_diplomatique','SGA5_FR_corrige_apparat','SGA5_FR_texte_de_lecture','SGA5_FR_master_annotated'],
 'EN':['SGA5_EN_diplomatic','SGA5_EN_corrected_apparatus','SGA5_EN_reading','SGA5_EN_master_annotated']}
KINDS=['derived-functor typography','formula / reference','word / reference','punctuation','typography / notation']

def read(p):return json.loads(Path(p).read_text())

def count_rows(p):
    with Path(p).open(newline='',encoding='utf-8') as f:return sum(1 for _ in csv.DictReader(f,delimiter='\t'))

def main():
    out=ROOT/'records';out.mkdir(parents=True,exist_ok=True)
    fr=read(CON/'validation_fr/INDEPENDENT_FR_MASTER_AUDIT.json')
    en=read(CON/'validation_en/INDEPENDENT_EN_MASTER_AUDIT.json')
    credits=read(CON/'validation_fr/READERS_CREDITS_AUDIT.json')
    assert fr['pass'] and en['passed'] and credits['pass']
    inherited=read(CON/'audit/AUDIT_FR.json')
    port=read(CON/'english/EN_PORT_AUDIT_SUMMARY.json')
    glossary=read(CON/'english/GLOSSARY_SUMMARY.json')
    changes=read(CON/'reader_changes/COMPLETE_READER_CHANGELOG_RECONSTRUCTION.json')
    assert changes['all_final_reader_reconstructions_exact']
    for lang,proof in changes['languages'].items():
        for chain in proof['complete_chains']:
            assert chain['final_reader_sha256']==digest(Path(chain['final_reader']).read_bytes()),lang+' stale complete change-log target'
    reproduction_path=CON/'packaging_audit/FINAL_SOURCE_REPRODUCTION.json'
    reproduction=None
    reproduction_note='The included rebuild driver records every executed stage and its audit checks.'
    if reproduction_path.exists():
        reproduction=read(reproduction_path)
        assert reproduction['source_rebuild_completed'] and reproduction['all_compared_artifacts_byte_identical'] and reproduction['all_five_final_reader_chains_reconstruct_exactly']
        for comparison in reproduction['comparisons']:
            assert comparison['byte_identical'] and digest(Path(comparison['path']).read_bytes())==comparison['sha256'],'Stale isolated-rebuild comparison: '+comparison['path']
        reproduction_note='An isolated source rebuild started with only implementation scripts, the declared reviewed inputs and the original three archives. It verified all 270 manifest members and reproduced all eight reader/master LaTeX sources, both frozen English sources, the French prepared layers and the final glossary byte for byte. All five complete reader reconstruction chains passed again. The isolated run stopped after source reconstruction; the eight PDF compilations reported above were performed separately on these identical final sources. The full report is `work/contributions/packaging_audit/FINAL_SOURCE_REPRODUCTION.json`.'
    assert inherited['validation']['counts_match'] and inherited['validation']['all_prepared_layers_reconstruct_exactly']
    assert not inherited['validation']['unresolved_terminal_searches'] and port['unresolved']==0
    variants={lang:read(PREP/f'{lang}_variants_ordered.json') for lang in NAMES}
    builds=[];pdftext={};counts=[]
    for lang,names in NAMES.items():
        for form,stem in enumerate(names):
            tex=ROOT/lang/(stem+'.tex');pdf=tex.with_suffix('.pdf')
            result=read(out/'build_outputs'/(stem+'.json'))
            assert result['success'] and result['error_count']==0 and result['missing_characters']==0
            assert result['source_sha256']==digest(tex.read_bytes()),stem+' stale TeX compilation'
            assert result['pdf_sha256']==digest(pdf.read_bytes()),stem+' PDF hash mismatch'
            text=subprocess.run(['pdftotext','-layout',str(pdf),'-'],capture_output=True,text=True,check=True).stdout
            pdftext[stem]=text
            entries=re.findall(r'\[(\d+)\]\s+((?:FR|EN)-\d{4}|R98-\d{2})',text)
            expected=len(variants[lang]) if form in [1,3] else 0
            assert len(entries)==expected,(stem,len(entries),expected)
            if expected:
                assert [i for _,i in entries]==[v['id'] for v in variants[lang]]
                assert [int(n) for n,_ in entries]==list(range(1,expected+1))
            result['printed_apparatus_entries_verified']=len(entries)
            result['pdf_text_sha256']=digest(text)
            result['language']=lang;result['form']=['diplomatic','corrected apparatus','reading','annotated master (default corrected apparatus)'][form]
            result['bookmark_warnings']=sum('Token not allowed in a PDF string' in w for w in result['warnings'])
            result['font_warnings']=sum('Font Warning:' in w for w in result['warnings'])
            assert not any('undefined' in w.lower() for w in result['warnings'])
            builds.append(result)
        assert pdftext[names[1]]==pdftext[names[3]],lang+' master PDF differs in extracted content'
        groups=collections.defaultdict(collections.Counter)
        for v in variants[lang]:groups[expose_for(int(v['page']))][v['kind']]+=1
        for _,exp in EXPOSES:
            for form in ['diplomatic','corrected apparatus','reading']:
                c=groups[exp] if form=='corrected apparatus' else collections.Counter()
                counts.append({'language':lang,'expose':exp,'form':form,**{kind:c[kind] for kind in KINDS},'total':sum(c.values())})
    summary={'six_readers_and_two_masters_compiled':True,'latex_errors':sum(x['error_count'] for x in builds),'missing_characters':sum(x['missing_characters'] for x in builds),'all_source_and_pdf_hashes_match':True,'master_and_corrected_PDF_texts_identical':True,'independent_master_audits_pass':True,'credits_audit_pass':True,'all_reader_change_chains_exact':True,'apparatus_entries':{k:len(v) for k,v in variants.items()},'separate_unresolved_notes':{'FR':30,'EN':31},'folio_markers':{'FR':483,'EN':793,'EN_distinct':479,'EN_unmarked_folios':[94,399,411,413]},'glossary':glossary,'open_item_rows':count_rows(CON/'decisions/OPEN_ITEMS_DECIDED.tsv'),'scan_rows':count_rows(CON/'scans/PLACES_98_DECIDED.tsv'),'builds':builds,'apparatus_counts':counts}
    write_json(out/'BUILD_SUMMARY.json',summary)
    if reproduction:
        summary['isolated_source_rebuild']={'completed':True,'compared_artifacts':len(reproduction['comparisons']),'all_byte_identical':True,'all_five_reader_chains_exact':True,'full_PDF_rebuild_executed_in_isolation':False}
        write_json(out/'BUILD_SUMMARY.json',summary)
    lines=['# Apparatus counts','',
           'One entry is one balanced variant call in the single annotated master. Independent projections verify every branch; the extracted corrected PDFs contain exactly the same ordered entry IDs and numbers. Diplomatic and reading PDFs contain no apparatus entries. The two masters compile by default in corrected-apparatus form.','',
           'Folio-based grouping follows the actual title boundaries in the source, including the appendix to Exposé I and the two indexes. The input English edit catalogue uses some broader exposition labels; the following grouping is explicitly computed from the recorded folio with `sga5_common.expose_for`. The five kind labels are the deterministic editorial categories retained in the final variant ledgers, not a claim that their mathematical meanings are disjoint.','',
           '| Language | Exposé / section | Form | Derived-functor typography | Formula / reference | Word / reference | Punctuation | Typography / notation | Total |',
           '|---|---|---|---:|---:|---:|---:|---:|---:|']
    for row in counts:lines.append('| '+' | '.join(str(row[k]) for k in ['language','expose','form']+KINDS+['total'])+' |')
    lines += ['',f"French corrected apparatus: **{len(variants['FR']):,} entries**. English corrected apparatus: **{len(variants['EN']):,} entries**. Each includes all 32 R98 scan decisions. The French corrected volume also has **30 unresolved-reading notes**, and the English has **31**, including its inherited editorial note from folio 43 relocated verbatim. These separate notes are excluded from the variant counts above.",'',
              'The original 875 English input edits are represented by 879 safe balanced master calls. The exact edit-component mapping, separate replay proofs, and preserved common gaps are in `work/contributions/validation_en/`. No French spelling variant is added to English merely because the French spelling differs.','']
    (out/'APPARATUS_COUNTS.md').write_text('\n'.join(lines))
    (out/'SOURCE_IDENTIFIERS.md').write_text('''# Source identifiers

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
''')
    table=['| File stem | PDF pages | LaTeX errors | Warnings | Overfull boxes | Underfull boxes | Missing glyphs |','|---|---:|---:|---:|---:|---:|---:|']
    for x in builds:table.append(f"| `{Path(x['file']).stem}` | {x['pages']} | {x['error_count']} | {x['warning_count']} | {x['overfull_hboxes']} | {x['underfull_hboxes']} | {x['missing_characters']} |")
    text=f'''# SGA 5 — French and English readers

Eight complete single-file LaTeX sources and eight PDFs are supplied: three readers and one annotated master per language. The edition was built from the three attached source archives, with all 270 manifest-listed files verified by size and SHA-256. No PDF has been omitted.

## Files

`SGA5_READERS_FR.zip` contains `SGA5_FR_diplomatique`, `SGA5_FR_corrige_apparat`, `SGA5_FR_texte_de_lecture`, and `SGA5_FR_master_annotated`, each as `.tex` and `.pdf`.

`SGA5_READERS_EN.zip` contains `SGA5_EN_diplomatic`, `SGA5_EN_corrected_apparatus`, `SGA5_EN_reading`, and `SGA5_EN_master_annotated`, each as `.tex` and `.pdf`.

`SGA5_READERS_RECORDS.zip` contains this README, the required decision/change/glossary/count tables, compilation logs and summaries, the complete prepared layers and variant catalogues, exact reconstruction proofs, scan evidence, and build scripts with their outputs. The `work/` layout is retained for the rebuild driver. Its root `MANIFEST.tsv` records package paths, bytes and hashes.

## One master for each language

Every body difference is a balanced `\\SGAvar{{printed}}{{corrected}}{{id}}` call in the language's annotated master. `SGAform=0` selects the diplomatic argument; `SGAform=1` selects the corrected argument and a linked apparatus call; `SGAform=2` selects the corrected argument without editorial calls or apparatus. The three reader sources have identical content after the two-line form header. Each master defaults to form 1. The extracted master PDF and corrected-reader PDF texts agree exactly.

There are **{len(variants['FR']):,} French** and **{len(variants['EN']):,} English** variant calls. Every call has a source and both complete TeX readings; PDF extraction verifies every apparatus ID, its order, and its printed number. The plain readers preserve the complete corrected authorial body, original footnotes, proofs, references and both indexes. Thirty readings requiring unavailable scans are recorded separately in each corrected volume, with both alternatives and a reason; they contribute no variant call because the retained body readings agree. English has one additional inherited editorial note from I 4.6, folio 43, moved verbatim out of all reader bodies into the corrected-only unresolved appendix. The original removed-reader-prose record and the exact deletion/reinsertion ledger document this relocation; there are therefore 31 English unresolved notes.

The English independent audit proves byte-exact projection of both bodies and preserves all 875 original input variants through 843 exact edit components. The French audit enumerates every raw serialization discrepancy: initial empty lines, the discarded display-math endline on p. 52, redundant paragraph-ending lines at pp. 73 and 204, and the comment/argument boundary on p. 248. Each has a specific TeX token or mode proof. There is no blanket whitespace equivalence rule in this audit. A reproducible pdfTeX token probe is included for p. 248. The final reader-body assembly is also reversed explicitly and compared with the master.

## Folios and missing front matter

French retains all **483** source folio markers, in their supplied order, with scan index = folio + 11. The print repeats 434 in the place of 435; the next marker is 436. The prefaces and a margin notice at that jump explain the repetition.

English has **793** source-supported section, paragraph or formula anchors on **479** distinct folios. Folios **94, 399, 411 and 413** have no safe independent English marker at the exact source boundary, so no interpolated marker is invented. The alignment table records every anchor and its method. Repeated anchors for the same printed folio are intentional. The English change log uses surrounding validated anchor bounds when a change has no uniquely exact folio.

The original title page, L. Illusie's Introduction (iii–viii), the Liste des SGA and the original Table des matières were not transcribed in the supplied sources. Their missing text is not reconstructed. New title/credit/preface pages are identified as this reader edition, and each table of contents is generated from the headings actually present. The supplied body from Exposé I through XV and both indexes is retained in full.

## Scan decisions and other editorial decisions

All **32** specified RΓ places on printed pp. 457–474 were read in the supplied scan strips and crops. Each has an upright R with two underlines. The diplomatic branches use `\\underline{{\\underline{{\\mathrm{{R}}}}}}\\Gamma`; the corrected branches use `\\mathrm{{R}}\\Gamma` under GLOBAL_ISSUES 98. Attached scripts are kept inside each complete variant so they remain attached to Γ. R98-18 on p. 460 also has the double underline. The separate plain-RΓ occurrence on p. 461 lies outside this list and remains plain. `PLACES_98_DECIDED.tsv` gives images, regions, readings and reasons; the evidence directory includes all 32 crops and overview sheets.

The new corrected French source has exactly 35 declared changes from the supplied current layer: the 32 scan readings; OPEN-H75 on p. 433 (`F'/G` → `f'/G`, by the explicitly defined induced endomorphism); SOL-EN-084 on p. 472 (`F` → `F_ν`, by the immediately preceding component formula, with the scan confirming printed F); and GLOBAL-98b on p. 441, where the supplied printed Frobenius glyph is retained pending its unavailable scan. The last is a retained reading in both branches, with the alternative in the unresolved notes. The diplomatic French source has exactly the 32 scan changes.

`OPEN_ITEMS_DECIDED.tsv` has **{summary['open_item_rows']}** explicit dispositions, covering all six REVIEW questions, the 89 English SOL observations, open merge/report items and relevant global issues. Eighteen Spanish-only observations are explicitly recorded as outside these French/English readers. Every decision gives its reason and affected forms. Stale “open” wording and superseded port decisions are reconciled to the later named evidence.

## Applied-fix inheritance

The French audit checks **4,173 diplomatic fix-log records**, **3,770 corrected fix-log records**, including **29** `misprint_correction` records, **88 hand records**, **36 resolved replay items**, and **8 findings in seven manual files**. The resulting inheritance table has **8,084 rows**. It verifies the manifest identities of the supplied final layers, replays every additional build edit, and records literal, contextual, scope or supersession evidence for every fix record. The independent master projections extend that proof into the readers. The audit also records all **117 reconciliation dispositions**.

The 590-item misprint register has no uniform status field. It provides 512 literal/projection witnesses in current and 78 entries requiring descriptive or supersession context. These figures do not mean that every proposed registry correction was inserted. Two historical p. 109 fix-log records cite an intermediate title with a final stop; the supplied final source omits that stop. Both discrepancies are documented, and the authoritative final text is retained.

The English port audit accounts for **1,856** records: 735 exact retained readings, one verified later port operation, 42 covered records, 67 readings with named later repairs, and 1,011 recorded not-applicable items; no port record remains unresolved. Exact replay applies 398 common operations at 515 occurrences, followed by the 95 input variants that change corrected source, to reproduce the frozen corrected English. Source-to-final links and all original port row IDs remain available.

## Change logs and glossary

`CHANGES_FR.tsv` contains **{changes['languages']['FR']['complete_change_rows']:,}** complete rows and `CHANGES_EN.tsv` contains **{changes['languages']['EN']['complete_change_rows']:,}**. These tables include source changes, exact body extraction, representation changes and final reader assembly. The French starting branches are August `o`, `c5`, `c4` and supplied current; the English starting branch is the released source. All five complete chains reconstruct the delivered corrected-reader `.tex` bytes exactly. `COMPLETE_READER_CHANGELOG_REPORT.md` explains the stages, and the reconstruction JSON records every source/final hash. Original CRLF bytes are preserved inside quoted TSV cells; read with a TSV parser opened using `newline=''`.

The glossary contains **{glossary['rows']} rows**, including all **{glossary['index_pairs']} paired term/notation index entries** and the observed forms in **{glossary['body_term_families']} audited body phrase families**. `GLOSSARY_INCONSISTENCIES.md` lists the **{glossary['multiple_form_families']}** families with multiple observed English forms and distinguishes contextual constructions from slips by their cited occurrences. Five documented lexical repair operations make 13 replacements. Counts are literal occurrence counts under each recorded phrase pattern; index rows retain their exact paired TeX. The coverage audit and contexts make the vocabulary scope explicit.

## Compilation and visual checks

Every file was compiled in three pdfLaTeX passes with a fixed build epoch. All eight compilations finished with **zero LaTeX errors**, **zero missing-character diagnostics**, and no undefined-reference warning. Remaining diagnostics are retained in full in `build_outputs/`.

{chr(10).join(table)}

French files have 52 hyperref PDF-bookmark warnings about mathematical tokens; English files have 55. English also retains three source `scriptsize`-in-math font warnings. The remaining counts above are line-spacing/overfull-box diagnostics. They are reported rather than suppressed. Visual inspection covered title/credit pages, generated contents, ordinary mathematical pages, the folio gap, the RΓ passages and scripts, both indexes, apparatus opening/long entries/scan entries, and the separate unresolved notes. The final check verifies the complete printed apparatus ID sequence and matching master/reader text.

## Rebuild

For an individual reader, place its single `.tex` file in a directory with a standard TeX Live installation and run `pdflatex -interaction=nonstopmode -halt-on-error FILE.tex` three times. Its packages include the usual AMS packages, Babel French/English, Latin Modern, geometry, microtype, tikz-cd, hyperref, marginnote, fvextra, xparse and needspace; the English source also uses ulem. No external source inputs or images are needed to compile a reader.

For the full source build, extract the records archive, place the original three supplied archives in the directory documented by `REBUILD.md`, then run its included rebuild driver. The original private `source_path` fields are not republished. The driver verifies source manifests, uses the retained reviewed decision catalogues, regenerates the prepared layers and masters, audits the results, reconstructs the change logs, compiles all eight files, and rebuilds package manifests. Scan judgments are preserved as explicit inputs with their evidence and exact offsets. The scripts stop on a failed hash, range, count or reconstruction.

{reproduction_note}

## Record path conventions

Paths beginning `fr/`, `fr_baseline_aug2026/`, `fixes/`, `conventions/`, `reports/` and the original corpus-record paths refer to members of `SGA5_FR.zip`. Paths beginning `en/` and `port/` refer to `SGA5_EN.zip`; original `scans/`, `checker_crops/` and `tex_pages/` refer to `SGA5_SCANS.zip`. In contribution reports, `prepared/` maps to `work/build/prepared/`, `scripts/` to `work/build/scripts/`, and `english/`, `audit/`, `decisions/`, `validation_fr/`, `validation_en/` to the corresponding `work/contributions/` directory. Root copies of `FR_SOURCE_WITNESSES.json` and `EN_variants_input.json` resolve the apparatus's short citation basenames; `SOURCE_IDENTIFIERS.md` specifies the record-number conventions. The standalone change utilities retain their own explicitly documented CLI layouts. Exact root delivery tables supersede the earlier source-only tables retained inside the contributions directories.

## Credits and rights

Each source and PDF carries the bibliographic and contributor credits from the supplied records, all 37 named human contributions, the required wording “AI-transcribed”, “AI-translated” and “AI-produced corrections”, and the requested rights statement in its language. This build is credited to GPT-6 Astra (OpenAI, ChatGPT Pro mode). The credits audit verifies the exact English rights statement and French translation across all eight source files. Original authors' rights and the stated CC0 dedication for rights actually held are preserved.

Only archive-relative paths appear in the published records. Temporary compiler files and source records containing private machine paths are excluded. Package integrity and privacy reports accompany the final delivery. Checkpoints preserve successive completed readers; these final three packages supersede them.
'''
    (out/'README.md').write_text(text)
    for lang in NAMES:(ROOT/lang/'README.md').write_text(text)
    print(json.dumps({'compiled_files':len(builds),'errors':summary['latex_errors'],'variants':summary['apparatus_entries'],'complete_change_rows':{k:v['complete_change_rows'] for k,v in changes['languages'].items()},'glossary_rows':glossary['rows']}))

if __name__=='__main__':main()
