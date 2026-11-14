#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='121_125'
observations={
1:('Qis/F underlined inside parentheses','The first two lines continue Scholium4.4, and the rule extends through the slash and F while leaving the parentheses plain.','Top of121'),
2:('The /X is a lower index on the site S','The base of the Hom sheaf is printed with lowered /X, exactly as the attached repaired source. The site letter rule is restored separately.','Notation4.5'),
3:('Corollary4.6 prose word groups underlined','The rules cover Soient, étant strictement parfait and La flèche canonique. The displayed Hom operators have their own rules.','Corollary4.6 before display'),
4:('est un isomorphisme underlined, stop outside','The final stop is separated from the end of the rule.','Corollary4.6 conclusion'),
5:('The two Hom operators in the proof have no underline','The main and witness both leave these Hom group operators plain. Their category C subscripts are independently underlined. The corollary above compares the associated sheaves, whose Hom rules are printed explicitly.','Proof4.6 display'),
6:('Definition4.7 opening prose underlined; amplitude term plain','The definition’s new phrase amplitude C_0-parfaite contenue dans l’intervalle is outside the word rules, which resume at et nous écrirons.','Definition4.7 opening'),
7:('et nous écrirons underlined','The rule precedes the amplitude notation display.','Definition4.7 before display'),
8:('Lowercase parf in the amplitude notation','The displayed abbreviation is parf, with a small p. It does not use the capitalized category name Parf. The source now reproduces those exact letter cases.','Definition4.7 amplitude display'),
9:('Final statement line underlined by word groups','Page121 ends immediately after quasi-isomorphisme. The formula naming the arrow begins122.','Page121 final line'),
10:('de underlined on122','The short word rule appears between the arrow F-prime→F and C(C_X) at the top of122. Its nominal source page121 preceded the repaired boundary.','Page122 first line'),
12:('Page122 begins F-prime→F','The arrow and its category expression begin122;121 ends with quasi-isomorphisme. The attached marker is in the observed position.','Boundary121/122'),
13:('Definition4.7 continuation word groups underlined','The strictness, interval condition and refinement conclusion agree with the image. The reference(2.1) and final object S remain plain.','Top of122'),
14:('Explanatory parenthesis underlined by word groups; new amplitude term plain','The numbered reference(4.3) is unruled, while its surrounding explanation has word rules. The new term amplitude C_0-parfaite finie stays plain.','Definition4.7 middle'),
15:('Existence-of-integers word groups underlined','The a and b themselves remain outside the word rules.','Definition4.7 finite amplitude'),
16:('Lowercase parf in C_0-parf-amp','The small-p abbreviation matches the display on121.','Definition4.7 finite-amplitude notation'),
17:('The defined C_0-parfait term is plain','The surrounding Nous dirons que, est, si and finite-amplitude predicate have word rules; the note call remains outside. The category C has its independent short underline.','Definition4.7 last definition'),
20:('Lowercase parf in the derived-category subscript','The index uses small letters; the next expression gives the category name Parf with a capital P. Both observed forms are preserved.','Notation4.9 first formula'),
21:('Lowercase parf as the subscript of D(_AS)','The two subsequent category names Parf(_AS) and Parf(S) retain their printed capital P.','Notation4.9 last sentence'),
22:('Proposition4.10 without terminal full stop','The main image leaves a space after10 before La catégorie. Retain the diplomatic absence and the existing corrected stop.','Page123 label'),
23:('Opening statement word groups underlined, including Parf','The prose rule continues under the first Parf operator, while its arguments have independent C rules. Restore the operator rule explicitly. The reference(1.1.4) remains plain.','Proposition4.10 opening'),
24:('S-equivalence assertion underlined by word groups','The preceding resp. triangle-functor line and the Giraud reference are plain. The source’s statement spans are rendered with those exceptions.','Proposition4.10 before items'),
25:('pour tout and et tous underlined','The membership X∈obS lies between the word rules. The missing S underline at this one occurrence is separately recorded from the witness.','Proposition4.10(i) opening'),
26:('la flèche canonique underlined','The phrase ends immediately before the first Hom display.','Proposition4.10(i) before display'),
27:('C_{0X} with adjacent lower indices','There is no comma between the0 and X.','Proposition4.10(i), first category'),
28:('C_{0X} with adjacent lower indices in the parenthetical category','The second occurrence also has no internal comma.','Proposition4.10(i), triangle category'),
29:('Both Hom operators underlined','The two sheaf-Hom operators have independent rules, with category indices and arguments outside them.','Proposition4.10(i), main display'),
30:('resp. and both Hom operators underlined','The rule under resp. and the two Hom rules are separately visible. Inline versus display placement is layout and does not create a textual variant.','Proposition4.10(i), parenthetical Hom formula'),
31:('est un isomorphisme and et underlined','The comma separates the two printed word rules.','Proposition4.10(i) ending'),
32:('The item(ii) prose is underlined with its first Parf operator','The first parenthetical resp. after Parf(C,C_0) is plain; the later resp. after D(C) is underlined. Preserve those local exceptions, including the separately observed missing closing parenthesis.','Proposition4.10(ii) first clause'),
33:('à un objet de and final resp. underlined','The category expressions remain independently typeset. The missing final resp. closing parenthesis is a separate printed error.','Proposition4.10(ii) second clause'),
34:('One closing parenthesis missing after Tr(D(C))','The witness gives three opens but only two closes in this resp. parenthesis. The corrected layer supplies the sole missing outside closer; the diplomatic layer keeps the printed omission.','Proposition4.10(ii), middle resp. clause'),
35:('One closing parenthesis missing at the end of Tr(K^b(C_0))','The witness confirms the second independent unclosed resp. clause. Retain the existing current closer and diplomatic omission.','Proposition4.10(ii), final resp. clause'),
36:('Page124 begins est parfait','Page123 ends alors G. The first word124 is est, followed by parfait and the localization argument. The attached marker is correct.','Boundary123/124'),
38:('C_{0X} has no internal comma','The single membership category in this paragraph has adjacent0 and X subscripts.','Page124, two distinguished triangles'),
39:('Both Hom operators in(**) underlined','The display is the same sheaf map for triangle objects that appeared in4.10(i). Both independent Hom rules are visible.','Page124 display(**)'),
40:('Lowercase parf in the first subscript of Remark4.10.1','The later Parf category name remains capitalized. The attached source preserves the printed cases.','Remark4.10.1'),
41:('Page125 begins Soit and its triangle','Page124 ends at the interval[a−n,b−n]. The full introductory word and triangle begin125, as the attached marker now records.','Boundary124/125'),
42:('No colon after aussitôt le','The line ends at le and is followed by Corollary4.12. The added colon was correctly removed.','Before Corollary4.12'),
43:('Corollary4.12 statement word groups underlined','The hypothesis, finite-amplitude condition and two functors agree with the complete image. The interval bounds, arrows and zero-degree conditions retain their independent notation.','Corollary4.12 before functors'),
44:('et underlined between the displays','The single conjunction has a short rule.','Corollary4.12 between functors'),
45:('Final equivalence assertion underlined; stop outside','The rule ends after catégories before the final stop.','Corollary4.12 conclusion'),
}
for n,(printed,reason,region) in observations.items():
    r.finding(batch,n,printed,reason,region,witness=132 if n==5 else 134 if n in[25,32,34,35] else None,actual_page=122 if n==10 else None)
