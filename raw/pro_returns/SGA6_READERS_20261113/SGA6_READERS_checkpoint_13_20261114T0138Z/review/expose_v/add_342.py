#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=342
r.finding('341_345',9,'The membership glyph after x has two uninterrupted legs, no crossbar and no apex spur: capital Lambda.',
 'The native tight crop and nearest-neighbour zoom, together with the main tight crop, resolve the empty interior throughout the expected crossbar region. The other A letters on the page have a crossbar. Preserve Lambda diplomatically. The argument is the element(0,x) of Z⊕A, so its actual coordinate domain is A under the explicitly stated inclusion x↦(0,x); retain current A.',
 'second paragraph, x membership',change='Retain diplomatic Lambda and current A.',witness=353)
r.finding('341_345',10,'A detached round stop occurs immediately after the fraction bar of(1+t)/(1+Lt), before et on applique.',
 'The native fraction-stop zoom resolves the short white gap between the bar and the round ink mark; the main detail corroborates it. No comma tail is visible. The paired diplomatic full stop and current comma preserve the source punctuation and the continuing coordinated clause respectively.',
 '5.6 explanatory parenthesis',change='Retain diplomatic stop and current comma.',witness=353)
r.finding('341_345',11,'The fourth-line denominator ends with plus followed by two dots; the numerator ends with three dots.',
 'Main fourth strip and native353 lower resolve exactly two denominator dots, against the three earlier ellipses. The formal denominator is the full series lambda_(Lt)(xD)=1+sum_{k>=1}lambda^k(xD)L^k t^k; its complete three-dot notation in current represents this same coefficientwise series. Retain the literal two-dot diplomatic ending.',
 '5.6 fourth-line denominator',change='Retain diplomatic two dots and current three-dot ellipsis.',witness=353)
r.finding('341_345',12,'The last fraction has no terminal punctuation.',
 'Both main bottom strip and native lower image show blank space after the denominator. The supplied absence of a full stop agrees.',
 'page-final fraction',witness=353)
r.finding('341_345',13,'The last denominator has two distinct product dots between lambda_(minus1)(N) and L^k; the second is lighter.',
 'Both scans resolve the two dots and their separation. The denominator is exactly lambda_(Lt)(xD)=1+sum_{k>=1}lambda^k(N,x)D L^k t^k by5.3.1, so there is one multiplication of D and L^k. Preserve both source dots in diplomatic and the single product in current.',
 'last denominator, doubled product dot',change='Retain diplomatic two low dots and current one low dot.',witness=353)
r.own_finding('ASTRA-V-GAMMA-EXPONENT-342',p,
 'The formula for gamma^p(0,x) literally sums i=0 to p-1 with coefficient binom(p-1,i) and factor lambda^i(N,x).',
 r'Current factor \lambda^{p-i}(N,x); diplomatic \lambda^i(N,x), with identical bounds and binomial coefficient.',
 'Repair only the exponent in the current summand.',
 'Main second strip and native353 top clearly resolve the exponent i without a preceding p-minus. Definition3.2 gives gamma^p(z)=lambda^p(z+(p-1)1). The actual map is coefficient extraction[t^p] from(1+t)^{p-1}lambda_t(z), giving sum_{i=0}^{p-1}binom(p-1,i)lambda^{p-i}(z). For z=(0,x), every p-i>=1, so lambda^{p-i}(z) is the embedded lambda^{p-i}(N,x). At p=1,x=0 the source sum gives the adjoined unit, but gamma^1(0,0)=0. The coordinator independently verified the coefficient expansion. Full exact proof and the initial injective map: identification_342.json.',
 'first displayed gamma formula',kind='misprint_in_print',witness=353)
r.patch(p,'current',r'\sum_{i=0}^{p-1}\binom{p-1}{i}\lambda^i(N,x)',r'\sum_{i=0}^{p-1}\binom{p-1}{i}\lambda^{p-i}(N,x)','ASTRA-V-GAMMA-EXPONENT-342','Preserve the printed bounds and binomial coefficient while restoring the exact coefficient-extraction exponent.')
r.own_finding('ASTRA-V-LOW-DOTS-342',p,
 'All product dots and ellipses in the main calculation are low. There are twenty product marks diplomatically, including the extra final-denominator dot, and nineteen in current; three complete diplomatic ellipses and four current ones.',
 r'Use occurrence-counted \mathbin{.} products and \ldots, retaining the paired literal two-dot ending.',
 'Preserve the physically observed low positions and the separately decided doubled-dot/two-dot variants.',
 'Each region was compared in the main strips and native353 top/lower: introduction1;5.5.4 two;5.6 definition4; first series line4; next fraction2; expanded fraction2; final fraction5 diplomatic/4 current. The complete ellipses in the expanded fraction are also on the baseline. Convert ellipses first so their controls cannot be confused with the product control prefix.',
 'all product dots and expanded-fraction ellipses',kind='symbol',witness=353)
r.patch(p,'diplomatic',r'\cdots',r'\ldots','ASTRA-V-LOW-DOTS-342','Preserve the three complete diplomatic low ellipses.',count=3)
r.patch(p,'current',r'\cdots',r'\ldots','ASTRA-V-LOW-DOTS-342','Preserve the four complete current low ellipses.',count=4)
r.patch(p,'diplomatic',r'\cdot',r'\mathbin{.}','ASTRA-V-LOW-DOTS-342','Preserve twenty diplomatic low product marks.',count=20)
r.patch(p,'current',r'\cdot',r'\mathbin{.}','ASTRA-V-LOW-DOTS-342','Preserve nineteen current low product marks.',count=19)
r.own_finding('ASTRA-V-PARAGRAPH-LABEL-342',p,
 'The label5.6 is ordinary unruled type.',
 r'5.6. in place of \textbf{5.6.}.',
 'Restore the inspected numbered-paragraph form.',
 'Both main second strip and native353 top show the label without a rule or bold weight.',
 '5.6 label',kind='convention',witness=353)
