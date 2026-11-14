#!/usr/bin/env python3
from review_helpers import Review,ROOT,underline_words
r=Review();batch='101_105'
observations={
1:('Opening prose underlined; derived-category formula separately set','The rule covers the stated prose through essentielle, ending before the formula.','First line'),
2:('Comma beside F in the first triangle','The comma is on the lower row to the right of F. All three arrows and their indices agree with the source.','Proof2.7(a), first triangle'),
3:('Statement2.7.1 underlined by word groups','The displayed prose groups carry visible rules, while the mathematical expressions have their own typography.','Proposition2.7.1 before its diagram'),
4:('Comma beside F in the second triangle','The comma is on the lower row, to the right of the F vertex.','Proposition2.7.1 triangle'),
5:('Closing statement word groups underlined','The last printed line ends et v un; the statement continues on102.','Last line'),
6:('Opening monomorphisme through degré underlined','The short continuation is underlined; the inequality and its final stop are independently set.','First line'),
7:('Definition2.8 prose groups underlined, defined term plain','The witness confirms the plain defined words and the separate category rule. The initial defined n also has a short rule, recorded separately below.','Definition2.8 before first display'),
8:('Definition2.8 prose groups underlined after the display','The first occurrence of the infinity-presentation term is defined without a word rule; its subsequent use is underlined.','Definition2.8 after first display'),
9:('C_{0X}, with adjacent subscripts and no comma','Both scans show the zero and X adjacent under the category letter.','Definition2.8 membership condition'),
10:('Three typed baseline dots in the first sequence','The witness resolves all three dots on the letter baseline. The hand-drawn arrows also sit low; their shaft height does not change the printed dot position.','Definition2.8 exact sequence'),
12:('Opening Proposition2.9 word groups underlined','The separate groups Soient, et and Conditions équivalentes have rules; the colon follows the last group.','Proposition2.9 opening'),
13:('Statement(i) prose groups underlined','The rules cover est de, présentation finie, resp. and the second présentation finie; n and infinity are independently set.','Proposition2.9(i)'),
14:('Statement(ii) prose groups underlined','The negative index (-n) is clearly present; pseudo-cohérent and the resp. clause are underlined.','Proposition2.9(ii)'),
15:('Punctual-site statement underlined by word groups','The site letter itself has a separate short rule; it is recorded as an occurrence-specific category-base notation below.','Proposition2.9 punctual-site assertion'),
16:('Both groups of three baseline dots in the second sequence','The witness places the dots on the typewritten letter baseline, as in the earlier sequence.','Proposition2.9 exact sequence'),
17:('avec and pour tout underlined','The membership formula has its independent underlined category C; the final i and full stop are outside the word rules.','Last assertion of Proposition2.9'),
18:("Page103 begins l'implication",'Page102 ends et. The apostrophe and the whole following word begin103; the attached marker is correctly placed.','Page103 first line and preceding page ending'),
19:('Comma to the right of H^n(F)[-n]','The triangle has F on the lower left, H^n(F)[-n] on the lower right, F-prime above and +1 on the downward left edge. Its comma is on the lower row.','Proof2.10(b) triangle'),
22:('Full stop to the right of H^{n+N}(F)[-n-N]','The last triangle ends with a full stop on the lower row. The following cohomology equalities and index bounds agree with the print.','Proof2.11(b) triangle'),
}
for n,(printed,reason,region) in observations.items():
    r.finding(batch,n,printed,reason,region,witness=113 if 7<=n<=17 else 114 if n==18 else None)
r.finding(batch,11,'A paragraph begins Nous dirons de présentation finie',
    'The new paragraph is visible in both scans. Retain the existing break as a typesetting decision; it does not alter a word or a mathematical expression.',
    'Paragraph after Bien entendu',verdict='amended',change='Retain paragraph break; classify as layout only.',witness=113)
r.finding(batch,23,'The cohomology expression is in the running paragraph',
    'The scan places H^n(F-prime≤n+F-double-prime≤n) before est de type fini on the same text line. The following sum identity is a separate display. Retain that disposition as layout, without a content correction.',
    'Proof2.12 final paragraph',verdict='amended',change='Keep attached inline formula; classify as layout only.')
id=r.finding(batch,20,'alors F est pseudo-cohérent.',
    'The unqualified conclusion is printed. The proof concludes n-pseudo-coherence on105. Its induction applies (n−1)-pseudo-coherence to F-prime: H^i(F-prime)=H^{i+1}(F), so the presentation index (i+1−n) is exactly i−(n−1). For the failure of the printed conclusion, take the punctual site of vector spaces over a field, C_0 finite-dimensional vector spaces, n=0, and F=M[1] with M an infinite-dimensional vector space. Every H^i(F) for i≥0 is zero, so the stated finite presentation hypotheses hold; H^(−1)(F)=M is not of finite type, contradicting (−1)-pseudo-coherence by2.10(b). Restore the n-qualified conclusion and its resp. clause as proved.',
    'Proposition2.11(b) last line',verdict='not applied and now applied',
    change='Current only: alors F est n-pseudo-cohérent (resp. pseudo-cohérent).')
