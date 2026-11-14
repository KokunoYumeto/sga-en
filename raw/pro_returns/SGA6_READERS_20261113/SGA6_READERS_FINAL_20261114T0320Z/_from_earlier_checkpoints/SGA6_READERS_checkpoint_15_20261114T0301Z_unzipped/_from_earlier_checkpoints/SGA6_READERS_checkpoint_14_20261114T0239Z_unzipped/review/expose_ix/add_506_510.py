#!/usr/bin/env python3
"""Personally compared IX506–510, including complete primary and native images."""
import re
from review_helpers import Review,base_text
r=Review();batch='506_510'
obs={
1:('Struck R in the derived direct image','Both complete506 images show the separately struck R. Retain mathbb R for the same derived functor Rg_*; the displayed comparison Rg_*F→g_*F is the degree-zero identification for the closed immersion g.','Proof1.8, derived direct image',506),
2:('Struck L in the derived inverse image','Both complete506 images show the struck L. Retain mathbb L for the same derived inverse-image functor Lg^*. Its Koszul-complex realization is displayed on507.','Last line',506),
3:('Struck L above tensor','Both complete506 images show the struck superscript L. Retain the attached mathbb L; the comparison is the identical derived tensor F tensor^L_(O_X) O_S, computed by the displayed Koszul resolution on507.','Last derived tensor',506),
4:('g^*(g_*(f)), with a small f','Both complete506 images print the lower-case f. The preceding sentence names the coherent class F and the507 calculation begins g^*(g_*(F)). The exact composite on that class is [F]↦[g_*F]↦sum_i(-1)^i[Tor_i^(O_X)(g_*F,O_S)]=[F]·lambda_-1(E). The structural morphism f:X→S has no element in this composite’s K-group domain. Keep the source lower-case f diplomatically and the existing current F correction.','Proof1.8, last paragraph',506),
5:('New paragraph at Soit F','Both complete506 images show the indentation and separate paragraph after VII2.7. Retain the attached paragraph break.','After Cet énoncé',506),
6:('507 begins with a separate Pour cela paragraph','The complete506/507 primary/native pairs show the break before Pour cela, with the506 final full stop. Retain the paragraph break and page boundary.','Boundary506/507',506),
7:('26 raised filled K dots across506–510','Every complete primary/native pair506–510 was compared:4 raised dots506,2 on507,1 on508,5 on509,14 on510. Restore those filled raised dots in both forms. The comparison K^bullet→K_bullet sends a locally free sheaf class[E] to its coherent-sheaf class[E]; the displayed module action sends([E],[F]) to[E tensor F]. Those maps relate the two printed positions while preserving the lower dots.','All26 raised K occurrences',506),
8:('Individually ruled modules and algebras; class letters plain','All complete506–510 primary/native images show the listed single rules. Restore only the letter, leaving indices and primes outside:506 E3,F6,O6;507 E10,F5,L4,A9,O15;508 A4,L4;509 A9,O1;510 E7,F2,L3,O1. The plain E in507 sur S(E),507 wedge^k(f^*(E)), and510 complet D(E) is genuinely unruled in the native details. Retain these three local source forms in both layers. The identity on E, the inclusion E→Sym^1(E), pullback f^*E and the identity on its flag functor supply the exact comparisons; the class map E↦[E] governs the separate plain K-class occurrences.','All module/algebra occurrences',506),
9:('Separately underlined statement prose','The complete primary/native images506,508,509,510 show separate rules under the statement word groups in1.7,1.8,2.2,2.3,3.1. Restore those precise prose groups, preserving the independent formula readings.','Statements1.7,1.8,2.2,2.3,3.1',506),
10:('Struck S in the first Koszul term','Both complete507 images and the native full-resolution first-display detail show the vertical stroke through S. Retain mathbb S; the algebra is the same Sym(E)=direct sum Sym^n(E), with identity on every homogeneous term.','First Koszul term',507),
11:('Struck S in the second Koszul term','Both complete507 images and the native detail show the same vertical stroke. Retain mathbb S for the same graded symmetric algebra and its identity on each homogeneous term.','Second Koszul term',507),
12:('Typed baseline dots in the Koszul complex','Both complete507 images show the dots on the baseline. Retain ldots and the same successive Koszul maps.','First displayed complex',507),
13:('Two struck S letters in the final Koszul terms','Both complete507 images and the native detail show the struck S in both final terms. Retain the attached mathbb S, the identity notation transport of the same Sym(E).','Final Koszul terms',507),
14:('No punctuation after the final zero','Both complete507 images end the first complex at0. Retain the attached absence of a comma.','First displayed complex ending',507),
15:('Struck S in où S(E)','Both complete507 images and the native detail show the vertical stroke of S. Retain mathbb S for the same symmetric algebra.','Sentence after first complex',507),
16:('Struck S in sur S(E), with plain E','Both complete507 images and the native detail show a struck S and an unruled E at this occurrence. Retain both locally observed forms; the E→Sym^1(E) identification is unchanged.','C’est une résolution sentence',507),
17:('Struck L above the derived tensor','Both complete507 images and the native detail show the struck superscript L. Retain mathbb L and the displayed comparison from the Koszul resolution tensor F to O_S tensor^L_(O_X) F.','Before Par suite',507),
18:('Singly underlined G','Both complete507 images show exactly one lower rule on G. Retain underline G with the superscript and subscript outside the rule; the same group scheme represents R↦R^times at each component.','2.1 torus expression',507),
19:('Subscript m S, without comma','Both complete507 images show m and S with spacing and no comma. Retain the attached subscript.','2.1 torus expression',507),
20:('Four small exterior wedges507 and one510','Both complete507 and510 image pairs show a small wedge with its exponent above, rather than a capital Lambda. Restore wedge in both forms at precisely those five places. The comparison is identity on the exterior-power object, namely the quotient of the tensor power by the alternating relations; its element e_1 wedge…wedge e_i maps to itself.','Exterior powers507 and510',507),
21:('Plain G on508','Both complete508 images show the typed G without a rule or an added stroke. Retain this local form. It names the same multiplicative-group functor R↦R^times as the ruled occurrences507 and509, via the identity on every R-point.','First proof paragraph',508),
22:('Subscript m S, without comma','Both complete508 images show no comma in that subscript. Retain the attached spacing.','First proof paragraph',508),
23:('No punctuation after the first exact-sequence zero','Both complete508 images end the first sequence at0. The later sequence visibly has its comma. Retain those two distinct occurrence readings.','First exact sequence',508),
24:('No punctuation after the quotient display','Both complete508 images end the quotient display without a comma. Retain the attached omission.','Last display',508),
25:('Singly underlined G','Both complete509 images show one lower rule under G. Retain it, with m and P_1 outside. The group represents the same functor of units over P_1.','Torus over P_1',509),
26:('Subscript m P_1, without comma','Both complete509 images show m P_1 and no comma. Retain the attached subscript.','Torus over P_1',509),
27:('No punctuation after the corollary quotient','Both complete509 images end the corollary display without a comma. Retain its absence.','Corollary2.3 display',509),
28:('Struck D in D_pi(E)','Both complete510 images show the doubled upright stroke of D. Retain mathbb D in all five displayed or inline flag-scheme occurrences. The identity on flags of locally free quotients of pullback E is the exact notation comparison.','Proposition3.1',510),
29:('Struck D and plain E in complet D(E)','Both complete510 images and the native detail show struck D and unruled E in this phrase. Retain those local forms, with identity on the same complete-flag functor.','First injectivity paragraph',510),
30:('Two struck D letters in the injectivity display','Both complete510 images show the struck D twice; the E letters in these two arguments do carry their own single lower rules. Retain D and restore only those observed E rules.','Last display',510),
31:('Struck D in the final line','Both complete510 images show the struck D and singly ruled E. Retain D and restore E’s observed rule.','Last line',510),
32:('Second tensor factor K-raised-dot(S)','Both complete510 images print S in the second factor of the surjectivity display. The statement on this same page and Corollary1.3 identify the map with alpha:a tensor b↦f^*a·b for b in K^bullet(X), balanced over K^bullet(S). Restore that X only in current. For S=Spec(k), E=k^2 and X=P^1, the printed domain is Z tensor_Z Z=Z and its natural map has image Z[O]; the known projective-bundle basis1,delta with delta=[O(1)]−1 shows the missing generator. The corrected map is Z tensor_Z K^bullet(P^1)→K_bullet(P^1),1 tensor b↦b. Diplomatic retains S.','Surjectivity display after D’après1.3',510),
}
for k,(printed,why,region,p) in obs.items():
 r.finding(batch,k,printed,why,region,witness=p+11,actual_page=p,verdict='not applied and now applied' if k in [7,8,9,20] else 'confirmed')
