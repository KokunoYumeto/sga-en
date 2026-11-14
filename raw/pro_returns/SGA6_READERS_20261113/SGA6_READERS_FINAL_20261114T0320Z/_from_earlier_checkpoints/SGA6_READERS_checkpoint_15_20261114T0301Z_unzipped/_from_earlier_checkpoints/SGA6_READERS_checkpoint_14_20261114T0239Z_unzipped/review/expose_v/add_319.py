#!/usr/bin/env python3
from review_helpers import Review
r=Review(); p=319
r.finding('316_320',17,'The first body word is choisirons; the preceding page ends pour éviter des confusions, nous.',
 'The main top strip and native witness top agree. The attached marker is already between nous and choisirons; it preserves the observed word boundary.',
 'page boundary 318/319',witness=330)
r.finding('316_320',18,'The first 1 in the defining element has a short rule beneath it; the 1 inside braces remains plain.',
 'The native top crop resolves the independent rule under the outer unit. It matches the unit named on318 and the same defining element repeated in2.3.3 below; retain the exact attached scope.',
 'L’élément définissant le morphisme paragraph',witness=330)
r.finding('316_320',19,'In2.3.3 the first 1 on the right has a short rule; the left argument’s 1 and the 1 inside the right braces are plain.',
 'The main lower strip and native lower crop resolve all three occurrences independently. The attached underline under the outer right unit agrees, including the following plus and braces outside its scope.',
 'display2.3.3',witness=330)
r.finding('316_320',20,'Donnons à titre d’exemple la valeur de Q₂,₂ starts a new indented paragraph after2.3.3.',
 'The native lower crop shows the gap and indentation. The attached paragraph break preserves all tokens and punctuation and adds no content correction.',
 'final paragraph',verdict='formatting observed; no content error',witness=330)
r.finding('316_320',21,'All six three-dot ellipses in the ψ series and the two λ-series arguments lie on the ordinary letter baseline.',
 'Both native crops directly place the dots below the neighbouring plus signs. Apply six occurrence-scoped cdots→ldots replacements on319. The proposal’s separate comment about316 has been checked against the actual lowered wedges: those four dots also lie on the letter baseline, as recorded and patched under ASTRA-V-ELLIPSES-316. Their alignment with the tops of the lowered wedges does not change that measured relation to the letter baseline.',
 'ψ series and λ_u / λ^i arguments',verdict='not applied and now applied',change={'mapping':r'\cdots → \ldots','occurrences':6,'scope':'printed319 only;316 separately recorded'},witness=330)
r.patch(p,'both',r'\cdots',r'\ldots','check/findings/findings_316_320.json#21','Preserve six directly observed baseline ellipses on319.',count=6)
r.page(p,'choisirons des indéterminées différentes','Donnons à titre d’exemple la valeur de Q_{2,2} :',
 'All words, hats and superscript t/u order, capital Ob and script C_o, both formal-series brackets and plus exponents, headed functor arrow, F^k/F^n indices, both i≥ bounds, all six baseline ellipses, both square-bracket floor expressions [n/i], both unit rules, every λ index and Q_{i,j}/X_{ij} index, weight ij and reference1.15, complete2.3.3 and its stop, and final colon compared. The outer1 in the initial composition formula is plain. No author note.',
 witness='Native witness330 top/lower crops; witness_319_top.png and witness_319_lower.png')
r.commit()
