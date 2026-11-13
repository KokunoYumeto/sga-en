"""Project scoped French derived-R glyph readings onto matching English formula occurrences."""
from pathlib import Path
import json,re,bisect,difflib,collections
import prepare_english as p
RX=re.compile(r'\\(?:uRHom|RHom|RGamma|RGc|RG|Rpi|Rj|rG|R)(?![A-Za-z@])|\\(?:mathrm|mathbb)\s*(?:\{R(?:Hom)?\}|R)|(?<![A-Za-z\\])R(?=[^A-Za-z]|[fijpg](?:[_^\x27(]|\\))')

def glyphs(s):return list(RX.finditer(s))
def print_r(s):
 if s==r'\uRHom':return r'\underline{\mathbb{R}\mathrm{Hom}}'
 if s in [r'\RHom',r'\mathrm{RHom}']:return r'\mathbb{R}\mathrm{Hom}'
 tails={r'\RGamma':r'\Gamma',r'\RG':r'\Gamma',r'\RGc':r'\Gamma_c',r'\Rpi':r'\pi',r'\Rj':'j',r'\rG':r'\Gamma^G'}
 return r'\mathbb{R}'+tails.get(s,'')

def upright_r(s):
 # A literal derived R in the English source needs the convention's explicit upright font.
 return r'\mathrm{R}' if s=='R' else s

MANUAL=[
 (12,r'K_X = \mathrm{R}^{!}f(K_Y)',r'K_X=\R^!f(K_Y)'),
 (12,r'(i) \qquad \mathrm{R} f_{*}',r'\R f_*\underline D_X(F)\xrightarrow{\sim}\underline D_Y\R_!f(F)'),
 (13,r'(ii) \qquad \mathrm{R}_{!}f',r'\R_!f\,\underline D_X(F)\xrightarrow{\sim}\underline D_Y\R f_*(F)'),
 (13,r'(i) \qquad \mathrm{R}^{!}f',r'\R^!f\,\underline D_Y(F)\xrightarrow{\sim}\underline D_X f^*(F)'),
 (13,r'(ii) \qquad f^{*}',r'f^*\underline D_YF\xrightarrow{\sim}\underline D_X\R^!f\,F'),
 (15,r'K_X = \mathrm{R}^{!}f(K_Y)',r'K_X=\R^!f(K_Y)'),
 (16,r'\mathrm{R}^{!}f \simeq \mathrm{R}^{!}i',r"\R^!f\simeq\R^!i\,\R^!f'"),
 (30,r'\mathrm{R}\,\underline{\Hom}(M, \mathrm{R} i^{!}(G)) \in \ob \D_c^{+}(X)',r'\R\,\underline{\Hom}(M,\R i^!G)\in\ob\D_c^+(X)'),
 (31,r'F \to \mathrm{R} j_{*}j^{*}(F)',r'F\longrightarrow \R j_*j^*F'),
 (32,r'\underline{D}_X = \mathrm{R}',r'\underline D_X=\R\,\underline{\Hom}(\ ,A_X)'),
 (33,r"(A'_Y, \mathrm{R}^{!}i(A_X))",r"(A'_Y,\R^!i(A_X))"),
 (34,r'\dim.\mathrm{q.inj}(\mathrm{R}^{!}f(A_S))',r'\dim.\,q.\,inj\bigl(\R^!f(A_S)\bigr)'),
 (40,r'(\underline{D}_XF)_{\ol{x}}&\simeq',r'(\underline{D}_XF)_{\ol{x}}&\simeq'),
 (44,r'K_Y=\mathrm{R}\Gamma_Y(K_X)',r'K_Y=\R\Gamma_Y(K_X)'),
 (328,r'\mathrm{R}\Gamma(X,u\mathbin',r'R\Gamma(X,u\otimes^L\operatorname{id}_M)'),
]

