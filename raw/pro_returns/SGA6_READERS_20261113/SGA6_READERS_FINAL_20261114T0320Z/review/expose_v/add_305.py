#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=305
r.finding('301_305',23,'de façon que le premier facteur… begins the page.',
 'The main first strip and native top crop begin with all four words de façon que le. Page 304 ends at K[T₁,…,T_{2n}]. The attached marker already follows that exact split.',
 'page start',witness=316)
reason='Both scans type le before j-ième fonction. The feminine noun fonction is correctly resumed by la in the current layer; the same paragraph prints la i-ième fonction in its next clause. Retain the printed le diplomatically and the existing current la.'
r.finding('301_305',24,'sur le j-ième fonction symétrique',reason,'first paragraph',witness=316,change='Retain the existing le/la layer distinction.')
for sid in ['fixes/FIXLOG_6_CURRENT.jsonl#407','fixes/RECONCILE_CODEX_6.json#308']:
 r.source(sid,'sur le j-ième fonction symétrique',reason,'first paragraph',witness=316,page=p,change='Retain the existing current feminine article.')
r.finding('301_305',25,'The page ends pour l’élément; the next page begins with (1+X^{(j)}t)_{j=1,…,k}.',
 'Both complete page-305 images end at the word élément. The main first strip of 306 begins with the parenthesized family and its j-range. The attached chunks already place the entire formula after the 306 marker. This next-page regional observation does not by itself mark 306 fully checked.',
 '305/306 boundary',witness=316)
r.decisions[-1]['image']+='; scan/SGA6_scan_360dpi.pdf#page=320 (first strip only)'
for ids,printed,region in [
 (['fixes/FIXLOG_6.jsonl#379','fixes/FIXLOG_6_CURRENT.jsonl#404'],'coefficient de χ₁ (resp. χ₂)','first paragraph'),
 (['fixes/FIXLOG_6.jsonl#380','fixes/FIXLOG_6_CURRENT.jsonl#405'],'Φ(χ₁)','second displayed equality'),
 (['fixes/FIXLOG_6.jsonl#381','fixes/FIXLOG_6_CURRENT.jsonl#406'],'(resp. χ₂, i=n+1,…,2n)','end of second displayed equality')]:
 for sid in ids:
  r.source(sid,printed,
   'The native top crop resolves the curved handwritten chi strokes in these series names. The ordinary polynomial-variable capitals X_j and X_i in the surrounding text have the typewriter form. The supplied correction transcribes the observed chi in both layers without changing the displayed maps or their coefficient assignment.',
   region,witness=316,change='Retain the applied χ transcription.')
r.source('fixes/RECONCILE_CODEX_6.json#296','χ₁,χ₂,χ and f_χ,f′_χ throughout the additivity argument on 304–305.',
 'Every location in this two-page entry has now been viewed directly: the three series names and two map labels on 304, and the coefficient names, Φ(χ₁) and resp. χ₂ on 305. Their handwritten crossed curves agree with χ in the preceding definitions. The polynomial variables X_i remain capital typewriter letters; f′_χ sends the two families of elementary symmetric polynomials to the corresponding coefficients of χ₁ and χ₂, exactly as the printed first paragraph of 305 specifies. All listed repairs are supported as transcription repairs in both layers.',
 'full two-page notation family, additivity argument',witness=315,page=304,change='Retain all listed applied χ transcription repairs in both layers.')
r.decisions[-1]['image']+='; scan/SGA6_scan_360dpi.pdf#page=319; scan/SGA6_witness_300dpi.djvu#page=316'
r.own_finding('ASTRA-V-ELLIPSES-305',p,'Three groups of baseline dots occur in the expanded-series formulas.',
 r'\ldots in Φ(1+X₁t+…+X_k t^k) and both groups in the definition of φ^{(j)}.',
 'Replace these three local cdots groups by ldots.',
 'The native top crop resolves the group in the additivity conclusion; the lower crop resolves both groups in the new universal series. The other index-list ellipses are already baseline ldots and remain unchanged.',
 'expanded-series formulas',kind='symbol',witness=316)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-305','Preserve the three observed baseline ellipses.',count=3)
r.own_finding('ASTRA-V-FONT-305',p,'1.7. is plain; the integer-ring Z has a doubled diagonal; all three lowercase phi forms are open at the upper left.',
 r'1.7.; \mathbb Z; \varphi^{(j)}, (\varphi^{(j)})_j, \varphi.',
 'Remove bold weight from 1.7.; retain the observed integer and phi forms.',
 'The native lower crop resolves the ordinary paragraph-number weight, the extra diagonal stroke of Z, the three phi loops and the parenthesized j indices. Every word of 1.7 and its continuation is plain, with no lexical underline.',
 'paragraph 1.7 and final continuation',kind='font',witness=316)
r.patch(p,'both',r'\textbf{1.7.}','1.7.','ASTRA-V-FONT-305','Preserve the ordinary typed paragraph number.')
r.page(p,'de façon que le premier facteur…','ils sont déterminés par leur valeur pour l’élément',
 'All permutations and coefficient assignments, three displayed products and their bounds, the fourth product in the concluding prose, all χ/f′ forms, complete multivariable generalization, weights and indices, doubled Z and three phi shapes compared. No author note.',
 witness='Native witness316 top and lower crops; witness_305_top.png and witness_305_lower.png')
r.commit()
