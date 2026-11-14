#!/usr/bin/env python3
import json
from review_helpers import Review,HERE
r=Review();p=356
prime_reason=('Both scans put the prime on the left N in N-prime_0=N0+d. The preceding universal generator N-prime_0 has gamma-degree at most d. Translation N0=N-prime_0+d has inverse N-prime_0=N0-d,and gives lambda_t(N0)=(1+t)^d gamma_(t/(1+t))(N-prime_0)=sum_(j=0)^d gamma^j(N-prime_0)t^j(1+t)^(d-j). Its degree is at most d,and evaluation at-1 gives lambda_(-1)(N0)=(-1)^d gamma^d(N-prime_0),exactly the identity printed below. The final prescribed map f(N-prime_0)=N-d then gives f(N0)=N. With the printed reversed relation it would instead give f(N0)=N-2d. At d=1 and N-prime_0 specialized to0,the printed relation yields N0=-1 with lambda^2(-1)=1;the corrected relation yields N0=1. Thus current restores precisely N0=N-prime_0+d;the separate final augmentation/filtration defect is not thereby repaired.')
r.finding('356_360',1,'The first line prints N-prime_0=N0+d,with the prime on the left.',
 prime_reason,'opening universal-element relation',verdict='not applied and now applied',
 change='Current restores N0=N-prime_0+d;diplomatic retains the reversed prime placement.',witness=367)
r.patch(p,'current',r"N'_0=N_0+d",r"N_0=N'_0+d",'check/findings/findings_356_360.json#1','Restore the exact translated universal element used by all subsequent formulas.')
wedge_reason=('All ten actual356 algebra-name glyphs have two unadorned sloping strokes,with their lower endpoints visibly below the neighboring capital baseline and no horizontal feet. Reproduce this local shape as an ordinary-atom wedge. It names the same augmented lambda-ring denoted Lambda in the attached TeX:the identification is the identity on every element,on multiplication,on augmentation and on every lambda operation. Consequently its Fil/Gr/Ch constructions and the two displayed maps are unchanged. This graphical decision introduces no exterior-power operation and does not infer any mathematical distinction from the shape. The actual357–360 occurrences will be decided only after those page images are viewed.')
r.finding('356_360',2,'The ten algebra-name occurrences on actual356 are small serifless wedges.',
 wedge_reason,'all actual356 algebra-name glyphs',verdict='actual356 scope decided;357–360 pending',
 change=r'Replace ten actual356 \Lambda controls by \mathord{\wedge};later pages remain unreviewed for this aggregate.',witness=367)
r.own_finding('ASTRA-V-WEDGE-356',p,
 'All ten algebra-name signs on356 are unadorned small wedges,including the four proposition occurrences,four following proof occurrences,and two final display occurrences.',
 r'Use ten \mathord{\wedge} glyphs.',
 'Preserve these ten inspected forms while keeping the named ring and every induced map identical.',
 wedge_reason,'6.11 statement,proof and final arrows',kind='symbol',witness=367)
