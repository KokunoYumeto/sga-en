#!/usr/bin/env python3
import json
from review_helpers import Review,read,HERE
r=Review();p=355
r.finding('351_355',30,'The first displayed pair ends in a closing parenthesis with no full stop.',
 'Main369 first strip and native366 top show the blank after the parenthesis. The attached ending agrees;the complete low ellipsis is separately rendered at its observed height.',
 'first display ending',witness=366)
family_reason=('Both scans print z_(alpha,j),then R with no membership symbol. The immediately following generator expression and its augmentation conditions use x_(alpha,j),and the same family is used as the target of the universal generators X_(alpha,j). The index-preserving renaming z_(alpha,j)↦x_(alpha,j) identifies this one family;the generator-evaluation map sends X_(alpha,j) to that element of R. Thus the existing current x_(alpha,j) in R restores both the family label and its missing relation. The coefficient family a_alpha in K and every index remain unchanged.')
r.finding('351_355',31,'The proof prints z_(alpha,j) R,with a z and no membership symbol.',
 family_reason,'On peut trouver opening family',witness=366)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#414','Printed z_(alpha,j) R.',family_reason,'On peut trouver opening family',page=p,witness=366)
r.source('fixes/RECONCILE_CODEX_6.json#302','Printed z_(alpha,j) R.',family_reason,'On peut trouver opening family',page=p,witness=366)
r.finding('351_355',32,'No comma follows a_alpha in K before tels que.',
 'The native top and main second strip show the blank before tels. The attached punctuation agrees.',
 'coefficient-family clause',witness=366)
r.finding('351_355',33,'The universal generators are separated by a comma;there is no et and no comma before soumis.',
 'Main third strip and native lower resolve N-prime_0,X_(alpha,j) soumis. The attached comma-only list is correct. The typed lower o follows the existing index-o/0 transcription convention.',
 'universal generator list',witness=366)
aggregate=next(x for x in read('decisions.jsonl') if x['source_id']=='check/findings/findings_351_355.json#10').copy()
aggregate.update(verdict='confirmed; entire actual351–355 scope completed',
 printed_reading='All eight statement bodies on351–355 have the explicitly recorded lexical underlines;mathematics and numbered locators remain plain.',
 change='All listed351–355 lexical rules are restored occurrence by occurrence;no remaining page scope is deferred.',
 region='eight statement bodies on351–355',
 reason='Every listed page has now been personally compared in full against main/native images.351:6.6.2 La relation;est vraie pour tout element;d augmentation;6.6.3 Pour tout;est un;ideal de.352:6.6.4 Soit;l homomorphisme d augmentation de;alors;pour tout;on a;6.6.5 Avec les notations de;6.6.7 Soit;une;algebre graduee de caracteristique nulle;a degres bornes;alors les deux filtrations definies sur;sont;identiques.353:6.8 La classe de Chern completee;est;un;homomorphisme de;algebres augmentees.354:6.9 Soit;une;algebre augmentee;alors;and separate i/e rules with their periods plain.355:6.10 Soient;un anneau binomial(source circumflex separately retained);une;algebre augmentee;un element de;tel que;pour;et;Alors. Mathematical letters,formula units,K-lambda prefixes,hyphens and punctuation outside these groups are plain. Source line-break hyphenation in augmentee does not add a lexical hyphen.')
aggregate['image']+='; scan/SGA6_scan_360dpi.pdf#page=369; scan/SGA6_witness_300dpi.djvu#page=366'
r.decisions.append(aggregate)
r.own_finding('ASTRA-V-UNDERLINE-355',p,
 'Proposition6.10 underlines nine lexical groups;its K-lambda prefix,letters and mathematical clauses remain plain.',
 'Nine explicit uline groups.',
 'Restore the actual statement rules with exact endpoints.',
 'Both source views resolve Soient;un anneau binomial with a printed circumflex;une;algebre augmentee across a line break;un element de;tel que;pour;et;Alors. The statement formula itself is unruled.',
 'Proposition6.10 statement',witness=366)
