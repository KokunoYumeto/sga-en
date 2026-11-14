#!/usr/bin/env python3
import re
from review_helpers import Review,base_text
r=Review();batch='386_390'
obs={
1:('The isomorphism L^bullet←L-prime^bullet points left','Both complete images show the upper barb at the left end of the handwritten arrow and an unheaded right endpoint. Retain the attached leftward isomorphism, from the strict resolution to L.','Strict resolution paragraph',386),
2:('de qui permet','Both complete images print de at the line end and qui permet next. Current changes the erroneous de to ce in the relative expression.','Strict resolution paragraph',386),
3:('Four explicit statement prose rules','Both full386 images show est; -parfait; Le morphisme canonique; est un isomorphisme de. Restore those four groups while preserving the plain item labels, category letters and punctuation.','Items i),ii) completing2.6',386),
4:('Occurrence-specific sheaf and complex rules','Every mathematical occurrence on386–390 was read in both complete images. The rules are restored below. On389, complex K and K_i are ruled, while K^bullet(X),K^bullet(S),K_naif and K_parf name the visibly plain K-groups. The two R^i cohomological symbols there are plain; the derived R and L have two rules and receive their own explicit glyph record.','All mathematical text386–390',386),
5:('Two commas after the top display','Both complete387 images have a comma after L and a second separated comma farther right. Diplomatic retains both; current keeps one, with the same sentence continuation et c’est un isomorphisme.','Top display',387),
6:('Four baseline stops between the triangle diagrams','Both full387 images show four separate baseline stops, followed by a comma. Retain the attached four-stop reading. Each triangle keeps its three exact vertices and the observed arrow orientations.','Sequence of distinguished triangles',387),
7:('Left vertical comparison has no arrowhead','Both full388 images show a straight vertical bar with a rotated tilde on its right. Retain the attached headless comparison and right-side label.','Commutative square left side',388),
8:('Right vertical comparison has no arrowhead','Both complete388 images show the same headless vertical bar and right-side rotated tilde. Retain the attached rendering.','Commutative square right side',388),
9:('389 starts2.8.Soit L^bullet','Both complete388–389 pairs confirm that388 ends correspondant est acyclique and389 starts the paragraph number2.8. The attached marker now precedes it and is correct.','Boundary388/389',389),
10:('Derived L has two lower rules','Both images show two distinct rules below L in Lf^*. Diplomatic renders those rules literally, current uses the double-struck L. The identity comparison of the two notations is the same derived pullback functor; flatness makes O_X tensor_(f^−1O_S) f^−1(−) exact, and the resolution comparison maps induce the printed identification with f^*.','Parenthetical derived-pullback identity',389),
11:('The prose K_i lacks its raised dot','Both images show ruled K_i without the raised complex dot; the preceding display has it on both K_i occurrences. The prose explicitly identifies these with the complexes of2.7. The comparison is degreewise identity on each K_i^bullet with its existing differential. Diplomatic keeps the missing dot; current retains its supplied dot.','Prose immediately after class equality',389),
12:('The final relation has three baseline stops','Both images show the three stops below the height of the plus signs. Retain the attached ldots.','Last displayed relation',389),
13:('390 begins achève par récurrence','Both complete389–390 pairs show389 ending on and390 beginning achève par. Retain the attached boundary.','Boundary389/390',390),
14:('The first flag-scheme D has two lower rules','Both images show the two rules. Keep the current bold D; restore the literal two rules diplomatically through the separate glyph decision below.','First D(E_i) in3.1',390),
15:('The first product-factor D has two lower rules','Both full images show the two rules beneath this D. Current retains bold D; diplomatic restores both source rules.','D(E_1) in3.1',390),
16:('The last product-factor D has two lower rules','Both complete images show the same pair of rules. Keep the occurrence-specific glyph decision.','D(E_n) in3.1',390),
17:('The product has three baseline stops','Both images show the three ordinary typed stops between the two product symbols. Retain the attached ldots.','Flag-scheme product',390),
18:('No comma follows the E_i before X=','Both complete images end that source line at E_i, with X= beginning the next. Diplomatic retains the omission. Current retains the supplied comma separating the sheaf/flag definitions from the following definition of X in the same hypothesis list.','Proposition3.1 hypotheses',390),
19:('The last line ends X_n et without a comma','Both full390 images have no comma after et. The personally read391 top begins pour tout i un O_Xi-Module without an initial comma. Retain the attached absence of the added comma; the top391 crop is boundary evidence only.','Boundary390/391',390),
20:('Explicit word-group rules in3.1','Both full390 images show the prose groups restored below. The quasi and compact groups have a gap at the hyphen. Variables, formula arguments, commas and the parenthetical K^bullet have their separate source styles.','Full Proposition3.1',390),
}
for k,(p,w,g,f) in obs.items():r.finding(batch,k,p,w,g,witness=f+11,verdict='amended' if k in [4,10,14,15,16] else 'not applied and now applied' if k in [2,3,20] else 'confirmed')
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':row.update(is_misprint=True,correction_status='accepted paired correction')
r.patch(386,'current','de qui permet','ce qui permet',f'check/findings/findings_{batch}.json#2',obs[2][1])

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'];t=t.replace(x['old'],x['new'])
 return t
