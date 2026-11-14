#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=324
r.finding('321_325',24,'The word following de nouvelles is printed oérations, omitting p.',
 'The native lower crop resolves the continuous letters oérations. The same sentence names the operations λ^i and introduces the operations γ^i; the section title and immediately preceding occurrence both spell opérations. Preserve the omitted letter diplomatically and restore that exact noun currently.',
 '3.1, de nouvelles oérations',verdict='not applied and now applied',change={'diplomatic':'oérations','current':'opérations'},witness=335)
r.patch(p,'current','de nouvelles oérations','de nouvelles opérations','check/findings/findings_321_325.json#24','Restore the missing p in the identified noun opérations.')
r.finding('321_325',25,'The E in si E est un fibré vectoriel has one short rule beneath the letter.',
 'The native lower crop resolves the independent rule and ordinary typed E. The attached underline agrees; the class notation on the next page is outside this particular locus.',
 'first bundle E in3.1',witness=335)
r.finding('321_325',26,'The E before devra être also has one short rule beneath the letter.',
 'The main final strip and native lower crop both resolve this second separate rule. The attached underline agrees and refers to the same rank-d vector bundle explicitly introduced above.',
 'second bundle E in3.1',witness=335)
r.own_finding('ASTRA-V-PARAGRAPH-324',p,'The paragraph number3.1. is ordinary typed text with no underline or added weight.',
 r'3.1. replaces \textbf{3.1.}.',
 'Preserve the directly observed plain paragraph-number form.',
 'The native lower crop directly shows its ordinary numeral strokes. The section title’s lexical underline is covered by the accepted section-heading convention; the gamma itself is plain.',
 'paragraph number3.1',kind='font',witness=335)
r.patch(p,'both',r'\textbf{3.1.}','3.1.','ASTRA-V-PARAGRAPH-324','Preserve the inspected plain paragraph number.')
r.page(p,'On suppose toujours que a∈K','somme alternée des puissances extérieures',
 'Full functor sentence and headed Ĝ_K arrow, all hats/indices and λ_Xt notation, full2.9.3 with0-to-infinity summation and stop, all three open-curl φ forms in2.9.4 and its semicolon, R_{n,a}, the K–λ-algebra definition and headed K→A map, full2.9.5 and its explanatory equality, title gamma, script C_o, plain3.1, missing p, all Chern prose and its two E rules, opening quotation and exact unfinished last phrase compared. The nominal324 finding#27 concerns the actual325 opening and is handled there. No author note.',
 witness='Native witness335 top/lower crops; witness_324_top.png and witness_324_lower.png')
r.commit()
