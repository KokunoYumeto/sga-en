#!/usr/bin/env python3
"""Explicit full-image comparison401–405 and the three406 boundary aliases."""
import re
from review_helpers import Review,base_text
r=Review();batch='401_405'
obs={
1:('G with two lower rules','Both complete401 images show two rules under the first G. Diplomatic restores those rules; current retains bold G. The two renderings represent the same rank-n quotient functor by the identity on every quotient and every base-change map.','Opening Grassmannian display',401),
2:('G with two lower rules','Both complete401 images show two rules under the infinite Grassmannian G. Diplomatic restores the literal rules, current retains bold G; the comparison is the identity at every finite quotient stage and hence on their displayed inverse system.','First paragraph, infinite Grassmannian',401),
3:('Three baseline stops','Both complete401 images show three low stops in the gamma-series polynomial. Retain the attached ldots.','Gamma-series display',401),
4:('Plain5.1. with a terminal stop','Both complete401 images show this ordinary-weight paragraph number and its stop. Retain the stop and restore the plain number.','Paragraph5.1',401),
5:('Occurrence-specific module rules on401,402,404','All five complete primary/native pairs were personally compared. On401 E is ruled three times, F once and O twice. On402 the sheaf inputs E,F in the class sentence and G twice are ruled, with two ruled O; the class outputs E,F,xi and the E in lambda^i(E) remain plain. On404 the six E occurrences in5.5 and its O are ruled. The comparison is the explicitly printed class map (E,F,O_X(1))↦([E],[F],[O_X(1)]); the plain classes in403–405 stay plain.','All module/class occurrences401–405',401),
6:('402 begins with f étant le morphisme structural','The complete401 page ends after the exact sequence and its comma; both complete402 images begin with f. Retain the attached marker before f.','Boundary401/402',402),
7:('The congruence is inline and has no final stop','Both complete402 images place the whole congruence inline and end with the barred equality without a final period. The independently adjudicated replay10 has already restored this exact placement. Retain that placement, with the separately decided current sign and duplicated-stop repairs.','First paragraph, final line',402),
8:('i.e..','Both complete402 images show two consecutive full stops after the e. The abbreviation is already complete at i.e.; current removes only the immediately duplicated final stop, and diplomatic retains both.','First paragraph, final line',402),
9:("bar x-prime = minus bar x",'Both complete402 images show the minus. Under the quotient map q:Fil^1K(X)→Fil^1K(X)/Fil^2K(X), x-prime−x=(xi−1)x belongs to Fil^2, so q(x-prime)=q(x). This supplies the precise comparison behind the existing current removal of the minus. For S=Spec(k),X=P^1, x=1−[O(−1)] has Euler characteristic1 and x^2=0, so its degree-one class has infinite order; the printed negative equality fails there.','First paragraph, barred equality',402),
10:('Plain5.2. with a terminal stop','Both complete402 images show ordinary weight and the terminal stop. Retain the stop and restore the plain paragraph number.','Paragraph5.2',402),
11:('Three baseline stops in5.2.1','Both complete402 images show low stops in the projective-bundle expansion. Retain ldots.','Formula5.2.1',402),
12:('New paragraph at Il est clair','Both complete402 images indent this paragraph after5.2.2. Retain the attached paragraph break.','After formula5.2.2',402),
13:('New paragraph at On vérifie','Both complete402 images indent this sentence after K(S)-linéaire. Retain the attached paragraph break.','Before formula5.2.3',402),
14:('New paragraph at Pour vérifier','Both complete402 images indent this sentence after5.2.3. Retain the attached paragraph break.','Induction paragraph',402),
15:('403 begins at the complete sum display','Both complete402/403 pairs put On peut lui appliquer f_*: at the end of402, and the full displayed sum at the beginning of403. Retain the marker before the display.','Boundary402/403',403),
16:('No equation number beside the filtration decomposition','Both complete403 images show an empty left margin beside this display. Retain the attached suppression of the invented5.3.1 number.','Proposition5.3 first display',403),
17:('Raised dots on the first two K symbols','Both complete403 images show raised dots matching the remaining K symbols in the display. Retain K^bullet in each place.','Proposition5.3 first display',403),
18:('Three baseline stops in the filtration sum','Both complete403 images show the low typed stops. Retain ldots.','Proposition5.3 first display',403),
19:('Raised dot on K in Fil^nK(S)','Both complete403 images show the raised dot, matching the other K symbols of the same sum. Retain K^bullet.','Membership display for x^n',403),
20:('Three baseline stops in the membership sum','Both complete403 images show the low typed stops. Retain ldots.','Membership display for x^n',403),
21:('New paragraph at C’est évident','Both complete403 images indent the new induction paragraph. Retain the attached paragraph break.','After membership display',403),
22:('hypothèses de4.1','Both complete403 images print4.1. The exact data used in the statement are f:P(E)→S, rank(E)=r+1 and x=1−[O(−1)], defined in5.1–5.2. The specialization of the general flag construction to its rank-one quotient gives this same projective bundle and class map, so the displayed decomposition is on precisely the object of5.1. Current retains5.1; diplomatic retains4.1.','Proposition5.3 opening',403),
23:('Individually observed statement word rules','All complete403–405 primary/native images were personally read. Restore only the observed word groups in5.3–5.9 and the continued5.7 sentence. Formula letters, reference numbers, punctuation and separating hyphens stay outside those rules. The ruled module letters are handled independently.','Statement prose403–405',403),
24:('First D on404 has two lower rules','Both complete404 images show two rules on D(E_i). Diplomatic restores both rules, current retains bold D. Both denote the identical complete-flag functor, with identity comparison on each flag and its pullbacks.','Corollaire5.5 first D',404),
25:('E_i in both occurrences','Both complete404 images show the short dotted index i in D(E_i) and the following E_i; the endpoint indices1,n are taller and separately legible in the same sentence. Retain the attached i in both places, adding the observed E rules separately.','Corollaire5.5 middle pair',404),
26:('First product D has two lower rules','Both complete404 images show two lower rules on the first D in the product. Diplomatic restores them; current retains bold D with the identical flag functor.','Corollaire5.5 product, first factor',404),
27:('Last product D has two lower rules','Both complete404 images show two lower rules on the final D in the product. Diplomatic restores them; current retains bold D with the identical flag functor.','Corollaire5.5 product, last factor',404),
28:('Three baseline stops between product factors','Both complete404 images show the low stops; retain ldots and the NOTE6 product-sign transport.','Corollaire5.5 product',404),
29:('Raised dots on the first two K symbols','Both complete404 images show raised dots on those K symbols. Retain K^bullet at both positions.','Corollaire5.6 graded display',404),
30:('Three baseline stops between direct summands','Both complete404 images show low stops. Retain ldots.','Corollaire5.6 graded display',404),
31:('Raised dot on K in Gr^iK(X)','Both complete404 images show the raised dot. Retain K^bullet.','Corollaire5.7 class sentence',404),
32:('Exp4 with no abbreviation stop','Both complete405 images print Exp4 with a space and no abbreviation stop. This is an unambiguous abbreviated locator for exposé4 of reference[2]: the expansion map Exp4↦Exposé4 gives exactly the same cited section as Exp.4. The stop does not repair a broken locator or alter its meaning; retain the author citation style in both layers rather than treating its expansion style as a source misprint.','Comparison citation before5.8',405),
33:('Raised dot on K in Fil^kK(X)','Both complete405 images show the raised dot. Retain K^bullet.','Corollaire5.8 display',405),
34:('New paragraph at Conséquence immédiate','Both complete405 images indent this proof sentence after the display. Retain the attached break.','After Corollaire5.8 display',405),
35:('New paragraph at On définit','Both complete405 images indent this sentence after f_*(lambda_-1(F))=1. Retain the attached break.','Definition of the coefficientwise series map',405),
36:('405 ends on déduit donc:;406 begins with the complete barred-f display','Both complete405/406 primary/native pairs were read. Retain the marker immediately before the opening display delimiter on406. The nominal405 findings37–39 are explicitly assigned to their actual source page406.','Boundary405/406',405),
37:('First barred f has no lower star','Both complete406 images show an empty subscript position under the first barred f. The map defined on405 is the coefficientwise extension sum a_it^i↦sum f_*(a_i)t^i; applying it to lambda_t(F) produces exactly the next two equal terms by the projection formula. Current restores its lower star; diplomatic retains the omitted star.','406 first display',406),
38:('Barred f in the Or sentence has no lower star','Both complete406 images show this second omission. The explicitly displayed coefficient formula sum(−1)^i f_*(xi^i)t^i is the value of the same coefficientwise map bar f_* on lambda_t(−xi). Current restores the star; diplomatic retains the printed omission.','406 second line',406),
39:('d’après4.2.3','Both complete406 images print4.2.3. Formula5.2.3 on the personally read402 gives f_*(xi^i)=sigma_i for i≥1 and f_*(1)=1. Applying these equalities coefficient by coefficient sends sum(−1)^i f_*(xi^i)t^i to sigma_-t(E), exactly the equality cited here. Current retains the reference5.2.3; diplomatic keeps4.2.3.','406 second line, reference',406),
}
for k,(p,w,g,f) in obs.items():
 verdict='reverted' if k==32 else 'amended' if k in [1,2,4,5,10,24,26,27] else 'not applied and now applied' if k in [8,23] else 'confirmed'
 r.finding(batch,k,p,w,g,witness=f+11,actual_page=f,verdict=verdict)
