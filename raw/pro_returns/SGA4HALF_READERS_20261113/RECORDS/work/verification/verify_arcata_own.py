# Invoke this script with python3.
"""Check each of the 44 Arcata own findings against explicit final-source evidence.

Operation targets and source variants are checked mechanically. Source-preserving
decisions use reviewed literal witnesses in arcata_own_witnesses.json. No reader
or component is edited. A nonzero exit reports unresolved coverage.
"""
from pathlib import Path
import collections,json,re,sys
from verify_final import ROOT,OUT,variants,select,compact,group,markers,jsonl,readjson,digest,write_tsv

B=ROOT/'work/arcata'
own=jsonl(B/'own_findings.jsonl');meta=jsonl(B/'variants.jsonl')
ops={L:readjson(B/(L+'_build.json')) for L in ['fr','en']}
opening=readjson(B/'opening_and_numbering_operations.json')
raw={};selected={};pages={};vv={};hashes={}
files={'fr':['sga4.5-intro.tex','ariane.tex','sga4.5-1.tex'],'en':['sga4half_intro_en.tex','ariane_en.tex','sga4half_1_en.tex']}
for L in files:
 raw[L]='\n'.join((B/L/f).read_text() for f in files[L]);vv[L]=variants(raw[L]);pages[L]={}
 hashes[L]={f:digest((B/L/f).read_bytes()) for f in files[L]}
 for side in ['printed','corrected']:
  t=select(raw[L],side);selected[L,side]=compact(t);mm=markers(t)
  pages[L,side]={m['page']:t[m['end']:(mm[i+1]['start'] if i+1<len(mm) else len(t))] for i,m in enumerate(mm)}
manual=readjson(OUT/'arcata_own_witnesses.json') if (OUT/'arcata_own_witnesses.json').exists() else {}

def page_list(expr):
 out=[]
 for part in str(expr).replace('–','-').split(','):
  part=part.strip()
  if re.fullmatch(r'\d+-\d+',part):a,b=map(int,part.split('-'));out.extend(str(n) for n in range(a,b+1))
  elif part in ['III','IV'] or part.isdigit():out.append(part)
 return out
def scope(L,side,expr):
 pp=page_list(expr)
 return compact('\n'.join(pages[L,side].get(p,'') for p in pp)) if pp else selected[L,side]
def both_contains(L,page,terms):
 checks=[]
 for side in ['printed','corrected']:
  t=scope(L,side,page)
  for term in terms:checks.append(dict(form=side,page=str(page),witness=term,present=compact(term) in t))
 return all(x['present'] for x in checks),checks
def manual_check(r,L):
 w=manual.get(r['id'],{}).get(L)
 if not w:return None
 checks=[]
 for ww in [w]+w.get('additional_checks',[]):
  page=ww.get('page',r['page'])
  for side in ['printed','corrected']:
   t=scope(L,side,page)
   for q in ww.get('contains',[]):checks.append(dict(form=side,page=page,witness=q,test='present',ok=compact(q) in t))
   for q in ww.get('absent',[]):checks.append(dict(form=side,page=page,witness=q,test='absent',ok=compact(q) not in t))
   for q in ww.get('regex',[]):checks.append(dict(form=side,page=page,witness=q,test='regex',ok=bool(re.search(q,t))))
 for src in w.get('absent_variant_sources',[]):checks.append(dict(source=src,test='no variant',ok=not any(src in v['source'].split(';') for v in vv[L])))
 return bool(checks) and all(c['ok'] for c in checks),dict(reason=w.get('reason','Reviewed literal source witness'),checks=checks)
def operation_check(r,L,aliases=None):
 ids={r['id']}|set(aliases or [])
 matches=[x for x in ops[L] if ids.intersection(x.get('id','').split(';'))]
 if not matches:return None
 checks=[]
 for op in matches:
  after=op.get('after','');before=op.get('before','')
  for side in ['printed','corrected']:
   target=compact(select(after,side));previous=compact(select(before,side))
   n=selected[L,side].count(target) if target else 0
   expected=int(op.get('count',op.get('occurrences',1)))
   # Complete passages can contain later corrections and page markers; reviewed
   # special cases are handled independently rather than accepted by this test.
   ok=bool(target) and n>=expected
   checks.append(dict(source_operation=op['id'],page=str(op.get('page','')),form=side,witness=target,minimum_occurrences=expected,actual_occurrences=n,ok=ok))
   if r['id'].startswith('S45-ASTRA-E-') and previous and previous not in target:
    residual=scope(L,side,op.get('page',r['page'])).count(previous)
    checks.append(dict(source_operation=op['id'],page=str(op.get('page','')),form=side,witness=previous,test='old English reading absent from affected pages',residual_occurrences=residual,ok=residual==0))
 return all(c['ok'] for c in checks),checks
