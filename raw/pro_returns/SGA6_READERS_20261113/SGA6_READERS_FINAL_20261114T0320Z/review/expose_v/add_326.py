#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=326
r.finding('326_330',1,'The page begins with3.3., followed by Soient K,K′ deux λ-anneaux.',
 'The main first strip and native top crop agree. The attached marker precedes3.3.; the preceding325 page ends with the coefficient equality. This confirms the same boundary already recorded under321_325#41.',
 'page boundary325/326',witness=337)
r.finding('326_330',2,'The final γ_t identity of3.3 stands in the running text at the next ordinary line, ending with a full stop.',
 'The native top crop shows ordinary line spacing and the blank before3.4. The attached inline rendering preserves the exact γ_t(f(x))=Ĝ_g(f)∘γ_t(x) tokens and punctuation; no content change follows from layout alone.',
 'end of3.3',verdict='formatting observed; no content error',witness=337)
r.finding('326_330',3,'The first paragraph prints D’après le définition3.2.ii).',
 'The native top crop resolves le, without an a. The article qualifies the feminine noun définition and refers to the explicit definition γ^n(x)=λ^n(x+n−1) in3.2(ii). Preserve le diplomatically and restore la currently.',
 'first paragraph, reference introduction',verdict='not applied and now applied',change={'diplomatic':'D’après le définition','current':'D’après la définition'},witness=337)
r.patch(p,'current',"D'après le définition","D'après la définition",'check/findings/findings_326_330.json#3','Restore the article agreeing with the explicitly referenced définition.')
r.finding('326_330',4,'The first arrow label has a low full stop between the two ρ⁻¹ symbols; the display’s closing comma has a visible descending tail.',
 'The native lower crop compares both marks directly. The first arrow is the Cartesian product map (α,β)↦(ρ⁻¹(α),ρ⁻¹(β)) from Ĝ×Ĝ to itself. Its subsequent composite is ρ∘m∘(ρ⁻¹×ρ⁻¹), with m the circle multiplication from2.3. This exact componentwise map identifies the corrected comma. Retain the printed stop in the diplomatic label and the attached comma in the corrected label.',
 '3.5, first arrow label',witness=337)
r.finding('326_330',5,'The defining sentence prints a small typed Latin v, with two sloping strokes and no closing horizontal top stroke.',
 'The native lower crop resolves the lighter typed words notée v and the following full stop. The sentence names precisely m_ρ=ρ∘m∘(ρ⁻¹×ρ⁻¹), so this glyph already has an explicit definition. Preserve v in both forms at this occurrence; no added top stroke is required to identify the operation. Later handwritten occurrences are outside this local glyph decision and will be individually compared.',
 '3.5, Cette nouvelle multiplication sera notée v',verdict='proposed glyph replacement not applied; printed definition retained',change='Retain literal v in both layers at the defining sentence.',witness=337)
r.source('fixes/RECONCILE_CODEX_6.json#297','The326 defining sentence has the typed Latin v directly observed in both scans.',
 'The queue’s rejected global v→nabla proposal is rejected at this exact definition locus. The operation is identified by m_ρ=ρ∘m∘(ρ⁻¹×ρ⁻¹), so retaining its printed name introduces no ambiguity about the map. The phrase all later uses is not adjudicated by this regional reading; later occurrences require their own image evidence.',
 'definition on326; future uses explicitly out of scope',verdict='rejection confirmed at326; later occurrences separately scoped',change='Keep the printed v here and compare subsequent glyphs locally.',witness=337,page=p)
r.own_finding('ASTRA-V-PARAGRAPHS-326',p,'The numbers3.3.,3.4. and3.5. are ordinary typed paragraph labels, with no underline or added weight.',
 r'Plain3.3.,3.4.,3.5. replace the three local textbf wrappers.',
 'Preserve the three directly observed paragraph-number forms.',
 'The main top/middle/lower strips and both native crops resolve each numeral group separately. No named theorem label is involved at these three loci.',
 'paragraph numbers3.3–3.5',kind='font',witness=337)
for n in ['3.3.','3.4.','3.5.']:
 r.patch(p,'both',r'\textbf{'+n+'}',n,'ASTRA-V-PARAGRAPHS-326','Preserve this inspected plain paragraph number.')
r.page(p,'3.3. Soient K,K′ deux λ-anneaux','sur(1+Xt,1+Yt); on a donc :',
 'Complete3.3 with prime boundaries, headed f map, double-stem N, incorrect article, all γ indices and Ĝ_g label; entire3.4.1 and p+q=n bound; all text of the transport construction, every ρ_t/γ_t occurrence and retained slash substitution; complete3.5 chain with three headed arrows, all hats, both product signs, full-stop/comma label pair, final comma, literal Latin v, independent universal pair, and terminal colon compared. The later-product glyph scope of Codex297 remains explicit. No author note.',
 witness='Native witness337 top/lower crops; witness_326_top.png and witness_326_lower.png')
r.commit()
