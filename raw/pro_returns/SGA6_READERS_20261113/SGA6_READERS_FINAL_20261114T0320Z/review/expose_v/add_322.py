#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=322
r.finding('321_325',7,'Both outer1 symbols in the first displayed product have short rules; the1 inside the second braces is plain.',
 'The native top crop resolves each rule independently. The attached underlines agree; the missing1+ inside the first braces is adjudicated separately under#8.',
 'first line of the first display',witness=333)
r.finding('321_325',8,'The first brace pair encloses Xt alone, with no1+ between the left brace and X.',
 'The native top crop resolves the complete short brace group. Equation2.3.3 defines λ_u(1+Xt)=1̲+{1+Xt}u. Its coefficient-of-u map therefore sends this universal line element to1+Xt. Substitution into the first factor of the displayed product requires exactly the missing1+; the following line already uses (1+Xt)∘(1+Yt). Restore these two tokens currently and keep the printed Xt diplomatically.',
 'first line, first brace group',verdict='not applied and now applied',change={'diplomatic':r'\{Xt\}u','current':r'\{1+Xt\}u'},witness=333)
r.patch(p,'current',r'\{Xt\}u',r'\{1+Xt\}u','check/findings/findings_321_325.json#8','Restore the exact coefficient required by the defining identity2.3.3.')
r.finding('321_325',9,'The unit before {(1+Xt)∘(1+Yt)}u is underlined.',
 'The native top crop resolves the short rule under this outer1; the two inner1 symbols remain plain. The attached form agrees.',
 'second line of the first display',witness=333)
r.finding('321_325',10,'The unit before {1+XYt}u is underlined; the1 within the braces is plain.',
 'The native top crop resolves the outer rule and the plain inner coefficient. The attached form agrees with the directly read preceding line.',
 'third line of the first display',witness=333)
r.finding('321_325',11,'The two nested outer units in1̲+{1̲+{1+Xt}u}v are underlined; the innermost1 is plain.',
 'The complete native second display resolves both short rules, both brace pairs, and the final u/v positions. The attached scopes agree.',
 'display following Pour le deuxième',witness=333)
r.finding('321_325',12,'Condition2.6(ii) ends at K with no full stop.',
 'The native top crop has clear space after K. The attached omission of the stop agrees in both layers, independently of the fraction/binomial pair.',
 'end of condition2.6(ii)',witness=333)
r.finding('321_325',13,'Condition2.6(ii) prints x over a short horizontal bar with n beneath it, and no enclosing parentheses.',
 'The native top crop directly contrasts this fraction with the parenthesized binomial on the next line. Under the injection j:K→K⊗_Z Q supplied by torsion-freeness, the prescribed coefficient is [t^n]exp(j(x)Log(1+t))=j(x)(j(x)−1)…(j(x)−n+1)/n!, with coefficient1 at n=0. Thus the condition for these prescribed coefficients to descend to K is binom(x,n)∈K, as explicitly used in λ^n(x) and2.6.1. The printed fraction x/n does not supply that coefficient: for x=3,n=2 the fraction is3/2 whereas binom(3,2)=3; at n=0 the printed denominator is0. Retain the fraction diplomatically and the existing binomial correction.',
 'condition2.6(ii), fraction glyph',witness=333)
r.finding('321_325',14,'The text reads une structure de pré-λ-anneau sur K, including de at the next line’s beginning.',
 'Both lower scans show de immediately before pré. The attached restoration agrees word for word.',
 'paragraph after2.6.1',witness=333)
r.own_finding('ASTRA-V-PARAGRAPH-322',p,'The paragraph number2.6. is ordinary typed text with no underline or added weight.',
 r'2.6. replaces \textbf{2.6.}.',
 'Preserve the observed plain paragraph-number form.',
 'The native top crop resolves the same ordinary numeral strokes as the nearby2.5.a) locator. This is a paragraph number, while the separate statement-label convention applies to named labels elsewhere.',
 'paragraph number2.6',kind='font',witness=333)
r.patch(p,'both',r'\textbf{2.6.}','2.6.','ASTRA-V-PARAGRAPH-322','Preserve the inspected plain paragraph number.')
r.page(p,'qui se vérifie d’après1.10','les deux membres dans les',
 'All four lines of the first equality chain, six underlined units across the two displays, both complete nested brace structures, each λ index and G superscript v, terminal stops, item c), paragraph2.6 and conditions i)/ii), both N forms, printed fraction versus later binomial parentheses, exact0-to-infinity summation, capital Log, terminal comma, three double-stroke Q forms and both subscript Z forms, the word de, all references, and final page words compared. No author note.',
 witness='Native witness333 top/lower crops; witness_322_top.png and witness_322_lower.png')
r.commit()