old=r'Soient \(K\) un anneau binômial, \(R\) une \(K\)-\(\lambda\)-algèbre augmentée, \(N\) un élément de \(R\) tel que \(\lambda^k(N)=0\) pour \(k>d\), et \(x\in\Fil^iR\). Alors :'
new=r'\uline{Soient} \(K\) \uline{un anneau binômial}, \(R\) \uline{une} \(K\)-\(\lambda\)-\uline{algèbre augmentée}, \(N\) \uline{un élément de} \(R\) \uline{tel que} \(\lambda^k(N)=0\) \uline{pour} \(k>d\), \uline{et} \(x\in\Fil^iR\). \uline{Alors} :'
r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-355','Preserve all nine inspected lexical rule groups and unchanged formula units.')
r.own_finding('ASTRA-V-BINOMIAL-355',p,
 'The source adjective is binomial spelled binômial,with a clear circumflex over o.',
 'Diplomatic binômial;current binomial.',
 'Correct only this lexical circumflex in current.',
 'Native366 top shows the circumflex as a separate peaked stroke. The named base ring and binomial lambda operations are the same as2.7 and the explicitly linked section6 hypothesis on344. The identity map on K and on its operations is unchanged;this is the same occurrence-scoped adjective repair as344.',
 'Proposition6.10 base-ring adjective',kind='misprint_in_print',witness=366)
r.patch(p,'current','binômial','binomial','ASTRA-V-BINOMIAL-355','Repair only this observed lexical adjective spelling.')
r.own_finding('ASTRA-V-ELLIPSES-355',p,
 'All twelve complete ellipses in coefficient tails,products and index sums are low.',
 r'Use twelve \ldots controls.',
 'Preserve the baseline of the complete source ellipses.',
 'The native top/lower and four main strips resolve all twelve full three-dot groups. The existing tuple-list ldots is already low and remains unchanged.',
 'formulas throughout355',kind='symbol',witness=366)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-355','Preserve all twelve complete low ellipses.',count=12)
coefficient_reason=('The source says tilde-c(a)=(a,1),while the preceding354 coefficient a was allowed in A. The exact defined value is(epsilon(a),c(a)). For a generator product P of weight w,write tilde-c(P)=(0,phi_P),with phi_P in1+completed(Gr A)^(>=w). Formula6.1.2 gives tilde-c(a)tilde-c(P)=(0,phi_P^epsilon(a)(c(a)*phi_P)). Since c(a) has augmentation-series constant1 and positive tail of degree>=1,6.5.3 puts the extra star factor in1+degrees>=w+1. Its degree-w coefficient is therefore epsilon(a) times that of phi_P. This equals[aP] in Gr^w A because a-epsilon(a) lies in Fil^1 A. For A=Z[L,L^-1],epsilon(L)=1,and L a line element,the literal defined value is tilde-c(L)=(1,1+[L-1]),not the printed scalar-coordinate expression. The printed6.9 conclusion follows from the exact leading-degree map:iteration of6.5.3 gives the coefficient(-1)^(w-1)(w-1)![P],and only w=m contributes modulo degree m+1. Preserve the source proof,record its coefficient shorthand/omission and the exact quotient interpretation;no replacement statement is needed.')
r.own_finding('ASTRA-V-COEFFICIENT-355',p,
 'The proof states tilde-c(a)=(a,1),and its displayed coefficient expressions suppress the associated-graded class maps until the final bar z.',
 'Retain the printed proof and make the exact leading-degree projection explicit in its evidence packet.',
 'Record the coefficient issue separately from the valid6.9 conclusion.',
 coefficient_reason,'opening6.9 proof continuation',kind='author_claim_issue',
 verdict='source decided and retained; exact quotient interpretation recorded',witness=366)
