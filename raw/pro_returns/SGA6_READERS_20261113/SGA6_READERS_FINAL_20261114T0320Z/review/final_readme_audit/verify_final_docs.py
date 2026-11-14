#!/usr/bin/env python3
"""Read-only consistency checks for final README and apparatus tables."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent


def readj(path):
    return json.loads((ROOT/path).read_text())


def readtsv(path):
    return list(csv.DictReader((ROOT/path).open(),delimiter='\t'))


def main():
    tables=readtsv('records/APPARATUS_COUNTS.tsv')
    lookup={(r['language'],r['expose'],r['kind'],r['form']):int(r['entries']) for r in tables}
    assert len(lookup)==len(tables)==576
    fr=readj('records/FR_APPARATUS_SOURCE_LINKS.json')
    en=readj('review/final_english_classification/CLASSIFICATION.json')
    for row in en['summary']['by_expose']:
        expose={'Indexes':'Indices'}.get(row['expose'],row['expose'])
        for kind,count in row['by_kind'].items():
            assert lookup[('EN',expose,kind,'corrected apparatus')]==count
    bounds=[(1,77,'0'),(78,159,'I'),(160,221,'II'),(222,273,'III'),(274,296,'IV'),
            (297,364,'V'),(365,415,'VI'),(416,465,'VII'),(466,497,'VIII'),(498,518,'IX'),
            (519,594,'X'),(595,615,'XII'),(616,666,'XIII'),(667,689,'XIV'),(691,700,'Indices')]
    fr_counts=Counter()
    for row in fr['variants']:
        page=str(row['page'])
        expose=next((name for a,b,name in bounds if a<=int(page)<=b),'unmapped') if page.isdigit() else ('Rear publisher matter' if page.startswith('rear') else 'Front matter')
        fr_counts[expose,row['kind']]+=1
    for (expose,kind),count in fr_counts.items():
        assert lookup[('FR',expose,kind,'corrected apparatus')]==count
    for row in tables:
        n=int(row['entries'])
        if row['form'] in ['diplomatic','reading']:
            assert n==0
        else:
            assert n==lookup[(row['language'],row['expose'],row['kind'],'corrected apparatus')]
    totals={language:dict(Counter({kind:sum(int(r['entries']) for r in tables if r['language']==language and r['form']=='corrected apparatus' and r['kind']==kind)
                                  for kind in {r['kind'] for r in tables}})) for language in ['FR','EN']}
    assert totals['FR']==fr['summary']['by_kind']
    assert totals['EN']==en['summary']['by_kind']
    gate=readj('records/RELEASE_VALIDATION.json');assert gate['passed']
    assert gate['apparatus_by_kind']==totals
    glossary=readj('review/english/terminology_final/HANDOFF.json')
    for field,value in gate['glossary'].items():
        assert glossary['exact_counts'][field]==value
    counts={}
    expected={'FINDINGS_DECIDED.tsv':9264,'MISPRINTS_6_DECIDED.tsv':966,
              'CHECK_FINDINGS.tsv':1923,'DECISIONS.tsv':226,'PAGES_CHECKED.tsv':720,
              'OPEN_ITEMS_DECIDED.tsv':23,'PRIOR_RESOLVED_REPLAY_REVIEW.tsv':4,'CODEX_DECIDED.tsv':260}
    for name,count in expected.items():
        counts[name]=len(readtsv('records/'+name));assert counts[name]==count
    pages=readtsv('records/PAGES_CHECKED.tsv')
    assert all(r['image'] and r['region'] and r['FR_master_begin'] and r['EN_master_begin'] for r in pages)
    note_audit=readj('review/english/aggregate/ORIGINAL_NOTE_LABEL_AUDIT.json')
    notes=[]
    for row in note_audit['branches']:
        assert row['author_note_commands']==len(row['exact_page_command_label_sequence'])==111
        notes.append(dict(branch=row['layer'],commands=111,
                          distinct_label_values=len({r['label'] for r in row['exact_page_command_label_sequence']})))
    reconstruction=readj('records/RELEASE_RECONSTRUCTION.json')
    assert reconstruction['passed'] and reconstruction['final_TeX_reconstructed_byte_for_byte']==8
    assert reconstruction['exact_English_packets_verified']==10 and reconstruction['packet_manifests_unchanged']
    readme=(ROOT/'README.md').read_text()
    docs=[]
    for name in ['README.md','records/APPARATUS_COUNTS.md','records/APPARATUS_COUNTS.tsv']:
        data=(ROOT/name).read_bytes();docs.append(dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    report=dict(record_type='read_only_final_document_consistency_review',
        reviewed_documents=docs,apparatus_table_rows_checked=576,apparatus_totals=totals,
        table_rows=counts,glossary_counts_verified=gate['glossary'],original_author_note_counts=notes,
        all_page_evidence_and_master_location_fields_populated=True,
        fresh_reconstruction_evidence='records/RELEASE_RECONSTRUCTION.json',
        reproduction_commands_assessed='README intake/build/compile commands match current argument interfaces; English handoff supplies exact aggregate order. Fresh archive-union reconstruction records eight byte-identical final TeX files and ten unchanged packet manifests.',
        factual_count_discrepancies=[],apparatus_MD_and_TSV_discrepancies=[],
        significant_spacing_typos_in_scoped_documents=[],
        qualification_finding=dict(
            issue='The retained-source examples originally listed only selected final-disposition pages while the opening referred generally to retained-source limitations.',
            supporting_index='review/final_readme_audit/ADDITIONAL_RETAINED_PASSAGES.json',
            existing_decisions_indexed=17,
            requested_action='Identify the existing final-disposition examples as selected and link the additional retention index, preserving its statement/proof-step scope distinctions.',
            explicit_additional_index_now_in_README='ADDITIONAL_RETAINED_PASSAGES' in readme),
        minor_wording_suggestion='111 counts author-note command instances, not distinct label values. “All 111 original author-note commands and their label/geometry keys agree” avoids that possible ambiguity.',
        new_source_scan_claim=False,new_mathematical_claim=False,shared_docs_or_sources_modified=False)
    (HERE/'FINAL_DOCUMENT_REVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(apparatus_rows=576,factual_count_errors=0,
                          additional_index_in_README=report['qualification_finding']['explicit_additional_index_now_in_README'],
                          original_note_counts=notes)))


if __name__=='__main__':
    main()
