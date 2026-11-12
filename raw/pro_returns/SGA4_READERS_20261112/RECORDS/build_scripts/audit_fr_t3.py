"""Independent final-layer check of the 378 reviewed Tome III misprints."""
import json
from pathlib import Path
from fr_core import find_exact, searchable, page_span

ROOT=Path(__file__).resolve().parents[1]

def main():
    layers=json.loads((ROOT/'work_fr/corrected_layers.json').read_text())
    pairs=[]
    for name in ['MP_T3_PATCHES.json','MP702_810_PAIRS.json']:
        pairs.extend(json.loads((ROOT/'output/shared'/name).read_text()))
    result=[]
    for row in pairs:
        one={'id':row['id'],'part':row.get('part',1),'file':row['file'],'page':row['page']}
        for side,key in [('dip','printed'),('corr','corrected')]:
            expected=row[key]
            if row['id']=='MP0915' and side=='corr':
                # The named, separately proved OM1326 scope extension also
                # changes the adjacent divisor expression in this full span.
                original=expected
                expected=expected.replace(r"V(x'_{1},\ldots,x'_{r})",r"V(x'_{1}\cdots x'_{r})")
                one['independent_correction']=dict(source='OM-DEC-1326-PRIMED-PRODUCT',
                  before=original,after=expected,evidence='OM_1326_SCOPE_DECISION.json')
            text=layers[side][row['file']]
            hits=find_exact(text,expected,row['page'])
            if not hits:
                hits=list(dict.fromkeys(h for p in [int(row['page'])-1,int(row['page'])+1]
                                        for h in find_exact(text,expected,p)))
            opposite=row['corrected' if key=='printed' else 'printed']
            opposite_hits=list(dict.fromkeys(h for p in [int(row['page'])-1,int(row['page']),int(row['page'])+1]
                                            for h in find_exact(text,opposite,p)))
            # A printed prefix inside the corrected reading does not verify
            # the printed branch. Compare complete source spans, including
            # the surrounding notation-forming macro and punctuation.
            covered=[h for h in hits if any(a<=h[0] and h[1]<=b and (a,b)!=h for a,b in opposite_hits)]
            hits=[h for h in hits if h not in covered]
            one[side]={'expected':expected,'occurrences':len(hits),'opposite_reading_covers':covered,'verified':len(hits)==1}
            if len(hits)==1:
                a,b=hits[0]
                one[side]['actual']=text[a:b]
                one[side]['context_before']=text[max(0,a-90):a]
                one[side]['context_after']=text[b:b+90]
        result.append(one)
    out=ROOT/'output/records/FR_T3_FINAL_BRANCH_AUDIT.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    failed=[(r['id'],r['part'],s,r[s]['occurrences']) for r in result for s in ['dip','corr'] if not r[s]['verified']]
    print('records',len({r['id'] for r in result}),'parts',len(result),'failed',failed)

if __name__=='__main__':main()
