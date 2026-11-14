#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT
r=Review()
batch='086_090'
obs={
1:('C_{0X}, with adjacent zero and X','The comma after the formula separates clauses; there is no comma between its indices.','First paragraph, avec E et F'),
2:('C_{0U}, with adjacent zero and U','The formula after f*Ker(u) has the two adjacent subscripts.','First paragraph, local kernel'),
3:('E^1 → ... → E^n, baseline dots','The three dots sit on the typed baseline between the arrows.','Long exact sequence (*)'),
4:('E^i∈ob C_{0X}','The subscripts after the long exact sequence contain no interposed comma.','Line immediately after (*)'),
5:('F∈ob C_{0X}','The subscripts in the local lifting definition contain no interposed comma.','Definition of local relevability'),
8:('F∈ob C_{0X},','The visible following comma is outside the category subscript.','First paragraph, avec F'),
9:("F′∈ob C_{0U}",'The two category subscripts are adjacent.','First paragraph, local epimorphism'),
10:('Cette condition begins a new paragraph','A new indented paragraph is visible. The attached paragraph break is retained as typesetting; it does not change content.','Second paragraph'),
11:('F_U followed by a comma','The comma is clearly visible to the right of the bottom right cell, like the comma after F above.','Second diagram, bottom right'),
12:('a), plain','The item letter is plain upright type, without a rule.','1.3 first example'),
13:('b), plain','The item letter is plain upright type, without a rule.','Second paragraph'),
14:('c), plain','The item letter is plain upright type, without a rule.','Third paragraph'),
16:('d), plain','The item letter is plain upright type, without a rule.','First example paragraph'),
17:('Lemme 1.3.1,','The witness shows a descending tail on the punctuation after the number. Retain the comma diplomatically; the corrected heading uses the full stop separating the label from its statement.','Lemma label'),
18:('Module, Conditions équivalentes','The comma is visible in both scans. Conditions starts the next sentence after the completed object declaration Soit P un O_S-Module. Correct the sentence stop in current.','Opening sentence of Lemma1.3.1'),
19:('Hom alone has its own underline','The short rule directly under Hom is separate from the statement rules and stops before the argument parentheses. It denotes the sheaf Hom used in the local splitting characterization.','Lemma1.3.1(i)'),
20:('Hom(P,.), baseline point','The argument placeholder is a typed point on the baseline in the witness.','Lemma1.3.1(i)'),
21:('Proposition1.4.1 word groups are underlined','The opening proposition has rules under its prose, separately from the symbols with their own rules. The recorded statement span is correct; local patches preserve upright word-group underlining.','Proposition1.4.1 opening'),
22:('Page89 ends on suppose que H^n(G) est','The last printed line ends at est. The words de C_0-type fini begin90. The supplied split and marker placement are correct.','Bottom text line'),
23:('plain C in C une S-catégorie','The witness has no rule under this C. It names the category whose fiber is subsequently denoted by underlined C_S; the current correction uses the same underlined category symbol consistently.','Proposition1.4.1 first line'),
24:('plain C after strictement pleine de','The witness has no rule under this C. It is the same ambient category in the inclusion C_0⊂C introduced by the statement; current restores the underlined symbol used for C_0 and the fiber C_S.','Proposition1.4.1 second line'),
25:('plain C after quasi-relevable dans','The witness has no rule under this C. It is the same category in the local lifting definition1.2 and in the fiber C_S; current restores its underline.','Proposition1.4.1 third line'),
26:('Page90 begins de C_0-type fini (1.2).','The first printed line and the last line of89 establish this page break exactly. The supplied marker is now correctly placed.','Page90 first line'),
27:('Proposition prose underlined through raffinement de S','The two opening lines are underlined by word groups. The following (P) paragraph has plain prose. Retain exactly this statement extent.','First two lines'),
28:('underlined S_{/S}, with lowered /S','The site letter has its own short rule and the slash and object S sit below the main baseline.','First line, X∈ob S_{/S}'),
29:('M de C_{0X}','The zero and X are adjacent subscripts without a comma.','Property(P), first line'),
30:('Démonstration followed by a full stop outside its rule','The visible rule stops before the point. The attached source already represents this; NOTE_6 accepts either punctuation placement as typesetting. Retain it without treating it as a mathematical correction.','Last paragraph heading'),
}
for n,(printed,reason,region) in obs.items():
    r.finding(batch,n,printed,reason,region,
        verdict='amended' if n in[10,30] else 'confirmed',witness=100 if n in[17,18,19,20,21,22,23,24,25] else None)
id=r.finding(batch,6,'u beside the diagonal H_U→E_U; U above E_U→F_U',
    'Both scans place the two letters on these separate arrows. The horizontal morphism is f*(u):f*E→f*F, hence u_U:E_U→F_U. The diagonal is the chosen local lift of H_U→F_U and has no previously assigned name. The square on87 explicitly labels the same horizontal restriction u_U. Keep the separated labels diplomatically; write u_U on the horizontal arrow and leave the lift unnamed in current.',
    'Second commutative triangle; main216dpi and witness300dpi',verdict='not applied and now applied',
    change='Current: remove diagonal label u and replace horizontal label U by u_U.',witness=97)
