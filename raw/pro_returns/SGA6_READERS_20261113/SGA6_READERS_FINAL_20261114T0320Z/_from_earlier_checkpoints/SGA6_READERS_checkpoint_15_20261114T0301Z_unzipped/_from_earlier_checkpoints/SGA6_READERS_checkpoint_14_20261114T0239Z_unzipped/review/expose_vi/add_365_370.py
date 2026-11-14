#!/usr/bin/env python3
"""Explicit readings of the six complete primary pages and native witnesses."""
import re,json
from review_helpers import Review,ROOT,REGISTRY,base_text
r=Review()
obs365={
32:("Exposé VI, then two double-ruled capital title lines",'Both complete images preserve the three blocks and the raised K dot. The attached title carries every word; capital accents follow NOTE_6.','Complete heading'),
33:('par Pierre BERTHELOT, underlined','Both images give the full first name and capital surname with a lower rule. Retain the exact credit.','Author line'),
34:('The ring homomorphism is inline','The f-star arrow occurs between the colon and munissant in the statement. The attached inline placement keeps the formula and its order.','Theorem1.1'),
35:('Baseline dots between the resolution arrows','Both scans place the three dots at the baseline, including the native lower-page image. Retain ldots between the same arrows.','Plan(b), resolution'),
36:('Module module','Both scans repeat the noun. Current removes the second, lower-case copy; diplomatic keeps both words. The graded module, ring and all qualification words remain identical.','Plan(a)'),
37:('The parenthesis opened before S(E) has no closing mate','Both scans end the EGA locator with a stop alone. Current adds one close before that stop, matching the opening before the symmetric-algebra explanation.','Plan(a), last line'),
38:('Theorem1.1 has individual upright word-group rules','The complete primary and native pages show the listed prose rules, with mathematical letters and formulas treated independently. Restore the explicit groups below.','Complete theorem'),
39:('E,F,M,L,N have individual letter rules','The primary enlarged Plan(b) confirms the rule under its M, also present in the witness. All seven E, two F, four M, four L and two N occurrences are ruled; indices and arguments remain outside the rules. The doubly ruled S retains the explicitly accepted NOTE_6 bold transport. The source P is separately adjudicated under ASTRA-VI-PROJECTIVE-P-365: literal double rule diplomatically, bold P currently.','Theorem and complete plan'),
}
for k,(p,w,g) in obs365.items():
 r.finding('361_365',k,p,w,g,witness=376,verdict='not applied and now applied' if k in [36,37,38,39] else 'confirmed')
