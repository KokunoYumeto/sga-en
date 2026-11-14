#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='091_095'
obs={
1:("Page91 starts que l'hypothèse de finitude",'The whole first line is on91;90 ends on vérifie. The existing marker has already been moved before que l\'.','First line'),
2:('C_{0X}, no comma between subscripts','The adjacent indices have no separator; the comma after the formula belongs to the sentence.','After second cohomology sequence'),
3:('Im, typed I followed by m','The printed image operator consists of the two letters Im. The explicit operatorname at this formula is correct, and the inspected source macro already uses renewcommand for Im, also preserving the two Im operators on90.','B^{n+1}(F_X) definition'),
4:('Full stop at the right of F_X','Both scans place this stop on the bottom row of the octahedron; the added node preserves that position.','Octahedron, bottom right'),
5:('The u′ segment E′—F_X has no arrowhead','The witness confirms the bare segment. Page91 defines u′:E′→F_X and G′ as its cone, fixing its direction; current correctly supplies the arrowhead at F_X while diplomatic retains the unheaded segment.','Octahedron, bottom edge'),
6:('(.) with one pair of parentheses','The print uses one parenthesized baseline point as the display label. The source tag{.} produces that label without doubling the parentheses.','Cohomology sequence label'),
7:('C_{0X}, no comma','The category indices are adjacent, without punctuation.','Paragraph after sequence(.)'),
8:('Page93 begins with H^n(u′):H^n(E_X)⊕M→H^n(F_X)','The whole display is printed at the top of93, followed by est un épimorphisme. The attached marker is correctly above its opening display delimiter.','First display and following line'),
9:('First two C plain; C in D(C) individually underlined','The witness confirms the two missing rules. The given category C is the category of the complexes E,F and the argument of its derived category D(C); current uses the underlined category symbol consistently for this same object.','Lemma1.4.2 first two lines'),
10:('n-quasi-isomorphisme and n-isomorphisme have no word-group underline','The word groups surrounding the defined names are underlined; the names themselves are plain. The existing split emphasis spans preserve this distinction.','Definition1.4.3'),
11:('Corollary1.4.5 prose underlined','The word groups throughout the statement are underlined. The existing emphasis span is correct and is changed locally to upright word-group rules.','Last statement before triangle'),
12:('Comma after the triangle on the F baseline','The comma is visible to the right of the diagram at its lower row.','Corollary1.4.5 triangle'),
14:('Underlined prose ends at en degré; following explanatory parenthesis is plain','The first two lines have exactly these prose rules; the parenthesis beginning i.e. is outside them. Retain the existing boundary.','First two lines'),
15:('Comma to the right of the first triangle','The comma is clearly printed on the F baseline.','First triangle, right side'),
16:('Comma to the right of the second triangle','The comma is clearly printed on the F baseline.','Second triangle, right side'),
17:('The three defined names beginning strictement C_0-n-pseudo-cohérent are plain','The witness shows their category symbols separately underlined, while the surrounding statement word groups carry prose rules. Keep those names outside the emphasis wrappers.','Definition2.1'),
18:('C_{0S}, with adjacent zero and S','Both scans show adjacent indices. The comma deletion is confirmed independently of the correction of the index S to X.','Definition2.1 membership condition'),
20:('Baseline ellipsis in the exact sequence','The three dots sit on the baseline below the arrows. The attached ldots matches the print.','Proof of Lemma2.1.1, displayed sequence'),
}
for n,(printed,reason,region) in obs.items():
    w=103 if n in[4,5] else 104 if n==9 else 106 if n in[17,18] else None
    r.finding(batch,n,printed,reason,region,witness=w)
id=r.finding(batch,19,'E^i∈ob C_{0S}',
    'The witness confirms S. The same sentence declares E a complex in the fiber C_X at X, hence each component E^i belongs to C_X; the full additive subcategory of that fiber is C_{0X}. The fixed object S of2.0 has no role in this arbitrary-X membership condition. Current corrects exactly this fiber index to X.',
    'Definition2.1, membership condition',verdict='not applied and now applied',change='Current C_{0S}→C_{0X}.',witness=106)
r.patch(95,'current',r'\mathcal C_{0S}',r'\mathcal C_{0X}',id,'The components belong to the fiber at the declared object X.')
id=r.finding(batch,13,'Underlined site S and plain object S',
    'The first S in Corollary1.4.4 names the site, the second its object. Page94 names the punctual site;2.0 explicitly declares the site and object separately. The occurrence map preserves these readings without altering the object subscripts.',
    'All S occurrences on93–95',verdict='not applied and now applied',change='Underline93 position1;94 position1;95 positions1,3,4,5,6.')
for p,indices in[(93,{1}),(94,{1}),(95,{1,3,4,5,6})]:
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        ordinal=[0]
        def sub(m):
            ordinal[0]+=1
            return r'\underline{S}' if ordinal[0] in indices else m.group(0)
        r.patch(p,layer,old,re.sub(r'(?<![A-Za-z\\])S(?![A-Za-z])',sub,old),id,'Use the observed site/object occurrence map.')
for p,count in[(91,5),(92,6),(93,9),(94,4),(95,14)]:
    id=f'ASTRA-I-C-{p:03d}';reason='The category C letters represented by this command have individual rules in the complete page image, including those inside C(C), K(C), or D(C); the complex-category or derived-category functor letter outside the parentheses stays plain.'
    r.own_finding(id,p,'Plain typed category C with an individual underline',r'\mathcal C',r'\underline{C}',reason,'All category symbols on the page')
    for layer in['diplomatic','current']:
        n=count+2 if p==93 and layer=='current' else count
        r.patch(p,layer,r'\mathcal C',r'\underline{C}',id,reason,n)
for p,n in[(93,8),(94,2),(95,4)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The inspected statement word groups and proof heading are upright and underlined, with formulas carrying their own separately recorded typography. Defined terms excluded from the original emphasis spans stay plain.'
    r.own_finding(id,p,'Upright underlined word groups',r'\emph spans',r'\uline word groups outside inline formulas',reason,'Statement prose and proof headings')
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        new,count=underline_words(old);assert count==n
        r.patch(p,layer,old,new,id,reason)
id='ASTRA-I-NUMBER-095';reason='The paragraph number2.0 is plain type. NOTE_6 leaves the paragraph-number convention open; retain the observed plain number, independently of its permitted bold statement labels.'
r.own_finding(id,95,'Plain 2.0.',r'\textbf{2.0.}','2.0.',reason,'Opening numbered paragraph',kind='font')
r.patch(95,'both',r'\textbf{2.0.}',r'2.0.',id,reason)
for p,b,e,w in[(91,"que l'hypothèse de finitude",'0→E_X→E′→M[−n]→0,',None),(92,'avec u′v=u_X.','à partir de la suite exacte (.), que',103),(93,'H^n(u′):H^n(E_X)⊕M→H^n(F_X)','Triangle E→E′ above F, followed by comma',104),(94,'où u′ est un quasi-isomorphisme','répondent à la question.',None),(95,'Autrement dit, en abrégé','qui en est un quotient.',106)]:
    r.page(p,b,e,'Complete prose, formulas and all diagram edges compared. The mathematical correction of the final transition-map formula on94 has its own explicit decision.',witness=w)
r.commit()
