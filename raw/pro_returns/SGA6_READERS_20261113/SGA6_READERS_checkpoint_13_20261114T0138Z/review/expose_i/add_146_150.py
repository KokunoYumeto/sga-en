#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='146_150'
observations={
1:('Page146 begins(les deux de gauche','The complete145/146 images put the whole parenthetical opening on146. The attached marker already agrees.','Boundary145/146',None),
2:('Definition6.11 prose groups underlined; rang and rg plain','On appelle, et l’on note and the following prose have rules. The defined word rang and its operator name rg remain plain.','Definition6.11 opening',None),
3:('Only Pour and on a underlined in6.12(a)','The category formulas and equality retain their independent typography. The printed S has its own rule.','Proposition6.12(a)',None),
4:('Soit, un morphisme de topos localement annelés and Pour underlined','The native witness leaves the later on a plain. Keep that local absence of a word rule.','Proposition6.12(b) opening',157),
5:('Double-stem L in the rank of Lu*(M)','The witness shows the doubled lower/vertical outline of the L; the L above the tensor sign in(a) is the plain typed superscript.','Proposition6.12(b) equality',157),
6:('Proposition6.12 final prose underlined','The native witness keeps the colon and final full stop outside, with separate short rules under the site S letters in the intervening formula.','Proposition6.12(b) final sentence',157),
8:('L’application i_X continues the same paragraph','The main page has ordinary line spacing and no paragraph indentation after the printed .). sequence. Preserve the attached running paragraph and all its punctuation.','Paragraph6.13 after the definition of L^n',None),
9:('Sous les hypothèses de and on a underlined','The reference6.13 remains plain between the two word rules.','Proposition6.14 opening',None),
10:('The explanatory parenthesis and En outre le rang have prose rules','The parentheses and final stop remain outside, while every constant-sheaf S has its independent rule.','Proposition6.14 explanatory sentence',None),
11:('définit un isomorphisme sur les faisceaux associés underlined','The final full stop stands beyond the word rule.','Proposition6.14 ending',None),
12:('Corollary6.15 statement underlined by word groups','The reference6.13 and the H^0 expression remain plain. The explicitly named final object S is plain, whereas the site letters and constant-sheaf indices have visible rules. The Parf operator has its own rule here.','Corollary6.15 statement',None),
13:('Soient underlined in7.1','The following E,F and derived-category formulas have no prose rule. Their S letters are plain.','Proposition7.1 opening',159),
14:('Proposition7.1(a) first prose assertion underlined','The word groups around F are ruled; the following Hom has its independent mathematical rule.','Proposition7.1(a) first sentence',159),
15:('Double-width R and underlined Hom; following Si underlined','The first R has closely inked stems in both scans. Its outline agrees with the separately resolved double stem in the same functor at the end of this paragraph. Retain that reconstruction and the independent Hom and Si rules.','Proposition7.1(a) first Hom expression',159),
16:('Proposition7.1(a) second prose assertion underlined','The pseudo-coherence, local tor-dimension and perfectness wording is ruled by word groups. The F∈D(S) formula remains independent, including its plain S.','Proposition7.1(a) second sentence',159),
17:('Second R has separated vertical stems; Hom underlined','The native witness resolves the two strokes before Hom at the paragraph ending.','Proposition7.1(a) final expression',159),
18:('Page149 begins b) Supposons que E','Page148 ends the formula RHom(E,F) with its stop. The item letter belongs to149 as in the attached marker.','Boundary148/149',160),
19:('Double-struck R and underlined Hom in the first formula','The native witness separates the R stems and the Hom rule. The surrounding part(b) prose is plain.','Proposition7.1(b), first Hom',160),
20:('R double-struck, Hom underlined, outer H plain','The cohomology symbol H^i has no rule here; its argument has the two observed functor glyph forms. All interval endpoints match.','Proposition7.1(b), vanishing formula',160),
21:('Thickened double-width R and ruled Hom inside tor.amp','The third R has closely overlapping ink in both scans; its broad left-stem outline matches the separately resolved R glyphs in the same paragraph. Preserve the attached double-struck reconstruction and explicitly record the filled stroke.','Proposition7.1(b), final parenthesis',160),
22:('Lemma7.1.1 prose word groups underlined','The i.e.(2.1) parenthesis opening and the surrounding formulas remain plain. The three S letters in the derived categories are plain as printed.','Lemma7.1.1 statement',None),
23:('Both Hom operators underlined; first has a raised dot; R double-struck','The main page shows a raised point immediately after the first Hom. The second Hom has an independent rule after the doubled R stem.','Lemma7.1.1 display',None),
24:('est un isomorphisme underlined; stop plain','The statement’s terminal point lies beyond the underline.','Lemma7.1.1 conclusion',None),
25:('H and both Ext operators underlined','The spectral sequence has E_2^{pq}, a raised dot on the parenthesized Ext complex, and a raised star on the abutment. The attached degrees and arrow agree.','Lemma7.1.1 spectral sequence',None),
26:('Both Ext operators underlined in the coproduct formula','The index is i_2−i_1=i, and the two arguments have degrees i_1 and i_2 respectively. The terminal comma agrees.','Lemma7.1.1 component formula',None),
27:('Final Ext operator underlined, raised dot retained','The vanishing is for q>0, followed by reference1.3.1. The next word isomorphismes still belongs to149.','Lemma7.1.1 proof end',None),
28:('Page150 starts with the E_2^{p0} display','The last word of149 is isomorphismes. The attached150 marker starts immediately before the display, as observed.','Boundary149/150',None),
29:('H and Hom underlined on the first display’s left side','The first Hom also has its printed raised dot; the spectral-sequence degree is p0.','Top display left side',None),
30:('Ext and H underlined; preceding isomorphism has a head','The tilde is above a rightward arrow with a visible head. Preserve xrightarrow{sim} at this position.','Top display middle',None),
31:('Top-display R has doubled stems and Hom has a rule','The printed final comma is retained after the nested parentheses.','Top display right side',None),
32:('Proposition7.1.2 opening word groups underlined','Soit, un morphisme de topos annelés, Soient, et and tels que l’on ait have prose rules. The two base-site S letters have their own rules; the following derived-category S letters are plain.','Proposition7.1.2 opening',None),
33:('R double-struck and Hom underlined in the boundedness hypothesis','The main page separates the R strokes before the ruled Hom; the target D^b(S) has a plain S.','Proposition7.1.2 first boundedness hypothesis',None),
34:('The joining et underlined','The word has its own short rule between the two boundedness hypotheses.','Proposition7.1.2 second hypothesis lead-in',None),
35:('L in Lf*(F) has a doubled stem','The ordinary f and its star remain separate from the doubled L.','Proposition7.1.2 second boundedness hypothesis',None),
36:('Il existe une flèche canonique fonctorielle underlined','The entire lead-in is ruled by word groups.','Proposition7.1.2 before display',None),
37:('All three L and both R glyphs double-struck; both Hom operators ruled','The source and target agree term by term, including the E,F order and final stop. Each derived-functor letter has its added stem.','Proposition7.1.2 displayed comparison',None),
38:('Celle-ci est un isomorphisme si and est parfait underlined','The E and final full stop remain outside the word rules.','Proposition7.1.2 end',None),
39:('The adjoint functors Lf* and Rf_* have doubled letters','The native witness resolves each vertical double stem in the prose.','Proof7.1.2 first line',161),
40:('Derived letters doubled and both Hom operators underlined','The native witness gives RHom(E,F) to Rf_*RHom(Lf*E,Lf*F), with a terminal full stop. The exact source/target order agrees.','Proof7.1.2 first display',161),
41:('Doubled R and L in the adjunction arrow','The witness gives F to Rf_*Lf*F, retaining the lower star of f_* and upper star of f*.','Proof7.1.2 inline adjunction',161),
42:('Duality display left side has doubled derived letters and ruled Hom','The native witness resolves Rf_*RHom(Lf*E,Lf*F) with the indicated argument order.','Proof7.1.2 duality display left side',161),
43:('Duality isomorphism has no arrowhead','The native witness has a tilde over a plain horizontal bar. This differs in observed strokes from the headed top-display isomorphism, and the attached simeq retains the actual sign.','Proof7.1.2 duality sign',161),
44:('Duality display right side has doubled R/L letters and ruled Hom','The nested target is RHom(E,Rf_*Lf*F), followed by the terminal point.','Proof7.1.2 duality display right side',161),
45:('Proposition7.2 prose word groups underlined','The SGA5 I1.6 citation remains plain, as do the displayed mathematical expressions.','Proposition7.2 opening',None),
46:('Both R letters doubled and both Hom operators underlined','The biduality arrow is E to RHom(RHom(E,F),F), in exactly that argument order.','Proposition7.2 display',None),
47:('Only Celle-ci est un isomorphisme si underlined','The rest of the final sentence has independently typed mathematical notation and a plain et.','Proposition7.2 end',None),
}
for n,(printed,reason,region,witness) in observations.items():r.finding(batch,n,printed,reason,region,witness=witness)

