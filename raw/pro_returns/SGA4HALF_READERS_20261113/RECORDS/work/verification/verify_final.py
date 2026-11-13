# Invoke this script with python3.
"""Independent structural, coverage, compilation, and privacy gate.

Run from any directory. The default preliminary report records unavailable
outputs as pending. --strict exits nonzero if any failure or pending check
remains. This script does not build or change the readers. It deliberately
does not import the assembly's TeX parser or use its asserted counts as proof.
"""
from pathlib import Path
import argparse,bisect,collections,csv,hashlib,json,re,sys,time

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
ORDER=['III','IV']+[str(i) for i in range(1,313)]
EXPECTED={'fr':312,'en':218}
FILES={
 'fr':[(0,0,'SGA4HALF_FR_diplomatique'),(1,0,'SGA4HALF_FR_corrige_apparat'),(2,0,'SGA4HALF_FR_texte_de_lecture'),(1,1,'SGA4HALF_FR_annotated_master')],
 'en':[(0,0,'SGA4HALF_EN_diplomatic'),(1,0,'SGA4HALF_EN_corrected_apparatus'),(2,0,'SGA4HALF_EN_reading'),(1,1,'SGA4HALF_EN_annotated_master')],
}
LOCAL_PATH=re.compile(r'(?<![\w:])/(?:workspace|home|root|mnt|tmp|private|Users|usr|var|etc|opt|Applications|Volumes|Library|srv|run|media)(?:/[^\s<>"\]\[{}]*)?(?![\w])|(?<![\w:])[A-Za-z]:/[^\s<>"\]\[{}]+|(?<![\w:])[A-Za-z]:(?:\\)+(?:Users|Documents and Settings|Windows|Program Files|ProgramData|Temp|tmp|workspace|home|projects?|build|work)(?:\\)+[^\s<>"\]\[{}]+',re.I)
EMAIL=re.compile(r'[A-Za-z0-9_.+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
CHECKS=[];VARIANTS=[];MARKERS=[];READERS=[];COVERAGE=[];PRIVACY=[];PDF_CHECKED_HASHES=set()

def relative(p):
 try:return Path(p).resolve().relative_to(ROOT).as_posix()
 except ValueError:return Path(p).name
def digest(x):return hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest()
def clean(s):return EMAIL.sub('[address omitted]',LOCAL_PATH.sub('[local path omitted]',str(s)))
def safe_value(x):
 if isinstance(x,str):return clean(x)
 if isinstance(x,list):return [safe_value(v) for v in x]
 if isinstance(x,dict):return {k:safe_value(v) for k,v in x.items()}
 return x
def check(scope,name,ok=None,expected='',actual='',detail='',pending=False):
 status='pending' if pending else ('pass' if ok else 'fail')
 r=dict(scope=scope,check=name,status=status,expected=expected,actual=actual,detail=detail)
 CHECKS.append(safe_value(r));return status=='pass'
def need(path,scope):
 if not path.exists():check(scope,'required input available',pending=True,expected=relative(path),actual='missing');return False
 return True
def readjson(p):return json.loads(p.read_text())
def readtsv(p):
 with p.open(newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def jsonl(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def write_tsv(path,rows,fields):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore');w.writeheader()
  for r in rows:
   w.writerow({k:clean(json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v) for k,v in r.items()})

def without_comments(s):
 """Blank comments without changing offsets, accounting for escaped percent."""
 out=list(s);i=0
 while i<len(s):
  if s[i]=='\\' and i+1<len(s):i+=2;continue
  if s[i]=='%':
   e=s.find('\n',i)
   if e<0:e=len(s)
   out[i:e]=' '*(e-i);i=e
  else:i+=1
 return ''.join(out)
def group(s,pos):
 while pos<len(s) and s[pos].isspace():pos+=1
 if pos==len(s) or s[pos]!='{':raise ValueError('expected a braced argument')
 start=pos+1;level=1;pos+=1
 while pos<len(s):
  c=s[pos]
  if c=='\\' and pos+1<len(s) and not s[pos+1].isalpha():pos+=2;continue
  if c=='{':level+=1
  elif c=='}':
   level-=1
   if not level:return s[start:pos],pos+1
  pos+=1
 raise ValueError('unclosed braced argument')
def variants(s):
 t=without_comments(s);rows=[]
 for m in re.finditer(r'\\var(?![A-Za-z@])',t):
  p=m.end()
  while p<len(t) and t[p].isspace():p+=1
  ident=''
  if p<len(t) and t[p]=='[':
   e=t.find(']',p)
   if e<0:raise ValueError('unclosed variant occurrence option')
   ident=t[p+1:e];p=e+1
   while p<len(t) and t[p].isspace():p+=1
  if p==len(t) or t[p]!='{':continue
  a,p=group(t,p);b,p=group(t,p);source,p=group(t,p)
  rows.append(dict(occurrence=ident,start=m.start(),end=p,line=t.count('\n',0,m.start())+1,printed=a,corrected=b,source=source))
 if any(b['start']<a['end'] for a,b in zip(rows,rows[1:])):raise ValueError('nested variant nodes')
 return rows
def select(s,side='corrected'):
 for r in reversed(variants(s)):s=s[:r['start']]+r[side]+s[r['end']:]
 return s
def compact(s):return re.sub(r'\s+',' ',without_comments(s)).strip()
def source_reading(s):
 """Undo display-only citation wrappers while retaining their original keys."""
 pos=0
 while (m:=re.search(r'\\PrintCite\s*\{',s[pos:])):
  a=pos+m.start();_,e=group(s,pos+m.end()-1);key,e=group(s,e)
  s=s[:a]+key+s[e:];pos=a+len(key)
 return compact(s)
def markers(s):
 return [dict(page=m[1],start=m.start(),end=m.end(),line=s.count('\n',0,m.start())+1)
         for m in re.finditer(r'\\(?:PrintPage|MathPage)\{(III|IV|[0-9]+)\}',without_comments(s))]
def normalized_modes(s):
 values={}
 edits=[]
 for name in ['EditionMode','EditionIsMaster']:
  ms=list(re.finditer(r'\\providecommand\s*(?:\\'+name+r'|\{\\'+name+r'\})\s*\{([012])\}',s))
  if len(ms)!=1:raise ValueError(name+' must have exactly one literal definition')
  m=ms[0];values[name]=int(m[1]);edits.append((m.start(1),m.end(1),'@'+name+'@'))
 for a,b,v in sorted(edits,reverse=True):s=s[:a]+v+s[b:]
 return s,values

def load_records():
 reg={};base=ROOT/'work/records'
 for name in ['SOL_FINDINGS_DECIDED.tsv','CHECK_FINDINGS.tsv','MISPRINTS_45.tsv','PAGES_CHECKED.tsv','DECISIONS.tsv']:
  p=base/name
  if need(p,'records'):reg[name]=readtsv(p)
 sol=reg.get('SOL_FINDINGS_DECIDED.tsv',[]);own=reg.get('CHECK_FINDINGS.tsv',[]);pg=reg.get('PAGES_CHECKED.tsv',[])
 required={f'S45-SOL-{i:04d}' for i in range(1,1248)}
 check('records','all Sol identities once',len(sol)==1247 and {r['id'] for r in sol}==required,1247,len(sol))
 check('records','every Sol verdict and evidence complete',all(r.get('verdict') in ['accepted','accepted with a corrected reading','rejected'] and all(r.get(k) for k in ['reason','image','region','printed_reading']) for r in sol),actual=len(sol))
 check('records','own-finding identities unique',len(own)==len({r['id'] for r in own}),len(own),len({r['id'] for r in own}))
 check('records','own-finding decisions complete',all(all(r.get(k) for k in ['id','page','place','change','kind','reason']) for r in own),actual=len(own))
 check('records','page table in original order',[r['printed_page'] for r in pg]==ORDER,314,len(pg))
 check('records','all page scan checks affirmative',all(r.get('checked_against_scan','').lower()=='true' and r.get('reason') and r.get('start_fr') and r.get('start_en') for r in pg),actual=len(pg))
 badmap=[]
 for r in pg:
  p=r['printed_page'];expected={'III':3,'IV':4}.get(p)
  if expected is None:expected=int(p)+(5 if int(p)<=109 else 39)
  if str(expected)!=r['pdf_page']:badmap.append(p)
 check('records','scan PDF-page mapping exact',not badmap,actual=badmap)
 for r in pg:
  try:ok=int(r['sol_findings'])+int(r['own_findings'])==int(r['number_of_findings'])
  except (KeyError,ValueError):ok=False
  if not ok:check('records','page findings subtotal '+r['printed_page'],False)
 ids={r['id']:r for r in sol+own}
 p=ROOT/'source/fr/codex_records/dec.csv'
 if need(p,'source registry'):
  with p.open(newline='') as f:
   for r in csv.DictReader(f):ids.setdefault(r['id'],r)
 # Historical aliases are required to be explicitly declared in DECISIONS.tsv.
 for r in reg.get('DECISIONS.tsv',[]):
  if r.get('kind')=='Duplicate historical identifier':
   for ident in re.findall(r'SGA45-[A-Z]+-[0-9]{4}[A-Z]',r.get('decision','')):ids.setdefault(ident,r)
 meta=[]
 for owner in ['arcata','rapport_cycle','sommes','finitude_verdier']:
  p=ROOT/'work'/owner/'variants.jsonl'
  if need(p,'variant metadata'):meta.extend(jsonl(p))
 metadata=collections.defaultdict(list)
 for r in meta:
  for ident in set([r.get('id',''),r.get('source','')]+r.get('sources',[])):
   if ident:metadata[ident].append(r)
 return reg,ids,metadata

def inspect_tex(reg,ids,metadata):
 reports={};canonical={};component_occurrences={}
 page_table={r['printed_page']:r for r in reg.get('PAGES_CHECKED.tsv',[])}
 op=ROOT/'work/records/VARIANT_OCCURRENCES.json'
 if need(op,'records'): 
  for lang in FILES:component_occurrences[lang]=[r for r in readjson(op) if r['language']==lang]
 for lang,specs in FILES.items():
  p=ROOT/'work/build'/('prepare_report_'+lang+'.json')
  if not need(p,lang):continue
  report=readjson(p);entries=report['entries'];reports[lang]=entries
  blocking=[d for d in report.get('diagnostics',[]) if d.get('kind') not in {'bookmark_math_alternative'}]
  check(lang,'preparation has no blocking diagnostics',not blocking and not report.get('unresolved_citations'),actual={'blocking_diagnostics':blocking,'informational_diagnostics':report.get('diagnostics'),'unresolved_citations':report.get('unresolved_citations')})
  wanted=[lang.upper()+f'-{i:04d}' for i in range(1,EXPECTED[lang]+1)]
  check(lang,'prepared occurrence identities', [r['occurrence'] for r in entries]==wanted,EXPECTED[lang],len(entries))
  report_byid={r['occurrence']:r for r in entries}
  for mode,master,name in specs:
   scope=name;p=ROOT/'deliverables'/lang.upper()/(name+'.tex')
   item=dict(reader=name,language=lang,mode=mode,master=bool(master),tex=relative(p))
   READERS.append(item)
   if not need(p,scope):continue
   s=p.read_text();item['tex_sha256']=digest(p.read_bytes())
   try:norm,values=normalized_modes(s)
   except ValueError as e:check(scope,'mode definitions parsed',False,detail=str(e));continue
   item['normalized_tex_sha256']=digest(norm)
   check(scope,'requested mode and master switches',values==dict(EditionMode=mode,EditionIsMaster=master),dict(EditionMode=mode,EditionIsMaster=master),values)
   if lang not in canonical:canonical[lang]=norm
   check(scope,'identical master apart from two switches',norm==canonical[lang],digest(canonical[lang]),digest(norm))
   for kind in ['prepared_body','apparatus']:
    prepared=ROOT/'work/build'/(kind+'_'+lang+'.tex')
    if need(prepared,scope):check(scope,'complete '+kind+' included verbatim',prepared.read_text() in s,detail=relative(prepared))
   check(scope,'flattened TeX has no input/include commands',not re.search(r'\\(?:input|include)\s*\{',without_comments(s)))
   pp=markers(s);seq=[r['page'] for r in pp]
   check(scope,'314 original-page markers in order',seq==ORDER,314,len(seq))
   item['tex_page_markers']=len(pp)
   if master:
    badlocations=[]
    for marker in pp:
     r=page_table.get(marker['page'],{})
     if r.get('master_'+lang)!=p.name or str(marker['line'])!=r.get('master_line_'+lang) or s[marker['end']:marker['end']+240].strip()!=r.get('master_marker_context_'+lang):badlocations.append(marker['page'])
    check(scope,'page-table master lines and contexts match actual markers',not badlocations,314,{'checked':len(pp),'mismatches':badlocations})
   try:vv=variants(s)
   except ValueError as e:check(scope,'balanced variant parsing',False,detail=str(e));continue
   check(scope,'variant identities unique and complete',[v['occurrence'] for v in vv]==wanted,EXPECTED[lang],len(vv))
   aa=re.findall(r'\\hypertarget\{apparatus:((?:FR|EN)-[0-9]+)\}\{([0-9]+)\}',without_comments(s))
   check(scope,'one TeX apparatus entry per occurrence',[a for a,n in aa]==wanted and all(int(n)==i for i,(a,n) in enumerate(aa,1)),EXPECTED[lang],len(aa))
   item['tex_variants']=len(vv);item['tex_apparatus_entries']=len(aa)
   mismatches=[];identical=[];invalid=[];unregistered=[]
   for v in vv:
    ident=v['occurrence'];r=report_byid.get(ident,{})
    match=all(v[k]==r.get(k) for k in ['printed','corrected','source'])
    if not match:mismatches.append(ident)
    if compact(v['printed'])==compact(v['corrected']):identical.append(ident)
    srcs=[x.strip() for x in v['source'].split(';') if x.strip()]
    valid=bool(srcs) and all(x in ids and ids[x].get('verdict')!='rejected' for x in srcs)
    mm=[m for x in srcs for m in metadata.get(x,[])]
    hasmeta=any(m.get('reason') for m in mm)
    if not valid:invalid.append(dict(occurrence=ident,source=v['source']))
    if not hasmeta:unregistered.append(dict(occurrence=ident,source=v['source']))
    if mode==1 and master==1:
     VARIANTS.append(dict(language=lang,occurrence=ident,page=r.get('page',''),source=v['source'],line=v['line'],matches_prepare_report=match,distinct_readings=compact(v['printed'])!=compact(v['corrected']),valid_decision=valid,valid_metadata=hasmeta,printed_sha256=digest(v['printed']),corrected_sha256=digest(v['corrected'])))
   check(scope,'variant readings match prepare report',not mismatches,actual=mismatches)
   check(scope,'no identical variant readings',not identical,actual=identical)
   check(scope,'every variant has a valid decision',not invalid,actual=invalid)
   check(scope,'every variant has reasoned source metadata',not unregistered,actual=unregistered)
   for r in pp:MARKERS.append(dict(reader=name,language=lang,printed_page=r['page'],tex_line=r['line'],pdf_page='',pdf_x='',pdf_y=''))
  raw=component_occurrences.get(lang,[])
  bad=[]
  if len(raw)!=len(entries):bad.append('count')
  for a,b in zip(raw,entries):
   if a['source']!=b['source'] or a['page']!=b['page'] or any(source_reading(a[k])!=source_reading(b[k]) for k in ['printed','corrected']):bad.append(b['occurrence'])
  check(lang,'assembled variants reconcile with component inventory',not bad,len(entries),{'component_count':len(raw),'mismatches':bad})
 if 'fr' in reports:
  ms=reg.get('MISPRINTS_45.tsv',[]);es=reports['fr'];bad=[]
  if len(ms)!=len(es):bad.append('count')
  for a,b in zip(ms,es):
   if a['source']!=b['source'] or a['printed_page']!=b['page'] or source_reading(a['printed_reading'])!=source_reading(b['printed']) or source_reading(a['correction'])!=source_reading(b['corrected']) or not a.get('reason'):bad.append(b['occurrence'])
  check('records','misprint register matches every French occurrence',not bad,EXPECTED['fr'],{'rows':len(ms),'mismatches':bad})
 return reports

def inspect_pdf_and_builds():
 try:import fitz
 except ImportError:
  check('PDF','PyMuPDF available for independent name-tree inspection',pending=True);return
 for item in READERS:
  name=item['reader'];lang=item['language'];pdf=ROOT/'deliverables'/lang.upper()/(name+'.pdf');tex=pdf.with_suffix('.tex')
  cfile=ROOT/'work/build'/(name+'.compile.json');scope=name
  if not need(pdf,scope) or not need(cfile,scope) or not tex.exists():continue
  item['pdf']=relative(pdf);item['pdf_sha256']=digest(pdf.read_bytes())
  try:record=readjson(cfile)
  except json.JSONDecodeError:
   check(scope,'compile record complete',pending=True,detail='The compilation record is being written.');continue
  final=record.get('final',{});th=record.get('tex_sha256',final.get('tex_sha256'));ph=record.get('pdf_sha256',final.get('pdf_sha256'))
  if th and ph:
   fresh=th==digest(tex.read_bytes()) and ph==item['pdf_sha256'];item['freshness_method']='compile-time SHA-256'
  else:
   fresh=pdf.stat().st_mtime_ns>=tex.stat().st_mtime_ns and cfile.stat().st_mtime_ns>=tex.stat().st_mtime_ns;item['freshness_method']='file modification times'
  if not fresh:
   check(scope,'PDF build is current and complete',pending=True,detail='Current TeX/PDF does not match the last completed compilation record; PDF may be stale or a build is running.');continue
  check(scope,'PDF build is current and complete',True,detail=item['freshness_method'])
  try:
   doc=fitz.open(pdf);names=doc.resolve_names();item['pdf_pages']=len(doc)
   pp={k:v for k,v in names.items() if k.startswith('printpage:')}
   aa={k:v for k,v in names.items() if k.startswith('apparatus:')}
   expectedpp={'printpage:'+lang+':'+p for p in ORDER}
   expectedaa={'apparatus:'+lang.upper()+f'-{i:04d}' for i in range(1,EXPECTED[lang]+1)} if item['mode']==1 else set()
   item['pdf_printpage_destinations']=len(pp);item['pdf_apparatus_destinations']=len(aa)
   check(scope,'PDF has exactly 314 expected print-page destinations',set(pp)==expectedpp,314,{'count':len(pp),'missing':sorted(expectedpp-set(pp)),'extra':sorted(set(pp)-expectedpp)})
   check(scope,'PDF apparatus destinations match selected mode',set(aa)==expectedaa,len(expectedaa),{'count':len(aa),'missing':sorted(expectedaa-set(aa)),'extra':sorted(set(aa)-expectedaa)})
   bad=[k for k,v in {**pp,**aa}.items() if not isinstance(v.get('page'),int) or not 0<=v['page']<len(doc)]
   check(scope,'all edition destinations point to existing PDF pages',not bad,actual=bad)
   mapped=[pp['printpage:'+lang+':'+p]['page'] for p in ORDER if 'printpage:'+lang+':'+p in pp]
   check(scope,'original-page destination pages are nondecreasing',all(a<=b for a,b in zip(mapped,mapped[1:])))
   for row in MARKERS:
    if row['reader']==name:
     d=pp.get('printpage:'+lang+':'+row['printed_page'],{});xy=d.get('to',('',''))
     row.update(pdf_page=d.get('page',-1)+1,pdf_x=xy[0],pdf_y=xy[1])
   missing_links=[];double_questions=[];replacement_chars=0
   for n,page in enumerate(doc,1):
    txt=page.get_text();privacy_text(relative(pdf),txt,pdf_page=n)
    if '??' in txt:double_questions.append(n)
    replacement_chars+=txt.count('\ufffd')
    for link in page.get_links():
     if link.get('kind')==fitz.LINK_GOTO and link.get('page',-1)<0:missing_links.append(n)
   privacy_text(relative(pdf)+' [metadata]',json.dumps(doc.metadata,ensure_ascii=False))
   PDF_CHECKED_HASHES.add(item['pdf_sha256'])
   check(scope,'PDF contains no unresolved double-question references',not double_questions,actual=double_questions)
   check(scope,'PDF internal links have destinations',not missing_links,actual=missing_links)
   item['pdf_text_replacement_characters']=replacement_chars
   item['pdf_font_count']=len({f[0] for p in doc for f in p.get_fonts()})
   doc.close()
  except Exception as e:check(scope,'PDF opens and resolves name tree',False,detail=clean(e));continue
  item['final_compile_pass']=final.get('pass_number')
  check(scope,'final compile exit and error list clear',final.get('exit_code')==0 and not final.get('errors') and final.get('pdf_exists') is True,0,{'exit_code':final.get('exit_code'),'errors':final.get('errors'),'pdf_exists':final.get('pdf_exists')})
  if th and ph:
   check(scope,'compiled TeX and PDF hashes match current artifacts',th==digest(tex.read_bytes()) and ph==digest(pdf.read_bytes()),actual={'tex_matches':th==digest(tex.read_bytes()),'pdf_matches':ph==digest(pdf.read_bytes())})
   item['freshness_method']='compile-time SHA-256'
  else:
   fresh=pdf.stat().st_mtime_ns>=tex.stat().st_mtime_ns and cfile.stat().st_mtime_ns>=tex.stat().st_mtime_ns
   check(scope,'PDF and compile record are newer than TeX',fresh,detail='Timestamp fallback: compile record has no source/PDF hashes.')
   item['freshness_method']='file modification times'
  n=final.get('pass_number');log=ROOT/'work/build'/(name+f'.pass{n}.log.txt')
  if not need(log,scope):continue
  text=log.read_text(errors='replace');item['final_log']=relative(log)
  errors=re.findall(r'^! .*|^(?:\./)?'+re.escape(name)+r'\.tex:[0-9]+:.*',text,re.M)
  missing=re.findall(r'^.*(?:Missing character:|Font[^\n]*not loadable|font[^\n]*not found).*(?:\n[^\n]*)?',text,re.M)
  unresolved=re.findall(r'^.*(?:There were undefined references|(?:Reference|Citation) [^\n]*undefined|undefined citations|multiply-defined labels|destination with the same identifier).*(?:\n[^\n]*)?',text,re.M|re.I)
  rerun=re.findall(r'^.*(?:Label\(s\) may have changed|Rerun to get (?:cross-references|outlines) right).*(?:\n[^\n]*)?',text,re.M|re.I)
  check(scope,'independent final-log error scan clear',not errors,actual=errors)
  check(scope,'no missing glyphs or unavailable fonts',not missing,actual=missing)
  check(scope,'no unresolved references or duplicate destinations',not unresolved,actual=unresolved)
  check(scope,'final cross-reference state stable',not rerun,actual=rerun)
  item['overfull_boxes']=len(re.findall(r'Overfull \\[hv]box',text));item['underfull_boxes']=len(re.findall(r'Underfull \\[hv]box',text))
  item['compile_warning_count']=len(final.get('warnings',[]))

def coverage_row(owner,source_id,language,page,status,evidence,origin,classification=''):
 COVERAGE.append(dict(owner=owner,source_id=source_id,language=language,printed_page=str(page),status=status,classification=classification,evidence=evidence,evidence_file=relative(origin)))
def load_coverage(reg):
 # Preserve each owner's explicit evidence and classify aggregate checks as such.
 for owner,filename in [('arcata','ACCEPTED_FIX_COVERAGE.tsv'),('sommes','accepted_fix_coverage.tsv')]:
  p=ROOT/'work'/owner/filename
  if need(p,'coverage '+owner):
   for r in readtsv(p):
    for lang in ['fr','en']:
     status=r.get(lang+'_status','');evidence=r.get(lang+'_evidence','')
     if r.get('verdict')=='rejected' and not evidence:evidence=r.get('reason') or r.get('evidence','')
     ok=bool(status and evidence) and not re.search(r'^(?:pending|unresolved|failed)',status,re.I)
     coverage_row(owner,r['id'],lang,r['page'],'covered' if ok else 'unresolved',evidence,p,status)
 p=ROOT/'work/rapport_cycle/records/accepted_fix_coverage.tsv'
 if need(p,'coverage rapport_cycle'):
  for r in readtsv(p):
   status=r.get('status','');w=r.get('witness','');ok=bool(status and w) and not re.search(r'^(?:pending|unresolved|failed)',status,re.I)
   coverage_row('rapport_cycle',r['id'],r['language'],r['page'],'covered' if ok else 'unresolved',w,p,status)
 p=ROOT/'work/sommes/own_fix_coverage.json'
 if need(p,'coverage sommes own'):
  for r in readjson(p):
   for lang in ['fr','en']:coverage_row('sommes',r['id'],lang,r['page'],'covered' if r.get('status')=='verified' and r.get('evidence') else 'unresolved',r.get('evidence',''),p,'Owner combined-language implementation check')
 p=ROOT/'work/finitude_verdier/accepted_fix_coverage.json'
 if need(p,'coverage finitude_verdier'):
  for r in readjson(p):coverage_row('finitude_verdier',r.get('source_id',r.get('id')),r['language'].lower(),r.get('printed_page',r.get('page','')),r['status'],r.get('evidence',''),p,r.get('classification',''))
 p=OUT/'arcata_own_fix_coverage.json'
 if need(p,'coverage arcata own'):
  for r in readjson(p):coverage_row('arcata',r.get('source_id',r.get('id')),r['language'],r.get('printed_page',r.get('page','')),r['status'],r.get('evidence',''),p,r.get('classification',''))
  status=OUT/'ARCATA_OWN_COVERAGE_STATUS.json'
  if need(status,'coverage arcata own'):
   d=readjson(status);stale=[]
   for lang,files in d.get('input_hashes',{}).items():
    for f,h in files.items():
     q=ROOT/'work/arcata'/lang/f
     if not q.exists() or digest(q.read_bytes())!=h:stale.append(relative(q))
   check('coverage arcata own','checked source hashes still current',not stale,actual=stale)
 # The glossary changes are independently recounted against the prepared body.
 p=ROOT/'work/build/GLOSSARY_CHANGES_APPLIED.json';body=ROOT/'work/build/prepared_body_en.tex'
 if need(p,'coverage glossary') and need(body,'coverage glossary'):
  r=readjson(p);t=body.read_text();ok=len(r)==7 and [str(x['page']) for x in r]==['27','27','35','36','40','51','70'] and not re.search(r'\b[Uu]nwindings?\b',t) and len(re.findall(r'\bunwound\b',t))==2
  coverage_row('glossary','S45-ASTRA-G-0001','en','27,35,36,40,51,70','covered' if ok else 'unresolved','Seven logged noun/heading corrections, no residual noun unwinding, and both verbal unwound occurrences retained.',p,'Independent final-body and applied-change-log check')
  coverage_row('glossary','S45-ASTRA-G-0001','fr','27,35,36,40,51,70','covered','The finding changes English terminology only; French is explicitly unchanged in the decision.',p,'French unchanged by this English-only finding')
 targets={r['id'] for r in reg.get('SOL_FINDINGS_DECIDED.tsv',[])+reg.get('CHECK_FINDINGS.tsv',[])}
 keys=collections.Counter((r['source_id'],r['language']) for r in COVERAGE)
 unknown=sorted({i for i,l in keys if i not in targets})
 duplicates=[i+':'+l for (i,l),n in keys.items() if n!=1]
 missing=[i+':'+l for i in sorted(targets) for l in ['fr','en'] if (i,l) not in keys]
 unresolved=[r['source_id']+':'+r['language'] for r in COVERAGE if r['status']!='covered' or not r['evidence']]
 check('coverage','only known source identities',not unknown,actual=unknown)
 check('coverage','one evidence row per source and language',not duplicates,actual=duplicates)
 check('coverage','all Sol and own findings have both-language coverage',not missing,expected=2*len(targets),actual={'rows':len(COVERAGE),'missing':missing},pending=bool(missing))
 check('coverage','all supplied evidence checks resolved',not unresolved,actual=unresolved)

def inspect_glossary_freshness():
 p=ROOT/'work/glossary/STATUS.json'
 if not need(p,'glossary'):return
 status=readjson(p);stale=[];newer_than_body=[]
 for r in status.get('input_hashes',[]):
  q=ROOT/r['path']
  if not q.exists() or digest(q.read_bytes())!=r['sha256']:stale.append(r['path'])
  lang='fr' if '/fr/' in r['path'] else 'en'
  prepared=ROOT/'work/build'/('prepared_body_'+lang+'.tex')
  if q.exists() and prepared.exists() and q.stat().st_mtime_ns>prepared.stat().st_mtime_ns:newer_than_body.append(r['path'])
 check('glossary','all counted source hashes current',len(status.get('input_hashes',[]))==22 and not stale,22,{'inputs':len(status.get('input_hashes',[])),'stale':stale})
 check('assembly','prepared bodies are newer than component inputs',not newer_than_body,actual=newer_than_body)

def privacy_text(file,text,pdf_page=''):
 for kind,rx in [('absolute local path',LOCAL_PATH),('email address',EMAIL)]:
  for m in rx.finditer(text):
   PRIVACY.append(dict(file=file,kind=kind,line=text.count('\n',0,m.start())+1,pdf_page=pdf_page,value_sha256=digest(m[0]),context=clean(text[max(0,m.start()-50):min(len(text),m.end()+50)].replace('\n',' '))))
def inspect_privacy(extra_roots):
 candidates=set();pdfs=set()
 for folder in [ROOT/'deliverables',ROOT/'work/records',ROOT/'work/glossary',ROOT/'work/build']+[ROOT/p for p in extra_roots]:
  if not folder.exists():continue
  if folder.is_file():
   (pdfs if folder.suffix.lower()=='.pdf' else candidates).add(folder);continue
  for p in folder.rglob('*'):
   if not p.is_file() or '__pycache__' in p.parts:continue
   # Raw TeX runtime logs, aux/out files, and intermediate images are excluded.
   if p.suffix.lower()=='.pdf':pdfs.add(p)
   elif p.suffix.lower() in ['.tex','.sty','.bib','.py','.sh','.tsv','.csv','.json','.jsonl','.md','.diff','.txt']:candidates.add(p)
 for p in sorted(candidates):privacy_text(relative(p),p.read_text(errors='replace'))
 for p in sorted(pdfs):
  h=digest(p.read_bytes())
  if h in PDF_CHECKED_HASHES:continue
  try:
   import fitz
   with fitz.open(p) as doc:
    for n,page in enumerate(doc,1):privacy_text(relative(p),page.get_text(),pdf_page=n)
    privacy_text(relative(p)+' [metadata]',json.dumps(doc.metadata,ensure_ascii=False))
   PDF_CHECKED_HASHES.add(h)
  except Exception as e:check('privacy','additional PDF readable',False,detail=relative(p)+': '+clean(e))
 check('privacy','distributable text/PDF scan has no paths or addresses',not PRIVACY,0,len(PRIVACY),detail='Raw runtime .log/.aux/.out files excluded; sanitized .log.txt files included. Hit values are hashed and redacted in this report.')
 return len(candidates)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--strict',action='store_true');parser.add_argument('--privacy-root',action='append',default=[],help='Additional project-relative staged package tree or text file')
 args=parser.parse_args();OUT.mkdir(parents=True,exist_ok=True)
 started=time.time()
 try:
  reg,ids,meta=load_records();inspect_tex(reg,ids,meta);inspect_pdf_and_builds();load_coverage(reg);inspect_glossary_freshness();privacy_files=inspect_privacy(args.privacy_root)
 except Exception as e:
  check('verifier','unexpected exception',False,detail=type(e).__name__+': '+clean(e));privacy_files=0
 totals=collections.Counter(r['status'] for r in CHECKS)
 result=dict(mode='strict' if args.strict else 'preliminary',result='pass' if not totals['fail'] and not totals['pending'] else ('incomplete' if not totals['fail'] else 'fail'),duration_seconds=round(time.time()-started,2),counts=dict(totals),readers=READERS,coverage_rows=len(COVERAGE),privacy_text_files=privacy_files,privacy_hits=len(PRIVACY),checks=CHECKS)
 (OUT/'FINAL_VERIFICATION.json').write_text(json.dumps(safe_value(result),ensure_ascii=False,indent=2)+'\n')
 write_tsv(OUT/'FINAL_STRUCTURE_CHECKS.tsv',CHECKS,['scope','check','status','expected','actual','detail'])
 write_tsv(OUT/'FINAL_VARIANT_VALIDATION.tsv',VARIANTS,['language','occurrence','page','source','line','matches_prepare_report','distinct_readings','valid_decision','valid_metadata','printed_sha256','corrected_sha256'])
 write_tsv(OUT/'FINAL_PAGE_MARKERS.tsv',MARKERS,['reader','language','printed_page','tex_line','pdf_page','pdf_x','pdf_y'])
 write_tsv(OUT/'FINAL_FIX_COVERAGE.tsv',COVERAGE,['owner','source_id','language','printed_page','status','classification','evidence','evidence_file'])
 write_tsv(OUT/'FINAL_PRIVACY_CHECK.tsv',PRIVACY,['file','kind','line','pdf_page','value_sha256','context'])
 print(json.dumps({k:result[k] for k in ['mode','result','counts','coverage_rows','privacy_text_files','privacy_hits','duration_seconds']},ensure_ascii=False))
 for r in CHECKS:
  if r['status']!='pass':print(r['status'].upper()+': '+r['scope']+' / '+r['check']+' / '+clean(str(r['actual']))[:1200])
 return 1 if args.strict and (totals['fail'] or totals['pending']) else 0

if __name__=='__main__':sys.exit(main())
