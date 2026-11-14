#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='156_160'
observations={
1:('The introductory sentence ends dans la','The main and witness leave the line after dans la empty. The following heading completes the sentence; proposition suivante is absent.','Before Proposition8.3',167,None),
2:('Double-stem R and underlined Hom in the first restricted complex','Both scans have the separate R stroke and Hom rule. The restriction U stays on the baseline.','First paragraph first RHom',167,None),
3:('Double-stem R and underlined Hom in the second restricted complex','The second argument order is F,E, with U on the restriction baseline.','First paragraph second RHom',167,None),
4:('First displayed RHom has doubled R and ruled Hom','The target begins with RHom(E,F), followed by a derived tensor sign.','First display first factor',167,None),
5:('Second displayed RHom has doubled R and ruled Hom','The second factor is RHom(F,E), and the U restricts the whole parenthesized product.','First display second factor',167,None),
6:('Dans la situation de, pour, et and on a underlined','The reference8.2 and the Hom formulas remain plain. The two trace orders vu and uv and pairing agree.','Proposition8.3 first assertion',167,None),
7:('En particulier, si and on a underlined','The commas and E=F are outside the word rules. The second display retains both occurrences of Id.','Proposition8.3 second assertion',167,None),
8:('Left triangle label Id⊗L τ_F','The native witness resolves a plain superscript L above the tensor on the vertical edge. The printed diagram is on157, although this inherited record was filed under156 before the marker move.','Page157 left triangle',168,157),
9:('Right triangle label τ_E⊗L Id','The native witness resolves the L above this tensor. The τ_E and Id order is exactly as printed. This inherited record belongs to157 after the marker correction.','Page157 right triangle',168,157),
10:('Page157 begins with both triangle diagrams','The complete156 page ends after the parenthetical proof lead-in and the author note. The first printed material on157 is the pair of triangles, followed by the square. The attached marker agrees.','Boundary156/157',168,None),
11:('Top square label Id⊗L τ_E','The native witness resolves the L and keeps the printed Id,τ_E order. No permutation of the label words is imposed.','Page157 square top edge',168,None),
13:('Corollary8.4 has five underlined prose groups','The E,F,U formula, reference8.2, Hom formulas, s and sus−1 remain independent. The trace equality and final stop agree.','Corollary8.4 statement',168,None),
14:('Plain typed E in E(C)','The native witness has no rule beneath E; C has its own lower rule.','Remark8.5 category construction',168,None),
15:('Plain typed E in the source of the trace functor','The printed E remains plain before D(S), while S and the first parf index have rules.','Remark8.5 inline functor source',168,None),
16:('First inline parf index underlined','The native witness gives a distinct lower rule beneath this index.','Remark8.5 inline category index',168,None),
17:('A underlined in the trace functor target','The short lower rule is attached to A.','Remark8.5 first target A',168,None),
18:('A underlined in its following description','The categorical A retains its rule; the later sheaf A defining it is plain.','Remark8.5 description of A',168,None),
19:('Plain E in the forgetful functor source','The native witness has an ordinary typed E without a rule.','Remark8.5 final display source',168,None),
20:('Source parf underlined; target parf plain','The native witness resolves the lower rule only under the first parf index. Both S letters have their own lower rules.','Remark8.5 final display indices',168,None),
21:('Plain E in the forgetful functor target','The target E is the same ordinary typed glyph as the source. No final punctuation follows the display.','Remark8.5 final display target',168,None),
22:('Plain typed E in the continued trace functor source','The complete158 image retains ordinary E, ruled S, plain parf and raised is.','Page158 first line category',169,None),
23:('Target A underlined','The final point lies after the ruled A.','Page158 first line target',169,None),
24:('Soient, d’où and On a underlined','The site S has its independent rule, while both Parf operators on158 are plain. Every Hom, trace, tensor and argument order agrees.','Proposition8.6 statement',169,None),
25:('BIBLIOGRAPHIE in plain capitals','The complete159 image has this unruled heading at its top. Its inherited record was filed under158 before the marker correction.','Page159 heading',None,159),
26:('Page159 begins BIBLIOGRAPHIE','The complete158 page ends with On termine grâce à8.1.1;159 begins the bibliography heading. The attached marker agrees.','Boundary158/159',None,None),
27:('Residues and Duality in plain type','The entire printed Hartshorne entry is plain, and its Lecture Notes number20, publisher, year1966 and punctuation agree.','Bibliography[H]',None,None),
28:('Catégories dérivées in plain type','The complete Verdier entry retains J-L., I.H.E.S. and1963 as printed.','Bibliography[V]',None,None),
29:('Cohomologie non abélienne in plain type','The Giraud entry retains the printed future-publication wording and abbreviated North Holl. Pub. Comp.','Bibliography[G]',None,None),
30:('Cohomologie étale des schémas in plain type','All three authors and the comma before et agree, as does the printed future-publication wording.','Bibliography SGA4',None,None),
31:('Cohomologie ℓ-adique et fonctions L in plain type','The raised-loop handwritten ℓ, author and future-publication wording agree.','Bibliography SGA5',None,None),
32:('Topos annelés et schémas relatifs in plain type','The Hakim initial M., thèse and parenthetical en préparation agree.','Bibliography[1]',None,None),
33:('Les catégories dérivées des catégories abéliennes in plain type','The Verdier title, initials and publisher abbreviation agree word by word.','Bibliography[2]',None,None),
34:('Homological Algebra in plain type','The Cartan/Eilenberg names and initials, Princeton and1956 agree.','Bibliography[MULT]',None,None),
}
for n,(printed,reason,region,witness,actual) in observations.items():r.finding(batch,n,printed,reason,region,witness=witness,actual_page=actual)

