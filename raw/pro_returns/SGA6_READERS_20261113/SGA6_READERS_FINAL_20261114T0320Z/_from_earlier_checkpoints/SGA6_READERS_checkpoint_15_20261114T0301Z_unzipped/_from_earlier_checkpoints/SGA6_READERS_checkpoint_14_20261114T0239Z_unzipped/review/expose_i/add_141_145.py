#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='141_145'
observations={
1:('Page141 opens6.2. Soient C','The complete140/141 images place6.2 at the start of141. The attached marker already agrees.','Boundary140/141',None),
2:('Bare summation sign in6.4.1','The hand-drawn sum has no index underneath it. The following exponent i and L^i supply the degree parameter exactly as printed.','Formula6.4.1',None),
3:('Add(C,.) with a baseline placeholder point','The point sits beside the low comma in the typed argument slot. Keep the attached literal point.','Paragraph6.3, representable functor',None),
5:('Definition6.5 opening prose underlined by word groups','The formula f_X:ob(C_X) to F(X), all mathematical letters and the reference1.1.1 have their independent styling. The final colon remains outside the word rule.','Definition6.5 opening',None),
6:('pour tout and est une fonction additive underlined','The reference6.1 and following semicolon remain plain. The indexing misprint is separately adjudicated.','Definition6.5(i)',None),
7:('Definition6.5(ii) prose word groups underlined','The arrow u:X to Y is outside the prose rule, and the base S has its own short rule.','Definition6.5(ii)',None),
8:('Definition6.5 last sentence underlined by word groups','The final Add expression is independently typed, with its own underlined base and category letters.','Definition6.5 closing sentence',None),
18:('Proposition6.7 opening prose underlined','The reference4.0 and its stop remain outside the word rules. All three category occurrences have independent rules.','Proposition6.7 before display',154),
19:('Proposition6.7 continues to sur S, at page end','The native witness gives prose rules, a rule under the second Parf operator, and the final site rule. The next page begins the complete word l’homomorphisme.','Proposition6.7 after display and page end',154),
20:('Page144 begins l’homomorphisme de restriction','The last words of143 are sur S,. The attached marker stands before l’ and the comment joins its continuation without a space.','Boundary143/144',None),
21:('l’homomorphisme de restriction underlined','The first line has one continuous word-group rule. The existing two TeX emphasis spans preserve the joined word.','Proposition6.7 continuation',None),
22:('est un isomorphisme underlined; stop outside','The statement’s final full stop lies beyond the rule.','Proposition6.7 end',None),
23:('Full stop after Remarque6.7.1','The main page clearly has the stop before the following parenthetical reference.','Remark6.7.1 heading',None),
24:('Il en est donc de même de a, cqfd. on a new line','The sentence follows a completed short line and starts at the left margin. Preserve the attached paragraph separation as layout.','Proof6.7 conclusion',None),
25:('Page145 begins6.8. Soient(S,A)','Page144 ends the remark with(*=−ou b). The next paragraph label belongs to145, as in the attached marker.','Boundary144/145',None),
26:('Page145 ends with the four-term k display','The viewed top region of146 starts(les deux de gauche étant des homomorphismes. The attached146 marker is correctly before that parenthesis.','Boundary145/146',None),
27:('Double-stem L in Lu*','The main image resolves the extra vertical stem of the L preceding u*. The superscript L above the tensor product below is plain.','Paragraph6.8, inverse-image functor',None),
28:('No comma at the bottom-right corner of the square','The square ends with the closing parentheses of k(D^−(_A-prime S-prime)_parf), with no following punctuation.','Paragraph6.8 square',None),
}
for n,(printed,reason,region,witness) in observations.items():r.finding(batch,n,printed,reason,region,witness=witness)
for n,region in [(13,'First displayed map'),(14,'Definition of the map on a triangle'),(15,'Additivity condition'),(16,'Arrow in6.6.1')]:
    r.finding(batch,n,'Closed phi with a stroke above and below the loop','The native witness shows the same closed loop and long crossing stroke in all four positions. Retain the attached phi consistently at these four occurrences.',region,witness=154)

