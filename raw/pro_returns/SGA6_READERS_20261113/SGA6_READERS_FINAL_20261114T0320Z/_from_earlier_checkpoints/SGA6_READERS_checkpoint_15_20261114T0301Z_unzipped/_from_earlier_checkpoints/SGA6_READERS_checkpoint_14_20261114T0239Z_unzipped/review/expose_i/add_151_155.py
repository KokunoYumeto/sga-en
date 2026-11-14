#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='151_155'
observations={
1:('Both Hom operators underlined and followed by raised dots','The biduality display has two independent Hom rules and two raised complex dots. Its argument order and final stop agree.','Proof7.2 display',None),
2:('Double-stem R followed by underlined Hom','The native witness resolves the two vertical R strokes in Definition7.3; the Hom rule is separate. The exponent is the duality vee.','Definition7.3 equality',162),
3:('Double-stem R and underlined Hom in the contravariant functor','The native witness resolves the added left stem and the Hom rule.','Paragraph after7.3, functor',162),
4:('Empty first argument in RHom( ,A)','Both the main and native witness have a clear blank before the comma. Retain the empty slot, with no inserted point or dash.','Paragraph after7.3, empty argument',162),
5:('First parf index plain; second parf index underlined','The two adjacent category expressions have exactly these printed rules; the second is followed by5.8.4.b).','Paragraph after7.3, two parf indices',162),
6:('Pour and the concluding existence phrase underlined','The category formulas and final colon remain outside the word rules. All S letters on this page are plain.','Lemma7.4 statement',162),
7:('First Cartan row has three ruled Hom operators and plain R letters','The native witness resolves each R as the ordinary single typed form. Each of the three Hom operators has its own rule. The isomorphism arrow has a head.','Lemma7.4 first display row',162),
8:('Second Cartan row has only its innermost Hom underlined','The first two global RHom operators are plain, and the inner RHom(F,G) has a Hom rule. Each R is the ordinary typed form. The arrow has a head.','Lemma7.4 second display row',162),
9:('Third Cartan row has only its innermost Hom underlined','The two Hom operators outside RHom(F,G) are plain. The inner R is plain and its Hom ruled. The arrowhead and final stop are visible.','Lemma7.4 third display row',162),
10:('Pour and the existence phrase underlined','The two category expressions retain their plain S letters and independent mathematics.','Lemma7.5 statement',163),
11:('Plain R and underlined Hom in the evaluation display','The witness shows the ordinary typed R and a short separate rule under Hom. The tensor has its plain superscript L.','Lemma7.5 display',163),
12:('No punctuation after the final F','The witness leaves the space after F blank. Retain the attached removal of the extra full stop.','Lemma7.5 display end',163),
13:('Soient underlined','The following formulas are independently typed with plain S letters.','Proposition7.6 opening',163),
14:('Comma after F∈ob D+(S), with no preceding stop','The main image has only a faint spot before the comma; the native witness shows a clean blank there. The visible comma has a full typed stroke. Retain the removal of the extra full stop.','Proposition7.6 second hypothesis',163),
15:('Sous l’une des hypothèses suivantes underlined','The word group has a rule through its words.','Proposition7.6 hypothesis lead-in',163),
16:('de tor-dimension finie underlined','The preceding G and final comma lie outside the rule.','Proposition7.6 item(i)',163),
17:('de tor-dimension finie et underlined','The E,F,G category formulas retain their independently typed forms.','Proposition7.6 item(ii)',163),
18:('il existe un homomorphisme fonctoriel canonique underlined','The full lead-in after the two items has its observed word rules.','Proposition7.6 before display',163),
19:('Both displayed R letters plain, both Hom operators underlined','The statement uses the single typed R twice. The source RHom(E,F)⊗G and target RHom(E,F⊗G), superscript L marks, arrow and stop agree.','Proposition7.6 display',163),
20:('Celui-ci est un isomorphisme quand and est parfait underlined','The E and terminal point remain outside the two word rules.','Proposition7.6 conclusion',163),
21:('Proof display has a double-stem R and underlined Hom','The native witness separates the extra R stem in the proof, which the preceding statement display does not print. Preserve each observed occurrence.','Proof7.6 display',163),
22:('Tensor functor printed as ⊗L G with an empty leading place','The native witness has no dash or point before the tensor sign. The reference is7.5.','Proof7.6 functor application',163),
23:('Il existe, and pour underlined','The two following formulas and joining et are plain; the existing mathematical parf rule is independent.','Corollary7.7 opening',None),
24:('parf index underlined in the first category expression','The rule belongs to the printed index itself.','Corollary7.7 category',None),
25:('un isomorphisme fonctoriel underlined','The two printed lines carry the same continuous word-group emphasis.','Corollary7.7 lead-in',None),
26:('Double-stem R, underlined Hom, headed isomorphism arrow','The main page resolves the added R stem, Hom rule and right arrowhead. The final punctuation is a comma.','Corollary7.7 display',None),
27:('avec la notation de underlined','The reference7.3 and final stop lie outside the rule.','Corollary7.7 end',None),
28:('parf index underlined in the proof','The proof has a rule under parf although its surrounding prose is plain.','Proof7.7 final category',164),
29:('Soient underlined','The following E,F and derived-category formula have their own mathematical typography.','Corollary7.8 opening',164),
30:('parf index underlined; membership sign physically incomplete','The native witness has the same broken upper/left portions of the membership glyph as the main scan. Its surviving strokes and the construction E,F followed by ob D(S) agree with the complete membership formula in7.7 and7.9. Retain the reconstructed membership sign and the visible parf rule.','Corollary7.8 first formula',164),
31:('Il existe une flèche naturelle underlined','The printed word group has a lower rule.','Corollary7.8 before display',164),
32:('Both R letters doubled and both Hom operators underlined','The pairing is RHom(E,F)⊗L RHom(F,E) to A, with a comma after the target.','Corollary7.8 pairing',None),
33:('Four prose groups ruled, quoted punctuation and i.e. plain','The rules cover qui est une, dualité parfaite, identifie modulo and chacun des complexes. The quotation marks, comma, i.e. and reference7.4 are outside. Apply that exact word-group segmentation.','Corollary7.8 after display',None),
34:('Both inline R letters doubled and Hom operators underlined','The two arguments occur in the printed orders E,F and F,E.','Corollary7.8 inline complexes',None),
35:('au dual de l’autre and au sens de ruled','The parentheses, reference7.3 and final stop remain plain. Apply that observed segmentation.','Corollary7.8 final phrase',None),
36:('Double-stem R and underlined Hom in les RHom','The proof operator retains the visible added R stroke and Hom rule.','Proof7.8 after pairing',None),
37:('Left derived Hom has double-stem R and ruled Hom','The first argument is F∨⊗L E and the second is A.','Proof7.8 aligned display left side',None),
38:('First right derived Hom has double-stem R and ruled Hom','The arguments are F∨ and E∨ in that order.','Proof7.8 aligned display first target',None),
39:('First isomorphism sign is a tilde over a headless bar','The main page clearly has no right arrowhead here, unlike the arrow of7.7. Keep simeq.','Proof7.8 first isomorphism sign',None),
40:('Second isomorphism sign is a tilde over a headless bar','The printed target is F∨∨⊗L E∨ and the accompanying reference7.6.','Proof7.8 second isomorphism sign',None),
41:('Third isomorphism sign is a tilde over a headless bar','The printed target is F⊗L E∨ and the accompanying reference7.2.','Proof7.8 third isomorphism sign',None),
42:('parf index underlined','The exercise prose is plain, while the index has its own visible mathematical rule. The following isomorphism has a head.','Exercise7.9',None),
43:('parf index underlined','The first category expression in8.1 retains its visible rule and reference5.8.4.b).','Paragraph8.1 opening',None),
44:('Double-stem R and underlined Hom in the trace map','The source is RHom(E,E), the target A, with a comma after A.','Paragraph8.1 trace display',None),
45:('Double-stem R and underlined Hom in the inverse isomorphism','The inline isomorphism to E∨⊗L E has a visible right arrowhead.','Paragraph8.1 after trace display',None),
46:('Baseline point in H^0(U,.)','The placeholder point sits on the baseline next to the comma. Its position differs from the raised cohomology exponent and is retained literally.','Paragraph8.1 functor',None),
47:('Double-stem R and underlined Hom inside H^0(U,...)','The outer H and following Hom_D(U) are plain. The native witness resolves the independent internal Hom rule.','Paragraph8.1 section identification',165),
48:('Page155 begins with8.1.1','The complete main154 page ends with the introductory sentence and its author note;155 begins the8.1.1 heading. The attached marker already agrees.','Boundary154/155',None),
49:('First displayed summation sign has no printed index','The two x symbols keep their i indices; no index is printed beneath the sum itself.','Paragraph8.1.1 first display',None),
50:('Inline trace sum has no printed index','The two factors keep their i indices. Preserve the bare summation sign.','Paragraph8.1.1 inline trace',None),
51:('Alternating-trace sum has no printed index','The superscript i remains on the sign and on E and u; the summation operator itself is bare.','Paragraph8.1.2 first display',None),
52:('H underlined in H^0(E∨⊗E)','The native witness has the short rule immediately beneath H. The section functors H^0(U,...) elsewhere retain their plain H.','Proof8.1.2 cohomology sheaf',166),
53:('Ordinary tensor sign with no L above it','The native witness resolves the filled crossing of the tensor and the blank above. The preceding E∨⊗E and x∨⊗x tensors in this same paragraph also have no L.','Proof8.1.2 evaluation arrow',166),
54:('First final-display sum has no printed indices','The native witness leaves the space under the sum empty, while retaining both ij subscripts on the paired sections.','Proof8.1.2 final display first sum',166),
55:('Second final-display sum has no printed index','The native witness confirms the bare sum, superscript i on the sign and the final comma before cqfd.','Proof8.1.2 final display second sum',166),
56:('parf index underlined','The8.2 category expression has a visible rule beneath the index, and its S remains plain.','Paragraph8.2 opening',None),
57:('Both R letters doubled and both Hom operators underlined','The pairing γ has the same argument order as7.8; the last punctuation is a full stop.','Paragraph8.2 pairing display',None),
58:('Double-stem R and underlined Hom in the section u','The outer H^0 is plain, with argument U followed by RHom(E,F).','Paragraph8.2 last line first section',None),
59:('Double-stem R and underlined Hom in the section v','The outer H^0 is plain, with argument U followed by RHom(F,E). The terminal stop remains on155.','Paragraph8.2 last line second section',None),
}
for n,(printed,reason,region,witness) in observations.items():r.finding(batch,n,printed,reason,region,witness=witness)

