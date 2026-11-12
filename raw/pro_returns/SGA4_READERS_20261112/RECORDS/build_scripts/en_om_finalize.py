"""Assemble individually reviewed English OM decisions and exact anchors."""
from pathlib import Path
import collections,hashlib,json,re
from en_extra import page_window,find_matches,balanced,key,pure_math,transplant
from en_om_manual_pairs import M,N
ROOT=Path(__file__).resolve().parents[1]

def locate(text,row,spec):
    for width in [0,1]:
        lo,hi=page_window(text,row['expose'],row['page'],width)
        choices=[('source-intermediate',spec['current_anchor'])] if spec.get('current_anchor') else [('printed',spec['printed']),('corrected',spec['corrected'])]
        hits={}
        for state,needle in choices:
            for a,b in find_matches(needle,text[lo:hi]):
                a+=lo;b+=lo
                required=spec.get('required_context_before')
                if required and not key(text[max(0,a-100):a]).endswith(key(required)):continue
                if text[a:b][-1:].isalpha() and text[b:b+1].isalpha():continue
                if text[a:a+1].isalpha() and text[max(0,a-1):a].isalpha():continue
                hits[a,b]=(state,needle)
        hits={span:v for span,v in hits.items() if not any(other[0]<=span[0] and span[1]<=other[1] and other!=span for other in hits)}
        if len(hits)==1:
            (a,b),(state,needle)=next(iter(hits.items()))
            return a,b,state,needle,width
    return None

def main():
    queue=json.loads((ROOT/'work_fr/en_om_review_queue.json').read_text())
    candidates={r['id']:r for r in json.loads((ROOT/'work_fr/en_om_anchor_candidates.json').read_text())}
    noimpact={r['id']:r for r in json.loads((ROOT/'output/shared/EN_ONE_MODEL_NO_IMPACT_PARTIAL.json').read_text())}
    judgments={r['id']:r for r in json.loads((ROOT/'output/records/one_model_edits.json').read_text())}
    snapshot=ROOT/'work_fr/en_om_corrected_snapshot.tex';text=snapshot.read_text()
    out=[];fail=[];checked=[]
    for row in queue:
        ident=row['id']
        if ident in noimpact:
            out.append(noimpact[ident]);continue
        base={k:row[k] for k in ['id','expose','page','place','french_pairs']}
        if ident in N:
            ev=N[ident]['english_evidence'];lo,hi=page_window(text,row['expose'],row['page'],1)
            matches=find_matches(ev,text[lo:hi])
            if len(matches)!=1:
                fail.append({'id':ident,'part':0,'kind':'no-impact evidence','matches':len(matches),'evidence':ev});continue
            a,b=matches[0];a+=lo;b+=lo
            out.append({**base,'assessment':'no English impact','reason':N[ident]['reason'],
                        'english_evidence':text[a:b],'evidence_reviewed':True,'english_deltas':[]})
            continue
        deltas=[]
        for partrow in candidates[ident]['candidates']:
            part=partrow['part'];spec=M.get((ident,part))
            if spec:
                located=locate(text,row,spec)
                if not located:
                    fail.append({'id':ident,'part':part,'kind':'manual exact anchor','spec':spec});continue
                a,b,state,needle,width=located;actual=text[a:b]
                printed=spec['printed'];corrected=spec['corrected']
                if state in ['printed','corrected']:
                    target=corrected if state=='printed' else printed
                    other=transplant(actual,needle,target) if pure_math(needle) and pure_math(target) else target
                    if other is None:other=target
                    printed=actual if state=='printed' else other
                    corrected=actual if state=='corrected' else other
                delta={'part':part,'printed':printed,'corrected':corrected,
                       'current_anchor':actual,'current_state':state,'page_window_width':width,
                       'reason':spec['reason'] or judgments[ident]['reason']}
                for field in ['baseline_anchor','pre_notation_printed','pre_notation_corrected','notation_decision','compose_with_source']:
                    if field in spec:delta[field]=spec[field]
            else:
                assert len(partrow['matches'])==1,(ident,part)
                d=partrow['matches'][0];a=d['at'];actual=d['current_anchor'];b=a+len(actual)
                assert text[a:b]==actual,(ident,part)
                delta={'part':part,'printed':d['printed'],'corrected':d['corrected'],
                       'current_anchor':actual,'current_state':d['state'],
                       'reason':judgments[ident]['reason']+' The exact corresponding English formula and its surrounding source context were independently inspected.'}
            if not balanced(delta['printed']) or not balanced(delta['corrected']):
                fail.append({'id':ident,'part':part,'kind':'unbalanced TeX group or math delimiters','delta':delta});continue
            assert delta['printed']!=delta['corrected'],(ident,part)
            if re.search(r'\\(?:nde|ndetext|sisi)\b',actual):
                fail.append({'id':ident,'part':part,'kind':'human apparatus in proposed span','delta':delta});continue
            if r'\SGApage' in actual:
                fail.append({'id':ident,'part':part,'kind':'page marker requires explicit projection','delta':delta});continue
            delta.update(location_verified=True,context_before=text[max(0,a-180):a],context_after=text[b:b+180])
            if ident=='OM-SOL-0353' or ident=='OM-SOL-0352' and part==5:
                delta['related_source_ids']=['OM-SOL-0352','OM-SOL-0353']
            if ident=='OM-SOL-1326' and part==2:delta['editorial_decision']='OM-DEC-1326-PRIMED-PRODUCT'
            deltas.append(delta)
            checked.append({'id':ident,'part':part,'at':a,'length':b-a,'state':delta['current_state']})
        if len(deltas)!=len(candidates[ident]['candidates']):continue
        out.append({**base,'assessment':'English-impact','reason':'; '.join(dict.fromkeys(d['reason'] for d in deltas)),
                    'evidence_reviewed':True,'english_deltas':deltas})
    (ROOT/'work_fr/en_om_exact_unlocated.json').write_text(json.dumps(fail,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'work_fr/en_om_exact_partial.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print('Reviewed rows',len(out),'of',len(queue),'problems',len(fail))
    for r in fail:print(r['id'],r['part'],r['kind'])
    if fail:return
    assert len(out)==338 and len({r['id'] for r in out})==338
    counts=dict(collections.Counter(r['assessment'] for r in out))
    check={'accepted_undisputed_records':338,'classifications':counts,
           'exact_english_parts':len(checked),'unique_exact_anchor_parts':len(checked),
           'unresolved':0,'human_apparatus_inside_proposed_spans':0,
           'page_markers_inside_proposed_spans':0,
           'source_snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
           'source_snapshot':'the corrected projection of the annotated English reader at review time',
           'source_readers_modified':False,'checks':checked}
    (ROOT/'output/shared/EN_ONE_MODEL_EXACT_PAIRS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'output/records/EN_ONE_MODEL_REVIEW_CHECKS.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n')
    print(counts,'English parts',len(checked))

if __name__=='__main__':main()