math_pattern=re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]|\\begin\{equation\}.*?\\end\{equation\}|(?<!\\)\$(?!\$).*?(?<!\\)\$',re.S)
def letters(t,alphabet):
 counts={}
 def one(m):
  s=m[0]
  for c in alphabet:
   s,n=re.subn(rf'(?<![A-Za-z\\]){c}(?![A-Za-z])',lambda _:r'\underline{'+c+'}',s);counts[c]=counts.get(c,0)+n
  return s
 return math_pattern.sub(one,t),counts
for p in range(386,391):
 id=f'ASTRA-VI-GLYPHS-{p}'
 why='Restore the individually inspected ordinary-letter rules; primes, raised dots and indices stay outside the letter rule. Ordinary O has its observed rule.'
 if p==386:why+=' Every complex L and its component L^i is ruled; F_k stays plain; all script C category names retain their visible form.'
 if p==387:why+=' All L,B,M,P,N,K occurrences are ruled. Comp_n and capital Id remain plain operator names. The triangle arrows and four literal stops are unchanged.'
 if p==388:why+=' All N,M,P,B occurrences are ruled, including both lower nodes of the comparison square. Script C_0 and plain Comp keep their own shapes.'
 if p==389:why+=' All complex L,M,K,K_i and the two degree-zero sheaf L occurrences are ruled. Every K-group letter is explicitly protected as plain. The class map is the source map H↦[H[0]], and a complex K_i^bullet maps to its class in K^bullet(S); these are the exact maps relating the recorded notations. The derived L operator is protected separately.'
 if p==390:why+=' All E_i,E_k,E,F_0 and ordinary O occurrences are ruled; X_i,S and all K-group letters remain plain. The three D operators have their own double-rule record.'
 r.own_finding(id,p,'Explicitly inspected rules and plain exceptions','Plain sheaf/complex letters and script O','Restore the observed occurrence rules.',why,'Complete mathematical text',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old.replace(r'\mathcal O',r'\underline{O}').replace(r'\mathbf L',r'\SGADerivedL')
  if p==389:
   for a in [r'K^{\bullet}(X)',r'K^{\bullet}(S)',r'K^{\bullet}_{\naif}',r'K^{\bullet}_{\mathrm{parf}}']:new=new.replace(a,a.replace('K',r'\SGAKeepK',1))
  new,c=letters(new,{386:'LB',387:'LBMPNK',388:'NMPB',389:'LMKB',390:'EF'}[p]);new=new.replace(r'\SGADerivedL',r'\mathbf L').replace(r'\SGAKeepK','K')
  assert new!=old;r.patch(p,layer,old,new,id,why)
 r.own[-1]['observed_rule_counts']=dict(c,ordinary_O=old.count(r'\mathcal O'))
for p,ct in [(386,3),(389,2)]:
 id=f'ASTRA-VI-DERIVED-R-{p}';why='Both complete images show two lower rules on each total derived-functor R counted here. Diplomatic reproduces those two rules; current uses double-struck R for the identical functor represented by F_k applied to an injective resolution, with identity comparison on that representative. On389 the two separate R^i symbols are visibly plain and are left unchanged.'
 r.own_finding(id,p,'Twice-underlined total derived R',r'\mathbf R','Literal double rule in diplomatic; double-struck R in current.',why,'All total RF_k occurrences',kind='font',witness=p+11)
 r.patch(p,'diplomatic',r'\mathbf R',r'\underline{\underline{\mathrm R}}',id,why,count=ct);r.patch(p,'current',r'\mathbf R',r'\mathbb R',id,why,count=ct)
id='ASTRA-VI-DERIVED-L-389';why=obs[10][1]
r.own_finding(id,389,'Twice-underlined derived L',r'\mathbf L','Literal double rule in diplomatic; double-struck L in current.',why,'Equality f^*=Lf^*',kind='font',witness=400)
r.patch(389,'diplomatic',r'\mathbf L',r'\underline{\underline{\mathrm L}}',id,why);r.patch(389,'current',r'\mathbf L',r'\mathbb L',id,why)
id='ASTRA-VI-FLAG-D-390';why='All three flag-scheme D occurrences have two distinct lower rules in both complete images. Diplomatic reproduces both rules; current retains the existing bold D. The notation map is identity on the functor of complete flags of locally free quotients of the specified E: it sends each flag and each pullback flag to itself, inducing the identity of its representing scheme. No scheme or flag type is changed.'
r.own_finding(id,390,'Twice-underlined flag-scheme D',r'\mathbf D','Restore literal double rules diplomatically; retain bold D in current.',why,'Three flag-scheme operators in3.1',kind='font',witness=401)
r.patch(390,'diplomatic',r'\mathbf D',r'\underline{\underline{D}}',id,why,count=3)

id='ASTRA-VI-WORD-RULES-386';why=obs[3][1]
r.own_finding(id,386,'Four theorem word-group rules','Plain statement prose','Restore the four individually read rules.',why,'Completion of Proposition2.6',witness=397)
for a,b in [(r'\text{ est }',r'\text{ \uline{est} }'),(r'\text{-parfait}',r'\text{\uline{-parfait}}'),(r'\text{Le morphisme canonique }',r'\text{\uline{Le morphisme canonique} }'),(r'\text{ est un isomorphisme de }',r'\text{ \uline{est un isomorphisme de} }')]:r.patch(386,'both',a,b,id,why)
def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
id='ASTRA-VI-WORD-RULES-390';why=obs[20][1]
r.own_finding(id,390,'Proposition3.1 word-group rules','Plain statement prose','Restore the directly read groups.',why,'Full Proposition3.1',witness=401)
for layer in ['diplomatic','current']:
 old=current(390,layer);a=old.index(r'\textbf{Proposition 3.1.}')+len(r'\textbf{Proposition 3.1.}');b=old.index('On vérifie immédiatement',a)
 new=old[:a]+rules(old[a:b],['Soient','un schéma quasi','compact','des','-Modules','localement libres de type fini','le schéma des drapeaux de',"Alors l'homomorphisme canonique",'est injectif','étant défini','soit à partir des','-Modules localement libres de type fini','soit à partir des complexes parfaits'])+old[b:]
 assert new!=old;r.patch(390,layer,old,new,id,why)
for p,s in [(387,'2.7.'),(389,'2.8.')]:
 id=f'ASTRA-VI-PARAGRAPH-NUMBER-{p}';why='Both complete images print this paragraph number in plain weight. Retain its exact digits and punctuation.'
 r.own_finding(id,p,s,r'\textbf{'+s+'}',s,why,'Paragraph opening',kind='font',witness=p+11);r.patch(p,'both',r'\textbf{'+s+'}',s,id,why)

r.finding('376_380',25,'Script C in all thirty category occurrences380–389','The complete primary and native images of380,383,384,386,387,388,389 have now all been personally read. Their visible top loops and C-shaped bowls agree with the existing mathcal C,C_0,C-prime. The damaged first380 symbol is identified by its exact definition and the later full-subcategory/list occurrences as already recorded. This completes the previously page380-scoped decision without inferring any later occurrence from an unchecked page.','All thirty named category occurrences in section2',verdict='confirmed',witness=391)
r.finding('381_385',7,'Twenty-one ruled Proj_0 operator names on381–389','All complete source images381–389 have now been read. The first fifteen occurrences on381–385 and the additional386(1),387(1),389(4) each show the Proj rule. The geometric Proj(B) on382 is plain. Retain the exact attached Projz occurrences; the additional pages complete the earlier limited-scope decision.','All inspected Proj_0 operators381–389',verdict='confirmed',witness=392)
ends={386:('i)RF_k(L^bullet) est C_0-parfait','est alors l’homomorphisme:'),387:('Proj_0(F_k(L^bullet))→L^bullet, ,','Comp_d(M-prime_U^bullet)=0 pour d<d_0.'),388:('On considère alors le morphisme canonique2.7.2','le complexe P_k^bullet correspondant est acyclique.'),389:('2.8.Soit L^bullet un complexe parfait','on trouve alors x_r=0;on'),390:('achève par récurrence','des schémas X_1,…,X_n et')}
for p,(a,b) in ends.items():r.page(p,a,b,notes='Entire primary and native pages personally compared. All diagram vertices and arrowheads, complex and group notations, source rules and final lines were read. The391 top additionally settles the final boundary, without constituting its full-page check. The misplaced HOLD37 paragraph is addressed with its390–391 continuation separately.',witness=p+11)
r.commit()
