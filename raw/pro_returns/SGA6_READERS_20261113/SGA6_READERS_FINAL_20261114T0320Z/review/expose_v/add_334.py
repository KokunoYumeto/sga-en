#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=334
r.finding('331_335',7,'The first word of334 is d une;333 ends qui se trouve ainsi muni.',
 'Both main348 and native345 show the first complete line d une structure de lambda-anneau. The previous page was fully compared through muni. The attached marker now precedes d une and is correct.',
 '333/334 boundary',witness=345)
r.finding('331_335',8,'In the first relation-family introduction, the inner P index is i without a prime, whereas the outer family index is i-prime in I-prime.',
 'The native top crop resolves the closing parenthesis immediately after i. Definition4.6 and Proposition4.7 on the same page both give the relation family(P_i-prime) indexed by i-prime in I-prime; the sentence also names its generated ideal using P_i-prime. The exact family is the map I-prime→A, i-prime↦P_i-prime. The attached diplomatic inner i/current inner i-prime pair restores that same bound variable and leaves every outer index unchanged.',
 'relation-family introduction before4.6',witness=345)
r.finding('331_335',9,'The arrow A/J→B in Proposition4.7 is unnamed in print; the condition at the end of that statement uses f-prime.',
 'Both native345 lower and main fourth strip show an empty interval between seul and A/J. Let q:A→A/J be the quotient and f:A→B the evaluation map of4.2, X_i↦b_i and lambda^n X_i↦lambda^n(b_i). The displayed relation hypothesis gives f(P_i-prime)=0; its kernel is the lambda-ideal described immediately above, so J lies in ker(f). The uniquely induced map is f-prime:A/J→B, a+J↦f(a), with f-prime q=f. Its values on the classes of X_i are precisely the printed b_i. Supply the missing name f-prime only in the current layer.',
 'Proposition4.7, unnamed quotient arrow',verdict='confirmed and now applied in current',change='Current A/J→B becomes f-prime:A/J→B; diplomatic unnamed arrow retained.',witness=345)
r.patch(p,'current',r'et un seul \(A/J\to B\)',r"et un seul \(f':A/J\to B\)",'check/findings/findings_331_335.json#9','Name the exact quotient map used by the statement condition.')
r.finding('331_335',10,'Proposition4.7 ends at b_i with no full stop.',
 'The native lower crop shows the dot of the subscript i above its stem, but no separate terminal dot to the right. The attached diplomatic absence/current supplied sentence stop is the exact recorded punctuation pair.',
 'Proposition4.7 end',witness=345)
r.own_finding('ASTRA-V-REFERENCE-334',p,
 'The gamma-stability paragraph literally ends comme il resulte des solutions3.2.',
 'Diplomatic solutions3.2; current relations3.2.',
 'Correct the reference noun solutions to relations in the current layer only.',
 'The native345 top crop and main third strip clearly resolve solutions. The cited Proposition3.2(ii) on325 states the relations gamma_t(x)=lambda_{t/(1-t)}(x) and lambda_t(x)=gamma_{t/(1+t)}(x). For n>=1 their coefficients are gamma^n(x)=sum_(j=1)^n binom(n-1,j-1)lambda^j(x) and lambda^n(x)=sum_(j=1)^n(-1)^(n-j)binom(n-1,j-1)gamma^j(x). The substitutions compose to t in both orders, so these integral triangular transformations are inverse. For every x of the given ideal J, membership of all positive-degree operations from either family gives membership of all operations from the other family. This is exactly the reference used in the sentence; identification_334.json records the maps and calculation.',
 'paragraph following Definition4.6, reference to3.2',kind='misprint_in_print',witness=345)
r.patch(p,'current','des solutions 3.2.','des relations 3.2.','ASTRA-V-REFERENCE-334','Use the noun identifying the two explicit substitution relations of3.2(ii).')
r.own_finding('ASTRA-V-STATEMENT-RULES-334',p,
 'Definition4.6 underlines Le, anneau and sera appele. Proposition4.7 underlines eight lexical spans, leaving the entire on ait phrase plain.',
 'Apply only the eleven inspected word-group rules; preserve formula and prime variants independently.',
 'Restore the exact lexical rules in both statements.',
 'Both native crops resolve the three definition spans and its entirely plain defined term. The proposition rules are Pour toute; algebre; et toute famille; d elements de; satisfaisant les relations; il existe un; homomorphisme et un seul; tel que pour tout. All family formulas, K/lambda symbols, the quotient arrow, i, on ait and final equation are outside the rules.',
 'Definition4.6 and Proposition4.7',witness=345)
