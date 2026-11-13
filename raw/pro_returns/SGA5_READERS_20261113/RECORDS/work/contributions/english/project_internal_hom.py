"""Match each English derived-Hom token to its explicit French formula occurrence."""
from pathlib import Path
import re,json,bisect,difflib,collections
import prepare_english as p
INTERNAL=r'\mathrm{R}\underline{\mathrm{Hom}}'
PLAIN=r'\mathrm{R}\mathrm{Hom}'
RX=re.compile(r'\\(?:uRHom|RHom)(?![A-Za-z])|'+re.escape(INTERNAL)+'|'+re.escape(PLAIN)+r'|R\\underline\{\\Hom\}')

def search_key(s):
 # Only the search key uses this exact list of two TeX constructions for
 # a derived tensor. The source strings and every token position remain intact.
 s=s.replace(r'\overset{\mathrm{L}}{\otimes}',r'\otimes^{L}')
 s=s.replace(r'\overset{\mathbf L}{\otimes}',r'\otimes^{L}')
 s=re.sub(r'\\otimes(_(?:\{[^{}]*\}|[A-Za-z0-9]))\^\{\\(?:mathbf|mathrm)\s*L\}',lambda m:r'\otimes^{L}'+m[1],s)
 s=re.sub(r'\\otimes\^\{\\(?:mathbf|mathrm)\s*L\}',lambda m:r'\otimes^{L}',s)
 return p.norm(s)

def project(en):
 fr=Path('work/sources/SGA5_FR/fr/sga5/current/s5.tex').read_text()
 frd=Path('work/sources/SGA5_FR/fr/sga5/diplomatic/s5.tex').read_text()
 fc,ec,direct,anchors=p.align_math(fr,en);fp=p.getpages(fr)
 _,dc,ddirect,danchors=p.align_math(fr,frd)
 fk=[search_key(m['text']) for m in fc];ek=[search_key(m['text']) for m in ec]
 fstarts=[v['start'] for v in fp.values()];folios=list(fp)
 def folio(x):return folios[max(0,bisect.bisect_right(fstarts,x)-1)]
 e0=en.index('Exposé III ---');e1=en.index('Exposé V ---')
 out=[];review=[];used=set()
 for fi,f in enumerate(fc):
  pg=folio(f['start'])
  if not 73<=pg<204:continue
  fs=list(RX.finditer(f['text']))
  if not fs:continue
  ei=direct.get(fi);method='exact formula token correspondence'
  if ei is None:
   aim=p.estimate(f['start'],anchors)
   opts=[]
   for j,e in enumerate(ec):
    if e0<=e['start']<e1 and abs(e['start']-aim)<2200 and len(list(RX.finditer(e['text'])))==len(fs):
     if any(e['start']+m.start() in used for m in RX.finditer(e['text'])):continue
     ratio=difflib.SequenceMatcher(None,fk[fi],ek[j],autojunk=False).ratio()
     if ratio>.88:opts.append((ratio-abs(e['start']-aim)/500000,j))
   opts.sort(reverse=True)
   if opts:ei=opts[0][1];method='formula correspondence with exact derived-Hom occurrence count and source-token order'
  if ei is None:
   review.append({'page':pg,'reason':'French formula has no eligible English match','fr_context':f['text']});continue
  e=ec[ei];es=list(RX.finditer(e['text']))
  if len(fs)!=len(es):
   review.append({'page':pg,'reason':'Derived-Hom token counts differ','fr_context':f['text'],'en_context':e['text']});continue
  di=ddirect.get(fi)
  if di is None:
   aim=p.estimate(f['start'],danchors)
   opts=[(difflib.SequenceMatcher(None,f['key'],d['key'],autojunk=False).ratio()-abs(d['start']-aim)/500000,j) for j,d in enumerate(dc) if abs(d['start']-aim)<2500 and len(list(RX.finditer(d['text'])))==len(fs)]
   if opts:di=max(opts)[1]
  assert di is not None,('no diplomatic formula for Hom audit',pg,f['text'])
  d=dc[di];ds=list(RX.finditer(d['text']));assert len(ds)==len(fs),(pg,f['text'],d['text'])
  for fm,em,dm in zip(fs,es,ds):
   ep=e['start']+em.start();fq=f['start']+fm.start()
   if ep in used:
    review.append({'page':pg,'reason':'English formula occurrence mapped twice','en_position':ep,'fr_position':fq});continue
   used.add(ep)
   internal=fm[0] in [r'\uRHom',INTERNAL,r'R\underline{\Hom}']
   after=INTERNAL if internal else em[0]
   out.append({'id':f'EN-III-HOM-{len(out)+1:04d}','page':pg,'expose':p.expose(pg),'start':ep,'end':e['start']+em.end(),'before':em[0],'after':after,'fr_position':fq,'fr_token':fm[0],'fr_expansion':INTERNAL if internal else PLAIN,'source_definition':r'\renewcommand{\uRHom}{\mathrm{R}\underline{\mathrm{Hom}}}' if fm[0]==r'\uRHom' else 'Explicit glyph sequence in the French formula','fr_context':f['text'],'fr_diplomatic_token':dm[0],'fr_diplomatic_context':d['text'],'en_context':e['text'],'alignment':method,'operation':'repair internal-Hom rendering' if after!=em[0] else 'retain exact source rendering','source':'fr/sga5/current/s5.tex;fr/sga5/diplomatic/s5.tex:scoped uRHom definition in Exposés III and III B'})
 # Every remaining English token is exposed for a source-based decision.
 unmapped=[]
 for m in RX.finditer(en,e0,e1):
  if m.start() not in used:unmapped.append({'start':m.start(),'end':m.end(),'token':m[0],'context':en[max(e0,m.start()-140):min(e1,m.end()+180)]})
 return out,review,unmapped

if __name__=='__main__':
 out=Path(__file__).parent;s=(out/'EN_corrected_flat.tex').read_text();rows,review,left=project(s)
 for name,value in [('EN_INTERNAL_HOM_AUDIT.json',rows),('EN_INTERNAL_HOM_REVIEW.json',review),('EN_INTERNAL_HOM_UNMAPPED.json',left)]:
  (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2))
 print(json.dumps({'mapped':len(rows),'repairs':sum(v['before']!=v['after'] for v in rows),'source_review':len(review),'english_unmapped':len(left)}))