for p,count,positions in [(154,3,[3]),(155,3,[1,3])]:
    id=f'ASTRA-I-SITE-{p:03d}';reason='Only the site letters in U∈ob S have lower rules. Every S inside D(S) on these two pages is plain. Apply the exact occurrence map of the complete main images.'
    r.own_finding(id,p,'Site S underlined in U∈ob S','All S plain',f'Underline positions{positions} of{count}',reason,'All site/object S occurrences')
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text();matches=list(re.finditer(r'(?<![A-Za-z\\])S(?![A-Za-z])',old));assert len(matches)==count
        new=old
        for i,m in reversed(list(enumerate(matches,1))):
            if i in positions:new=new[:m.start()]+r'\underline{S}'+new[m.end():]
        r.patch(p,layer,old,new,id,reason)

for p,labels in [(154,['8.0.','8.1.']),(155,['8.1.1.','8.1.2.','8.2.'])]:
    id=f'ASTRA-I-ITEMS-{p:03d}';reason='The inspected paragraph numbers have the same plain type weight as the running text. Preserve the exact numbers and punctuation while removing the added bold.'
    r.own_finding(id,p,'Plain paragraph numbers','Bold paragraph numbers','Plain labels',reason,'Paragraph labels',kind='font')
    for label in labels:r.patch(p,'both',r'\textbf{'+label+'}',label,id,reason)

