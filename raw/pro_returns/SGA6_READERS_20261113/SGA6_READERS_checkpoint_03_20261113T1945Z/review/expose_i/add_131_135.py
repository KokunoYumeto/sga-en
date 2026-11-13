#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='131_135'
observations={
2:('Proposition5.1(i) prose word groups underlined','The isomorphism, flatness and degree-vanishing predicates have word rules; all mathematical expressions remain independently typeset.','Proposition5.1(i)',None),
3:('Proposition5.1(ii) prose word groups underlined','The rules cover pour tout, Module à droite, on a and pour. The cohomology H has a separate short rule.','Proposition5.1(ii)',None),
4:('Underlined H in the cohomology-sheaf expression','The main page clearly gives the H its own rule below the baseline. Keep the attached underlined operator and plain raised i.','Proposition5.1(ii), cohomology formula',None),
5:('Comma to the right of F in the triangle','The main and witness place a comma beyond the bottom-right vertex. The three vertices, arrows and +1 label agree with the attached diagram.','Proof5.1.1 triangle',142),
7:('The defined amplitude plate phrase is plain','The surrounding definition words have rules. The reference(5.1) and the defined phrase remain outside those rules.','Definition5.2 opening',None),
8:('Definition5.2 final sentence underlined by word groups','The later amplitude plate finie phrase is itself ruled, including the ou de tor-dimension finie parenthesis. The final rule reaches the stop.','Definition5.2 last sentence',None),
9:('Page133 begins5.5. Soient X∈obS','Page132 ends A-Modules plats. The paragraph number belongs at the top of133, as the attached marker records. Its type weight is repaired separately.','Boundary132/133',None),
10:('The /X is lowered after the site S','Both slash and X belong to the lower index; retain the attached subscript and add the independently observed S rule.','Paragraph5.5, localized topos',None),
13:('Le foncteur underlined','The rule covers the opening words, with a plain item letter a).','Corollary5.6.1(a) opening',144),
14:('induit un foncteur underlined','The rule continues across the print’s line break before the derived-functor display.','Corollary5.6.1(a) before display',144),
15:('Si, est commutatif and le foncteur underlined','The coefficient A is outside the word rules; the item letter b) is plain.','Corollary5.6.1(b) opening',144),
16:('induit un foncteur underlined','The last word group precedes the tensor-product display.','Corollary5.6.1(b) before display',144),
17:('Heavily inked double-width L at the first Lf*','The two scans fill the first stem, while the displayed occurrence immediately below resolves the two strokes of the same Lf* operator. Retain the double-struck reconstruction and explicitly record the filled interior instead of claiming a visible gap here.','Corollary5.6.1(a) inline functor',144),
18:('Double-struck L in the displayed Lf*','The witness separates the two stems. The tensor-product superscript L elsewhere on the page is plain.','Corollary5.6.1(a) display',144),
19:('Left coefficient A-prime in D^−(_{A-prime}S-prime)','The small stroke is level with the top of the lowered A, exactly the prime used on S-prime.','Proposition5.6 coefficient index',None),
20:('Left coefficient A-prime in the first target','The witness resolves the high prime at the lowered coefficient.','Corollary5.6.1(a) inline target',144),
21:('Left coefficient A-prime in the displayed target','The same raised coefficient prime is explicit in the subcategory of finite tor-dimension.','Corollary5.6.1(a) displayed target',144),
23:('Double-struck R before the first Hom','The native witness clearly resolves the additional left stem. All S letters in this object-level Hom formula are plain, as printed.','Exercise5.7(b), inline Hom functor',145),
24:('Hom has one independent underline','The witness separates the single rule from the typewritten letters.','Exercise5.7(b), inline Hom functor',145),
25:('Double-struck R before the second Hom','The second occurrence also has the explicit double stem.','Exercise5.7(b), displayed Hom functor',145),
26:('Displayed Hom has one independent underline','The remaining formula, including the opposite-category circle and torf/injf indices, agrees with the native witness.','Exercise5.7(b), displayed Hom functor',145),
27:('Theorem5.8 opening word groups underlined','Soient, un topos annelé, avec and Conditions équivalentes have rules. The two site letters S have independent rules, whereas the S object symbols in the preceding exercise are plain.','Theorem5.8 opening',None),
28:('Theorem5.8(ii) prose word groups underlined','The numbered references(2.15) and(5.2) remain plain. The degree is m−1, followed by pseudo-cohérent.','Theorem5.8(ii)',145),
29:('The concluding lead-in is underlined, with plain quotation marks','The witness puts the rules under the words parfait and pseudo-cohérent but leaves both quotation marks outside. The colon also lies outside.','After Theorem5.8',145),
30:('parf.amp and parf.dim use the printed a','The complete images on127–135 and the native witness of134 show parf.amp/parf.dim. Both attached macro definitions already expand to these letter strings. Retain those definitions; the macro names themselves are internal TeX identifiers.','Theorem5.8(i) and repeated amplitude notation',145),
31:('Reference(2,15) with a comma','The printed comma is clear in the corollary. Section2.15 on108 defines pseudo-coherence for Modules, the property invoked here. Retain(2,15) diplomatically and the established reference(2.15) in current.','Corollary5.8.1',None),
32:('Lemma5.8.2 opening word groups underlined','The bimodule side conventions and the canonical-map assertion match the print, with formulas outside the word rules.','Lemma5.8.2 before formula',None),
33:('Final isomorphism assertion underlined by word groups','The rule extends under Celui-ci est un isomorphisme pour, injectif et and de présentation finie; the final stop is outside.','Lemma5.8.2 after formula',None),
34:('All three Hom operators in5.8.2.1 underlined','The underlines are independent of the B,A coefficient indices. The displayed target and full stop match the source.','Formula5.8.2.1',None),
35:('Both Hom operators in(*) underlined','The coefficient of the middle tensor product is the constant sheaf Z_S, with plain final-object S.','Proof5.8.2, formula(*)',146),
36:('Numeric author-note call before the full stop','The witness gives G, then parenthesized raised1, then the stop. Preserve the attached order and restore the original note label explicitly.','Formula(*) ending',146),
37:('Hom_A(E,F) underlined in(**)','The formula is the evaluation map E⊗_{Z_S}Hom_A(E,F)→F, with no added terminal stop.','Proof5.8.2, formula(**)',None),
38:('Hom_A(E,F) underlined in the adjunction explanation','The parenthetical text names the identity of this same sheaf-Hom object; its rule is visible.','After formula(**)',None),
39:('Hom_B(F,G) underlined in(***)','The final evaluation arrow and its terminal full stop agree with the print.','Proof5.8.2, formula(***)',None),
}
for n,(printed,reason,region,witness) in observations.items():r.finding(batch,n,printed,reason,region,witness=witness)
r.finding(batch,1,'Proposition5.1 opening word groups underlined; bound m≤n',
  'Both native scans show a separate slanted lower stroke beneath the less-than sign in the opening bound. The checker’s scan field and both layers lost that stroke. The later parenthetical supposer m<n has only a strict chevron. Preserve the prose rules and amend only the first bound to m≤n in both layers.',
  'Proposition5.1 opening bound',verdict='amended',change='Keep statement word rules; replace the first m<n with m≤n in both layers.',witness=142)
