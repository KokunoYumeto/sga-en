from pathlib import Path
import csv,json,re,difflib,sys
OUT=Path(__file__).resolve().parent
SRC=OUT.parents[1]/'source'
def readj(name):
 p=OUT/name
 return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []
DEC=readj('decisions.jsonl');VAR=readj('variants.jsonl');EXTRA=readj('patches.jsonl');PG=readj('pages.jsonl')
SOL={r['id']:r for r in csv.DictReader((SRC/'check/SOL_FINDINGS.tsv').open(),delimiter='\t')}
PAGES=json.loads((SRC/'check/PAGES.json').read_text())
raw={}
for r in SOL.values():
 if r['id'] not in {x['id'] for x in DEC}:continue
 data=json.loads((SRC/'check/sol'/f"{r['batch']}.json").read_text())
 m=[a for a in data if str(a.get('page'))==r['printed_page'] and a.get('where')==r['where'] and a.get('kind')==r['kind']]
 if len(m)==1 and m[0].get('fix'):raw[r['id']]=m[0]['fix']
def comp(n):return 2 if n<=109 else 3 if n<=128 else 4 if n<=153 else 5
def norm(s):return re.sub(r'\s+',' ',s).strip()
def matches(text,old):
 # Treat only source whitespace as flexible; do not rewrite TeX tokens.
 parts=re.split(r'\s+',old.strip());pat=r'\s+'.join(re.escape(p) for p in parts)
 return list(re.finditer(pat,text)) if old.strip() else []
def locate(text,old,page):
 ms=matches(text,old)
 if len(ms)==1:return ms[0]
 if not ms:return None
 # Anchor ambiguous literal occurrences against source page location.
 p=next((p for p in PAGES if p['tome']=='1' and p['label']==str(page)),None)
 target=p['lines'][0] if p else 0
 return min(ms,key=lambda m:abs(text[:m.start()].count('\n')+1-target))
def replace(text,old,new,page,ident,log,multiple=False):
 ms=matches(text,old)
 if not ms:
  log.append(dict(id=ident,page=str(page),status='already present' if matches(text,new) else 'unmatched',before=old,after=new))
  return text
 if multiple:
  p=next(p for p in PAGES if p['tome']=='1' and p['label']==str(page));lo,hi=p['lines']
  ms=[m for m in ms if lo-10<=text[:m.start()].count('\n')+1<=hi+12]
 else:ms=[locate(text,old,page)]
 for m in reversed(ms):text=text[:m.start()]+new+text[m.end():]
 log.append(dict(id=ident,page=str(page),status='applied',occurrences=len(ms),before=old,after=new))
 return text