for row in r.decisions:
 key=row.get('related_finding',row['source_id'])
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':
  row.update(is_misprint=key!=f'check/findings/findings_{batch}.json#32',correction_status='Author citation style retained' if key==f'check/findings/findings_{batch}.json#32' else 'accepted paired correction')
 if key==f'check/findings/findings_{batch}.json#32' and row['type']=='fixlog':
  row.update(verdict='confirmed',change='Retain the diplomatic removal of the added abbreviation stop; restore the same source style in current.')
for n,k in [(428,9),(429,22),(430,37),(431,38),(432,39)]:
 p,w,g,f=obs[k]
 r.source(f'fixes/FIXLOG_6_CURRENT.jsonl#{n}',p,w,g,page=f,witness=f+11,change='Retain the paired current correction.')
 r.decisions[-1].update(is_misprint=True,correction_status='accepted paired correction')
r.patch(402,'current','i.e..','i.e.',f'check/findings/findings_{batch}.json#8',obs[8][1])
r.patch(405,'current','Exp. 4','Exp 4',f'check/findings/findings_{batch}.json#32',obs[32][1])

id='ASTRA-VI-GAMMA-SUBSTITUTION-403'
why='Both complete403 images print lambda_(t/1−t), without denominator parentheses. The next two explicit fractions have denominator1−t. In A[[t]], the continuous substitution rho(t)=t/(1−t) is inverse to eta(t)=t/(1+t): direct substitution gives rho(eta(t))=eta(rho(t))=t. Applying rho coefficientwise to lambda_u(1−xi^-1)=(1+u)/(1+xi^-1 u) gives1/(1−xt), x=1−xi^-1, exactly the rest of the displayed equation. Current adds only the denominator parentheses; diplomatic keeps the source slash string. The literal arithmetic parse t/1−t=0 would give1; on P^1 the printed final expression is1+xt with chi(x)=1, so that parse fails. This is a specified formal substitution, not an unsupported rewriting of notation.'
r.own_finding(id,403,r'\lambda_{t/1-t}',r'\lambda_{t/1-t}',r'Diplomatic unchanged; current \lambda_{t/(1-t)}',why,'Gamma-series calculation',kind='misprint_in_print',witness=414)
r.own[-1].update(is_misprint=True,correction_status='accepted paired denominator delimiters')
r.patch(403,'current',r'\lambda_{t/1-t}',r'\lambda_{t/(1-t)}',id,why)

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,layer,x['source_id']);t=t.replace(x['old'],x['new'])
 return t
