#!/usr/bin/env python3
import json
from review_helpers import Review,HERE
r=Review();p=295
r.finding('291_295',24,'Six parf rules on 294 and eight on 295; all coh subscripts plain.',
 'Every occurrence in the two complete pages has been inspected. The native top/lower crops of 294 and the top/projection/lower crops of 295 show a rule beneath parf itself, with no rule beneath a subscript, prime or following comma. The attached parf mapping established at 274 reproduces these fourteen observed occurrences.',
 'all relative-perfect category subscripts on 294–295',witness=305,
 change='Confirm the explicit underlined parf form in this inspected two-page scope.')
r.decisions[-1]['image']+='; scan/SGA6_scan_360dpi.pdf#page=309; scan/SGA6_witness_300dpi.djvu#page=306'
r.finding('291_295',27,'f_*(ax)=a f_*(x), with no punctuation after the display.',
 'The main strip and native projection crop have no comma or stop after the closing parenthesis. The next line begins pour. The attached formula already agrees.',
 'projection display',witness=306)
r.finding('291_295',28,'Ordinary typed L over the tensor sign with S below.',
 'The native lower crop resolves the single ordinary L and the lower S; the attached mathrm L matches.',
 'derived tensor functor in 3.3.3',witness=306)
r.finding('291_295',29,'The last body line is K^•(f1)⊗K^•(f2)→K^•(f), followed by a stop.',
 'No opening parenthesis follows this display on 295. The directly viewed 296 begins with (Bien entendu, and the attached marker already preserves that boundary.',
 'page end',witness=306)
reason=('The source reads x∈K_•(X) in the first branch and a∈K_•(S), x∈K^•(X/S) in the second. The immediately preceding pushforward is defined on K_•(X/S). The first domain is repaired to that exact relative domain: for a=[A] perfect on S and x=[E] in K_•(X/S), ax=[E⊗^L_S A], and III3.7 identifies Rf_*E⊗^L_S A with Rf_*(E⊗^L_S A); its finite-amplitude condition holds for A. The second coefficient is retained: 3.3.2.2 applied to X→S→S pairs x=[E] in K^•(X/S) with a=[M] in K_•(S), giving [E⊗^L_S M] in K_•(X/S). Here III3.7 uses E’s finite S-amplitude, and both sides land in K_•(Y/S). The source absolute first domain fails concretely for S=Y=Spec k[x1,x2,…], X=Spec k and the closed immersion f defined by all variables: O_X is perfect over k, whereas f_*O_X=k is not finitely presented over the base ring, so the absolute pushforward does not land in D^b(Y)_coh. The complete map identification and local finite-presentation obstruction are saved in identification_295.json. Only the first missing /S is changed.')
r.source('fixes/RECONCILE_CODEX_6.json#295','First x-domain K_•(X); second coefficient K_•(S), with x∈K^•(X/S).',
 reason,'two branches following the projection formula',verdict='amended',witness=306,page=p,
 change='Apply only x∈K_•(X)→x∈K_•(X/S) in current. Reject the proposed replacement of the second coefficient K_•(S) by K^•(S).')
r.own_finding('ASTRA-IV-PROJECTION-295',p,'pour f propre, a∈K^•(S), x∈K_•(X) (resp. f propre et parfait, a∈K_•(S), x∈K^•(X/S)).',
 r'x\in K_{\bullet}(X) in the first branch; a\in K_{\bullet}(S) in the second.',
 'Supply /S only in the first x-domain of the corrected layer.',reason,
 'projection-formula domain line',kind='misprint_in_print',witness=306)
r.patch(p,'current',r'\(x\in K_{\bullet}(X)\)',r'\(x\in K_{\bullet}(X/S)\)',
 'ASTRA-IV-PROJECTION-295','Restore the exact domain of the relative pushforward already defined in 3.3.2.3; preserve the valid mixed coefficient in the second branch.')
r.own_finding('ASTRA-IV-FONT-295',p,'The O in cl(O_X) has a short rule beneath O alone.',
 r'\underline O_X', 'Replace the single calligraphic O by its observed underlined form.',
 'Both the main first strip and native top crop show the short lower rule, with the X subscript outside it.',
 'first paragraph',kind='font',witness=306)