obs={
1:('2°)1,...,xi^(r+1) begins366','Both scans place the entire second item above every other line on366. The attached marker precedes2° and retains the correct split.','Boundary365/366',366),
2:('K has a raised solid dot','The two K superscripts have solid dots, while2° and3° use small circles. Retain the existing bullet forms; no extrapolation to unviewed occurrences is made.','Plan items2° and3°',366),
3:('Individually ruled sheaf letters; the target M in(1.2.1) is plain','All six complete pages and native witnesses were read. B,M,N,P,Q on366 are ruled except the target M of(1.2.1), whose missing rule is separately recorded with its exact component map. On370 only the sheaf letters before Lemme1.5.1 are ruled; its ring-case A,B,M and tilded letters are plain. Restore the occurrence-specific mapping below.','Every sheaf letter on366–370',366),
4:('Individual upright statement-word rules','The statements on367,368 and370 have separately ruled prose groups. Their numbers, variables, formulas and terminal punctuation remain outside those prose rules; the individual sheaf rules are restored separately.','Proposition1.2.3, Proposition1.3, Corollary1.4 and Lemme1.5.1',367),
5:('On obtient ainsi starts a new indented paragraph','Both images show the paragraph indentation after(1.2.2). Retain the existing blank line.','After(1.2.2)',367),
6:('A headed isomorphism between the two decompositions','Both images show a tilde over a right-pointing arrow here; the first two comparisons on the page have a bar without an arrowhead. Retain the exact three observed forms.','Proof1.2.3, display',367),
7:('No stop follows décomposition','Both images end the first paragraph without a stop. Diplomatic keeps the omission; current supplies the sentence-ending full stop already present.','First paragraph end',368),
8:('Gamma_*(Proj_0 M-prime), with one surrounding pair','Both images show no inner parentheses around M-prime in this occurrence, while the preceding Proj_0(M-prime) retains them. Keep the two exact formulas.','Last paragraph',368),
9:('EGA III2.3.1','The native300dpi crop shows the short inner horizontal stroke and lower right vertical of G; its main-scan stroke is weak. The full page also supplies the clearly printed EGA locators above. Retain EGA as the damaged-glyph reading.','Last paragraph, EGA locator',368),
10:('S in S(E) has two lower rules','The native pages368–370 and primary images confirm the two rules under S and the single rule under E. The existing Sym macro gives the NOTE_6 accepted bold S; E receives its own rule.','Every Sym occurrence in the reviewed pages',368),
11:('noethériennnes','The three adjacent n letters occur in both images. Current removes the duplicated n; diplomatic retains it.','First paragraph',369),
12:('dans le cas ou S est noethérien','Both images have unaccented ou. Current restores où for the relative expression dans le cas où, retaining the complete mathematical clause.','Second paragraph',369),
13:('g_0 is above the lower horizontal arrow','Both complete images give g above, f left, f_0 right and g_0 above. The attached diagram matches these positions and all four endpoints.','Cartesian square',369),
14:('et un faisceau begins370','The native and primary369 end at lambda-prime≥lambda;370 begins with all three words et un faisceau. Retain the attached marker.','Boundary369/370',370),
15:('F=u-prime-star_lambda-prime(F_lambda-prime)','Both scans show the prime immediately after u and the star above. Retain u-prime: X→X_lambda-prime, with the same pullback argument. The base-map u has source S and is connected by the displayed Cartesian base-change construction; no prime is dropped.','First line',370),
16:('u-prime_lambda-prime: X→X_lambda-prime','The parenthetical morphism has the same visible prime after u as the preceding formula. Retain both occurrences.','Second line',370),
17:('Toutes les hypothèses…sont donc vérifiée','Both scans have singular vérifiée. Current adds s to agree with Toutes les hypothèses; diplomatic preserves the typed singular.','End of first paragraph',370),
18:('Par ailleurs begins a new indented paragraph','The paragraph starts after the preceding sentence ending sur S. The attached break preserves the source.','Corollary proof',370),
19:('Passons begins a new indented paragraph','Both scans place the transition to part(b) in its own paragraph after the EGAII3.4 sentence. Retain the attached break.','Before Lemme1.5.1',370),
}
for k,(p,w,g,f) in obs.items():
 r.finding('366_370',k,p,w,g,witness=f+11,verdict='amended' if k==3 else 'not applied and now applied' if k in [4,11,12,17] else 'confirmed')
for p,old,new,id in [
 (365,'-Module module gradué','-Module gradué','check/findings/findings_361_365.json#36'),
 (365,'voir EGA II 8.12.1.','voir EGA II 8.12.1).','check/findings/findings_361_365.json#37'),
 (369,'noethériennnes','noethériennes','check/findings/findings_366_370.json#11'),
 (369,'dans le cas ou','dans le cas où','check/findings/findings_366_370.json#12'),
 (370,'sont donc vérifiée,','sont donc vérifiées,','check/findings/findings_366_370.json#17')]:
 why=next(x['reason'] for x in r.decisions if x['source_id']==id);r.patch(p,'current',old,new,id,why)
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':row.update(is_misprint=True,correction_status='accepted paired correction')

id='ASTRA-VI-BASE-SHEAF-369'
why=('The primary and native pages both print O_X with no zero. The same sentence defines X_0=P(E_0), the diagram gives g:X→X_0, and F=g^*(F_0). The printed component operation is g^*F_0=O_X tensor over g^{-1}O_{X_0} with g^{-1}F_0, using the ring map g-sharp:g^{-1}O_{X_0}→O_X. Thus the module supplied before this pullback is over O_{X_0}; adding only the zero restores the domain sheaf already specified by the displayed g. Diplomatic keeps O_X; current uses O_{X_0}.')
r.own_finding(id,369,'F_0 un O_X-Module',r'F_0 un \mathcal O_X-Module',r'Current O_{X_0}; diplomatic O_X.',why,'Sentence immediately below the Cartesian square',kind='misprint_in_print',witness=380)
r.own[-1].update(is_misprint=True,correction_status='accepted paired correction')
r.patch(369,'current',r'soit \(F_0\) un \(\mathcal O_X\)-Module',r'soit \(F_0\) un \(\mathcal O_{X_0}\)-Module',id,why)

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,x['source_id']);t=t.replace(x['old'],x['new'])
 return t

