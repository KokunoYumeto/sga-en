#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=339
r.finding('336_340',11,'L element starts a new indented paragraph after equation5.3.1.',
 'Both main353 and native350 show the gap and indentation. The supplied paragraph separation agrees; the mathematical tokens and the equation stop are unchanged.',
 'after5.3.1',verdict='formatting observed; no content error',witness=350)
r.finding('336_340',12,'The last line literally prints par substitution, on encore en utilisant.',
 'Main fourth strip and native350 lower show n in on, not u. The two descriptions refer to the same evaluation: the unique lambda-homomorphism sends N to N-double-prime and x to x-double-prime, hence each lambda-coordinate to its named image, exactly polynomial substitution. Preserve on diplomatically and repair the disjunction to ou in current.',
 'last line before340',verdict='confirmed and now applied in current',change='Current on encore becomes ou encore; diplomatic retains on.',witness=350)
r.patch(p,'current','par substitution, on encore en utilisant','par substitution, ou encore en utilisant','check/findings/findings_336_340.json#12','Repair the printed conjunction while preserving the exact common evaluation map.')
r.own_finding('ASTRA-V-LOW-DOTS-339',p,
 'Three products are printed with low dots: the two in5.3.1 and the later x-times-lambda-minus-one in the following paragraph.',
 r'Use three \mathbin{.} controls.',
 'Preserve their observed baseline position.',
 'Native350 top/lower and the main second/third strips locate all three dots below the equality bars and beside the lower letter contours. The operands remain unchanged.',
 '5.3.1 and immediately following paragraph',kind='symbol',witness=350)
r.patch(p,'both',r'\cdot',r'\mathbin{.}','ASTRA-V-LOW-DOTS-339','Preserve all three inspected low product marks.',count=3)
r.own_finding('ASTRA-V-PARAGRAPH-LABEL-339',p,
 'The label5.3 is ordinary unruled type.',
 r'5.3. instead of \textbf{5.3.}.',
 'Restore the directly observed paragraph-label form.',
 'The main and native second regions show neither a rule nor reinforced weight beneath or around the numbered paragraph label.',
 '5.3 label',kind='convention',witness=350)
r.patch(p,'both',r'\textbf{5.3.}',r'5.3.','ASTRA-V-PARAGRAPH-LABEL-339','Preserve the ordinary numbered paragraph.')
r.own_finding('ASTRA-V-AUTHOR-CLAIM-339',p,
 'The opening sentence says that f is injective and identifies A with the symmetric polynomials in the N_i;338 defines A with the independent x and its higher lambda-coordinates, but B with only the N_i.',
 'Retain the complete source proof and add the explicit domain issue, restricted morphism and verification of the lemma actually used.',
 'Demonstrate the failure for the printed full A without changing the stated divisibility lemma.',
 'Set d=1. Then A=Z[N,x,lambda^2x,...], B=Z[N1], and every map with N↦N1 has x↦p(N1) for a polynomial p, hence kills the nonzero polynomial x-p(N). In particular the allowed lambda-map N↦N1,x↦0 kills x. The preceding reduction only uses the subring A0=Z[N,...,lambda^dN]. Its lambda-map f0 into B sends lambda^kN to the elementary symmetric polynomial e_k. The leading-monomial argument in author_claim_issue_339.json proves injectivity and image B^{S_d}. Evaluating N_i↦1 is a lambda-map and makes lambda_{-1}(N) zero, so each positive lambda coefficient has every factor1-N_i. The product divides in B; the quotient is symmetric by cancellation, descends to A0, then to A. The weighted P_p expression then proves the full5.2 divisibility with x. This verifies the lemma through explicit maps while retaining the printed overbroad injectivity claim with its defect noted.',
 '338 final construction and339 first two paragraphs',kind='author_claim_issue',verdict='source reading retained; domain defect demonstrated and reduced lemma verified',witness=350)
