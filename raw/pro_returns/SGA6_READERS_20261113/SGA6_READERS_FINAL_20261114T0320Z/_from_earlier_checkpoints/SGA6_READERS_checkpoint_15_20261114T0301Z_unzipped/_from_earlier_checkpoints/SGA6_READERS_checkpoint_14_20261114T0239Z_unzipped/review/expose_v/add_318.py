#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=318
r.finding('316_320',12,'The parenthetical pair is printed1+Xt,1+Xt in Ĝ(Z[X,Y]).',
 'Both scans resolve the repeated X. The second317 square compares m:Ĝ×Ĝ→Ĝ with m∘τ, where τ(α,β)=(β,α). On the independent universal pair(1+Xt,1+Yt), equation2.3.1 gives m=1+XYt and m∘τ=1+YXt; these coincide in the commutative ring Z[X,Y]. The multi-variable uniqueness of1.7/1.10 then applies to these two separately bilinear natural operations. Repeating X specializes the universal pair along Y↦X. Restore Y in the corrected universal-pair test and retain the printed repetition diplomatically.',
 'first paragraph, parenthetical commutativity test',verdict='not applied and now applied',change={'diplomatic':'1+Xt,1+Xt','current':'1+Xt,1+Yt'},witness=329)
r.patch(p,'current',r'(resp. \(1+Xt,1+Xt\) de',r'(resp. \(1+Xt,1+Yt\) de','check/findings/findings_316_320.json#12','Restore the second independent variable in the exact universal-pair commutativity test.')
r.finding('316_320',13,'The prose has lowercase p₂ with a descender; the preceding family name and following displayed polynomial use capital P.',
 'The native top crop directly contrasts p₂ with P_n and the displayed P₂. The explicit following polynomial is the n=2 member of the just-named family P_n. The attached diplomatic p₂ and corrected P₂ agree with the source glyph and this exact identification.',
 'before the P₂ display',witness=329)
r.finding('316_320',14,'On a également la relation suivante starts a separate indented paragraph.',
 'The native top crop shows the break after the displayed P₂ formula and its full stop. The attached layout agrees without changing any mathematical token.',
 'paragraph after the P₂ display',verdict='formatting observed; no content error',witness=329)
r.finding('316_320',15,'Both names of the unit have a rule under1 alone; the circle index of the second name remains outside.',
 'The native lower crop resolves the two independent short rules and the plain lower circle. The source explicitly identifies this unit with1+t using ψ(t)∘(1+1·t)=ψ(t) from2.3.2. The attached underline scope agrees.',
 'unit-naming sentence',witness=329)
r.finding('316_320',16,'The final paragraph prints lui même with a space and no hyphen.',
 'The native lower crop resolves the gap between the two words. They form the reflexive expression lui-même referring to the same functor Ĝ being composed with itself. Preserve the printed spacing diplomatically and restore the hyphen in the corrected layer.',
 'last paragraph',verdict='not applied and now applied',change={'diplomatic':'lui même','current':'lui-même'},witness=329)
r.patch(p,'current','composé avec lui même','composé avec lui-même','check/findings/findings_316_320.json#16','Restore the reflexive compound’s hyphen in the corrected layer.')
r.own_finding('ASTRA-V-SPECIALIZATION-318',p,'The source explicitly cites1.8 for coefficient substitution and1.15 for the weights of P_n; both reference numbers are retained.',
 r'Retain D’après1.8 and (voir1.15), with the exact coefficient-specialization map recorded.',
 'Retain the printed locators and their contextual identification.',
 'Section1.8 defines C₀ and the forgetful/gross-filtration functors g and i. For the ordinary polynomial ring R=Z[X_i,Y_j], the coefficient map f:R→A sends X_i↦a_i and Y_j↦b_j. Naturality of the operation gives Ĝ(f)(m_R(1+ΣX_it^i,1+ΣY_jt^j))=m_A(1+Σa_it^i,1+Σb_jt^j), so its nth coefficient is exactly P_n(a_i,b_j). This is the unfiltered specialization of the universal-polynomial calculation explicitly given in1.15, using the passage to C₀ established in1.8. The source’s contextual reference does not require a replacement number. The first formula’s three monomials, coefficient−2 and all variable indices agree with the scans.',
 'coefficient-substitution paragraph and P₂ display',kind='mathematical_context',verdict='printed reading retained; exact specialization recorded',witness=329)
r.page(p,'où la signification des flèches est évidente','pour éviter des confusions, nous',
 'Complete continuation of both squares’ proof, all triple/pair variables and hats, both reference numbers in the universal-polynomial paragraph, all inequalities in1≤i,j≤n, p₂/P₂ case distinction, entire P₂ formula and stop, capital Ob and script C_o, all ψ/a specializations in2.3.2, both unit rules and plain circle index, last script C_o, missing hyphen, and final page words compared. No author note.',
 witness='Native witness329 top/lower crops; witness_318_top.png and witness_318_lower.png')
r.commit()