r.patch(p,'both',r'\mathcal O_X',r'\underline O_X','ASTRA-IV-FONT-295','Preserve the actual underlined O without underlining its subscript.')
r.own_finding('ASTRA-IV-NUMBERS-294-295',p,'Numbers 3.3.2.1.–3.3.2.4. and 3.3.3. are ordinary typed numerals.',
 r'label=3.3.2.\arabic*.; ordinary 3.3.3.', 'Remove bold weight from the now fully inspected four-item enumeration and the next paragraph number.',
 'Items 1 and 2 on 294 and items 3 and 4 on 295 have all been directly compared. Their shared enumeration helper is changed only after viewing the full four-item scope; the following 3.3.3. number is also plain.',
 'numbered items on 294–295',kind='font',witness=306)
r.patch(294,'both',r'label=\textbf{3.3.2.\arabic*.}',r'label=3.3.2.\arabic*.','ASTRA-IV-NUMBERS-294-295','Preserve ordinary weight for all four directly inspected item numbers.')
r.patch(p,'both',r'\textbf{3.3.3.}',r'3.3.3.','ASTRA-IV-NUMBERS-294-295','Preserve the plain paragraph number.')
r.own_finding('ASTRA-IV-NOTATION-295',p,'Fifteen raised round K marks, eight parf rules, ordinary R and L, and superscript exclamation marks in f^!.',
 r'K^{\bullet}; underlined parf; plain R and \mathrm L; f^!.',
 'Retain the inspected notation.',
 'All pullback and pushforward maps, both projection branches, the upper shriek functor and map, and the four final pairing displays have been compared. The exclamation marks are raised and retain their separate dots; they are neither stars nor lower shrieks. No lexical emphasis or author note appears on the page.',
 'all formulas and prose',kind='symbol',verdict='confirmed',witness=306)
