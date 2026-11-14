#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=327
for index,printed,region in [
 (6,'Si K est un λ-anneau starts a new indented paragraph after3.5.1.','paragraph before3.5.2'),
 (7,'Le n-ième polynôme universel starts a new indented paragraph after3.5.2.','paragraph before3.5.3'),
 (8,'Notons enfin starts a new indented paragraph after3.5.3.','unit paragraph')]:
 r.finding('326_330',index,printed,'Both native crops resolve the corresponding indentation and spacing. The attached paragraph break agrees without changing the formula tokens or punctuation.',region,verdict='formatting observed; no content error',witness=338)
r.finding('326_330',9,'The unit at the end of the327 unit paragraph has a short rule under1 alone; its downward-triangle index is outside the rule.',
 'The native lower crop resolves the underline, the separate closed triangle and the following full stop. The source identifies this unit as ρ_t(1+t)=1/(1−t). The attached scope agrees at this first occurrence. The remaining seven listed occurrences belong to actual328 and require that page’s separate comparison.',
 '327 unit notation only;328 continuation explicitly scoped',verdict='327 occurrence confirmed;328 occurrences separately scoped',change='Retain the inspected327 underline and its plain triangle index.',witness=338)
r.finding('326_330',10,'The quoted opérations λ at3.6 has no prime after λ.',
 'The native lower crop shows a clear interval between λ and the closing quotation. The same paragraph later assigns the notation λ′ to these λ-operations of the transported structure; its composite is Ĝ(ρ_t)∘λ_u∘ρ_t⁻¹. The attached initial unprimed λ and later primed λ agree with that explicit naming.',
 '3.6 opening quoted phrase',witness=338)
r.finding('326_330',11,'The lower horizontal λ′_u label lies above its headed rightward arrow.',
 'The native lower diagram resolves the prime, lower u and the arrowhead at the right target. The attached position and label agree.',
 '3.6.1 lower horizontal arrow',witness=338)
r.finding('326_330',12,'The right vertical label Ĝ(ρ_t) lies to the left of its downward arrow.',
 'The native lower diagram resolves the label on the interior side of the square. The upper/lower target braces, hats, t/u variables and plus indices were compared along with the arrow. The attached position agrees.',
 '3.6.1 right vertical arrow',witness=338)
r.own_finding('ASTRA-V-NUMERATOR-327',p,'The last numerator in3.5.1 is printed1+(1+X+Y+XY)t, including the extra inner1+.',
 r'Diplomatic \frac{1+(1+X+Y+XY)t}{(1+Xt)(1+Yt)}; corrected \frac{1+(X+Y+XY)t}{(1+Xt)(1+Yt)}.',
 'Remove only the inner1+ in the corrected numerator.',
 'Both main and native top images resolve this exact numerator. In R=Z[X,Y][[t]], the explicitly defined automorphism is ρ(h(t))=h(t/(1−t)). Apply it to the immediately preceding fraction: setting c=(1+X)(1+Y), its numerator becomes(1+(c−1)t)/(1−t)^2 and its denominator becomes(1+Xt)(1+Yt)/(1−t)^2. Cancellation of the unit(1−t)^2 yields exactly[1+(X+Y+XY)t]/[(1+Xt)(1+Yt)]. At X=Y=0 the preceding expression isρ(1)=1, whereas the printed final expression is1+t. The coordinator independently confirmed this exact calculation. Full source-linked derivation: review/expose_v/identification_327.json.',
 '3.5.1, final numerator',kind='misprint_in_print',witness=338)
r.patch(p,'current',r'\frac{1+(1+X+Y+XY)t}{(1+Xt)(1+Yt)}',r'\frac{1+(X+Y+XY)t}{(1+Xt)(1+Yt)}','ASTRA-V-NUMERATOR-327','Apply the explicitρ substitution to the preceding line, removing only the surplus inner1+.')
r.own_finding('ASTRA-V-PRODUCT-GLYPHS-327',p,'All five local product signs are closed downward triangles: in3.5.1,3.5.2, the polynomial paragraph, the unit paragraph and the unit index.',
 r'Retain all five \nabla occurrences on327; retain the separately observed typed v on326.',
 'Preserve the occurrence-specific glyphs and record their identical defining map.',
 'Both native crops resolve the horizontal top stroke and two descending sides of each triangle. The first line of3.5.1 explicitly identifies this product withρ(ρ⁻¹(α)∘ρ⁻¹(β)), the same m_ρ=ρ∘m∘(ρ⁻¹×ρ⁻¹) named v on326. Thus the exact map relates the different printed names while their local glyphs remain unchanged. This supplies actual327 evidence for the later-use portion of Codex297; subsequent uses remain individually scoped.',
 'all five327 product/marker occurrences',kind='symbol',verdict='printed forms confirmed and retained',witness=338)
