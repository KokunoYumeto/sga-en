#!/usr/bin/env python3
import re
from review_helpers import Review,base_text
r=Review();batch='381_385'
obs={
1:('A maps by a headed isomorphism to f_*O_Y','The native image resolves the right arrowhead beneath the tilde. Retain the attached headed arrow.','First display',381),
2:('No comma follows2.3.1.1','Both full images end this display at O_Y. Retain the attached absence of added punctuation.','Equation2.3.1.1',381),
3:('No stop follows2.3.1.2','Both full images end the display at (S,A). Retain the attached reading.','Equation2.3.1.2',381),
4:('Comme l’homomorphisme begins a paragraph','Both images show this new indentation after pour tout A-Module M. Retain the attached boundary.','After2.3.1.3',381),
5:('Si M est un begins a paragraph','Both full images show the new paragraph after the reference[4],p.164. Retain the attached boundary.','Last paragraph',381),
6:('The first382 display has a headed isomorphism','The complete382 images and native382_top.png resolve the right head under the tilde. The preceding381 ends En effet,l’isomorphisme:. Retain the attached headed arrow and its actual382 location.','Top382 display',382),
7:('All fifteen Proj_0 operator names carry a rule','The individually read occurrences are381(1),382(5),383(4),384(3),385(2). The separate Proj(B) on382 is plain. Retain the attached Projz forms at those fifteen loci. Later386–389 occurrences require their own image records.','Operator names381–385',381),
8:('Occurrence-specific mathematical-letter rules','Both complete images of each page were read. Restore the listed sheaf letters below, preserving the two plain B occurrences on383, two plain L occurrences on384, and the plain E in385 P(E) diplomatically. Those omissions receive separate exact-object corrections in current. F_k is the plain functor name, while the sheaf F has its observed rule.','All mathematical text381–385',381),
9:('382 begins with M→f_*M-tilde=bar-f_*M-tilde','The381 final line and382 first display were read in both complete images. The attached marker now precedes the display and is correct.','Boundary381/382',382),
10:('U in (M|U) is on the line','Both images show the full-height U beside the restriction bar. Retain the attached baseline restriction.','First localization formula',382),
11:('U in the tensor base (B|U) shares the index baseline','Both images place U at the baseline of that tensor index. Retain the attached restriction form.','First localization formula tensor base',382),
12:('U in the last factor (B|U)_s is on the line','Both images show the restriction U at the factor baseline. Retain the attached reading.','First localization formula last factor',382),
13:('U in Spec((B|U)_(s)) is on the line','Both images show that baseline restriction and a headless isomorphism sign. Retain both.','Affine-chart display',382),
14:('e>o uses a small baseline letter o','Both complete images show the small o, compared with the full-height zero in d>0 above. NOTE6 handles index zero only, so retain this baseline o diplomatically. The construction uses a homogeneous section of positive integral degree, and applies the same D_+ chart construction with substitution(s,d)↦(t,e); its lower bound is the integer0. Current restores0 in this one baseline position.','Final paragraph degree of t',382),
15:('The diagram is a triangle with U centered below','Both images show D_+(st) hooked into D_+(s), with the two diagonal structural arrows to U. The attached diagram preserves those vertices, labels and arrow orientations.','Initial diagram',383),
16:('The two module expressions are inline','Both full images put the formulas and et in the prose line beginning il s’agit de montrer. Retain the attached inline placement.','First prose sentence',383),
17:('The inner inverse-image letter is i','Native383_inner.png resolves the low i stem and separate upper ink; the preceding f has an ascender and hook. The diagram gives f_(U,st)=f_(U,s)∘i. Its inverse-image composition is i^−1∘f_(U,s)^−1=f_(U,st)^−1, with the equality on a stalk over y given by the identity on M_(f(y)). Applying i^* to the preceding tensor expression therefore yields f_(U,s)^−1 inside i^−1. Current changes only this inner i to f; diplomatic retains i.','First isomorphism chain second line',383),
18:('The first tensor-base restriction is (B|U)_(s)','Both full images show U on the local index baseline. Retain the attached restriction. The plain B at this locus is separately preserved diplomatically.','First isomorphism chain first line',383),
19:('The second tensor-base restriction is (B|U)_(s)','Both full images show U on the local index baseline. Retain the attached restriction; its plain B has a separate decision.','First isomorphism chain second line',383),
20:('The third tensor-base restriction is (B|U)_(s)','Both images show baseline U and ruled B. Retain that restriction and restore its observed rule below.','First isomorphism chain third line',383),
21:('The next tensor-base restriction is (B|U)_(st)','Both images show baseline U and ruled B. Retain the attached restriction.','Display after D’autre part',383),
22:('The final tensor base is (B|U)_(s)','Both complete images show baseline U. Retain the attached restriction.','Last localization display tensor base',383),
23:('The final factor is (B|U)_(st)','The native image resolves the B rule, and both images show baseline U. Retain the restriction and restore the observed B rule.','Last localization display final factor',383),
24:('On voit également begins a paragraph','Both images show the final indented paragraph after the derived-category display. Retain the attached break.','Final prose line',383),
25:('383 ends foncteur;384 begins Proj_0','Both complete pages show this exact boundary. Retain the attached marker after foncteur.','Boundary383/384',384),
26:('Si L est un begins a paragraph','Both complete images show the new indentation following2.4.2. Retain the attached boundary.','After2.4.2',384),
27:('The restriction D_+(U,s) is on the line','Both complete images place the chart expression beside the restriction bar. Retain the attached form.','Display after M=F_k(F)',384),
28:('F|D_+(U,s) uses a baseline chart expression','Both images show the same restriction notation at the target. Retain the attached reading.','Final display',384),
29:('F|D_+(U,s) uses a baseline chart expression','The first385 display continues the previous construction with the same on-line restriction. Retain the attached form.','First display',385),
30:('The formula defining alpha_d is inline','Both images put the entire map in the prose line before the EGA references. Retain its attached inline placement. The earlier use at s^n has a separate degree correction.','Definition of alpha_d',385),
31:('dans le cas ou','Both complete images print ou without the accent. Current restores où in this relative clause only.','Quasi-coherent case paragraph',385),
32:('The dot after L sits on the ordinary baseline','The complete images and native385_prop.png show a baseline full stop immediately after the ruled L; native385_rule_X.png compares it with the nearby sentence stop. The attached subscript bullet places the dot below that baseline. Diplomatic now renders L followed by an ordinary math stop; current keeps the raised complex dot. The same complex is the argument of RF_k and Proj_0 RF_k in the personally read386 top. Its component indexing and differential are unchanged: the comparison is identity in every degree.','Proposition2.6 complex name',385),
33:('Explicit statement word-group rules','Both full385 images show the groups restored below. The hyphen in quasi-compact is outside the two word rules, E in P(E) is plain, and the rule after sur ends before X as the native385_rule_X.png crop confirms. The top386 continuation is personally read as boundary evidence; its full-page review will record its own rules.','Proposition2.6 first portion',385),
34:('385 ends vérifiées:;386 begins item i)','Both complete385 pages end at this colon. The personally viewed386 top starts the first proposition item. The attached marker now precedes the display opening and is correct. This crop is not a full386 review.','Boundary385/386',385),
}
for k,(p,w,g,f) in obs.items():
 r.finding(batch,k,p,w,g,witness=f+11,actual_page=f,verdict='amended' if k in [8,14,32] else 'not applied and now applied' if k in [17,31,33] else 'confirmed')
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint' or row['source_id']==f'check/findings/findings_{batch}.json#14':row.update(is_misprint=True,correction_status='accepted paired correction')
for p,old,new,k,layer in [
 (382,r'\(e>o\)',r'\(e>0\)',14,'current'),
 (383,r'i^{-1}\Bigl(i_{U,s}^{-1}',r'i^{-1}\Bigl(f_{U,s}^{-1}',17,'current'),
 (385,'dans le cas ou $F$','dans le cas où $F$',31,'current'),
 (385,r'L_{\bullet}',r'L\mathord{.}',32,'diplomatic')]:
 id=f'check/findings/findings_{batch}.json#{k}';why=next(x['reason'] for x in r.decisions if x['source_id']==id);r.patch(p,layer,old,new,id,why)
