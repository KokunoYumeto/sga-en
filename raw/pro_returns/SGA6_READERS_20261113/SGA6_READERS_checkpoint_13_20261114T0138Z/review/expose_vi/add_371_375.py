#!/usr/bin/env python3
import re,json,shutil
from review_helpers import Review,ROOT,base_text
r=Review();batch='371_375'
obs={
1:('et il est clair qu’il surjectif','Both full scans omit est with no insertion above the line. Current supplies that verb only; diplomatic keeps the printed omission.','Proof1.6, after the display defining L',371),
2:('Occurrence-specific sheaf rules, with three local exceptions','Both full scans give the separately restored sheaf rules. Lemme1.5.2 uses plain ring/module letters;374 has plain class E and ruled sheaf E, connected by the printed class map. The first B in372(iii) and the second comparison target M on373 are unruled in both scans and receive separate paired decisions.','All mathematical letters on371–375',371),
3:('Individual upright statement word rules','The four complete statements have the explicitly mapped prose rules below. Their variables, labels and formulas remain independently styled.','Statements on371,372 and375',371),
4:('Baseline ellipses in four exact sequences','Both native and primary images place all four ellipses at the baseline, at the level of their terminal punctuation. Replace cdots by ldots in precisely these four positions.','Two sequences371; one372; one374',371),
5:('M a une begins372','The complete371 ends Par suite, si;372 begins with the underlined M and a une. The attached marker is correct.','Boundary371/372',372),
6:('de L begins373','Both372 images end base homogène;373 starts de L aient. The attached marker preserves the exact break.','Boundary372/373',373),
7:('A colon after canonique(1.2.1)','Both complete373 images have the colon after the reference before the first displayed comparison. Retain the supplied colon.','First comparison introduction',373),
8:('M_n0 tensor B(−n0) is inline','The formula begins an ordinary prose line and continues est isomorphe. Retain its inline placement, every index and the surrounding text.','Induction paragraph',373),
9:('374 begins with the complete Proj resolution','373 ends suite exacte: and374 begins0→Proj_0(L_{r+1}). The attached boundary is correct.','Boundary373/374',374),
10:('No punctuation after the filtration display','Both374 scans end the display immediately after the three matching closes, without a stop. Retain the attached omission of an added stop.','Display after En utilisant la filtration',374),
11:('No comma after K^bullet(S)','The complete clause proceeds directly to on considère; the source line break contributes no comma. Retain the attached reading.','Opening1.9',374),
12:('The twisted free-group equality omits n_i','Both375 scans lack the coefficients present in the immediately preceding free-group equality. The automorphism T_n of A sends each basis generator(E) to(E tensor O_X(n)); its inverse is T_{−n}. Z-linearity gives T_n(sum_i n_i R_i)=sum_i n_i T_n(R_i) with R_i=(L_i)−(M_i)+(N_i). Thus every displayed coefficient is preserved by the printed tensorization map. Current restores n_i; diplomatic keeps its omission.','Display after the tensorization automorphism',375),
}
for k,(p,w,g,f) in obs.items():r.finding(batch,k,p,w,g,witness=f+11,verdict='amended' if k==2 else 'not applied and now applied' if k in [1,3,4,12] else 'confirmed')
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint':row.update(is_misprint=True,correction_status='accepted paired correction')
for p,old,new,k in [(371,"qu'il surjectif.","qu'il est surjectif.",1),(375,r'(F(n))-(G(n))=\sum_i \bigl',r'(F(n))-(G(n))=\sum_i n_i\bigl',12)]:
 id=f'check/findings/findings_{batch}.json#{k}';why=next(x['reason'] for x in r.decisions if x['source_id']==id);r.patch(p,'current',old,new,id,why)
for p,n in [(371,2),(372,1),(374,1)]:r.patch(p,'both',r'\cdots',r'\ldots',f'check/findings/findings_{batch}.json#4','The four directly read exact-sequence ellipses are baseline typed stops.',count=n)

