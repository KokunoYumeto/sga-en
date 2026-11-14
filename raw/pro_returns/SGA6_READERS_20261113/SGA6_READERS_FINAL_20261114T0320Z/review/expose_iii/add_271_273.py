#!/usr/bin/env python3
import re,json
from review_helpers import Review,ROOT,base_text,underline_words
r=Review();batch='271_275'
prior={json.loads(x)['source_id']:json.loads(x) for x in (ROOT/'review/expose_iii/decisions.jsonl').read_text().splitlines()}
obs={
1:('The y-indexed rank formula begins271','The complete270 page ends la fonction; both271 scans start with the whole formula and est. Retain the existing marker.','Boundary270/271',282),
2:('rank_k(x) in the opening y-indexed formula',prior['check/findings/findings_266_270.json#12']['reason'],'First line271',282),
3:('parf with its own lower rule','Both scans give the lowered parf its own rule. Preserve uparf with the other mathematical symbols outside the prose rules.','Proposition5.7 membership',282),
4:('H^i(Rf_*(E)tensor^L_Yk(y) without the outer close','The source closes k(y), but leaves H^i( open. Current closes the full cohomology argument with one additional parenthesis; diplomatic retains the exact printed omission.','Proposition5.7(i), first sentence',282),
5:('The first displayed function also lacks the outer close','Both complete scans repeat the same omission in the alternating-rank display. Current supplies the one matching close for H^i(.','Proposition5.7(i), display',282),
6:('A full stop follows the displayed function','The source continues the sentence La fonction…est constructible after this stop. Preserve the printed stop in diplomatic and its removal in current. No mathematical symbol changes.','Proposition5.7(ii), display',282),
7:('Individual upright statement word rules','The rules include the et between the two EGA locators, followed by the full proposition and all three item statements. Apply the explicit occurrence map below.','Proposition5.7 and items(i)–(iii)',282),
8:('A baseline full stop after the ordinary tensor','The final proof expression T_-p has a low placeholder and an ordinary tensor, with no raised L. The chosen strictly perfect representative is retained as printed.','End of proof5.6',282),
9:('A new indented paragraph after complexe parfait','Both scans show the separate pasted paragraph beginning L’assertion(i). Retain the existing paragraph break and every word.','Proof5.7, second paragraph',283),
11:('b)On peut développer','Item b and On both start273;272 ends the E_y definition and a full stop. Retain the existing boundary.','Boundary272/273',284),
12:('M) with one unmatched close on the left','The projection comparison opens and closes Rf_*(E) before the tensor. The extra close after M has no opening mate. Current removes only that surplus close; diplomatic keeps it.','Remark5.8(b), displayed arrow',284),
13:('isomorphime','Both scans omit the s in this word. The term isomorphisme is used throughout the preceding projection formula and the immediately corresponding5.8(a) assertion. Preserve the printed spelling in diplomatic and the supplied s in current.','After the projection comparison',284),
14:('New paragraph at A la différence','The final sentence of the preceding paragraph ends D(X)). The next indented line starts the separate discussion of assertions1 and2. Retain the attached paragraph break.','Remark5.8(b), final paragraph',284),
15:('BIBLIOGRAPHIE in ruled capitals','Both scans show the all-capital word with a lower rule. Preserve the capitals; the heading transport retains its rule.','Bibliography heading',284),
16:('Ein Theorem der Analytischen Garbentheorie, plain','The full title has ordinary upright letters with no lower rule. The initial capital A and trailing baseline dots remain as printed.','Bibliography[1]',284),
17:('Residues and Duality, plain','The title has ordinary upright letters and no lower rule. Preserve its printed case, series number20 and year1966.','Bibliography[H]',284),
18:('Théorie des faisceaux, plain','The full title, publisher Hermann and year1958 are printed upright without a lower rule.','Bibliography[T.F]',284),
19:('ce oadre que','The full native scan confirms the closed o beside the open c in ce and ces; the primary agrees. Current cadre restores the French word in dans ce cadre, while diplomatic retains the typed o.','Complete author note1',284),
}
for k,(reading,why,region,wit) in obs.items():r.finding(batch,k,reading,why,region,witness=wit)
why=('Both scans show three opening parentheses and only the close after IV3.1.0. The clause contains two cited items joined by et, EGA III6 and IV3.1.0; the finite verb que pour f plat continues On peut montrer outside the citation. '
 'Close the first individual citation after III6 and close the encompassing cf. parenthesis after the already closed IV3.1.0 citation. This preserves each original opening and all citation tokens in their original order. '
 'The token map on EGA,III,6,IV,3.1.0 is the identity; no locator, functor or asserted base-change map is replaced. Current inserts these two closing delimiters, diplomatic retains the print.')
