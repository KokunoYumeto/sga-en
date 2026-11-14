#!/usr/bin/env python3
"""Complete IX503–505 plus the now fully seen501–504 raised-dot finding."""
from pathlib import Path
import re,shutil
from review_helpers import Review,base_text
r=Review();batch='501_505'
obs={
4:('Eleven filled raised K dots:501 two,503 four,504 five','All three complete primary/native image pairs have now been personally compared. Every listed K has a filled raised dot. Restore that dot, retaining the lower-dot coherent groups. The source comparison sends a locally-free sheaf class[E] to its coherent class[E]; the action on coherent F is[E]·[F]=[E tensor F]. This is the explicit morphism connecting the two source positions. The two501 occurrences were already restored under ASTRA-IX-RAISED-K-501.','All raised K occurrences501,503,504',501),
9:('No punctuation after the projective-limit display','Both complete503 images show no final comma after Spec(A_f). Retain the attached omission.','First display',503),
10:('Separate statement word-group rules','The complete primary/native503–505 images show the individual rules under Corollaries1.3–1.4 and Proposition1.6. Restore those exact prose groups. In504 the continuous phrase On suppose que pour tout point s de includes the point letter s in its rule; that single occurrence receives its observed rule as emphasis. The statement formula letters elsewhere remain independently as read.','Statements1.3,1.4,1.6',503),
11:('504 ends si on suppose f;505 begins de présentation finie).','Both complete504/505 source pairs confirm the boundary before de. Retain the attached marker with no added paragraph break.','Boundary504/505',505),
12:('Three singly ruled E letters and four singly ruled O letters','Both complete505 images show all three E letters and the four structure-sheaf O letters with a separate lower rule. Restore each letter’s rule with indices outside. Identity on the same locally free E and on each sheaf of regular functions gives the notation comparison; no sheaf or stalk is replaced.','Proposition1.6 and proof; regular-local-ring discussion',505),
}
for k,(p,w,g,f) in obs.items():r.finding(batch,k,p,w,g,witness=f+11,actual_page=f,verdict='not applied and now applied' if k in [4,10,12] else 'confirmed')

id='ASTRA-IX-NONZERO-LOCALIZATION-503'
why='Both complete503 images explicitly say f parcourt l’ensemble des éléments de A. On502 the source made A integral and K its fraction field. Including f=0 gives A_0=0; every A_f maps to this terminal localization, so the all-element colimit is0. For A=Z this contradicts the named Q, and no unital map0→Q can be a fraction-field cocone because1_Q≠0_Q. Over nonzero f, the map colim A_f→Frac(A) sends a/f^n to the same fraction. Its inverse sends a/b to its image from A_b; equality a/b=c/d becomes ad=bc in the common localization A_(bd), proving well-definedness and both inverse identities. The generic point(0) belongs to D(f) exactly for f≠0, matching the following nonempty U=Spec(A_f). Current inserts only non nuls; diplomatic retains the printed domain. The independent context audit and exact maps are in localization_index_503.json.'
r.own_finding(id,503,'l’ensemble des éléments de A','Same unrestricted domain','Current-only insertion non nuls; keep the source domain diplomatically.',why,'Opening fraction-field localization limit',kind='misprint_in_print',witness=514)
r.own[-1].update(is_misprint=True,correction_status='accepted paired localization-domain correction',proof_file='review/expose_ix/localization_index_503.json')
r.patch(503,'current',"l'ensemble des éléments de $A$","l'ensemble des éléments non nuls de $A$",id,why)
shutil.copyfile(Path(__file__).parents[1]/'english/EN_INDEPENDENT_IX_LOCALIZATION_AUDIT_503.json',Path(__file__).parent/'localization_index_503.json')
for p,n in [(503,4),(504,5)]:
 id=f'ASTRA-IX-RAISED-K-{p}';why=obs[4][1]
 r.own_finding(id,p,f'{n} filled raised K dots',r'K^\circ','Restore the raised bullet in both forms.',why,'Raised K dots',kind='symbol',witness=p+11)
 r.patch(p,'both',r'K^\circ',r'K^{\bullet}',id,why,count=n)
id='ASTRA-IX-GLYPHS-505';why=obs[12][1]
r.own_finding(id,505,'Three ruled E and four ruled O','Plain E; mathcal O','Restore each observed rule.',why,'Sheaf and stalk letters',kind='font',witness=516)
r.patch(505,'both','$E$',r'$\underline{E}$',id,why,count=3)
r.patch(505,'both',r'\mathcal O',r'\underline{O}',id,why,count=4)
r.own[-1]['observed_rule_counts']={'E':3,'O':4}

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,layer,x['source_id']);t=t.replace(x['old'],x['new'])
 return t
def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
for p,label in [(503,'Corollaire 1.3.'),(504,'Corollaire 1.4.'),(505,'Proposition 1.6.')]:
 id=f'ASTRA-IX-WORD-RULES-{p}';why=obs[10][1]
 r.own_finding(id,p,'Individually ruled statement groups','Plain statement prose','Restore the observed groups and the one ruled point s on504.',why,'Statement prose',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old;a=s.index(r'\textbf{'+label+'}')+len(r'\textbf{'+label+'}')
  b=len(s) if p==503 else s.index('On prend pour famille',a) if p==504 else s.index('Comme $f$ est lisse',a)
  part=s[a:b]
  if p==503:phrases=['Soit','un morphisme plat de schémas noethériens','On suppose que pour tout point','de',"l'homomorphisme",'est surjectif',"Alors l'homomorphisme déduit de"]
  elif p==504:
   assert part.count('point $s$ de')==1;part=part.replace('point $s$ de',r'point $\underline{s}$ de')
   phrases=['Soit','un morphisme plat de schémas noethériens','On suppose que pour tout point','de',"l'homomorphisme canonique",'est un isomorphisme',"Alors l'homomorphisme",'est surjectif','Si de plus','possède une section','de tor-dimension finie','alors']
  else:phrases=['Soient','un schéma noethérien','un','-Module localement libre de type fini','le fibré vectoriel associé à','et','le morphisme structural de','Alors','est un isomorphisme']
  s=s[:a]+rules(part,phrases)+s[b:];assert s!=old;r.patch(p,layer,old,s,id,why)

id='ASTRA-IX-LOCAL-NOTATION-503-505'
why='All complete primary/native503–505 images were compared.503 keeps the field K plain and the coherent-group K with a lower dot; its two typed products xi_i·n_i retain the explicit cdot transport for the additive integer action.504 and505 each have a visibly struck coefficient Z; mathbb Z retains it. The integer comparison sends n to n[O], the very canonical map named in1.4. The capital Id in504 and the headless wavy-over-straight isomorphism505 agree with the attached commands. Retain these occurrence-specific forms.'
r.own_finding(id,503,'Plain field K; lower coherent-group dots; struck Z504–505; capital Id504','Same forms','Retain those observed forms.',why,'Local field, group and coefficient notation503–505',kind='font',verdict='confirmed',witness=514)
r.own[-1].update(is_misprint=False,source_pages=[503,504,505])
for p,a,b in [(503,'Par ailleurs,on a K=lim_f A_f','est surjectif.'),(504,'On prend pour famille(xi_i)_(i∈I)','si on suppose f'),(505,'de présentation finie).','La proposition résulte alors du lemme suivant:')]:
 r.page(p,a,b,notes='Both complete primary/native pages personally compared. This closes every occurrence of aggregate finding501_505#4. The503 localization-domain repair has an independent exact audit.',witness=p+11)
r.commit()