for n in[11,12,22]:
    r.finding(batch,n,'The indicated functor is inline in its sentence',
      'The complete page places the formula within the running sentence. The attached inline form preserves all objects, arrows, signs and punctuation. Classify the display/inline choice as layout.',
      'Inline functor identified by the finding',verdict='amended',change='Retain attached inline rendering; layout classification only.')

id='ASTRA-I-BOUND-131';reason='Main PDF145 and witness142 both have a separate slanted lower stroke, giving m≤n in Proposition5.1. The native crops also show the later supposer m<n without a lower stroke. Change only the first expression, by direct glyph comparison; this repairs the transcription rather than changing the printed assertion.'
r.own_finding(id,131,'m≤n in Proposition5.1',r'tels que \(m<n\)',r'tels que \(m\leq n\)',reason,'Proposition5.1 opening',kind='symbol',witness=142)
r.patch(131,'both',r'tels que \(m<n\)',r'tels que \(m\leq n\)',id,reason)
id='ASTRA-I-DOT-131';reason='The native witness places the functor’s placeholder point at the baseline, level with the full stop after supposer m<n. The argument slot remains the same; use the observed point instead of a centered multiplication dot.'
r.own_finding(id,131,'Baseline placeholder after the tensor functor',r'\otimes}_A\cdot',r'\otimes}_A.',reason,'Final proof paragraph',kind='symbol',witness=142)
r.patch(131,'both',r'\otimes}_A\cdot',r'\otimes}_A.',id,reason)

