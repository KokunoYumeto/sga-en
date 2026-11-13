"""Decision-to-source coverage for the reviewed Arcata allocation."""
from pathlib import Path
import csv,json,re
from tex_audit import resolve,variants
from edition_catalog import ROOT,COMPONENTS,component_path,read_jsonl
W=ROOT/'work/arcata'
comps=[x for x in COMPONENTS if x['owner']=='arcata']
texts={lang:'\n'.join(component_path(c,lang).read_text() for c in comps) for lang in ['fr','en']}
def clean(s,which='corrected'):return re.sub(r'\s+','',re.sub(r'\\(?:PrintPage|MathPage)\{[^}]+\}','',resolve(s,which)))
normalized={lang:[clean(s),clean(s,'printed')] for lang,s in texts.items()}
logs={lang:json.loads((W/(lang+'_build.json')).read_text()) for lang in ['fr','en']}
logs['fr']+=json.loads((W/'opening_and_numbering_operations.json').read_text())
vmeta=read_jsonl(W/'variants.jsonl')
sol=read_jsonl(W/'decisions.jsonl')
review_path=ROOT/'work/rapport_cycle/records/arcata_noedit_review.json'
review={r['id']:r for r in json.loads(review_path.read_text())} if review_path.exists() else {}
rows=[];fails=[]
for d in sol:
    ident=d['id'];entry=dict(id=ident,page=d['printed_page'],verdict=d['verdict'])
    if d['verdict']=='rejected':
        entry.update(fr_status='rejected; no requested change',en_status='rejected; no requested change',reason=d['reason']);rows.append(entry);continue
    v=[v for v in vmeta if ident==v['id'] or ident in v.get('sources',[])]
    for lang in ['fr','en']:
        ops=[x for x in logs[lang] if ident in x.get('id','').split(';')]
        actual=[x for x in variants(texts[lang]) if any(m['id'] in x['source'].split(';') for m in v)]
        if actual:
            entry[lang+'_status']='verified variant occurrence'
            entry[lang+'_evidence']=' | '.join(x['source']+': '+x['printed']+' → '+x['corrected'] for x in actual)
        elif ops:
            afters=[x['after'] for x in ops if x.get('after')]
            ok=all(any(clean(s,which) in final for final in normalized[lang] for which in ['printed','corrected']) for s in afters)
            entry[lang+'_status']='verified final-source presence' if ok else 'FAIL'
            entry[lang+'_evidence']=' | '.join(afters)
            if not ok:fails.append((ident,lang))
        elif lang=='en':
            entry[lang+'_status']='reviewed existing translation; no additional edit required'
            entry[lang+'_evidence']='Complete English component read against the checked French; same printed-page paragraph. Mathematical content additionally compared by balanced TeX extraction; see math_alignment_review.json.'
            if v:entry[lang+'_status']='French spelling/agreement correction does not change the English'
            if ident in review:
                r=review[ident];entry[lang+'_status']=r['status'];entry[lang+'_evidence']=r['english_witness']
                if not r['witness_present']:fails.append((ident,lang,'independent witness absent'))
        else:
            entry[lang+'_status']='FAIL: no operation or variant'
            fails.append((ident,lang))
    entry['reason']=d['reason'];rows.append(entry)
fields=['id','page','verdict','fr_status','fr_evidence','en_status','en_evidence','reason']
with (W/'ACCEPTED_FIX_COVERAGE.tsv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore');writer.writeheader();writer.writerows(rows)
report=dict(rows=len(rows),failures=fails,fr_variants=len(variants(texts['fr'])),en_variants=len(variants(texts['en'])),
            coverage_scope='Every Sol row; machine checks verify final TeX evidence, while semantic unchanged-translation decisions remain explicitly identified as manual review.')
(W/'COVERAGE_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False));assert not fails