issue={
 'source_id':'ASTRA-V-AUTHOR-CLAIM-339','page':339,'record_type':'author_claim_issue',
 'verdict':'printed reading retained; full-domain injectivity fails; exact restricted argument proves the divisibility used',
 'image':['scan/SGA6_scan_360dpi.pdf#page=352','scan/SGA6_scan_360dpi.pdf#page=353','scan/SGA6_witness_300dpi.djvu#page=349','scan/SGA6_witness_300dpi.djvu#page=350'],
 'source_definitions':{
  '338_5.1':'A=Z[N,...,lambda^dN; x,...,lambda^jx,...], with only lambda^iN=0 for i>d.',
  '338_B':'B is generated over Z by N1,...,Nd with lambda^i(Nj)=0 for i>=2, hence B=Z[N1,...,Nd].',
  '338_map':'The displayed f:A→B is specified on N by N↦sum_i Ni; no image of x is stated.',
  '339_claim':'f is injective and identifies A with the ring of symmetric polynomials in the Ni.'
 },
 'explicit_obstruction':{
  'd':1,
  'rings':'A=Z[N,x,lambda^2x,...]; B=Z[N1].',
  'every_extension':'A map with N↦N1 sends x to some p(N1) in B. The element x-p(N) is nonzero in the displayed independent polynomial coordinates of A and maps to0.',
  'concrete_lambda_map':'Choose f(N)=N1 and f(x)=0. The source relations hold, so4.7 supplies the lambda-map. It kills the nonzero variable x.',
  'conclusion':'No such full-domain map is injective for this allowed d, and the printed assertion cannot follow from the elementary-symmetric images of the N-coordinates alone.'
 },
 'exact_restricted_morphism':{
  'domain':'A0=Z[N,lambda^2N,...,lambda^dN], the actual lambda-subring generated by N; its inclusion j:A0→A sends every coordinate to the identical coordinate.',
  'map':'f0:A0→B,lambda^kN↦e_k(N1,...,Nd), defined by N↦sum_i Ni. It equals f composed with j for every extension f in the source construction.',
  'injectivity':'Order N1>...>Nd lexicographically. The leading monomial of e_k is N1...Nk. Thus the leading exponent vector of e_1^{a1}...e_d^{ad} is(a1+...+ad,a2+...+ad,...,ad). The triangular map from(a1,...,ad) is injective, so distinct monomials in the independent A0 coordinates have distinct leading monomials; no nonzero polynomial relation maps to0.',
  'image':'Every e_k is symmetric. Conversely a symmetric polynomial has lexicographically leading exponent vector b1>=...>=bd. Subtract its leading coefficient times e1^{b1-b2}e2^{b2-b3}...ed^{bd}. This removes the leading symmetric orbit while preserving integrality and degree. Iteration in each finite degree terminates, expressing the polynomial over Z in the e_k. Therefore the image is exactly B^{S_d}.'
 },
 'divisibility_verification':{
  'element':'D=lambda_{-1}(N) in A0 maps to product_i(1-N_i). For p>=1 put R_p=f0(lambda^p(D)).',
  'evaluations':'For each i, e_i:B→Z[N1,...,omit Ni,...,Nd] sends Ni↦1 and every other Nj to itself. All target images are line elements, so e_i is a lambda-map by the defining relations. It sends f0(D) to0 and therefore e_i(R_p)=lambda^p(0)=0.',
  'factor_product':'Each1-N_i divides R_p by polynomial division in Ni. These factors are distinct nonassociate primes in the polynomial ring over Z; hence their product divides R_p. Write R_p=f0(D)Q_p with Q_p in B.',
  'symmetric_descent':'Both R_p and f0(D) are symmetric. For every permutation sigma, f0(D)(sigma(Q_p)-Q_p)=0. B is an integral domain and f0(D) is nonzero, so Q_p is symmetric. The proved image description gives Q_p=f0(q_p) for q_p in A0; injectivity then gives lambda^p(D)=D q_p in A0 and hence in A.',
  'x_extension':'The2.3 polynomial P_p(lambda^ix,lambda^jD) is of positive weight p in its second family. Every monomial therefore contains at least one positive lambda^j(D), each divisible by D. Consequently lambda^p(xD) is divisible by D in the full A, exactly the assertion of5.2.'
 },
 'editorial_action':'Preserve the source body in both forms, including the full-A injectivity sentence. Add this explicit domain note and the exact restricted proof; introduce no replacement theorem or guessed image of x into the source.'
}
(HERE/'author_claim_issue_339.json').write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
r.page(p,'ce qui montre que pour1<=k<=d','lambda-homomorphisme de A dans',
 'Complete four main353 strips and native350 top/lower compared. Checked the exact full-A injectivity assertion, every product bound and N_i substitution, ordinary5.3, equation5.3.1 and its three low dots, all primes in the A-prime map, its headed arrow, reinforced integer-ring Z, both d and d-prime inequalities, N-double-prime/x-double-prime, literal on encore and final unfinished phrase. No underlined body span or author note occurs.',
 witness='Native350 top/lower: witness_339_top.png and witness_339_lower.png.')
r.commit()
