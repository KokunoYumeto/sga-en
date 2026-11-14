#!/usr/bin/env python3
import re,json
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='261_265'
obs={
1:('du type O_U,X','The full primary and native pages begin with du;260 ends with faisceaux. The existing boundary therefore places the first word correctly.','Boundary260/261',272),
2:('pseuso-cohérent','Both scans type pseuso in this sentence. The surrounding occurrences and the named pseudo-coherence condition identify the s-for-d typing error. Keep pseuso in diplomatic and pseudo in current.','Supposons E sentence',272),
3:('R plain, Hom ruled','The individual lower rule belongs to Hom alone. Retain the separate ordinary R.','Definition of T-prime',272),
4:('Baseline full stop','The placeholder after the ordinary tensor is aligned with the text baseline in both scans.','First tensor-functor placeholder',272),
5:('Baseline full stop','The placeholder inside H^p(E tensor^L .) is likewise low; the L itself remains ordinary and raised.','Second tensor-functor placeholder',272),
6:('tion a)(resp.a-prime),etc.)','The first printed syllable tion continues condi- at the end of261. Preserve the existing split-word marker.','Boundary261/262',273),
7:('quasi-séparé ruled, comma plain','Only this adjective has the prose rule in remark(iv). Set it upright with its lower rule and keep the comma outside.','Remark5.2(iv), opening',273),
9:('Headless tilde over a horizontal line','Both full scans show a headless comparison in b-prime. The preceding comparison in a-prime has a visible right arrowhead and retains that head.','Proposition5.3(b-prime) parenthesis',274),
10:('c)Pour tout changement de base','The item label begins264. Page263 ends the b-prime condition and two complete author notes. The existing item boundary is exact.','Boundary263/264',275),
11:('Comma on the display line','The comma is printed after the formula5.3.1.1 on264. Page265 begins composée de. The already moved comma remains with its display.','Display5.3.1.1',275),
12:('composée de','The whole morphisme X-prime→X phrase and display5.3.1.1 belong to264. Retain the existing marker immediately before composée de.','Boundary264/265',276),
}
for k,(reading,why,region,wit) in obs.items():
 r.finding(batch,k,reading,why,region,witness=wit,actual_page=264 if k==11 else None)
why='Both scans print etc). où in the middle of the sentence. The preceding parenthesis on the same page uses etc.) la condition. The abbreviation stop belongs to etc., followed by the closing parenthesis; the relative clause où continues that sentence. Move only the stop in current, preserving the printed order in diplomatic.'
r.finding(batch,8,'etc). où',why,'Remark5.2(iv), analogue condition',verdict='not applied and now applied',change='Current etc.) où; diplomatic etc). où.',witness=273)
r.patch(262,'current',"etc). où l'on remplace","etc.) où l'on remplace",f'check/findings/findings_{batch}.json#8',why)
for row in r.decisions:
 if any(f'check/findings/findings_{batch}.json#{k}' in {row['source_id'],row.get('related_finding')} for k in [2,8]):row['is_misprint']=True

id='ASTRA-III-REFERENCE-261'
why=('Both full261 scans print strictly perfect followed by(2.1). Definition I2.1 on95 was re-read directly: its third alternative says that every E^i lies in C0 and E^i=0 for almost all i. '
 'In the ringed-topos setting here, C0 consists locally of finite-rank free O-modules, so this is exactly the bounded finite-free complex used for the subsequent dévissage. '
 'The identification sends each complex term and each differential to itself; after a chosen local basis E^i≅O^{r_i}, the basis map sends (a_j) to sum a_j e_j with inverse the coordinate maps. '
 'III2.1 on236 is the proper-direct-image finiteness conjecture and supplies no such definition. Restore the missing exposé locator I in current, leaving the mathematical assertion and the printed diplomatic locator intact.')
r.own_finding(id,261,'strictement parfait(2.1)','Same printed locator','Current strictement parfait(I2.1).',why,'Proof5.1.1, final reduction',kind='reference',witness=272)
r.own[-1].update(is_misprint=True,supplemental_images=['scan/SGA6_scan_360dpi.pdf#page=109','scan/SGA6_scan_360dpi.pdf#page=250'])
r.patch(261,'current','strictement parfait (2.1)','strictement parfait (I 2.1)',id,why)
for p,n in [(261,5),(262,6),(263,2),(264,6),(265,11)]:
 id=f'ASTRA-III-STRUCTURE-{p}';why='Every counted structure-sheaf O has an ordinary typed contour and an individual lower rule in both complete scans. Restore that observed glyph, preserving its argument and indices.'
 r.own_finding(id,p,'Ruled ordinary O',r'\mathcal O',r'\underline{O}',why,'All structure-sheaf symbols',kind='font',witness=p+11)
 r.patch(p,'both',r'\mathcal O',r'\underline{O}',id,why,count=n)
id='ASTRA-III-AUTHOR-NOTES-263';why='The two complete author notes and their raised parenthesized calls were read in both scans:1 defines Qcoh(Y) using O_Y,2 cites3.7. Preserve the full text and original numbering.'
r.own_finding(id,263,'Author calls1 and2',r'Continuous \footnote numbering','Restore original numbered author notes.',why,'Two author notes and calls',kind='symbol',witness=274)
for old,new in [(r'\footnote{\(\Qcoh(Y)\)',r'\SGAAuthorFootnote{1}{\(\Qcoh(Y)\)'),(r'\footnote{en vertu de (3.7).}',r'\SGAAuthorFootnote{2}{en vertu de (3.7).}')]:
 r.patch(263,'both',old,new,id,why)

