#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=337
r.finding('336_340',6,'Corollaire4.14 prints two wavy strokes, approximately-equal, between Gr^kB and Gr^kA.',
 'Main351 third strip and native348 lower crop both resolve the lower stroke as wavy as well as the upper one. The supplied approx preserves this exact glyph; the mathematical maps are recorded independently in identification_337.json.',
 'Corollaire4.14 first comparison sign',witness=348)
r.finding('336_340',5,
 'On336 the seven lemma word rules are present and4.12 has no underlined body. On337 Remarques4.13 and Corollaire4.14 likewise have no underlined body words or formulas.',
 'Both complete337 images and native348 top/lower were compared word by word. Only the labels Remarques and Corollaire have their usual rules, represented by the accepted bold statement labels. The seven336 rules remain patched. The338 statements still require their own image comparison.',
 '336 and337 inspected scope;338 continuation separately scoped',verdict='336 and337 scopes confirmed;338 continuation separately scoped',
 change='Retain the336 rule patch; no body emphasis on337.',witness=348)
r.own_finding('ASTRA-V-LOW-DOTS-337',p,
 'Four product dots are low: B.M_(k+1), the two Gr-module factors in4.14, and the later a-bar.m. The single three-dot ellipsis in4.14 is also low.',
 r'Four \mathbin{.} products and one \ldots.',
 'Restore the observed low positions, preserving every operand and index.',
 'Native348 resolves all four product marks at the lower part of the adjacent letters; the three dots between the direct-sum symbols share that baseline. Their exact occurrences were checked against the four main strips.',
 'Remarque4.13(i), Corollaire4.14 and first proof paragraph',kind='symbol',witness=348)
r.patch(p,'both',r'\cdot M',r'\mathbin{.}M','ASTRA-V-LOW-DOTS-337','Preserve the three low module-product marks.',count=3)
r.patch(p,'both',r'\bar a\cdot m',r'\bar a\mathbin{.}m','ASTRA-V-LOW-DOTS-337','Preserve the low product after a-bar.')
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-LOW-DOTS-337','Preserve the one low ellipsis.')
r.own_finding('ASTRA-V-AUTHOR-CLAIM-337',p,
 'Remarque4.13(i) calls the decomposition4.12 a direct sum; (ii) asserts4.12 for every indicated quotient; (iii) asserts its analogue for a family of variables. The proof of4.14 then invokes that decomposition for its inverse.',
 'Retain the complete source body in both layers; attach the precise dependent-claim note.',
 'Link the demonstrated4.12 obstruction to the three repeated statements and to the cited proof step. Keep the coefficient implication and graded formula separately assessed.',
 'In the exact336 example, Y3 is absent from the printed right side at k=1, as shown by e:B→Z[T],Y3↦T and all other positive generators↦0. Thus4.13(i) does not decompose all of Fil^1B. For(ii), take the zero lambda-ideal and the quotient map q=id_B. For(iii), take the singleton family and the identity renaming X1↦X. These are explicit maps back to the same counterexample. The source inverse in4.14 cannot be obtained by that displayed decomposition on the representative Y3. However Y3 belongs to Fil^3B, so its class in Gr^1B is zero; this obstruction does not refute4.14. The independent coefficient map and its two-sided inverse are proved in identification_337.json. Full scope and the failed ideal assertion on336 are recorded in author_claim_issue_337.json.',
 'Remarques4.13 and proof of Corollaire4.14',kind='author_claim_issue',verdict='source reading decided and retained; dependent defect precisely scoped',witness=348)
r.own_finding('ASTRA-V-GRADED-MAP-337',p,
 'The right-to-left map sends the class of a times a weight-i monomial m to the class of am in Gr^kB.',
 'Retain Corollaire4.14, its approximately-equal glyph and the printed proof. Record the explicit coefficient inverse outside the body.',
 'Verify the graded isomorphism independently of the erroneous finite tail in4.12.',
 'Write each b uniquely in the independent gamma-coordinate monomials m. The coefficient calculation from4.11, P-prime in3.5 and Q-prime in3.6 shows that b lies in Fil^kB exactly when its coefficient at a weight-w monomial belongs to Fil^{max(k-w,0)}A. A complete two-inclusion proof, not an assumed replacement formula, is in identification_337.json. The inverse on Gr^kB takes the coefficient at each w<=k modulo Fil^{k+1-w}A. Monomials of w>=k+1 disappear in the quotient. This map and [a]m↦[am] are well-defined and compose to identity term by term. It also proves the coefficient implication in4.13(i) for the unique monomial expansion, while leaving its claimed4.12 decomposition defect explicit.',
 'Corollaire4.14 and its coefficient maps',kind='exact_identification',verdict='retained with explicit isomorphism proof',witness=348)
