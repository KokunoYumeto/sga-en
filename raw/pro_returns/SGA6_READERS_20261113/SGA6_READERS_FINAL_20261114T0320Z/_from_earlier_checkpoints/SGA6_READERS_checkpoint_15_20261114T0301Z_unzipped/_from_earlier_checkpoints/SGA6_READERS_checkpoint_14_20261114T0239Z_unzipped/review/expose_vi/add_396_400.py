#!/usr/bin/env python3
"""Explicit readings from both complete source images396–400."""
import re
from review_helpers import Review,base_text
r=Review();batch='396_400'
obs={
1:('étant effectués du poids i','Both complete396 images print effectués. The operation specified is the assignment w(c_i)=w(c_i^(j))=i used to select the isobaric coefficient equations; the corresponding French verb is affecter. Current corrects this word to affectés, preserving every variable and the assigned weight; diplomatic retains effectués.','First line, end of4.3',396),
2:('Three baseline stops between the monomials','Both complete396 images show the three low stops. Retain the attached ldots.','Corollaire4.4 display',396),
3:('Plain4.5. with a final stop','Both full396 images show this plain paragraph number with its stop. Retain the stop and restore ordinary weight below.','Paragraph4.5',396),
4:('Individually read sheaf and class occurrences','All five complete primary/native pairs were personally compared. The rules restored below follow each occurrence. The source explicitly gives the class map F_j↦[F_j] and E↦[E] on396, and the componentwise map (F_1,F_2)↦([F_1],[F_2]) on400; the ruled inputs and plain output classes are preserved accordingly. The final sheaf index in397 is separately amended from the checker reading after the native crop resolves m.','All mathematical text396–400',396),
5:('Fourteen double-rule D and fourteen double-rule G operators','Every listed operator was directly inspected in both complete pages: D counts1,4,7,2 on396–399; G counts5,9 on399–400. Diplomatic restores literal double rules and current uses bold operators. Each rendering denotes the identical represented flag/quotient functor, with identity comparison on each quotient and its pullbacks.','All D,G operators396–400',396),
6:('Occurrence-specific statement word rules','All listed source statements were read in both images of396–400. Restore the separately observed word groups, preserving plain formula letters, numbers, punctuation and hyphens except the specifically observed -Module group. The lemma continuation and each later statement are separately scoped below.','Statements396–400',396),
7:('Module localement de rang n, without libre','Both full397 images omit libre. This corollary is explicitly the case p_i=1 of4.5, whose hypothesis is the same locally free sheaf E of rank n. The specialization keeps id_E and changes only the partition to n blocks of size1; it therefore carries the printed4.5 local-freeness hypothesis. Retain the existing current libre and the diplomatic omission.','Corollaire4.7 hypothesis',397),
8:('Nine P operators with two lower rules','Both complete397 images show the same pair of rules on all nine projective P operators, including the one in the O subscript and the diagram. Diplomatic renders both rules literally; current uses bold P, preserving the functor of invertible quotients by its identity natural transformation.','All nine projective operators',397),
9:('Comma after the bottom S vertex','Both complete397 images show the comma after S. All three arrows and labels h,f,g agree with the attached diagram. Retain the comma.','Triangular diagram',397),
10:('Three baseline stops in the xi_2 monomial','Both full397 images show the three low stops, with the final semicolon after the bound. Retain the attached ldots.','First induction basis display',397),
11:('Three baseline stops in the xi_1 monomial on398','The actual display is at the top of398, personally read in both complete398 images. Its three stops are on the baseline; the attached ldots and marker position are correct.','Top398 basis display',398),
12:('Two separate roman-numbered relations','Both full397 images print separate lines i),ii), with the i under the sum sign. Retain the existing enumerated presentation and the complete formulas.','First two relations',397),
13:('398 begins at the complete basis display','Both complete397/398 pairs place les éléments: at the end of397 and the entire following display on398. Retain the attached marker before its opening display delimiter.','Boundary397/398',398),
14:('New paragraph at Si C est','Both full398 images indent Si C est after sont vérifiées. Retain the attached paragraph break.','Algebra C presentation',398),
15:("c'est homomorphisme",'Both complete399 images print c’est before homomorphisme. The following assertion concerns the just-defined map F_i-prime↦F_i and the next sentence calls it cet homomorphisme. Current corrects c’est to cet, preserving that same map and sentence.','Surjectivity sentence',399),
16:('grassmanienne with one n','Both full399 images print one n. Retain the diplomatic spelling and the attached current grassmannienne correction.','Paragraph4.9',399),
17:('New paragraph at Ce n’est','Both complete399 images indent this sentence after the corollary display. Retain the attached paragraph.','After Corollaire4.8',399),
18:('Plain4.9. with a final stop','Both full399 images show ordinary weight and the final stop. Retain the stop and restore plain paragraph styling.','Paragraph4.9 opening',399),
19:('New paragraph at Soient F_1,F_2','Both full400 images indent this sentence after4.9.1. Retain the attached paragraph break.','After the inverse-limit definition',400),
20:('leur classe','Both complete400 images print leur classe. The immediately preceding sheaves and the repeated unruled pair are related by the componentwise class map (F_1,F_2)↦([F_1],[F_2]). This supplies a distributive reading of the singular classe, one class for each named sheaf. The proposed plural is an editorial wording change without a uniquely established source misprint. Restore the author wording in current and keep it in diplomatic.','Class notation sentence',400),
21:('isomorphisme.:','Both complete400 images show a separate period before the colon. Diplomatic keeps it; current retains the removal of the stray period.','Proposition4.10 introduction',400),
22:('Tilde over a right-pointing arrow','Both full400 images and the enlarged native400_iso crop show the lower horizontal shaft with a right arrowhead. Retain the attached xrightarrow with tilde.','Proposition4.10 displayed isomorphism',400),
23:('Multiplication stop on the baseline','Both full400 images show the product stop at baseline height, while the main-image speck before the second equals is absent from the native page. Retain the literal period product and do not add a token for that scan defect.','Product of the two gamma series',400),
24:('New paragraph at Cette relation','Both complete400 images indent this sentence after the reciprocal display. Retain the attached paragraph.','Final paragraph',400),
}
for k,(p,w,g,f) in obs.items():
 r.finding(batch,k,p,w,g,witness=f+11,actual_page=f,verdict='reverted' if k==20 else 'amended' if k in [3,4,5,8,18] else 'not applied and now applied' if k in [1,6,15] else 'confirmed')
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':row.update(is_misprint=row.get('related_finding',row['source_id'])!=f'check/findings/findings_{batch}.json#20',correction_status='Author language retained' if row.get('related_finding',row['source_id'])==f'check/findings/findings_{batch}.json#20' else 'accepted paired correction')
for n,k in [(425,7),(424,16),(426,20),(427,21)]:
 r.source(f'fixes/FIXLOG_6_CURRENT.jsonl#{n}',obs[k][0],obs[k][1],obs[k][2],witness=obs[k][3]+11,
  verdict='reverted' if k==20 else 'confirmed',change='Restore source leur classe in current.' if k==20 else 'Retain the paired correction.')
 r.decisions[-1].update(is_misprint=k!=20,correction_status='Author language retained' if k==20 else 'accepted paired correction')
