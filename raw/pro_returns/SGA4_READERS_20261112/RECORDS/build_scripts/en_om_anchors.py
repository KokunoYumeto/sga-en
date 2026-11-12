"""Recover exact English one-model pairs; every candidate is inspected before use."""
from pathlib import Path
import collections,json,re
from en_extra import page_window,find_matches,transplant,balanced,pure_math,key
ROOT=Path(__file__).resolve().parents[1]

def candidates():
    q=json.loads((ROOT/'work_fr/en_om_review_queue.json').read_text());c=(ROOT/'work_fr/en_om_corrected_snapshot.tex').read_text();out=[]
    for row in q:
        if row['assessment']!='English-impact':continue
        r={k:v for k,v in row.items() if k!='english_page'};r['candidates']=[]
        for p in r['french_pairs']:
            old,new=p['printed'],p['corrected'];got=[]
            if pure_math(old) and pure_math(new):
                for width in (0,1):
                    lo,hi=page_window(c,r['expose'],r['page'],width)
                    for state,needle,target in [('corrected',new,old),('printed',old,new)]:
                        hits=find_matches(needle,c[lo:hi])
                        for a,b in hits:
                            a+=lo;b+=lo;actual=c[a:b]
                            # The complete TeX token must be retained.
                            if re.search(r'\\[A-Za-z]+$',c[max(0,a-100):a]) and actual[:1].isalpha():continue
                            if actual[-1:].isalpha() and c[b:b+1].isalpha():continue
                            other=transplant(actual,needle,target)
                            if other is None or not balanced(other,False):continue
                            got.append({'part':p['part'],'printed':other if state=='corrected' else actual,'corrected':actual if state=='corrected' else other,'state':state,'current_anchor':actual,'at':a,'context_before':c[max(0,a-140):a],'context_after':c[b:b+140]})
                    # A corrected full expression contains its deficient prefix.
                    seen={}
                    for g in got:seen[(g['at'],len(g['current_anchor']))]=g
                    got=list(seen.values());got=[g for g in got if not any(h['at']<=g['at'] and g['at']+len(g['current_anchor'])<=h['at']+len(h['current_anchor']) and (h['at'],len(h['current_anchor']))!=(g['at'],len(g['current_anchor'])) for h in got)]
                    if got:break
            r['candidates'].append({'part':p['part'],'matches':got})
        out.append(r)
    (ROOT/'work_fr/en_om_anchor_candidates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print('Impact',len(out),'records with unique matches all parts',sum(all(len(p['matches'])==1 for p in r['candidates']) for r in out))
if __name__=='__main__':candidates()