for id,k in [('fixes/FIXLOG_6_CURRENT.jsonl#464',4),('fixes/FIXLOG_6_CURRENT.jsonl#465',32)]:
 printed,why,region,p=obs[k];r.source(id,printed,why,region,witness=p+11,page=p,change='Keep the source form diplomatically and the existing current-only correction.')
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint' or row['source_id'] in ['fixes/FIXLOG_6_CURRENT.jsonl#464','fixes/FIXLOG_6_CURRENT.jsonl#465']:
  row.update(is_misprint=True,correction_status='accepted paired correction with explicit source-domain comparison')

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,layer,x['source_id']);t=t.replace(x['old'],x['new'])
 return t

id='ASTRA-IX-RAISED-K-506-510';why=obs[7][1]
r.own_finding(id,506,obs[7][0],r'K^\circ','Restore the26 observed filled raised dots.',why,obs[7][2],kind='symbol',witness=517)
r.own[-1].update(source_pages=list(range(506,511)),observed_occurrences={506:4,507:2,508:1,509:5,510:14},is_misprint=False)
for p,n in [(506,4),(507,2),(508,1),(509,5),(510,14)]:r.patch(p,'both',r'K^\circ',r'K^{\bullet}',id,why,count=n)
id='ASTRA-IX-EXTERIOR-WEDGE-507-510';why=obs[20][1]
r.own_finding(id,507,obs[20][0],r'\Lambda','Restore the five small exterior wedges.',why,obs[20][2],kind='symbol',witness=518)
r.own[-1].update(source_pages=[507,510],is_misprint=False)
for p,n in [(507,4),(510,1)]:r.patch(p,'both',r'\Lambda',r'\wedge',id,why,count=n)

