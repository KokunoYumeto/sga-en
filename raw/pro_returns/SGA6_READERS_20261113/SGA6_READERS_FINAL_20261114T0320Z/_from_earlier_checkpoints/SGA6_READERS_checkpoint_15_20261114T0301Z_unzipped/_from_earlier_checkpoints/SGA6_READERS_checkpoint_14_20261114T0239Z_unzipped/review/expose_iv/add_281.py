#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=281
items={
3:('Les hypothèses (i) et (ii)… begins a new paragraph','The indentation is visible in the main scan. The attached break preserves the observed arrangement without a mathematical change.','paragraph after the two hypotheses'),
4:('Tensor-product display immediately followed by the object-map display','There is no lexical envoie between the two displayed lines. The inherited deletion is directly verified.','2.6, two tensor displays'),
5:('f^{-1}(E) with no trailing comma','Both scans leave blank space after the terminal parenthesis. The inherited comma removal is correct.','object-map display'),
6:('induit un foncteur','Both scans begin this continuation with induit, without et.','line before (2.6.1)'),
7:('Notons D… follows (2.6.2) at the running left margin','The existing continuation arrangement agrees with the image; no further layout change is needed.','after (2.6.2)'),
8:('K^•(_A′X′_A)_{A′} = k(D(_A′X′_A)_{A′-parf} .; closing k-parenthesis omitted','The native lower crop shows the underlined parf followed by blank space and a full stop, with no final parenthesis. The corrected delimiter closes the already opened k( applied to the named category; it changes no object or map. Preserve the omission in diplomatic and the supplied closing parenthesis in current.','last display')}
for i,(a,b,c) in items.items():r.finding('281_285',i,a,b,c,witness=292)
id='ASTRA-IV-UNDERLINE-281'
r.own_finding(id,p,'2.6. Accouplements entre K^• et K^• (cas non commutatif).; only lexical title groups have rules.',
 'The complete numbered heading is bold.', 'Use plain 2.6 and underlined Accouplements entre, et, and cas non commutatif; keep both formulas, parentheses, and stop independent.',
 'Native witness 292 shows three lexical rules ending before the closing parenthesis; the numbered paragraph is plain.', '2.6 heading',witness=292)
r.patch(p,'both',r'\textbf{2.6. Accouplements entre \(K^{\bullet}\) et \(K^{\bullet}\) (cas non commutatif).}',r'2.6. \uline{Accouplements entre} \(K^{\bullet}\) \uline{et} \(K^{\bullet}\) (\uline{cas non commutatif}).',id,'Exact lexical title underlines observed in both scans.')
r.own_finding('ASTRA-IV-NOTATION-281',p,'Seven raised round K dots; three parf rules, with A′- outside the rules in the two relative occurrences.',
 'K^{\\bullet}; chapter parf macro underlines parf only.', 'Retain the inspected attached notation.',
 'All seven K marks were compared to the adjacent A′/X′ ticks; all three parf occurrences have their own lower rule. This page evidence supplements the wider queued conventions without deciding unviewed pages.',
 'heading, first equality, naive-group displays, final relative-perfect category',kind='symbol',verdict='confirmed',witness=292)
r.page(p,'(i) l’objet final de X est quasi-compact ;','K^•(_A′X′_A)_{A′} = k(D(_A′X′_A)_{A′-parf} .',
 'Complete prose, two hypotheses, bimodule sides and prime placements, tensor maps and subscripts, both numbered displays and final missing delimiter compared. No author note. Broad findings 281–285 #1 and #2 remain to be completed upon direct comparison of their remaining pages.',witness='Native witness 292 heading/tensor region and final relative-category region; witness_281_heading.png and witness_281_lower.png')
r.commit()
