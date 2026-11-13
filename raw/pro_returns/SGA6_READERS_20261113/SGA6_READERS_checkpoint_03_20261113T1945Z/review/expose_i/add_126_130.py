#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='126_130'
observations={
1:('quasi-relevable underlined','The complete main page and witness show one rule beneath this entire adjective.','Remark4.12.2 opening',137),
3:('Plain C_0 in the first inline K^b(C_0)','Both scans omit the rule at this one C. The C_0 in the preceding sentence and all later occurrences have their rules. The same full embedding i:C_0→C induces K^b(i), followed by localization to D(C); its domain is exactly the named C_0. Preserve the missing rule diplomatically and retain the corrected rule at this occurrence.','Remark4.12.2 first inline functor',137),
4:('Loop crossed by a long diagonal slash as the second upper index','The witness resolves the closed loop and long slash. Keep the attached varnothing glyph at this exact occurrence.','Remark4.12.2 definition of acyclic subcategory',137),
5:('The same crossed-loop upper index','The first quotient display repeats the sign of the preceding definition.','Remark4.12.2 first display',137),
6:('The same crossed-loop upper index after the minus','The indication explicitly refers to2.7 and reproduces its acyclic-subcategory index. The witness resolves the loop and slash.','Indications first display',137),
7:('The same crossed-loop upper index after b','The sign is legible separately from the missing quotient slash discussed in finding9.','Indications final display, source',137),
8:('The same crossed-loop upper index after the minus','The target quotient has its quotient slash and this separate crossed-loop superscript.','Indications final display, target',137),
9:('No quotient slash between K^b(C_0) and K^{b,∅}(C_0)','Both scans show the two expressions adjacent. The inclusion K^b(C_0)→K^−(C_0) sends bounded acyclic complexes into K^{−,∅}(C_0); composing with the latter quotient therefore factors through K^b(C_0)/K^{b,∅}(C_0). This is the source already displayed above. Retain the existing corrected slash and the diplomatic omission.','Indications final display, source',137),
10:('Page127 begins F-prime^i=F^i','Page126 ends with défini par; the truncation formula begins127. The attached marker now matches the printed break.','Boundary126/127',None),
11:('Corollary4.14 prose rules and an independent parf.amp rule','Soient, et and Conditions équivalentes have word rules. Item(i) also rules the parf.amp operator, which the earlier prose-only fix omitted; ASTRA-I-OPRULE-127 restores that exact rule.','Corollary4.14 opening and item(i)',138),
12:('Corollary4.14(ii) word groups underlined, including i.e.','The complete line shows a rule beneath i.e. as well as the resolution and refinement clauses. The formulas remain outside the prose rules.','Corollary4.14(ii) before display',138),
13:('Three baseline full stops in the resolution','The witness places all three stops at the bottom of the neighboring arrow shafts and letters. Keep the attached baseline ellipsis.','Corollary4.14(ii) exact sequence',138),
14:('Adjacent indices0 and X without a comma','The category C rule is separate from the two lowered indices. No comma appears between0 and X.','Corollary4.14(ii) after display',138),
15:('avec underlined','The word rule is followed by the independently typeset membership formula.','Corollary4.14(ii) after display',138),
16:('pour tout and est un raffinement de underlined','The variable i and object S remain outside the word rules.','Corollary4.14(ii) ending',138),
17:('The second dimension parfaite phrase is plain','The defined term after Nous appellerons is unruled; the surrounding words are ruled. The earlier phrase est de dimension parfaite is ruled, and the two parf.dim operators have different observed rule states.','Definition4.14.1',138),
19:('Proposition4.17 opening word groups underlined','Soient, et, avec and Considérons les conditions have rules; the colon and item labels remain outside.','Proposition4.17 opening',None),
20:('Proposition4.17 conclusion underlined by word groups','The statement rules stop around formulas, the inline(i)/(ii) labels and the plain i.e. The direct sums remain printed with plus signs.','Proposition4.17 final statement paragraph',None),
21:('Page129 begins F-prime^i=F-double-prime^i=0','Page128 ends en tronquant, que. The complete degreewise vanishing formula begins129, as the attached marker records.','Boundary128/129',None),
22:('parf.dim(F)⊂[a,b]','The main page plainly types dim. Here F=F-prime+F-double-prime, and condition4.17(ii) gives parf.amp(F)⊂[a,b]. After the stated truncations, F^i belongs to C_0 for i>a, so the proof invokes exactly Lemma4.16 with that amplitude hypothesis. Retain the current amp correction and diplomatic dim.','Page129 first line',None),
23:('No comma before puisque','The main page runs directly from C_0 to puisque. The source’s extra comma was correctly removed.','Page129 opening paragraph',140),
24:('Proposition4.18 opening prose word groups underlined','The reference(4.0) is plain. The six S letters naming sites and the category C letters have independent short rules.','Proposition4.18 opening',140),
26:('Crossed-loop sign as the third value of the star','The witness shows the loop and long diagonal slash in(*=−,+,∅), matching the sign at2.13 and the five acyclic indices on126. Retain the attached varnothing.','Proposition4.18 functor condition',140),
27:('Functor and perfect-complex assertion underlined by word groups','The reference(cf.(2.13)) is plain. The rules beneath un foncteur, au-dessus de and the concluding implication are explicit.','Proposition4.18 remaining statement',140),
29:('D*(C) without the prime after sous-catégorie triangulée de','The displayed perfect subcategory is D*(C-prime)_{C-prime_0-parf}. Definition4.9 gives the full inclusion j into D*(C-prime), identical on objects and morphisms;4.10 applied to the primed trio gives its triangulated structure. This precise inclusion supplies the missing prime in the ambient expression. Keep the printed unprimed C diplomatically.','Proof4.18 final clause',None),
30:('Corollary4.19 statement word groups underlined','The reference(2.16) remains plain; the rules resume at si and cover the stated perfectness predicates.','Corollary4.19 opening',140),
32:('est parfait underlined, stop outside','The short final predicate has its own rule.','Corollary4.19 ending',140),
33:('Left coefficient index A-prime','The witness resolves the high prime on the lowered A before S-prime_A. Keep the attached primed coefficient.','Corollary4.19 first category',140),
34:('Left coefficient index A-prime','The second category also shows the high prime on lowered A.','Corollary4.19 second category',140),
35:('Left coefficient index A-prime','The proof’s first category has A-prime on the left and A on the right; its S-prime is the plain final object.','Proof4.19 first category',140),
37:('Left coefficient index A-prime in the functor target','The target category has both the coefficient prime and the site prime.','Proof4.19 final functor',140),
38:('Le foncteur underlined','The rule belongs to the words; the adjacent derived-functor expression has independently observed mathematical fonts.','Corollary4.19.1(a) opening',141),
40:('Double-struck L in the first Lf*','The first stem is heavily inked, but its doubled outer contour agrees in both scans with the clear separated stems in the next two occurrences of this same functor. Keep mathbb L. The L above each tensor product is plain.','Corollary4.19.1(a) first formula',141),
41:('Left coefficient index A-prime','The target of the first derived inverse-image functor has the raised prime beside the lowered A.','Corollary4.19.1(a) first target',141),
42:('induit un foncteur underlined','The word rule precedes the first display.','Corollary4.19.1(a) before display',141),
43:('Double-struck L in the display','The witness clearly separates the two stem strokes.','Corollary4.19.1(a) display',141),
44:('Left coefficient index A-prime','The same primed coefficient appears in the perfect subcategory target.','Corollary4.19.1(a) displayed target',141),
45:('Si, est commutatif and le foncteur underlined','The A between the word groups remains plain.','Corollary4.19.1(b) opening',141),
47:('induit un foncteur underlined','The concluding word rule precedes the tensor-product display.','Corollary4.19.1(b) before display',141),
48:('Double-struck L inside the final amplitude expression','The witness clearly resolves the double stem. The two interval bounds are unchanged.','Remark4.19.2 final formula',141),
}
for n,(printed,reason,region,witness) in observations.items():
    r.finding(batch,n,printed,reason,region,witness=witness)
