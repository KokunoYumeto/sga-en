#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=343
r.finding('341_345',14,'Donc begins a new indented paragraph after342 final fraction.',
 'The complete boundary images resolve the indentation. The supplied blank line after the343 marker agrees.',
 '342/343 boundary paragraph',verdict='formatting observed; no content error',witness=354)
r.finding('341_345',15,'The numerator prints(1+...+L^(k-1)), without a separately written L+ term.',
 'Main357 first strip and native354 top resolve the three dots immediately after1+. The precise polynomial represented by the abbreviation is T_k=sum_(j=0)^(k-1)L^j, fixed by(1-L)T_k=1-L^k from the previous page. Removing the extra explicit L+ preserves that exact polynomial; no term or coefficient is lost.',
 'top fraction numerator',witness=354)
r.finding('341_345',16,'The proposition has ten lexical rules: Soient; un anneau binomial; une; algebre augmentee; un element de; tel que; pour; Alors pour tout; et tout; on a.',
 'Each rule endpoint is resolved in native354 top and main first/second strips. K-lambda and its hyphens, every mathematical unit, commas and the final colon are outside the rules. The proof paragraphs are plain.',
 'Proposition5.7 statement',verdict='confirmed and now applied',change='Restore the ten inspected word rules only.',witness=354)
old=next(line for line in (HERE/'page_343_diplomatic.tex').read_text().splitlines() if line.startswith(r'\textbf{Proposition 5.7.}'))
new=r'''\textbf{Proposition 5.7.} \uline{Soient} \(K\) \uline{un anneau binomial}, \(A\) \uline{une} \(K\)-\(\lambda\)-\uline{algèbre augmentée}, \(N\) \uline{un élément de} \(A\) \uline{tel que} \(\lambda^k(N)=0\) \uline{pour} \(k>d\). \uline{Alors pour tout} \(x\in A\) \uline{et tout} \(p\ge1\), \uline{on a} :'''
r.patch(p,'both',old,new,'check/findings/findings_341_345.json#16','Restore the ten observed lexical rules without altering the retained mathematical statement.')
r.finding('341_345',17,'Soit A_0 starts a new indented proof paragraph after5.7.1.',
 'Both scans show the new paragraph; the supplied separation agrees with no changed formula tokens.',
 'after5.7.1',verdict='formatting observed; no content error',witness=354)
r.own_finding('ASTRA-V-LOW-MARKS-343',p,
 'The top geometric-polynomial ellipsis and the single product dot in the first proof display are low marks.',
 r'Use one \ldots and one \mathbin{.}.',
 'Preserve the two observed baseline mark positions.',
 'Native354 top resolves the three dots below the plus bars. The lower crop resolves the product dot after gamma^p(N0,X0) at the lower letter contour. All juxtaposed products elsewhere remain juxtaposed.',
 'top fraction and first proof display',kind='symbol',witness=354)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-LOW-MARKS-343','Preserve the one low ellipsis.')
r.patch(p,'both',r'\cdot',r'\mathbin{.}','ASTRA-V-LOW-MARKS-343','Preserve the one low product dot.')
r.own_finding('ASTRA-V-AUTHOR-CLAIM-343',p,
 'Proposition5.7 assumes only that lambda^k(N)=0 for k>d, and asserts gamma^p(N,x) in Fil^(p-d)A for every x and p>=1. Its final map is asserted to preserve augmentations while sending N-prime_0 to N-d.',
 'Retain the printed proposition and proof with their explicit counterexample and failed augmentation square; insert no replacement hypothesis or theorem.',
 'Demonstrate the precise scope defect in the statement and its transfer map.',
 'Take K=A=Z with binomial lambda-structure and epsilon=id,N=0,d=1,x=1,p=2. The stated finite-degree condition holds. Here D=lambda_(minus1)(0)=1, so5.5.4 gives gamma^2(0,1)=gamma^2(1)=lambda^2(2)=1, whereas Fil^1Z=ker(id)=0. The prescribed source map sends the generator N-prime_0, whose augmentation is0, to N-d=-1, whose target augmentation is-1. It is therefore not an augmentation-preserving map. The exact allowed specialization from the universal d=1 ring sends U=N-prime_0 to-1 and X-prime_0 to0; it sends the universal value gamma^2(N0,1)=-U in Fil^1 to1. Thus the asserted filtration transport is precisely the step that fails. Full packet: author_claim_issue_343.json.',
 'Proposition5.7 and final proof substitution',kind='author_claim_issue',verdict='source reading decided and retained; exact counterexample established',witness=354)
r.own_finding('ASTRA-V-LOCAL-CALCULATION-343',p,
 'The second proof display and its following sentence both print unprimed gamma^d(N0). The display has an outside(-1)^d but no such sign inside gamma^p.',
 'Retain these literal forms and record the exact calculation; do not silently repair primes alone.',
 'Document both the augmentation error and the nonlinear sign issue in the printed local step.',
 'Let beta=gamma^d(N-prime_0)=(-1)^d D with D=lambda_(minus1)(N0). The preceding product is exactly gamma^p(N0,X0)beta=(-1)^d gamma^p(X0D)=(-1)^d gamma^p((-1)^d X0 beta), by5.5.4. The printed gamma^d(N0) has augmentation gamma^d(d)=binom(2d-1,d), already1 at d=1, so it is not the displayed augmentation-zero factor. Even a prime-only change does not reproduce the exact expression: for d=1,p=2,X0=1,U=N-prime_0 with gamma_t(U)=1+Ut, the actual product is-U^2, the printed expression is-(1+U), and the prime-only expression is0. These values follow from gamma_t(1)=1/(1-t) and gamma_t(-U)=1/(1+Ut). The full maps and calculations accompany author_claim_issue_343.json. The universal filtration argument itself is kept separate from the failed final specialization.',
 'second proof display and following augmentation assertion',kind='author_claim_issue',verdict='literal calculation retained with exact discrepancy documented',witness=354)