r.patch(p,'both',r'\Lambda',r'\mathord{\wedge}','ASTRA-V-WEDGE-356','Preserve the ten local algebra-name glyphs as ordinary math atoms.',count=10)
x_reason=('Both scans print capital X as the image of X0. The preceding355 definition is X0=sum_alpha a_alpha product_j gamma^(i_j)(X_(alpha,j)),and the stated map sends each X_(alpha,j) to x_(alpha,j) while fixing a_alpha in K. Applying the lambda-map term by term gives sum_alpha a_alpha product_j gamma^(i_j)(x_(alpha,j))=x by the displayed decomposition on355. Thus the exact target element is the already specified lowercase x;retain the existing current correction and diplomatic capital.')
r.source('fixes/FIXLOG_6_CURRENT.jsonl#415','The final specialization sentence prints X0 sur X with capital target X.',x_reason,'image of X0 in final6.10 paragraph',page=p,witness=367)
r.source('fixes/RECONCILE_CODEX_6.json#303','The final specialization sentence prints X0 sur X with capital target X.',x_reason,'image of X0 in final6.10 paragraph',page=p,witness=367)
transfer_reason=('The source asserts that f:R0→R,N-prime_0↦N-d,X_(alpha,j)↦x_(alpha,j),is compatible with the lambda filtrations. In the already verified355 example K=Z,R=Z[L,L^-1],N=0,d=i=1,x=L-1,its generator U=N-prime_0 has source augmentation0 but maps to-1 with target augmentation-1. Thus it sends U in Fil^1 R0 outside Fil^1 R. For one universal augmentation-zero generator V=X0,put N0=1+U. The exact defining operation gives gamma^2(N0,V)+V=(2+U)gamma^2(V)-(1+U)V^2-UV. Every term belongs to the universal weight Fil^2. The prescribed specialization U↦-1,V↦L-1,gamma^p(V)↦0 for p>=2 sends this expression to L-1,which is outside Fil^2 R by the quotient map L↦1+u into Z[u]/(u^2). This identifies the exact failed transport in the printed proof. Its universal local calculation,with N0=N-prime_0+d,is valid;the unrestricted specialization step is retained with the defect recorded. No replacement theorem or extra hypothesis is inserted.')
r.own_finding('ASTRA-V-AUTHOR-CLAIM-CONTINUATION-356',p,
 'The final6.10 paragraph asserts filtration compatibility for the map sending N-prime_0 to N-d.',
 'Retain the asserted compatibility in both forms and attach the exact failed augmentation square.',
 'Record the actual356 continuation of the355 author-claim issue.',
 transfer_reason,'final6.10 specialization paragraph',kind='author_claim_issue',
 verdict='source decided and retained; exact transport failure recorded',witness=367)
r.own_finding('ASTRA-V-UNIVERSAL-CALCULATION-356',p,
 'The two proof displays retain gamma^d(N-prime_0),and the second has the sign(-1)^d both outside gamma^(d+i) and inside its argument.',
 'Retain the complete printed local calculation after the independently justified opening prime correction.',
 'Verify the exact sign and weight maps used before specialization.',
 'Put beta=gamma^d(N-prime_0),D=lambda_(-1)(N0)=(-1)^d beta,and C=(-1)^(d+i-1)(d+i-1)!. The first expression is(gamma^(d+i)(N0,X0)-C X0)beta. By5.5.4 it equals(-1)^d gamma^(d+i)((-1)^d X0 beta)-C X0 beta. Setting z=(-1)^d X0 beta and multiplying by the unit(-1)^d gives gamma^(d+i)(z)-Cz,the third displayed expression. The polynomial beta is an independent degree-d variable;the universal coefficient-weight filtration proved in the337–338 packets shows that multiplication by beta shifts every monomial weight by exactly d and is injective over K. Thus the initial weighted reduction and6.9 application are supported by these exact maps. This does not assert filtration preservation under the later f.',
 'three displays in universal6.10 calculation',kind='exact_identification',
 verdict='confirmed with exact maps and signs',witness=367)
