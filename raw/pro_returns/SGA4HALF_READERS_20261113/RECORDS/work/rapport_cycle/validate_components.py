"""Validate recorded repairs against the finalized page-marked components.

No source inference is made from a missing substring. Unresolved checks are
reported explicitly and must receive an inspected, source-specific witness.
"""
from pathlib import Path
import json,re,hashlib,collections,csv
P=Path(__file__).resolve().parent
def jlines(n):return [json.loads(l)for l in(P/n).read_text().splitlines()]
def escaped(s,i):
 n=0;i-=1
 while i>=0 and s[i]=='\\':n+=1;i-=1
 return n%2
def arg(s,i):
 while s[i].isspace():i+=1
 assert s[i]=='{',(i,s[i:i+50]);depth=1;j=i+1
 while depth:
  if not escaped(s,j):
   if s[j]=='{':depth+=1
   elif s[j]=='}':depth-=1
  j+=1
 return s[i+1:j-1],j
def expand(s,mode):
 out=[];last=0
 for m in re.finditer(r'\\var\{',s):
  if m.start()<last:continue
  a,i=arg(s,m.end()-1);b,i=arg(s,i);c,i=arg(s,i)
  out.append(s[last:m.start()]);out.append(expand(a if mode=='dip'else b,mode));last=i
 out.append(s[last:]);return ''.join(out)
def variants(s):
 out=[]
 for m in re.finditer(r'\\var\{',s):
  a,i=arg(s,m.end()-1);b,i=arg(s,i);c,i=arg(s,i)
  pg=re.findall(r'\\(?:PrintPage|MathPage)\{(\d+)\}',s[:m.start()])
  out.append(dict(id=c,printed=a,corrected=b,page=pg[-1]if pg else'',offset=m.start()))
 return out
def norm(s):
 s=re.sub(r'\\(?:PrintPage|MathPage)\{[^}]*\}','',s)
 s=re.sub(r'(?m)(?<!\\)%.*$','',s)
 return re.sub(r'\s+','',s)
def blocks(s):
 ms=list(re.finditer(r'\\(?:PrintPage|MathPage)\{(\d+)\}',s));out={}
 for i,m in enumerate(ms):out[int(m[1])]=s[m.end():ms[i+1].start()if i+1<len(ms)else len(s)]
 return out
def comp(n):return 2 if n<=109 else 3 if n<=128 else 4 if n<=153 else 5
def witness(needle,scope,mode='corr'):
 a=norm(expand(needle,mode));b=norm(expand(scope,mode))
 return bool(a)and a in b
dec=jlines('decisions.jsonl');own=jlines('own_findings.jsonl');ledger=jlines('variants.jsonl')
manual_path=P/'coverage_witnesses.json'
manual=json.loads(manual_path.read_text())if manual_path.exists()else{}
texts={};pgs={};vactual={};logs={};oldcov={};changes={}
for c in range(2,6):
 changes[c]=json.loads((P/f'en_changes_{c}.json').read_text())
 for lang,fn in [('fr',f'sga4.5-{c}.tex'),('en',f'sga4half_{c}_en.tex')]:
  key=(lang,c);texts[key]=(P/lang/fn).read_text();pgs[key]=blocks(texts[key]);vactual[key]=variants(texts[key]);logs[key]=json.loads((P/f'records/{lang}_build_{c}.json').read_text())
 for d in json.loads((P/f'records/english_coverage_{c}.json').read_text()):oldcov[d['id']]=d.get('status',d.get('english_status',''))