for p,count in [(151,1),(152,1),(153,2)]:
    id=f'ASTRA-I-PROOFSTOP-{p:03d}';reason='The inspected proof word has a lower rule, and its following full stop is outside that rule. The colon following the first proof word on152 is already separate.'
    r.own_finding(id,p,'Preuve underlined, following stop plain',r'\emph{Preuve.}',r'\emph{Preuve}.',reason,'Proof headings')
    r.patch(p,'both',r'\emph{Preuve.}',r'\emph{Preuve}.',id,reason,count=count)

id='ASTRA-I-NOTE-154';reason='The main image and native witness give a raised star inside baseline parentheses at both the call and the note. The call precedes the sentence’s final stop. Preserve the entire author note and its reference8.5.'
r.own_finding(id,154,'Raised-star author call and note label','Automatically numbered footnote',r'\SGAAuthorFootnote{raisedstar}',reason,'Trace definition and lower author note',kind='font',witness=165)
r.patch(154,'both',r"\footnote{L'hypothèse",r"\SGAAuthorFootnote{raisedstar}{L'hypothèse",id,reason)

for p,count,plain in [(151,3,('dual',',','.')), (152,9,(',',)), (153,9,('«~','~», i.e.\\ ','(7.4)','(7.3)','(',')')), (154,1,())]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='Reproduce the inspected upright word rules, keeping every mathematical expression independent. On151 the defined word dual is plain. On153 the quotation marks, i.e., parentheses and references7.4/7.3 are outside the rules. The trace term on154 has its own word rule.'
    r.own_finding(id,p,'Upright underlined word groups with explicit plain exceptions',r'\emph spans',r'\uline word groups',reason,'All existing emphasis spans',witness={151:162,152:163,153:164,154:165}[p])
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in ['both',layer]:old=old.replace(patch['old'],patch['new'])
        new,n=underline_words(old,plain=plain);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)

for p,b,e,w in [(151,'Preuve. On définit la flèche','Hom(E,RHom(F,G)).',162),(152,'Preuve : C’est standard','au cas où E=A.',163),(153,'Corollaire7.7. Il existe, pour','se ramener à E=F=A.',164),(154,'Exercice7.9. Soient E,F','Author note: définition de Tr_E|U, voir8.5.',165),(155,'8.1.1. Si E=A','v∈H^0(U,RHom(F,E)).',166)]:
    r.page(p,b,e,'Complete prose and author note, every category bound, duality exponent, derived-functor letter, Hom rule, arrowhead, bare or indexed sum, tensor exponent, punctuation and boundary compared. Statement labels and section titles retain the expressly permitted NOTE_6 typesetting convention.',witness=w)
r.commit()
