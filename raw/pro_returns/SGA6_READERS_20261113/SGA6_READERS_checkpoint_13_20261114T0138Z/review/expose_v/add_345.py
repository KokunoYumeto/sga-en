#!/usr/bin/env python3
"""Personally inspected folio345, including the native witness."""
from review_helpers import Review,HERE
import json
r=Review();p=345
unit_reason=('The native lower crop resolves a low period between the two ones, with no descending comma tail. '
 'For I(A)=1+completed(A)^+ with its displayed ring law, its additive zero is the series1, hence 1*phi=phi*1=1. '
 'Formula6.1.2 gives (1,1)(a,phi)=(a,1^a phi^1(1*phi))=(a,phi), and the right product is identical. '
 'Thus the corrected pair is exactly(1,1). The scalar homomorphism is j:K→K×I(A),a↦(a,1); '
 'the projection pi(a,phi)=a satisfies pi∘j=id_K, and ker(pi)={(0,phi)}.')
r.finding('341_345',21,'The second source factor has two low dots; the hat covers the first. The other source factor and target have one.',
 'Both main359 upper strip and native356 top show the two detached low marks. The operation is the natural component I(A)×I(A)→I(A) constructed at the end of344;6.1.1 evaluates its two inputs at1+X and1+Y in the same completed graded algebra. Thus the second factor has the same single object-placeholder as the first, justifying removal of only its duplicated dot in the corrected form.',
 'first display, second factor',witness=356)
r.finding('341_345',22,'The prose literally reads lois de composition definie par, with singular definie.',
 'Main third strip and native lower crop both resolve the singular ending. The adjective modifies the plural lois de composition and the two displayed operations; corrected definies preserves both operations and their arguments.',
 'paragraph before6.1.2',witness=356)
id23=r.finding('341_345',23,'The scalar quantifier literally has a,a-prime in A.',
 'The source first defines the ring E(A)=K×I(A), whose projection pi:E(A)→K sends(a,phi) to a; the scalar inclusion is j(a)=(a,1), and pi∘j=id_K. The printed A is related to the required K by its structure homomorphism iota_A:K→A_0, but the first coordinate of E(A) is still the element of K itself. For A=K[T] with T of degree1, the graded inclusion sends constants to degree0, and T is not an allowed first coordinate. Formula6.1.3 is exactly j(a)(a-prime,phi)=(aa-prime,phi^a). Therefore change only this quantifier to a,a-prime in K in the corrected layer. Full maps are recorded in identification_345.json.',
 'quantifier before the sum law',verdict='not applied and now applied',change='Diplomatic A; corrected K in the scalar quantifier.',witness=356)
r.patch(p,'current',r"\forall\,a,a'\in A",r"\forall\,a,a'\in K",id23,'Restore the exact first-coordinate domain of K×I(A).')
r.finding('341_345',24,'L anneau ainsi construit begins an indented paragraph after the multiplication display.',
 'Main third strip and native lower crop confirm the indentation. The supplied paragraph break is retained as layout; its mathematical and lexical token sequence is unchanged.',
 'paragraph after6.1.2',witness=356)
r.finding('341_345',25,'The printed unit is(1.1), using a period.',unit_reason,
 'paragraph after6.1.2, unit pair',witness=356)
for n in (410,411):
 r.source(f'fixes/FIXLOG_6_CURRENT.jsonl#{n}',
  'Printed singular definie.' if n==410 else 'Printed unit(1.1).',
  'The plural agreement repair preserves the two displayed composition laws.' if n==410 else unit_reason,
  'paragraph before6.1.2' if n==410 else 'unit pair after6.1.2',page=p,witness=356)
for n in (310,299):
 r.source(f'fixes/RECONCILE_CODEX_6.json#{n}',
  'Printed singular definie.' if n==310 else 'Printed unit(1.1).',
  'The exact source agreement slip is confirmed in both images; retain the existing corrected plural.' if n==310 else unit_reason,
  'composition-law paragraph' if n==310 else 'unit pair',page=p,witness=356)
for id in ('fixes/FIXLOG_6.jsonl#1478','fixes/FIXLOG_6_CURRENT.jsonl#1583'):
 r.source(id,'Folio344 ends foncteurs sur script G:;345 begins with the two operation displays.',
  'The complete previously viewed344 lower image and the newly viewed345 upper image establish this exact page boundary. The historical log uses the earlier C_g encoding of the script G glyph; its marker placement is correct after that final colon.',
  '344/345 boundary',page=p,witness=356)
