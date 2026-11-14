#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=283
r.finding('281_285',10,'2.7. Loi contravariante et structure d’anneau sur K^•, with no terminal full stop.',
 'The heading ends at the raised-dot K; no full stop follows. The attached text already preserves this punctuation. The separate word-rule patch concerns the observed heading typography.', 'heading',witness=294)
reason=('The displayed (2.7.1) maps derived K-groups by Lf*. For a flat resolution F of E, A′ tensor_{f^{-1}A} f^{-1}F represents both A′ tensor_A^L E in (2.6.5) and Lf*E; identity on that complex gives the required identification. For a finite locally free/direct-summand object E, the underived tensor A′ tensor_{f^{-1}A} f^{-1}E is f*E, giving the naive product (2.6.2) and (2.7.2). The inclusion comparison sends each such E to its degree-zero complex, which is exactly the vertical map in the printed diagram. Thus current correctly swaps only the two reference locators; diplomatic retains their printed order.')
r.finding('281_285',11,'dans (2.6.2) (resp. (2.6.5))',reason,'after (2.7.2)',witness=294)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#391','dans (2.6.2) (resp. (2.6.5))',reason,'after (2.7.2)',witness=294,change='Retain current (2.6.5) (resp. (2.6.2)); diplomatic preserves the printed order.')
r.source('fixes/RECONCILE_CODEX_6.json#287','dans (2.6.2) (resp. (2.6.5))',reason,'after (2.7.2)',witness=294,page=283,change='Confirm the existing reference swap in current only.')
for i,s,region in [(12,'est un foncteur contravariant de','end of a)'),(13,"l’homomorphisme",'first assertion word in b)'),(14,'munit','b), before K^•(X)'),(15,'d’une structure d’anneau commutatif avec unité','final line')]:
 r.finding('281_285',i,s+' underlined','The exact lexical group has a visible lower rule in both scans. Mathematical units, reference numerals and surrounding parenthetical resp. remain independently printed.',region,witness=294)
f=r.finding('281_285',2,'Eight parf occurrences on 281–283 each carry a lower rule; the A′- prefix is outside that rule.',
 'All eight named occurrences have now been directly compared: three on 281, three in (2.6.4) on 282, and two in 2.7(a) on 283. Their attached chapter parf macro gives the observed rule under parf alone. This decision is restricted to these eight occurrences and does not override the plain parf exception on 279.',
 '281 first equality and final relative categories; 282 (2.6.4); 283 2.7(a)',witness=292,change='Retain the eight inspected underlined parf forms.')
for row in r.decisions:
 if row['source_id']==f:row['image']='scan/SGA6_scan_360dpi.pdf#pages=295-297; scan/SGA6_witness_300dpi.djvu#pages=292-294'
id='ASTRA-IV-O-283'
r.own_finding(id,p,'Two individual rules below O, with X subscript outside each rule.',r'\mathcal O_X',r'\underline{O}_X',
 'The native lower-page crop shows a short horizontal rule below each O. It ends before the X subscript. Preserve these two observed glyphs explicitly without redefining any macro.', '2.7(b), opening topos and A=O_X',kind='font',witness=294)
r.patch(p,'both',r'\mathcal O_X',r'\underline{O}_X',id,'Two observed structure-sheaf glyphs with individual lower rules.',2)
id='ASTRA-IV-UNDERLINE-283'
r.own_finding(id,p,'Plain 2.7; heading lexical rule ending before K^•; four assertion word groups underlined.',
 'Bold full heading and emph assertion groups.', 'Occurrence-specific upright word rules, with independent formulas and punctuation.',
 'Main strips and native lower crop show the exact four existing emphasis boundaries; the heading number and K remain outside the title rule.', 'heading and assertions in a)/b)',witness=294)
r.patch(p,'both',r"\textbf{2.7. Loi contravariante et structure d'anneau sur \(K^{\bullet}\)}",r"2.7. \uline{Loi contravariante et structure d'anneau sur} \(K^{\bullet}\)",id,'Observed lexical title rule and plain number.')
for s in ['est un foncteur contravariant de',"l'homomorphisme",'munit',"d'une structure d'anneau commutatif avec unité"]:
 r.patch(p,'both',r'\emph{'+s+'}',r'\uline{'+s+'}',id,'Observed upright lexical underline.')
r.page(p,'2.7. Loi contravariante et structure d’anneau sur K^•','d’une structure d’anneau commutatif avec unité',
 'All prose and formulas, thirteen raised K marks, two parf rules, two O rules, all prime placements, f*/g* order and four diagram arrows compared. Reference swap is justified by the explicit tensor realization of Lf* and f*. Checker #16 is actually on 284 and will be decided there. No author note.',witness='Native witness 294 reference/diagram and lower assertion regions; witness_283_refs.png and witness_283_lower.png')
r.commit()
