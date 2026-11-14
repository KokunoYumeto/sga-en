#!/usr/bin/env python3
import json
from review_helpers import Review,read,HERE
r=Review();p=354
for n,printed,region in ((24,'Si a in K starts an indented new paragraph.','paragraph after opening sentence'),(27,'Par additivite starts an indented new paragraph.','paragraph following square')):
 r.finding('351_355',n,printed,'Main368 and native365 top show the paragraph indent. The attached break is already correct; no additional content change follows from layout.',region,witness=365)
r.finding('351_355',25,'Both horizontal gamma_t arrow labels are above their shafts.',
 'Both scans resolve the lower label above its rightward arrow. The four arrow directions and all other label positions are also compared. The attached above placement agrees; the separately recorded target omission is independent of label placement.',
 'commutativity square, lower arrow label',witness=365)
r.finding('351_355',26,'The lower-right diagram corner ends with a closing parenthesis and no full stop.',
 'Main second strip and native top show the blank after this object. The attached punctuation agrees.',
 'commutativity square ending',witness=365)
comma_reason=('Both scans end the source line with a in A and show no comma before the next-line epsilon(x_i)=0. These are successive constraints on the same generator product:the coefficient a ranges in A,the x_i have augmentation0,and the index sum is at least m. The current comma separates the first and second constraints without altering that exact tuple of data or its generator map(a,(x_i),(i_i))→a product gamma^(i_i)(x_i). Retain the diplomatic omission and existing corrected comma.')
r.finding('351_355',28,'No source comma follows a in A before epsilon(x_i)=0.',
 comma_reason,'generator-product constraints',witness=365)
r.finding('351_355',29,'The displayed expansion of tilde-c(z) has no final full stop.',
 'The native lower crop shows the blank after the closing parentheses. The attached display already agrees. The next and last gamma-compatibility formula does have a full stop,which is retained.',
 'sum of Chern-class products ending',witness=365)
aggregate=next(x for x in read('decisions.jsonl') if x['source_id']=='check/findings/findings_351_355.json#10').copy()
aggregate.update(verdict='confirmed for inspected351–354 scope',printed_reading='The inspected351–354 statements have the recorded lexical rules;actual355 remains outside this completed scope.',
 change='Restore the four354 statement word groups and the separate i/e rules;355 pending.',region='statement bodies, inspected351–354 portion')
aggregate['reason']+=' Actual354 is fully compared:6.9 underlines Soit;une;algebre augmentee;alors. In i.e. only i and e are underlined separately;both periods are plain. Mathematical formulas and the K-lambda prefix remain plain.'
aggregate['image']+='; scan/SGA6_scan_360dpi.pdf#page=368; scan/SGA6_witness_300dpi.djvu#page=365'
r.decisions.append(aggregate)
r.own_finding('ASTRA-V-UNDERLINE-354',p,
 'Proposition6.9 has four lexical rule groups;the letters i and e of i.e. each have their own small rule.',
 'Four word uline groups and separate uline{i}.uline{e}.',
 'Restore these inspected rules,keeping punctuation and formula units plain.',
 'Native365 top/lower resolve the four statement rule endpoints and the gap under each full stop of i.e.;the proofs are unruled.',
 'Proposition6.9 body and i.e.',witness=365)
r.patch(p,'both',r'Soit \(A\) une \(K\)-\(\lambda\)-algèbre augmentée, \(z\in\Fil^mA\)~; alors :',r'\uline{Soit} \(A\) \uline{une} \(K\)-\(\lambda\)-\uline{algèbre augmentée}, \(z\in\Fil^mA\)~; \uline{alors} :','ASTRA-V-UNDERLINE-354','Preserve the four lexical rule groups.')
r.patch(p,'both','\ni.e.\n','\n'+r'\uline{i}.\uline{e}.'+'\n','ASTRA-V-UNDERLINE-354','Preserve the two separate single-letter rules with unruled periods.')
r.own_finding('ASTRA-V-LOW-DOTS-354',p,
 'The two complete product ellipses,the index-sum ellipsis,and both explicit coefficient product dots are low.',
 r'Use three \ldots and two \mathbin{.} tokens.',
 'Preserve source dot height and the distinction between multiplication tokens and complete series ellipses.',
 'The native lower crop resolves all three complete ellipses and the two product periods between a and its gamma factor or tilde-c(a) and its next factor. Adjacent factors and index bounds are unchanged.',
 'two generator products and index-sum bound',kind='symbol',witness=365)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-LOW-DOTS-354','Preserve three complete low ellipses.',count=3)
