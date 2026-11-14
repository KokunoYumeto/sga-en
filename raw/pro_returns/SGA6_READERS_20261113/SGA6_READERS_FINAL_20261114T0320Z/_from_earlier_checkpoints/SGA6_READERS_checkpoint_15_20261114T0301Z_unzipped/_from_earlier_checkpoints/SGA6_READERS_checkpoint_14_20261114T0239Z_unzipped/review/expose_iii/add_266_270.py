#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='266_270'
obs={
1:('rep.localement constante','Both scans print rep. in this second list; the corresponding first list spells resp. Retain the printed abbreviation in diplomatic and the missing-s correction in current.','Definition5.4, second list',278),
2:('Separate upright word-group rules','The complete267,268 and270 scans were compared. Record the precise prose rules with the occurrence-specific patches below; retain independent mathematical glyphs and plain item labels.','Definition5.4,Lemma5.5,Corollary5.6',278),
3:('Author call1 after the comma in display5.5.1','The call follows the final comma of the displayed rank identity. On a has no call. Keep that placement and restore the explicit original label1.','Display5.5.1 and author note',279),
4:('la compatibilité du rang','The269 page begins with la;268 ends résulte donc de, followed by its separate author note. Retain the existing marker.','Boundary268/269',280),
5:('Missing close for the resp. parenthesis','Both scans open a prose parenthesis before resp. and leave it open before est semi-continue. The mathematical H^1 argument already has its own close. Current supplies only the prose close; diplomatic retains the omission.','Proof5.5(ii), first comparison',280),
6:('Capital X inside E_k(X)','The preceding sentence explicitly defines E_k(x)=E_x tensor^L_OXx k(x), with x the varying point. The rank equality uses precisely that object and the canonical scalar extension O_Xx→k(x). On a finite free representative, its terms O_Xx^{r_i} tensor k(x)→k(x)^{r_i} send (a_j)tensor b to (a_j b), with inverse coordinates e_jtensor b_j. Both ranks are sum(-1)^i r_i. Retain current x in this exact identified fibre notation, preserving capital X in diplomatic.','Proof5.5(ii), locally constant rank',280),
7:('Z-prime^p(E)) with an extra close','Both scans show two closes after the single argument E, with no surrounding prose parenthesis opened. Current deletes the surplus close; diplomatic keeps it.','Proof5.5(ii), flat cokernels',280),
8:('localement libre de type fini','The printed singular libre follows the joint subject Z-prime^{p+1}(E) et Z-prime^p(E), with plural sont plats. Current supplies the plural agreement libres only there; the later singular H^p(E) est localement libre remains unchanged.','Proof5.5(ii), two locally free modules',280),
9:('H^1(E_k(x) without its outer close','The note has a close for k(x), but none for H^1(. The headless comparison separates the two cohomology terms. Keep the printed omission in diplomatic and the unique outer close in current.','Starred author note',280),
10:('est localement constante','The first word270 is est. Page269 ends at the formula rg(H^p(E)_x), followed by its starred note. Preserve the existing boundary.','Boundary269/270',281),
11:('Page270 ends la fonction','Both full270 and271 scans show the entire y-indexed rank formula on271. Retain the current marker before that formula.','Boundary270/271',281),
}
for k,(reading,why,region,wit) in obs.items():r.finding(batch,k,reading,why,region,witness=wit)
why=('The print on271 reads rank over k(x), with x the generic point fixed on270 and y the varying point. The actual fibre E tensor_X^L k(y) is a k(y)-complex and is exactly the fibre in5.6(i) with its bound variable renamed x→y. '
 'This relabelling sends the scalar extension O_X,y→k(y) and every term and differential to themselves. The need for the y field is witnessed by X=Spec(k[t]), E=O_X and cohomological degree0: at y=(t), the fibre is k with t acting by0. '
 'An action of the generic field k(t) extending this k[t] action would make t invertible and zero on a nonzero module, which is impossible. Current k(y) therefore restores the stated fibre-rank function. Keep printed k(x) in diplomatic; assign the record to actual271.')
r.finding(batch,12,'rank_k(x) of the k(y)-fibre',why,'First line271',actual_page=271,witness=282)
for num,related in [(384,1),(385,7),(386,8),(387,12)]:
 row=next(x for x in r.decisions if x['source_id']==f'check/findings/findings_{batch}.json#{related}')
 r.source(f'fixes/FIXLOG_6_CURRENT.jsonl#{num}',row['printed_reading'],row['reason'],row['region'],change='Retain current correction; preserve printed diplomatic reading.',witness=282 if num==387 else row['page']+11,page=row['page'])
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type']=='misprint' or row['source_id'].startswith('fixes/FIXLOG_6_CURRENT.jsonl#'):row['is_misprint']=True
for p,n in [(266,1),(267,9),(268,10),(269,2),(270,6)]:
 id=f'ASTRA-III-STRUCTURE-{p}';why='The complete primary and native pages show ordinary typed O contours with individual lower rules at every counted structure-sheaf occurrence. Preserve all indices and replace only the contour/rule encoding.'
 r.own_finding(id,p,'Ruled ordinary O',r'\mathcal O',r'\underline{O}',why,'All structure-sheaf symbols',kind='font',witness=p+11)
 r.patch(p,'both',r'\mathcal O',r'\underline{O}',id,why,count=n)
