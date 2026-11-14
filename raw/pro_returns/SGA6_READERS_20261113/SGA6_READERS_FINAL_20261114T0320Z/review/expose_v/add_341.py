#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=341
r.finding('341_345',1,'Comme starts a new indented paragraph at the page top, after340 final display.',
 'Both complete boundary images resolve the new paragraph. The supplied blank line after the341 marker preserves it.',
 '340/341 paragraph boundary',verdict='formatting observed; no content error',witness=352)
r.finding('341_345',2,'The sentence before5.4.2 ends with a semicolon after d-prime.',
 'Main355 first strip and native352 top resolve a raised dot above a comma-shaped lower mark. The supplied semicolon agrees.',
 'before5.4.2',witness=352)
r.finding('341_345',3,'Ses operations sont donc definie par has no final s on definie.',
 'Both scans resolve the singular spelling after the plural subject operations. The paired source keeps it diplomatically and adds the agreement s only in current.',
 'before5.5.2',change='Retain diplomatic définie and current définies.',witness=352)
for sid in ['fixes/FIXLOG_6_CURRENT.jsonl#408','fixes/RECONCILE_CODEX_6.json#309']:
 r.source(sid,'The source prints definie without s.',
  'Direct main/native comparison confirms the printed ending. The current agreement repair is exactly the plural subject operations with definies; diplomatic remains literal.',
  'sentence before5.5.2',change='Retain the existing paired ending.',witness=352,page=p)
r.finding('341_345',4,'The addition row of5.5.2 ends after(n+n-prime,x+x-prime), without punctuation.',
 'Both scans show blank space after the parenthesis; the supplied omission of the former comma agrees.',
 '5.5.2 addition row',witness=352)
r.finding('341_345',5,'The multiplication row of5.5.2 also ends at its closing parenthesis, without a full stop.',
 'Main third strip and native352 lower show no stop. Diplomatic already agrees. Current retains an inherited stop after its separately corrected x-prime; remove that stop alone while retaining the mathematically verified x-prime.',
 '5.5.2 multiplication row end',verdict='confirmed and current replay now applied',change='Current x-dot_N x-prime). becomes x-dot_N x-prime); diplomatic absence unchanged.',witness=352)
r.patch(p,'current',r"x\cdot_N x').",r"x\cdot_N x')",'check/findings/findings_341_345.json#5','Remove only the unprinted stop after the corrected multiplication row.')
r.source('fixes/REPLAY_MANUAL_6.json#9','There is no full stop after the multiplication-row closing parenthesis.',
 'The old y anchor was absent from current because the independent operand repair had already supplied x-prime. The exact replay therefore removes the stop from the current x-prime anchor, with both observed decisions preserved.',
 '5.5.2 current punctuation replay',verdict='not applied and now applied',change='Apply the same no-stop reading to the already corrected x-prime row.',witness=352,page=p)
r.finding('341_345',6,'The printed last term is x-dot_N y, although the two inputs are(n,x) and(n-prime,x-prime).',
 'Both scans clearly resolve y. Write D=lambda_(minus1)(N) and x star y=xyD. In the unitization, (n,x)(n-prime,x-prime)=(nn-prime,nx-prime+n-prime x+x star x-prime), obtained by multiplying n times the adjoined unit plus x with its second counterpart. Thus the exact second operand is x-prime. With A=Z,N=0,n=n-prime=0,x=1,x-prime=0,y=1, the printed expression gives(0,1) for multiplication by zero, while the unitization gives(0,0). Keep y in diplomatic and x-prime in current. Full maps: identification_341.json.',
 '5.5.2 last operand',change='Retain diplomatic y and current x-prime.',witness=352)
for sid in ['fixes/FIXLOG_6_CURRENT.jsonl#409','fixes/RECONCILE_CODEX_6.json#298']:
 r.source(sid,'The printed final operand is y.',
  'The exact unitization product pairs the first A-coordinate x with the second A-coordinate x-prime; the displayed n=n-prime=0 test in identification_341.json distinguishes the two formulas. The supplied current-only x-prime repair is retained.',
  '5.5.2 last operand',change='Retain the existing paired y/x-prime reading.',witness=352,page=p)
r.finding('341_345',7,'The injection notation x to(0,x) uses a wavy shaft and a right arrowhead.',
 'Main third strip and native352 lower resolve the wavy shaft; it has no mapsto bar. The supplied rightsquigarrow preserves that observed glyph for the explicitly defined inclusion.',
 'after5.5.2',witness=352)
r.finding('341_345',8,'L anneau begins a new indented paragraph after5.5.1.',
 'Both scans show the new paragraph. The supplied separation agrees without a change of mathematical tokens.',
 'after5.5.1',verdict='formatting observed; no content error',witness=352)
r.own_finding('ASTRA-V-LOW-DOTS-341',p,
 'Nine low product dots: two in5.4.2, three in5.5.1, two in5.5.2 and two in5.5.3.',
 r'Use \mathbin{.} at all nine inspected product marks; retain the two N subscripts on their own product symbols.',
 'Preserve the observed baseline marks without changing operands or indices.',
 'Every listed dot is resolved in native352 top/lower and the corresponding main strips. Their low location is distinct from the height of the equality bars.',
 'all four numbered formulas',kind='symbol',witness=352)
r.patch(p,'both',r'\cdot',r'\mathbin{.}','ASTRA-V-LOW-DOTS-341','Preserve the nine low product marks.',count=9)
r.own_finding('ASTRA-V-PARAGRAPH-LABEL-341',p,
 'The numbered paragraph5.5 is ordinary unruled type.',
 r'5.5. instead of \textbf{5.5.}.',
 'Restore the directly observed paragraph label.',
 'The native top and main first strip show its ordinary weight and absence of a word rule.',
 '5.5 label',kind='convention',witness=352)
