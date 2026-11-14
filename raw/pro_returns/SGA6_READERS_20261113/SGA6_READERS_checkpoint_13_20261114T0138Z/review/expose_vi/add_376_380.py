#!/usr/bin/env python3
import re
from review_helpers import Review,base_text
r=Review();batch='376_380'
obs={
1:('The first class lacks its final closing parenthesis','Both full images have two closing parentheses after L_i(n), three after M_i(n), and four after N_i(n). The free-group expression is the image of (L_i(n))−(M_i(n))+(N_i(n)) under the generator map (H)↦(f_*H); each generator has its own outer pair. Current restores precisely the missing close after the first generator.','First display',376),
2:('D’après1.2 begins a paragraph','Both images show a fresh indented paragraph. Retain its existing break; the reference itself has a separate paired correction below.','After first display',376),
3:('Il en résulte begins a paragraph','Both complete pages confirm the attached blank-line paragraph boundary.','After local-freeness display',376),
4:('On peut écrire begins a paragraph','The indentation follows equation1.11.1 in both images. Retain the attached boundary.','After1.11.1',376),
5:('L’égalité1.11.1 begins a paragraph','The visible new paragraph follows the definitions of F,F-prime. Retain the attached boundary.','After definitions',376),
6:('D’après le lemme1.10 begins a paragraph','Both images show the new indented paragraph before the last display.','Before final display',376),
7:('Occurrence-specific sheaf rules; plain class letters','Every occurrence on376–380 was read in both complete images. The precise restoration below preserves plain E in all lambda and sigma expressions and plain checked E,F in the gamma expressions, while restoring their sheaf occurrences. The map connecting them is cl_Y:H↦[H] in K^bullet(Y), with cl_X(f^*H)=f^*cl_S(H). No class-letter rule is supplied by inference.','All mathematical text376–380',376),
8:('First direct sum has no index','Both full377 images show a bare circled-plus sign. Retain the attached unindexed first direct sum.','Top display first line',377),
9:('Second direct sum has no index','The second circled-plus sign is likewise unindexed. Retain the attached reading.','Top display second line',377),
10:('Par ailleurs begins a paragraph','The new paragraph is indented in both images. Retain the attached break.','After top display',377),
11:('The Koszul sum has no written index','Both images show the bare summation sign immediately followed by (−1)^(i−1). Retain the printed omission of the sum index.','Differential formula',377),
12:('No full stop follows the differential formula','Both complete images end the formula with its last parenthesis only. Retain the attached reading.','Differential formula end',377),
13:('sigma has subscript Greek rho−i','The enlarged native crop native377_rho.png resolves the round rho with its continuous descending stroke; the p in pour tout p has its separate serif head. The homogeneous degree-p term of the printed Koszul complex is wedge^i(E) tensor Sym^(p−i)(E), whose class is lambda^i([E]) sigma_(p−i). Taking the alternating sum gives the displayed relation with p−i. Current retains this uniquely indexed reading; diplomatic keeps rho−i.','Equation1.11.3',377),
14:('Seven ellipses consist of baseline stops','The one ellipsis in376(1.11.1), the one in the377complex and all five in its differential formula are at the ordinary punctuation baseline in both complete images.','Seven explicit formula loci376–377',377),
15:('The first zero equation has no printed label','Both full378 images have an empty label area. The later two references explicitly name1.11.4. Substitution p(j)=n_0+r+j in this first equation and interchange of the two finite sums give the next equality; the i≤r summands vanish by1.11.2, leaving (−1)^(r+1)lambda^(r+1)(E) sum_j x_j sigma_(n_0−1+j)=0. Multiplication by (−1)^(r+1) gives the printed reduction. This identifies the first zero equation as the referenced relation. Keep it unnumbered diplomatically and restore label1.11.4 in current.','First equation and both later references',378),
16:('Pour i≠r+1 begins a paragraph','Both images show the indentation after the double-sum equality. Retain the attached boundary.','After double-sum equality',378),
17:('Par conséquent begins a paragraph','Both images show the fresh indented paragraph after the vanishing display.','After vanishing sum',378),
18:('Or E est de rang begins a paragraph','The paragraph begins with the visibly ruled sheaf E. Retain the existing paragraph break and restore that separate letter rule below.','After reduced relation',378),
19:('Cette relation begins a paragraph','Both complete379 images confirm the attached boundary after1.12.1.','After1.12.1',379),
20:('homomorpnisme','Both complete images show a short n arch at the second h position, while the initial h has its ascender. Current keeps homomorphisme; diplomatic preserves the typed n.','First prose paragraph',379),
21:('The stated basis ends in xi^(k+r+1)','Both images clearly include the final +1. Multiplication m_(xi^k):K^bullet(X)→K^bullet(X), a↦xi^k a, is a K^bullet(S)-module automorphism with inverse m_(xi^(−k)). It sends the already proved basis1,xi,…,xi^r exactly to xi^k,…,xi^(k+r). The next power satisfies1.9.1 multiplied by xi^k. For S=Spec k,r=0,X=P^0_k,xi=1, the printed two-element list is(1,1), and the nonzero coefficient vector(1,−1) maps to0. Current removes only the final +1.','Remarque1.13 basis',379),
22:('éléments linéairement indépendant','Both images lack the plural s on the adjective modifying éléments. Current restores indépendants only.','Remarque1.13',379),
23:('No comma after x^(r+1)','The first exact-sequence introduction continues on considère without a comma in both images. Retain the attached reading.','Before first exact sequence',379),
24:('On obtient un résultat begins a paragraph','The source starts this indented paragraph after1.13.1. Retain the existing boundary.','After1.13.1',379),
25:('Script C at all six category occurrences on380','The clear C_0,C,C-prime and final list show the same top loop and C-shaped bowl. The first C is damaged to short traces in both scans. Its exact object definition is the category of graded B-Modules and degree-preserving morphisms; the later C_0 is its full subcategory, fixing the same category symbol C. The first and last damaged A occurrences are tied to the explicitly named category of O_X-Modules and its complex L^bullet. Retain the existing mathcal A,C on380. Later pages383–389 require their own image records before extending this occurrence verdict.','Section2.2 category names',380),
26:('La notation starts a paragraph','Both complete images show the new indentation after séminaire. Retain the attached paragraph break.','Opening section2',380),
27:('Pour tout n starts a paragraph','Both complete images show the new indentation after sont abéliennes. Retain the attached boundary.','Final paragraph',380),
28:('380 ends with the twisted complex;381 begins2.3','The complete380 images end with L^bullet tensor O_X(n). The personally viewed primary381 top begins2.3.Nous aurons besoin. The attached marker now precedes2.3 and is correct. This top crop supplies boundary evidence only, not a full381 review.','Boundary380/381',380),
29:('Individual word-group rules in Théorème2.1','Both complete380 images show exactly the prose groups restored below, with all mathematical variables and punctuation independently styled. Only the labels of the surrounding Remarques carry rules.','Theorem2.1',380),
}
for k,(p,w,g,f) in obs.items():
 r.finding(batch,k,p,w,g,witness=f+11,verdict='amended' if k in [7,25] else 'not applied and now applied' if k in [14,21,22,29] else 'confirmed')
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':row.update(is_misprint=True,correction_status='accepted paired correction')
for old,new,k in [(r'\xi^{k+r+1}',r'\xi^{k+r}',21),('linéairement indépendant sur','linéairement indépendants sur',22)]:
 id=f'check/findings/findings_{batch}.json#{k}';why=next(x['reason'] for x in r.decisions if x['source_id']==id);r.patch(379,'current',old,new,id,why)