def build_fr(c):
 text=(SRC/'fr/codex_dip'/f'sga4.5-{c}.tex').read_text();log=[]
 for d in DEC:
  n=int(d['printed_page'])
  if comp(n)!=c or d['verdict']=='rejected' or d['kind'] in ['misprint_in_print','marker']:continue
  if d['id'] in ['S45-SOL-0335','S45-SOL-0344','S45-SOL-0358']:
   log.append(dict(id=d['id'],page=str(n),status='already repaired in Codex base',before=d['fix_old'],after=d['fix_new']));continue
  old,new=d['fix_old'],d['fix_new']
  if d['id'] in raw:
   original=SOL[d['id']]
   if old==original['fix_old']:old=raw[d['id']]['old']
   if new==original['fix_new']:new=raw[d['id']]['new']
  if d['id']=='S45-SOL-0341':
   log.append(dict(id=d['id'],page=str(n),status='already restored; variant 0342 supplies diplomatic reading',before=old,after=new));continue
  text=replace(text,old,new,n,d['id'],log)
 for d in EXTRA:
  n=int(d['page'])
  if comp(n)!=c:continue
  text=replace(text,d['old'],d['new'],n,d['id'],log,multiple=d.get('multiple',False) or d['id'] in ['S45-ASTRA-R-0004','S45-ASTRA-R-0005','S45-ASTRA-R-0008','S45-ASTRA-R-0016','S45-ASTRA-R-0017'])
 for d in VAR:
  n=int(d['page'])
  if comp(n)!=c or d.get('embedded'):continue
  after=d.get('prefix','')+'\\var{'+d['printed']+'}{'+d['corrected']+'}{'+d['id']+'}'+d.get('suffix','')
  text=replace(text,d['old'],after,n,d['id'],log)
 supplement=OUT/f'supplement_fr_{c}.json'
 if supplement.exists():
  for d in json.loads(supplement.read_text()):
   text=replace(text,d['old'],d['new'],d['page'],d['id'],log)
 for p in PG:
  n=int(p['printed_page'])
  if comp(n)!=c:continue
  anchor=p['start_fr'];m=locate(text,anchor,n)
  if m:
   pos=m.start()
   # Put a list marker after its item token to keep LaTeX list syntax valid.
   if text[pos:].startswith('\\item '):pos+=6
   text=text[:pos]+f'\\PrintPage{{{n}}}'+text[pos:]
   p['start_fr_resolved']=anchor;p['fr_marker_present']=True
  else:log.append(dict(page=str(n),status='marker unmatched',before=anchor))
 (OUT/'fr'/f'sga4.5-{c}.tex').write_text(text)
 (OUT/'records'/f'fr_build_{c}.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
 print('FR',c,'entries',len(log),'unmatched',[x for x in log if x['status'] in ['unmatched','marker unmatched']])
def build_en(c):
 text=(SRC/'en/sources/components'/f'sga4half_{c}_en.tex').read_text();log=[]
 changes=json.loads((OUT/f'en_changes_{c}.json').read_text())
 for d in changes:
  old,new=d['old'],d['new'];ms=matches(text,old)
  if len(ms)>1 and not d.get('all'):
   log.append(dict(id=d['id'],page=str(d['page']),status='AMBIGUOUS',matches=len(ms),before=old));continue
  if not ms:
   log.append(dict(id=d['id'],page=str(d['page']),status='already present' if matches(text,new) else 'unmatched',before=old,after=new));continue
  for m in reversed(ms):text=text[:m.start()]+new+text[m.end():]
  log.append(dict(id=d['id'],page=str(d['page']),status='applied',before=old,after=new,occurrences=len(ms),ai_translated=d.get('ai_translated',False)))
 for v in VAR:
  if comp(int(v['page']))!=c or not v.get('en_old'):continue
  old=v['en_old'];new=v.get('en_prefix','')+'\\var{'+v['printed_en']+'}{'+v['corrected_en']+'}{'+v['id']+'}'+v.get('en_suffix','')
  ms=matches(text,old)
  if v.get('en_anchor'):
   anchors=matches(text,v['en_anchor'])
   ms=[m for m in ms if len(anchors)==1 and m.start()>anchors[0].end()][:1]
  if len(ms)!=1:log.append(dict(id=v['id'],page=v['page'],status='variant unmatched' if not ms else 'variant ambiguous',before=old));continue
  m=ms[0];text=text[:m.start()]+new+text[m.end():]
  log.append(dict(id=v['id'],page=v['page'],status='variant applied',before=old,after=new))
 for p in PG:
  if comp(int(p['printed_page']))!=c:continue
  ms=matches(text,p['start_en'])
  if len(ms)!=1:log.append(dict(page=p['printed_page'],status='marker unmatched' if not ms else 'marker ambiguous',before=p['start_en']));continue
  pos=ms[0].start()
  if text[pos:].startswith('\\item '):pos+=6
  text=text[:pos]+f"\\PrintPage{{{p['printed_page']}}}"+text[pos:]
 (OUT/'en'/f'sga4half_{c}_en.tex').write_text(text)
 (OUT/'records'/f'en_build_{c}.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
 print('EN',c,'entries',len(log),'unmatched',[x for x in log if 'unmatched' in x['status'] or 'ambiguous' in x['status'].lower()])
if __name__=='__main__':
 for c in map(int,sys.argv[1:]):
  build_fr(c)
  if (OUT/f'en_changes_{c}.json').exists():build_en(c)