for n in[2,25,28,31,36,39,46]:
    r.finding(batch,n,'The indicated formula is in running text',
      'The complete printed page places this formula within its sentence. The attached inline form preserves every term, arrow, index and punctuation; classify the display/inline choice as layout.',
      'The inline functor or tensor formula identified by this finding',verdict='amended',change='Retain attached inline rendering; layout classification only.')
for number,finding in[(345,22),(346,29)]:
    printed,reason,region,witness=observations[finding]
    r.source(f'fixes/FIXLOG_6_CURRENT.jsonl#{number}',printed,reason,region,
      change='Retain existing current correction; preserve the printed reading diplomatically.')

for p,counts in[(126,(20,21)),(127,(8,8)),(128,(10,10)),(129,(27,27)),(130,(2,2))]:
    id=f'ASTRA-I-C-{p:03d}';reason='The category letters represented by these commands are typed C with an independent underline; primes and object/numeric indices stay outside the rule. The lone missing printed rule in126 is preserved separately in the diplomatic text.'
    r.own_finding(id,p,'Underlined typed category C letters',r'\mathcal C',r'\underline{C}',reason,'Every represented category C occurrence')
    if counts[0]==counts[1]:r.patch(p,'both',r'\mathcal C',r'\underline{C}',id,reason,counts[0])
    else:
        for layer,count in zip(['diplomatic','current'],counts):r.patch(p,layer,r'\mathcal C',r'\underline{C}',id,reason,count)

