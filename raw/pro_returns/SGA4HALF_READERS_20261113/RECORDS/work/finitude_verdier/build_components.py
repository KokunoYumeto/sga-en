"""Apply manually reviewed exact replacements and directly observed page boundaries."""
from pathlib import Path
import json,re
W=Path(__file__).parent
ROOT=W.parents[1]
P=[json.loads(s) for s in (W/'pages.jsonl').read_text().splitlines()]
OPS=json.loads((W/'operations.json').read_text())
REPORT=[]

def relax(s):return s.replace(r'\n','\n')
def apply(part,first,last):
 for lang in ['fr','en']:
  src=ROOT/'source'/('fr/codex_dip/sga4.5-'+part+'.tex' if lang=='fr' else 'en/sources/components/sga4half_'+part+'_en.tex')
  text=src.read_text()
  if part=='8':
   anchor=r'\section{Catégories triangulées:' if lang=='fr' else r'\section{Triangulated categories:'
   text=text.replace(anchor,(W/('contents_263_'+lang+'.tex')).read_text()+'\n'+anchor,1)
  pages=[p for p in P if first<=int(p['printed_page'])<=last]
  starts=[];cursor=0
  for p in pages:
   anchor=p['start_'+lang]
   pos=text.find(anchor,cursor)
   if pos<0:raise ValueError((lang,p['printed_page'],'anchor not found',anchor))
   starts.append((p,pos));cursor=pos+len(anchor)
  parts=[]
  for i,(p,start) in enumerate(starts):
   end=starts[i+1][1] if i+1<len(starts) else len(text)
   body=text[start:end]
   for op in OPS:
    if op['lang']!=lang or op['page']!=int(p['printed_page']):continue
    old=op['old'];new=op['new']
    if op['id']=='S45-SOL-1035':
     old=old.replace(r'\item ','');new=new.replace(r'\item ','')
    if old not in body and relax(old) in body:old=relax(old);new=relax(new)
    if op['mode']=='all_scoped':
     n=body.count(old)
     if n==0:REPORT.append(dict(lang=lang,page=p['printed_page'],id=op['id'],status='FAILED',count=n,old=old))
     else:
      body=body.replace(old,new)
      REPORT.append(dict(lang=lang,page=p['printed_page'],id=op['id'],status='applied',count=n,before=old,after=new))
     continue
    # Explicit local selector for the second definition, not paragraph4.1.
    sel=body.index(r'\label{VII:4-2}') if op['id']=='S45-SOL-1047' else 0
    n=body[sel:].count(old)
    if n!=1:
     REPORT.append(dict(lang=lang,page=p['printed_page'],id=op['id'],status='FAILED',count=n,old=old));continue
    pos=body.index(old,sel)
    body=body[:pos]+new+body[pos+len(old):]
    REPORT.append(dict(lang=lang,page=p['printed_page'],id=op['id'],status='applied',before=old,after=new))
   mark='\\MathPage' if p.get('math') else '\\PrintPage'
   parts.append(mark+'{'+p['printed_page']+'}'+body)
  output=text[:starts[0][1]]+''.join(parts)
  if part=='7':output+='\n'+(W/('bibliography_261_'+lang+'.tex')).read_text()
  dest=W/lang/('sga4.5-'+part+'.tex' if lang=='fr' else 'sga4half_'+part+'_en.tex')
  dest.write_text(output)

apply('7',233,261)
apply('8',262,311)
apply('erratum',312,312)
(W/'build_report.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2))
print('Applied',sum(r['status']=='applied' for r in REPORT),'failed',sum(r['status']=='FAILED' for r in REPORT))
for r in REPORT:
 if r['status']=='FAILED':print(r)