claim_reason=('The source6.10 assumes only lambda^k(N)=0 for k>d,with no condition epsilon(N)=d. Take K=Z,R=Z[L,L^-1] with lambda_t(sum_j m_j L^j)=product_j(1+L^j t)^m_j and epsilon(L)=1;set N=0,d=1,i=1,x=L-1. Then D=lambda_(-1)(N)=1,and the defining section5 identity gamma^p(N,x)D=gamma^p(xD) gives gamma^2(N,x)=gamma^2(x)=0,because gamma_t(L-1)=1+(L-1)t. The printed difference is therefore x. The exact canonical filtration is Fil^q R=(L-1)^q:every augmentation-zero z is sum m_j(L^j-1),so gamma_t(z)=product(1+(L^j-1)t)^m_j has its coefficient gamma^r(z) in(L-1)^r;the reverse inclusion follows from products of gamma^1(L-1). The ring map R→Z[u]/(u^2),L→1+u,L^-1→1-u,kills Fil^2 but sends x to nonzero u. Thus this admissible data violates the printed6.10 assertion. Preserve the statement and record the exact obstruction;do not insert a missing hypothesis or a replacement theorem. Its actual356 specialization will be compared separately.')
r.own_finding('ASTRA-V-AUTHOR-CLAIM-355',p,
 'Proposition6.10 has the printed finite-lambda hypothesis on N and no augmentation value condition.',
 'Retain the entire printed6.10 statement in both forms.',
 'Record the explicit Laurent-polynomial counterexample and filtration quotient map.',
 claim_reason,'Proposition6.10 statement',kind='author_claim_issue',
 verdict='source decided and retained; exact counterexample recorded',witness=366)