for n in[18,19,37]:
    r.finding(batch,n,'The indicated formula is in running text',
        'The complete page shows the category assignment or triangle formula within the sentence. The existing inline rendering preserves all words, arrow directions, degree labels and punctuation. Classify the display/inline choice as layout.',
        'Example4.8 category assignments' if n in[18,19] else 'Page124 triangle formulas',verdict='amended',change='Retain the attached inline rendering; layout classification only.')
id='ASTRA-I-SITE-MISSING-123';reason='Both scans leave the S in X∈obS without a rule. The quantified X indexes the fibers C_{0X}; the fiber projection C_0→the base site sends those objects to X. Paragraph4.0 names that base site with underlined S, and the proof on124 repeats X∈ob underlined S for these same triangle fibers. Thus the one missing rule belongs to the same explicitly identified base-site symbol. Add it only in current; preserve the witness’s plain letter diplomatically.'
r.own_finding(id,123,'Plain S in X∈obS',r'\(X\in\Ob S\)','Current only: underline this S',reason,'Proposition4.10(i), quantified base object',kind='misprint_in_print',witness=134)
r.patch(123,'current',r'\(X\in\Ob S\)',r'\(X\in\Ob \underline{S}\)',id,reason)
for p,count in[(121,11),(122,20),(123,29),(124,23),(125,13)]:
    id=f'ASTRA-I-C-{p:03d}';reason='All represented category letters have an independent short rule beneath typed C; their primes, numeric or object subscripts remain outside.'
    r.own_finding(id,p,'Underlined typed C',r'\mathcal C',r'\underline{C}',reason,'Every category C occurrence')
    r.patch(p,'both',r'\mathcal C',r'\underline{C}',id,reason,count)
id='ASTRA-I-M-121';reason='The five M occurrences in Notation4.5 are typed capitals with short independent rules, including the M_X fiber and the Hom_M index.'
r.own_finding(id,121,'Five underlined typed M category letters',r'\mathcal M',r'\underline{M}',reason,'Notation4.5, every M occurrence')
r.patch(121,'both',r'\mathcal M',r'\underline{M}',id,reason,5)
id='ASTRA-I-PARFRULE-123';reason='The statement rules visibly extend through the first Parf operator after La catégorie and after tout objet de. The other Parf operators have no such rule. Apply the two exact local rules while retaining the separate C argument rules.'
r.own_finding(id,123,'Parf underlined at two statement openings',r'Plain \Parf operator at both positions',r'\underline{\Parf} at those two positions',reason,'Proposition4.10 opening and item(ii)')
for prefix in ['La catégorie','tout objet de']:
    r.patch(123,'both',prefix+r' \(\Parf(',prefix+r' \(\underline{\Parf}(',id,reason)
