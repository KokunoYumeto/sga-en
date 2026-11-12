"""Check the inspected English pairs against both assembled master branches.

The input order is the same explicit precedence order used by en_extra.py.
The byte-to-token map in en_extra.compact is included with the build scripts.
No occurrence is credited merely because its item ID appears in an inventory.
"""
import hashlib,json,re
from pathlib import Path
from build_en import select_inline_variants
from en_common import EXPOSE
from en_extra import find_matches,page_window

ROOT=Path(__file__).resolve().parents[1]
INPUTS=['EN_REVIEW_EXTRA45.json','EN_T3_EXACT_PAIRS.json',
        'EN_T2_LATE_EXACT_PAIRS.json','EN_T3_AUTO_REPAIR_PAIRS.json',
        'EN_T1_T2_EXACT_PAIRS.json']

def inspect(text,expected,opposite,exp,page):
    for width in [0,1]:
        window=page_window(text,exp,page,width)
        if window is None:continue
        a,b=window;local=text[a:b]
        hits=find_matches(expected,local)
        other=find_matches(opposite,local) if opposite and opposite!=expected else []
        covered=[h for h in hits if any(x<=h[0] and h[1]<=y and (x,y)!=h for x,y in other)]
        hits=[h for h in hits if h not in covered]
        if len(hits)==1:
            x,y=hits[0]
            return dict(verified=True,occurrences=1,window_pages=width,actual=local[x:y],
              context_before=local[max(0,x-100):x],context_after=local[y:y+100])
    return dict(verified=False,occurrences=len(hits) if window else 0,
      expected=expected,opposite_reading_covers=covered if window else [])

def main():
    master=(ROOT/'output/en/SGA4_EN_annotated_master.tex').read_text()
    bodies={side:select_inline_variants(master,flag).split(r'\backmatter',1)[0]
            for side,flag in [('diplomatic',False),('corrected',True)]}
    for side in bodies:
        bodies[side]=re.sub(r'\\SGAvariantmark\{[^}]+\}','',bodies[side])
    rows={}
    manual=ROOT/'output/records/EN_MANUAL_PAIRS.json'
    for p in json.loads(manual.read_text()) if manual.exists() else []:
        rows.setdefault(p['id'],dict(id=p['id'],expose=EXPOSE[p['file']],page=p['page'],
          assessment='English-impact',review_file='EN_MANUAL_PAIRS.json',english_deltas=[]))['english_deltas'].append(p)
    for name in INPUTS:
        path=ROOT/'output/shared'/name
        for r in json.loads(path.read_text()) if path.exists() else []:
            rows[r['id']]=dict(r,review_file=name)
    composed=ROOT/'output/records/EN_COMPOSED_REVIEW_READINGS.json'
    if composed.exists():
        for r in json.loads(composed.read_text())['records']:
            row=dict(r,review_file='EN_COMPOSED_REVIEW_READINGS.json')
            if row['assessment'].lower().startswith('no'):
                assert len(row['english_deltas'])==1
                assert row['english_deltas'][0]['printed']==row['english_deltas'][0]['corrected']
                row['english_reading']=row['english_deltas'][0]['printed']
            rows[r['id']]=row
    result=[]
    for ident,r in sorted(rows.items()):
        common=r['assessment'].lower().startswith('no')
        deltas=[dict(printed=r.get('english_reading',r.get('anchor','')),
                     corrected=r.get('english_reading',r.get('anchor','')))] if common else r.get('english_deltas',[r.get('english_delta',{})])
        for part,d in enumerate(deltas,1):
            if not d:continue
            row=dict(id=ident,part=part,expose=r['expose'],page=r['page'],
              review_file=r['review_file'],assessment=r['assessment'])
            for side,k,other in [('diplomatic','printed','corrected'),('corrected','corrected','printed')]:
                expected=d.get(k,'')
                row[side]=inspect(bodies[side],expected,d.get(other,''),r['expose'],r['page']) if expected else dict(verified=False,reason='No literal English anchor supplied in the reviewed input.')
            result.append(row)
    payload=dict(master_sha256=hashlib.sha256(master.encode()).hexdigest(),
      item_count=len({r['id'] for r in result}),part_count=len(result),
      passed=all(r[s]['verified'] for r in result for s in ['diplomatic','corrected']),parts=result)
    (ROOT/'output/records/EN_REVIEWED_FINAL_BRANCH_AUDIT.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    failures=[(r['id'],r['part'],s,r[s].get('occurrences'),r[s].get('reason')) for r in result for s in ['diplomatic','corrected'] if not r[s]['verified']]
    print('English inspected pairs:',payload['item_count'],'items,',len(result),'parts; failing sides',len(failures))
    for fail in failures:print(fail)
    return payload

if __name__=='__main__':main()