r.patch(p,'both',r'\textbf{5.6.}',r'5.6.','ASTRA-V-PARAGRAPH-LABEL-342','Preserve the ordinary paragraph number.')
r.own_finding('ASTRA-V-UNIVERSAL-INJECTION-342',p,
 'The initial paragraph asserts injectivity of A_N→A in the universal polynomial-ring case specified on341.',
 'Retain the assertion with the actual evaluation and cancellation proof.',
 'Verify the source map in its stated universal domain.',
 'Here Phi(n,x)=n+xD, D=lambda_(minus1)(N), in A=Z[N,...,lambda^dN;lambda^iX,lambda^iY,i>=1]. The lambda-evaluation q sends N to1 and every higher lambda^jN to0, while retaining the X/Y coordinates. It sends D to0 and restricts to the identity on Z. Thus Phi(n,x)=0 forces n=0 after q. Since A is an integral polynomial ring and D is nonzero (evaluation N↦0 sends it to1), xD=0 then gives x=0. Its lambda compatibility is exactly5.3.1 on(0,x) and the binomial operation on the adjoined integers. The proof is recorded in identification_342.json and does not assert injectivity for an arbitrary specialized A.',
 'opening paragraph, map continued from341',kind='exact_identification',verdict='retained with exact morphism proof',witness=353)
packet={
 'source_id':'ASTRA-V-GAMMA-EXPONENT-342','page':342,'record_type':'exact_identification',
 'image':['scan/SGA6_scan_360dpi.pdf#page=356','scan/SGA6_witness_300dpi.djvu#page=353'],
 'printed':'gamma^p(0,x)=sum_(i=0)^(p-1)binom(p-1,i)lambda^i(N,x).',
 'current_repair':'Only lambda^i(N,x) becomes lambda^(p-i)(N,x); preserve p-1 upper bound, i=0 lower bound, coefficient and comma.',
 'coefficient_map':{
  'ring':'A_N with unit1_N=(1,0),z=(0,x).',
  'definition':'gamma^p(z)=lambda^p(z+(p-1)1_N) by3.2.',
  'series':'lambda_t(z+(p-1)1_N)=lambda_t(z)(1+t)^(p-1).',
  'map':'[t^p]:A_N[[t]]→A_N extracts the degree-p coefficient. Applying it to that exact product gives sum_(i=0)^(p-1)binom(p-1,i)lambda^(p-i)(z).',
  'coordinate_identification':'Each p-i>=1, so lambda^(p-i)(z)=(0,lambda^(p-i)(N,x)) by5.5.3. This proves the repaired summand in the embedded A coordinate.',
  'counterexample':'At p=1,x=0, the printed sum consists of lambda^0=(1,0), whereas gamma^1(0,0)=(0,0). These differ already in the first integer coordinate under the augmentation A_N→Z.',
  'independent_review':'Coordinator confirmed the coefficient expansion and the p=1,z=0 obstruction.'
 },
 'universal_injection':{
  'ring':'A=Z[N,lambda^2N,...,lambda^dN;lambda^iX,lambda^iY,i>=1].',
  'D':'D=lambda_(minus1)(N)=1-N+lambda^2N-...+(-1)^d lambda^dN.',
  'map':'Phi:A_N→A,(n,x)↦n+xD.',
  'multiplication':'Phi((n,x)(m,y))=nm+(ny+mx+xyD)D=(n+xD)(m+yD).',
  'lambda_compatibility':'Phi sends(1,0) to1 and the positive coefficient(0,lambda^p(N,x)) to lambda^p(N,x)D=lambda^p(xD), exactly5.3.1. Additivity then handles every(n,x).',
  'evaluation':'q:A→Z[lambda^iX,lambda^iY,i>=1] sends N↦1,lambda^jN↦0 for j>=2, and fixes the other independent coordinates. It is the lambda-evaluation at the line element1 and satisfies q(D)=0.',
  'injectivity':'From Phi(n,x)=0, q yields n=0. The independent evaluation N↦0,lambda^jN↦0 sends D to1, so D is nonzero. A is an integral polynomial ring, hence xD=0 implies x=0.',
  'scope':'This is the actual universal case named immediately before the assertion. No injectivity claim for arbitrary specializations is used.'
 }
}
(HERE/'identification_342.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'envoyant(1,0)sur1,et(0,x)surx.lambda_(minus1)(N)','last fraction denominator1+sum_(k>=1)lambda^k(N,x).lambda_(minus1)(N)..L^k t^k',
 'Full main356 strips and native353 top/lower compared. Checked universal injection, literal barless Lambda with main/native tight views, wrong printed gamma exponent and exact current repair, ordinary5.6, reinforced Z, every sum index and L-substitution, the open composition circle, detached fraction-level stop with native zoom, literal two-dot ending and doubled product dot, all low marks and absence of final punctuation. No author note or ruled body span.',
 witness='Native353 top/lower, witness_342_Lambda and fraction_stop crops/zooms; corresponding main tight crops.')
r.commit()