r.patch(104,'current',r"finie), alors \(F\) est pseudo-cohérent.}",r"finie), alors \(F\) est \(n\)-pseudo-cohérent (resp. pseudo-cohérent).}",id,'The proof and the explicit punctual-site counterexample determine the qualified conclusion.')
id=r.finding(batch,21,'F^i≠0 pour i>n+N',
    'The diagonal stroke of the printed inequality is clear. The complex belongs to C^− and hence vanishes above a bound. The induction removes the highest nonzero component F^{n+N} by the displayed exact sequence, leaving F-prime zero above n+N−1. Its required starting bound is F^i=0 for i>n+N; the printed inequality is incompatible with a bounded-above complex.',
    'Proof2.11(a) first line',verdict='not applied and now applied',change='Current only: F^i=0.')
r.patch(104,'current',r'\(F^i\neq0\)',r'\(F^i=0\)',id,'The exact sequence removes the highest component of a bounded-above complex.')
id='ASTRA-I-SIGN-103'
reason='Both scans print strictement n-pseudo-cohérent. Assertion2.9(ii) is (−n)-pseudo-coherence. Apply2.4 to the actual map0→F, with pseudo-coherence parameter−n and quasi-isomorphism parameter1: its replacement E→F is strictly(−n)-pseudo-coherent and the comparison0→E is the identity in degrees≥1. Thus E^i=0 for i≥1, while the required components E^(−n),…,E^0 lie in C_0. These are precisely the terms of the n-presentation in2.8. The missing minus sign is determined by this exact substitution into2.4.'
r.own_finding(id,103,'strictement n-pseudo-cohérent',r'strictement \(n\)-pseudo-cohérent','Current only: strictement (−n)-pseudo-cohérent',reason,'Proof2.9, third printed line',kind='misprint_in_print',witness=114)
r.patch(103,'current',r'avec \(E\) strictement \(n\)-pseudo-cohérent et \(E^i=0\) pour \(i\geq 1\)',r'avec \(E\) strictement \((-n)\)-pseudo-cohérent et \(E^i=0\) pour \(i\geq 1\)',id,reason)
id='ASTRA-I-DEFINEDN-102';reason='The enlarged witness detail shows a short rule beneath the first n in the defined n-C_0-presentation term, in addition to the independent rule under C. The following words présentation finie have no rule.'
r.own_finding(id,102,'First defined n separately underlined',r'plain n',r'\underline{n}',reason,'Definition2.8 first defined term',witness=113)
r.patch(102,'both',r'est de} \(n\)-\(\mathcal C_0\)-présentation finie',r'est de} \(\underline{n}\)-\(\mathcal C_0\)-présentation finie',id,reason)
for p,count in[(101,9),(102,8),(103,3),(104,3),(105,2)]:
    id=f'ASTRA-I-C-{p:03d}';reason='Each category C represented by this command is a typed letter with an individual short underline in the page image. The outer complex and derived-category functor letters retain their independently observed typography.'
    r.own_finding(id,p,'Underlined typed category C',r'\mathcal C',r'\underline{C}',reason,'All category C occurrences')
    r.patch(p,'both',r'\mathcal C',r'\underline{C}',id,reason,count)
for p,old,new in[(102,r'Dans le cas où \(S\)',r'Dans le cas où \(\underline{S}\)'),(103,r'Si \(S\) est ponctuel',r'Si \(\underline{S}\) est ponctuel')]:
    id=f'ASTRA-I-SITE-{p:03d}';reason='This occurrence names the punctual site and has a short underline. Every other S on the page names an object or its fiber subscript and remains plain, exactly as the image shows.'
    r.own_finding(id,p,'Underlined site S',r'plain S',r'\underline{S} at the single site occurrence',reason,'Punctual-site assertion')
    r.patch(p,'both',old,new,id,reason)
for p,items in[(103,2),(104,4)]:
    id=f'ASTRA-I-ITEMS-{p:03d}';reason='The a) and b) labels are plain type; statement and proof labels have no bold weight or separate underline.'
    r.own_finding(id,p,'Plain a), b) labels',r'\textbf item labels','Plain item labels',reason,'All a)/b) labels',kind='font')
    r.patch(p,'both',r'\textbf{a)}','a)',id,reason,items//2)
    r.patch(p,'both',r'\textbf{b)}','b)',id,reason,items//2)
for p,count in[(101,4),(102,11),(103,3),(104,4),(105,2)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The inspected statement and proof spans use upright underlined word groups. The formulas, the defined terms explicitly left plain, and the separate category/site rules retain their independent markings.'
    r.own_finding(id,p,'Upright underlined word groups',r'\emph spans',r'\uline groups outside inline formulas',reason,'Every source emphasis span compared to the page')
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        new,n=underline_words(old);assert n==count
        r.patch(p,layer,old,new,id,reason)
for p,b,e,w in[(101,'est pleinement fidèle','et v un',None),(102,"monomorphisme induisant l'identité",'sur les définitions, et',113),(103,"l'implication(ii)⇒(i)",'On conclut grâce à(2.5) et(2.6).',114),(104,'Proposition2.11.','H^i(F′)≃H^{i+1}(F) pour i<n+N−1.',None),(105,"Par l'hypothèse de récurrence",'H^n(F′≤n+F″≤n)=H^n(F′≤n)+H^n(F″≤n),',None)]:
    r.page(p,b,e,'Entire prose, formulas, diagrams, punctuation, labels and statement word groups compared. New mathematical repairs retain the printed reading diplomatically.',witness=w)
r.commit()