coefficient_packet={
 'record_type':'exact_identification_and_proof_issue','page':355,'source_ids':['ASTRA-V-COEFFICIENT-355'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=369','scan/SGA6_witness_300dpi.djvu#page=366'],
 'source_scope':'354 quantified a in A;355 says tilde-c(a)=(a,1) and concludes6.9 with the bar z term.',
 'actual_pair':'tilde-c(a)=(epsilon(a),c(a));for a=L in the augmented line-element Laurent ring it is(1,1+[L-1]).',
 'graded_projection':'q_w:Fil^w A→Gr^w A=Fil^w A/Fil^(w+1)A. For P=product gamma^(i_j)(x_j),w=sum i_j,one has q_w(aP)=epsilon(a)q_w(P) because(a-epsilon(a))P lies in Fil^(w+1).',
 'pair_product':'tilde-c(a)(0,phi_P)=(0,phi_P^epsilon(a)(c(a)*phi_P)). The last factor has no nonzero coefficient through degree w by6.5.3.',
 'iterated_coefficient':'The degree-w coefficient of the Ch product of k rank-zero factors with degrees i_j is(-1)^(k-1)(w-1)!/product_j(i_j-1)! times the product of their leading coefficients. Each factor has leading coefficient(-1)^(i_j-1)(i_j-1)!q_(i_j)(gamma^(i_j)x_j);multiplication gives(-1)^(w-1)(w-1)!q_w(P).',
 'sum_map':'Only products of weight m contribute to Gr^m. Their coefficient sum is(-1)^(m-1)(m-1)!q_m(z),which is precisely the stated6.9 result.',
 'disposition':'Retain the source proof. Record that its displayed a as a scalar is justified only after the exact degree projection or an explicit choice of K coefficients as in3.10.2. No new textual theorem is inserted.'
}
(HERE/'identification_355.json').write_text(json.dumps(coefficient_packet,ensure_ascii=False,indent=2)+'\n')
issue={
 'record_type':'author_claim_issue','page':355,'source_ids':['ASTRA-V-AUTHOR-CLAIM-355'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=369','scan/SGA6_witness_300dpi.djvu#page=366'],
 'printed_hypotheses':'K binomial;R an augmented K-lambda-algebra;N in R with lambda^k(N)=0 for k>d;x in Fil^i R. No epsilon(N)=d condition is stated.',
 'printed_assertion':'gamma^(d+i)(N,x)-(-1)^(d+i-1)(d+i-1)!x lies in Fil^(i+1)R.',
 'example':{
  'ring':'K=Z,R=Z[L,L^-1],epsilon(L)=1. Define lambda_t(sum_j m_jL^j)=product_j(1+L^jt)^m_j for finite integer coefficient families. These are the line-element lambda operations;the universal lambda identities follow by substitution of the line powers and extension to additive inverses through reciprocals of formal series.',
  'augmentation_map':'epsilon:R→Z sends each L^j to1,and sends the displayed total lambda series to(1+t)^(sum_j m_j),so it commutes with every lambda coefficient.',
  'data':'N=0,d=1,i=1,x=L-1. All lambda^k(N) with k>=1 vanish;epsilon(x)=0 so x is in Fil^1.',
  'modified_operation':'D=lambda_(-1)(0)=1. The defining identity gamma^p(N,x)D=gamma^p(xD) therefore gives gamma^p(0,x)=gamma^p(x).',
  'ordinary_gamma':'gamma_t(L-1)=lambda_(t/(1-t))(L-1)=(1+Lt/(1-t))/(1+t/(1-t))=1+(L-1)t,hence gamma^2(x)=0.',
  'printed_difference':'For d=i=1,the printed difference is0-(-1)^1 1!x=x.'
 },
 'exact_filtration':{
  'ideal':'I=(L-1).',
  'containment':'Every augmentation-zero element z has the expression sum_j m_j(L^j-1). Each L^j-1 lies in I,also for negative j. The product gamma_t(z)=product_j(1+(L^j-1)t)^m_j shows gamma^r(z) in I^r. Every canonical-filtration generator of total index at least q therefore lies in I^q.',
  'reverse_containment':'x=L-1 has augmentation zero,and gamma^1(x)^q=x^q is a defining generator of Fil^q. Since Fil^q is an ideal,it contains I^q.',
  'identity':'Fil^q R=I^q for q>=1.',
  'separating_map':'h:R→Z[u]/(u^2) sends L to1+u,L^-1 to1-u. It is a well-defined ring map because(1+u)(1-u)=1. It kills I^2=Fil^2 and sends the asserted difference x to nonzero u.'
 },
 'relationship_to_earlier_issue':'The earlier5.7 packet author_claim_issue_343.json concerns the same absence of a prescribed augmentation for N. This example establishes the actual6.10 failure independently from its printed proof.',
 'disposition':'Source reading decided and retained. Record the exact counterexample;no corrected theorem or extra hypothesis is proposed. Actual356 continuation remains for its own direct comparison.'
}
(HERE/'author_claim_issue_355.json').write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
r.page(p,'Compte tenu de la definition de c,et de(6.6.4),on obtient:','X0=sum_alpha a_alpha product gamma^(i_j)(X_(alpha,j)),',
 'Full main369 four strips and native366 top/lower compared. Checked every factorial/sign/index in the6.9 calculation,first display absence of stop,source scalar-pair claim and exact leading-degree map,all12 complete low ellipses and the final bar z,the9 source lexical rules and circumflex,all6.10 hypotheses and absence of epsilon(N)=d,the exact Laurent-ring obstruction,printed z/no-membership variant and existing current correction,comma-free K clause,generator comma/prime/typed lower o,all inequality bounds4.9.1/4.12/4.15 citations,universal weights and final X0 formula. The universal weight-filtration identification is supported by the coefficient proof already recorded on337–338;no exact-weight4.12 tail equality is reused. No author note.',
 witness='Native366 top/lower complete body;all statement rules,source z,missing membership,bar z,primes and augmentation values resolved.')
r.commit()