r.own_finding('ASTRA-V-LOW-DOTS-345',p,
 'Six hatted object placeholders are low periods; the diplomatic second factor has one additional low period. The two internal multiplication dots in6.1.2 are also low.',
 r'Use \mathord{.} for the six placeholders and diplomatic extra dot; use \mathbin{.} for the two currently centered product dots.',
 'Restore only the eight corrected/nine diplomatic observed low glyphs.',
 'All six hatted dots and the extra second-factor dot are resolved in native356 top; the two internal product dots are resolved in native356 lower at the same lower baseline as the already literal product periods. The placeholder and product roles retain their displayed maps and factor ordering.',
 'first two displays, first prose line, and6.1.2',kind='symbol',witness=356)
r.patch(p,'both',r'\widehat{\cdot}',r'\widehat{\mathord{.}}','ASTRA-V-LOW-DOTS-345','Preserve six observed low object-placeholder periods.',count=6)
r.patch(p,'diplomatic',r'\widehat{\mathord{.}}\cdot{}^{+}',r'\widehat{\mathord{.}}\mathord{.}{}^{+}','ASTRA-V-LOW-DOTS-345','Preserve the additional printed low placeholder period.')
r.patch(p,'both',r'\cdot',r'\mathbin{.}','ASTRA-V-LOW-DOTS-345','Preserve the two internal low product dots in6.1.2.',count=2)
r.own_finding('ASTRA-V-SCRIPT-G-345',p,
 'The single category letter in Ob(G) is a connected hand-drawn script G with a descending tail.',
 r'Retain \mathcal G at this occurrence.',
 'Confirm the actual345 occurrence; the other nominal345 occurrence from the historical global queue is now at the verified344 page end.',
 'Native356 top resolves the connected tail. Its object A is exactly the graded K-algebra input to the functor just defined. The historical16-occurrence queue counts344 final G and345 Ob(G) together under its old345 marker; both are now directly inspected, leaving only347 to close that aggregate.',
 'Soit A in Ob(G)',kind='convention',verdict='confirmed',witness=356)
packet={
 'record_type':'mathematical_identification','page':p,
 'source_ids':[id23,'check/findings/findings_341_345.json#25','fixes/RECONCILE_CODEX_6.json#299'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=359','scan/SGA6_witness_300dpi.djvu#page=356'],
 'printed':{'scalar_domain':'a,a-prime in A','unit':'(1.1)'},
 'corrected':{'scalar_domain':'a,a-prime in K','unit':'(1,1)'},
 'maps':{
  'I':'I(A)=1+completed(A)^+, with addition equal to ordinary series multiplication and multiplication * from6.1.1.',
  'E':'E(A)=K×I(A); (a,phi)+(b,psi)=(a+b,phi psi); (a,phi)(b,psi)=(ab,phi^b psi^a(phi*psi)).',
  'projection':'pi:E(A)→K, pi(a,phi)=a, is a ring homomorphism by both displayed laws.',
  'scalar_inclusion':'j:K→E(A), j(a)=(a,1); pi∘j=id_K. Products and sums of these pairs follow the ordinary K operations.',
  'kernel':'i:I(A)→E(A), i(phi)=(0,phi), identifies I(A) with ker(pi); its inverse is second-coordinate projection on that kernel.',
  'A_relation':'The graded K-algebra structure is iota_A:K→A_0. It maps a scalar to its constant coefficient; it does not change the declared first-coordinate set K in E(A). For A=K[T], deg(T)=1, the coefficient of T of every iota_A(a) is0, whereas that coefficient of T is1.',
  'unit_calculation':'The additive zero of I(A) is the series1, so1*phi=phi*1=1. Then(1,1)(a,phi)=(a,1^a phi^1(1*phi))=(a,phi), and(a,phi)(1,1)=(a,phi).',
  'scalar_action':'j(a)(b,phi)=(ab,1^b phi^a(1*phi))=(ab,phi^a), exactly6.1.3.'},
 'disposition':'Retain the printed domain and period in the diplomatic layer; use precisely K and the ordered pair comma in the corrected layer.'
}
(HERE/'identification_345.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'two operation displays','(aa-prime,phi^a).',
 'Full main359 four strips and native356 top/lower compared. Checked every placeholder and completion hat, doubled dot, two headed arrows and their star/a labels,6.1.1 numerator and denominator, both polynomial primes and weight subscripts, exponential reference3.8, two R_(n,a), script G, all scalar domains, every varphi prime and exponent, addition semicolon, multiplication stop, printed unit period, kernel pair,6.1.3, and both page boundaries. No author note or lexical underlining.',
 witness='Native356 top/lower: witness_345_top.png and witness_345_lower.png.')
r.commit()