def variant_check(r,L):
 mm=[m for m in meta if r['id'] in {m.get('id',''),m.get('source','')}|set(m.get('sources',[]))]
 if not mm:return None
 checks=[]
 for m in mm:
  ids={m.get('id',''),m.get('source','')}|set(m.get('sources',[]));ids.discard('')
  found=[v for v in vv[L] if ids.intersection(v['source'].split(';'))]
  if L=='en' and m.get('en_printed')==m.get('en_corrected')=='':
   checks.append(dict(source=m['id'],no_english_variant=True,reason=m.get('english_applicability','French spelling/agreement change does not change the English wording.'),ok=not found))
  else:
   checks.append(dict(source=m['id'],occurrences=len(found),readings=[dict(printed=v['printed'],corrected=v['corrected']) for v in found],ok=bool(found) and all(compact(v['printed'])!=compact(v['corrected']) for v in found)))
 return all(c['ok'] for c in checks),checks

rows=[]
for r in own:
 for L in ['fr','en']:
  ident=r['id'];result=None;classification=''
  # Exact manual checks take precedence and are never silently ignored on failure.
  result=manual_check(r,L)
  if result is not None:classification='reviewed page-scoped literal witness'
  elif ident.startswith('S45-ASTRA-E-') and L=='fr':
   result=(True,dict(reason=r['reason'],decision=r['change'],scope='This record identifies a discrepancy in the supplied English; it does not prescribe an additional French change.'))
   classification='French unchanged by an English-only finding'
  elif (result:=variant_check(r,L)) is not None:classification='actual source variant or explicit English non-applicability'
  elif ident=='S45-ASTRA-A-0028':
   original=(B/'arcata_bibliography.tex').read_text()
   if L=='en':original=original.replace('Bibliographie','Bibliography')
   checks=[]
   for side in ['printed','corrected']:
    target=compact(select(original,side));body=re.sub(r'\\(?:PrintPage|MathPage)\{[^}]*\}','',selected[L,side]);body=compact(body)
    checks.append(dict(form=side,whole_bibliography_present=target in body,numbered_items=len(re.findall(r'\\item\[\{\[[0-9]+\]\}\]',target))))
   result=(all(x['whole_bibliography_present'] and x['numbered_items']==16 for x in checks),checks);classification='complete sixteen-entry bibliography against restoration source'
  elif ident=='S45-ASTRA-A-0032':
   source=ROOT/'work/common'/('general_contents_'+L+'.tex');body=ROOT/'work/build'/('prepared_body_'+L+'.tex')
   if source.exists() and body.exists():
    target=compact(source.read_text());ok=target in compact(body.read_text())
    result=(ok,dict(source=source.relative_to(ROOT).as_posix(),sha256=digest(source.read_bytes()),complete_contents_present=ok));classification='complete original general contents included in prepared body'
  elif ident=='S45-ASTRA-A-0001':
   if L=='fr':result=both_contains(L,'IV',['étaient devenues'])
   else:result=both_contains(L,'IV',['had become'])
   classification='restored damaged French verb and existing English meaning'
  elif ident=='S45-ASTRA-A-0004':
   result=both_contains(L,'4',['Inputs of etale cohomology']);classification='original quoted lecture title preserved'
  elif ident=='S45-ASTRA-A-0010' and L=='en':
   result=both_contains(L,'27',[r'K\"unneth']);classification='existing English spelling agrees with the print'
  elif ident=='S45-ASTRA-A-0026':
   result=both_contains(L,'70',[r'\tag{2.3.1}',r'\tag{2.3.2}']);classification='printed local equation numbers retained'
  else:
   aliases=[]
   if ident=='S45-ASTRA-A-0005' and L=='en':aliases=['S45-ASTRA-E-0001']
   if ident=='S45-ASTRA-A-0006':aliases=['S45-SOL-0054']
   result=operation_check(r,L,aliases)
   if result is not None:classification='explicit operation targets survive in both selected forms'
  if result is None:ok=False;evidence='No mechanically checked variant, operation, restoration, or reviewed literal witness supplied.'
  else:ok,evidence=result
  rows.append(dict(source_id=ident,id=ident,printed_page=str(r['page']),language=L,status='covered' if ok else 'unresolved',classification=classification,evidence=evidence,decision=r['change'],reason=r['reason']))

OUT.mkdir(parents=True,exist_ok=True)
(OUT/'arcata_own_fix_coverage.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
write_tsv(OUT/'arcata_own_fix_coverage.tsv',rows,['source_id','printed_page','language','status','classification','evidence','decision','reason'])
unresolved=[r['source_id']+':'+r['language'] for r in rows if r['status']!='covered']
summary=dict(own_ids=len(own),language_checks=len(rows),covered=len(rows)-len(unresolved),unresolved=unresolved,input_hashes=hashes)
(OUT/'ARCATA_OWN_COVERAGE_STATUS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='input_hashes'},ensure_ascii=False))
sys.exit(bool(unresolved))
