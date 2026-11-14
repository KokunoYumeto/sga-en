#!/usr/bin/env python3
from review_helpers import Review,read
r=Review();p=353
r.finding('351_355',19,'Folio353 begins x-gamma^n(x prime) in(Ch A)_(n+1). En iterant;352 ends Par suite,',
 'The full main367 top and native364 top start at that formula. The preceding full352 comparison ends at the comma after suite. The attached marker is exact.',
 '352/353 boundary',witness=364)
r.finding('351_355',20,'The definition underlines classe de Chern totale de, including de on the following line.',
 'Both scans show a separate short rule under de at the next line start. The existing emph span has the correct extent; the exact lexical rule is now rendered explicitly with uline.',
 '6.7 defined term',witness=364,change='Preserve the already corrected span and render its inspected underline explicitly.')
r.finding('351_355',21,'Formula6.7.1 ends in three low dots with no additional full stop.',
 'Native364 top resolves all three dots and the blank after them. The supplied punctuation is correct; the ellipsis is made explicitly low by the local symbol patch.',
 '6.7.1 final series tail',witness=364)
tilde_reason=('The statement has plain c in both scans, while6.7.2 and the next sentence have an explicit tilde. The defined pair map is tilde-c:A→K×I(Gr A),x↦(epsilon(x),c(x)). Its first projection is epsilon and its second projection is c. The ideal inclusion i:I(Gr A)→Ch(Gr A),phi↦(0,phi), would instead have zero first projection; for x=1 its value is(0,1), while the completed map has value(1,1). Thus the augmentation-compatible map asserted in6.8 is exactly the already defined pair map tilde-c. Retain the printed plain c diplomatically and the supplied current tilde; no mathematical map is changed by this name repair.')
r.finding('351_355',22,'The Proposition6.8 arrow is labelled plain c, without tilde;both preceding uses of the completed class have tilde.',
 tilde_reason,'Proposition6.8 map label',witness=364)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#413','Plain c in6.8;tilde-c in6.7.2.',tilde_reason,'Proposition6.8 map label',page=p,witness=364)
r.source('fixes/RECONCILE_CODEX_6.json#301','Plain c in6.8;tilde-c in6.7.2.',tilde_reason,'Proposition6.8 map label',page=p,witness=364)
r.finding('351_355',23,'The final product line ends with the closing parentheses and no comma.',
 'The complete native lower and main fourth strip show the blank after the final parenthesis. The attached omission of the comma agrees.',
 'last displayed product ending',witness=364)
aggregate=next(x for x in read('decisions.jsonl') if x['source_id']=='check/findings/findings_351_355.json#10').copy()
aggregate.update(verdict='confirmed for inspected351–353 scope',printed_reading='The inspected351–353 statements have the recorded lexical rules;actual354–355 remain outside this completed scope.',
 change='Restore the five353 statement groups, in addition to the previously inspected351–352 groups;354–355 pending.',
 region='statement bodies, inspected351–353 portion')
aggregate['reason']+=' Actual353 is now fully compared:6.8 underlines La classe de Chern completee;est;un;homomorphisme de;algebres augmentees. Both K-lambda prefixes, their hyphens, the map and the final stop are unruled.'
aggregate['image']+='; scan/SGA6_scan_360dpi.pdf#page=367; scan/SGA6_witness_300dpi.djvu#page=364'
r.decisions.append(aggregate)
r.own_finding('ASTRA-V-UNDERLINE-353',p,
 'The definition has one lexical rule including de;Proposition6.8 has five word-rule groups with both K-lambda prefixes plain.',
 'Six explicit lexical uline groups.',
 'Restore the actual353 rules without changing the mathematical letters or hyphens.',
 'Native top/lower resolve all rule endpoints;the completed-class name below6.7.2 and the proof paragraphs are unruled.',
 '6.7 definition and6.8 statement',witness=364)
r.patch(p,'both',r'\emph{classe de Chern totale de}',r'\uline{classe de Chern totale de}','ASTRA-V-UNDERLINE-353','Render the inspected underline with its full existing extent.')
r.patch(p,'both','La classe de Chern complétée ',r'\uline{La classe de Chern complétée} ','ASTRA-V-UNDERLINE-353','Preserve the first statement rule.')
r.patch(p,'both',r'est un \(K\)-\(\lambda\)-homomorphisme de \(K\)-\(\lambda\)-algèbres augmentées.',r'\uline{est} \uline{un} \(K\)-\(\lambda\)-\uline{homomorphisme de} \(K\)-\(\lambda\)-\uline{algèbres augmentées}.','ASTRA-V-UNDERLINE-353','Preserve the remaining four statement rules and plain formula prefixes.')
r.own_finding('ASTRA-V-PARAGRAPH-353',p,'The paragraph locator6.7. is plain and unruled.',
 '6.7.','Restore its observed plain style.',
 'Both upper page views show the locator without rule or emphasized type;the numbered proposition label retains the accepted statement-label convention.',
 'paragraph6.7 locator',kind='font',witness=364)
r.patch(p,'both',r'\textbf{6.7.}','6.7.','ASTRA-V-PARAGRAPH-353','Preserve the plain paragraph locator.')
r.own_finding('ASTRA-V-LOW-DOTS-353',p,
 'The one complete series ellipsis and all four product dots in the final display are low.',
 r'Use \ldots and four \mathbin{.} product tokens.',
 'Preserve the observed low dots and their respective series/product roles.',
 'The native6.7.1 tail is on the baseline;the final two-line product has two low full product dots on each line. Each product joins the unchanged adjacent gamma factors.',
 '6.7.1 tail and final two product lines',kind='symbol',witness=364)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-LOW-DOTS-353','Preserve the complete low ellipsis.')
r.patch(p,'both',r'\bigr).',r'\bigr)\mathbin{.}','ASTRA-V-LOW-DOTS-353','Preserve the first line two low product dots.',count=2)
for old,new in ((r'\bigr)^{\epsilon(y)}.',r'\bigr)^{\epsilon(y)}\mathbin{.}'),(r'\bigr)^{\epsilon(x)}.',r'\bigr)^{\epsilon(x)}\mathbin{.}')):
 r.patch(p,'both',old,new,'ASTRA-V-LOW-DOTS-353','Preserve the second line low product dot.')
r.own_finding('ASTRA-V-NABLA-353',p,
 'The final binary product glyph has a closed downward triangle.',
 r'Retain \nabla at this actual353 occurrence.',
 'Confirm this local glyph without a global replacement of the typed v on326.',
 'Main fourth strip and native lower show the upper closing stroke and both sloping sides. Its operation is m_rho= rho composed with m composed with(rho inverse,rho inverse),the same map introduced on326 and used in the inspected327 formulas. The occurrence-specific retained triangle denotes that stated operation.',
 'last display binary product',kind='symbol',verdict='confirmed; source retained',witness=364)
r.page(p,'x-gamma^n(x prime) in(Ch A)_(n+1). En','final product closes with parentheses, no comma',
 'Full main367 four strips and native364 top/lower compared. Checked the p-n iteration and p+1 terminal index, plain6.7, all complete/hatted G forms and quotient prime, the widehat Gr A positive target, every i-index in6.7.1, its low tail and absent stop, both tildes in6.7.2 prose, the plain-c statement variant and exact coordinate projections, all six lexical rule groups, comma after the map, all epsilon argument factors and exponents, four low product dots, the closed final nabla and every remaining word and punctuation. No author note.',
 witness='Native364 complete body top/lower;definition rule across the line break,plain c,all product symbols resolved.')
r.commit()