packet={
 'record_type':'exact_identification','page':356,
 'source_ids':['check/findings/findings_356_360.json#1','ASTRA-V-UNIVERSAL-CALCULATION-356','ASTRA-V-AUTHOR-CLAIM-CONTINUATION-356'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=370','scan/SGA6_witness_300dpi.djvu#page=367'],
 'translated_element':prime_reason,
 'local_sign_identity':'For p=d+i,beta=gamma^d(N-prime_0),D=(-1)^d beta,C=(-1)^(p-1)(p-1)!: (gamma^p(N0,X0)-C X0)beta=(-1)^d gamma^p((-1)^d X0 beta)-C X0 beta=(-1)^d(gamma^p(z)-Cz),z=(-1)^d X0 beta.',
 'weight_injection':'In the universal polynomial ring R0,the variable beta has weight d. The map r→r beta is injective because it shifts the beta monomial exponent by1 with coefficient unchanged,and its inverse on its image removes that factor. Hence r beta has weight at least d+i+1 exactly when r has weight at least i+1. The equality of the canonical and coefficient-weight filtrations is the independently proved337–338 construction,not the defective exact-weight tail formula4.12.',
 'specialization_images':{'N-prime_0':'N-d','N0=N-prime_0+d':'N','X_(alpha,j)':'x_(alpha,j)','X0':'x'},
 'specific_transport':{
  'universal_ring':'For d=i=1,write U=N-prime_0,V=X0,N0=1+U. The polynomial generators include U of weight1 and gamma^p(V) of weight p.',
  'operation_calculation':'For a line element N0,lambda^2(N0,V)=-N0 V^2+(1+N0)lambda^2(V);this follows by expanding lambda^2(V(1-N0)) and dividing by1-N0 in the universal polynomial ring. Since gamma^2(N0,V)=lambda^2(N0,V)+V and gamma^2(V)=lambda^2(V)+V,the exact difference gamma^2(N0,V)+V is(2+U)gamma^2(V)-(1+U)V^2-UV.',
  'source_weight':'All three displayed terms have total weight at least2,so the source difference lies in Fil^2 R0.',
  'map':'f(U)=-1,f(V)=L-1,f(gamma^p(V))=0 for p>=2. The source relation gamma^k(U)=0 for k>1 is respected because gamma_t(-1)=1-t.',
  'image':'f sends the source difference to L-1;the ring map L→1+u into Z[u]/(u^2) sends this to nonzero u and kills Fil^2 R.',
  'augmentation_square':'epsilon_0(U)=0 but epsilon(f(U))=-1. The asserted filtration compatibility fails already in degree1.'
 },
 'disposition':'Make the opening prime-placement correction and retain the existing capital-X correction separately. Preserve the printed local calculation and the later false filtration-compatibility claim with the exact source/image obstruction recorded.'
}
(HERE/'identification_356.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
issue=json.loads((HERE/'author_claim_issue_355.json').read_text())
issue['continuation_356']={'source_id':'ASTRA-V-AUTHOR-CLAIM-CONTINUATION-356','image':['scan/SGA6_scan_360dpi.pdf#page=370','scan/SGA6_witness_300dpi.djvu#page=367'],'printed':'The map sending N-prime_0 to N-d is asserted to preserve the lambda filtrations.','exact_failure':packet['specific_transport'],'independent_textual_correction':'The opening relation is corrected only in current from N-prime_0=N0+d to N0=N-prime_0+d;this does not repair the unrestricted final specialization.'}
issue['disposition']='The355 statement and356 filtration-compatibility claim are decided and retained with an exact counterexample and failed transport. Only the independent prime-placement and capital-X textual slips are corrected;no new hypothesis or replacement theorem is inserted.'
(HERE/'author_claim_issue_355.json').write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
r.page(p,'et on va montrer6.10 d abord pour X0 et N-prime_0=N0+d','A→Gr(Ch A),wedge→Ch(Gr wedge).',
 'Full main370 four strips and native367 top/lower compared. Checked opening prime placement and its exact affine translation,all d+i exponents,factorials,beta primes,inside/outside signs and stops in three displays,the source specialization and capital target X,exact augmentation and filtration obstruction,plain unruled6.11 statement body,all10 lowered unadorned algebra-name wedges,the char-zero hypothesis under the locally explicit Q-algebra convention6.5,all n/k bounds,A_0/Gr^0 indices,headed lower arrows and wavy functor-assignment arrow,every remaining word and punctuation. No author note.',
 witness='Native367 top/lower complete body;opening N prime,all proof signs,capital X,and all ten small wedge glyphs resolved.')
r.commit()
