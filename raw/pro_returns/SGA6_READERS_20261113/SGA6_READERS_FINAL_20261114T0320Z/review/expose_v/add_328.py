#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=328
r.finding('326_330',9,
 'All eight unit numerals have a rule under 1 alone: the one on327, two 1_o in328 row3, three 1_nabla in row4, one in row5, and one in3.6.2. The indices remain outside those rules.',
 'The complete327 comparison and the native339 top crop resolve every listed rule individually. Of the seven occurrences on328, the attached layers omit the two rules in row3 and the first denominator rule in row4. Restore exactly these three; the remaining four already agree. This closes the whole327–328 scope of the finding.',
 '327 unit paragraph;328 initial display and3.6.2',verdict='confirmed; three remaining omissions now restored',
 change='Underline the two row3 unit numerals and the first denominator unit numeral in row4, in both layers.',witness=339,actual_page=328)
r.patch(p,'both',r'\frac{1_o+\{1+(X+1)t\}u}{1_o+\{1+t\}u}',r'\frac{\underline{1}_o+\{1+(X+1)t\}u}{\underline{1}_o+\{1+t\}u}',
 'check/findings/findings_326_330.json#9','Restore the two separately inspected unit rules in row3.')
r.patch(p,'both',r'\frac{\{1+Xt\}u}{1_\nabla+\underline{1}_\nabla.u}',r'\frac{\{1+Xt\}u}{\underline{1}_\nabla+\underline{1}_\nabla.u}',
 'check/findings/findings_326_330.json#9','Restore the first denominator unit rule in row4.')
r.finding('326_330',13,
 'The third row has Ghat(empty_t), with a clear blank before the subscript t; the rho drawn in the preceding two rows is absent.',
 'Both main342 and native339 resolve the empty position. The explicitly defined operation on327 is lambda-prime_u=Ghat(rho_t) composed with lambda_u composed with rho_t inverse. The first two328 rows retain that same outer Ghat(rho_t); the third merely expands lambda_u on the quotient, using lambda_u(a-b)=lambda_u(a)/lambda_u(b). Thus the omitted character is exactly rho and the already paired diplomatic empty subscript/current rho agrees with this composite.',
 'initial display, third row, outer Ghat argument',witness=339,actual_page=328)
r.finding('326_330',14,
 'In the fourth-row denominator, the second underlined1 has a closed-triangle index followed by a baseline full stop before u. No raised prime is printed there.',
 'The native339 top crop separates the low dot from the triangle and from the u. The displayed map Ghat(rho_t) sends the old unit1_o=1+t to the transported unit1_nabla=1/(1-t); its u-series denominator is1_nabla+1_nabla.u. This exact coefficient map identifies the printed factors and supports the already restored literal dot.',
 'initial display, fourth-row denominator',witness=339,actual_page=328)
r.finding('326_330',15,
 'Folio328 starts with the entire lambda-prime_u(1+Xt) aligned display;327 ends with on a :.',
 'The first main342 strip and native339 top show the display opening beneath the header. The attached marker now precedes the display opening and agrees with the observed boundary.',
 '327/328 page boundary',witness=339)
for index,printed,region in [
 (16,'Si on note gamma-prime begins a new indented paragraph after the initial display.','paragraph before3.6.2'),
 (17,'On notera Q-prime_i,j begins a new indented paragraph after3.6.2.','paragraph after3.6.2'),
 (19,'Soient K un lambda-anneau begins a new indented paragraph after the weight range j to ij.','paragraph before3.6.3'),
 (20,'On remarquera enfin begins a new indented paragraph after3.6.4.','paragraph after3.6.4')]:
 r.finding('326_330',index,printed,
  'Main and native scans show the indentation and separation. The attached paragraph break agrees; the observation entails no new mathematical or punctuation change.',
  region,verdict='formatting observed; no content error',witness=339)
r.finding('326_330',18,
 'Both triples of stops in gamma-prime^i(1+...+X_n t^n+...) are on the baseline.',
 'The main second strip and native top crop show the dots aligned with the bottoms of the adjacent typed characters. The attached two ldots commands agree.',
 'coefficient-definition paragraph',witness=339)
r.finding('326_330',21,
 'The first named functor in3.7 is Ghat with a typed small o as its index; the second has a closed downward-triangle index.',
 'The native lower crop resolves the full typed o, with the same form as the two unit indices above. The paragraph explicitly identifies Ghat_o with the structure of section2 and Ghat_nabla with its transport by rho in section3. Thus the printed names are related by the already defined isomorphism rho, and the attached local o agrees with the glyph without changing that relation.',
 '3.7 functor names',witness=339)
r.own_finding('ASTRA-V-INTEGER-FONT-328',p,
 'The coefficient ring in the Q-prime paragraph has a single typed Z. The N in3.6.3 has an additional left vertical stroke.',
 r'Use Z[X_1,\ldots,X_{ij}] at the one inspected ring occurrence; retain \mathbb N in3.6.3.',
 'Replace only the local mathbb Z with the observed plain Z in both layers.',
 'The native tight crop witness_328_Z_zoom.png and main_328_Z.png resolve one top bar, one diagonal and one lower bar, with no separately drawn additional stroke. The full native lower crop independently shows the doubled left stem of N. The exact identification of the coefficient rings is the map n↦n and X_r↦X_r for every r, preserving addition and multiplication; this font patch changes no coefficient or variable.',
 'Q-prime coefficient ring and3.6.3 index domain',kind='font',witness=339)
r.patch(p,'both',r'\mathbb Z[X_1,\ldots,X_{ij}]',r'Z[X_1,\ldots,X_{ij}]','ASTRA-V-INTEGER-FONT-328','Preserve the one inspected plain typed Z.')
r.own_finding('ASTRA-V-PARAGRAPH-328',p,
 'The paragraph number3.7. is plain typed text without an underline.',
 r'3.7. replaces \textbf{3.7.}.','Preserve the observed plain paragraph-number form.',
 'Both lower scans resolve the numeral group before Pour eviter les confusions.','paragraph number3.7',kind='font',witness=339)
r.patch(p,'both',r'\textbf{3.7.}','3.7.','ASTRA-V-PARAGRAPH-328','Preserve the inspected plain paragraph number.')
r.page(p,"lambda-prime_u(1+Xt)=Ghat(rho_t)(lambda_u(rho_t inverse(1+Xt)))",'Il resulte des considerations precedentes que pour se donner une',
 'Compared every word and symbol in all five opening rows; the missing rho, all seven unit rules, all triangle indices, the low product dot, rho inverse indices, all gamma/lambda primes,3.6.2–3.6.4 in full, coefficient t^j, isobaric bounds j and ij, plain Z and doubled-left-stem N, both paragraph references, functor names, and final continuation. All four main strips and both native339 crops viewed. No author note.',
 witness='Native339 top/lower and tight Z crops: witness_328_top.png, witness_328_lower.png, witness_328_Z.png, witness_328_Z_zoom.png; main_328_Z.png.')
r.commit()