id='ASTRA-I-OPRULE-127';reason='The native witness shows a rule under parf.amp in4.14(i), and under only the second parf.dim operator in4.14.1 after le plus petit entier n tel que. The first parf.dim after et nous écrirons remains plain. Reproduce those two exact local operator rules.'
r.own_finding(id,127,'Two local operator underlines','Both operators plain','Underline parf.amp in4.14(i) and second parf.dim in4.14.1',reason,'Corollary4.14 and Definition4.14.1',witness=138)
r.patch(127,'both',r'\item \(\perfamp(F)',r'\item \(\underline{\perfamp}(F)',id,reason)
r.patch(127,'both',r'tel que \(\perfdim(F)',r'tel que \(\underline{\perfdim}(F)',id,reason)
id='ASTRA-I-OPRULE-128';reason='The statement of Lemma4.16 rules the parf.amp operator in its hypothesis. The later amplitude operators in the proof and Proposition4.17 have no such rule and remain plain.'
r.own_finding(id,128,'Underlined parf.amp in Lemma4.16',r'Plain \perfamp',r'\underline{\perfamp}',reason,'Lemma4.16 amplitude hypothesis')
r.patch(128,'both',r"On suppose que l'on a \(\perfamp(F)",r"On suppose que l'on a \(\underline{\perfamp}(F)",id,reason)

site_positions={127:[4],128:[2],129:[1,2,3,4,5,6,7,8,9,12,13,14],130:list(range(1,13))}
site_counts={127:4,128:2,129:14,130:12}
for p,positions in site_positions.items():
    id=f'ASTRA-I-SITE-{p:03d}';reason='The exact selected S letters have visible independent site rules. The other S letters denote the fixed object or its fibers. In129 the first S-prime inside the proof category and the S-prime before =objet final are plain; the site after de is ruled. In130 both fiber-product bases are ruled and are braced explicitly in TeX.'
    r.own_finding(id,p,'Site S underlined at the exact selected positions','Plain S commands',f'Underline positions{positions}',reason,'Every site/object S occurrence',witness=p+11 if p in[127,129,130] else None)
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
r.finding(batch,18,'Observed site rules restored with object S forms retained',
  'The four full pages and native witnesses at127,129,130 determine exact occurrence maps. The final object S-prime in the proof of4.19 remains plain, while the base sites in that same sentence have rules.',
  'Folios127–130, site/object letter convention',verdict='not applied and now applied',change='Apply the four exact S occurrence maps.',witness=138)

id='ASTRA-I-ITEMS-130';reason='The item letters a), b) and paragraph number5.0 are typed in the same weight as running text. Keep the accepted statement/section heading convention, and remove the added bold at only these three labels.'
r.own_finding(id,130,'Plain a), b) and5.0',r'\textbf labels','Plain labels',reason,'Corollary4.19.1 and paragraph5.0',kind='font')
for label in ['a)','b)','5.0.']:r.patch(130,'both',r'\textbf{'+label+'}',label,id,reason)
for p,count in[(126,3),(127,9),(128,6),(129,8),(130,4)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='Render the observed statement and proof-label word rules upright. Mathematical symbols retain their separately inspected rules and fonts; numbered references, the defined dimension parfaite term, and the plain i.e./item labels in4.17 retain their observed local exceptions.'
    r.own_finding(id,p,'Upright underlined prose word groups',r'\emph spans',r'\uline groups with explicit plain exceptions',reason,'Every existing emphasis span')
    for layer in['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        plain={126:['(4.7)'],127:['(4.14)'],128:['(i)','(ii)','i.e.'],129:['(4.0)'],130:[]}[p]
        new,n=underline_words(old,plain);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)

for p,b,e,w in[(126,'Remarque4.12.2. Soit C','à son tronqué F-prime défini par',137),(127,'F-prime^i=F^i','F l’est aussi.',138),(128,'Preuve. Procéder par récurrence','puis, en tronquant, que',None),(129,'F-prime^i=F-double-prime^i=0','En particulier :',140),(130,'Corollaire4.19.1. a) Le foncteur','C’est ce que nous allons examiner maintenant',141)]:
    r.page(p,b,e,'Complete prose, formulas, five crossed-loop indices on126, truncation and exact-sequence indices, local operator rules, functor arrows, perfect-amplitude bounds and page boundaries compared. The top of131 was read regionally to confirm that the sentence after maintenant continues with dans le cas; no final stop is inserted.',witness=w)
r.commit()