for p,n in [(376,1),(377,6)]:r.patch(p,'both',r'\cdots',r'\ldots',f'check/findings/findings_{batch}.json#14','All seven personally inspected formula ellipses are baseline typed stops.',count=n)

id='ASTRA-VI-REFERENCE-376'
why=('Both full images print D’après1.2. Section1.2 defines the graded-module functors; the stated simultaneous vanishing and local freeness are the conclusions of1.3 on368, already personally read. The application map substitutes each of the finite family L_i,M_i,N_i,F,G for its variable F and keeps the same projective-bundle morphism f:X→S. Each is a locally free finite-type O_X-module and is flat over S because f is flat. Taking the maximum of their finitely many twist bounds gives every local-freeness assertion and R^1 f_*L_i(n)=0. The long exact sequence then yields0→f_*L_i(n)→f_*M_i(n)→f_*N_i(n)→0. Current changes only the cited final digit from2 to3.')
r.own_finding(id,376,'D’après1.2',"D'après 1.2,","D'après 1.3,",why,'Paragraph after first display',kind='misprint_in_print',witness=387)
r.own[-1].update(is_misprint=True,correction_status='accepted paired reference correction')
r.patch(376,'current',"D'après 1.2,","D'après 1.3,",id,why)

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'];t=t.replace(x['old'],x['new'])
 return t
math_pattern=re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]|\\begin\{equation\}.*?\\end\{equation\}',re.S)
def letters(t,alphabet):
 counts={}
 def one(m):
  s=m[0]
  for c in alphabet:
   s,n=re.subn(rf'(?<![A-Za-z\\]){c}(?![A-Za-z])',lambda _:r'\underline{'+c+'}',s);counts[c]=counts.get(c,0)+n
  return s
 return math_pattern.sub(one,t),counts
