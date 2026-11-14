#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='136_140'
observations={
1:('Lemma5.8.3 opening prose word groups underlined','The rules cover Soit, un, Module à gauche and Conditions équivalentes. The coefficient A, hyphen, stop and colon retain their observed plain forms.','Lemma5.8.3 opening',None),
2:('Both item predicates underlined','The mathematical E and the final semicolon/full stop stand outside the rules.','Lemma5.8.3(i)/(ii)',None),
3:('Hom_A(E,.) has one underline','The native witness separates the rule from the Hom letters and lowered coefficient A.','Proof5.8.3 first Hom',147),
4:('The argument placeholder is a baseline point','The witness puts the point at the same baseline as the adjacent punctuation. The attached literal point agrees.','First Hom argument',147),
5:('Both displayed Hom operators underlined','The formula runs Hom_A(E,F) to Hom_A(E,F-double-prime) to0; every coefficient, prime and arrow agrees.','Proof5.8.3 first display',147),
6:('Internal Hom into I underlined','The native witness shows the rule; its coefficient Z is adjudicated separately in finding8.','Proof5.8.3 second inline Hom',147),
7:('Second argument placeholder is a baseline point','The point preceding the comma is level with the lower punctuation, as in the preceding Hom.','Internal Hom(.,I)',147),
9:('Both upper-row Hom operators underlined','The main and witness show plain final-object S in the constant-sheaf coefficient; the two tensor subscripts are A.','Commutative diagram, upper row',147),
10:('All four lower-row Hom operators underlined','The composite Hom expressions, both vertical downward arrows and the final stop agree with the scan.','Commutative diagram, lower row',None),
11:('Only Preuve de underlined','The reference(5.8) and the full stop remain plain.','Last paragraph opening',None),
12:('Page137 begins flèche de troncature','The last words of136 are en degré<m, la; the attached137 marker already stands before flèche de.','Boundary136/137',None),
13:('The upper truncation row begins with an arrow','There are no leading dots. All three displayed degree labels and the outgoing arrow agree.','Truncation diagram, upper row',None),
14:('The lower truncation row begins with an arrow','The first displayed term is0; there are no leading dots. The quotient E^m/B^m and the last term E^{m+1} agree.','Truncation diagram, lower row',None),
15:('Upper-row trailing dots lie on the baseline','The attached ldots reproduces the observed row ending.','Truncation diagram, upper-row ending',None),
16:('Lower-row trailing dots lie on the baseline','The attached ldots reproduces the observed row ending.','Truncation diagram, lower-row ending',None),
17:('Comma to the right of the distinguished triangle','The comma is level with the bottom E-double-prime to E-prime edge. The +1 label is on the descending edge.','Triangle in proof5.8',None),
18:('parf.amp(E) with a','The print reads parf.amp. Both attached macro definitions already expand to the printed parf spelling, and this occurrence is explicitly written with operatorname.','Proof5.8 conclusion',None),
19:('The defined parf index is underlined','The independent rule below parf is clearly visible; the S occurrence map is applied separately.','Remark5.8.4(b), first category',None),
20:('The parf index underlined in the tensor functor','The following coh indices remain plain as printed. Both attached forms retain the parf rule.','Remark5.8.4(b), final display',None),
22:('Corollary5.9 prose word groups underlined','The MULT and EGA references stay plain; all category, ring and cohomological expressions have their independent mathematical styling.','Corollary5.9 before display',None),
23:('The displayed conjunction et underlined','Only the word et has its text rule between the two formulas.','Corollary5.9(i) ending',None),
24:('The parf index underlined; torf and coh plain','The index has a separate visible rule in(ii), while the other index spellings agree without rules.','Corollary5.9(ii)',None),
25:('The Autrement dit paraphrase underlined by word groups','The final full stop remains outside the prose rule; all formulas agree with the source.','Corollary5.9 concluding statement',None),
27:('Corollaire5.10 without a stop after the number','The complete main page has no terminal stop at this heading. Keep the attached reading in both layers.','Corollary5.10 heading',None),
28:('Corollary5.10 prose word groups underlined','The reference SGA4 IV6.4.1 stays plain. The site localization has /X in the lower index, and the final display keeps its plain parf index.','Corollary5.10 statement',None),
29:('Definition6.1 word groups underlined','The native witness shows the defined phrase fonction additive de C dans F plain. Mathematical letters remain independently typed. The return arrow of the triangle is dashed and has no +1 label.','Definition6.1 before triangle',151),
30:('Only on a underlined after the triangle','The additive equality and final full stop remain plain.','Definition6.1 after triangle',151),
31:('The final definition sentence has prose rules','The mathematical C,F and Add(C,F) retain their independent plain typed forms.','Definition6.1 last sentence',151),
33:('Page140 ends noté Add(C,F).;141 begins6.2.','The complete140 image and the top region of141 place the paragraph label at the next page opening. The attached boundary already agrees.','Boundary140/141',None),
}
for n,(printed,reason,region,witness) in observations.items():r.finding(batch,n,printed,reason,region,witness=witness)

