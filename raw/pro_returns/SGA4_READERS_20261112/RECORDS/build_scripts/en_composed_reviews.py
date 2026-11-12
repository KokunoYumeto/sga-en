"""Record independently specified compositions for the final English audit.

These expectations are derived from the inspected canonical pair and the
separately identified original human record or bounded notation decision.
The generated master is deliberately not read by this script.
"""
from en_common import *
import hashlib

def main():
    reviewed={}
    for p in json.loads((RECORDS/'EN_MANUAL_PAIRS.json').read_text()):
        reviewed.setdefault(p['id'],dict(id=p['id'],expose=EXPOSE[p['file']],page=p['page'],assessment='English-impact',english_deltas=[]))['english_deltas'].append(p)
    for name in ['EN_REVIEW_EXTRA45.json','EN_T3_EXACT_PAIRS.json','EN_T2_LATE_EXACT_PAIRS.json','EN_T3_AUTO_REPAIR_PAIRS.json','EN_T1_T2_EXACT_PAIRS.json']:
        for row in json.loads((ROOT/'output/shared'/name).read_text()):reviewed[row['id']]=row
    human={r['id']:r for r in json.loads((RECORDS/'EN_HUMAN_RECORDS.json').read_text())}
    out=[]
    for ident in ['MP0093','MP0100','MP0105','MP0112','MP0114','MP0129','MP0143','MP0380']:
        r=reviewed[ident]
        common=r['assessment'].lower().startswith('no')
        old=dict(printed=r['english_reading'],corrected=r['english_reading']) if common else r['english_deltas'][0]
        pair={side:old[side] for side in ['printed','corrected']}
        sources=[ident]
        if ident in ['MP0093','MP0100','MP0105','MP0112']:
            pair={side:re.sub(r'\\Pi(?![A-Za-z@])',lambda m:r'\pi',text) for side,text in pair.items()}
            sources.append('FR-ED93-PI')
            reason='The inspected local correction is composed with the bounded printed cardinal convention in I 8.13 through the end of section9. Only the exact Pi control word in this local expectation is replaced by pi; the mathematical product exception lies elsewhere.'
        elif ident=='MP0114':
            pair={side:text.replace(r'\begin{enonce*}{Lemma ',r'\begin{enonce*}{LEMMA ') for side,text in pair.items()}
            sources.append('FR-ED93-LABELS')
            reason='The heading number correction is composed with the recorded uppercase printed statement label. The number and target remain those of the inspected pair.'
        elif ident in ['MP0129','MP0143']:
            hid={'MP0129':'EN-ORG-0033','MP0143':'EN-ORG-0035'}[ident]
            h=human[hid]
            assert h['printed'].count('Academic Press')==1
            pair=dict(printed=h['printed'].replace('Academic Press','Academie Press',1),corrected=h['corrected'])
            sources.append(hid)
            reason='The diplomatic publisher spelling is the canonical Academie reading. The corrected bibliography retains the complete original human second reading, including its independently recorded quotation marks or italic title and punctuation.'
        else:
            hid='EN-ORG-0207';h=human[hid]
            target=r'\Mod(\Ysheaf{\Gamma}(S\times D),\mathcal{O}_S)'
            printed=r'\Mod(\Ysheaf{\Gamma}(S\times D,\mathcal{O}_S),\mathcal{O}_S)'
            assert h['printed'].count(target)==1
            pair=dict(printed=h['printed'].replace(target,printed,1),corrected=h['corrected'])
            sources.append(hid)
            reason='The canonical extra O_S argument is restored in the diplomatic first human paragraph. The corrected second paragraph retains the full original human construction of the additive functor and image complex; its first Mod expression has the canonical corrected argument.'
        out.append(dict(id=ident,part=1,expose=r['expose'],page=r['page'],assessment=r['assessment'],source_ids=sources,reason=reason,original_review_expected={side:old[side] for side in ['printed','corrected']},english_deltas=[dict(pair,location_verified=True,verification_basis='Independently derived from the named reviewed source pair and original human record or printed-notation decision; final master checked separately.')]))
    r=reviewed['MP0113'];base=r['english_deltas'][0]
    om=next(r for r in json.loads((ROOT/'output/shared/EN_ONE_MODEL_EXACT_PAIRS.json').read_text()) if r['id']=='OM-SOL-0136')['english_deltas'][0]
    assert base['printed'].count(om['corrected'])==1
    pair=dict(printed=base['printed'].replace(om['corrected'],om['printed'],1),corrected=base['corrected'])
    out.append(dict(id='MP0113',part=1,expose=r['expose'],page=r['page'],assessment=r['assessment'],source_ids=['MP0113','OM-SOL-0136'],reason='The canonical transfinite-recursion index repair and the independently accepted missing-predicate correction occupy one reviewed sentence. The diplomatic branch retains both printed defects; the corrected branch contains both corrected readings.',original_review_expected={side:base[side] for side in ['printed','corrected']},english_deltas=[dict(pair,location_verified=True,verification_basis='Compose the independently reviewed missing is in OM-SOL-0136 with the exact MP0113 formula pair; no generated-master text is used.')]))
    payload=dict(released_source_sha256=hashlib.sha256(RELEASE.read_bytes()).hexdigest(),method='No generated-master text is used to construct these expectations.',records=out)
    (RECORDS/'EN_COMPOSED_REVIEW_READINGS.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print(len(out),'explicit composed expectations')

if __name__=='__main__':main()