r.patch(396,'current','étant effectués du poids','étant affectés du poids',f'check/findings/findings_{batch}.json#1',obs[1][1])
r.patch(399,'current',"c'est homomorphisme",'cet homomorphisme',f'check/findings/findings_{batch}.json#15',obs[15][1])
r.patch(400,'current',r'\(F_1,F_2\) leurs classes dans',r'\(F_1,F_2\) leur classe dans',f'check/findings/findings_{batch}.json#20',obs[20][1])

repairs=[
 ('ASTRA-VI-FLAG-LAST-INDEX-397',397,r'\(F_1,\ldots,F_n\)',r'\(F_1,\ldots,F_m\)',
  'The complete source images show the last index with three m strokes; native397_Fn.png resolves them at native resolution. The attached transcription has n. Section4.5 defines F_i=ker(L_i→L_(i−1)) for1≤i≤k, and this corollary sets every p_i=1 with sum p_i=n, hence k=n. The exact indexed family is therefore (F_i)_(1≤i≤n), whose ordered class map gives xi_i=[F_i]. Current retains that final n; diplomatic restores the printed m. No m is bound in this passage.','diplomatic'),
 ('ASTRA-VI-FLAG-NOTATION-REFERENCE-397',397,'notation de 3.5','notation de 4.5',
  'Both complete397 images print3.5. The personally read4.5 on396 defines exactly the canonical quotients L_i and their kernels F_i. Under the stated specialization p_i=1,k=n, the comparison keeps each kernel F_i and sends it to its class xi_i. The reference is therefore4.5; current changes only its first digit.','current'),
 ('ASTRA-VI-FLAG-BASIS-REFERENCE-397',397,'et le corollaire 3.4','et le corollaire 4.4',
  'Both complete397 images print corollaire3.4. The basis statement used is the personally read Corollaire4.4 on396. Here A=K^bullet(P(E)), the rank-(n−1) kernel is F, and the inductive presentation maps A[T_2,...,T_n]/(sigma_i−lambda^i(F)) isomorphically to K^bullet(D(F)) by T_i↦xi_i. Applying4.4 to these n−1 ordered variables gives exactly xi_2^alpha_2...xi_(n−1)^alpha_(n−1),0≤alpha_i≤n−i. Current changes only3.4 to4.4.','current'),
 ('ASTRA-VI-FLAG-SPLITTING-REFERENCES-398',398,'notations de 3.5 et 3.7','notations de 4.5 et 4.7',
  'Both complete398 images print3.5 and3.7. The personally read4.5 defines the block sheaves F_j, and4.7 defines the classes of the invertible factors on each full-flag bundle. Pull back F_j to its full-flag bundle, take its successive rank-one kernels Q_i^(j), and apply [Q_i^(j)]=xi_i^(j); these exact operations give the variables of this paragraph. Current changes the two leading reference digits to4, leaving the source readings diplomatic.','current')]
