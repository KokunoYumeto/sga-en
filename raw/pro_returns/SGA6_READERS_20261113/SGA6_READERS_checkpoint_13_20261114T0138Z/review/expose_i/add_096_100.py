#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='096_100'
obs={
1:('pour tout j without following punctuation','The displayed line ends after j; the next printed line begins et and ends in the full stop. The attached comma deletion is correct.','Last displayed cohomology isomorphism'),
2:('Plain a)','The letter stands outside the underline beginning Si.','Proposition2.2 first item'),
3:('Plain b)','The letter stands outside the underline beginning Les.','Proposition2.2 second item'),
4:('First defined -pseudo-cohérent plain; its initial n has a short separate rule','Both scans show the word without a rule and short separate rules under n and the category C. The word-span repair is present, but the separate n rule was omitted from its fix. Restore that observed underline in both layers.','Definition2.3 first defined term'),
5:('Second defined -pseudo-cohérent plain; later repeated -pseudo-cohérent underlined','The witness distinguishes the newly defined term from its use in the next clause. The split emphasis preserves these exact word groups.','Definition2.3 second defined term and following clause'),
6:('Proposition2.4 prose underlined before its diagram','All recorded word groups have visible rules. Preserve the attached emphasis span with upright word-group underlining.','Proposition2.4 first paragraph'),
7:('Comma on the F baseline after the triangle','The comma is clearly visible to the right of the lower vertex.','Proposition2.4 triangle'),
8:('Proposition2.4 prose underlined after its diagram','The recorded prose through en degré is underlined, with its mathematical symbols individually set.','Proposition2.4 closing lines'),
9:('Plain a)','The item label precedes the rule under Si and has no individual rule.','Proposition2.5 first item'),
10:('Proposition2.5(a) prose underlined','The statement has visible word-group rules, including both resp. clauses. The attached span is retained.','Bottom statement'),
11:('Plain b) at top of99','This finding was nominally filed under98 before the marker repair. The printed item actually starts99 and its letter has no rule.','Page99 first line'),
12:('Soit underlined at top of99','This finding was nominally filed under98 before the marker repair. The short rule is under Soit on the first line of99.','Page99 first line'),
13:('Page99 begins b) Soit','Page98 ends the full statement2.5(a). The first line of99 is the item letter followed by Soit, before the displayed triangle. The existing marker is correctly placed.','Page99 first line and previous page ending'),
14:('Proposition2.5(b) prose underlined after the triangle','The visible rules cover the specified word groups, keeping the diagram and its mathematical arguments independently set.','First paragraph after triangle(*)'),
15:('Full stop to the right of E in rotated triangle','The period is printed on the lower row. The original first triangle has no terminal punctuation; the third triangle has a comma. The attached three diagrams reproduce those readings.','Second triangle, right of E'),
16:('Page100 begins the opening quote of “vraie”','The opening quotation mark is on100, while99 ends par une. The existing marker correctly precedes that opening mark.','First line and previous page ending'),
17:('Only catégorie triangulée has the word-group underline','The preceding sous-S- is plain prose apart from the site letter’s independent underline. The existing split emphasis matches the page.','Line before Proposition2.7'),
19:('Proposition2.7 without a terminal full stop','The witness confirms a blank after7 before Supposons. Retain that omission diplomatically and the heading stop already restored in current.','Proposition2.7 label'),
20:('Opening proposition prose underlined','The visible prose rules are separate from the short rules on S and C. The span recorded in the attached source is correct.','Proposition2.7 opening'),
21:('C_{0S}, zero and S adjacent','There is no comma between the subscripts; the following full stop is outside the formula.','Proposition2.7 opening identities'),
22:('Plain a)','The item letter precedes and is outside the rule under Si.','Proposition2.7(a)'),
23:('Statement(a) prose underlined; reference(2.1) plain','The prose rule ends before the reference. Preserve the existing statement boundary.','Proposition2.7(a)'),
24:('Plain b)','The item letter precedes and is outside the rule under Désignons par.','Proposition2.7(b)'),
25:('Statement(b) prose underlined','The words through Le foncteur canonique have their visible rules; the formulas carry the independent category typography.','Proposition2.7(b) before final display'),
26:('K^{−,∅}(C_0): loop crossed by a long oblique stroke','The witness shows a small loop crossed by a projecting slash. MainPDF188, printed174, Proposition2.2.9 displays this same handwritten sign beside a separately typed b in the two quotient formulas. Here the immediately following words define this subcategory by acyclicity: its objects have cohomology in the empty set of degrees. The inclusion sends this zero-cohomology subcategory into K^−(C_0), as the denominator of the displayed localization. Retain varnothing. Only that notation region on174 was consulted here.','Proposition2.7(b), name of acyclic subcategory'),
27:('Same K^{−,∅}(C_0) in the denominator','The same crossed-loop glyph is visible in the final display and names the acyclic subcategory just defined above. The source varnothing preserves it.','Last displayed quotient'),
}
for n,(printed,reason,region) in obs.items():
    w=109 if n in[4,5] else 111 if n in[19,20,21,26,27] else None
    r.finding(batch,n,printed,reason,region,witness=w,actual_page=99 if n in[11,12] else None,
        verdict='not applied and now applied' if n==4 else 'confirmed',
        change='Keep the word-span repair; additionally underline the first defined n.' if n==4 else None)