r.patch(p,'both',r'\textbf{5.5.}',r'5.5.','ASTRA-V-PARAGRAPH-LABEL-341','Preserve the ordinary paragraph-number form.')
r.own_finding('ASTRA-V-ZERO-TERM-341',p,
 'The5.5.3 series is summed from p=0, although5.3 defined lambda^p(N,x) in A only for p>=1.',
 'Retain the printed p=0 bound and document its value as the adjoined identity of A_N.',
 'Make the exact constant-term convention explicit in the apparatus, without extending the earlier division identity to p=0.',
 'The inclusion is i:A→A_N,x↦(0,x), while the new unit is1_N=(1,0). The series is H_x=1_N+sum_{p>=1}i(lambda^p(N,x))t^p, and5.5.3 is(1+t)^n H_x. Formula5.4.1 proves H_(x+y)=H_x H_y with the stated twisted product. Lambda^0 must be1_N. Extending5.3.1 to p=0 would instead demand an inverse of D=lambda_(minus1)(N) in A, which does not exist in the universal polynomial ring; this extension is not made. The explicit construction is recorded in identification_341.json.',
 '5.5.3 constant coefficient',kind='exact_identification',verdict='printed bound retained with exact unit convention',witness=352)
r.own_finding('ASTRA-V-UNIT-CLAIM-341',p,
 'The paragraph after5.5.1 states that A with the new multiplication is no longer unital.',
 'Retain the phrase and attach its exact exceptional example; retain the unitization construction.',
 'Record that the literal assertion of absence of a unit does not hold for every allowed N.',
 'Take A=Z with its binomial lambda-structure,N=0,d=1. Then every lambda^k(N)=0 for k>d and D=lambda_(minus1)(0)=1, so x star y=xy and1 remains a unit. The source unitization still exists: Phi:Z⊕Z→Z×Z,(n,x)↦(n,n+x) is a ring isomorphism with inverse(u,v)↦(u,v-u). It sends the adjoined unit(1,0) to(1,1), and the inclusion x↦(0,x) to the second factor. This exact map verifies the construction while demonstrating the scope problem in the prose. No replacement theorem or body rewrite is proposed.',
 'paragraph after5.5.1',kind='author_claim_issue',verdict='source retained; explicit unit example recorded',witness=352)
packet={
 'source_id':'ASTRA-V-ZERO-TERM-341','page':341,'record_type':'exact_identification',
 'image':['scan/SGA6_scan_360dpi.pdf#page=355','scan/SGA6_witness_300dpi.djvu#page=352'],
 'twisted_product':'D=lambda_(minus1)(N); x star y=xyD on the additive group A.',
 'unitization':{
  'group':'Z⊕A','unit':'(1,0)','inclusion':'i(x)=(0,x)',
  'product':'(n,x)(n-prime,x-prime)=(nn-prime,nx-prime+n-prime x+xx-prime D).',
  'derivation':'Expand(n1+i(x))(n-prime1+i(x-prime)); use1 as identity and i(x)i(x-prime)=i(xx-prime D). This proves the exact second A-coordinate x-prime in5.5.2.',
  'printed_y_test':'At A=Z,N=0,n=n-prime=0,x=1,x-prime=0,y=1, the source final y gives(0,1), whereas multiplication by(0,0) gives(0,0).'
 },
 'constant_term':{
  'series':'H_x(t)=(1,0)+sum_{p>=1}(0,lambda^p(N,x))t^p; lambda_t(n,x)=(1+t)^n H_x(t) in A_N[[t]].',
  'identity':'The p=0 term is the adjoined unit(1,0), not an element i(a) of the augmentation ideal.',
  'additivity':'For p>=1 the coefficient of H_x H_y is i(lambda^p(N,x)+lambda^p(N,y)+sum_{i+j=p,i,j>0}lambda^i(N,x)lambda^j(N,y)D). Formula5.4.1 identifies this with i(lambda^p(N,x+y)), and the constant coefficient remains(1,0). Thus H_x H_y=H_(x+y).',
  'first_coefficient':'The positive definition gives lambda^1(N,x)=x by cancellation of D in the universal polynomial ring and substitution, hence the first coefficient of lambda_t(n,x) is(n,x).',
  'scope':'5.3.1 is retained only for p>=1 as printed. No inverse of D or value in A for its p=0 division expression is introduced.'
 },
 'unit_prose_issue':{
  'example':'A=Z,N=0,d=1 yields D=1 and the ordinary unital product.',
  'isomorphism':'Phi:Z⊕Z→Z×Z,(n,x)↦(n,n+x); inverse(u,v)↦(u,v-u).',
  'product_check':'The second coordinate of Phi((n,x)(m,y)) is nm+ny+mx+xy=(n+x)(m+y); the first is nm.',
  'scope':'The source phrase asserting absence of a unit fails for this allowed instance; the displayed unitization is nonetheless verified by Phi. Source prose is retained with the exact example recorded.'
 }
}
(HERE/'identification_341.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'Comme l anneau considere est integre','On definit alors un homomorphisme A_N→A, en',
 'All main355 strips and native352 top/lower compared. Checked top semicolon,5.4.2 factors, ordinary5.5, every twisted product and N index, two reinforced Z forms, literal definie and y, absent punctuation in both5.5.2 rows, wavy inclusion arrow, p=0 and infinity in5.5.3, all nine low dots, uppercase N/X/Y and final headed arrow. Zero-term convention and unit-prose example are separately recorded. No author note or ruled body span.',
 witness='Native352 top/lower: witness_341_top.png and witness_341_lower.png.')
r.commit()