r.patch(86,'current',r"""\arrow[dl,"u"']""",r'\arrow[dl]',id,'The diagonal is the unnamed chosen lift.')
r.patch(86,'current',r'E_U \arrow[r,"U"]',r'E_U \arrow[r,"u_U"]',id,'The horizontal arrow is the pullback f*(u)=u_U.')
id=r.finding(batch,15,'(SGA4 V3.11) k un corps',
    'The scan has no separator before k. The sentence enumerates the four named data G, the topos S, k and the category C; insert the missing comma separating the S clause from the k clause in current.',
    'Example c), first line',verdict='not applied and now applied',change='Current adds a comma after the closing reference parenthesis.')
r.patch(88,'current',r'(SGA 4 V 3.11) \(k\)',r'(SGA 4 V 3.11), \(k\)',id,'Restore the missing enumeration separator.')
r.patch(89,'current',r'-Module, Conditions équivalentes',r'-Module. Conditions équivalentes','check/findings/findings_086_090.json#18','Separate the completed object declaration from the next sentence.')
id=r.finding(batch,7,'The site letter is underlined; the space/object S retains its plain form',
    'Direct comparison of86–90 distinguishes the underlined site S from the plain space S in88 and plain object S in89–90. The local mapping records every occurrence, including the site S used as a subscript to O in89. Three omitted site underlines in the opening proposition on89 are separately retained diplomatically and corrected with an explicit source.',
    'Every S occurrence on86–90',verdict='not applied and now applied',
    change='Explicit occurrence maps:86 positions1–5;87 positions1–4;88 positions3,5,6,7,9–15;89 positions1–9,14;90 position1. Current additionally restores89 positions10–12.',witness=100)

# Patches are deliberately local and tied to the complete image comparison.
for p,cc in[(86,18),(87,13),(88,21),(89,10),(90,5)]:
    reason='Every category C represented by this command on the inspected page is a plain capital with a single rule; its primes and indices sit outside that rule.'
    r.own_finding(f'ASTRA-I-C-{p:03d}',p,'Underlined typed C',r'\mathcal C',r'\underline{C}',reason,'All category C occurrences represented by mathcal C')
    for layer in['diplomatic','current']:
        count=cc+3 if p==89 and layer=='current' else cc
        r.patch(p,layer,r'\mathcal C',r'\underline{C}',f'ASTRA-I-C-{p:03d}',reason,count)

for p,count in[(88,4),(89,6)]:
    id=f'ASTRA-I-O-{p:03d}';reason='Every structure-sheaf O on this inspected page is typed upright with a short individual underline.'
    r.own_finding(id,p,'Underlined plain O',r'\mathcal O',r'\underline{O}',reason,'Structure sheaves, including the89 footnote')
    r.patch(p,'both',r'\mathcal O',r'\underline{O}',id,reason,count)

# Apply S by its observed ordinal on each complete page, never globally by name.
smap={86:set(range(1,6)),87:set(range(1,5)),88:{3,5,6,7,9,10,11,12,13,14,15},89:set(range(1,10))|{14},90:{1}}
for p in range(86,91):
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        # Reproduce precisely the preceding explicit edits to obtain the anchor.
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        ordinal=[0]
        def sub(m):
            ordinal[0]+=1
            if ordinal[0] not in smap[p]:return m.group(0)
            return r'{\underline{S}}' if old[m.start()-1:m.start()]=='_' else r'\underline{S}'
        new=re.sub(r'(?<![A-Za-z\\])S(?![A-Za-z])',sub,old)
        r.patch(p,layer,old,new,'check/findings/findings_086_090.json#7','Use the explicit occurrence map stated in the scan decision.')

id='ASTRA-I-S-089-PROP';reason='The witness prints plain S three times in the opening data of Proposition1.4.1. These denote the site and the base of its fibered category; the same site reappears as the underlined S in S∈ob S. Current restores the underlined site notation, retaining the plain object S and the printed readings diplomatically.'
r.own_finding(id,89,'Plain S in Soient S un site, S-catégorie, sous-S-catégorie','Plain S in both attached layers','Current underlines exactly these three site occurrences.',reason,'Proposition1.4.1 first two lines',kind='misprint_in_print',witness=100)
r.patch(89,'current',r'\emph{Soient \(S\) un site,',r'\emph{Soient \(\underline{S}\) un site,',id,reason)
r.patch(89,'current',r'\(\underline{C}\) une \(S\)-catégorie',r'\(\underline{C}\) une \(\underline{S}\)-catégorie',id,reason)
r.patch(89,'current',r'\(\underline{C}_0\) une sous-\(S\)-catégorie',r'\(\underline{C}_0\) une sous-\(\underline{S}\)-catégorie',id,reason)