def project(en):
 base=Path('work/build/prepared');frc=(base/'FR_corrected_body.tex').read_text();frd=(base/'FR_diplomatic_body.tex').read_text()
 fc,ec,direct,anchors=p.align_math(frc,en);fkeys=[m['start'] for m in fc];fps=p.getpages(frc);dps=p.getpages(frd)
 out=[];review=[];mapped=0
 for pg,cp in fps.items():
  dp=dps[pg];cs=p.mathchunks(cp['text']);ds=p.mathchunks(dp['text'])
  sm=difflib.SequenceMatcher(None,[m['key'] for m in cs],[m['key'] for m in ds],autojunk=False)
  pairs=[]
  for op,a,b,k,l in sm.get_opcodes():
   if op=='equal' or b-a==l-k:pairs.extend((a+i,k+i) for i in range(b-a))
   else:
    for j in range(a,b):
     cand=sorted([(difflib.SequenceMatcher(None,cs[j]['key'],ds[q]['key'],autojunk=False).ratio(),q) for q in range(k,l)],reverse=True)
     if cand and cand[0][0]>.7:pairs.append((j,cand[0][1]))
  for ci,di in pairs:
   c,d=cs[ci],ds[di];cg,dg=glyphs(c['text']),glyphs(d['text'])
   if len(cg)!=len(dg):
    if r'\mathbb{R}' in d['text'] and r'\mathrm{R}' in c['text']:review.append({'page':pg,'reason':'French R occurrence counts differ','corrected':c['text'],'diplomatic':d['text']})
    continue
   changed=[i for i,(a,b) in enumerate(zip(cg,dg)) if r'\mathbb{R}' in b[0] and r'\mathrm' in a[0]]
   if not changed:continue
   fpos=cp['start']+c['start'];fi=bisect.bisect_left(fkeys,fpos);ei=direct.get(fi)
   manual=[needle for page,frneedle,needle in MANUAL if pg==page and frneedle in c['text']]
   if manual:
    assert len(manual)==1,(pg,c,manual)
    opts=[j for j,e in enumerate(ec) if manual[0] in e['text']]
    if not opts:raise ValueError(('manual glyph correspondence absent',pg,manual[0]))
    aim=p.estimate(fpos,anchors);ei=min(opts,key=lambda j:abs(ec[j]['start']-aim))
   if ei is None:
    aim=p.estimate(fpos,anchors);cand=sorted([(difflib.SequenceMatcher(None,c['key'],e['key'],autojunk=False).ratio()-abs(aim-e['start'])/300000,j) for j,e in enumerate(ec) if abs(aim-e['start'])<3000],reverse=True)
    if cand and cand[0][0]>.85:ei=cand[0][1]
   if ei is None:
    review.append({'page':pg,'reason':'English R formula not aligned','corrected':c['text'],'diplomatic':d['text']});continue
   e=ec[ei];eg=glyphs(e['text'])
   if len(eg)!=len(cg):
    review.append({'page':pg,'reason':'English R occurrence counts differ','corrected':c['text'],'english':e['text'],'fr_count':len(cg),'en_count':len(eg)});continue
   for q in changed:
    m=eg[q];old=m[0];new=print_r(old)
    if new==old:continue
    out.append({'page':pg,'start':e['start']+m.start(),'end':e['start']+m.end(),'before':new,'after':upright_r(old),'original':old,'source':'conventions/GLOBAL_ISSUES_SGA.md:98;fr/sga5/diplomatic/s5.tex:macro R/RHomCore;fr/sga5/current/s5.tex:macro R/RHomCore','kind':'derived-functor typography','reason':'The corresponding French formula has this exact scoped blackboard-R expansion in the diplomatic layer and an upright-R expansion in the corrected layer. English occurrence mapped by formula and within-formula R order.','fr_corrected':c['text'],'fr_diplomatic':d['text'],'en_context':e['text']})
    mapped+=1
 # Exact repeated formulas can map twice at a boundary; de-duplicate the same English character span.
 uniq={}
 for v in out:uniq[(v['start'],v['end'])]=v
 return list(uniq.values()),review
if __name__=='__main__':
 out=Path(__file__).parent;v,r=project((out/'EN_corrected_flat.tex').read_text())
 (out/'EN_GLYPH_VARIANTS.json').write_text(json.dumps(v,ensure_ascii=False,indent=2));(out/'EN_GLYPH_REVIEW.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps({'glyphs':len(v),'review':len(r)}))