# The native300dpi crop of(1.2.1) establishes this one unruled target.
id='ASTRA-VI-TARGET-RULE-366'
why=('Both images, including the native300dpi enlarged display, leave the target M unruled although the source M_n and the later M_k carry their own rules. The map is explicitly x tensor a↦a.x, with x∈M_n and a∈B_{k-n}, landing in M_k. These component maps assemble in the very same graded sheaf M already fixed in1.2. Current restores its letter rule; diplomatic retains the exact isolated omission. No module, grading or morphism is replaced.')
r.own_finding(id,366,'M_n tensor B(-n)→M, with the target M plain',r'Plain target M',r'Diplomatic plain M; current ruled M.',why,'Display(1.2.1), final M',kind='misprint_in_print',witness=377)
r.own[-1].update(is_misprint=True,correction_status='accepted paired notation correction')

math_pattern=re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]|\\begin\{equation\}.*?\\end\{equation\}',re.S)
def letter_rules(t,letters,keep_target=False):
 counts={}
 def change(m):
  s=m[0]
  if keep_target:s=s.replace(r'\longrightarrow M,',r'\longrightarrow \SGAKeepTarget,')
  for c in letters:
   pat=rf'(?<![A-Za-z\\]){c}(?![A-Za-z])';s,n=re.subn(pat,lambda _:r'\underline{'+c+'}',s);counts[c]=counts.get(c,0)+n
  s=s.replace(r'\SGAKeepTarget','M');return s
 return math_pattern.sub(change,t),counts

for p in range(365,371):
 id=f'ASTRA-VI-GLYPHS-{p}'
 why='Restore only the individually observed ordinary-letter rules. Arguments, exponents and subscripts retain their exact original positions. The source O has a typed ordinary contour and a lower rule; The symmetric-algebra S retains the explicit NOTE_6 transport. Projective P occurrences are separately adjudicated in amend_projective_p.py; that exception was not stated in NOTE6.'
 if p==366:why+=' The one plain display target M is preserved in diplomatic and linked to its separately recorded same-sheaf correction.'
 if p==370:why+=' The ring-case letters and all tilded letters from Lemme1.5.1 onward remain plain as directly observed.'
 r.own_finding(id,p,'Observed single lower rules on the specified sheaf letters',r'Plain E,F,M,L,N or B,M,N,P,Q; mathcal O','Restore the exact observed rules.',why,'Complete page; occurrence-specific mathematical spans',kind='font',witness=p+11)
 counts=None
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old.replace(r'\mathcal O',r'\underline{O}')
  if p==370:
   n=new.index(r'\textbf{Lemme 1.5.1.}');head,c=letter_rules(new[:n],'EFM');new=head+new[n:]
  else:new,c=letter_rules(new,'EFLMN' if p==365 else 'BMNPQ' if p==366 else 'BM' if p==367 else 'EFM',keep_target=p==366)
  assert new!=old;r.patch(p,layer,old,new,id,why);counts=c
 r.own[-1]['observed_rule_counts']=dict(counts,ordinary_O=old.count(r'\mathcal O'))

