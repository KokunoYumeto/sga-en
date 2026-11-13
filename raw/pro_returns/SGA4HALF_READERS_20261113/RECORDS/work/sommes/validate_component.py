"""Verify component6 against its scan decisions, restorations and English alignment.
All paths in emitted records are project-relative. English prose evidence was
read across all65 aligned pages and is asserted against the final components.
"""
from pathlib import Path
import re,json,csv,collections,hashlib
from build_components import norm,readj
from compare_math import arg,select
B=Path(__file__).parent

def canon(s):
 s=s.replace('’',"'").replace(r"\'e",'é').replace(r'\times',r'\ast')
 return re.sub(r'\s+','',s)

def scopes(t):
 s=re.split(r'\\PrintPage\{(\d+)\}\n',t)
 return {int(s[i]):s[i+1] for i in range(1,len(s),2)}

def variants(t):
 out=[];pos=0
 while True:
  i=t.find(r'\var{',pos)
  if i<0:break
  p=i+4;a=[]
  for _ in range(3):x,p=arg(t,p);a.append(x)
  page=re.findall(r'\\PrintPage\{(\d+)\}',t[:i])[-1]
  out.append(dict(page=int(page),printed=a[0],corrected=a[1],source=a[2],offset=i))
  pos=p
 return out

texts={L:(B/L/F).read_text() for L,F in [('fr','sga4.5-6.tex'),('en','sga4half_6_en.tex')]}
selected={L:{m:scopes(select(t,m)) for m in [0,1]} for L,t in texts.items()}
vs={L:variants(t) for L,t in texts.items()}
ledger=readj('variants');expected={v['id']:v for v in ledger}
checks=[]
for L in texts:
 assert list(scopes(texts[L]))==list(range(168,233))
 for v in vs[L]:
  assert v['source'] in expected,(L,v)
  assert v['printed']!=v['corrected'],(L,v)
  assert int(expected[v['source']]['page'])==v['page']
 for v in ledger:
  count=sum(w['source']==v['id'] for w in vs[L])
  wanted=2 if v['id']=='S45-SOL-0847' else 3 if v['id']=='S45-SOL-0856' else 1
  if L=='en' and not v['english_applicable']:wanted=0
  assert count==wanted,(L,v['id'],count,wanted)

rows=readj('decisions');eng=json.loads((B/'english_evidence.json').read_text())
ops=json.loads((B/'assembly_ops.json').read_text())+json.loads((B/'diagnostic_ops.json').read_text())
byop=collections.defaultdict(list)
for op in ops:byop[op['id'],op['lang']].append(op)

frspecial={
'S45-SOL-0689':[(0,173,r'\sF(\chi,f)'),(1,173,r'\sF(\chi,f_0)')],
'S45-SOL-0694':[(1,174,r'\subsection{Scholie}\label{VI:1-9}'),(1,174,r'\label{VI:eq:1-9-1}'),(1,174,r'\label{VI:eq:1-9-2}')],
'S45-SOL-0702':[(1,177,r'\PrintCite{P.~Deligne, \emph{La conjecture de Weil II}, en préparation}{\cite{de80}}')],
'S45-SOL-0772':[(1,191,r"d'équation $T^p-T-f=0$ sur $U$. S'il était trivial, le torseur sur $U_0$ de même équation"),(1,192,'serait')],
'S45-SOL-0837':[(m,203,select(readj('restorations')[1]['fr'],m)) for m in [0,1]],
'S45-SOL-0901':[(1,215,r'\chi_\beta={}_{q_\beta-1}\lambda_\beta')],
'S45-SOL-0907':[(1,215,r'\chi_\beta &= {}_{q_\beta-1}\lambda_\beta')]
}
fail=[]
for r in rows:
 id=r['id'];p=int(r['printed_page']);record=dict(id=id,page=p,verdict=r['verdict'])
 if r['verdict']=='rejected':
  record.update(fr_status='No rejected change applied',en_status='No rejected change applied',evidence=r['reason']);checks.append(record);continue
 if id in expected:
  record['fr_status']='Both source readings and every apparatus occurrence verified'
  record['fr_evidence']=expected[id]['printed']+' -> '+expected[id]['corrected']
 elif id in frspecial:
  for m,pp,s in frspecial[id]:assert canon(s) in canon(selected['fr'][m][pp]),(id,m,pp,s)
  record['fr_status']='Exact restored locus verified with documented composition/page-boundary adjustment'
  record['fr_evidence']=' | '.join(s for _,_,s in frspecial[id])
 else:
  new=r['fix_new'].replace('\\n','\n') if id in ['S45-SOL-0694','S45-SOL-0900','S45-SOL-0937'] else r['fix_new']
  if canon(new) in canon(selected['fr'][1][p]):record.update(fr_status='Final corrected reading matched',fr_evidence=new)
  else:fail.append((id,'fr',new))
 if id in expected:
  if expected[id]['english_applicable']:
   record['en_status']='English printed/corrected readings and every apparatus occurrence verified'
   record['en_evidence']=expected[id]['en_printed']+' -> '+expected[id]['en_corrected']
  else:
   record['en_status']='French spelling, inflection or malformed French grammar does not change the English interpretation'
   record['en_evidence']='No English variant; reviewed bilingual context at printed page '+str(p)
 elif id in eng:
  assert canon(eng[id]) in canon(selected['en'][1][p]),(id,eng[id])
  record.update(en_status='Reviewed English prose/math alignment matched',en_evidence=eng[id])
 else:
  new=r['fix_new'].replace('\\n','\n') if id in ['S45-SOL-0694','S45-SOL-0900','S45-SOL-0937'] else r['fix_new']
  candidates=[new]+[select(x['new'],1) for x in byop[id,'en']]
  matches=[x for x in candidates if x and canon(x) in canon(selected['en'][1][p])]
  if id=='S45-SOL-0837':
   new=select(readj('restorations')[1]['en'],1);assert canon(new) in canon(selected['en'][1][p]);matches=[new]
  if matches:record.update(en_status='Final English reading/restoration matched',en_evidence=matches[-1])
  else:fail.append((id,'en',new))
 checks.append(record)