r.source('fixes/RECONCILE_CODEX_6.json#297','The definition on326 has a typed Latin v; the five inspected occurrences on327 have closed downward triangles.',
 'The global proposed v→nabla replacement is rejected at the326 definition. The327 forms are independently confirmed as nablas, not inferred from that proposal. Both pages explicitly identify the same map m_ρ=ρ∘m∘(ρ⁻¹×ρ⁻¹), with327’s first line repeating its elementwise formula. Keep each observed glyph in its own occurrence; later usages remain outside this two-page decision.',
 '326 definition and five327 occurrences; later usages separately scoped',verdict='326 rejection confirmed;327 actual nablas confirmed; later occurrences separately scoped',change='No global glyph replacement; preserve the inspected local forms.',witness=337,page=326)
for row in r.decisions:
 if row['source_id']=='fixes/RECONCILE_CODEX_6.json#297':
  row['image']='scan/SGA6_scan_360dpi.pdf#page=340; scan/SGA6_witness_300dpi.djvu#page=337; scan/SGA6_scan_360dpi.pdf#page=341; scan/SGA6_witness_300dpi.djvu#page=338'
r.own_finding('ASTRA-V-PARAGRAPH-327',p,'The paragraph number3.6. is ordinary typed text without underline or added weight.',
 r'3.6. replaces \textbf{3.6.}.',
 'Preserve the directly observed plain paragraph-number form.',
 'Both lower scans resolve the numeral group before the quoted opérations λ phrase.',
 'paragraph number3.6',kind='font',witness=338)
r.patch(p,'both',r'\textbf{3.6.}','3.6.','ASTRA-V-PARAGRAPH-327','Preserve the inspected plain paragraph number.')
packet={
 'source_id':'ASTRA-V-NUMERATOR-327','page':327,
 'record_type':'exact_identification','verdict':'printed formula decided; current-only local correction',
 'image':['scan/SGA6_scan_360dpi.pdf#page=341','scan/SGA6_witness_300dpi.djvu#page=338'],
 'region':'3.5.1, last two lines',
 'evidence_files':['review/expose_v/page_327_s1.png','review/expose_v/witness_327_top.png','review/expose_v/witness_327_numerator.png'],
 'printed_previous':r'\rho\left(\frac{(1+(X+1)(Y+1)t)(1+t)}{(1+(X+1)t)(1+(Y+1)t)}\right)',
 'printed_last':r'\frac{1+(1+X+Y+XY)t}{(1+Xt)(1+Yt)}',
 'corrected_last':r'\frac{1+(X+Y+XY)t}{(1+Xt)(1+Yt)}',
 'ring':'R=Z[X,Y][[t]]; every displayed denominator has constant coefficient1 and is a unit.',
 'maps':{
  'rho':'h(t)↦h(t/(1−t))',
  'rho_inverse':'h(t)↦h(t/(1+t))',
  'transported_product':'m_ρ=ρ∘m∘(ρ⁻¹×ρ⁻¹), where m is the circle product of2.3',
  'specialization':'ev_(0,0):Z[X,Y][[t]]→Z[[t]], X↦0,Y↦0,t↦t'
 },
 'calculation':[
  'Put c=(1+X)(1+Y) and u=t/(1−t).',
  '(1+c u)(1+u)=[1+(c−1)t]/(1−t)^2.',
  '(1+(1+X)u)(1+(1+Y)u)=(1+Xt)(1+Yt)/(1−t)^2.',
  'Cancel the common unit denominator(1−t)^2.',
  'c−1=X+Y+XY, giving exactly the corrected final numerator.'
 ],
 'specialization_check':'At X=Y=0, the penultimate expression isρ((1+t)^2/(1+t)^2)=ρ(1)=1; the printed last expression is1+t, while the corrected last expression is1.',
 'change':'Keep the printed final expression diplomatically. In the current layer remove exactly the inner1+ and leave all other factors, signs and punctuation unchanged.',
 'forms':'French diplomatic/current and corresponding English transfer',
 'independent_review':'Coordinator independently confirmed the substitution and cancellation.'
}
(HERE/'identification_327.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'(1+Xt)∇(1+Yt)=ρ(ρ⁻¹(1+Xt)∘ρ⁻¹(1+Yt))','Elles sont définies par leur valeur pour1+Xt; on a :',
 'Every symbol in all four lines of3.5.1, exact extra inner1+ and paired correction, all five closed-triangle product signs, entire3.5.2 and3.5.3, P′_n prime placement, Z and double-stem N, both inequality bounds and weight range n…2n, comma before(1.15), all universal polynomial arguments, unit rule and plain triangle index, unprimed quoted λ, all four square arrows and labels/targets, all three chain arrows and labels, everyλ′ and final colon compared. Nominal327 findings#13/#14 belong to actual328 and are handled there. No author note.',
 witness='Native witness338 top/lower and numerator crops; witness_327_top.png, witness_327_lower.png and witness_327_numerator.png')
r.commit()