for p,counts in[(146,[(r'\mathcal C_1',r'\underline{C}_1',1),(r'\mathcal C_{1X}',r'\underline{C}_{1X}',1)]),(147,[(r'\mathcal C',r'\underline{C}',1)]),(148,[(r'\mathcal C',r'\underline{C}',4)])]:
    id=f'ASTRA-I-C-{p:03d}';reason='The printed category C letters on this page have individual lower rules. Apply only the rendered occurrences; the unprinted macro definitions at the end of146 remain byte-for-byte unchanged.'
    r.own_finding(id,p,'Underlined C at every rendered occurrence','Script C letters',r'\underline{C}',reason,'Category letter occurrences',kind='font')
    for old,new,count in counts:r.patch(p,'both',old,new,id,reason,count=count)
site_maps={146:(15,list(range(1,16))),147:(14,list(range(1,15))),148:(15,[1,2,3,4,7,8,9,10,12]),149:(4,[1]),150:(9,[1,2])}
for p,(count,positions) in site_maps.items():
    id=f'ASTRA-I-SITE-{p:03d}';reason='The exact rule map follows the scan. On148 the final object is explicitly named with a plain S, and the subsequent D(S) arguments stay plain through150; the base-site letters carry their own visible rules. Constant-sheaf indices on146–148 are ruled as printed. Macro definitions after the printed146 text are excluded from this glyph edit.'
    r.own_finding(id,p,'Exact site/object S rule map','Plain S commands',f'Underline positions{positions}; keep all other positions plain',reason,'Every rendered S occurrence',witness={146:157,148:159,149:160,150:161}.get(p))
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        cut=old.find('% Additional notation');cut=len(old) if cut<0 else cut
        printed=old[:cut];suffix=old[cut:]
        matches=list(re.finditer(r'(?<![A-Za-z\\])S(?![A-Za-z])',printed));assert len(matches)==count,(p,len(matches),count)
        new=printed
        for i,m in reversed(list(enumerate(matches,1))):
            if i in positions:new=new[:m.start()]+r'\underline{S}'+new[m.end():]
        new=new.replace(r'_\underline{S}',r'_{\underline{S}}')+suffix
        r.patch(p,layer,old,new,id,reason)