def select_rules(t,letter,ordinals,total):
 pattern=r'(?<![A-Za-z\\])'+letter+r'(?![A-Za-z])'
 ms=list(re.finditer(pattern,t));assert len(ms)==total,(letter,len(ms),total)
 for i,m in reversed(list(enumerate(ms,1))):
  if i in ordinals:t=t[:m.start()]+r'\underline{'+letter+'}'+t[m.end():]
 return t
for p in range(506,511):
 id=f'ASTRA-IX-GLYPHS-{p}';why=obs[8][1]
 r.own_finding(id,p,'Occurrence-specific single module/algebra rules','Plain module letters and mathcal O','Restore only the individually observed rules.',why,'Module/algebra notation',kind='font',witness=p+11)
 r.own[-1].update(is_misprint=False,observed_rule_counts={506:{'E':3,'F':6,'O':6},507:{'E':10,'F':5,'L':4,'A':9,'O':15},508:{'A':4,'L':4},509:{'A':9,'O':1},510:{'E':7,'F':2,'L':3,'O':1}}[p])
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old
  assert s.count(r'\mathcal O')=={506:6,507:15,508:0,509:1,510:1}[p]
  s=s.replace(r'\mathcal O',r'\underline{O}')
  if p==506:
   s=select_rules(s,'E',{1,2,5},7)
   for before,after in [(r'Soit $F$',r'Soit $\underline{F}$'),(r'\mathbb Rg_*(F)=g_*(F)',r'\mathbb Rg_*(\underline{F})=g_*(\underline{F})'),(r'donc de $F$',r'donc de $\underline{F}$'),(r'\mathbb Lg^*(F)=F\otimes',r'\mathbb Lg^*(\underline{F})=\underline{F}\otimes')]:
    assert s.count(before)==1,before;s=s.replace(before,after)
   assert s.count(r'\underline{F}')==6
  elif p==507:
   s=select_rules(s,'E',set(range(1,10))|{12},13);s=select_rules(s,'F',{1,2,4,5,6},7)
   assert s.count(r'L_\bullet')==3 and s.count('L_i')==1
   s=s.replace(r'L_\bullet',r'\underline{L}_\bullet').replace('L_i',r'\underline{L}_i')
   s=select_rules(s,'A',set(range(1,10)),9)
  elif p==508:
   s=select_rules(s,'A',{1,2,3,4},4);s=select_rules(s,'L',{1,2,3,7},9)
  elif p==509:s=select_rules(s,'A',set(range(1,10)),9)
  else:
   s=select_rules(s,'E',{1,2,3,4,6,7,8},8);s=select_rules(s,'F',{1,2},2);s=select_rules(s,'L',{1,2,3},3)
  assert s!=old;r.patch(p,layer,old,s,id,why)

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(x).replace(r'\ ',r'\s+') for x in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
blocks={
506:[('Lemme 1.7.','Comme $X$ est régulier',['Soient','un anneau principal',"Alors l'homomorphisme canonique",'est un isomorphisme']),('Proposition 1.8.','Cet énoncé',['Soient','un schéma noethérien','un','-Module localement libre de rang','le fibré vectoriel associé à','le morphisme structural de','et','la section nulle de',"Alors l'homomorphisme composé",'où',"est défini d'après","est la multiplication par l'élément",'de','en notant','la classe de','dans','et en posant'])],
508:[('Proposition 2.2.',"On suppose d'abord",['Avec les notations et les hypothèses de','soit','le morphisme structural de',"Alors l'homomorphisme",'est surjectif','et son noyau est le sous-groupe de','engendré par les sous-groupes','pour','ou','ce qui revient au même','parcourant un système de générateurs de'])],
509:[('Corollaire 2.3.','Si $S$ est régulier',['Avec les notations et les hypothèses de','supposons que','soit régulier','alors on a un isomorphisme canonique','où',"est l'idéal de",'engendré par les','pour','parcourant un système de générateurs de'])],
510:[('Proposition 3.1.','On reprend les notations',['Soient','un schéma noethérien','un','-Module localement libre de rang',"une suite d'entiers tels que",'et','le schéma des drapeaux de type','de',"Alors l'homomorphisme canonique",'est un isomorphisme'])],
}
for p,entries in blocks.items():
 id=f'ASTRA-IX-WORD-RULES-{p}';why=obs[9][1]
 r.own_finding(id,p,obs[9][0],'Plain statement prose','Restore the individual observed word groups.',why,'Statement prose',witness=p+11);r.own[-1]['is_misprint']=False
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old
  for label,end,phrases in entries:
   a=s.index(r'\textbf{'+label+'}')+len(r'\textbf{'+label+'}');b=s.index(end,a)
   s=s[:a]+rules(s[a:b],phrases)+s[b:]
  assert s!=old;r.patch(p,layer,old,s,id,why)