r.patch(p,'both',r'\sum a.',r'\sum a\mathbin{.}','ASTRA-V-LOW-DOTS-354','Preserve the low scalar product token.')
r.patch(p,'both',r'\widetilde c(a).',r'\widetilde c(a)\mathbin{.}','ASTRA-V-LOW-DOTS-354','Preserve the low completed-class product token.')
target_reason=('Both source lower objects literally read Ch A and Ghat_g(Ch A). The left arrow is the map defined in6.7.2 and asserted in6.8:tilde-c:A→Ch(Gr A),x↦(epsilon(x),c(x)),where the degree-i coefficient c^i(x) is the class of gamma^i(x-epsilon(x)) in Fil^i A/Fil^(i+1)A. Thus its actual codomain is K×(1+product_(i>=1)Gr^i A). The functor Ghat_g applied to this map acts coefficientwise:1+sum b_i t^i↦1+sum tilde-c(b_i)t^i,with target Ghat_g(Ch(Gr A)). The bottom gamma_t has source Ch(Gr A). In these exact objects the equality of the two routes is the coefficient identity tilde-c(gamma^i x)=gamma^i(tilde-c x),which is precisely the compatibility the paragraph is proving. Definition6.2 takes a graded input;here its functor is precomposed with Gr. Restore Gr A in both lower objects in current only;all four arrow labels and directions remain unchanged.')
r.own_finding('ASTRA-V-DIAGRAM-TARGET-354',p,
 'The two lower square objects are printed Ch A and Ghat_g(Ch A),without Gr.',
 r'Current lower objects \Ch(\Gr A) and \widehat G_g(\Ch(\Gr A));diplomatic retains both omissions.',
 'Restore the graded argument of the two lower objects using the exact6.7.2 map and its coefficientwise functor image.',
 target_reason,'commutativity square,two lower objects',kind='misprint_in_print',witness=365)
r.patch(p,'current',r'\Ch A \arrow[r,"\gamma_t"]',r'\Ch(\Gr A) \arrow[r,"\gamma_t"]','ASTRA-V-DIAGRAM-TARGET-354','Restore the actual codomain of tilde-c as defined in6.7.2.')
r.patch(p,'current',r'\widehat G_g(\Ch A)',r'\widehat G_g(\Ch(\Gr A))','ASTRA-V-DIAGRAM-TARGET-354','Restore the target of the coefficientwise map Ghat_g(tilde-c).')
packet={
 'record_type':'exact_identification','page':354,'source_ids':['ASTRA-V-DIAGRAM-TARGET-354'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=368','scan/SGA6_witness_300dpi.djvu#page=365'],
 'printed_square':{'upper_left':'A','upper_right':'Ghat_g(A)','lower_left':'Ch A','lower_right':'Ghat_g(Ch A)','left_arrow':'tilde-c','right_arrow':'Ghat_g(tilde-c)','both_horizontal_arrows':'gamma_t'},
 'source_definition_6_2':'For a graded K-algebra B,Ch(B)=K×(1+completed B^+) with the operations constructed in6.1.',
 'source_definition_6_7_1':'c^i(x)=class_(Gr^i A)(gamma^i(x-epsilon(x)));c(x)=1+sum_(i>=1)c^i(x).',
 'source_definition_6_7_2':'tilde-c(x)=(epsilon(x),c(x)),with values in Ch(Gr A) as explicitly stated in6.8 on353.',
 'corrected_square':{'upper_left':'A','upper_right':'Ghat_g(A)','lower_left':'Ch(Gr A)','lower_right':'Ghat_g(Ch(Gr A))','left_arrow':'tilde-c','right_arrow':'Ghat_g(tilde-c)','both_horizontal_arrows':'gamma_t'},
 'right_arrow_map':'1+sum_(i>=1)b_i t^i →1+sum_(i>=1)tilde-c(b_i)t^i;the coefficients are elements of Ch(Gr A).',
 'coefficient_comparison':'The upper/right route at x has coefficient tilde-c(gamma^i(x));the left/bottom route has coefficient gamma^i(tilde-c(x)). Their equality is exactly the gamma compatibility under proof.',
 'functor_composition':'The graded-input functor Ch of6.2 is evaluated on the associated-graded functor Gr applied to the augmented filtered ring A. This explicitly describes the relationship between the two constructions;no grading or identification of the original A with Gr A is asserted.',
 'patch_scope':'Current restores only the two omitted Gr arguments in the lower square objects. Diplomatic retains Ch A. All arrow labels,directions,subscripts and punctuation remain as printed.'
}
(HERE/'identification_354.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'d ou le resultat d apres(6.1.2) en passant au quotient.','tilde-c(gamma^(i_j)(x_j))=gamma^(i_j)(tilde-c(x_j)).',
 'Full main368 four strips and native365 top/lower compared. Checked every opening tilde and scalar pair,all four diagram arrow directions and label positions,g subscripts,plain Ch A source arguments and the exact current Gr restorations,diagram punctuation,3.7.2 and6.1.4 references,four word rules and separate i/e rules,all m/i/j factorial exponents and graded-class subscripts,missing source constraint comma and existing current comma,both coefficient products and all three low ellipses,no stop on the middle sum but an actual final stop on the last formula. No author note.',
 witness='Native365 top/lower complete body;diagram bottom labels,morphism tildes,missing comma and all six rule groups resolved.')
r.commit()