def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'];t=t.replace(x['old'],x['new'])
 return t
def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
def protect_notes(s):
 notes=[]
 while r'\SGAAuthorFootnote{' in s:
  a=s.index(r'\SGAAuthorFootnote{');end=a+len(r'\SGAAuthorFootnote')
  for unused in range(2):
   assert s[end]=='{';depth=1;end+=1
   while depth:
    if s[end]=='{' and s[end-1]!='\\':depth+=1
    elif s[end]=='}' and s[end-1]!='\\':depth-=1
    end+=1
  notes.append(s[a:end]);s=s[:a]+f'@@ANOTE{len(notes)}@@'+s[end:]
 return s,notes
for p in range(261,266):
 id=f'ASTRA-III-WORD-RULES-{p}';why='Restore the exact upright word-group rules read in both complete scans. Mathematical symbols, statement labels and author-note prose keep their separately observed settings. The proof reference5.1.1 is outside the rule under Preuve de.'
 r.own_finding(id,p,'Observed upright word-group rules','Unruled statement prose or italic emphasis','Restore the inspected lower rules.',why,'Assertions, proof labels and named property',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old
  if p==261:
   a=new.index(r'\((5.1.1)\) :');b=new.index(r'\emph{Preuve de',a)
   new=new[:a]+rules(new[a:b],['la flèche','est un isomorphisme si','est pseudo-cohérent et','injectif'])+new[b:]
   new=new.replace(r'\emph{Preuve de \((5.1.1)\).}',r'\uline{Preuve de} \((5.1.1)\).')
  elif p==262:
   pass
  elif p==263:
   new=new.replace("(propriété d'échange)",r"(\uline{propriété d'échange})")
   a=new.index('Soient',new.index(r'\textbf{Proposition 5.3.}'));b=new.index(r'\begin{enumerate}',a)
   new=new[:a]+rules(new[a:b],['Soient','un morphisme de schémas quasi-compacts et quasi-séparés',"un complexe à cohomologie quasi-cohérente et d'amplitude plate finie rel.",'à','et','Considérons les conditions suivantes'])+new[b:]
   a=new.index(r'\begin{enumerate}');part,notes=protect_notes(new[a:])
   part=rules(part,['Le foncteur','de','dans','est exact à droite','La flèche canonique','composée de la flèche canonique',"et de l'isomorphisme",'est un isomorphisme pour tout','est exact à gauche',"composée de l'isomorphisme",'et de la flèche canonique'])
   for i,n in enumerate(notes,1):part=part.replace(f'@@ANOTE{i}@@',n)
   new=new[:a]+part
  elif p==264:
   b=new.index(r'\emph{Preuve.}')
   new=rules(new[:b],['Pour tout changement de base','la flèche canonique','est un isomorphisme','Alors on a','En outre','si','est propre','pseudo-cohérent rel.','à','donc parfait rel.','et sous réserve de validité de','pour','donc en particulier si','est projectif ou si','est noethérien','les conditions précédentes sont équivalentes'])+new[b:]
   a=new.index(r'\textbf{Lemme 5.3.1.}')+len(r'\textbf{Lemme 5.3.1.}')
   new=new[:a]+rules(new[a:],['Soit','un schéma quasi-séparé','et soit','un complexe à cohomologie localement bornée et quasi-cohérente','Alors la condition','équivaut à la condition','Pour tout schéma','au-dessus de','la flèche canonique','est un isomorphisme','En outre','si','est pseudo-cohérent','la condition','implique que','pour tout morphisme'])
  elif p==265:
   b=new.index(r'\emph{Preuve.}')
   new=rules(new[:b],['composée de','et de la flèche canonique','est un isomorphisme'])+new[b:]
  new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.');new,_=underline_words(new)
  assert new!=old,p;r.patch(p,layer,old,new,id,why)
r.page(261,'du type O_U,X','(ii)Si x est un point de X…la condi-',notes='All five ruled O letters, three ordinary derived L letters, one Hom rule, both low placeholders and every star label read. Enlarged primary/native crops confirm two stars in the restriction sentence.',witness=272)
r.page(262,'tion a)(resp.a-prime),etc.) relative à E_x','a_qcoh↔a-prime_qcoh↔b_qcoh←b-prime_qcoh',notes='All four remarks, both implication chains, six ruled O letters, two small ob occurrences and the sole quasi-séparé prose rule read. Current abbreviation-stop order corrected.',witness=273)
r.page(263,'résultent de(5.1)appliqué au topos ponctuel','b-prime ends pour tout M∈ob Qcoh(Y); two complete author notes',notes='Both Hom rules, two O rules, ten ordinary derived L letters, the headed a-prime comparison, headless b-prime comparison, all four conditions and both author notes read.',witness=274)
r.page(264,'c)Pour tout changement de base','Display5.3.1.1 with its comma',notes='All three displayed canonical arrows, six ruled O letters, three ordinary L letters, full equivalence chain and complete printed hypotheses read. The numbered equation belongs wholly to264.',witness=275)
r.page(265,'composée de H^{-p-1}(E-dual)tensorO_Xprime','Starred canonical arrow with final stop',notes='All eleven ruled O letters, ten ordinary L letters, canonical arrow directions, both affine-module arguments and final dual comparison read. The EGA chapter glyph and its IV subscript are retained as printed.',witness=276)
r.commit()