packet={
 'source_id':'ASTRA-IV-PROJECTION-295','related_source_id':'fixes/RECONCILE_CODEX_6.json#295','page':295,
 'status':'Printed reading decided; current-only first-domain correction; second coefficient retained',
 'printed_reading':r'pour f propre, a∈K^•(S), x∈K_•(X) (resp. f propre et parfait, a∈K_•(S), x∈K^•(X/S)).',
 'current_change':{'old':r'x\in K_{\bullet}(X)','new':r'x\in K_{\bullet}(X/S)','other_branch':'a∈K_•(S) is unchanged'},
 'evidence':[
  {'path':'review/expose_iv/page_295_s2.png','inspection':'Directly compared the source branches and preceding relative pushforward.'},
  {'path':'review/expose_iv/witness_295_projection.png','inspection':'Native witness 306 confirms every dot, subscript and absent /S.'},
  {'path':'review/expose_iv/page_294_s3.png','inspection':'Directly compared the relative-perfect/coherent pairing of 3.3.2.2.'},
  {'path':'review/expose_iv/main_247_projection_hypotheses.png','inspection':'Regional image of III3.7: finite flat amplitude for M or finite S-amplitude for E.'},
  {'path':'review/expose_iv/main_248_projection_map.png','inspection':'Regional image of the actual canonical projection isomorphism.'}
 ],
 'fixed_setting':'Use the printed S quasi-compact, X and Y of finite type over S, proper f:X→Y, g:Y→S and h=g∘f, together with the stated finiteness assumption of 3.3.2.3. The second branch also retains its printed perfectness assumption on f.',
 'first_branch':[
  'The named pushforward is F_coh:K_•(X/S)→K_•(Y/S), [E]↦[Rf_*E]. This is exactly the map displayed immediately before the formula.',
  'For a=[A] in K^•(S), Lh^*A is an absolute perfect complex on X. The product is μ_X(a,[E])=[Lh^*A⊗^L_X E]=[E⊗^L_S A] in K_•(X/S). The corresponding μ_Y uses Lg^*A. The first equality is the canonical base-change/tensor identification, with the usual derived symmetry sign on homogeneous tensor factors.',
  'III3.7 supplies π_{E,A}:Rf_*E⊗^L_S A→Rf_*(E⊗^L_S A). A has finite flat amplitude because it represents K^•(S). Passing to classes gives F_coh(μ_X(a,x))=μ_Y(a,F_coh(x)), both in K_•(Y/S).'
 ],
 'second_branch':[
  'For x=[E] in K^•(X/S) and a=[M] in K_•(S), apply 3.3.2.2 to X→S→S. The identity morphism identifies D^b(id_S)_coh with D^b(S)_coh by the identity on complexes and morphisms. Its first pairing gives T_X(x,a)=[E⊗^L_S M] in K_•(X/S); T_Y is defined in the same way.',
  'The displayed relative-perfect pushforward is F_parf:K^•(X/S)→K^•(Y/S), [E]↦[Rf_*E]. The perfectness and finiteness assumptions are kept exactly as printed.',
  'E has finite S-amplitude. Thus the other stated amplitude alternative of III3.7 applies to π_{E,M}:Rf_*E⊗^L_S M→Rf_*(E⊗^L_S M). Passing to classes gives F_coh(T_X(x,a))=T_Y(F_parf(x),a), both in K_•(Y/S). This proves that the printed coefficient K_•(S) is already the correct domain for this mixed pairing.',
  'The inclusion maps K^•(S)→K_•(S) and K^•(X/S)→K_•(X/S), induced by the identity on perfect complexes, make the two pairings agree on their common perfect-complex inputs: both produce the class of E⊗^L_S A. No inverse to either inclusion is used.'
 ],
 'counterexample_to_the_printed_first_absolute_domain':[
  'Fix a field k. Put A=k[x1,x2,…], m=(x1,x2,…), S=Y=Spec A, X=Spec(A/m)=Spec k, g=id_S and f=h the closed immersion. Both S and X are affine and hence quasi-compact; X and Y are of finite type over S. The closed immersion factors through P^0_S=S, so it is projective and proper. The printed projective finiteness case applies to its relative pushforward.',
  'The degree-zero object O_X is a rank-one free k-module, hence defines x=[O_X] in the printed absolute K_•(X). Let a=[O_S] in K^•(S); multiplication by a leaves x unchanged.',
  'The exact direct image for this closed immersion sends O_X to the A-module k=A/m. At the point m, the vector space mA_m/(mA_m)^2 has the infinitely many linearly independent classes of x1,x2,… over k. Their independence follows from the degree-one terms in the polynomial ring; denominators outside m have nonzero constant term and do not create a finite relation.',
  'Consequently mA_m cannot be generated by finitely many elements: the images of any finite generating set would span that cotangent vector space. The cyclic A_m-module k is not finitely presented, since the kernel mA_m of A_m→k is not finitely generated.',
  'A pseudo-coherent degree-zero module admits locally a finite free presentation, obtained from the degree −1 and degree 0 terms of a sufficiently accurate finite-free approximation. Therefore this k is not pseudo-coherent at m. Rf_*O_X cannot be an object of D^b(Y)_coh, so the absolute pushforward specified by the printed first domain is not defined on this x.',
  'For this closed immersion, III1.1(iii), with the subsequent smooth map id_S, identifies relative pseudo-coherence of E with absolute pseudo-coherence of f_*E. The corrected relative domain thus excludes O_X in this example, exactly where the printed absolute domain admitted it. This is a concrete obstruction to replacing the relative map by an unrestricted absolute map.'
 ],
 'scope':'Only /S in the first x-domain is supplied in current. Diplomatic retains the source. The second coefficient, hypotheses, displayed formula, and all pushforward definitions remain unchanged. The regional consultations of III247–248 create no additional full-page status.'
}
(HERE/'identification_295.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'On en déduit en particulier…','K^•(f1)⊗K^•(f2)→K^•(f).',
 'All prose, hypotheses, fifteen raised K dots, lower K dots, eight parf rules, the underlined O, ordinary R/L, upper-shriek exclamation marks, exact markers and final pairing displays compared. The printed first projection domain lacks /S; the current-only correction is justified by the named relative pushforward and a concrete obstruction. The second coefficient K_•(S) is retained with its exact mixed pairing.',
 witness='Native witness 306 top, projection and lower regions; witness_295_top.png, witness_295_projection.png and witness_295_lower.png')
r.commit()
