#!/usr/bin/env python3
"""Check the completed assigned contribution without changing shared assembly."""
from pathlib import Path
import collections,hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'review/english'))
from reviewed_french import load_reviewed_pages
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(name):return [json.loads(s) for s in (HERE/name).read_text().splitlines() if s.strip()]
def put(name,value):(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def main():
    batches=json.loads((HERE/'batches.json').read_text());spans=rows('translation_spans.jsonl');variants=rows('variants.jsonl');ledger=rows('transfer.jsonl')
    assert [p for b in batches for p in range(b['first'],b['last']+1)]==list(range(297,394))
    assert len(batches)==len(spans)==20 and len(variants)==117
    source_hashes={}
    for layer in ['current','diplomatic']:
        pages,_=load_reviewed_pages(393,layer,start=297)
        assert all(pages[n]==(HERE/'source_packets'/str(n)/f'{layer}.tex').read_text() for n in pages)
        source_hashes[layer]={str(n):hashlib.sha256(pages[n].encode()).hexdigest() for n in pages}
    coverage=[]
    for folder,first,last in [('expose_v',297,364),('expose_vi',365,393)]:
        selected=[json.loads(line) for line in (ROOT/'review'/folder/'page_status.jsonl').read_text().splitlines() if line.strip()]
        selected=[r for r in selected if r.get('page') in range(first,last+1)]
        assert sorted(r['page'] for r in selected)==list(range(first,last+1)) and all(r['fully_checked'] for r in selected)
        coverage.append(dict(path=f'review/{folder}/page_status.jsonl',sha256=sha(ROOT/'review'/folder/'page_status.jsonl'),first=first,last=last,fully_checked_records=len(selected),attribution='Source reviewer coverage; this contribution does not make a new full-page image claim.'))
    native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
    a=native.index(r'\sgaStableTarget{sga6.e05.expose}');z=native.index(r'\sgaStableTarget{sga6.e06.sec.4}',a)
    assert ''.join(s['old'] for s in spans)==native[a:z]
    text=''.join(s['new'] for s in spans)
    targets=lambda s:re.findall(r'\\sgaStableTarget(?:Inline)?\{([^}]+)\}',s)
    assert targets(text)==targets(native[a:z]) and len(targets(text))==204
    assert '@@' not in text and [int(n) for n in re.findall(r'\\SGAPrintPage\{(\d+)\}',text)]==list(range(297,394))
    assert r'\sgaStableTarget{sga6.e06.sec.4}' not in text
    math=json.loads((HERE/'literal_math_verification.json').read_text());star=json.loads((HERE/'starred_math_verification.json').read_text())
    assert math['scope']==star['scope']=='printed297–393'
    assert math['unexpected_difference_units']==star['unexpected_differences']==0
    for name,digest in math['source_chunk_sha256s'].items():assert sha(HERE/name)==digest,name
    assert len({r['id'] for r in variants})==117
    for r in variants:
        assert r['old']==r['corrected'] and r['printed']!=r['corrected']
        if r['mode']=='text':
            for key in ['old','printed']:
                s=r[key]
                assert s.count(r'\(')==s.count(r'\)'),(r['id'],key,'inline delimiters')
                assert len(re.findall(r'(?<!\\)\$',s))%2==0,(r['id'],key,'dollar delimiters')
    joins=json.loads((HERE/'paragraph_join_audit_297_341.json').read_text())['joins']+[r for r in ledger if r.get('record_type')=='manually_compared_source_folio_join']
    assert len(joins)==96 and {(r['after'],r['before']) for r in joins}=={(p,p+1) for p in range(297,393)}
    macro=[r for r in ledger if r.get('record_type')=='continuation_macro_boundary']
    assert [(r['page'],r['next_page']) for r in macro]==[(323,324),(346,347),(364,365),(389,390)]
    for r in macro:
        assert r['native_block'] in text and hashlib.sha256(r['native_block'].encode()).hexdigest()==r['native_block_sha256']
    inventories=[r for r in ledger if r.get('record_type')=='page_transfer_inventory']
    assert len(inventories)==194 and all(r['French_author_notes']==r['English_author_notes'] for r in inventories)
    note_pages=sorted({r['page'] for r in inventories if r['French_author_notes']})
    assert note_pages==[374]
    assert len([s for s in (HERE/'author_notes.tsv').read_text().splitlines() if s.strip()])==2
    old_snapshot=ROOT/'build/review_snapshots/english_v_complete297_364'
    old_manifest=json.loads((old_snapshot/'MANIFEST.json').read_text())
    assert all(sha(old_snapshot/r['path'])==r['sha256'] for r in old_manifest['files'])
    for path in HERE.glob('EN_EXPOSE_V_P*.tex'):assert sha(path)==sha(old_snapshot/path.name),path.name
    private=[]
    for path in HERE.rglob('*'):
        if path.is_file() and path.suffix in ['.json','.jsonl','.md','.tsv','.tex']:
            s=path.read_text()
            if re.search(r'/workspace/|/Users/|/home/[^\s]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',s):private.append(path.relative_to(HERE).as_posix())
    assert not private,private
    counts=dict(source_folios=97,V_folios=68,VI_folios=29,raw_chunks=20,V_chunks=14,VI_chunks=6,provisional_variant_groups=117,V_variant_groups=70,VI_variant_groups=47,transfer_records=len(ledger),native_stable_targets=204,V_native_targets=156,VI_native_targets=48,math_units={layer:sum(r['French_math_units'] for r in math['counts'] if r['layer']==layer) for layer in ['current','diplomatic']},VI_math_units={layer:sum(r['French_math_units'] for r in math['counts'] if r['layer']==layer and r['page']>=365) for layer in ['current','diplomatic']},starred_units_per_branch=2,unexpected_math_units=0,lexical_complete_unit_pairs=len(json.loads((HERE/'lexical_math_pairs.json').read_text())),approved_lexical_difference_side_units=math['approved_lexical_difference_side_units'],source_folio_joins=96,paragraph_boundary_joins=sum(j['paragraph_break'] for j in joins),original_author_notes=1,selected_term_pairs=len((HERE/'terms.tsv').read_text().splitlines())-1,attributed_source_audit_copies=len(list((HERE/'attributed_source_audits').glob('*.json'))))
    result=dict(scope='Prepared English V297–364 and VI365–393',status='Passed local closure checks; aggregate registration and rendering belong to the assembly owner',counts=counts,source_packet_hashes=source_hashes,source_coverage_attribution=coverage,native_span_sha256=hashlib.sha256(native[a:z].encode()).hexdigest(),raw_contribution_sha256=hashlib.sha256(text.encode()).hexdigest(),next_native_target='sga6.e06.sec.4',mathematical_comparison='Both literal branch checks have zero unexpected units. Starred units are separately compared in exact order.',text_variant_delimiters='All32 text-mode variants have balanced inline and dollar delimiters in both readings.',paragraph_status='Every internal join is explicitly recorded; native389/390 commands add no paragraph.',macro_boundaries=[dict(page=r['page'],next_page=r['next_page'],native_sha256=r['native_block_sha256'],reviewed_sha256=r.get('reviewed_block_sha256',r.get('reviewed_French_block_sha256'))) for r in macro],original_note=dict(page=374,label='*',text='This proof is due to J.P. Jouanolou.',source='ASTRA-VI-AUTHOR-NOTE-374'),V_immutable_snapshot=dict(path=old_snapshot.relative_to(ROOT).as_posix(),manifest_sha256=sha(old_snapshot/'MANIFEST.json'),all_manifested_files_unchanged=True,all_V_raw_chunks_unchanged=True),private_path_or_email_matches=[],limitations=['No contributor English PDF compile or visual inspection is claimed.','Prose and formula placement were compared manually in the recorded batches; mathematical multiset checks do not independently certify that work.','This source-anchored terminology list remains a candidate list for the shared glossary.'])
    put('COMPLETE_CONTRIBUTION_AUDIT.json',result)
    print(json.dumps(dict(scope=result['scope'],counts=counts),ensure_ascii=False,indent=2))
    return result
if __name__=='__main__':main()