for p in range(376,381):
 id=f'ASTRA-VI-GLYPHS-{p}'
 why='Both complete images were read. Restore the visible ordinary-letter sheaf rules, keeping indices, accents and powers outside each rule; ordinary O has its own rule.'
 if p==376:why+=' All F,G,L_i,M_i,N_i,E_j,E-prime_j and F-prime are ruled; the free-group name A-prime remains plain.'
 if p==377:why+=' All E are ruled except the single class argument E of lambda^i(E) in1.11.3. The exterior-power glyph is the two-stroke wedge visible in the complex and differential; the existing wedge commands preserve those strokes. The recorded NOTE6 transport of the double-underlined symmetric algebra S remains in force.'
 if p==378:why+=' Exactly three sheaf E occurrences are ruled: Or E est de rang; de type fini E; symétrique de E. Every E inside lambda and sigma is visibly plain.'
 if p==379:why+=' The first exact sequence has ruled F,E; the dual exact sequence has ruled checked E,F, with checks outside the rules. All checked E,F in the gamma expressions are plain. In the final paragraph the sheaf E=(O_S)^(r+1) is ruled and the class E=r+1 is plain. Their explicit map is H↦[H], and the free sheaf maps to r+1 times[O_S].'
 if p==380:why+=' All three E, four B, three L and six O occurrences have separately visible rules. The complex L has a raised dot. Category script letters retain their own observed shapes.'
 r.own_finding(id,p,'Explicitly inspected mathematical letter rules','Plain sheaf letters and script O','Restore the occurrence-specific rules.',why,'All mathematical text',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old.replace(r'\mathcal O',r'\underline{O}');c={}
  if p==376:new,c=letters(new,'FGLMNE')
  if p==377:
   new=new.replace(r'\lambda^i(E)',r'\lambda^i(\SGAKeepE)');new,c=letters(new,'FE');new=new.replace(r'\SGAKeepE','E')
  if p==378:
   for a,b in [(r'Or \(E\)',r'Or \(\underline{E}\)'),(r'de type fini \(E\)',r'de type fini \(\underline{E}\)'),(r'symétrique de \(E\)',r'symétrique de \(\underline{E}\)')]:assert new.count(a)==1;new=new.replace(a,b)
   c={'sheaf_E':3}
  if p==379:
   a=new.rfind(r'\[',0,new.index(r'0\longrightarrow F'));b=new.index('On remarque alors',a)
   part,c=letters(new[a:b],'FE');part=part.replace(r'\check \underline{E}',r'\check{\underline{E}}').replace(r'\check \underline{F}',r'\check{\underline{F}}');new=new[:a]+part+new[b:]
   new=new.replace(r'si \(E=',r'si \(\underline{E}=');c['final_sheaf_E']=1
  if p==380:new,c=letters(new,'EBL')
  assert new!=old;r.patch(p,layer,old,new,id,why)
 r.own[-1]['observed_rule_counts']=dict(c,ordinary_O=old.count(r'\mathcal O'))

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
id='ASTRA-VI-WORD-RULES-380';why='Map the individually read theorem prose groups to upright ruled text; mathematical letters and punctuation keep the separately recorded forms.'
r.own_finding(id,380,'The explicit word groups in Théorème2.1','Plain statement words','Restore the directly observed rules.',why,'Full Théorème2.1 statement',witness=391)
for layer in ['diplomatic','current']:
 old=current(380,layer);a=old.index(r'\textbf{Théorème 2.1.}')+len(r'\textbf{Théorème 2.1.}');b=old.index(r'\textbf{2.2.}',a)
 new=old[:a]+rules(old[a:b],['Soient','un schéma quasi-compact','un','-Module localement libre de rang','le fibré projectif associé','soit','la classe','dans','du complexe égal à','en degré nul','et nul pour les autres degrés','Alors','muni de sa structure naturelle de','algèbre est','module libre admettant pour base'])+old[b:]
 assert new!=old;r.patch(380,layer,old,new,id,why)
for p,s in [(376,'1.11.'),(380,'2.2.')]:
 id=f'ASTRA-VI-PARAGRAPH-NUMBER-{p}';why='Both complete images give the paragraph number in plain type. Keep its exact digits and stop.'
 r.own_finding(id,p,s,r'\textbf{'+s+'}',s,why,'Paragraph opening',kind='font',witness=p+11);r.patch(p,'both',r'\textbf{'+s+'}',s,id,why)
ends={376:('Displayed equality of the classes of f_*F(n),f_*G(n)','Equality of cl(f_*F(n)) and cl(f_*F-prime(n))'),377:('Or f_*F(n)=direct sum','cela suffit à entrainer la nullité des x_j).'),378:('D’après1.11.3,on peut écrire','les relations1.11.3 peuvent encore s’écrire:'),379:('1.12.1 lambda_t(E).sigma_−t(E)=1.','l’égalité1.13.1 se réduit à:'),380:('1.13.2 x^(r+1)=0.','complexe L^bullet tensor O_X(n).')}
for p,(a,b) in ends.items():r.page(p,a,b,notes='Entire primary and native pages personally compared, including all formulas, individual sheaf/class rules, punctuation and final lines. The381top was additionally read to settle the final boundary; no full381 claim is made here.',witness=p+11)
r.commit()