id='ASTRA-I-C-141';reason='Every category C on141, including the four in the author note, is a plain typed letter; the single D in the functor target is also plain. The first two C letters on142 continue the same lemma and are plain. The letterforms are read directly, without inferring a font from a category’s properties.'
r.own_finding(id,141,'Thirty-six plain C letters and one plain D',r'\mathcal C and \mathcal D','Plain C and D with control-word delimiters preserved',reason,'Paragraphs6.2/6.3, Lemma6.4 and author note',kind='font',witness=152)
r.patch(141,'both',r'\mathcal C','C',id,reason,count=36)
r.patch(141,'both',r'\to\mathcal D',r'\to D',id,reason)
for p,count in [(142,20),(143,24),(144,20),(145,14)]:
    id=f'ASTRA-I-C-{p:03d}';reason='The inspected C occurrences have independent lower rules throughout this page, except the first two C letters of142, which continue Lemma6.4 and remain plain. All indices, primes and is superscripts retain their printed positions.'
    r.own_finding(id,p,'Exact plain/underlined category C occurrence map',r'\mathcal C',r'C at142 positions1/2; \underline{C} at all remaining positions',reason,'Every category C occurrence',kind='font',witness=153 if p==142 else 154 if p==143 else None)
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        matches=list(re.finditer(re.escape(r'\mathcal C'),old));assert len(matches)==count,(p,len(matches))
        new=old
        for i,m in reversed(list(enumerate(matches,1))):
            replacement='C' if p==142 and i<=2 else r'\underline{C}'
            new=new[:m.start()]+replacement+new[m.end():]
        r.patch(p,layer,old,new,id,reason)
r.finding(batch,4,'Plain C/D through6.4; underlined C from6.5','The full141 image, its native author-note crop and the complete142 image determine the exact letters. Replace the36 C and one D on141, retain plain C at the first two positions of142, and restore the later visible C rules.','Category letter forms on141–142',verdict='not applied and now applied',change='Apply exact glyph maps in both layers.',witness=152)

id='ASTRA-I-INDEX-142';reason=('The printed quantifier is X∈ob C_X. The family just defined has one function f_U:ob(C_U) to F(U) for each U∈ob S. Its additive condition is f_U(L)=f_U(L-prime)+f_U(L-double-prime) on the direct sum or distinguished triangle in that fibre. Thus the quantifier selecting those functions is U∈ob S, with the original dummy variable X retained. Current replaces only C_X by the base S; diplomatic retains the print.')
r.finding(batch,9,'X∈ob C_X',reason,'Definition6.5(i), indexing quantifier',verdict='not applied and now applied',change='Current: X∈ob S, with the printed site rule.')
for row in r.decisions:
    if row.get('source_id')==f'check/findings/findings_{batch}.json#9' or row.get('related_finding')==f'check/findings/findings_{batch}.json#9':row['is_misprint']=True
r.own_finding(id,142,'X∈ob C_X','Both layers retain the printed fibre index','Current X∈ob S',reason,'Definition6.5(i)',kind='misprint_in_print')
r.own[-1]['is_misprint']=True
r.patch(142,'current',r'pour tout \(X\in\Ob\underline{C}_X\)',r'pour tout \(X\in\Ob S\)',id,reason)
r.finding(batch,10,'The lower f_X edge is a line without a head','The scan has a head on f_Y and a headless f_X line. The declared map f_X:ob(C_X) to F(X) immediately above determines the orientation; the square expresses f_X(u*L)=F(u)(f_Y(L)). Keep the headless stroke diplomatically and the existing rightward arrow in current.','Definition6.5 commutative square',change='Retain diplomatic dash and current rightward f_X arrow.')
r.finding(batch,17,'The first inline Cart(C^is,F) has plain F','The native witness shows no F rule here, while the adjacent Cart expressions have one. The fibre construction on142 sends a value x∈F(U) to the object(U,x), with restriction arrows specified by F(u); projection to x is its inverse description. For a cartesian functor, c∈C_U maps to(U,f_U(c)). This identifies the intended codomain with the explicitly named underlined F used on both sides of phi. Keep the isolated plain glyph diplomatically and the existing restored rule in current.','Definition of phi, first inline Cart argument',witness=154)

for p,count in[(142,18),(143,16),(144,14),(145,15)]:
    id=f'ASTRA-I-SITE-{p:03d}';reason='Every S at these inspected positions has its own lower rule, including the Add and Cart subscripts and the primed site. Preserve all primes and brace bare subscripts after inserting the rule.'
    r.own_finding(id,p,'All site S letters underlined','Plain S commands',r'\underline{S} at each observed occurrence',reason,'Every S occurrence',witness=153 if p==142 else 154 if p==143 else None)
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        matches=list(re.finditer(r'(?<![A-Za-z\\])S(?![A-Za-z])',old));expected=count+(1 if p==142 and layer=='current' else 0);assert len(matches)==expected,(p,layer,len(matches),expected)
        new=old
        for m in reversed(matches):new=new[:m.start()]+r'\underline{S}'+new[m.end():]
        new=new.replace(r'_\underline{S}',r'_{\underline{S}}')
        r.patch(p,layer,old,new,id,reason)
