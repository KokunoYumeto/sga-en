from pathlib import Path
import re,json,difflib
B=Path(__file__).parent; S=B.parent.parent/'source'
def readj(n):return [json.loads(x) for x in (B/(n+'.jsonl')).read_text().splitlines()]
def clean(x):
 return x.replace('’',"'")
def norm(x):return re.sub(r'\s+','',clean(x))
def locate(t,pat,start=0):
 # Flexible whitespace but every non-whitespace character remains exact.
 pat=clean(pat)
 pieces=re.split(r'(\s+)',pat)
 rx=''.join(r'\s*' if x.isspace() else re.escape(x) for x in pieces)
 return list(re.finditer(rx,t[start:]))
def loc(t,pat,start=0):
 ms=locate(t,pat,start)
 return [(start+m.start(),start+m.end()) for m in ms]
texts={'fr':(S/'fr/codex_dip/sga4.5-6.tex').read_text(),'en':(S/'en/sources/components/sga4half_6_en.tex').read_text()}
if __name__=='__main__':
 rows=readj('pages')
 out=[]
 for lang,t in texts.items():
  out.append(lang.upper())
  for r in rows:
   p=int(r['printed_page']); a=r['start_'+lang];ms=loc(t,a)
   out.append(f'{p}: {a!r} -> '+str([t[:m[0]].count('\n')+1 for m in ms]))
 (B/'anchor_diagnostics.txt').write_text('\n'.join(out))
 print('\n'.join(out))

def positions(t,pat):
 pat=clean(pat)
 compact=re.sub(r'\s+','',pat)
 rx=r'\s*'.join(re.escape(c) for c in compact)
 if compact and compact[0].isalpha():rx=r'(?<![A-Za-zÀ-ÿ])'+rx
 if compact and compact[-1].isalpha():rx+=r'(?![A-Za-zÀ-ÿ])'
 return list(re.finditer(rx,t))

def scopes(lang):
 t=texts[lang]
 restores=readj('restorations')
 t+='\n'+restores[-1][lang]
 starts=[];cur=0
 for r in readj('pages'):
  ms=loc(t,r['start_'+lang],cur)
  if not ms:raise ValueError((lang,r['printed_page'],r['start_'+lang]))
  a,b=ms[0];starts.append((int(r['printed_page']),a));cur=b
 return t[:starts[0][1]],{p:t[a:(starts[i+1][1] if i+1<len(starts) else len(t))] for i,(p,a) in enumerate(starts)}

def diagnostic():
 out=[];ops=[];states={};pres={}
 for lang in ['fr','en']:pres[lang],states[lang]=scopes(lang)
 # Shared reading changes. English prose is aligned manually after mathematical substitutions.
 for r in readj('decisions'):
  if r['verdict']=='rejected' or r['kind']=='misprint_in_print' or r['id']=='S45-SOL-0837':continue
  old,new=r['fix_old'],r['fix_new'];p=int(r['printed_page'])
  if r['id'] in ['S45-SOL-0694','S45-SOL-0900','S45-SOL-0937']:
   old=old.replace('\\n','\n');new=new.replace('\\n','\n')
  for lang in ['fr','en']:
   body=states[lang][p]
   # Mathematical strings contain no French prose unless the leading part is an explicit TeX command/formula.
   if lang=='en' and not (old.startswith(('\\','$','(', 'E_', '{F','V-0','a_i','x\\','x_','s=s')) and not re.search(r'\b(?:est|de|et|sur|un|en|degré|Pour|ce|le|Pour|dès|comme|les|puis|cas)\b',old)):
    out.append(dict(lang=lang,page=p,id=r['id'],status='prose alignment required',old=old,new=new));continue
   om=positions(body,old);nm=positions(body,new)
   if nm and (not om or old in new):status='already present'
   elif len(om)==1:
    m=om[0];states[lang][p]=body[:m.start()]+new+body[m.end():];status='applied'
   else:status='missing' if not om else 'multiple'
   out.append(dict(lang=lang,page=p,id=r['id'],status=status,old=old,new=new,count=len(om)))
   if status=='applied':ops.append(dict(lang=lang,page=p,id=r['id'],old=old,new=new))
 # Unit-group symbol repair (superscript only).
 for r in readj('notation_units'):
  for lang in ['fr','en']:
   p=int(r['page']);old=r['replace'];new=r['with'];body=states[lang][p];count=body.count(old)
   states[lang][p]=body.replace(old,new)
   out.append(dict(lang=lang,page=p,id=r['source'],status='applied notation' if count else 'notation already present',count=count))
 # Non-variant extra repairs/restorations.
 for r in readj('edits'):
  if r['kind']=='variant':continue
  lang=r['lang'];p=int(r['page']);body=states[lang][p];old=r['old'];new=r['new'];om=positions(body,old);nm=positions(body,new)
  if nm and (not om or old in new):status='already present'
  elif len(om)==1:
   m=om[0];states[lang][p]=body[:m.start()]+new+body[m.end():];status='applied'
  else:status='missing' if not om else 'multiple'
  out.append(dict(lang=lang,page=p,id=r['source'],status=status,old=old,new=new,count=len(om)))
  if status=='applied':ops.append(dict(lang=lang,page=p,id=r['source'],old=old,new=new))
 # Insert restorations already containing reviewed variants.
 for r in readj('restorations')[:2]:
  p=int(r['page'])
  for lang in ['fr','en']:
   body=states[lang][p]
   if p==168:states[lang][p]=body.rstrip()+'\n\n'+r[lang]+'\n\n'
   if p==203:
    anchor='On a entre sommes de Gauss' if lang=='fr' else 'We have the following identity between Gauss sums and Jacobi sums.'
    m=positions(body,anchor)
    if m:states[lang][p]=body[:m[0].start()]+r[lang]+body[m[0].start():]
    else:out.append(dict(lang=lang,page=p,id=r.get('source',r.get('id')),status='restore anchor missing',old=anchor))
 # Variant diagnostics only, not yet inserting, so repeated and nested expressions remain visible.
 for r in readj('variants'):
  p=int(r['page'])
  for lang in ['fr','en']:
   if lang=='en' and not r['english_applicable']:continue
   old,new=(r['printed'],r['corrected']) if lang=='fr' else (r['en_printed'],r['en_corrected'])
   body=states[lang][p]
   if r['id'] in body:status='embedded restoration'
   else:
    om=positions(body,old);nm=positions(body,new)
    status=f'variant old={len(om)} new={len(nm)}'
   out.append(dict(lang=lang,page=p,id=r['id'],status=status,old=old,new=new))
 (B/'diagnostic_report.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 (B/'diagnostic_ops.json').write_text(json.dumps(ops,ensure_ascii=False,indent=2))
 for lang in ['fr','en']:
  (B/f'diagnostic_{lang}.tex').write_text(pres[lang]+''.join('\\PrintPage{'+str(p)+'}\n'+body for p,body in states[lang].items()))
 (B/'diagnostic_report.txt').write_text('\n'.join(f"{r['lang']} {r['page']} {r['id']} {r['status']} {r.get('old')!r} -> {r.get('new')!r}" for r in out))
 print('Reports written',len(out))

if __name__=='__main__':diagnostic()