for p,title in [(507,'Fibrés principaux sous les tores déployés'),(510,'Fibrés projectifs et fibrés en drapeaux')]:
 id=f'ASTRA-IX-HEADING-{p}';why='Both complete primary/native images show one rule under the heading words. NOTE_6 explicitly accepts subsection headings without that rule; retain the attached heading command, with the identical word sequence. The507 paragraph number2.1 is plain in both source images and lies under the separate pending paragraph-number convention, so remove its added bold styling in both layers.'
 r.own_finding(id,p,'Single heading word rule;507 paragraph2.1 plain','Accepted subsection heading;507 bold2.1','Retain the accepted heading command; restore only the507 plain paragraph numeral.',why,'Section heading and paragraph numeral',kind='font',witness=p+11);r.own[-1]['is_misprint']=False
 if p==507:r.patch(p,'both',r'\textbf{2.1.}','2.1.',id,why)
id='ASTRA-IX-PLAIN-E-507-510'
r.own_finding(id,507,'Plain E in sur S(E),wedge^k(f^*E),and complet D(E)','Same three plain E occurrences','Retain those occurrence-specific forms.',obs[8][1],'Three locally unruled module arguments',kind='font',verdict='confirmed',witness=518);r.own[-1].update(source_pages=[507,510],is_misprint=False)
id='ASTRA-IX-PRODUCT-DOT-507'
why='Both complete507 images show a low typed multiplication point in F.lambda_-1(E). Retain the explicit cdot typesetting already declared for the IX module action. The map is K_bullet(S) tensor_Z K^bullet(S)→K_bullet(S),[F] tensor[E]↦[F tensor E], extended additively to the alternating exterior-power class. The factors and their order are unchanged.'
r.own_finding(id,507,'F.lambda_-1(E)',r'F\cdot\lambda_{-1}(E)','Retain the explicit dot transport.',why,'Final line of the Tor-class calculation',kind='symbol',verdict='confirmed',witness=518);r.own[-1]['is_misprint']=False
for p,a,b in [(506,'Lemme1.7.Soient A un anneau principal','la classe de Lg^*(F)=F tensor^L_(O_X)O_S.'),(507,'Pour cela,on considère le complexe:','la classe de A_m dans K^bullet(S).'),(508,'Proposition2.2.Avec les notations','dans le cas où P est de rang1.'),(509,'On poursuit la démonstration par récurrence','Le corollaire résulte donc immédiatement de2.2.'),(510,'3.Fibrés projectifs et fibrés en drapeaux','se factorise par K_bullet(X),cet')]:
 r.page(p,a,b,notes='Complete primary/native pages personally compared. Native details additionally confirm the507 struck symmetric-algebra S and three source plain E occurrences across507/510. Historical nominal HOLD57–59 belong to later text already reviewed elsewhere.',witness=p+11)
r.commit()