id='ASTRA-I-PARF-148';reason='The Corollary6.15 statement has a visible word rule under Parf inside the mathematical expression; the earlier Parf in the proof has none. Preserve that exact occurrence difference.'
r.own_finding(id,148,'Parf underlined only in Corollary6.15','Both occurrences plain',r'\underline{\Parf} at the statement occurrence',reason,'Corollary6.15')
r.patch(148,'both',r'fonctions additives de \(\Parf(\underline{S})\)',r'fonctions additives de \(\underline{\Parf}(\underline{S})\)',id,reason)

for p,labels in[(146,['a)','b)']),(147,['6.13.']),(148,['7.0.','a)']),(149,['b)'])]:
    id=f'ASTRA-I-ITEMS-{p:03d}';reason='The inspected item and paragraph labels are in the plain running type weight. Remove the added bold at these exact labels.'
    r.own_finding(id,p,'Plain item/paragraph labels','Bold labels','Plain labels',reason,'Selected labels',kind='font')
    for label in labels:r.patch(p,'both',r'\textbf{'+label+'}',label,id,reason)
for p,count in[(146,1),(147,1),(148,1),(149,2),(150,1)]:
    id=f'ASTRA-I-PROOFSTOP-{p:03d}';reason='The word Preuve is underlined and its full stop lies beyond the rule. Preserve the exact six inspected headings on these pages.'
    r.own_finding(id,p,'Preuve ruled, following stop plain',r'\emph{Preuve.}',r'\emph{Preuve}.',reason,'Proof headings',witness={146:157,150:161}.get(p))
    r.patch(p,'both',r'\emph{Preuve.}',r'\emph{Preuve}.',id,reason,count=count)
r.finding(batch,7,'Six proof-heading stops outside the rules','The complete five main pages and native witness details show one heading each on146/147/148/150 and two on149. Apply only these inspected local occurrences.','Six proof headings on146–150',verdict='not applied and now applied',change='Place the six stops outside the prose rules.',witness=161)
for p,count in[(146,10),(147,6),(148,9),(149,7),(150,9)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The observed statement, definition and proof word groups have upright rules. The plain defined rang and rg on146, plain on a in6.12(b), and the wholly plain assertion7.1(b) retain their existing states; formulas preserve their independently adjudicated notation.'
    r.own_finding(id,p,'Upright underlined prose word groups',r'\emph spans',r'\uline groups',reason,'Every existing emphasis span',witness={146:157,148:159,149:160,150:161}.get(p))
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        new,n=underline_words(old);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)
for p,b,e,w in[(146,'(les deux de gauche étant','compatible avec les images inverses.',157),(147,'Preuve. Il suffit de montrer','définit un isomorphisme sur les faisceaux associés.',None),(148,'Preuve. La première assertion','il en est de même de RHom(E,F).',159),(149,'b) Supposons que E','On en déduit des isomorphismes',160),(150,'E_2^{p0}=H^p(Hom^bullet(E,F))','E∈ob D(S)_parf et F=A.',161)]:
    r.page(p,b,e,'Complete prose, rank formulas, every degree interval, all primes and stars, raised complex dots, spectral-sequence degrees and coproduct index, Hom/Ext rules, derived-functor letter strokes, every arrow and isomorphism sign, punctuation and page boundaries compared.',witness=w)
r.commit()