id='ASTRA-VI-SYZYGY-372'
why=('The complete main and native pages define Z_i=ker(d_i:L_i→L_{i−1}), then print remplacer L_{r+1} par Z_{r+1}. Write Z_{−1}=M. The exact sequences0→Z_i→L_i→Z_{i−1}→0 and the stated affine projective-dimension bound pd(M)≤r+1 give Ext^1(Z_r,N)=Ext^{r+2}(M,N)=0. Hence the finite-presentation Z_r is projective on each affine open and1.5.1 gives its graded local freeness. The exact truncation is0→Z_r→L_r→…→L_0→M→0, with the kernel inclusion as first differential. The old differential factors L_{r+1}→Z_r→L_r; this factorization and the identities on L_r,…,L_0 give its comparison map. An injective top term with this same exact tail maps isomorphically onto ker(d_r)=Z_r, uniquely by the kernel universal property. The printed Z_{r+1} instead has zero composite with d_{r+1}. Concrete source instance:r=0,S=Spec k,B=k[t],M=B/(t),L_1=B(−1)→L_0=B by multiplication by t. Then Z_0=(t),Z_1=0; using Z_1 leaves the nonzero kernel(t) unresolved. Current changes only the final subscript to r. The earlier i≥r+1 sentence is true and remains intact. Independent text/math audit:independent_syzygy_audit_372.json; it makes no additional image-reading claim.')
r.own_finding(id,372,'remplacer L_{r+1} par Z_{r+1}',r'L_{r+1} par Z_{r+1}',r'Current replaces the last Z_{r+1} by Z_r only.',why,'Final sentence of proof1.6',kind='misprint_in_print',witness=383)
r.own[-1].update(is_misprint=True,correction_status='accepted paired correction')
r.patch(372,'current',r'remplacer \(L_{r+1}\) par \(Z_{r+1}\)',r'remplacer \(L_{r+1}\) par \(Z_r\)',id,why)
shutil.copy2(ROOT/'review/english/EN_INDEPENDENT_VI_SYZYGY_AUDIT_372.json',ROOT/'review/expose_vi/independent_syzygy_audit_372.json')