issue={
 'source_id':'ASTRA-V-AUTHOR-CLAIM-343','page':343,'record_type':'author_claim_issue',
 'verdict':'source retained; statement counterexample and failed transfer map established',
 'image':['scan/SGA6_scan_360dpi.pdf#page=357','scan/SGA6_witness_300dpi.djvu#page=354'],
 'source_hypotheses':'K is binomial; A is an augmented K-lambda-algebra; lambda^k(N)=0 for k>d. No equality epsilon(N)=d is stated. The quantified x is any element of A and p>=1.',
 'source_claim':'gamma^p(N,x) belongs to Fil^(p-d)A.',
 'counterexample':{
  'K_and_A':'K=A=Z with lambda_t(a)=(1+t)^a and epsilon_A=id_Z.',
  'parameters':{'N':0,'d':1,'x':1,'p':2},
  'hypothesis_check':'lambda^k(0)=0 for every k>=1, hence for every k>d.',
  'operation_value':'D=lambda_(minus1)(0)=1. Relation5.5.4 therefore gives gamma^2(N,x)=gamma^2(1)=lambda^2(1+2-1)=binom(2,2)=1.',
  'filtration_value':'Fil^(p-d)A=Fil^1Z=ker(epsilon_A)=0 by3.10.',
  'conclusion':'The required membership is1 in0, which fails.'
 },
 'failed_augmentation_square':{
  'source':'A0 has epsilon0(N-prime_0)=epsilon0(X-prime_0)=0 and N0=N-prime_0+d,X0=X-prime_0+epsilon_A(x).',
  'printed_map':'f:A0→A,N-prime_0↦N-d,X-prime_0↦x-epsilon_A(x).',
  'comparison_on_generator':'epsilon_A(f(N-prime_0))=epsilon_A(N)-d, whereas epsilon0(N-prime_0)=0. In the concrete example these are-1 and0.',
  'explicit_lambda_specialization':'For d=1 write U=N-prime_0. The relation gamma^k(U)=0 for k>1 is satisfied by U↦-1 because gamma_t(-1)=1-t. Send X-prime_0 and its higher gamma-coordinates to0. This is the actual lambda-specialization f, sending N0=U+1 to0 and X0=1 to1, but it does not commute with the augmentations.',
  'filtration_failure':'The universal value gamma^2(N0,1)=-U is of weight1 and lies in Fil^1A0. Its image under f is1, outside Fil^1Z. This is the exact failed transport, rather than an unrelated counterexample.'
 },
 'local_display_discrepancy':{
  'printed':'(-1)^d gamma^p(X0 gamma^d(N0)) in Fil^pA0; the following sentence calls gamma^d(N0) augmentation-zero.',
  'exact_identity':'Set beta=gamma^d(N-prime_0)=(-1)^d D. Then gamma^p(N0,X0)beta=(-1)^d gamma^p(X0D)=(-1)^d gamma^p((-1)^d X0 beta).',
  'augmentation':'epsilon0(N0)=d, hence epsilon0(gamma^d(N0))=gamma^d(d)=binom(2d-1,d). For d=1 it equals1.',
  'degree_two_calculation':'In the d=1 quotient R=Z[U], N0=U+1 is a line element, gamma_t(U)=1+Ut. Specialize X-prime_0↦0 and epsilon_A(x)=1, so X0=1. Then gamma_t(N0)=(1+Ut)/(1-t), gamma_t(-U)=1/(1+Ut), and gamma^2(N0,1)=1-N0=-U. The preceding product equals-U^2; the printed expression is-gamma^2(N0)=-(1+U); changing only N0 to N-prime_0 would give-gamma^2(U)=0.',
  'disposition':'Record the two exact unprimed occurrences and the required nonlinear sign calculation outside the body. No isolated prime-only or guessed theorem repair is applied.'
 },
 'weight_filtration_reference':{
  'source':'The universal ring is a polynomial ring in the indicated gamma-coordinates, with canonical filtration equal to their weight filtration.',
  'verification':'The coefficient proof in identification_337.json applies successively to the two free gamma-variable families; the quotient killing gamma^k(N-prime_0) for k>d preserves the weight filtration by the explicit quotient argument in author_claim_issue_338.json. Multiplication by the independent weight-d variable beta is injective and shifts every monomial weight by exactly d. This verifies the universal weighted step without using the defective finite tail of4.12.',
  'scope':'The failure demonstrated here is the printed local expression and the claimed final augmentation-compatible specialization, not the polynomial-coordinate weight description.'
 },
 'editorial_action':'Retain the full proposition and proof in both forms with the explicit defect note. No replacement hypothesis, replacement theorem or source-body reconstruction is proposed.'
}
(HERE/'author_claim_issue_343.json').write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
r.page(p,'Donc lambda^p(N+L,x) est le coefficient','donc N0 sur N et X0',
 'All four main357 strips and native354 top/lower compared. Checked the omitted explicit L term in the geometric abbreviation, fraction bounds and stop, ten proposition word rules, all prime/subscript combinations in A0 and its generators, epsilon-labelled headed map, each coordinate weight, the first primed beta display, both later unprimed gamma^d(N0) occurrences and outside sign, absent stop after the second display, claimed augmentation compatibility and final unfinished phrase. The exact author-claim defects are recorded independently of scan completeness. No author note.',
 witness='Native354 top/lower: witness_343_top.png and witness_343_lower.png.')
r.commit()