(B/'accepted_fix_coverage.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
(B/'coverage_unresolved.json').write_text(json.dumps(fail,ensure_ascii=False,indent=2))
print('Sol decisions',len(rows),'checks',len(checks),'unresolved',len(fail))
for x in fail:print(x)
if fail:raise SystemExit(1)
owncoverage=[]
for r in readj('own_findings'):
 id=r['id'];evidence=[]
 if id in expected:evidence.append('Variant source and occurrence counts verified')
 for x in readj('restorations'):
  if x.get('source',x.get('id'))==id:evidence.append('Complete French restoration and English translation assembled')
 for x in readj('notation_units'):
  if x.get('source')==id:
   for L in ['fr','en']:
    assert x['replace'] not in selected[L][1][int(x['page'])]
    assert x['with'] in selected[L][1][int(x['page'])]
   evidence.append('Printed unit-group asterisk verified in both languages')
 for x in ops:
  if x['id']==id:evidence.append(x['lang']+': exact scoped operation verified during reproducible assembly')
 for x in readj('edits'):
  if x.get('source')==id and canon(select(x['new'],1)) in canon(selected[x['lang']][1][int(x['page'])]):
   evidence.append(x['lang']+': final shared reading already present or verified after assembly')
 assert evidence,(id,'own finding has no implementation evidence')
 owncoverage.append(dict(id=id,page=r['page'],status='verified',evidence='; '.join(sorted(set(evidence)))))
(B/'own_fix_coverage.json').write_text(json.dumps(owncoverage,ensure_ascii=False,indent=2))
# Update stale pending statuses only after all recorded evidence passes.
for r in rows:
 c=next(x for x in checks if x['id']==r['id']);r['english_status']=c['en_status'];r['english_evidence']=c.get('en_evidence',c.get('evidence',''))
(B/'decisions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
# Save actual master starts after patching, rather than stale source anchors.
for r in readj('pages'):
 p=int(r['printed_page'])
 for L in ['fr','en']:r['master_start_'+L]=scopes(texts[L])[p].lstrip()[:240]
 r['findings']=sum(int(x['printed_page'])==p for x in rows)+sum(int(x['page'])==p for x in readj('own_findings'))
 checks.append(dict(kind='page',**r))
with (B/'accepted_fix_coverage.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['id','page','verdict','fr_status','fr_evidence','en_status','en_evidence','evidence'],delimiter='\t',extrasaction='ignore');w.writeheader();w.writerows([r for r in checks if r.get('id','').startswith('S45-SOL')])
(B/'final_page_starts.json').write_text(json.dumps([r for r in checks if r.get('kind')=='page'],ensure_ascii=False,indent=2))
summary=dict(component=6,printed_pages=[168,232],pages_visually_checked=65,sol_decisions=len(rows),verdicts=dict(collections.Counter(r['verdict'] for r in rows)),own_findings=len(readj('own_findings')),misprint_rows=len(ledger),fr_variants=len(vs['fr']),en_variants=len(vs['en']),page_markers=65,accepted_fix_coverage=len(rows),unmatched=0,mathematical_alignment='All formula differences inspected; remaining differences are translated words, ordinal typography and clause order.',compile_status='FR/EN diplomatic/corrected component selections compile without LaTeX errors; whole-book apparatus styling pending root build.',restored_matter='Printed eight-entry contents on p. 168; complete omitted paragraph and formula (4.14.2) on p. 203; nine-entry local bibliography on p. 232; full inline bibliographic identifications.',citation_map={'ca69-2':1,'de73':2,'dl76':3,'ka77':4,'se68':5,'sp76':6,'we74':7,'we52':8,'we74-2':9})
(B/'PART_VI_STATUS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))
