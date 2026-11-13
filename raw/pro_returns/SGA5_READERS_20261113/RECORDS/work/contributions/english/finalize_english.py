"""Finalize the English branches, retaining explicit source-to-reading maps."""
from pathlib import Path
import re,json,csv,difflib,bisect,collections,hashlib
import prepare_english as p
import project_glyphs as glyph
import project_internal_hom as ih
OUT=Path(__file__).parent
SRC=Path('work/sources')

def balanced(s):
 n=0
 for m in re.finditer(r'(?<!\\)[{}]',s):
  n+=1 if m[0]=='{' else -1
  if n<0:return False
 return n==0

def apply_patches(s,records):
 audit=[]
 for r in records:
  if r.get('language')!='EN':continue
  old,new=r['old'],r['new'];n=s.count(old);expect=r.get('expected_count',1)
  if n!=expect:raise ValueError((r['id'],'patch count',n,expect))
  s=s.replace(old,new)
  audit.append({**r,'applied_count':n})
 return s,audit

def main():
 en0=(SRC/'SGA5_EN'/p.ENREL).read_text();frc=(SRC/'SGA5_FR'/p.FRC).read_text();frd=(SRC/'SGA5_FR'/p.FRD).read_text()
 decisions=json.loads(Path('work/contributions/decisions/open_item_patches.json').read_text())
 en,audit=apply_patches(en0,decisions)
 # The two French layers give this explicit local definition in III and III B.
 # Expand only these English occurrences, preserving the same rendered symbol.
 scope0=en.index('Exposé III ---');scope1=en.index('Exposé V ---')
 scoped=en[scope0:scope1];scoped_count=len(re.findall(r'\\uRHom(?![A-Za-z])',scoped))
 scoped=re.sub(r'\\uRHom(?![A-Za-z])',lambda m:r'\mathrm{R}\underline{\mathrm{Hom}}',scoped)
 en=en[:scope0]+scoped+en[scope1:]
 audit.append({'id':'EN-III-URHOM-SCOPE','page':'73-203','language':'EN','old':r'\uRHom','new':r'\mathrm{R}\underline{\mathrm{Hom}}','applied_count':scoped_count,'reason':'Both French source layers explicitly define the local internal derived Hom with R outside the underline in Exposés III and III B. The English preamble underlined the whole token; these scoped occurrences now retain the French rendering.','source':'fr/sga5/current/s5.tex;fr/sga5/diplomatic/s5.tex'})
 common=[
 {'id':'EN-208-COMPOSITION','page':208,'old':r'w_{ts}\circ w_{sr}=w_{tr}.','new':r'w_{sr}\circ w_{ts}=w_{tr}.','reason':'Carry the corrected French composition order of the projective-system transition morphisms, with the printed order retained in the diplomatic branch.','source':'fr/sga5/current/s5.tex;fr/sga5/diplomatic/s5.tex'},
 {'id':'EN-18-EXPLICIT-FORMULAS','page':18,'old':r'and the corresponding nonzero cohomology modules are isomorphic to $A_{\ol{x}}$.','new':r'and $\H^{-r(x)}(P_{\ol{x}})\simeq A_{\ol{x}}$, $\H^{+r(x)}(P\'_{\ol{x}})\simeq A_{\ol{x}}$.'.replace("\\'","'"),'reason':'Restore the two formulas explicitly given in the French sentence, so their individual printed misprints can be retained in the diplomatic English.','source':'fr/sga5/current/s5.tex;fr/sga5/diplomatic/s5.tex'},
 {'id':'GLOSSARY-FIBRE','page':'40-41','old':'fiber','new':'fibre','reason':'Use the ported English majority spelling fibre for the same French term fibre; covers singular and plural.','source':'GLOSSARY_SGA5_FR_EN.tsv'},
 {'id':'GLOSSARY-AR-NULL','page':241,'old':'AR-zero','new':'AR-null','reason':'Use AR-null, the rendering of AR-nul in the defining V 2.2.1 and the rest of the ported English.','source':'GLOSSARY_SGA5_FR_EN.tsv'}]
 common.extend([
 {'id':'GLOSSARY-SUBPRESCHEME','page':15,'old':'subpreschemes','new':'sub-preschemes','reason':'The one plural spelling denotes the same family (Y_i) of sous-préschémas in Lemma 1.14 as the hyphenated sub-prescheme used throughout the ported English. Use the existing spelling with its plural suffix.','source':'GLOSSARY_SGA5_FR_EN.tsv;sga5 I Lemma1.14'},
 {'id':'GLOSSARY-CUP-PRODUCT','page':'104-118','old':'cup product','new':'cup-product','reason':'The six occurrences translate cup-produit and cite the same pairings 4.1.4/4.2.5 used by the hyphenated rendering in the English index and the rest of the volume. Retain every formula and object while making the spelling consistent.','source':'GLOSSARY_SGA5_FR_EN.tsv;fr/sga5/current/s5.tex:ExposéIII'},
 {'id':'GLOSSARY-NEIGHBOURHOOD','page':'41-45','old':'neighborhood','new':'neighbourhood','reason':'Use the majority English spelling neighbourhood for voisinage, with no change to the stated open neighbourhood or local hypothesis.','source':'GLOSSARY_SGA5_FR_EN.tsv'},
 {'id':'EN-116-RESTORE-CLAUSE','page':116,'old':r"where $M_1=f_{1!}L_1$, $M_2=f_{2*}L_2$, and $M_3=f_{3*}L_3$.",'new':r"where $M_1=f_{1!}L_1$, $M_2=f_{2*}L_2$, and $M_3=f_{3*}L_3$, and an analogous commutative square with $\RHom$, which the reader will write down.",'reason':'Restore the French clause following (5.2.6), which the ported English omitted. The exact internal-Hom source rendering is supplied by the per-occurrence audit.','source':'fr/sga5/current/s5.tex:folio116;fr/sga5/diplomatic/s5.tex:folio116'},
 {'id':'EN-III-SECTION-COUNTER','page':76,'old':r'\section{Notation and recalls of Künneth formulae}','new':'\\setcounter{section}{0}\n'+r'\section{Notation and recalls of Künneth formulae}','reason':'The four numbered sections of Exposé III are 1–4 in both French source layers. Reset the carried LaTeX section counter before the first of them.','source':'fr/sga5/current/s5.tex:folio76'},
 {'id':'EN-30-CODOMAIN','page':30,'old':r'another dévissage gives'+'\n\\[\n   '+r'\R\,\underline{\Hom}(M,\R i^!G)\in\ob\D_c^+(Y).','new':r'another dévissage gives'+'\n\\[\n   '+r'\R\,\underline{\Hom}(M,\R i^!G)\in\ob\D_c^+(X).','reason':'Both French source layers give X in this concluding membership assertion. Preserve that source reading in both English forms; retain the separate missing parenthesis in the diplomatic form.','source':'fr/sga5/current/s5.tex:folio30;fr/sga5/diplomatic/s5.tex:folio30'},
 {'id':'EN-315-SGA3','page':315,'old':'(SGA 4 XXII 5.5.1)','new':'(SGA 3 XXII 5.5.1)','reason':'The corrected French citation is SGA 3 XXII 5.5.1; retain SGA 4 in the diplomatic reading.','source':'fr/sga5/current/s5.tex;fr/sga5/diplomatic/s5.tex'},
 {'id':'EN-482-INDEX-SECTION','page':482,'old':r'\sgaindexentry{rationality of $L$-functions (theorem)}{XV 2 no. 2}','new':r'\sgaindexentry{rationality of $L$-functions (theorem)}{XV 3 no. 2}','reason':'The corrected French index locates the rationality theorem in Exposé XV, section3, no.2. The print has XIV2.','source':'fr/sga5/current/s5.tex;fr/sga5/diplomatic/s5.tex'}])
 for r in common:
  n=en.count(r['old'])
  if not n:raise ValueError(('common absent',r['id']))
  en=en.replace(r['old'],r['new']);audit.append({**r,'language':'EN','applied_count':n})
 hom_rows,hom_review,hom_unmapped=ih.project(en)
 assert not hom_review and not hom_unmapped,(hom_review,hom_unmapped)
 for v in sorted(hom_rows,key=lambda x:x['start'],reverse=True):
  assert en[v['start']:v['end']]==v['before']
  en=en[:v['start']]+v['after']+en[v['end']:]
  if v['after']!=v['before']:audit.append({'id':v['id'],'page':v['page'],'language':'EN','old':v['before'],'new':v['after'],'applied_count':1,'reason':'Exact French formula occurrence and its explicit scoped macro expansion give R followed by underlined Hom; see EN_INTERNAL_HOM_AUDIT.tsv for both French readings and the matching English formula.','source':v['source']})
 OUT.joinpath('EN_INTERNAL_HOM_AUDIT.json').write_text(json.dumps(hom_rows,ensure_ascii=False,indent=2))
 OUT.joinpath('EN_INTERNAL_HOM_REVIEW.json').write_text(json.dumps(hom_review,ensure_ascii=False,indent=2))
 OUT.joinpath('EN_INTERNAL_HOM_UNMAPPED.json').write_text(json.dumps(hom_unmapped,ensure_ascii=False,indent=2))
 with OUT.joinpath('EN_INTERNAL_HOM_AUDIT.tsv').open('w') as h:
  fields=['id','page','expose','before','after','fr_token','fr_expansion','fr_diplomatic_token','source_definition','alignment','operation','fr_context','fr_diplomatic_context','en_context','source']
  w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(hom_rows)
 OUT.joinpath('EN_corrected_flat.tex').write_text(en)
 OUT.joinpath('EN_common_corrections.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
 cand,review,stats,anchors=p.initial_projection(frd,frc,en)
 OUT.joinpath('projection_candidates_final.json').write_text(json.dumps(cand,ensure_ascii=False,indent=2))
 OUT.joinpath('projection_review_final.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
 OUT.joinpath('alignment_anchors.json').write_text(json.dumps(anchors))
 fpages=p.getpages(frc); ms=p.mathchunks(en);mstarts=[m['start'] for m in ms]
 edits=[];exclusions=[]
 def locate(page,needle):
  poss=[m.start() for m in re.finditer(re.escape(needle),en)]
  if not poss:raise ValueError(('needle absent',page,needle))
  aim=p.estimate(fpages[int(page)]['start'],anchors)
  return min(poss,key=lambda x:abs(x-aim))
 def add(page,corrected,printed,source,reason='',position=None):
  if 73<=int(page)<204:
   corrected=corrected.replace(r'\RHom',ih.INTERNAL);printed=printed.replace(r'\RHom',ih.INTERNAL)
  a=locate(page,corrected) if position is None else position;b=a+len(corrected)
  assert en[a:b]==corrected,(page,corrected)
  if corrected==printed:return
  edits.append({'id':f'EN-MANUAL-{len(edits)+1:04d}','page':int(page),'start':a,'end':b,'before':printed,'after':corrected,'source':source,'kind':'print_correction','reason':reason})
 # Manual correspondences require full English context where the translation changes display grouping.
 add(19,r"P\simeq L[r_0],\qquad P'\simeq L^\vee[-r_0]",r"P\simeq L[-r_0],\qquad P'\simeq L^\vee[+r_0]",'fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(32,r'\underline D_X=\R\,\underline{\Hom}(\ ,A_X)',r'\underline D_X=\R\,\Hom(\ ,A_X)','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(41,r'(4.5.3)^{\mathrm{bis}}',r'(4.5.3)','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(42,r'(4.5.3)$^{\mathrm{bis}}$',r'(4.5.3)','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 for pg,tail in [(59,'K'),(60,'K'),(66,'F')]:
  a=locate(pg,r'\dim.\mathrm{top}_{\bar{x}}('+tail+')')
  add(pg,r'\dim.\mathrm{top}_{\bar{x}}('+tail+')',r'\operatorname{dimstop}_{\bar{x}}('+tail+')','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex',position=a)
 add(83,r'f_1^{*}F_1\otimes^{L}_{S}f_2^{*}F_2',r'f_1^{*}F_1\otimes^{L}f_2^{*}F_2','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(84,r'u_1\otimes^L_S E_2',r'u_1\otimes_S E_2','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(84,r'\draw[->] (D) -- (E);',r'\draw (D) -- (E);','FR_variants.json:FR-0352;fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex','The printed diagram (2.5.1) omits this arrowhead; the corrected layer supplies it.')
 add(85,r"\RHom(E\otimes^L_SP',F\otimes^L_SQ')",r"\RHom(E\otimes^L_SP',F'\otimes^L_SQ')",'fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 # Entire square to preserve all eleven printed symbol changes, including a missing derived L and an extra parenthesis.
 marker=r'f^{*}\RHom(P,Q)\otimes^L f^{*}\RHom(L,M)'.replace(r'\RHom',ih.INTERNAL)
 ix=locate(85,marker);j=bisect.bisect_right(mstarts,ix)-1;ec=ms[j]['text']
 ep=ec.replace('P','E').replace('Q','F')
 old=r'f^{*}\RHom(E\otimes^LL,F\otimes^LM)'.replace(r'\RHom',ih.INTERNAL);new=r'f^{*}\RHom(E\otimes^LL,F\otimes^LM))'.replace(r'\RHom',ih.INTERNAL)
 assert old in ep;ep=ep.replace(old,new)
 old=r'\RHom(f^{*}(E\otimes^LL),f^{*}(F\otimes^LM))'.replace(r'\RHom',ih.INTERNAL);new=r'\RHom(f^{*}(E\otimes^L1),f^{*}(F\otimes M))'.replace(r'\RHom',ih.INTERNAL)
 assert old in ep;ep=ep.replace(old,new)
 add(85,ec,ep,'fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex',position=ms[j]['start'])
 add(307,r'P_T(F)\to T',r'P_T(F)\to F','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(309,r'$j_i$-th',r'$j$-th','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(328,r'R\Gamma_Y(X,u\otimes^L\operatorname{id}_M)',r'R\Gamma(X,u\otimes^L\operatorname{id}_M)','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(331,r'g^*(g_*(\cdot))c_{d-1}(\check F)',r'g^*(g_*(\cdot)c_{d-1}(\check F))','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(341,r'\sum_{0\le p\le d}g_1^*(b_p)\bar\xi^p',r'\mathop{\phantom{\sum}}\limits_{0\le p\le d}g_1^*(b_p)\bar\xi^p','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(385,r"\mathbb Z_\ell[G_{y'}]",r'\mathbb Z_\ell[G]','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(390,r'\EP(C)\clKstar{\Lambda_\nu[G]}(\Lambda_\nu[G])',r'\EP(C)\operatorname{cl}_{K^{\bullet}(\Lambda_\nu[G]}(\Lambda_\nu[G])','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(400,r'\EP(C)\clKstar{\Lambda[G]}(\Lambda[G])',r'\EP(C)\operatorname{cl}_{K^{\bullet}(\Lambda[G]}(\Lambda[G]','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 for pg,whole in [(394,r"\varphi:\mathbb Z_\ell[G']\longrightarrow \mathbb Z_\ell[G]"),(395,r"Sw_{G,x}\simeq Sw_{G',x}\otimes_{\mathbb Z_\ell[G']}\mathbb Z_\ell[G]")]:
  pos=locate(pg,whole)
  for m in re.finditer(re.escape(r'\mathbb Z'),whole):
   add(pg,r'\mathbb Z','Z','FR_variants.json:FR-0803;FR_variants.json:FR-0804;FR_variants.json:FR-0806;fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex','Retain the exact printed plain Z and corrected blackboard Z at this occurrence.',position=pos+m.start())
 add(397,r'and $\underline{\Gamma}^G$ sends an injective sheaf',r'and $\Gamma^G$ sends an injective sheaf','FR_variants.json:FR-0812;fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(397,r'adjoints of $\Gamma_C$ and $\underline{\Gamma}^G$',r'adjoints of $\Gamma_C$ and $\Gamma^G$','FR_variants.json:FR-0813;fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(411,r'\otimes_{\La_m}^{\mathbb L}\La_n&\simeq R\Hom',r'\otimes_{\La_m}\La_n&\simeq R\Hom','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(436,r"g^{-1}f'(T)=",r'g^{-1}f^{1}(T)=','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(436,r"\nu(g^{-1}f')>1",r'\varepsilon(g^{-1}f^{1})>1','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 add(433,r"let $f'/G_{x'}$ be the endomorphism",r"let $F'/G_{x'}$ be the endomorphism",'OPEN-H75')
 add(93,ih.INTERNAL+r'_S(f_{1!}L_1,f_{2*}L_2)',ih.PLAIN+r'_S(f_{1!}L_1,f_{2*}L_2)','fr/sga5/current/s5.tex:folio93;fr/sga5/diplomatic/s5.tex:folio93')
 add(97,r'Rp_{2!}A_X',r'Rp_{2!}A_{X_2}','fr/sga5/current/s5.tex:folio97;fr/sga5/diplomatic/s5.tex:folio97','Preserve the printed nested subscript as one TeX argument, as explicitly grouped in the French source.')
 add(126,r"f_*c''_*"+ih.INTERNAL+r"(c_2''{}^*L_2,c_1''{}^!L_1)",r"f_*c''_*"+ih.PLAIN+r"(c_2''{}^*L_2,c_1''{}^!L_1)",'fr/sga5/current/s5.tex:folio126;fr/sga5/diplomatic/s5.tex:folio126')
 add(101,r"E''=C'\times_XD'",r"E''=C'\times_{X'}D'",'fr/sga5/current/s5.tex:folio101;fr/sga5/diplomatic/s5.tex:folio101')
 add(385,r'$\sigma_y$',r"$\sigma_{y'}$",'fr/sga5/current/s5.tex:folio385;fr/sga5/diplomatic/s5.tex:folio385','The printed prime belongs inside the y subscript; preserve the exact grouped source reading.')
 add(385,r"$\sigma'_y$",r"$\sigma'_{y'}$",'fr/sga5/current/s5.tex:folio385;fr/sga5/diplomatic/s5.tex:folio385','The printed y-prime subscript is distinct from the existing prime on sigma; preserve both source groups.')
 add(472,r'with $F_\nu$ annihilated by $\ell^{\nu+1}$',r'with $F$ annihilated by $\ell^{\nu+1}$','SOL-EN-084')
 needle=r'\R\,\underline{\Hom}(M,\R i^!G)\in\ob\D_c^+(X)'
 add(30,needle,r'\R\,\underline{\Hom}(M,\R i^!G\in\ob\D_c^+(X)','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 # Prose/reference variants are supplied in a separate exact-reading catalogue.
 extra=OUT/'manual_prose_variants.json'
 if extra.exists():
  for v in json.loads(extra.read_text()):
   needle=v['after'].replace('}{XV 2 no. 2}', '}{XV 3 no. 2}')
   add(v['page'],needle,v['before'],v['source'],v.get('reason',''))
  add(315,'(SGA 3 XXII 5.5.1)','(SGA 4 XXII 5.5.1)','fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex')
 for x in cand:
  a,b=x['start'],x['end']
  if any(not(b<=v['start'] or v['end']<=a) or (a==b and v['start']<=a<=v['end']) for v in edits):continue
  if x['page'] in [19,30] and x['ratio']<.87:
   exclusions.append({**x,'disposition':'manual paragraph-level correspondence required; rejected wrong local match'});continue
  if not balanced(x['before']) or not balanced(x['after']):
   exclusions.append({**x,'disposition':'macro expansion handled separately; raw candidate is not a standalone TeX fragment'});continue
  x={**x,'id':f'EN-PROJ-{len(edits)+1:04d}'};edits.append(x)
 # Project the scoped source-macro glyph differences onto exact English formula occurrences.
 glyph_edits,glyph_review=glyph.project(en)
 for i,g in enumerate(glyph_edits,1):
  overlaps=[v for v in edits if not(g['end']<=v['start'] or v['end']<=g['start'])]
  if not overlaps:
   edits.append({**g,'id':f'EN-GLYPH-{i:04d}'});continue
  if len(overlaps)!=1:raise ValueError(('glyph crosses variants',g,overlaps))
  v=overlaps[0];a,b=g['start']-v['start'],g['end']-v['start']
  if not(0<=a<=b<=len(v['after'])):raise ValueError(('glyph partial overlap',g,v))
  # Relate the unchanged glyph token in the full expression's two exact readings.
  matches=[]
  for op,aa,bb,cc,dd in difflib.SequenceMatcher(None,v['after'],v['before'],autojunk=False).get_opcodes():
   if op=='equal' and aa<=a and b<=bb:matches.append((cc+a-aa,cc+b-aa))
  if len(matches)!=1:raise ValueError(('glyph has no unique exact subspan in printed expression',g,v))
  ga,gb=matches[0];v['before']=v['before'][:ga]+g['before']+v['before'][gb:]
  if g['after']!=g.get('original',g['after']):
   # The manual expression originally contained the same source token.
   v['original']=v.get('original',v['after']);v['after']=v['after'][:a]+g['after']+v['after'][b:]
  v['source']+='; '+g['source'];v.setdefault('glyph_sources',[]).append({k:g[k] for k in ['page','fr_corrected','fr_diplomatic','en_context'] if k in g})
 OUT.joinpath('EN_GLYPH_VARIANTS.json').write_text(json.dumps(glyph_edits,ensure_ascii=False,indent=2))
 OUT.joinpath('EN_GLYPH_REVIEW.json').write_text(json.dumps(glyph_review,ensure_ascii=False,indent=2))
 # The 32 scan readings retain individual source IDs. The extra plain R at p461 is common to both forms.
 xv=en.index('Exposé XV ---'); rg=list(re.finditer(r'\\RGamma|(?<![A-Za-z\\])R\\Gamma|\\R\\Gamma',en[xv:]))
 assert len(rg)==33,len(rg)
 folios=[457]*7+[458]*4+[459]+[460]*10+[461]*2+[470]*2+[472]*2+[473]*2+[474]*2
 rr=[m for i,m in enumerate(rg) if i!=22]
 for i,(m,pg) in enumerate(zip(rr,folios),1):
  a=xv+m.start();b=xv+m.end()
  edits.append({'id':f'R98-{i:02d}','page':pg,'start':a,'end':b,'before':r'\underline{\underline{\mathrm{R}}}\Gamma','after':r'\mathrm{R}\Gamma','original':en[a:b],'source':f'R98-{i:02d}','kind':'derived_functor_glyph','reason':'Direct scan decision; corrected derived-functor convention GLOBAL_ISSUES 98.'})
 # Canonical corrected spelling at the R98 sites is applied before source-offset reconciliation below.
 # Common scan replacements must also exist in the corrected branch.
 encoding=[]
 for v in edits:
  a,b=v['start'],v['end'];old=v['before'];tail=en[b:b+1]
  if old in [r'\ol',r'\check'] and tail.isalpha():
   # Retain the exact accent argument while delimiting the TeX control word.
   v['end']+=1;v['after']+=tail;v['before']=old+'{'+tail+'}'
  elif re.search(r'\\[A-Za-z]+$',old) and tail.isalpha():
   v['before']=old+' '
  elif not old and tail.isalpha() and re.search(r'\\[A-Za-z]+$',en[:a]):
   # A deleted subscript marker can otherwise merge \\mu and n into \\mun.
   v['before']=' '
  if old!=v['before']:
   eid=f'EN-ENCODING-{len(encoding)+1:02d}'
   encoding.append({'id':eid,'variant_id':v['id'],'page':v['page'],'raw_projected_fragment':old,'encoded_printed_fragment':v['before'],'reason':'Delimit the control word and its exact source argument so TeX renders the recorded French printed reading without creating a new command name.','source':'fr/sga5/diplomatic/s5.tex'})
   v['source']+='; '+eid;v['encoding_repair']=eid
 OUT.joinpath('EN_ENCODING_REPAIRS.json').write_text(json.dumps(encoding,ensure_ascii=False,indent=2))
 ee=sorted(edits,key=lambda v:(v['start'],v['end']))
 # Separate math-span groups ensure markers and TeX arguments do not break a formula.
 for i in range(1,len(ee)):
  if ee[i]['start']<ee[i-1]['end']:raise ValueError(('overlap',ee[i-1],ee[i]))
 dip=en;cur=en
 for v in reversed(ee):
  a,b=v['start'],v['end'];assert en[a:b]==v.get('original',v['after'])
  dip=dip[:a]+v['before']+dip[b:];cur=cur[:a]+v['after']+cur[b:]
 # Reconcile output positions after the common spelling expansions.
 delta=0
 for v in ee:
  v['start_corrected']=v['start']+delta;v['end_corrected']=v['start_corrected']+len(v['after']);delta+=len(v['after'])-(v['end']-v['start'])
  v['expose']=p.expose(v['page'])
 OUT.joinpath('EN_corrected_flat.tex').write_text(cur)
 OUT.joinpath('EN_diplomatic_flat.tex').write_text(dip)
 OUT.joinpath('EN_variants.json').write_text(json.dumps(ee,ensure_ascii=False,indent=2))
 OUT.joinpath('EN_projection_exclusions.json').write_text(json.dumps(exclusions,ensure_ascii=False,indent=2))
 OUT.joinpath('EN_preparation_summary.json').write_text(json.dumps({'variants':len(ee),'scan_variants':32,'common_correction_operations':len(audit),'projection_stats':stats,'projection_review':len(review),'projection_review_disposition':'Every raw matcher diagnostic is disposed of in EN_PROJECTION_REVIEW_DECIDED.tsv; full manual reading pairs supersede unresolved token fragments.','excluded_candidates':len(exclusions),'excluded_candidate_disposition':'Rejected p19 wrong-nearby-formula candidate; the exact intended English formula has a full manual variant.','scoped_R_glyph_occurrences':len(glyph_edits),'scoped_R_glyph_unmapped':len(glyph_review),'internal_Hom_occurrences':len(hom_rows),'internal_Hom_unmapped':len(hom_unmapped),'source_encoding_repairs':len(encoding)},indent=2))
 print(json.dumps({'variants':len(ee),'common_corrections':len(audit),'excluded_candidates':len(exclusions),'review_cases':len(review)}))
if __name__=='__main__':main()