for p in [401,402,404]:
 id=f'ASTRA-VI-GLYPHS-{p}';why=obs[5][1]
 r.own_finding(id,p,'Single rules on the individually specified module letters','Plain module letters and script O','Restore the observed rules, leaving classes plain.',why,'Module/class notation',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old.replace(r'\mathcal O',r'\underline{O}')
  if p==401:
   pairs=[('$E$ un',r'$\underline{E}$ un'),('associé à $E$',r'associé à $\underline{E}$'),(r'\longrightarrow F\longrightarrow f^*(E)',r'\longrightarrow \underline{F}\longrightarrow f^*(\underline{E})')]
  elif p==402:
   pairs=[('les classes de $E$, $F$,',r'les classes de $\underline{E}$, $\underline{F}$,'),('Si $G$ est',r'Si $\underline{G}$ est'),(r'R^if_*(G)',r'R^if_*(\underline{G})')]
  else:
   pairs=[]
   a=s.index(r'\textbf{Corollaire 5.5.}');b=s.index('Le raisonnement',a)
   part,n=re.subn(r'(?<![A-Za-z\\])E_',lambda _:r'\underline{E}_',s[a:b]);assert n==6,n
   s=s[:a]+part+s[b:]
  for a,b in pairs:assert s.count(a)==1,(p,a);s=s.replace(a,b)
  assert s!=old;r.patch(p,layer,old,s,id,why)
 r.own[-1]['observed_rule_counts']={401:{'E':3,'F':1,'O':2},402:{'E':1,'F':1,'G':2,'O':2},404:{'E':6,'O':1}}[p]
for p,c,n in [(401,'G',2),(404,'D',3)]:
 id=f'ASTRA-VI-DOUBLE-OPERATORS-{p}';why=obs[1 if p==401 else 24][1]
 r.own_finding(id,p,f'{n} {c} operators with two lower rules',r'\mathbf '+c,'Literal two rules diplomatic; bold operator current.',why,'All flag/Grassmannian operators',kind='font',witness=p+11)
 r.patch(p,'diplomatic',r'\mathbf '+c,r'\underline{\underline{'+c+'}}',id,why,count=n)
for p,num in [(401,'5.1.'),(402,'5.2.')]:
 id=f'ASTRA-VI-PARAGRAPH-NUMBER-{p}';why=obs[4 if p==401 else 10][1]
 r.own_finding(id,p,num,r'\subsection*{'+num+'}',num,why,'Paragraph number',kind='font',witness=p+11)
 r.patch(p,'both',r'\subsection*{'+num+'}',num,id,why)

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
for p in [403,404,405]:
 id=f'ASTRA-VI-WORD-RULES-{p}';why=obs[23][1]
 r.own_finding(id,p,'Separately inspected statement word groups','Statement prose left plain','Restore the observed word rules.',why,'Statements and their continuations',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old
  if p==403:
   a=s.index(r'\textbf{Proposition 5.3.}')+len(r'\textbf{Proposition 5.3.}');b=s.index('On remarque',a)
   s=s[:a]+rules(s[a:b],['Avec les notations et les hypothèses de','on a pour','tout','une décomposition en somme directe de','modules','la filtration considérée étant la filtration de','algèbre augmentée définie','en','et'])+s[b:]
  elif p==404:
   spans=[('Corollaire 5.4.','Corollaire 5.5.',['La filtration induite par','sur','est identique à la filtration de']),
    ('Corollaire 5.5.','Le raisonnement',['Soient','un schéma quasi','compact','des','Modules','localement libres de type fini','le schéma de drapeaux de',"Alors l'homomorphisme canonique",'est injectif']),
    ('Corollaire 5.6.','Conséquence immédiate',['Avec les notations et les hypothèses de','est un','module libre','admettant pour base','Pour tout','on a','Enfin','les éléments','sont liés par la relation','où','est la','ième classe de Chern de']),
    ('Corollaire 5.7.',None,['Avec les notations et les hypothèses de','la','algèbre','est engendrée par les','où','est la classe dans','de',"L'idéal des relations entre les",'est engendré par les relations déduites de'])]
   for start,end,phrases in spans:
    a=s.index(r'\textbf{'+start+'}')+len(r'\textbf{'+start+'}')
    b=len(s) if end is None else s.index(r'\textbf{'+end+'}',a) if end.startswith('Corollaire') else s.index(end,a)
    s=s[:a]+rules(s[a:b],phrases)+s[b:]
  else:
   a=s.index('\n')+1;b=s.index('Ce résultat',a)
   s=s[:a]+rules(s[a:b],['où','est la classe de Chern totale'])+s[b:]
   for start,end in [('Corollaire 5.8.','Conséquence immédiate'),('Proposition 5.9.','On définit')]:
    a=s.index(r'\textbf{'+start+'}')+len(r'\textbf{'+start+'}');b=s.index(end,a)
    s=s[:a]+rules(s[a:b],['Avec les notations et les hypothèses de','on a pour','tout','En particulier','si on pose','on obtient'])+s[b:]
  assert s!=old;r.patch(p,layer,old,s,id,why)

id='ASTRA-VI-AUTHOR-SPELLINGS-401'
why='Both complete401 images show four occurrences of polynome without a circumflex and entrainera without a circumflex. The same polynomial expressions and the identity homomorphism on their coefficient ring identify each named object exactly. Retain the author’s repeated spellings in both forms; no silent orthographic normalization is introduced.'
r.own_finding(id,401,'polynome four times; entrainera','Same source spellings','Retain both layers unchanged.',why,'Completion proof',kind='word',verdict='confirmed',witness=412)
r.own[-1].update(is_misprint=False,correction_status='Author spellings retained')
for p,a,b in [(401,'K^bullet(G_S^(n,r))=','0→F→f^*E→O_X(1)→0,'),(402,'f étant le morphisme structural','On peut lui appliquer f_*:'),(403,'sum_(i=0)^(r+1)(−1)^i lambda^i(E)f_*(xi^(n−i))=0.','sur K^bullet(S).'),(404,'Corollaire5.4.','c(E−n)=product c(F_j−p_j),'),(405,'où c est la classe de Chern totale','De la relation E=F+xi, on déduit donc:')]:
 r.page(p,a,b,notes='Both complete primary/native pages personally read. Complete406 primary/native images additionally verify the boundary and the nominal405 aliases37–39. Source class maps and formal substitutions are recorded explicitly.',witness=p+11)
r.commit()