text=(HERE/'page_334_diplomatic.tex').read_text()
old=next(line for line in text.splitlines() if line.startswith(r'\textbf{Définition 4.6.}'))
new=r'''\textbf{Définition 4.6.} \uline{Le} \(\lambda\)-\uline{anneau} \(A/J\) \uline{sera appelé} \(\lambda\)-anneau engendré sur \(K\) par la famille de générateurs \((X_i)_{i\in I}\) soumis aux relations \((P_{i'})_{i'\in I'}\).'''
r.patch(p,'both',old,new,'ASTRA-V-STATEMENT-RULES-334','Restore the three definition word rules.')
for layer in ['diplomatic','current']:
 text=(HERE/f'page_334_{layer}.tex').read_text()
 old=next(line for line in text.splitlines() if line.startswith(r'\textbf{Proposition 4.7.}'))
 if layer=='current':old=old.replace(r'et un seul \(A/J\to B\)',r"et un seul \(f':A/J\to B\)")
 new=old
 for a,b in [
  ('Pour toute ',r'\uline{Pour toute} '),
  (r'-algèbre \(B\)',r'-\uline{algèbre} \(B\)'),
  ('et toute famille ',r'\uline{et toute famille} '),
  ("d'éléments de ",r"\uline{d'éléments de} "),
  ('satisfaisant les relations ',r'\uline{satisfaisant les relations} '),
  ('il existe un ',r'\uline{il existe un} '),
  ('homomorphisme et un seul ',r'\uline{homomorphisme et un seul} '),
  ('tel que pour tout ',r'\uline{tel que pour tout} '),
 ]:
  assert new.count(a)==1,(layer,a)
  new=new.replace(a,b)
 assert new.count(r'\uline{')==8
 r.patch(p,layer,old,new,'ASTRA-V-STATEMENT-RULES-334','Restore eight proposition rules while retaining that layer’s exact map-name and terminal-stop form.')
packet={
 'source_id':'ASTRA-V-REFERENCE-334','page':334,'record_type':'exact_identification',
 'image':['scan/SGA6_scan_360dpi.pdf#page=348','scan/SGA6_witness_300dpi.djvu#page=345'],
 'region':'reference at the end of the gamma-stability paragraph',
 'printed':'comme il resulte des solutions3.2','corrected':'comme il resulte des relations3.2',
 'source_reference':'Exposé V, Proposition3.2(ii), printed325, already fully compared.',
 'maps':{
  'rho_minus':'A[[t]]→A[[t]], h(t)↦h(t/(1-t))',
  'rho_plus':'A[[t]]→A[[t]], h(t)↦h(t/(1+t))'
 },
 'calculation':[
  '(t/(1-t))/(1+t/(1-t))=t and(t/(1+t))/(1-t/(1+t))=t.',
  'For1<=j<=n, [t^n](t/(1-t))^j=binom(n-1,j-1).',
  'For1<=j<=n, [t^n](t/(1+t))^j=(-1)^(n-j)binom(n-1,j-1).',
  'The constant term lambda^0(x)=gamma^0(x)=1 contributes nothing in positive degree.',
  'Thus gamma^n(x)=sum_(j=1)^n binom(n-1,j-1)lambda^j(x), and lambda^n(x)=sum_(j=1)^n(-1)^(n-j)binom(n-1,j-1)gamma^j(x).',
  'Both matrices have integral entries and compose to the identity. Applying either expression to x in J shows the two positive-operation stability conditions define the same subset of ideals, with the identity map J↦J as the identification.'
 ],
 'change':'Change only solutions to relations in the current source; keep the exact printed noun diplomatically.',
 'forms':'French diplomatic/current and corresponding English transfer'
}
(HERE/'identification_334.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'d une structure de lambda-anneau','f passe donc au quotient et definit',
 'All words and symbols compared across four main strips and native345 top/lower. Checked first-word boundary; intersection/generated-ideal statements with n>=1; all inner and outer family primes and both relation names; all eleven lexical rules; literal solutions reference and its exact coefficient identification; every evaluation variable; the unnamed quotient arrow and f-prime condition; missing terminal dot; complete final proof fragment. No author note.',
 witness='Native345 top/lower: witness_334_top.png and witness_334_lower.png.')
r.commit()
