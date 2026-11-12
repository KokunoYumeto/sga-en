"""Check final assembled English OM branches against independently reviewed pairs."""
from pathlib import Path
import collections,difflib,hashlib,json,re
from en_one_model_review import selected
from en_extra import compact,find_matches,page_window,key
ROOT=Path(__file__).resolve().parents[1]

def inspect_context(evidence,text,expose,page):
    lo,hi=page_window(text,expose,page,1)
    context=text[lo:hi];ek,em=compact(evidence);ck,cm=compact(context)
    match=difflib.SequenceMatcher(None,ek,ck,autojunk=False).find_longest_match()
    if not match.size:return {'verified':False,'matched_key_characters':0}
    a,b=cm[match.b][0],cm[match.b+match.size-1][1]
    x,y=em[match.a][0],em[match.a+match.size-1][1]
    return {'verified':match.size>=40,'matched_key_characters':match.size,
            'reviewed_context_span':evidence[x:y],'actual_context_span':context[a:b],
            'actual_before':context[max(0,a-80):a],'actual_after':context[b:b+80]}

def main():
    path=ROOT/'output/en/SGA4_EN_annotated_master.tex';master=path.read_text()
    start=master.index(r'\mainmatter');end=master.index(r'\backmatter')
    body=master[start:end];dip=selected(body,False);corr=selected(body,True)
    variants=json.loads((ROOT/'output/records/EN_VARIANTS.json').read_text())
    linked=collections.defaultdict(list)
    for v in variants:
        for ident in re.findall(r'OM-(?:OPUS|SOL)-\d{4}',v['source']):linked[ident].append(v)
    rows=json.loads((ROOT/'output/shared/EN_ONE_MODEL_EXACT_PAIRS.json').read_text())
    out=[];problems=[]
    canonical=json.loads((ROOT/'output/shared/EN_T3_AUTO_REPAIR_PAIRS.json').read_text())
    mp915=next(x for x in canonical if x['id']=='MP0915')['english_deltas'][0]
    for r in rows:
        ident=r['id'];entry={'id':ident,'expose':r['expose'],'page':r['page'],
                            'assessment':r['assessment'],'variant_ids':[v['id'] for v in linked[ident]],'parts':[]}
        if r['assessment']=='no English impact':
            entry['context_checks']={side:inspect_context(r['english_evidence'],text,r['expose'],r['page'])
                                     for side,text in [('printed',dip),('corrected',corr)]}
            entry['status']='verified-no-English-delta' if not linked[ident] and all(x['verified'] for x in entry['context_checks'].values()) else 'requires-review'
            if entry['status']=='requires-review':problems.append(entry)
            entry['evidence']=r['english_evidence'];entry['reason']=r['reason'];entry['french_pairs']=r['french_pairs'];out.append(entry);continue
        for d in r['english_deltas']:
            expected={side:d[side] for side in ['printed','corrected']}
            part={'part':d['part'],'reviewed_expected':dict(expected)}
            if ident=='OM-SOL-1326' and d['part']==2:
                # The independently reviewed MP0915 prefix composes with this
                # product equation. This derives the expected branch from two
                # review inputs, never from generated master bytes.
                old,new=mp915['printed'],mp915['corrected']
                assert key(new) in key(expected['printed'])
                hits=find_matches(new,expected['printed']);assert len(hits)==1
                a,b=hits[0];expected['printed']=expected['printed'][:a]+old+expected['printed'][b:]
                part['composition']={'source_ids':['MP0915','OM-SOL-1326','OM-DEC-1326-PRIMED-PRODUCT'],
                    'review_inputs':['shared/EN_T3_AUTO_REPAIR_PAIRS.json','shared/EN_ONE_MODEL_EXACT_PAIRS.json'],
                    'operation':'Use the MP0915 printed Y prefix in the diplomatic branch; retain the independently reviewed OM product correction in the corrected branch.',
                    'canonical_prefix_pair':{'printed':old,'corrected':new}}
            part['expected_after_composition']=expected
            for side,text in [('printed',dip),('corrected',corr)]:
                lo,hi=page_window(text,r['expose'],r['page'],1)
                context=text[lo:hi];hits=find_matches(expected[side],context);part[side+'_literal_hits']=len(hits)
                part[side+'_actual_spans']=[{'text':context[a:b],'before':context[max(0,a-90):a],'after':context[b:b+90]} for a,b in hits]
                part[side+'_in_linked_variant']=[v['id'] for v in linked[ident] if key(expected[side]) in key(selected(v[side],side=='corrected'))]
            part['status']='verified-literal-pair' if all(part[s+'_literal_hits'] and part[s+'_in_linked_variant'] for s in ['printed','corrected']) else 'requires-composed-span-review'
            if part['status']!='verified-literal-pair':
                problems.append({'id':ident,'expose':r['expose'],'page':r['page'],**part,'expected':d,'linked_variants':linked[ident]})
            entry['parts'].append(part)
        entry['status']='verified' if all(p['status']=='verified-literal-pair' for p in entry['parts']) else 'requires-composed-span-review';out.append(entry)
    (ROOT/'work_fr/en_om_final_branch_problems.json').write_text(json.dumps(problems,ensure_ascii=False,indent=2)+'\n')
    audit={'passed':not problems,'master_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'master':'en/SGA4_EN_annotated_master.tex',
           'review_input':'shared/EN_ONE_MODEL_EXACT_PAIRS.json',
           'review_input_sha256':hashlib.sha256((ROOT/'output/shared/EN_ONE_MODEL_EXACT_PAIRS.json').read_bytes()).hexdigest(),
           'records':len(out),'impact_records':sum(r['assessment']=='English-impact' for r in rows),
           'no_impact_records':sum(r['assessment']=='no English impact' for r in rows),
           'parts':sum(len(r['parts']) for r in out),'problems':len(problems),
           'comparison_method':'Each mathematical pair is checked in both selected page contexts and in its source-linked variant. The compact comparison uses only the explicitly enumerated TeX/glyph maps in build_scripts/en_extra.py; actual raw matched spans are retained. No-impact judgments retain the individually reviewed French pair and English evidence, with a final unchanged context span and absence of an OM variant verified separately.',
           'rows':out}
    (ROOT/'work_fr/en_om_final_branch_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'output/records/EN_ONE_MODEL_FINAL_BRANCH_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print('Records',len(out),'problems',len(problems))
    for p in problems:print(p['id'],p.get('part','no-impact'),p.get('printed_literal_hits'),p.get('corrected_literal_hits'),p.get('variant_ids'))

if __name__=='__main__':main()