reason=('The native witness has a double-struck Z without S. This internal-Hom notation already gives the required sheaf: for each site object U, an additive sheaf map M|U to I|U commutes with integer repeated addition, and hence with locally constant integer sections by gluing. Conversely a Z_S-linear map is additive. The identity on maps and its inverse identify internal Hom_Z(M,I) with internal Hom_ZS(M,I), compatibly with restriction. Preserve the printed abbreviation in both layers; no mathematical correction is warranted.')
r.finding(batch,8,'Internal Hom_Z(.,I), without an S index',reason,'Proof5.8.3, exactness tested by internal Hom into I',verdict='amended',change='Keep the diplomatic Z; revert the current addition of S.',witness=147)
for row in r.decisions:
    if row.get('related_finding')==f'check/findings/findings_{batch}.json#8':
        if row['type']=='misprint':row.update(verdict='reverted',is_misprint=False,change='Not a misprint: keep printed Hom_Z(.,I) in both layers.')
        elif row['type']=='fixlog':row.update(verdict='confirmed',change='The diplomatic removal of S correctly restores the printed abbreviation.')
id='ASTRA-I-HOMZ-136'
r.own_finding(id,136,'Internal Hom_Z(.,I)',r'\underline{\Hom}_{\mathbb Z_S}(.,I)',r'\underline{\Hom}_{\mathbb Z}(.,I) in current',reason,'Proof5.8.3, internal Hom into I',kind='formula',verdict='reverted',witness=147)
r.patch(136,'current',r'\underline{\Hom}_{\mathbb Z_S}(.,I)',r'\underline{\Hom}_{\mathbb Z}(.,I)',id,reason)

id='ASTRA-I-REF-136';reason=('Both scans print(3.17.1). Formula5.8.2.1 on135 specializes with B=Z_S and G=I to the vertical map Hom_ZS(F,I) tensor_A E to Hom_ZS(Hom_A(E,F),I), sending h tensor e to the map t ↦ h(t(e)); replacing F by F-double-prime gives the other vertical map. These are precisely the two displayed arrows, and the next sentence explicitly invokes5.8.2 for their invertibility. Keep the printed reference diplomatically and correct it to(5.8.2.1) in current.')
r.own_finding(id,136,'Reference(3.17.1)','(3.17.1)','(5.8.2.1) in current',reason,'Before the commutative Hom diagram',kind='misprint_in_print',witness=147)
r.own[-1]['is_misprint']=True
r.patch(136,'current','flèches canoniques de (3.17.1)','flèches canoniques de (5.8.2.1)',id,reason)

for p,positions,count in [(137,list(range(1,10)),9),(138,list(range(1,8))+[10,11,12,13],13),(139,list(range(1,6)),5)]:
    id=f'ASTRA-I-SITE-{p:03d}';reason='The exact occurrence map follows the visible S rules. On138 the second E∈D^b(_AS) and the explicitly named final object S are plain; the surrounding site letters carry rules. The native witness confirms these adjacent forms in the proof of5.9.'
    r.own_finding(id,p,'Site letters S underlined at selected positions','Plain S commands',f'Underline positions{positions}',reason,'Every S occurrence',witness=149 if p==138 else None)
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        matches=list(re.finditer(r'(?<![A-Za-z\\])S(?![A-Za-z])',old));assert len(matches)==count,(p,len(matches),count)
        new=old
        for i,m in reversed(list(enumerate(matches,1))):
            if i in positions:new=new[:m.start()]+r'\underline{S}'+new[m.end():]
        new=new.replace(r'\times_\underline{S}',r'\times_{\underline{S}}')
        r.patch(p,layer,old,new,id,reason)