for p,label in [(267,'1'),(269,'*')]:
 id=f'ASTRA-III-AUTHOR-NOTE-{p}';why='The original author call and the complete lower note were read in both scans. Restore the exact parenthesized label and preserve every word and formula of the note.'
 r.own_finding(id,p,'Author label '+label,r'Continuous \footnote numbering','Restore original label '+label,why,'Author note and its call',kind='symbol',witness=p+11)
 r.patch(p,'both',r'\footnote{',r'\SGAAuthorFootnote{'+label+'}{',id,why)
id='ASTRA-III-AUTHOR-NOTE-268';why='The numbered author call1 follows the comma inside5.5.1; the complete note defines rg of a perfect complex and cites I6.11. Preserve that text and place the explicit matching mark and note.'
r.own_finding(id,268,'Author call1 in5.5.1 and complete note',r'Automatic \footnotemark/\footnotetext','Restore original author label1.',why,'Rank identity and author note',kind='symbol',witness=279)
r.patch(268,'both',r'\mbox{\footnotemark}',r'\mbox{\SGAAuthorFootMark{1}}',id,why)
r.patch(268,'both',r'\footnotetext{',r'\SGAAuthorFootText{1}{',id,why)
def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'];t=t.replace(x['old'],x['new'])
 return t
def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
for p in [267,268,270]:
 id=f'ASTRA-III-WORD-RULES-{p}';why='Both full scans show these separate upright prose rules. Formula letters, variables, mathematical exponents and item numbers remain independently set. Author-note text and proof prose remain plain except the observed Preuve label.'
 r.own_finding(id,p,'Observed statement word rules','Plain statement prose','Restore the inspected upright rules.',why,'Definition,Lemma or Corollary statements',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old
  if p==267:
   a=new.index(r'\textbf{Définition 5.4.}')+len(r'\textbf{Définition 5.4.}');b=new.index(r'\SGAAuthorFootnote{1}',a)
   new=new[:a]+rules(new[a:b],['Soit','un topos','notons',"l'ensemble de ses points",'Soient','un ensemble ordonné','une application','et','On dit que','est semi-continue supérieurement','semi-continue inférieurement','resp.','rep.','localement constante','en',"s'il existe",'un objet','ponctué','de','tel que pour tout point','on ait',"si elle l'est en tout point"])+new[b:]
   a=new.index(r'\textbf{Lemme 5.5.}')+len(r'\textbf{Lemme 5.5.}')
   new=new[:a]+rules(new[a:],['Soient','un topos localement annelé','et','Alors on a','avec les notations de'])
  elif p==268:
   b=new.index(r'\emph{Preuve.}')
   new=rules(new[:b],['Si','est parfait','les','pour','sont des espaces vectoriels de rang fini sur','nuls sauf un nombre fini','et la fonction','est localement constante sur','est','pseudo-cohérent','un espace vectoriel de rang fini sur','est semi-continue supérieurement sur','Si en outre le foncteur','de','dans','est exact','est localement libre de type fini et la fonction précédente est localement constante','Supposons','resp.','et soit','Si le foncteur','est exact à droite','à gauche','sur la catégorie','des','Modules','il existe un ouvert','ponctué','tel que le foncteur','soit exact à droite','sur'])+new[b:]
  elif p==270:
   a=new.index('Soient',new.index(r'\textbf{Corollaire 5.6}'));b=new.index(r'\emph{Preuve.}',a)
   new=new[:a]+rules(new[a:b],['Soient','un schéma','un complexe','pseudo-cohérent','Alors','Pour','est de rang fini sur','et la fonction','est constructible et semi-continue supérieurement sur','Supposons','quasi-séparé et','à cohomologie quasi-cohérente et localement bornée','Si le foncteur','est exact sur la catégorie des','Modules quasi-cohérents','la fonction','est localement constante et','est localement libre de type fini','Inversement','si','est localement noethérien et réduit et si la fonction précédente est localement constante','le foncteur'])+new[b:]
  new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.');new,_=underline_words(new)
  assert new!=old;r.patch(p,layer,old,new,id,why)
r.page(266,'Si E vérifie la condition(5.1a))','en vertu de(4.3.2).',notes='Both complete paragraphs, the single ruled O, all reference digits and the full blank remainder read.',witness=277)
r.page(267,'Définition5.4.Soit X un topos','avec les notations de(5.4.1b)); author note1',notes='All definition and example text, nine ruled O letters, original P without x in the rank expression, the complete author note and lemma opening read. Existing current rep. correction retained.',witness=278)
r.page(268,'(i)Si E est parfait','l’assertion(i)résulte donc de; author note1',notes='All three lemma conditions, eleven ordinary derived L letters, ten O rules, the complete rank identity and numbered author note read.',witness=279)
r.page(269,'la compatibilité du rang','rank(H^p(E)_x); complete starred author note',notes='All three cohomology degrees, two O rules, two ordinary L letters, the five-arrow exact sequence, the paired flat modules and all five printed typographical slips read. The original starred note label is restored.',witness=280)
r.page(270,'est localement constante','et,sur U,la fonction',notes='Both headless stalk comparisons, six O rules, eight ordinary derived L letters, the full corollary and beginning of its proof read. The next page’s rank-field correction is explicitly assigned to271.',witness=281)
r.commit()