target_reason=next(x['reason'] for x in r.own if x['source_id']=='ASTRA-VI-TARGET-RULE-366')
r.patch(366,'current',r'\longrightarrow M,',r'\longrightarrow \underline{M},','ASTRA-VI-TARGET-RULE-366',target_reason)

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
phrases={
365:['Soient','un schéma quasi-compact','un','-Module localement libre de rang','le fibré projectif associé','le morphisme structural','définit un homomorphisme d\'anneaux','munissant',"d'une structure de",'algèbre','Soit','la classe du faisceau','Alors','est un','module libre admettant pour base'],
367:['Les entiers','intervenant dans la décomposition','ne dépendent pas de la décomposition choisie'],
368:['Soient','un schéma quasi-compact','un','-Module localement libre de type fini','le fibré projectif associé','Soit','-Module de présentation finie','plat sur','Il existe un entier','tel que pour','on ait'],
370:['Avec les hypothèses de','il existe un','-Module gradué','de présentation finie','et plat sur','tel que'],
}
for p in [365,367,368,370]:
 id=f'ASTRA-VI-WORD-RULES-{p}';why='Both complete images establish these upright prose rules. The patch maps each inspected word group to its ruled rendering, while keeping every word, variable and formula in its original order.'
 r.own_finding(id,p,'Explicit statement word-group rules','Plain statement prose','Restore the observed rules.',why,'Statements on this page',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old
  start={365:r'\textbf{Théorème 1.1.}',367:r'\textbf{Proposition 1.2.3.}',368:r'\textbf{Proposition 1.3.}',370:r'\textbf{Corollaire 1.4.}'}[p]
  end={365:r'\textbf{Plan de la démonstration :}',367:'Supposons données',368:r'\[',370:r'Soit \(n_0\)'}[p]
  a=new.index(start)+len(start);b=new.index(end,a);new=new[:a]+rules(new[a:b],phrases[p])+new[b:]
  if p==365:new=new.replace(r'\textbf{Plan de la démonstration :}',r'\uline{Plan de la démonstration} :')
  if p==368:
   for a,b in [(r'\text{pour }',r'\text{\uline{pour} }'),(r'\text{ est localement libre de type fini sur }',r'\text{ \uline{est localement libre de type fini sur} }'),(r'\text{ est un }',r'\text{ \uline{est un} }'),(r'\text{-Module gradué de présentation finie (1.2).}',r'\text{\uline{-Module gradué de présentation finie} (1.2).}')]:
    assert new.count(a)==1;new=new.replace(a,b)
  if p==370:
   a=new.index(r'\textbf{Lemme 1.5.1.}')+len(r'\textbf{Lemme 1.5.1.}');b=new.index(r'Comme \(M\)',a)
   groups=['Soient','un anneau','une','algèbre graduée à degrés positifs','telle que','un','module gradué','On suppose que','est projectif de type fini','en tant que','module non gradué',"le faisceau d'algèbres sur",'défini par','le','Module associé à','alors','est localement sur','libre de type fini sur','comme','Module gradué']
   new=new[:a]+rules(new[a:b],groups)+new[b:]
  assert new!=old;r.patch(p,layer,old,new,id,why)

id='ASTRA-VI-PARAGRAPH-NUMBERS-366';why='The complete source and witness print1.2,1.2.1 and1.2.2 with the same ordinary type weight as the surrounding prose. Restore that observed weight; theorem labels retain the separately accepted NOTE_6 treatment.'
r.own_finding(id,366,'Ordinary paragraph numbers1.2,1.2.1,1.2.2','Bold subsection/paragraph commands','Render the three paragraph numbers in ordinary weight.',why,'Three numbered paragraph openings',kind='font',witness=377)
for old,new in [(r'\subsection*{1.2.}','1.2.'),(r'\textbf{1.2.1.}','1.2.1.'),(r'\textbf{1.2.2.}','1.2.2.')]:r.patch(366,'both',old,new,id,why)

boundaries={365:('Exposé VI and the two-line title','les N_j étant localement libres de type fini sur S.'),366:('2°)1,...,xi^(r+1)','pour un certain entier k.'),367:('Soit M un B-Module gradué libre de type fini.','d’où le résultat.'),368:('Il résulte en particulier de1.2.3','direct sum n≥n_1 of M-prime_n,'),369:('donc tel que','il existe un indice lambda-prime≥lambda'),370:('et un faisceau F_lambda-prime','libre de type fini sur B-tilde, cqfd.')}
for p,(a,b) in boundaries.items():r.page(p,a,b,notes='Complete primary and native pages read, including all formulas, word groups, punctuation and lower blank portion. Folios365/366 and369/370 boundary movements confirmed. Native enlarged crops resolve366 target M and368 weak G.',witness=p+11)
r.commit()