r.finding(batch,21,'Exact S rule maps on137–139','The complete pages and native witness of138 fix each occurrence individually, including the adjacent plain final object. No rule is inferred solely from a category name.','Site and object notation on137–139',verdict='not applied and now applied',change='Apply the three occurrence maps.',witness=149)

for p,labels in[(137,['a)','b)']),(140,['6.0.'])]:
    id=f'ASTRA-I-ITEMS-{p:03d}';reason='The main page prints these item or paragraph labels in the running type weight. Remove the added bold at the exact labels.'
    r.own_finding(id,p,'Plain labels','Added bold labels','Plain labels',reason,'Selected item and paragraph labels',kind='font')
    for label in labels:r.patch(p,'both',r'\textbf{'+label+'}',label,id,reason)

for p,count in[(138,1),(139,2)]:
    id=f'ASTRA-I-PROOFSTOP-{p:03d}';reason='The word Preuve has a rule; its following full stop stands just beyond that rule. Apply the exact inspected occurrences only.'
    r.own_finding(id,p,'Preuve underlined; following stop plain',r'\emph{Preuve.}',r'\emph{Preuve}.',reason,'Proof headings',witness=149 if p==138 else None)
    r.patch(p,'both',r'\emph{Preuve.}',r'\emph{Preuve}.',id,reason,count=count)
r.finding(batch,26,'Proof-heading stops outside the underline','The native witness of138 and both proof headings on the complete139 page show the word rule ending before the full stop. The three exact local occurrences are repaired.','Three proof headings on138–139',verdict='not applied and now applied',change='Move the three stops outside the emphasis before applying upright word rules.',witness=149)

id='ASTRA-I-C-140';reason='All six category letters C in Definition6.1 are plain typed letters. The native witness explicitly shows Soient C, ob(C), and Add(C,F) without an added lower rule or script form. The parenthesized Ob(C) arguments preserve their TeX command delimiters.'
r.own_finding(id,140,'Six plain typed C letters',r'\mathcal C','C',reason,'Definition6.1 and its final sentence',kind='font',witness=151)
r.patch(140,'both',r'\mathcal C','C',id,reason,count=6)
r.finding(batch,32,'Plain typed C at all six positions',reason,'Definition6.1 category letter',verdict='not applied and now applied',change='Replace exactly six script C forms with plain C in both layers.',witness=151)
id='ASTRA-I-O-140';reason='The three structure-sheaf letters O are typed with separate lower rules: the opening O_X, O_U in(ii), and O_X in(iii). Reproduce each observed glyph and retain its subscript.'
r.own_finding(id,140,'Three underlined typed O letters',r'\mathcal O',r'\underline{O}',reason,'Paragraph6.0 structure-sheaf letters',kind='font')
r.patch(140,'both',r'\mathcal O',r'\underline{O}',id,reason,count=3)

for p,count in[(136,5),(138,8),(139,4),(140,5)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The observed statement, proof and term word groups have upright rules. Mathematical expressions keep their independently observed fonts, and the defined fonction additive phrase on140 remains plain. Exact proof stops are handled before this transport.'
    r.own_finding(id,p,'Upright underlined word groups',r'\emph spans',r'\uline groups with explicit plain exceptions',reason,'Every existing emphasis span',witness={136:147,138:149,140:151}.get(p))
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        plain={136:['.','-'],138:['«','»'],139:[],140:[]}[p]
        new,n=underline_words(old,plain);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)

for p,b,e,w in[(136,'Voici maintenant un cas particulier','acyclique en degré<m, la',147),(137,'flèche de troncature','D^b(S)_coh. in the tensor-product display',None),(138,'Cette formule est le point de départ','D^b(_AX)_coh=D^b(_AX)_parf.',149),(139,'Autrement dit, pour que','espace analytique complexe lisse sur C.',None),(140,'6. Rang d’un complexe parfait','noté Add(C,F).',151)]:
    r.page(p,b,e,'Complete prose, every formula and coefficient, diagram vertices/arrows, primes and degree bounds, punctuation, definitions, reference digits and page boundaries compared. The native witness settles the internal-Hom coefficient and the locally plain category/object letters.',witness=w)
r.commit()
