#!/usr/bin/env python3
import json
from review_helpers import Review,HERE
r=Review();p=352
r.finding('351_355',11,'Folio352 begins(Ch A)_n est un lambda-ideal;351 ends et.',
 'The actual352 main first strip and native363 top start with that complete sentence. The attached marker already has this exact boundary; the next paragraph starts Soit alors.',
 '351/352 boundary',witness=363)
r.finding('351_355',12,'The Corollary6.6.4 display has no full stop after the final parenthesis.',
 'Main second strip and native363 top show the blank after the closing parenthesis. Retain the attached omission of the stop.',
 'first corollary display ending',witness=363)
for n,printed,region in ((13,'Par definition starts an indented proof paragraph.','Corollary6.6.4 proof'),(15,'D apres le corollaire precedent starts an indented proof paragraph.','Corollary6.6.5 proof')):
 r.finding('351_355',n,printed,'The paragraph indent is visible in both scans. The supplied paragraph break is already correct; this is a layout confirmation.',region,witness=363)
lambda_reason=('Both scans have lambda without an exponent after(-1)^i. Put z=x-epsilon(x). The stated definition is gamma^n(z)=lambda^n(z+n-1). Since lambda_t(z+n)=(1+t)lambda_t(z+n-1), comparison of coefficients and the finite alternating sum gives sum_(i=0)^n(-1)^i lambda^i(z+n)=(-1)^n lambda^n(z+n-1): adjacent lower coefficients cancel pairwise. Thus the missing superscript is exactly i. The bounds0,n and the sign(-1)^n stay unchanged.')
r.finding('351_355',14,'The finite alternating sum prints(-1)^i lambda(x+n-epsilon(x)), with no exponent on lambda.',
 lambda_reason,'Corollary6.6.4 proof, finite sum',verdict='not applied and now applied',
 change='Current restores lambda^i; diplomatic retains the missing exponent.',witness=363)
r.patch(p,'current',r'(-1)^i\lambda(x+n-\epsilon(x))',r'(-1)^i\lambda^i(x+n-\epsilon(x))',
 'check/findings/findings_351_355.json#14','Restore the coefficient operation identified by the exact finite telescoping identity.')
fil_reason=('Both scans clearly lower n under Fil. The explicit reference to3.10 identifies its ideal by the generators product gamma^(i_j)(z_j), epsilon(z_j)=0 and sum i_j>=n. The identity on each such generator gives the exact identification of the label Fil_n here with Fil^n in3.10; the proof then sends those generators into(Ch A)_n using6.6.4 and the ring-filtration product. There is no changed ideal, index value or map to repair. Retain this observed index placement in both forms rather than impose a uniform typography on the source label.')
r.finding('351_355',16,'The source uses Fil_n with a lowered n, and the right side also has lowered n.',
 fil_reason,'Corollary6.6.5 filtration notation',verdict='proposal rejected; source notation retained',
 change='Retain Fil_n in both forms, with the exact identity on the3.10 generators recorded.',witness=363)
r.finding('351_355',17,'The final gamma^n(x prime) formula continues inline with comma car on the same source line.',
 'Both scans show ordinary line spacing and the comma before car. The attached inline representation already preserves these formula tokens and punctuation. No further content change follows from the former display layout.',
 'last proof formula',verdict='formatting decision; existing tokens retained',change='Retain the attached inline formula and its comma.',witness=363)
r.finding('351_355',18,'The final words are Par suite, with a comma.',
 'Both source lower views show the comma after suite at the page end. The attached ending already agrees.',
 'final page words',witness=363)
r.finding('351_355',10,'The actual351 two statements and352 three statements have the recorded lexical underlines; mathematical symbols and locators remain plain.',
 'This update extends the personally inspected aggregate through352. On351 the two statements each have the three groups already recorded. On352,6.6.4 has Soit;l homomorphisme d augmentation de;alors;pour tout;on a.6.6.5 has Avec les notations de.6.6.7 has Soit;une;algebre graduee de caracteristique nulle;a degres bornes;alors les deux filtrations definies sur;sont;identiques. The K-hyphen and all formula letters stay plain. Actual353–355 groups remain for their own page comparisons.',
 'statement bodies, inspected351–352 portion',verdict='confirmed for inspected351–352 scope',change='Restore the thirteen352 word-rule groups in addition to the six351 groups;353–355 pending.',witness=363)