rows=[]
for d in dec+own:
 ident=d['id'];n=int(d.get('printed_page',d.get('page')));c=comp(n)
 for lang in ['fr','en']:
  key=(lang,c);page=pgs[key][n];scope='\n'.join(pgs[key].get(i,'')for i in range(n-1,n+2))
  rec=dict(id=ident,page=n,language=lang,component=c,verdict=d.get('verdict','accepted'),kind=d['kind'],status='',witness='',source=f'{lang}/'+(f'sga4.5-{c}.tex'if lang=='fr'else f'sga4half_{c}_en.tex'),page_sha256=hashlib.sha256(page.encode()).hexdigest())
  vv=[v for v in vactual[key]if v['id']==ident]
  ll=[l for l in logs[key]if l.get('id')==ident]
  if rec['verdict']=='rejected':rec.update(status='rejected; no repair required',witness=d['reason'])
  elif d['kind']=='marker':
   rec.update(status='page boundary present',witness=r'\PrintPage{'+str(n)+'} '+page[:160])
  elif vv:
   rec.update(status='variant occurrences verified',witness=json.dumps(vv,ensure_ascii=False))
  elif ll:
   ok=[x for x in ll if x.get('after')and(witness(x['after'],scope)or witness(x['after'],scope,'dip'))]
   if ok:rec.update(status='recorded repair present in source',witness=' || '.join(x['after']for x in ok))
   else:rec.update(status='UNRESOLVED',witness=json.dumps(ll,ensure_ascii=False))
  elif lang=='en':
   # Shared changes carry several source ids, e.g. the individually checked
   # total-degree asterisks of Cycle. Verify the transformed tokens locally.
   shared=[x for x in changes[c]if ident in x.get('sources',[])]
   if shared and any(witness(x['new'],scope)for x in shared):rec.update(status='shared English repair present',witness=' || '.join(x['new']for x in shared))
   elif oldcov.get(ident):
    # Mathematical transcription repairs often already appear verbatim in
    # the supplied English. Verify that reading at the corresponding page.
    same=[]
    if d['kind']in ['formula','symbol','number','font']:
     same=[x['after']for x in logs[('fr',c)]if x.get('id')==ident and x.get('after')and witness(x['after'],scope)]
    if same:rec.update(status='English inherited mathematical repair verified',witness=' || '.join(same))
    else:rec.update(status='English already conveys printed reading',witness=oldcov[ident])
   else:rec.update(status='UNRESOLVED',witness='No recorded English patch or explicit coverage decision.')
  elif d['kind']in['translation']:
   rec.update(status='English-only translation repair; French unchanged',witness=d['reason'])
  else:rec.update(status='UNRESOLVED',witness='No recorded French operation or variant.')
  m=manual.get(ident+':'+lang)
  if m:
   needles=m.get('needles',[])
   assert all(witness(x,scope,m.get('mode','corr'))for x in needles),(ident,lang,m)
   rec.update(status=m['status'],witness=m['reason']+' || '+' || '.join(needles))
  rows.append(rec)
(P/'records/accepted_fix_coverage.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with(P/'records/accepted_fix_coverage.tsv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
counts=collections.Counter(r['status']for r in rows)
unresolved=[r for r in rows if r['status']=='UNRESOLVED']
print('COVERAGE',len(rows),'rows',dict(counts))
for r in unresolved:print(r['id'],r['language'],r['page'],r['witness'][:1000])
part_counts={}
for c,lo,hi in [(2,76,109),(3,110,128),(4,129,153),(5,154,167)]:
 part_counts[c]={}
 for lang in ['fr','en']:
  assert list(pgs[(lang,c)])==list(range(lo,hi+1)),(lang,c,'page markers')
  actual=vactual[(lang,c)]
  for v in actual:
   candidates=[x for x in ledger if x['id']==v['id']]
   def pair(x):
    if lang=='fr':return x['printed'],x['corrected']
    return x.get('printed_en',x.get('en_printed',x['printed'])),x.get('corrected_en',x.get('en_corrected',x['corrected']))
   assert any(norm(a)==norm(v['printed'])and norm(b)==norm(v['corrected'])for a,b in map(pair,candidates)),(lang,c,v)
   assert norm(v['printed'])!=norm(v['corrected']),(lang,c,'identical variant',v)
  part_counts[c][lang]=dict(markers=len(pgs[(lang,c)]),variants=len(actual),all_variant_pairs_match_ledger=True,all_variants_change_content=True)
status=dict(rows=len(rows),sol_ids=len(dec),own_ids=len(own),status_counts=dict(counts),unresolved=len(unresolved),parts=part_counts)
(P/'records/accepted_fix_coverage_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
assert not unresolved,'Unresolved source coverage checks remain.'