for p,count in[(86,3),(87,1),(90,3)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The recorded word groups are upright and underlined. Their existing emphasis spans match the scan; use underlining for these observed spans.'
    r.own_finding(id,p,'Underlined upright word groups',r'\emph{...}',r'\uline{...}',reason,'Definitions and emphasized words')
    r.patch(p,'both',r'\emph{',r'\uline{',id,reason,count)

old90=r'''\uline{de \(\underline{C}_0\)-%
type fini (1.2). Alors l'ensemble des \(X\in\Ob \underline{S}_{/S}\) vérifiant la propriété \((P)\) ci-dessous est un raffinement de \(S\)}.'''
new90=r'''\uline{de} \(\underline{C}_0\)-%
\uline{type fini (1.2). Alors l'ensemble des} \(X\in\Ob \underline{S}_{/S}\) \uline{vérifiant la propriété} \((P)\) \uline{ci-dessous est un raffinement de} \(S\).'''
r.patch(90,'both',old90,new90,'ASTRA-I-TERMS-090','The first statement rules skip its formulas and the final object S. Preserve the separate site underline; the later emphasis en degré n seulement remains continuous as printed.')

# In89 the statement rules skip formulas. Keep these mathematical symbols outside
# the word-group wrappers so a missing symbol underline stays visible diplomatically.
id='ASTRA-I-TERMS-089';reason='Both scans underline the prose of Lemma1.3.1 and Proposition1.4.1 by word groups, skipping the formulas; the independent rules under category, site and sheaf symbols must remain separately visible.'
r.own_finding(id,89,'Upright underlined prose, with formulas outside the prose rules',r'\emph blocks',r'\uline word groups separated at inline formulas',reason,'Defined type fini and both statements',witness=100)
for layer in['diplomatic','current']:
    old=(ROOT/f'build/page_packets/89/{layer}.tex').read_text()
    for patch in r.patches:
        if patch['page']==89 and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
    pos=0;pieces=[];count=0
    while True:
        start=old.find(r'\emph{',pos)
        if start<0:pieces.append(old[pos:]);break
        pieces.append(old[pos:start]);depth=1;j=start+6
        while depth:
            if old[j]=='{' and old[j-1]!='\\':depth+=1
            if old[j]=='}' and old[j-1]!='\\':depth-=1
            j+=1
        content=old[start+6:j-1]
        spans=re.split(r'(\\\(.*?\\\))',content,flags=re.S)
        for span in spans:
            if not span:continue
            if span.startswith(r'\('):pieces.append(span)
            elif span.strip():
                lead=span[:len(span)-len(span.lstrip())];tail=span[len(span.rstrip()):]
                pieces.append(lead+r'\uline{'+span.strip()+'}'+tail)
            else:pieces.append(span)
        count+=1;pos=j
    assert count==6
    r.patch(89,layer,old,''.join(pieces),id,reason)

id='ASTRA-I-Z-089';reason='The witness shows a single typed Z in n∈Z: one diagonal and two horizontal strokes. Preserve that printed integer-domain symbol in both layers, retaining its meaning as the degree n of the complexes.'
r.own_finding(id,89,'plain Z',r'\mathbb Z','Z',reason,'Proposition1.4.1 last line',kind='font',witness=100)
r.patch(89,'both',r'n\in\mathbb Z',r'n\in Z',id,reason)
id='ASTRA-I-NOTE-089';reason='The call and the complete note use a parenthesized asterisk. Preserve this explicit author label instead of assigning the running numerical counter.'
r.own_finding(id,89,'(*)','Unlabeled automatic footnote',r'\SGAAuthorFootnote{*}',reason,'Example d) and bottom footnote',kind='footnote')
r.patch(89,'both',r'\footnote{\(\underline{O}',r'\SGAAuthorFootnote{*}{\(\underline{O}',id,reason)
id='ASTRA-I-DOTS-090';reason='All four continuation ellipses of the complex diagram sit on the baseline of the adjacent typed E or F, as the baseline dots in86.'
r.own_finding(id,90,'Four baseline ellipses',r'\cdots',r'\ldots',reason,'Both ends of the two-row complex diagram',kind='symbol')
r.patch(90,'both',r'\cdots',r'\ldots',id,reason,4)
for p,b,e,w in[(86,'Nous dirons que C_0 est localement stable','soit un raffinement de X.',97),(87,'Nous dirons que C_0 est localement quasi-relevable','de type fini au',None),(88,'sens ordinaire.','opère continûment.',None),(89,'En fait, les exemples b) et c)','on suppose que H^n(G) est',100),(90,'de C_0-type fini (1.2).','on vérifie',None)]:
    r.page(p,b,e,'Complete body, diagrams and any author footnote compared; heading typography follows NOTE_6.',witness=w)
r.commit()