r.decisions[-1]['image']='scan/SGA6_scan_360dpi.pdf#page=365; scan/SGA6_scan_360dpi.pdf#page=366; scan/SGA6_witness_300dpi.djvu#page=362; scan/SGA6_witness_300dpi.djvu#page=363'
r.own_finding('ASTRA-V-UNDERLINE-352',p,
 'The three corollaries underline respectively five,one,and seven lexical groups; the numbers,letters,formulas and K-hyphen are unruled.',
 'Thirteen explicit lexical uline groups.',
 'Restore only these inspected352 word rules.',
 'The native top/lower crops resolve every endpoint. The proof paragraphs and the mathematical factors in the statement lines have no rules.',
 'Corollaries6.6.4,6.6.5,6.6.7',witness=363)
for old,new in (
 (r"Soit \(\epsilon\) l'homomorphisme d'augmentation de \(\Ch A\)~; alors, pour tout \(x\in\Ch A\), on a :",r"\uline{Soit} \(\epsilon\) \uline{l'homomorphisme d'augmentation de} \(\Ch A\)~; \uline{alors}, \uline{pour tout} \(x\in\Ch A\), \uline{on a} :"),
 (r'Avec les notations de 3.10,',r'\uline{Avec les notations de} 3.10,'),
 (r'Soit \(A\) une \(K\)-algèbre graduée de caractéristique nulle, à degrés bornés~; alors les deux filtrations définies sur \(\Ch A\) sont identiques.',r'\uline{Soit} \(A\) \uline{une} \(K\)-\uline{algèbre graduée de caractéristique nulle}, \uline{à degrés bornés}~; \uline{alors les deux filtrations définies sur} \(\Ch A\) \uline{sont} \uline{identiques}.')):
 r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-352','Preserve the exact observed lexical rule endpoints and plain mathematics.')
r.own_finding('ASTRA-V-ELLIPSES-352',p,'All ten complete ellipses in the coefficient tuples are low.',
 r'Use \ldots in place of ten \cdots controls.',
 'Preserve the source ellipsis height.',
 'Main four strips and native top/lower show all ten complete tails at the text baseline; no incomplete tail occurs on this page.',
 'coefficient tuples throughout352',kind='symbol',witness=363)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-352','Preserve all ten complete low ellipses.',count=10)
evaluation_reason=('The source uses lambda_(-1)(x) for arbitrary augmentation n in its proof of the finite Corollary6.6.2. Section5.1 had defined lambda_(-1)(N) for lambda^i(N)=0 above a finite bound. In the exact example K=Q,A=Q[Y]/(Y^2),degree Y=2,u=(2,1+Y),x=u-1=(1,1+Y), the elementary-symmetric evaluation e1→0,e2→Y and6.6.1 give lambda_t(u)=1+u t+t^2. The character is ch(a,1+bY)=a-bY, hence ch(lambda_t(x))=1+t-Yt/(1+t). Its alternating partial sum through N>=1 is NY, whose degree-two coefficient does not stabilize. Thus full-series evaluation at-1 is not defined by the degree-completion topology for this x. The finite map S_n=sum_(i=0)^n(-1)^i lambda^i is well-defined and commutes with the quotient by the lambda-ideal(Ch A)_(n+1); comparison with the truncated pair gives exactly the finite statement6.6.2. Retain the printed proof notation, with this evaluation limitation explicit and no change to that finite corollary.')
r.own_finding('ASTRA-V-LAMBDA-EVALUATION-352',p,
 'The opening proof applies lambda_(-1) to an arbitrary augmentation-n pair and prints an equality for it.',
 'Retain the printed lambda_(-1) expressions in both forms.',
 'Record the full-series evaluation limitation separately; the finite alternating-sum assertion is retained.',
 evaluation_reason,'opening proof, lambda_(-1) notation',kind='author_claim_issue',
 verdict='source decided and retained; exact evaluation issue recorded',witness=363)