r.finding(batch,10,'(cf.(EGA III6 et(IV3.1.0) que',why,'Remark5.8(a), citation parenthesis',verdict='not applied and now applied',change='Current(cf.(EGA III6)et(IV3.1.0))que.',witness=283)
r.patch(272,'current','(cf. (EGA III 6 et (IV 3.1.0) que','(cf. (EGA III 6) et (IV 3.1.0)) que',f'check/findings/findings_{batch}.json#10',why)
for path,num,k,verdict in [('fixes/FIXLOG_6.jsonl',374,19,'reverted'),('fixes/FIXLOG_6_CURRENT.jsonl',388,19,'amended'),('fixes/FIXLOG_6_CURRENT.jsonl',389,12,'confirmed'),('fixes/FIXLOG_6_CURRENT.jsonl',390,13,'confirmed')]:
 row=next(x for x in r.decisions if x['source_id']==f'check/findings/findings_{batch}.json#{k}')
 why=row['reason']+(' The historical diplomatic Codex replacement is reverted by the later scan-backed restoration; retain oadre in diplomatic.' if verdict=='reverted' else ' Treat this current edit as a correction of the print, preserving its diplomatic counterpart.')
 r.source(f'{path}#{num}',row['printed_reading'],why,row['region'],verdict=verdict,change='Retain the paired diplomatic/current readings.',witness=284)
for row in r.decisions:
 if row.get('kind')=='misprint_in_print' or row['type'] in ['misprint','fixlog'] and row['source_id'] in [f'fixes/FIXLOG_6.jsonl#374']+[f'fixes/FIXLOG_6_CURRENT.jsonl#{i}' for i in [388,389,390]]:row['is_misprint']=True
for p,n in [(271,3),(272,1)]:
 id=f'ASTRA-III-STRUCTURE-{p}';why='All counted structure-sheaf letters have ordinary typed O contours and individual lower rules in both complete scans. Retain the exact indices.'
 r.own_finding(id,p,'Ruled ordinary O',r'\mathcal O',r'\underline{O}',why,'All structure-sheaf symbols',kind='font',witness=p+11)
 r.patch(p,'both',r'\mathcal O',r'\underline{O}',id,why,count=n)
id='ASTRA-III-AUTHOR-NOTE-273';why='Both full scans show author note1 after continuité and its complete text below the bibliography. Restore that original raised-number call and matching note label without changing its historical attribution or wording.'
r.own_finding(id,273,'Author label1',r'Continuous \footnote numbering','Restore original author note1.',why,'Remark5.8(b) call and full lower note',kind='symbol',witness=284)
r.patch(273,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',id,why)
def current(p,layer):
 t=base_text(p,layer)
 for x in r.patches:
  if x['page']==p and x['layer'] in ['both',layer]:
   assert t.count(x['old'])==x['expected_count'];t=t.replace(x['old'],x['new'])
 return t
def rules(t,phrases):
 pat='(?<![A-Za-zÀ-ÿ])('+'|'.join(re.escape(s).replace(r'\ ',r'\s+') for s in sorted(phrases,key=len,reverse=True))+')(?![A-Za-zÀ-ÿ])'
 return re.sub(pat,lambda m:r'\uline{'+m[0]+'}',t)
for p in [271,272]:
 id=f'ASTRA-III-WORD-RULES-{p}';why='Restore the exact upright prose rules seen in both scans. The separate parf and O rules remain independent, the last proof’s ordinary tensor and low placeholder remain intact, and all mathematical conditions are preserved verbatim.'
 r.own_finding(id,p,'Observed upright word-group rules','Plain statement prose or italic proof label','Restore the inspected rules.',why,'Proposition5.7 or proof label',witness=p+11)
 for layer in ['diplomatic','current']:
  old=current(p,layer);new=old
  if p==271:
   a=new.index(r'\textbf{Proposition 5.7.}')+len(r'\textbf{Proposition 5.7.}')
   new=new[:a]+rules(new[a:],['et','Soient','un morphisme propre de schémas quasi-compacts','Alors','sous réserve de validité de','donc par exemple si','est projectif ou si','est noethérien','Pour','les','sont des espaces vectoriels de rang fini sur','nuls sauf un nombre fini','et la fonction','est localement constante sur','La fonction','est constructible et semi-continue supérieurement sur','Supposons','quasi-séparé','si le foncteur','est exact sur la catégorie des','Modules quasi-cohérents','est un','Module localement libre de type fini','et la fonction de','est localement constante','Inversement','si','est noethérien et réduit','et si la fonction de','le foncteur'])
  new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve}.');new,_=underline_words(new)
  assert new!=old;r.patch(p,layer,old,new,id,why)
r.page(271,'y↦rank_k(x)H^p(E tensor^L_Xk(y))est','Modules quasi-cohérents.',notes='All six ordinary L letters, three O rules, the individual parf rule, the low placeholder, both missing outer parentheses and the stray display stop read. The opening rank-field correction has an explicit scalar-action proof.',witness=282)
r.page(272,'Preuve.D’après(4.8),Rf_*(E)est un complexe parfait.','où E_y=Li_y^*(E)(resp.i_y^*(E)).',notes='Entire page including the pasted paragraph, one O rule, three ordinary raised L letters plus ordinary baseline Li_y^*, both headed comparison arrows, all citations and the blank lower portion read.',witness=283)
r.page(273,'b)On peut développer','Complete author note1 after the three bibliography entries.',notes='All ordinary derived L letters, three small ob occurrences, coh subscript, author language tapis, the projection comparison, every bibliography word/number and the complete author note read. The following unprinted IV macro block is code, outside this page’s printed matter.',witness=284)
r.commit()
