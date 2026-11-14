#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=329
r.finding('326_330',22,'The first paragraph prints commumatif for3.7.1 and commutatif for3.7.2.',
 'Both scans resolve the first word letter by letter, including the extra m in place of t. The stated condition is equality of the composites Ghat^u(lambda_t) composed with lambda_u and lambda_u composed with lambda_t in the first displayed square. The neighbouring second condition spells the same adjective commutatif. Preserve commumatif diplomatically and correct this one word in the current layer.',
 'first paragraph, first diagram condition',verdict='confirmed; corrected layer now repaired',change='Current commumatif becomes commutatif; diplomatic word retained.',witness=340)
r.patch(p,'current','soit commumatif,','soit commutatif,','check/findings/findings_326_330.json#22','Repair the printed spelling in the current layer only.')
r.finding('326_330',23,'There is only blank space between the two squares, with no word et.',
 'The complete main second strip and native top crop show the space between3.7.1 and3.7.2. The attached text already removes the added conjunction.',
 'between3.7.1 and3.7.2',witness=340)
r.finding('326_330',24,'The lower horizontal label lambda_u is above the rightward headed arrow in3.7.1.',
 'Main and native images resolve the u and the arrowhead, and show the label on the upper side. All four targets and both vertical labels have been compared. The attached label position agrees.',
 '3.7.1 bottom arrow',witness=340)
r.finding('326_330',25,'The left vertical gamma_t segment of3.7.2 has no arrowhead; the other three edges of that square have heads.',
 'The native top crop resolves the lower end of the vertical stroke as a plain termination, while the neighbouring right vertical arrow has its two head branches. The map is explicitly gamma_t:A→Ghat^t(A)_nabla, x↦lambda_{t/(1-t)}(x), from3.2 and the immediately preceding description. Its source and target fix the downward orientation used in the current layer. The attached diplomatic dash/current headed arrow therefore preserve both the observed omission and the specified map.',
 '3.7.2 left vertical segment',witness=340)
r.finding('326_330',26,'The lower horizontal gamma-prime_u label is above its rightward headed arrow in3.7.2.',
 'The native top crop resolves the prime above gamma and the separate lower u. The attached label and its placement agree.',
 '3.7.2 bottom arrow',witness=340)
r.finding('326_330',27,'3.8.1 ends with exp(-xLog(1-t)) and has no terminal full stop.',
 'Both main lower strips and the native lower crop show blank space immediately after the closing parentheses. The attached absence of punctuation agrees.',
 '3.8.1 end',witness=340)
r.finding('326_330',28,'Soit a un element de K starts a new indented paragraph.',
 'Both lower scans show the indentation after3.8.1. The attached paragraph break agrees and changes no mathematical token.',
 'paragraph after3.8.1',verdict='formatting observed; no content error',witness=340)
r.finding('326_330',29,'The following unnumbered rho_t calculation ends at the outer closing parenthesis with no punctuation.',
 'Both lower scans resolve the a exponent, inner and outer closing parentheses, followed by blank space. The terminal dot occurs instead at the end of3.8.2 below. The attached punctuation agrees at both separate positions.',
 'unnumbered display between3.8.1 and3.8.2',witness=340)
r.own_finding('ASTRA-V-PARAGRAPH-329',p,'The paragraph number3.8. is plain typed text.',
 r'3.8. replaces \textbf{3.8.}.','Preserve the observed plain paragraph-number form.',
 'Main and native scans show the same weight as the surrounding typed numerals and no rule.','paragraph number3.8',kind='font',witness=340)
r.patch(p,'both',r'\textbf{3.8.}','3.8.','ASTRA-V-PARAGRAPH-329','Preserve the inspected plain paragraph number.')
r.own_finding('ASTRA-V-SLASH-329',p,'3.8.1 literally prints (1/1-t)^x with no additional denominator parentheses.',
 r'Retain (1/1-t)^x in both layers.','Keep the observed slash notation and document its exact interpretation.',
 'Under rho:h(t)↦h(t/(1-t)), the binomial-ring formula2.6.1 gives gamma_t(x)=rho((1+t)^x)=(1/(1-t))^x=exp(-xLog(1-t)). The substitution identity1+t/(1-t)=1/(1-t) identifies the printed slash expression with the adjacent exponential without adding unprinted parentheses. All identities are in(K tensor_Z Q)[[t]], and the canonical map K→K tensor_Z Q is injective for the torsion-free binomial ring defined in2.7.',
 '3.8.1 slash notation',kind='notation',verdict='printed form confirmed and retained',witness=340)
r.own_finding('ASTRA-V-PRODUCT-GLYPHS-329',p,
 'All nine local product or product-index occurrences have closed downward triangles: one in the first paragraph, four in3.7.2, and four in3.8.',
 r'Retain all nine local \nabla occurrences.','Retain the individually observed triangle glyphs.',
 'Both native crops resolve the horizontal top stroke and descending sides at each occurrence. The unnumbered calculation explicitly identifies gamma_t(a) nabla(1+Xt) with rho_t(lambda_t(a) circle rho_t inverse(1+Xt)), using the same transported product map m_rho=rho composed with m composed with(rho inverse times rho inverse) named by a typed v on326. This record concerns only the nine inspected329 occurrences.',
 'all nine329 product/marker occurrences',kind='symbol',verdict='printed forms confirmed and retained',witness=340)
r.page(p,'structure de lambda-anneau sur un anneau A','est le polynome R_n,a (2.9).',
 'All words and symbols compared in four main strips and both native340 crops. This includes the paired commumatif spelling; both complete squares, every o/triangle index, all eight arrow strokes and the missing left head, all labels and gamma prime; full3.8.1, slash notation and logarithm; both rho_t fractions and exponent;3.8.2 with upper infinity/lower n=0, binomial coefficient, X^n t^n and final dot; nine local triangle glyphs and the complete final paragraph. No author note.',
 witness='Native340 top/lower: witness_329_top.png and witness_329_lower.png.')
r.commit()