for p,old,new,w in[(116,r'\otimes_A\cdot',r'\otimes_A.',127),(121,r'(\,\cdot\,,F_X)',r'(\,.\,,F_X)',132)]:
    id=f'ASTRA-I-DOT-{p:03d}';reason='The native witness and main scan place this placeholder at the baseline. On116 it aligns with the stops in i.e. and est exact.; on121 it lies at the bottom of the capital F, just above the comma tail. A centered multiplication dot would raise it. Retain the same functor argument slot and set the observed literal point.'
    r.own_finding(id,p,'Baseline placeholder point',old,new,reason,'Proposition3.7(a) tensor placeholder' if p==116 else 'Proof4.6 Hom placeholder',kind='symbol',witness=w)
    r.patch(p,'both',old,new,id,reason)
r.finding('116_120',2,'Proposition3.7(a) prose word groups underlined',
    'The rule starts at Soit; i.e. is plain. The morphism is flat on the right and the displayed functor is f*=A-prime⊗_A with a baseline placeholder point. The latter is independently resolved from the witness and patched in ASTRA-I-DOT-116.',
    'Proposition3.7(a) before display',witness=127)
site_positions={121:[1,2,3,4],122:list(range(2,11)),123:[1,2,4],124:[1,2],125:[1,2]}
site_counts={121:8,122:10,123:4,124:2,125:2}
for p,positions in site_positions.items():
    id=f'ASTRA-I-SITE-{p:03d}';reason='The recorded positions have visible site S rules. Other S letters name the fixed object or fiber and remain plain. On123 the witness’s single missing rule at X∈obS is a separate current-only repair, not part of this both-layer occurrence map.'
    r.own_finding(id,p,'Underlined site S at the exact selected positions','Plain S commands',f'Underline positions{positions}',reason,'Every site/object S occurrence')
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        matches=list(re.finditer(r'(?<![A-Za-z\\])S(?![A-Za-z])',old));assert len(matches)==site_counts[p],(p,len(matches))
        new=old
        for i,m in reversed(list(enumerate(matches,1))):
            if i in positions:new=new[:m.start()]+r'\underline{S}'+new[m.end():]
        r.patch(p,layer,old,new,id,reason)
r.finding(batch,11,'Visible site rules restored; object/fiber S retained plain',
    'All five complete images were read. Exact occurrence maps implement the printed S forms. The omitted rule in123(i) is confirmed by witness134 and repaired only in current using the same fiber projection and proof notation.',
    'All five pages, site/object convention',verdict='not applied and now applied',change='Apply five exact maps and the separately sourced current-only rule on123.',witness=134)
id='ASTRA-I-NOTE-122';reason='The call and bottom label have a raised star within baseline parentheses. The call is before the final full stop, outside the definition’s word rule. Preserve the complete author note and its independently underlined C_0.'
body=r'Bien entendu, quand cela ne pourra prêter à confusion, nous omettrons \(\underline{C}_0\) dans les expressions précédentes.'
r.own_finding(id,122,'Raised star in parentheses at call and note label',r'Automatically numbered \footnote',r'\SGAAuthorFootnote{raisedstar}',reason,'Definition4.7 final call and bottom note',kind='font')
r.patch(122,'both',r'\footnote{'+body+'}',r'\SGAAuthorFootnote{raisedstar}{'+body+'}',id,reason)
plain_parenthesis=r'(resp. \(\Tr(\Parf(\underline{C},\underline{C}_0))\))'
for p,count in[(121,6),(122,7),(123,9),(125,3)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The observed statement words are upright and underlined. The defined amplitude phrases remain plain; all mathematical letter and operator rules are independent. The numbered references and the first resp. parenthesis in4.10(ii) remain outside the word rules.'
    r.own_finding(id,p,'Upright underlined statement word groups',r'\emph spans',r'\uline groups with explicit plain exceptions',reason,'All existing emphasis spans')
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        plain={121:[],122:['(2.1)','(4.3)'],123:['(1.1.4)','([G] II 2.2.4)',plain_parenthesis],125:[r'\ à ']}[p]
        new,n=underline_words(old,plain);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)
for p,b,e,w in[(121,'si F est strictement parfait','tels qu’il existe un quasi-isomorphisme',132),(122,'F-prime→F de C(C_X)','sur A.; note se termine par expressions précédentes.',None),(123,'Proposition4.10 La catégorie','alors G',134),(124,'est parfait. Quitte à localiser','contenue dans[a−n,b−n].',None),(125,'Soit and the triangle','au lieu de amplitude C_0-parfaite.',None)]:
    r.page(p,b,e,'Every word, mathematical expression, all nine amplitude-table cells, triangle arrows, punctuation, note matter and page boundaries compared where present. Witness details and the current-only missing site rule are separately recorded.',witness=w)
r.commit()
