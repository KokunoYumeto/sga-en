#!/usr/bin/env python3
"""Validate the completed books and write their shared release documentation.

This gate reads actual final files and completed review receipts. It never
promotes an unreviewed source item merely because a PDF compiles.
"""
from pathlib import Path
import collections,csv,hashlib,json,re,shutil
import fitz
from checkpoint import EXPOSES,exposure
from package_release import FORM_NAMES,PRIVATE

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'records'
EN=ROOT/'review/english'

def readj(rel):return json.loads((ROOT/rel).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rows(path):
    with path.open(newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def jsonl(path):return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]

def page_gate():
    table=rows(REC/'PAGES_CHECKED.tsv')
    expected=['cover','cover-verso','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']+[str(i) for i in range(1,701)]+[f'rear-{i}' for i in range(715,721)]
    assert len(table)==720 and [r['folio'] for r in table]==expected
    cache={}
    for n,row in enumerate(table,1):
        assert row['pdf_page']==str(n) and row['checked_against_scan']=='true'
        assert row['image'] and row['reason']
        for col in ['FR_master_begin','EN_master_begin']:
            rel,line=row[col].rsplit('#line=',1)
            if rel not in cache:cache[rel]=(ROOT/rel).read_text().splitlines()
            actual=cache[rel][int(line)-1]
            assert re.search(r'%+\s*scan idx\s+'+str(n-1)+r'\s*\|\s*folio\s+'+re.escape(row['folio'])+r'\s*%+\s*$',actual),(n,col)
    return dict(original_physical_leaves=720,numeric_folios=700,front_leaves=14,rear_leaves=6,
      all_checked=True,all_both_master_line_locations_verified=True)

def decision_gate():
    status=readj('records/CHECKPOINT_STATUS.json')
    totals={'finding':3751,'fixlog':5513,'misprint':724,'replay':20,'manual':7,'hold_difference':119,'rejected_codex':141}
    for kind,n in totals.items():assert status[kind]=={'total':n,'decided':n,'pending':0}
    expected={'FINDINGS_DECIDED.tsv':9264,'MISPRINTS_6_DECIDED.tsv':966,'OPEN_ITEMS_DECIDED.tsv':23,
      'PRIOR_RESOLVED_REPLAY_REVIEW.tsv':4,'CODEX_DECIDED.tsv':260,'CHECK_FINDINGS.tsv':1923,'DECISIONS.tsv':226}
    counts={}
    for name,n in expected.items():
        rs=rows(REC/name);assert len(rs)==n,(name,len(rs),n)
        assert len({r['id'] for r in rs})==len(rs),name
        for r in rs:
            assert r['verdict'] and not r['verdict'].startswith('pending') and r['reason'],(name,r['id'])
        counts[name]=len(rs)
    assert not readj('records/REVIEW_IMPORT_DIAGNOSTICS.json')['unresolved_duplicate_ids']
    patches=readj('records/PATCH_APPLICATION_FR.json')
    pc=collections.Counter(r['status'] for r in patches)
    assert pc['blocked']==0 and pc['applied']==4992
    return status,dict(historical=totals,tables=counts,French_patch_statuses=dict(pc),
      additional_explicit_source_error_decisions=242,pending=0)

def french_gate():
    d=readj('records/FR_FINAL_SOURCE_INVARIANTS.json')
    for key in ['forms_from_identical_master','source_marker_order_exact','source_links_complete']:assert d[key]
    assert d['variants']==d['body_calls']==d['apparatus_entries']==970
    for proof in d['change_streams']:
        assert proof['exact_reconstruction']
        assert proof['after_sha256']==sha(ROOT/proof['after_source'])
    q=readj('records/FR_FINAL_RENDERED_QA.json');assert q['passed']
    for r in q['compiles']:
        assert r['source_sha256']==sha(ROOT/r['file']) and r['pdf_sha256']==sha(ROOT/r['pdf'])
    links=readj('records/FR_APPARATUS_SOURCE_LINKS.json')['summary']
    assert links['variants']==links['sourced_variants']==970 and links['unresolved']==0
    return d

def english_gate():
    generation=readj('review/english/final/GENERATION_STATUS.json')
    release=readj('review/english/final/RELEASE_STATUS.json')
    assert release['status']=='complete; stable for coordinator archival'
    for book in release['final_books']:
        for key in ['tex','pdf']:
            assert sha(ROOT/book[key]['path'])==book[key]['sha256']
    assert generation['variant_groups']==691 and not generation['remaining_source_folios']
    assert generation['annotated_master_sha256']==sha(EN/'final/SGA6_EN_annotated_master.tex')
    catalogue=readj('review/english/aggregate/INPUT_CATALOG.json')
    assert catalogue['full_English_transfer_complete'] and not catalogue['unreviewed_numeric_folios']
    source=readj('review/english/aggregate/SOURCE_SPAN_COMPLETENESS.json')
    assert len(source['original_marker_keys'])==720 and source['numeric_folios']==list(range(1,701))
    assert len(source['exact_sealed_span_applications'])==142
    assert source['each_original_marker_once'] and source['no_remaining_numeric_gap']
    assert source['source_comment_and_visible_command_order_identical']
    assert not source['hyperlink_audit']['dangling_hyperlinks']
    math=readj('review/english/aggregate/LITERAL_MATH_VERIFICATION.json')
    assert not math['remaining_folios'] and math['unexpected_difference_units']==0
    branches=readj('review/english/aggregate/SINGLE_MASTER_BRANCH_AUDIT.json')
    assert branches['variant_groups']==691
    assert all(r['exact_reconstruction_pass'] for r in branches['branches'])
    for r in branches['forms']:
        assert r['only_master_switch_differs']
        assert r['sha256']==sha(EN/'final'/('SGA6_EN_'+r['form']+'.tex'))
    notes=readj('review/english/aggregate/ORIGINAL_NOTE_LABEL_AUDIT.json')
    assert all(r['author_note_commands']==111 and r['command_label_sequence_equal'] and r['no_unlabelled_legacy_note_commands'] for r in notes['branches'])
    joins=readj('review/english/aggregate/FOLIO_JOIN_AUDIT.json')
    assert joins['numeric_join_records']==699 and joins['nonwhitespace_tokens_identical'] and joins['forward_and_reverse_reconstruction_pass']
    macro=readj('review/english/aggregate/MACRO_EXPANSION_CLOSURE.json')
    assert macro['unresolved_page_command_groups']==0 and macro['approved_lexical_page_command_groups']==11
    assert sha(ROOT/macro['static_audit'])==macro['static_audit_sha256']
    assert sha(ROOT/macro['decision_file'])==macro['decision_file_sha256']
    assert all(r['exact_identity_or_translation_map'] for r in macro['dispositions'])
    change=readj('review/english/final/CHANGES_EN_RECONSTRUCTION.json')
    assert change['forward_exact_reconstruction'] and change['reverse_exact_reconstruction']
    assert change['final_reader_sha256']==sha(ROOT/change['final_reader'])
    transfer=readj('review/english/final/TRANSFER_LEDGER_STATUS.json')
    assert transfer['rows']==len(jsonl(EN/'final/TRANSFER_LEDGER.jsonl'))
    for r in transfer['input_files']:assert sha(ROOT/r['path'])==r['sha256']
    late=readj('review/english/visual_qa_late/VISUAL_QA.json')
    assert late['status']=='complete' and late['defect_count']==0
    assert late['pdf_sha256']==sha(ROOT/late['source_pdf'])
    visual=readj('review/english/visual_qa_final/VISUAL_QA.json')
    assert visual['concrete_defects_observed']==0 and visual['directly_viewed_images']==len(visual['observations'])
    for r in visual['observations']:
        assert not r['concrete_defect_observed'] and sha(ROOT/r['pdf'])==r['pdf_sha256']
    variants=jsonl(EN/'final/VARIANTS.jsonl')
    assert len(variants)==691==len({v['id'] for v in variants})
    for v in variants:
        assert v['printed']!=v['corrected'] and v['source'] and v['scan_image'] and v['scan_region'] and v['reason'],v['id']
    return dict(variant_groups=691,translation_spans=142,transfer_ledger_rows=transfer['rows'],
      exact_mathematical_comparison_unexpected_units=0,approved_complete_lexical_pairs=math['complete_lexical_pair_records'],
      original_author_note_commands=111,numeric_folio_joins=699,source_marker_leaves=720,
      raw_change_hunks=change['raw_hunks'],literal_change_hunks=change['literal_source_change_hunks'],
      line_ending_hunks=change['line_ending_only_hunks'],
      original_leaf_coverage_complete=True,branch_reconstruction_exact=True),variants

def compile_gate():
    result=[]
    en_status=readj('review/english/final/EN_CANDIDATE_BUILD_STATUS.json')
    for language,names in FORM_NAMES.items():
        for name in names:
            directory='readers/fr/final' if language=='FR' else 'review/english/final'
            src=ROOT/directory/(name+'.tex');pdf=src.with_suffix('.pdf')
            if language=='FR':
                r=readj('records/COMPILE_'+name+'.json')
                assert r['exit_code']==0 and r['passes']==2 and not r['errors']
                assert r['source_unchanged_during_compile'] and sha(src)==r['source_sha256'] and sha(pdf)==r['pdf_sha256']
                warnings=r['warnings']
            else:
                form=name.removeprefix('SGA6_EN_');r=en_status[form]
                assert len(r['runs'])==2 and all(x['exit_code']==0 for x in r['runs'])
                assert r['pdf_present'] and r['source_unchanged_during_compile']
                assert sha(src)==r['source_sha256'] and sha(pdf)==r['pdf_sha256']
                warnings=r['runs'][-1]['diagnostics']
            assert not PRIVATE.search(src.read_text()),src.name
            assert not re.search(r'\\(?:input|include|includegraphics|bibliography|addbibresource)\b',src.read_text()),src.name
            doc=fitz.open(pdf)
            pdf_text='\n'.join(p.get_text() for p in doc)
            extra=json.dumps(doc.metadata,ensure_ascii=False)
            for p in doc:
                for link in p.get_links():
                    extra+=' '+str(link.get('uri',''))+' '+str(link.get('file',''))
            assert not PRIVATE.search(pdf_text+'\n'+extra),pdf.name
            result.append(dict(language=language,file=src.relative_to(ROOT).as_posix(),source_sha256=sha(src),
              pdf=pdf.relative_to(ROOT).as_posix(),pdf_sha256=sha(pdf),pdf_pages=len(doc),pdf_bytes=pdf.stat().st_size,
              passes=2,errors=0,warnings=warnings,warning_count=len(warnings)))
    return result

def glossary_gate():
    folder=EN/'terminology_final'
    audit=json.loads((folder/'GLOSSARY_AUDIT.json').read_text())
    final_verification=json.loads((folder/'FINAL_VERIFICATION.json').read_text())
    assert final_verification['passed'] and final_verification['glossary_rows']==audit['glossary_rows']
    assert audit['source_leaf_pairs']==720 and audit['printed_index_rows']==234
    for name in ['GLOSSARY_SGA6_FR_EN.tsv','GLOSSARY_INCONSISTENCIES.md','CROSS_VOLUME_TERMS.tsv','CROSS_VOLUME_DECISIONS.tsv']:
        assert (folder/name).is_file()
        shutil.copy2(folder/name,REC/name)
    assert len(rows(REC/'GLOSSARY_SGA6_FR_EN.tsv'))==audit['glossary_rows']
    assert len(rows(REC/'CROSS_VOLUME_TERMS.tsv'))==audit['cross_volume_difference_rows']
    shutil.copy2(EN/'final/CHANGES_EN.tsv',REC/'CHANGES_EN.tsv')
    return audit

def apparatus_counts(english_variants):
    fr=readj('records/FR_VARIANTS.json')
    classification=readj('review/final_english_classification/CLASSIFICATION.json')
    assert classification['summary']['unresolved']==classification['summary']['missing_source_decisions']==classification['summary']['missing_pair_attributions']==0
    # The independent handoff supplies one explicitly sourced row per group.
    entries=classification.get('entries',classification.get('variants',[]))
    assert len(entries)==len(english_variants)==691
    classified={r.get('variant_id',r.get('id')):r for r in entries}
    assert set(classified)=={v['id'] for v in english_variants}
    en=[]
    for v in english_variants:
        r=classified[v['id']];assert str(r['folio'])==str(v['page'])
        assert r['printed']==v['printed'] and r['corrected']==v['corrected']
        en.append(dict(id=v['id'],page=v['page'],kind=r['kind']))
    kinds=['source misprint correction','mathematical source correction','explicit notation convention','adjudicated source correction']
    expos=['Front matter']+[e[0] for e in EXPOSES]+['Rear publisher matter']
    expos.insert(expos.index('XII'),'XI')
    machine=[];lines=['# Apparatus counts','',
      'Each count is a variant group with two different literal readings. A group may contain more than one atomic correction or source-record alias. Only the corrected-apparatus form and the annotated-master PDF print these entries. The diplomatic and reading forms print zero apparatus entries.','',
      'Exposé XI has no body in the source (Non rédigé) and no variant. French spelling corrections that produce unchanged English create no English variant. Grouping is recorded independently in each annotated master.','']
    summaries={}
    for language,vs in [('FR',fr),('EN',en)]:
        counter=collections.Counter((exposure(v['page']),v['kind']) for v in vs)
        summaries[language]=dict(collections.Counter(v['kind'] for v in vs))
        assert set(summaries[language])<=set(kinds)
        lines+=['## '+language,'','| Exposé or matter | Kind | Diplomatic | Corrected apparatus | Reading | Annotated master |','|---|---|---:|---:|---:|---:|']
        for exp in expos:
            shown=False
            for kind in kinds:
                n=counter[(exp,kind)]
                for form,value in [('diplomatic',0),('corrected apparatus',n),('reading',0),('annotated master',n)]:
                    machine.append(dict(language=language,expose=exp,kind=kind,form=form,entries=value))
                if n:
                    lines.append(f'| {exp} | {kind} |0|{n}|0|{n}|');shown=True
            if not shown:lines.append(f'| {exp} | all kinds |0|0|0|0|')
        for kind in kinds:
            n=summaries[language].get(kind,0);lines.append(f'| All | {kind} |0|{n}|0|{n}|')
        lines+=['',f'Total groups: {len(vs)}.','']
    lines+=['French source links and kind bases: records/FR_APPARATUS_SOURCE_LINKS.json. English source links and kind bases: review/final_english_classification/CLASSIFICATION.json. The companion APPARATUS_COUNTS.tsv explicitly includes every zero combination.','']
    (REC/'APPARATUS_COUNTS.md').write_text('\n'.join(lines))
    with (REC/'APPARATUS_COUNTS.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['language','expose','kind','form','entries'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(machine)
    return summaries

def documentation(compiles,decisions,french,english,glossary,kinds):
    text=['# SGA 6 — French and English readers','',
      'The release contains six readers and two annotated masters, with all eight standalone LaTeX sources and all eight compiled PDFs. All 720 original scan leaves have completed review dispositions. All historical decision queues are decided. The tables retain every recorded disposition. Selected retained-source limitations and the attributed publisher-notice restitution are explained below and in the reader prefaces, with links to the additional retained-passage records.','',
      '## Archives and opening the books','',
      '- SGA6_READERS_FR.zip: readers/fr/final/, containing the French diplomatic, corrected-apparatus and reading forms, plus their common annotated master; each has a PDF.',
      '- SGA6_READERS_EN.zip: review/english/final/, containing the corresponding English forms and annotated master; each has a PDF. It also carries the entire unchanged manifest closure of the ten sealed English reconstruction/evidence packets at their recorded paths.',
      '- SGA6_READERS_RECORDS.zip: the decision tables, complete change logs, glossary, source-transfer evidence, captured glossary inputs, build scripts and sanitized build diagnostics.',
      '',
      'Extract all three archives into the same directory to retain the recorded relative paths. Each archive has a MANIFEST.tsv with path, source, bytes, SHA-256 and role. Each also carries this README. All eight requested PDFs are included; none is omitted for size.','',
      '## Completed page and decision review','',
      '| Record class | Completed | Pending |','|---|---:|---:|',
      '| Original scan leaves |720|0|',
      '| Checker findings |3751|0|',
      '| FIXLOG rows, both French branches |5513|0|',
      '| Historical misprint-register records |724|0|',
      '| Replay records, including four already resolved historically |20|0|',
      '| Hand-placed findings |7|0|',
      '| Rejected Codex records |141|0|',
      '| HOLD-tree differences |119|0|','',
      'The scan comprises 14 front leaves, folios 1–700, and 6 rear leaves. PAGES_CHECKED.tsv has 720 rows, with image/region evidence, finding counts and an exact line location in both final annotated masters. Its numbered-page relation is original PDF page = folio+14. The source comments preserve scan indices 0–719 in order. The missing folio 690 marker has been restored. Source-certified blank leaves keep their marker comments; they add no empty visible margin label.','',
      f"The aggregate tables contain {decisions['tables']['FINDINGS_DECIDED.tsv']:,} FINDINGS_DECIDED rows, {decisions['tables']['MISPRINTS_6_DECIDED.tsv']:,} MISPRINTS_6_DECIDED rows, {decisions['tables']['CHECK_FINDINGS.tsv']:,} own findings and {decisions['tables']['DECISIONS.tsv']:,} convention/boundary decisions. The misprint table includes 724 historical records and 242 additional explicit source-error dispositions. These are record counts; their grouping in the apparatus is separately recorded.",
      '',
      'OPEN_ITEMS_DECIDED.tsv contains the 16 originally open replay items plus 7 manual findings. PRIOR_RESOLVED_REPLAY_REVIEW.tsv preserves the four already-resolved replay items and their second review. CODEX_DECIDED.tsv contains 141 rejected Codex records and 119 HOLD differences. Every imported duplicate has an explicit merge resolution. No verdict is left pending.','',
      '## Construction and correspondence of forms','',
      'The French builder applies the exact reviewed patches to both attached French layers. There are 4,992 applied branch patches, four already-present applications and zero blocked anchors. The final typography applications include 930 applications from the completed convention pass and 98 applications for 49 numeric-only headings in both branches. All patches retain their old/new strings, expected counts, source IDs and reasons.',
      '',
      'Each language has one annotated master. Its literal diplomatic and corrected alternatives determine all three forms through a form switch. The diplomatic form selects the source reading; the corrected-apparatus form selects the corrected reading and prints the corresponding source-linked entry; the reading form selects that same corrected text while omitting the new apparatus. The Introduction, original author/editor notes, tables, indexes and transcribed publisher matter remain in all three forms.',
      '',
      'The French exact branch reconstruction, actual final-master body comparison and all 720 original markers pass. The English checks likewise reconstruct both source branches and show that the three rendered sources differ by the master switch. All 111 original author-note commands and their label/geometry keys agree with the reviewed source in both English branches. Captured macro states at each variant preserve the locally active meanings when alternatives are printed in the apparatus.',
      '',
      'Generated layout transports have explicit inverses: heading boxes retain their literal contents; source-folio labels attach to their opening headings; each of the fourteen written exposés begins on a fresh output page; and the English presentation-only line breaks retain formula payloads. Exposé XI has no body and creates no opening or apparatus entry.',
      '',
      '### Apparatus totals','',
      '| Kind | French | English |','|---|---:|---:|']
    for kind in ['source misprint correction','mathematical source correction','explicit notation convention','adjudicated source correction']:
        text.append(f"| {kind} |{kinds['FR'].get(kind,0)}|{kinds['EN'].get(kind,0)}|")
    text+=['| **All groups** |**970**|**691**|','',
      'APPARATUS_COUNTS.md and its complete TSV give the counts by exposé, form and kind. Every group has different literal readings and adjudicated source links. The French independent provenance audit checks all 970 groups, including repeated short-pair contexts and 90 manual full-context mappings. The English classification preserves every source ID and explicit related source.',
      '',
      '### English transfer and terminology','',
      f"The English reconstruction uses {english['translation_spans']} exact reviewed native-source spans covering all 720 original leaves. TRANSFER_LEDGER.jsonl retains {english['transfer_ledger_rows']:,} attributed correction/typography/aggregate rows. The two complete mathematical branches have zero unexpected literal-unit differences after the {english['approved_complete_lexical_pairs']} explicitly recorded lexical translation pairs and exact wrapper transports. The check includes starred equation environments and the complete equation crossing 526/527. All 699 numeric folio joins have recorded separator comparisons and inverse-checked whitespace transports.",
      '',
      f"The glossary contains {glossary['glossary_rows']:,} rows; all 234 printed terminology/notation index rows are paired and adjudicated. GLOSSARY_INCONSISTENCIES.md records {glossary['admitted_multiple_rendering_groups']} admitted groups with more than one English rendering. CROSS_VOLUME_TERMS.tsv and CROSS_VOLUME_DECISIONS.tsv record {glossary['cross_volume_difference_rows']} decisions against the supplied SGA 4, 4½, 5 and 7 glossaries and notation records. The two reviewed générisation passages on 648–649 use generization in both English branches.",
      '',
      'Glossary counts retain an explicit scope for each row: surface-form occurrences on a leaf that co-attests the complete French phrase, exact paired index rows, or literal macro/token uses in the declared folios. The audit accounts for every supplied inventory row and every printed index row. It does not present these different count scopes as a single word total. Detailed source and semantic attestations remain in review/english/terminology_final/.',
      '',
      '### Literal change logs','',
      f"CHANGES_FR.tsv contains {french['changes_rows']:,} literal hunks across four independently reconstructing streams: each of the two specified before sources (Codex HOLD and the attached corrected layer) to the reviewed author-text projection, and each to the exact final corrected-reader TeX including generated editorial/apparatus material. Scope and source columns identify each stream.",
      '',
      f"CHANGES_EN.tsv contains {english['raw_change_hunks']:,} exact released-reader-to-final-reader hunks, including {english['line_ending_hunks']:,} reversible line-ending hunks and {english['literal_change_hunks']:,} other literal source hunks. Forward and reverse reconstruction both pass. The 142 native-to-reviewed translation spans and the separately recorded English-only corrections are additionally labelled by their own scope and baseline. Their before/after text is complete.",
      '',
      '## Source passages retained after adjudication','',
      'The decisions on 431, 443 and 590–592 include explicit counterexamples to the examined printed assertions. A unique authorial textual repair was not established, so those passages remain verbatim in the French author text and faithfully translated in English, in all forms. The source blanks for references on 464 and the integral-group memberships on 465 are also retained. The 465 record supplies the rational construction and states exactly what the available argument establishes. These are completed retention dispositions; unchanged passages create no diplomatic/corrected variant.',
      '',
      'Those final-disposition pages are selected examples. Additional retained assertions or proof steps are indexed in review/final_readme_audit/ADDITIONAL_RETAINED_PASSAGES.json and its readable Markdown companion: II 206–207; III 244–245 and 256–257; IV 295; and V 336–339, 341, 343, 352 and 354–356. The index preserves 17 existing decision IDs with their original reasons, image references and proof-packet paths. Several of those packets independently verify a stated conclusion while identifying a defective intermediate equality, domain, coefficient shorthand or evaluation; each record states the precise affected scope. The index adds no new mathematical verdict.',
      '',
      'The full calculations, source images/regions and reasons are preserved in review/final_dispositions/ and the underlying decisions. The prefaces make these limitations visible to readers. This release does not claim a replacement theorem for any of those passages.',
      '',
      '## Notation conventions and exact identifications','',
      'The complete source policy is review/global_conventions/CONVENTIONS_SGA6.md, supplemented by review/global_numeric_headings/. Required GLOBAL_ISSUES 76, 81, 82, 84, 86, 87, 88 and six NOTE_6 supplements are decided. Each scope is tied to observed occurrences; no blanket glyph substitution is inferred from a mathematical role.',
      '',
      '- Raised K/Gr dots, lower complex/coherent-group dots, genuine primes, Tate/cohomological asterisks, baseline series dots and completion placeholders retain their observed positions and local scope.',
      '- Source word rules use upright underlined lexical groups. Individually ruled mathematical letters, double rules and primes outside the rules retain their own commands. Plain defined terms, reference numerals and resp. tokens follow the documented exclusions. Ordinary item and paragraph labels use ordinary weight; NOTE_6 statement-label styling remains explicit.',
      '- Category/site glyph transports fix the already-bound objects and morphisms. The named filtered category fixes its groups, filtration subgroups and filtration-preserving maps. For the graded category in V, the degree-filtration functor j and associated graded Gr are recorded; the map B→Gr(jB) sends each homogeneous element to its class of the same degree, with the inverse taking that class back to the element.',
      '- The small exterior wedge fixes each elementary exterior tensor in the same alternating quotient, including degree and Module argument. The wedge-shaped algebra name in V 356–360 fixes the named augmented lambda-ring, its multiplication, augmentation and lambda operations. The source-specific choice of ordinary atom versus operator is retained.',
      '- For derived tensor notation the documented fixed representative P gives the identity chain map on P⊗F; for a derived image a fixed injective representative I gives the identity on f_*I and its cohomology. Locally declared double-rule/double-struck representations preserve those same objects and maps. Symmetric-algebra letter transports fix the graded algebra and therefore the degree-zero affine charts and the projective bundle obtained by gluing them.',
      '- Hom, Isom, Proj and Pic rules follow the source occurrences. Wavy Picard-functor rules and neighboring scheme-letter rules remain visible. Their representability relation is the recorded natural identification of T-points with the functor values. The structure-sheaf O, XIV phi, c-ell/cl, n°, Ob/ob, Ab.fil. punctuation and macro resets follow their source-scoped decisions.',
      '- The explicitly admitted coefficient-field spelling sends every rational number to itself and preserves addition and multiplication. Double-struck coefficient letters, plain/script exceptions, Gro and all later macro states have their local source declarations and exact English transports recorded.',
      '',
      '## Original front/rear matter and attributed restitution','',
      'The original cover, title/colophon, preface, Introduction and contents are transcribed. The rear leaves retain 188 catalogue entries and the two ISBN lines; the two blank rear leaves keep their source markers. Bibliographic data identify Lecture Notes in Mathematics 225, Springer, 1971, and all named volume authors and collaborators.',
      '',
      'The inside-cover publisher notice is partly hidden by an attached label in the scanned copy and has no matching witness leaf. Its obscured wording is an explicitly attributed restitution from the corresponding 1971 Springer Lecture Notes in Mathematics 228 notice, whose 17 visible comparison points agree. The covered physical strokes of the SGA 6 copy have not been recovered. Evidence, comparison tables and the source PDFs are retained in review/publisher_notice_recovery/.',
      '',
      'Institutional stamps, barcodes, handwritten prices, attached labels and other copy-specific marks are omitted as documented; nontextual publisher logos are omitted. No printed author/editor text, original note, Introduction, index entry, catalogue entry or ISBN is intentionally removed from the reading form.',
      '',
      '## Credits and rights','',
      'Each reader preserves the human contributions and source attributions specified in the supplied English repository records and SOURCES.md, including the named original authors/editors and credited transcription, typesetting and English-source contributions. Source attribution remains attached to inherited English formulations.',
      '',
      'The edition uses the required wording AI-transcribed, AI-translated and AI-produced corrections. It credits Codex’s August 2026 layers/corrections, Claude Opus 5.5 at effort max for the 10–13 November 2026 numbered-page review, and this build to GPT-6 Astra (OpenAI, ChatGPT Pro mode). Both languages carry the exact requested rights statement in their respective prefaces, including the conditional dedication of rights actually held under CC0 1.0 and the requested GitHub-issue takedown contact.',
      '',
      '## Compilation and rendered checks','',
      '| File | PDF pages | Passes | Errors | Warnings |','|---|---:|---:|---:|---:|']
    for r in compiles:text.append(f"| {Path(r['file']).name} |{r['pdf_pages']}|2|0|{r['warning_count']}|")
    text+=['',
      'All eight final sources compiled in two passes with zero errors and unchanged source hashes during compilation. The French diplomatic and reading forms each report one 2.18752 pt vertical-box warning at output 346. Both pages were viewed: original note, bottom formula and page number remain separate with no observed clipping or overlap. The French apparatus and master have no warnings. The English warnings are underfull paragraphs: five in each apparatus/master and four in each short form, with zero overfull or other final diagnostics. Every distinct warned paragraph was directly viewed; the full receipts and bounded observations are retained.',
      '',
      'French final rendered QA covers 19 directly viewed pages and confirms identical extracted page text for all 553 apparatus/master pages. The English bounded late audit directly views eight output pages at seven source loci; the English owner’s final report adds front matter, title/folio alignment, original notes, macro-sensitive formulas, apparatus and remaining layout checks. These output checks supplement the recorded source collation; they do not substitute for it.',
      '',
      'Exact path-free diagnostics are in records/COMPILE_SGA6_FR_*.json and review/english/final/EN_CANDIDATE_BUILD_STATUS.json. RELEASE_VALIDATION.json records the final 16 source/PDF hashes and the aggregate gates. Local filesystem paths and email addresses are excluded from the exported text records and readers. The supplemental RELEASE_PDF_PRIVACY.json audit covers all 20 included PDFs, including the 12 supporting source/probe PDFs, and records zero unresolved privacy matches.',
      '',
      '## Rebuilding','',
      '1. Extract the four originally supplied input archives into a common work directory, retaining their distinct original manifests. Extract the three release archives over that directory.',
      '2. Run python3 scripts/intake.py --archives followed by the four original archive filenames to verify the supplied manifests and regenerate the input registry.',
      '3. Run python3 scripts/build_french.py --final. The saved review records are the authoritative exact patch inputs. Earlier observation scripts document completed image reads and do not create automatic source verdicts.',
      '4. Run python3 scripts/compile_readers.py with the four TeX paths under readers/fr/final/. A standard complete TeX Live installation provides the required packages; the optional isolated runtime wrapper falls back to the installed environment.',
      '5. Follow review/english/final/HANDOFF.md for the exact English collection, aggregate verification, final build, compile and record commands. The exact sealed packet paths named in aggregate/INPUT_CATALOG.json are included in the English archive. Every original packet manifest and member is retained; the original collector verification remains unchanged.',
      '6. Run python3 scripts/merge_records.py, then python3 scripts/finalize_french_records.py. Run the English final record writer specified in its handoff. Run python3 scripts/finalize_release.py after the completed English/glossary/provenance reports are present.',
      '',
      'A fresh directory assembled from the planned release payloads and original inputs successfully rebuilt all eight final TeX files byte for byte. The unchanged collector verified all ten original English packet manifests and their 2,942 members. The commands, source hashes and exact results are recorded in records/RELEASE_RECONSTRUCTION.json.',
      '',
      'A rebuild may change PDF creation metadata and engine-dependent pagination; actual compile receipts bind the delivered PDFs to the delivered TeX hashes. The source reconstruction proofs and recorded decisions remain the reproducible content checks.',
      '',
      '## Historical checkpoints and omissions','',
      'All previously created numbered checkpoint archives and frozen stages remain unchanged. Their manifests, README files and archive hashes are retained under records/checkpoint_history/. Current files at a repeated relative path carry the completed reviewed state; prior byte versions remain in their named immutable checkpoint archives.',
      '',
      'RELEASE_PACKAGING_PLAN.json lists every omitted generated historical PDF and every historical checkpoint path absent from this release. The final eight PDFs are retained. The ten sealed English packets additionally retain their historical probe PDFs, images and sanitized diagnostic logs as exact original-manifest members. Outside those packets, original input archives, nested checkpoint ZIPs, runtime packages, caches, raw engine transcripts, auxiliary files and reproducible scan crops/contact sheets are omitted. Exact source-image page/region evidence, review scripts, sanitized diagnostics and reconstruction inputs are supplied. The downloaded third-party reference book review/publisher_notice_recovery/gabriel_ulmer1971.pdf and its exploratory text excerpts are omitted from final redistribution. Its source URL, byte count, page count, PDF hash and exact excerpt hashes are retained in candidates_1971.json and records/SUPPLEMENTARY_SOURCE_EXPORT.json. Both publisher front-matter PDFs used for comparison are included.','']
    (ROOT/'README.md').write_text('\n'.join(text))

def main():
    page=page_gate()
    status,decisions=decision_gate()
    french=french_gate()
    english,variants=english_gate()
    compiles=compile_gate()
    glossary=glossary_gate()
    kinds=apparatus_counts(variants)
    reconstruction=readj('records/RELEASE_RECONSTRUCTION.json')
    assert reconstruction['passed'] and reconstruction['final_TeX_reconstructed_byte_for_byte']==8
    for r in reconstruction['source_files']:assert sha(ROOT/r['path'])==r['reconstructed_sha256']
    documentation(compiles,decisions,french,english,glossary,kinds)
    final_files=[]
    for r in compiles:
        final_files.extend([dict(path=r['file'],sha256=r['source_sha256'],role='standalone annotated source'),
          dict(path=r['pdf'],sha256=r['pdf_sha256'],role='final compiled PDF')])
    status['release_complete']=True
    status['completion_basis']='records/RELEASE_VALIDATION.json; retained-source limitations explicitly stated in the reader prefaces and README.'
    save(REC/'CHECKPOINT_STATUS.json',status)
    gate=dict(passed=True,pages=page,decisions=decisions,French=dict(variants=970,branch_source_exact=True,changes_rows=french['changes_rows']),
      English=english,glossary={k:glossary[k] for k in ['glossary_rows','printed_index_rows','admitted_multiple_rendering_groups','cross_volume_difference_rows']},
      apparatus_by_kind=kinds,compiles=compiles,final_files=final_files,
      highlighted_final_disposition_pages=['431','443','464','465','590–592'],
      additional_retained_assertions_or_proof_steps='review/final_readme_audit/ADDITIONAL_RETAINED_PASSAGES.json',
      fresh_archive_union_reconstruction='records/RELEASE_RECONSTRUCTION.json',
      publisher_notice='Attributed contemporary 1971 LNM 228 restitution; covered source strokes unrecovered.',
      privacy='Final TeX, PDF extracted text, metadata and file/URI links inspected for exported private paths/email addresses; archive text records receive their own packaging gate.')
    save(REC/'RELEASE_VALIDATION.json',gate)
    print(json.dumps(dict(passed=True,books=len(compiles),final_files=len(final_files),pages=720,
      French_variants=970,English_variants=691,glossary_rows=glossary['glossary_rows'],warnings={Path(r['file']).name:r['warning_count'] for r in compiles}),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