for id,p,old,new,why,layer in repairs:
 printed=new if layer=='diplomatic' else old;corr=old if layer=='diplomatic' else new
 r.own_finding(id,p,printed,old,'Diplomatic: '+printed+'; current: '+corr,why,'Canonical flag indices or references',kind='misprint_in_print',witness=p+11)
 r.own[-1].update(is_misprint=True,correction_status='accepted paired index/reference correction')
 r.patch(p,layer,old,new,id,why)

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'],(p,layer,x['source_id']);t=t.replace(x['old'],x['new'])
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
for p in range(396,401):
 id=f'ASTRA-VI-GLYPHS-{p}';why=obs[4][1]
 r.own_finding(id,p,'Individually inspected single rules on sheaf letters','Plain sheaf letters and script O','Restore only the observed rules.',why,'All mathematical text',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old.replace(r'\mathcal O',r'\underline{O}')
  if p==396:
   s,c=letters(s,'L')
   pairs=[(r'\(E\) un',r'\(\underline{E}\) un'),(r'D_\pi(E)',r'D_\pi(\underline{E})'),(r'f^*(E)',r'f^*(\underline{E})'),
    (r'la classe de \(E\)',r'la classe de \(\underline{E}\)'),(r'\(F_i\) le noyau',r'\(\underline{F}_i\) le noyau'),
    (r'la classe de \(F_j\)',r'la classe de \(\underline{F}_j\)'),(r'\Lambda^i(F_j)',r'\Lambda^i(\underline{F}_j)')]
   for a,b in pairs:assert a in s,(p,a);s=s.replace(a,b)
   c.update(E=4,F=3)
  elif p==397:
   a=s.index(r'\textbf{Corollaire 4.7.}');prefix=s[:a];tail=s[a:]
   tail=tail.replace(r'\lambda^i(E)',r'\lambda^i(\SGAKeepE)');tail,c=letters(tail,'EF');s=prefix+tail.replace(r'\SGAKeepE','E')
  elif p==398:
   s=s.replace(r'\lambda_t(E)',r'\lambda_t(\SGAKeepE)').replace(r'\lambda^i(E)',r'\lambda^i(\SGAKeepE)')
   s,c=letters(s,'EF');s=s.replace(r'\SGAKeepE','E')
  elif p==399:
   a=s.index('Pour en déduire');first,c=letters(s[:a],'E');s=first+s[a:]
  else:
   a=r'Soient \(F_1,F_2\) les faisceaux';b=r'Soient \(\underline{F}_1,\underline{F}_2\) les faisceaux';assert a in s;s=s.replace(a,b);c={'F':2}
  assert s!=old;r.patch(p,layer,old,s,id,why)
 r.own[-1]['observed_rule_counts']=dict(c,ordinary_O=old.count(r'\mathcal O'))

for p,dc,gc in [(396,1,0),(397,4,0),(398,7,0),(399,2,5),(400,0,9)]:
 id=f'ASTRA-VI-DOUBLE-OPERATORS-{p}';why=obs[5][1]
 r.own_finding(id,p,f'{dc} double-rule D and {gc} double-rule G','Plain D/G operators','Literal double rule in diplomatic; bold operators in current.',why,'All D/G operators on this page',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old
  for c,n in [('D',dc),('G',gc)]:
   if not n:continue
   pat=rf'(?<![A-Za-z\\]){c}(?=[_(])'
   replacement=r'\underline{\underline{'+c+'}}' if layer=='diplomatic' else r'\mathbf '+c
   s,ct=re.subn(pat,lambda _:replacement,s);assert ct==n,(p,c,ct,n)
  assert s!=old;r.patch(p,layer,old,s,id,why)
id='ASTRA-VI-PROJECTIVE-OPERATORS-397';why=obs[8][1]
r.own_finding(id,397,'Nine projective P with two lower rules',r'\mathbb P','Literal double rules in diplomatic; bold P in current.',why,'All nine projective P operators',kind='font',witness=408)
r.patch(397,'diplomatic',r'\mathbb P',r'\underline{\underline{P}}',id,why,count=9);r.patch(397,'current',r'\mathbb P',r'\mathbf P',id,why,count=9)
id='ASTRA-VI-EXTERIOR-WEDGE-396';why='Both complete396 images show the two unfooted strokes of the exterior-power wedge before the ruled F_j, matching the inspected exterior glyphs in the preceding Koszul calculation. Restore wedge in both layers. The operation remains the same alternating quotient F_j^tensor i→wedge^i F_j and its class lambda_i^(j).'
r.own_finding(id,396,'Exterior power written with the two-stroke wedge',r'\Lambda^i',r'\wedge^i',why,'Class of the exterior power in4.5',kind='symbol',witness=407);r.patch(396,'both',r'\Lambda^i',r'\wedge^i',id,why)

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
for p in [396,397,399,400]:
 id=f'ASTRA-VI-WORD-RULES-{p}';why=obs[6][1]
 r.own_finding(id,p,'Explicit statement word-group rules','Plain statement prose','Restore only the observed word groups.',why,'Statements on this page',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);s=old
  if p==396:
   marker_end=s.index('\n')+1;b=s.index(r'\end{enumerate}')
   top=rules(s[marker_end:b],['et','étant effectués du poids','étant affectés du poids','et ces',"relations engendrent l'idéal des relations entre les"]);s=s[:marker_end]+top+s[b:]
   a=s.index(r'\textbf{Corollaire 4.4.}')+len(r'\textbf{Corollaire 4.4.}');b=s.index('Pour la démonstration',a)
   s=s[:a]+rules(s[a:b],['Les éléments de','de la forme','forment une base de','considéré comme module sur'])+s[b:]
   a=s.index(r'\textbf{Théorème 4.6.}')+len(r'\textbf{Théorème 4.6.}')
   s=s[:a]+rules(s[a:],['Avec les hypothèses et les notations de','la','algèbre','est engendrée par les',"l'idéal des relations entre les",'est engendré par les relations déduites de'])
  elif p==397:
   a=s.index(r'\textbf{Corollaire 4.7.}')+len(r'\textbf{Corollaire 4.7.}');b=s.index('On procède par récurrence',a)
   s=s[:a]+rules(s[a:b],['Soient','un schéma quasi','compact','un','-Module localement de rang','-Module localement libre de rang','le fibré en drapeaux de','les classes des faisceaux inversibles','notation de','Alors','est la','algèbre engendrée par les','soumis aux relations'])+s[b:]
  elif p==399:
   a=s.index(r'\textbf{Corollaire 4.8.}')+len(r'\textbf{Corollaire 4.8.}');b=s.index("Ce n'est",a)
   s=s[:a]+rules(s[a:b],['Avec les hypothèses et les notations de','posons','alors la','algèbre','est engendrée par les',"l'idéal des relations entre les",'est engendré par les relations déduites de'])+s[b:]
  else:
   a=s.index(r'\textbf{Proposition 4.10.}')+len(r'\textbf{Proposition 4.10.}');b=s.index("D'après 4.8",a)
   s=s[:a]+rules(s[a:b],['Soit','un schéma quasi','compact','Alors','avec les notations de','on a un isomorphisme'])+s[b:]
  assert s!=old;r.patch(p,layer,old,s,id,why)
for p,num in [(396,'4.5.'),(399,'4.9.')]:
 id=f'ASTRA-VI-PARAGRAPH-NUMBER-{p}';why='Both complete source images print the paragraph number in ordinary weight with its terminal stop. Keep the digits and stop and restore the observed weight.'
 r.own_finding(id,p,num,r'\subsection*{'+num+'}',num,why,'Paragraph number',kind='font',witness=p+11);r.patch(p,'both',r'\subsection*{'+num+'}',num,id,why)
ends={396:('(c_i et c_i^(j) étant effectués du poids i)','lambda_t(E)=product_(j=1)^k lambda_t(F_j).'),397:('En d’autres termes','K^bullet(S) les éléments:'),398:('xi_1^alpha_1...xi_(n−1)^alpha_(n−1)','par4.3.ii), compte'),399:('tenu de la structure','O_(G_S^(n,r))^r comme'),400:('quotient de O_(G_S^(n,r))^(r+1)','On peut donc écrire:')}
for p,(a,b) in ends.items():r.page(p,a,b,notes='Both complete primary/native pages personally compared. Native crops resolve the printed final m on397 and the right-pointing isomorphism on400. The class maps, flag indices and exact reference substitutions are explicitly recorded.',witness=p+11)
r.commit()