r.source('fixes/FIXLOG_6.jsonl#1627','foncteur ends383; Proj_0 begins384',obs[25][1],'Complete boundary383/384',witness=395,change='Retain the attached corrected page marker.')

id='ASTRA-VI-ADJOINT-TARGET-382'
why=('Both images and native382_top.png show a bare M at the target, while the preceding line twice has M-tilde. The preceding isomorphism is phi:M→bar-f_*M-tilde. The stated adjunction Hom_Y(bar-f^*M,N)=Hom_(S,A)(M,bar-f_*N) sends phi to epsilon_(M-tilde)∘bar-f^*phi:bar-f^*M→M-tilde. On an affine stalk A_p this is m tensor a↦a m in the localized module. Thus the displayed adjoint has exactly the previously defined target M-tilde. Current restores its tilde alone.')
r.own_finding(id,382,r'bar-f^*(M)→M',r'\bar f^{\,*}(M)\longrightarrow M',r'\bar f^{\,*}(M)\longrightarrow\widetilde M',why,'Second display',kind='misprint_in_print',witness=393);r.own[-1].update(is_misprint=True,correction_status='accepted paired target correction')
r.patch(382,'current',r'\bar f^{\,*}(M)\longrightarrow M',r'\bar f^{\,*}(M)\longrightarrow \widetilde M',id,why)
id='ASTRA-VI-DEGREE-385'
why=('Both full images and native385_alpha.png print alpha_d(s^n). The immediately following definition has alpha_d:Gamma(V,B_d)→Gamma(f^−1(V),O_X(d)), while s^n has degree nd. The graded algebra map alpha sends a homogeneous b of degree q to its section of O_X(q); its multiplicativity gives alpha_(nd)(s^n)=alpha_d(s)^(tensor n). Multiplication by this section on D_+(V,s) is an isomorphism O→O(nd), whose inverse sends the restricted z of degree nd to a section of F. For B=k[x_0,x_1],s=x_0,d=1,n=2, x_0^2 belongs to B_2 and the printed alpha_1 has domain B_1; alpha_2(x_0^2)=alpha_1(x_0)^2 is the exact typed value. Current changes only this first alpha subscript to nd; the general definition of alpha_d stays intact.')
r.own_finding(id,385,r'z.alpha_d(s^n)^−1',r'z.\alpha_d(s^n)^{-1}',r'z.\alpha_{nd}(s^n)^{-1}',why,'Definition of the localization map2.5.2',kind='misprint_in_print',witness=396);r.own[-1].update(is_misprint=True,correction_status='accepted paired homogeneous-degree correction')
r.patch(385,'current',r'z.\alpha_d(s^n)^{-1}',r'z.\alpha_{nd}(s^n)^{-1}',id,why)

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
for p in range(381,386):
 id=f'ASTRA-VI-GLYPHS-{p}'
 why='Both full images were personally compared. Restore the individually visible sheaf-letter rules, leaving indices, tildes and powers outside each rule. Ordinary O is ruled.'
 if p==381:why+=' All A,B,M and the M under its tilde are ruled. Paragraph numbers are plain.'
 if p==382:why+=' All B and M are ruled, including both tilded M in the first display. The bare target M keeps its absent tilde only in diplomatic; the adjunction correction is separately sourced.'
 if p==383:why+=' The first two tensor-base B letters are visibly plain and protected; the remaining four B letters have rules. All M are ruled. The six headless isomorphism signs and the script category C are retained.'
 if p==384:why+=' F_k is a plain functor name at every occurrence; the sheaf F is ruled. The L in F_k(L) and the first L in L↝f_*L(n) are both plain and protected. All other L,B,M and sheaf F letters are ruled.'
 if p==385:why+=' F_k remains plain and the sheaf F is ruled. The first E in the proposition is ruled; E inside P(E) is plain and protected. L has its own rule, with the printed baseline stop outside it.'
 r.own_finding(id,p,'Explicit occurrence-specific sheaf rules','Plain sheaf letters and script O','Restore the directly read rules and retain the identified exceptions diplomatically.',why,'All mathematical text',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old.replace(r'\mathcal O',r'\underline{O}').replace('F_k',r'\SGAKeepFunctor')
  if p==383:new=new.replace(r'f_{U,s}^{-1}((B|U)_{(s)})',r'f_{U,s}^{-1}((\SGAKeepB|U)_{(s)})')
  if p==384:new=new.replace(r'\SGAKeepFunctor(L)',r'\SGAKeepFunctor(\SGAKeepL)').replace(r'$L\leadsto',r'$\SGAKeepL\leadsto')
  if p==385:new=new.replace(r'\mathbf P(E)',r'\mathbf P(\SGAKeepE)')
  new,c=letters(new,{381:'ABM',382:'BM',383:'BM',384:'BLFM',385:'MFBEL'}[p])
  new=new.replace(r'\widetilde \underline{M}',r'\widetilde{\underline{M}}')
  for a,b in [(r'\SGAKeepFunctor','F_k'),(r'\SGAKeepB','B'),(r'\SGAKeepL','L'),(r'\SGAKeepE','E')]:new=new.replace(a,b)
  assert new!=old;r.patch(p,layer,old,new,id,why)
 r.own[-1]['observed_rule_counts']=dict(c,ordinary_O=old.count(r'\mathcal O'))

for p,id,old,new,ct,why in [
 (383,'ASTRA-VI-ALGEBRA-RULES-383',r'f_{U,s}^{-1}((B|U)_{(s)})',r'f_{U,s}^{-1}((\underline{B}|U)_{(s)})',2,'Both images leave these two B letters plain, while the next four B occurrences are ruled. The first and second lines expand the same pullback tensor product over R=(B|U)_(s). The coefficient-ring comparison is id_R, induced by id_B under restriction and homogeneous localization b/s^m↦b/s^m. Current restores the two omitted rules without replacing any coefficient object.'),
 (384,'ASTRA-VI-FUNCTOR-ARG-RULE-384',r'F_k(L)',r'F_k(\underline{L})',1,'Both images and native384_LR.png leave the argument L in F_k(L) plain, while the immediately preceding L and the right-side L(n) have rules. The definition F_k(L)=direct-sum_(n≥k) f_*(L tensor O_X(n)) takes the identical O_X-module L as argument. Current restores this rule; the underlying object comparison is id_L.'),
 (384,'ASTRA-VI-MAP-ARG-RULE-384',r'$L\leadsto',r'$\underline{L}\leadsto',1,'Both complete images leave the source L of L↝f_*L(n) plain and rule its target occurrence. This is exactly the functor T_n:L↦f_*(L tensor O_X(n)) just used in the acyclicity statement, with source comparison id_L and identity on the tensor factor O_X(n). Current restores the omitted source rule.'),
 (385,'ASTRA-VI-PROJECTIVE-ARG-RULE-385',r'\mathbf P(E)',r'\mathbf P(\underline{E})',1,'Both complete images and native385_prop.png leave E inside P(E) plain; the same proposition introduces the ruled sheaf E immediately before it. The construction is X=Proj(Sym(E)), using exactly this sheaf. Its comparison is induced by id_E on each symmetric power, hence id_Sym(E) and id_Proj(Sym(E)). Current restores this one omitted rule; diplomatic retains plain E.')]:
 r.own_finding(id,p,old,old,new,why,'Isolated printed rule omission',kind='misprint_in_print',witness=p+11);r.own[-1].update(is_misprint=True,correction_status='accepted paired notation correction');r.patch(p,'current',old,new,id,why,count=ct)

for p in [384,385]:
 id=f'ASTRA-VI-DERIVED-R-{p}';why='Both complete images show two separate horizontal rules under the derived-functor R, resolved on384 in native384_LR.png and on385 beside2.5.3. Diplomatic renders both rules literally. Current uses the double-struck R for these specific occurrences. The notation map denotes the same functor: an injective resolution L→I^bullet is sent to F_k(I^bullet), with the identity chain map giving the comparison between the two renderings. No unviewed occurrence is changed.'
 r.own_finding(id,p,'Twice-underlined derived R',r'\mathbf R',r'Diplomatic \underline{\underline{\mathrm R}}; current \mathbb R.',why,'Equation2.4.2' if p==384 else 'Equation2.5.3',kind='font',witness=p+11)
 r.patch(p,'diplomatic',r'\mathbf R',r'\underline{\underline{\mathrm R}}',id,why);r.patch(p,'current',r'\mathbf R',r'\mathbb R',id,why)
for p,nums in [(381,['2.3.','2.3.1.']),(382,['2.3.2.']),(383,['2.3.3.']),(384,['2.4.','2.5.'])]:
 id=f'ASTRA-VI-PARAGRAPH-NUMBER-{p}';why='Both full images print these paragraph numbers in plain weight. Keep their exact digits and stops.'
 r.own_finding(id,p,','.join(nums),'Bold paragraph numbers','Restore the source plain weight.',why,'Paragraph openings',kind='font',witness=p+11)
 for s in nums:r.patch(p,'both',r'\textbf{'+s+'}',s,id,why)
def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
id='ASTRA-VI-WORD-RULES-385';why='Restore only the directly viewed prose groups; quasi and compact have separate rules, the hyphen remains outside, and the final X after sur is plain as the native close-up confirms. All formulas retain their independent letter rules.'
r.own_finding(id,385,'Proposition2.6 word-group rules','Plain statement prose','Restore the observed groups.',why,'Complete proposition portion on385',witness=396)
for layer in ['diplomatic','current']:
 old=current(385,layer);a=old.index(r'\textbf{Proposition 2.6.}')+len(r'\textbf{Proposition 2.6.}')
 new=old[:a]+rules(old[a:],['Soient','un schéma quasi','compact','un','-Module localement libre de type fini','et','un complexe parfait sur','Alors','il existe un entier','tel que pour','les propriétés suivantes soient vérifiées'])
 assert new!=old;r.patch(385,layer,old,new,id,why)
ends={381:('2.3.Nous aurons besoin','En effet,l’isomorphisme:'),382:('M→f_*M-tilde=bar-f_*M-tilde','On considère:'),383:('Triangle D_+(st),D_+(s),U','On voit également sur les constructions précédentes que le foncteur'),384:('Proj_0 sur la catégorie','bar-f^*_(U,s)(M_(s),U)→F|D_+(U,s),'),385:('il suffit,d’après la définition','les propriétés suivantes soient vérifiées:')}
for p,(a,b) in ends.items():r.page(p,a,b,notes='Entire primary and native pages personally compared. Native crops resolve the headed arrow382, inner i383, isolated missing rules, double R rules and385 baseline stop. The386 top was read for the boundary only. The385 section-equality defect has a separately recorded author-claim audit.',witness=p+11)
r.commit()