id='ASTRA-VI-RECIPROCAL-374'
why=('Both complete images print the inline slash expression1/1+xi t without denominator parentheses. The immediately preceding identity is lambda_t(xi)=1+xi t. By the stated pre-lambda addition law, lambda_t(−xi)lambda_t(xi)=lambda_t(0)=1 in K^bullet(X)[[t]]. The series1+xi t has constant coefficient1, and its uniquely determined inverse is sum_{j≥0}(−xi)^j t^j. This identifies the full denominator1+xi t without changing its letters or their order. For the source instance S=Spec k,r=0,X=P^0_k,xi=1, the ordinary ungrouped expression1/1+t gives1+t, whose product with1+t is1+2t+t^2, while the required product is1. Current inserts the two denominator parentheses; diplomatic retains the source slash expression.')
r.own_finding(id,374,r'lambda_t(−xi)=1/1+xi t',r'\lambda_t(-\xi)=1/1+\xi t',r'\lambda_t(-\xi)=1/(1+\xi t)',why,'Sentence immediately before(1.9.1)',kind='misprint_in_print',witness=385)
r.own[-1].update(is_misprint=True,correction_status='accepted paired denominator grouping')
r.patch(374,'current',r'\lambda_t(-\xi)=1/1+\xi t',r'\lambda_t(-\xi)=1/(1+\xi t)',id,why)

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
for p in range(371,376):
 id=f'ASTRA-VI-GLYPHS-{p}'
 why='Restore the ordinary typed sheaf letters with the separately visible lower rules; their indices and arguments remain outside each rule. Ordinary O has its own rule.'
 if p==371:why+=' Lemme1.5.2 and its resolution have plain ring-case A,B,M,L and remain plain; the sheaf rules begin at Proposition1.6.'
 if p==372:why+=' The first B in item(iii) is visibly plain; this diplomatic exception is protected and separately corrected.'
 if p==373:why+=' The second comparison target M is visibly plain; the first target is ruled. Preserve this occurrence-specific diplomatic evidence.'
 if p==374:why+=' The first E in f^*(E)→O_X(1) and the E after cl are sheaves and ruled. The E before =cl and inside the lambda formulas are their classes and plain. Their exact map is cl_S:E↦[E], with cl_X(f^*E)=f^*(cl_S(E)). The final coefficient lambda^i(E) is carried from K^bullet(S) through the ring homomorphism f^* already stated in1.1; retain the printed omission of that structural-map notation.'
 if p==375:why+=' The free-group names A,A-prime,B remain plain; their sheaf generators F,G,L_i,M_i,N_i retain the visible letter rules.'
 r.own_finding(id,p,'Explicitly inspected ordinary-letter rules','Plain sheaf letters and script O','Restore only the recorded occurrence rules.',why,'Complete mathematical text',kind='font',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old.replace(r'\mathcal O',r'\underline{O}')
  if p==371:
   a=new.index(r'\textbf{Proposition 1.6.}');tail,c=letters(new[a:],'EBML');new=new[:a]+tail
  else:
   if p==372:new=new.replace(r'\text{est isomorphe comme }B',r'\text{est isomorphe comme }\SGAKeepB')
   if p==373:new=new.replace(r'\longrightarrow M.',r'\longrightarrow \SGAKeepM.')
   new,c=letters(new,{372:'BELMNZ',373:'BLMF',374:'BLMNF',375:'FGLMN'}[p]);new=new.replace(r'\SGAKeepB','B').replace(r'\SGAKeepM','M')
   if p==374:
    new=new.replace(r'f^*(E)\to',r'f^*(\underline{E})\to').replace(r'\text{avec } E=\cl E',r'\text{avec } E=\cl\underline{E}')
    c['sheaf_E']=2;c['plain_class_E']=4
  assert new!=old;r.patch(p,layer,old,new,id,why)
 r.own[-1]['observed_rule_counts']=dict(c,ordinary_O=old.count(r'\mathcal O'))

for p,id,old,new,why in [
 (372,'ASTRA-VI-ALGEBRA-RULE-372',r'\text{est isomorphe comme }B',r'\text{est isomorphe comme }\underline{B}','Both images leave the first B after comme unruled, while the next B and B(m) have their own rules. The proposition explicitly sets B=Sym(E). Its filtered submodules, quotient L^(m)/L^(m+1), and comparison N_m tensor B(m) use this same algebra and its original action. The algebra identification is id_B, with quotient action b·[l]=[bl]; no algebra is replaced. Current restores the one missing B rule, diplomatic keeps its absence.'),
 (373,'ASTRA-VI-TARGET-RULE-373',r'\longrightarrow M.',r'\longrightarrow \underline{M}.','The first displayed comparison ends in ruled M; the second ends in plain M in both images. Both are explicitly the map(1.2.1), x tensor a↦a.x, whose degree-k target is M_k. The second uses its n_0 component and lands in the same fixed graded sheaf M. Current restores this one target rule; diplomatic preserves the observed omission.')]:
 r.own_finding(id,p,old,old,new,why,'Isolated mathematical-letter rule omission',kind='misprint_in_print',witness=p+11);r.own[-1].update(is_misprint=True,correction_status='accepted paired notation correction');r.patch(p,'current',old,new,id,why)

def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
for p in [371,372,375]:
 id=f'ASTRA-VI-WORD-RULES-{p}';why='Map each word group directly read in both complete images to its upright ruled rendering. All mathematical symbols, punctuation and item labels retain their separately recorded forms.'
 r.own_finding(id,p,'Explicit statement word-group rules','Plain statement words','Restore the directly observed rules.',why,'Full statements on this page',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old
  if p==371:
   a=new.index(r'\textbf{Lemme 1.5.2.}')+len(r'\textbf{Lemme 1.5.2.}');b=new.index(r'\[',a)
   new=new[:a]+rules(new[a:b],['Soient','un anneau','une','algèbre de présentation finie','un','module de présentation finie','On suppose','et','plats sur','que pour tout corps résiduel','de','est de dimension projective','sur','ce qui est le cas si','Sous ces conditions','admet une résolution de longueur','par des','modules projectifs de type fini'])+new[b:]
   a=new.index(r'\textbf{Proposition 1.6.}')+len(r'\textbf{Proposition 1.6.}');b=new.index("Montrons d'abord",a)
   new=new[:a]+rules(new[a:b],['Soient','un schéma quasi-compact','un','-Module localement libre de rang','son algèbre symétrique','avec sa graduation habituelle','-Module gradué de présentation finie','plat sur','Alors il existe une résolution graduée','les','étant des','-Modules gradués qui sont localement libres de type fini','en tant que','-Modules gradués'])+new[b:]
  if p==372:
   a=new.index(r'\textbf{Proposition 1.7.}')+len(r'\textbf{Proposition 1.7.}');b=new.index(r'\[',a)
   new=new[:a]+rules(new[a:b],['Soient','un schéma quasi-compact','un','-Module localement libre de type fini','et','-Module gradué','localement libre de type fini','Alors il existe une filtration décroissante de','par des sous-','-Modules gradués','telle que'])+new[b:]
   for a,b in [(r'\text{pour }',r'\text{\uline{pour} }'),(r'\text{pour tout }',r'\text{\uline{pour tout} }'),(r'\text{est isomorphe comme }',r'\text{\uline{est isomorphe comme} }'),(r'\text{-Module gradué à un}',r'\text{\uline{-Module gradué à un}}'),(r'\text{-Module gradué de la forme }',r'\text{\uline{-Module gradué de la forme} }'),(r'\text{où }',r'\text{\uline{où} }'),(r'\text{ est un }',r'\text{ \uline{est un} }'),(r'\text{-Module localement libre de type fini.}',r'\text{\uline{-Module localement libre de type fini}.}')]:new=new.replace(a,b)
  if p==375:
   a=new.index(r'\textbf{Lemme 1.10.}')+len(r'\textbf{Lemme 1.10.}');b=new.index(r'Soit \(A\)',a)
   new=new[:a]+rules(new[a:b],['Avec les notations et les hypothèses de','soient','deux faisceaux localement libres de type fini sur','tels que','alors il existe un entier','tel que pour','on ait','sont localement libres de type fini sur'])+new[b:]
  assert new!=old;r.patch(p,layer,old,new,id,why)

id='ASTRA-VI-AUTHOR-NOTE-374';why='Both images show the original asterisk call and matching lower asterisk label. Restore that author mark while preserving verbatim the attribution of this demonstration to J.P.Jouanolou.'
r.own_finding(id,374,'(*) author note','Continuous footnote counter','Restore the original author asterisk.',why,'Final line and complete lower author note',kind='symbol',witness=385)
r.patch(374,'both',r'\footnote{',r'\SGAAuthorFootnote{*}{',id,why)
for p,s in [(373,'1.8.'),(374,'1.9.')]:
 id=f'ASTRA-VI-PARAGRAPH-NUMBER-{p}';why='Both source images print this paragraph number in ordinary weight. Preserve its exact digits and punctuation.'
 r.own_finding(id,p,s,r'\textbf{'+s+'}',s,why,'Paragraph opening',kind='font',witness=p+11);r.patch(p,'both',r'\textbf{'+s+'}',s,id,why)
ends={371:('Lemme1.5.2.Soient A un anneau','Par suite, si'),372:('M a une résolution partielle globale','les éléments d’une base homogène'),373:('de L aient des degrés','On en déduit une suite exacte:'),374:('0→Proj_0(L_{r+1})','Author asterisk note crediting J.P.Jouanolou.'),375:('Lemme1.10.Avec les notations','et on a donc encore:')}
for p,(a,b) in ends.items():r.page(p,a,b,notes='Entire primary and native pages personally compared. Every displayed sequence, formula, index, statement rule and final line read. Isolated missing rules and mathematical corrections have separate exact-map reasons. The complete original author note374 is retained.',witness=p+11)
r.commit()