reason='The native witness prints Id⊗τ_F with no L on the square’s left edge, while the same source/target edge in the left triangle has L. Its map is the derived contraction β=id_(E∨)⊗L(ev_F∘c_(F,F∨))⊗L id_E from E∨⊗L F⊗L F∨⊗L E to E∨⊗L E: c exchanges the middle factors, ev_F:F∨⊗L F→A is the evaluation used in8.1, and the two unit factors are removed by the unit isomorphisms. This is the very contraction already used in the parallel triangle. Restore the omitted derived-functor exponent in current, preserving the printed ordinary tensor label in diplomatic.'
id=r.finding(batch,12,'Square left edge prints Id⊗τ_F without L',reason,'Page157 square left edge',verdict='not applied and now applied',change=r'Current: \Id\otL\tau_F; diplomatic retains \Id\otimes\tau_F.',witness=168)
for row in r.decisions:
    if row.get('source_id')==id or row.get('related_finding')==id:row['is_misprint']=True
r.patch(157,'current',r'''\arrow[d,"\Id\otimes\tau_F"']''',r'''\arrow[d,"\Id\otL\tau_F"']''',id,reason)

for p,count in [(157,3),(158,2)]:
    id=f'ASTRA-I-C-{p:03d}';reason='Every printed category C on these two pages has a lower rule, including the C inside E(C) and the two C_0 occurrences in the final proof. The indices stay outside the rules.'
    r.own_finding(id,p,'Underlined typed C','Script C',r'\underline{C}',reason,'All category C occurrences',kind='font',witness=p+11)
    r.patch(p,'both',r'\mathcal C',r'\underline{C}',id,reason,count=count)
for p,count in [(157,10),(158,4)]:
    id=f'ASTRA-I-SITE-{p:03d}';reason='Both main and witness resolve a lower rule beneath every S on these pages, including the three D(S) expressions on157 and the continued one on158. Keep the lower indices and surrounding formula punctuation separate.'
    r.own_finding(id,p,'All S letters underlined','Plain S',r'\underline{S} at every printed occurrence',reason,'All S occurrences',witness=p+11)
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in ['both',layer]:old=old.replace(patch['old'],patch['new'])
        new,n=re.subn(r'(?<![A-Za-z\\])S(?![A-Za-z])',lambda m:r'\underline{S}',old);assert n==count,(p,n,count)
        new=new.replace(r'_\underline{S}',r'_{\underline{S}}')
        r.patch(p,layer,old,new,id,reason)

id='ASTRA-I-NOTE-156';reason='The complete main page and native witness print a raised star inside baseline parentheses at the call and note. The call precedes the final full stop, and the note itself ends after Tr_E|U with no additional stop.'
r.own_finding(id,156,'Raised-star author call and note','Automatic numerical footnote',r'\SGAAuthorFootnote{raisedstar}',reason,'Cup-product definition and lower note',kind='font',witness=167)
r.patch(156,'both',r'\footnote{même remarque',r'\SGAAuthorFootnote{raisedstar}{même remarque',id,reason)
for p in [156,157,158]:
    id=f'ASTRA-I-PROOFSTOP-{p:03d}';reason='The main and witness put the full stop beyond the lower rule beneath Preuve. Preserve the single inspected occurrence on this page.'
    r.own_finding(id,p,'Preuve ruled, stop outside',r'\emph{Preuve.}',r'\emph{Preuve}.',reason,'Proof heading',witness=p+11)
    r.patch(p,'both',r'\emph{Preuve.}',r'\emph{Preuve}.',id,reason)
for p,count in [(156,9),(157,6),(158,4)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='Apply the inspected upright word rules to the existing emphasis spans. The formulas, outside punctuation and references keep their independent typography, including the plain Parf operators on158.'
    r.own_finding(id,p,'Upright underlined prose groups',r'\emph spans',r'\uline word groups',reason,'All existing emphasis spans',witness=p+11)
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in ['both',layer]:old=old.replace(patch['old'],patch['new'])
        new,n=underline_words(old);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)

for p,b,e,w in [(156,'On peut interpréter u','Author note: même remarque que pour la définition de Tr_E|U',167),(157,'Two triangle diagrams, followed by the square','Par suite, l’homomorphisme',168),(158,'trace se prolonge de manière unique','On termine grâce à(8.1.1).',169),(159,'BIBLIOGRAPHIE','[MULT] Cartan,H. et Eilenberg,S. Homological Algebra,Princeton,1956.',None)]:
    r.page(p,b,e,'Complete prose, diagrams and all arrow labels, trace orders, tensor exponents, category rules, footnote and bibliography compared. The unprinted macro definitions after the159 bibliography remain unchanged. Statement labels and section titles follow NOTE_6’s allowed typesetting convention.',witness=w)
r.commit()
