#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=330
r.finding('326_330',30,
 'Eleven lexical spans are underlined in Definition3.9: Soit; un; anneau; on appelle; la donnee d une; algebre; et d un; homomorphisme de; algebres; est un; homomorphisme compatible aux augmentations. Both defined expressions remain plain.',
 'The native341 top crop resolves each endpoint. The mathematical K, A, lambda and arrow, the connecting hyphens, the defined K-lambda-algebre augmentee and the defined homomorphisme de K-lambda-algebres augmentees are outside the rules. The final full stop also follows the rule. Restore exactly these word spans in both layers.',
 'Definition3.9 statement',verdict='confirmed and now applied',change='Apply the eleven inspected lexical rules, preserving all mathematical tokens and both plain defined terms.',witness=341)
old=(HERE/'page_330_diplomatic.tex').read_text().split('\n\n')[0].split('\n',1)[1]
new=r'''\textbf{Définition 3.9.} \uline{Soit} \(K\) \uline{un} \(\lambda\)-\uline{anneau}~; \uline{on appelle} \(K\)-\(\lambda\)-algèbre augmentée \uline{la donnée d'une} \(K\)-\(\lambda\)-\uline{algèbre} \(A\) \uline{et d'un} \(\lambda\)-\uline{homomorphisme de} \(K\)-\uline{algèbres} \(A\to K\)~; un homomorphisme de \(K\)-\(\lambda\)-algèbres augmentées \uline{est un} \(\lambda\)-\uline{homomorphisme compatible aux augmentations}.'''
r.patch(p,'both',old,new,'check/findings/findings_326_330.json#30','Restore the eleven directly observed word-group rules.')
r.finding('326_330',31,
 'All seven constant-sheaf Z occurrences are underlined and have a reinforced diagonal. The two introducing sheaf names F and F-prime have rules under F alone. The final element F-F-prime and all A, A^n, U_n remain plain.',
 'The native top and lower crops individually resolve the five Z occurrences inside H^0 and the two outside, plus both introducing F names. The supplied seven Z rules and the F-prime rule already agree; only the rule in soit alors F le faisceau is absent. The prime lies wholly outside its rule. Restore the first F locally and retain the other observed forms.',
 'Example3.9.1 constant-sheaf and module notation',verdict='confirmed; first F rule now restored',change='Underline only F in soit alors F le faisceau; retain the other eight existing rules.',witness=341)
r.patch(p,'both',r'soit alors \(F\) le faisceau',r'soit alors \(\underline{F}\) le faisceau','check/findings/findings_326_330.json#31','Restore the separately inspected first sheaf-name rule.')
r.finding('326_330',32,'The lower paragraph prints entraine with a dotted i and no circumflex.',
 'Both main344 and native341 lower crops resolve the single dot; other accents on the page are present. The supplied diplomatic entraine/current entraîne pair matches the observed spelling and its lexical correction.',
 'last paragraph, additivity of rank sentence',witness=341)
r.finding('326_330',33,'Il est immediat begins a new indented paragraph after the element F-F-prime of K-bullet(X).',
 'The native lower crop and main third strip show the indentation and intervening space. The supplied paragraph break agrees without a new content change.',
 'break before final paragraph',verdict='formatting observed; no content error',witness=341)
r.finding('331_335',2,'The opening numeral on actual331 is3.10, with no final full stop.',
 'Main345 first strip and native342 header crop show clear white space between the last zero and Soit. The attached diplomatic/current layers already pair3.10 with3.10. respectively; this is the omitted terminal paragraph-number punctuation, with the printed numeral otherwise identical. Only this header region of331 was used for this boundary decision.',
 'actual331 opening paragraph numeral',witness=342,actual_page=331)
r.source('check/findings/findings_326_330.json#34','Actual331 opens with3.10 and no terminal stop.',
 'This duplicate punctuation proposal concerns the same directly viewed header as findings_331_335#2, rather than any text on330. Retain the existing diplomatic3.10/current3.10. pair and the already corrected boundary.',
 'actual331 opening numeral',verdict='confirmed; duplicate cross-page proposal',change='No additional patch; paired forms already present.',witness=342,page=331)
r.source('fixes/MANUAL_6_findings/MANUAL_6_findings_326_330.json#1','Actual331 opens with3.10 and no terminal stop.',
 'The former old-string miss resulted from the moved330/331 marker. The directly viewed main345/native342 header and attached331 packet now contain the exact diplomatic3.10/current3.10. pair. The manual queue item is decided at its actual printed locus.',
 'actual331 opening numeral',verdict='manual queue resolved at actual331',change='Retain the paired numeral forms; no second application.',witness=342,page=331)
r.finding('326_330',35,'330 ends dans la suite. and331 begins3.10 Soit A une K-lambda-algebre augmentee.',
 'The complete330 lower image and the separate331 first-line region were compared in both scans. The attached marker precedes3.10 and agrees. The331 header view does not establish a full-page331 comparison.',
 '330/331 page boundary',witness=341)
for row in r.decisions:
 if row['source_id']=='check/findings/findings_326_330.json#35':
  row['image']='scan/SGA6_scan_360dpi.pdf#page=344; scan/SGA6_witness_300dpi.djvu#page=341; scan/SGA6_scan_360dpi.pdf#page=345; scan/SGA6_witness_300dpi.djvu#page=342'
r.page(p,'Definition3.9. Soit K un lambda-anneau','C est toujours de celle-ci qu il sera question dans la suite.',
 'Every word and symbol compared across all four main strips and both native341 crops: eleven definition rules and plain exceptions; all punctuation of the labels; eight raised-dot K occurrences; seven reinforced underlined Z occurrences; two separately underlined F names and plain F-F-prime; both A powers and all four non-strict inequalities, all U_n indices, complete augmentation/rank construction and entraine spelling. End boundary also checked against331 header only. No author note.',
 witness='Native341 top/lower: witness_330_top.png and witness_330_lower.png; regional boundary comparison with witness_331_header.png.')
r.commit()