proof={
 'source_id':'ASTRA-V-GRADED-MAP-337','page':337,'record_type':'exact_identification',
 'image':['scan/SGA6_scan_360dpi.pdf#page=351','scan/SGA6_witness_300dpi.djvu#page=348'],
 'source_statement':'Gr^kB approx Gr^kA direct-sum Gr^(k-1)A.M1 direct-sum ... direct-sum Gr^0A.Mk.',
 'coordinates':'B=A[Y1,Y2,...], Yj=gamma^jX, wt(Yj)=j; every polynomial has a unique finite expansion sum_m a_m m. This is the gamma-coordinate identification of4.3/4.10.',
 'coefficient_test':{
  'notation':'For this proof only, H^k is the set of finite expansions with a_m in Fil^{max(k-wt(m),0)}A. No altered4.12 statement is inserted into either source layer.',
  'multiplication':'The coefficient of mn in a_m m times b_n n lies in Fil^{max(p-wt(m),0)+max(q-wt(n),0)}A, contained in Fil^{max(p+q-wt(mn),0)}A. Consequently H^p H^q is contained in H^{p+q}; H^0=B and every H^k is an ideal.',
  'gamma_of_monomial':'For a positive-weight monomial m, iterated product polynomials P-prime_r express gamma^r(m) in gamma^l(Yj). Every such P-prime term has total input-index weight at least r by3.5. The Q-prime_(j,l) expression of gamma^l(Yj) has gamma-coordinate weight at least l by3.6. Substitution therefore gives only monomials of weight at least r, so gamma^r(m) belongs to H^r.',
  'gamma_of_coefficient_times_monomial':'Apply4.11 through the actual A-lambda-homomorphism B→B sending X to m. A term of gamma-input weight n in gamma^r(aX) has coefficient in Fil^{max(r-n,0)}A. Its substituted product of gamma^j(m) lies in H^n by the preceding step. The term is in H^r, and so is gamma^r(am).',
  'gamma_of_general_augmentation_zero_element':'Write b=a0+sum_{m positive} a_m m. Its augmentation is epsilon_A(a0), hence epsilon_B(b)=0 gives epsilon_A(a0)=0. Additivity gamma_t(b)=gamma_t(a0) product_m gamma_t(a_m m), together with gamma^r(a0) in Fil^rA and the previous step, gives gamma^r(b) in H^r. Definition3.10.1 and the ideal/product properties then give Fil^kB contained in H^k.',
  'reverse_inclusion':'A monomial m of weight w is a product of gamma^j(X) with total index w, hence belongs to Fil^wB. The inclusion A→B preserves the canonical filtrations by3.10. For w<=k, a_m in Fil^{k-w}A implies a_m m in Fil^kB. For w>=k, m is already in Fil^kB and multiplication by every a_m is allowed. Thus H^k is contained in Fil^kB.',
  'result':'The coefficient test is proved in both directions directly from the preceding definitions and polynomial identities.'
 },
 'forward_map':'For 0<=i<=k and m in M_i, send [a]m with a in Fil^{k-i}A to [am] in Fil^kB/Fil^{k+1}B.',
 'forward_well_defined':'Changing a by Fil^{k+1-i}A changes am by Fil^{k+1}B.',
 'inverse_map':'For [b] in Gr^kB, expand b=sum a_m m uniquely. For each wt(m)=i<=k, take [a_m] in Fil^{k-i}A/Fil^{k+1-i}A; discard terms of weight greater than k.',
 'inverse_well_defined':'The proved coefficient test for Fil^{k+1}B shows that every coefficient of a change of representative has zero indicated class. Terms of weight greater than k belong to Fil^{k+1}B.',
 'compositions':'The inverse after the forward map returns the same monomial and coefficient class. The forward map after the inverse differs from b only by coefficient changes and weight>k terms in Fil^{k+1}B. Both compositions are identities.',
 'scope':'This establishes the printed graded formula and the monomial-coefficient implication in4.13(i). It does not make the printed4.12 finite tail contain Y3 at k=1, and no replacement theorem or source-body emendation is proposed.'
}
(HERE/'identification_337.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
issue={
 'source_id':'ASTRA-V-AUTHOR-CLAIM-337','page':337,'record_type':'author_claim_issue',
 'verdict':'source retained with dependent obstruction demonstrated and graded claim separately verified',
 'image':['scan/SGA6_scan_360dpi.pdf#page=351','scan/SGA6_witness_300dpi.djvu#page=348'],
 'parent_issue':'review/expose_v/author_claim_issue_336.json',
 'base_example':'K=A=Z with identity augmentation, B=Z[X,Y2,Y3,...], Yj=gamma^jX, k=1. The printed4.12 right side S=ZX+B(X^2,Y2) is annihilated by e:B→Z[T],Y3↦T,all other positive generators↦0; Y3 in Fil^1B maps to T.',
 'dependent_statements':[
  {'locus':'4.13(i), first sentence','claim':'The4.12 decomposition is a direct sum of A-modules.','assessment':'The direct-sum presentation does not cover all Fil^1B: its addition map has image S and cannot hit Y3. The terms of S lie in disjoint weight ranges, but that injectivity does not supply the missing surjectivity.'},
  {'locus':'4.13(i), coefficient implication','claim':'The displayed coefficients belong to Fil^{k-j}A.','assessment':'For the unique monomial expansion this coefficient assertion follows from the explicit two-inclusion calculation in identification_337.json. It is not refuted by the failure of the preceding existence assertion.'},
  {'locus':'4.13(ii)','claim':'4.12 holds for every quotient by an augmentation-contained lambda-ideal.','assessment':'Take J=0, which is such a lambda-ideal, with q:B→B/J=B equal to the identity. The same e and Y3 give the same failure.'},
  {'locus':'4.13(iii)','claim':'The analogous4.12 statement holds for a family of indeterminates.','assessment':'Take the singleton family {X1}. The lambda-isomorphism sending X1 to X and gamma^jX1 to Yj identifies its asserted formula with the failed example exactly.'},
  {'locus':'proof of4.14','claim':'An inverse is defined by the4.12 decomposition and4.13(i).','assessment':'That cited decomposition is unavailable on the representative Y3. Its class in Gr^1B is nevertheless zero, since Y3 is in Fil^3B. Thus this is a defect in the cited construction, not a counterexample to the graded formula. The coefficient construction in identification_337.json explicitly supplies mutually inverse maps for that formula.'}
 ],
 'related_336_ideal_assertion':{
  'source':'The two paragraphs following4.12 call its right side an ideal and the family a ring filtration.',
  'test':'For k=1, X is in S but XY3 is not. Use the ordinary ring map h:B→Z[u,v]/(u^2) sending X to u,Y3 to v and all other positive generators to0. Then h(S)=Z u, while h(XY3)=uv is not in Z u; the polynomial basis modulo u^2 has independent u and uv terms.',
  'conclusion':'The stated right side is not even an ideal in this example. This explains why the following reduction cannot prove the displayed tail formula.'
 },
 'editorial_action':'Retain all source body statements in both forms; attach this scope-specific note and the independent exact graded-map proof. No replacement theorem is proposed.'
}
(HERE/'author_claim_issue_337.json').write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
r.page(p,'engendrant la filtration canonique.','ces deux fleches sont inverses l une de l autre.',
 'Complete main351 strips and native348 top/lower compared word and symbol. Checked every proof gamma/P-prime/Q-prime, all4.13 indices and punctuation, absence of statement-body underlining, the two-wavy-stroke approx, four low product marks and low ellipsis, coefficient bars and complete inverse-map paragraph. The author claims and the graded-map proof are separately documented without replacing the source body. No author note.',
 witness='Native348 top/lower: witness_337_top.png and witness_337_lower.png.')
r.commit()