packet={
 'record_type':'author_claim_issue_and_exact_identification','page':352,
 'source_ids':['ASTRA-V-LAMBDA-EVALUATION-352','check/findings/findings_351_355.json#14','check/findings/findings_351_355.json#16'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=366','scan/SGA6_witness_300dpi.djvu#page=363'],
 'source_passages':{
  '339_5_1':'Soient K un anneau binomial,A une K-lambda-algebre,N,x deux elements de A tels que lambda^k(N)=0 pour k>d. On pose lambda_(-1)(N)=sum_(i=0)^d(-1)^i lambda^i(N).',
  '350_6_6_1':'For x=(n,1+...+a_n),lambda^i(x)=0 for i>n,lambda^n(x)=(1,1+a1),and the finite sum_(i=0)^n(-1)^i lambda^i(x) has pair(0,1-(n-1)!a_n+higher degrees). The diplomatic source has the separately decided >= and missing-pair-parenthesis errors.',
  '351_6_6_2':'The relation6.6.1.iii is true for every element X of augmentation n. It is expressly the finite sum relation.',
  '352_proof':'For arbitrary x=(n,1+a1+...+an+...) the proof calls lambda_(-1)(x), compares it modulo(Ch A)_(n+1) with lambda_(-1)(n,1+...+an),and prints lambda_(-1)(x)=(0,1-(n-1)!an+...).'
 },
 'evaluation_example':{
  'ring':'K=Q,A=Q[Y]/(Y^2),degree Y=2;A has degrees0 and2 only.',
  'character':'ch(a,1+bY)=a+eta(Log(1+bY))=a-bY, since Y^2=0 and eta in degree2 is multiplication by-1. Inverse a+cY→(a,1-cY).',
  'universal_map':'Q[e1,e2]→A sends e1→0,e2→Y. Apply Ch to this graded map and the rank-two universal splitting computation6.6.1;u=(2,1+Y) has lambda_t(u)=1+u t+1 t^2.',
  'rank_one_element':'x=u-1=(1,1+Y),because the unit is(1,1) and addition of pairs multiplies their series coordinates.',
  'exact_series':'lambda_t(x)=lambda_t(u)/(1+t); applying ch gives(1+(2-Y)t+t^2)/(1+t)=1+t-Yt/(1+t).',
  'coefficients':'ch(lambda^0 x)=1;ch(lambda^1 x)=1-Y;ch(lambda^i x)=(-1)^iY for i>=2.',
  'partial_sum_map':'The additive coefficient map [Y]:A→Q sends ch(sum_(i=0)^N(-1)^i lambda^i x)=NY to N for every N>=1.',
  'topology':'The degree filtration is zero above degree2;therefore these nonstationary partial sums do not converge in the degree completion. Full-series evaluation at t=-1 is not supplied for x by that topology.'
 },
 'finite_statement_map':{
  'operation':'S_n:Ch(A)→Ch(A),x→sum_(i=0)^n(-1)^i lambda^i(x).',
  'quotient':'q_n:Ch(A)→Ch(A)/(Ch A)_(n+1) is a lambda-ring quotient by Lemma6.6.3. Therefore q_n(S_n(x))=S_n(q_n(x)) term by term.',
  'comparison':'q_n(x)=q_n(n,1+a1+...+an);the latter pair has lambda-degree at most n by6.6.1. Thus S_n has exactly the asserted leading coefficient. This proves the printed finite corollary without evaluating the infinite series of the original x.'
 },
 'missing_superscript':lambda_reason,
 'filtration_index_identity':fil_reason,
 'disposition':'Preserve all printed lambda_(-1) occurrences and the finite6.6.2 statement. Only the independently identified missing lambda superscript receives a current textual correction. No replacement theorem or new hypothesis is inserted.'
}
(HERE/'identification_352.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'(Ch A)_n est un lambda-ideal.','Par suite,',
 'Full main366 four strips and native363 top/lower compared word by word. Checked arbitrary-pair coordinates, every lambda_-1 subscript, exact factorial and signs, all ten low ellipses, five/one/seven word-rule groups, no stop after6.6.4 display, the missing lambda exponent and its finite coefficient proof, explicit Fil_n retention by identity on3.10 generators, the printed numbering jump6.6.5 to6.6.7, the bounded-degree hypothesis, both primed pairs, fraction bar and final a_p prime, every punctuation and the final comma. The lambda_-1 evaluation limitation is a separate retained-source proof issue. No author note.',
 witness='Native363 top/lower complete body compared; missing lambda exponent and lowered Fil index resolved in top crop.')
r.commit()