r.finding(batch,11,'Underlined S at all observed base-site positions','The four complete pages show the separate S rules, including lowered Add/Cart indices. The current indexing repair in6.5(i) acquires the same rule as its explicitly stated family index.','Site notation on142–145',verdict='not applied and now applied',change='Apply exact S rules in both layers.',witness=153)

cart_reason='The scan has one rule under each Cart operator (2 on142,6 on143,4 on144). The active source definition is \\providecommand{\\Cart}{\\underline{\\operatorname{Cart}}}. Its exact expansion already supplies that rule; the earlier local wrapper expanded to \\underline{\\underline{\\operatorname{Cart}}} and produced two rules in the rendered reader. Withdraw that wrapper and retain the source macro at these twelve positions. The separately ruled S subscript is unchanged.'
for p,count in[(142,2),(143,6),(144,4)]:
    id=f'ASTRA-I-CART-{p:03d}'
    r.own_finding(id,p,'One rule under Cart',r'\Cart already supplies one rule','Retain the original macro; withdraw the extra wrapper',cart_reason,'Every Cart occurrence',verdict='amended',witness=153 if p==142 else 154 if p==143 else None)
r.finding(batch,12,'Twelve Cart operators independently underlined',cart_reason,'All twelve Cart operators',change='Retain the original Cart macro: its active definition supplies one rule.',witness=154)
id='ASTRA-I-PARF-143';reason='The native witness leaves Parf plain in the displayed k map, then visibly extends the word rule under Parf in the following statement after dans. Restore only that second occurrence.'
r.own_finding(id,143,'Second Parf underlined; first plain','Both Parf operators plain',r'\underline{\Parf} at the statement occurrence only',reason,'After the Proposition6.7 display',witness=154)
r.patch(143,'both',r'dans \(\Parf(\underline{C},\underline{C}_0)\)',r'dans \(\underline{\Parf}(\underline{C},\underline{C}_0)\)',id,reason)

for p,labels in[(141,['6.2.','6.3.']),(142,['a)']),(143,['b)']),(145,['6.8.','6.9.'])]:
    id=f'ASTRA-I-ITEMS-{p:03d}';reason='The exact paragraph numbers and item letters use the plain running type in the scan. Remove their added bold.'
    r.own_finding(id,p,'Plain paragraph/item labels','Bold labels','Plain labels',reason,'Selected labels',kind='font')
    for label in labels:r.patch(p,'both',r'\textbf{'+label+'}',label,id,reason)
id='ASTRA-I-NOTE-141';reason='Both the main call and native witness note label use a raised star within baseline parentheses. Preserve the whole note, its lowercase opening nous, and all four plain C letters.'
r.own_finding(id,141,'Parenthesized raised-star author note','Automatic footnote number','Explicit raisedstar author note',reason,'Paragraph6.3 and bottom author note',kind='font',witness=152)
r.patch(141,'both',r'\footnote{nous',r'\SGAAuthorFootnote{raisedstar}{nous',id,reason)
for p in[141,144]:
    id=f'ASTRA-I-PROOFSTOP-{p:03d}';reason='The proof-heading rule ends after Preuve; the stop remains outside. Apply the one inspected heading on this page.'
    r.own_finding(id,p,'Proof word underlined, stop plain',r'\emph{Preuve.}',r'\emph{Preuve}.',reason,'Proof heading')
    r.patch(p,'both',r'\emph{Preuve.}',r'\emph{Preuve}.',id,reason)
for p,count in[(141,2),(142,4),(143,2),(144,4)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The observed statement and proof word groups are upright with rules. Mathematical expressions keep their separately adjudicated letterforms. Numbered references and the explicitly plain punctuation remain outside those prose rules.'
    r.own_finding(id,p,'Upright underlined prose groups',r'\emph spans',r'\uline word groups',reason,'Every existing emphasis span',witness=154 if p==143 else None)
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        plain={141:['.','(',')'],142:['(1.1.1)','.'],143:['(4.0).'],144:[]}[p]
        new,n=underline_words(old,plain);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)
for p,b,e,w in[(141,'6.2. Soient C','Formula6.4.1 f(L)=sum(-1)^i f(L^i); note ends à homotopie près.',152),(142,'pour L∈ob K^b(C)','associée à un groupe',153),(143,'abélien, et l’on a un homomorphisme','pour tout faisceau abélien F sur S,',154),(144,'l’homomorphisme de restriction','(*=−ou b).',None),(145,'6.8. Soient(S,A)','k(C_1)→k(C_0)→k(D^−(S)_parf)→k(Parf(S))',None)]:
    r.page(p,b,e,'Complete prose, all category and site letter occurrences, functor names, degree and is superscripts, every diagram edge/label, punctuation, author note and page boundaries compared. Native crops resolve the phi strokes, isolated F rule, Parf rule and raised-star note.',witness=w)
r.commit()