site_positions={131:[1,2],132:list(range(1,11)),133:list(range(1,16))+[18,19,20],134:[1,2,5,17,18],135:[1,4]}
site_counts={131:2,132:10,133:20,134:18,135:6}
for p,positions in site_positions.items():
    id=f'ASTRA-I-SITE-{p:03d}';reason='Exact occurrence maps reproduce the visible S rules. The fixed final-object S and its module or constant-sheaf indices remain plain. In134 every S in the two Hom functors is plain, while the theorem’s site letters are ruled. Bare fiber-product subscripts are braced when their S is underlined.'
    r.own_finding(id,p,'Underlined site S at selected positions','Plain S commands',f'Underline positions{positions}',reason,'Every site/object S occurrence',witness=p+11 if p in[131,133,134,135] else None)
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        matches=list(re.finditer(r'(?<![A-Za-z\\])S(?![A-Za-z])',old));assert len(matches)==site_counts[p],(p,len(matches))
        new=old
        for i,m in reversed(list(enumerate(matches,1))):
            if i in positions:new=new[:m.start()]+r'\underline{S}'+new[m.end():]
        new=new.replace(r'\times_\underline{S}',r'\times_{\underline{S}}')
        r.patch(p,layer,old,new,id,reason)
r.finding(batch,6,'Site S rules restored with printed object S forms preserved',
  'The five complete pages and the native witness regions determine exact occurrence maps. The author notes explicitly identify the plain S as the final object of the underlined site S; the six plain S letters in the134 Hom functors are preserved.',
  'All five pages, S convention',verdict='not applied and now applied',change='Apply the five exact S maps.',witness=145)

for p,labels in[(132,['5.3.','5.4.']),(133,['5.5.','a)','b)']),(134,['a)','b)'])]:
    id=f'ASTRA-I-ITEMS-{p:03d}';reason='The paragraph numbers and item letters are printed in the running type weight. Remove the added bold at these exact labels; retain the agreed treatment of statement headings.'
    r.own_finding(id,p,'Plain paragraph numbers and item letters',r'\textbf labels','Plain labels',reason,'The selected paragraph and item labels',kind='font')
    for label in labels:r.patch(p,'both',r'\textbf{'+label+'}',label,id,reason)

id='ASTRA-I-NOTE-134';reason='The first call, repeated call and bottom label are all a raised1 inside baseline parentheses. Preserve the complete final-object explanation and the same label at both calls.'
r.own_finding(id,134,'Repeated parenthesized raised1 author note','Automatic footnote and repeated current counter','Explicit author note1 and repeated mark1',reason,'Exercise5.7(a)/(b) and bottom note',kind='font',witness=145)
r.patch(134,'both',r'\footnote{\(S\) = objet final de \(\underline{S}\)}',r'\SGAAuthorFootnote{1}{\(S\) = objet final de \(\underline{S}\)}',id,reason)
r.patch(134,'both',r'\footnotemark[\value{footnote}]',r'\SGAAuthorFootMark{1}',id,reason)
id='ASTRA-I-NOTE-135';reason='The formula call and bottom label use parenthesized raised1. The call precedes the full stop. Preserve the complete lowercase-on note and the plain object S versus underlined site S.'
r.own_finding(id,135,'Parenthesized raised1 at formula and note','Automatic note mark/text','Explicit author note1 mark/text',reason,'Formula(*) and bottom note',kind='font',witness=146)
r.patch(135,'both',r'\text{\footnotemark}',r'\text{\SGAAuthorFootMark{1}}',id,reason)
r.patch(135,'both',r'\footnotetext{on note',r'\SGAAuthorFootText{1}{on note',id,reason)

for p,count in[(131,6),(132,3),(133,6),(134,4),(135,4)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The observed prose word groups are upright and underlined. The newly defined amplitude plate phrase, numbered references and quoted punctuation retain their explicit plain states; mathematical fonts and rules are treated independently.'
    r.own_finding(id,p,'Upright underlined prose word groups',r'\emph spans',r'\uline groups with explicit plain exceptions',reason,'Every existing emphasis span')
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        plain={131:['(ii) de (5.1)'],132:['(5.1)'],133:['(2.16)'],134:['«','»'],135:['(4.8)','(2,15)','(2.15)','(5.2)']}[p]
        new,n=underline_words(old,plain);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)

for p,b,e,w in[(131,'dans le cas de la catégorie des Modules','et écrire la suite exacte de cohomologie.',142),(132,'Définition5.2. Un objet','par des A-Modules plats.',None),(133,'5.5. Soient X','de la notion d’amplitude',144),(134,'plate, et le fait que','on en déduit :; note S=objet final de S',145),(135,'Corollaire5.8.1. Pour que','identité pour E=A.; note valeur Z.',146)]:
    r.page(p,b,e,'Complete prose, indices and bounds, triangle orientation and +1, tensor and Hom arrows, author-note calls/text, degree superscripts, punctuation and page boundaries compared. Native detail crops settle the non-strict first bound on131 and the locally plain object symbols.',witness=w)
r.commit()