r.patch(98,'both',r'est} \(n\)-\(\mathcal C_0\)-pseudo-cohérent',r'est} \(\underline{n}\)-\(\mathcal C_0\)-pseudo-cohérent',
    'check/findings/findings_096_100.json#4','The first n has its own short underline in both scans.')
id=r.finding(batch,18,'The site S is underlined in exactly the three site occurrences',
    'The S in X∈ob S, in sous-S-catégorie and in Supposons que S names the site and has a short rule. The object subscript S in the first C_S and the last fiber identities stays plain.',
    'All S occurrences on100',verdict='not applied and now applied',change='Underline positions2,3,4 of the six S occurrences; retain object positions1,5,6.')
old=r'\(X\in\Ob S\)';new=r'\(X\in\Ob \underline{S}\)';r.patch(100,'both',old,new,id,'The membership is in the underlined site.')
r.patch(100,'both',r'une sous-\(S\)-',r'une sous-\(\underline{S}\)-',id,'The base of the fibered subcategory is the site.')
r.patch(100,'both',r'Supposons que \(S\)',r'Supposons que \(\underline{S}\)',id,'The punctual site has its printed underline.')
for p,count in[(96,7),(97,4),(98,10),(99,3),(100,21)]:
    id=f'ASTRA-I-C-{p:03d}';reason='Each category C represented by this command has an individual short rule in the full page image. The outside complex, homotopy and derived-category functor letters remain plain.'
    r.own_finding(id,p,'Underlined typed category C',r'\mathcal C',r'\underline{C}',reason,'All category C occurrences')
    r.patch(p,'both',r'\mathcal C',r'\underline{C}',id,reason,count)
for p,count in[(96,8),(98,6),(99,3),(100,4)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The inspected statement and proof word groups are upright and underlined. The independently marked mathematical symbols and the plain defined terms retain their separate typography.'
    r.own_finding(id,p,'Underlined upright word groups',r'\emph spans',r'\uline word groups outside inline formulas',reason,'Every existing emphasis span compared against the printed word groups')
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        new,n=underline_words(old);assert n==count
        r.patch(p,layer,old,new,id,reason)
for p,b,e,w in[(96,'Proposition2.2.','et H^j(M′)=0 pour j≥i.',None),(97,'La formule du cône','achève la démonstration de(2.2).',None),(98,'Définition2.3.','(n−m)-pseudo-cohérent (resp.pseudo-cohérent).',109),(99,'b) Soit','où u est définie par une',None),(100,'“vraie” flèche','K^−(C_0)/K^{−,∅}(C_0)→D(C)',111)]:
    r.page(p,b,e,'Complete prose, formulas, item labels, diagrams and word groups compared. On174 only the quotient-notation reference region was consulted.',witness=w)
r.commit()
