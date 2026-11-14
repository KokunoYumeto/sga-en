#!/usr/bin/env python3
import re
from review_helpers import Review,ROOT,underline_words
r=Review();batch='111_115'
observations={
2:('Opening derived-tensor-product prose underlined','The first line continues the preceding statement; the rule ends with the word tensoriel before the separately typed formula.','First line of111'),
3:('Statement2.16 word groups underlined','All bounds m, m-prime, n, n-prime, sup(m+n-prime,m-prime+n) and the final n+n-prime agree with the print. The independent site and coefficient letters are handled separately.','Statement2.16 continued'),
4:('Prime present on A in D^−(_{A′}S′)','The coefficient is A-prime in both the assertion and its proof. The short prime sits on the coefficient, separately from the prime on S.','Statement2.16 parenthetical category'),
6:('on a','The proof reads on at the end of one line and a at the start of the next. The attached replacement of alors restores these exact words.','Proof2.16, E=(A_U)^p'),
7:('Sous les hypothèses de and on a underlined','The reference(2.16) and the final colon remain outside the rules.','Corollary2.16.1 opening'),
8:('Functor statement word groups underlined','The words around the two formulas have rules. The two derived-functor letters are independently double-struck.','Corollary2.16.1(a)'),
9:('Double-struck L before f* in the running text','The witness resolves the two vertical strokes in L. The tensor-product superscript L remains plain as printed.','Corollary2.16.1(a), first Lf*'),
10:('Double-struck L before f* in the display','Both the main scan and witness show the doubled vertical stem. Retain the existing mathbb L.','Corollary2.16.1(a), displayed Lf*'),
11:('notation de underlined','The parenthesis and the reference(2.6) have no rule.','After the display in2.16.1(a)'),
12:('Tensor-functor statement word groups underlined','The word groups Si, est commutatif, le foncteur and induit un foncteur have rules; the site S letters have their own short rules.','Corollary2.16.1(b)'),
13:('n-pseudo-oohérent in the exercise','The first consonant of cohérent is mistyped as o. The same term is spelled cohérent elsewhere in the same sentence and in Definition2.3. Preserve oohérent diplomatically and the existing corrected cohérent.','Exercise2.16.2 conclusion'),
14:('Defined précohérent left plain','The rules stop after est and resume at the following parenthesis. The attached split leaves the defined word plain.','Definition3.1 first defined term'),
15:('C_{0U} with no internal comma','The comma follows the entire membership formula; no comma separates the two subscripts.','Definition3.1 membership of E'),
16:('Defined cohérent left plain','The defined word lies between two separately underlined prose groups, exactly as précohérent above.','Definition3.1 second defined term'),
17:('Lemme3.3 without a terminal full stop','The label ends after the numeral3. The attached diplomatic omission and corrected full stop preserve the two stated forms.','Lemma3.3 label'),
18:('Soit underlined','The word has a short rule before the three-arrow sequence, whose last H carries no additional punctuation.','Lemma3.3(a) opening'),
19:('Continued statement3.3(a) underlined by word groups','The page starts une suite exacte. The formulas G, H and F remain separately typed between the prose rules.','Top of113'),
20:('Soit underlined','The short word rule precedes F→G→H→0. No initial zero is printed in this part.','Lemma3.3(b) opening'),
21:('Statement3.3(b) word groups underlined','The printed finite-type hypothesis belongs to F, the precoherence hypothesis to G, and the conclusion to H. The attached text matches every term.','Lemma3.3(b) continuation'),
22:('Soit underlined','The word precedes the exact sequence with both initial and terminal zero.','Lemma3.3(c) opening'),
23:('Statement3.3(c) word groups underlined','The two hypotheses are on F and H; the conclusion is on G, with the parenthetical finite-type clause included.','Lemma3.3(c) continuation'),
24:('C_{0U} with adjacent subscripts','The membership formula has no extra comma between0 and U.','Proof3.3(b), membership of H-prime'),
25:('F-prime membership begins115; avec ends114','The full images show the last word avec on114 and the first membership formula on115. The attached marker is already at that exact boundary.','Boundary114/115'),
27:('No colon after immédiatement le','The line ends at le, followed by the new corollary label on the next paragraph.','Before Corollary3.4'),
28:('Corollary3.4 prose underlined; plural endings visible','The typescript additions give limites, inductives and finies in the plural. Those visible corrections belong to the printed reading. The source keeps all three.','Corollary3.4 before display'),
29:('Continuation3.4 word groups underlined','The exact sequence has E^0 through E^4; the listed coherent terms are E^0,E^1,E^3,E^4 and the conclusion concerns E^2.','Corollary3.4 after display'),
30:('Opening3.5 prose underlined; final reference plain','The rules cover the words up to conditions de; the final reference and the two closing parentheses remain plain. The abbreviation i.e. is also outside a rule.','Corollary3.5 hypothesis'),
31:('Conditions équivalentes sur underlined','The formula F∈ob C_S and the following colon have their independent typography.','Corollary3.5(a) opening'),
32:('Three equivalence clauses underlined by word groups','The three clauses are finite presentation, coherence and infinity-presentation. Each F and the final reference(2.8) remain outside the rules.','Corollary3.5(a), items(i)–(iii)'),
33:('Soient and On a underlined','The category formula, integer membership and colon remain outside these word rules. The integer Z has the visible second stem.','Corollary3.5(b) opening'),
34:('Four word groups underlined inside the display','The rules cover pseudo-cohérent, cohérent pour, et and de type fini. The n, the cohomology expressions and the bound i≥n+1 stay separately typed.','Corollary3.5(b) final equivalence'),
}
for n,(printed,reason,region) in observations.items():
    r.finding(batch,n,printed,reason,region,witness=122 if n in[9,10,11,12] else None)
id=r.finding(batch,5,"X′=u(X)",
    'The morphism in2.16 is specified by f^(−1):S→S-prime. Its value on X is therefore f^(−1)(X), and the proof explicitly uses U-prime=f^(−1)(U). The symbol u in that proof is instead the derived tensor functor E-prime⊗^L_A on complexes. Substituting the defined inverse-image morphism gives the required object of S-prime and the exact localizations in the proof.',
    'Statement2.16, definition of X-prime',verdict='not applied and now applied',change='Current only: X-prime=u(X)→X-prime=f^(−1)(X).')
r.patch(111,'current',r"\(X'=u(X)\)",r"\(X'=f^{-1}(X)\)",id,'Use the inverse-image functor defined on site objects, as in the proof’s U-prime=f^(−1)(U).')
r.finding(batch,26,'Broken vertical v-arrow, with three separated stem segments',
    'The native witness reproduces the same separated stem segments as the main scan. The adjacent u-arrow and w-arrow have continuous stems over the corresponding lengths. Preserve the observed broken stroke with the existing dashed arrow; no new mathematical property is assigned to it.',
    'Proof3.3(c), top diagram, H-prime→H',witness=126)
id='ASTRA-I-MODULEPLURAL-111';reason='The proof names E as a complex whose degree terms are left A_U-Modules; the printed singular ending Module is the grammatical slip in complexe de A_U-Module. The correction adds only the missing plural s, keeping every coefficient, side convention and mathematical statement.'
r.own_finding(id,111,'un complexe de A_U-Module à gauche',r'un complexe de \(A_U\)-Module à gauche','Current only: Module→Modules',reason,'Proof2.16, definition of E',kind='misprint_in_print')
r.patch(111,'current',r'un complexe de \(A_U\)-Module à gauche',r'un complexe de \(A_U\)-Modules à gauche',id,reason)
for p,count in[(112,7),(113,8),(114,4),(115,9)]:
    id=f'ASTRA-I-C-{p:03d}';reason='Every occurrence represented by this command is a typed C with a short independent underline. Primes and subscripts stay outside its rule.'
    r.own_finding(id,p,'Underlined typed C',r'\mathcal C',r'\underline{C}',reason,'All category C occurrences')
    r.patch(p,'both',r'\mathcal C',r'\underline{C}',id,reason,count)
site_positions={111:[i for i in range(1,21) if i!=5],112:[1,2,3,4]}
for p,positions in site_positions.items():
    id=f'ASTRA-I-SITE-{p:03d}';reason='The selected S occurrences name the site or its categories and have short independent rules. The final object X=S on111 and the fiber/object S occurrences on112–115 are plain as printed. Both base subscripts of the tensor-product fiber products on111 are underlined and are braced in TeX to contain the whole glyph command.'
    r.own_finding(id,p,'Underlined site S at the recorded positions','Plain S commands',f'Underline S occurrences{positions}',reason,'All site and object S occurrences',witness=122 if p==111 else None)
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        matches=list(re.finditer(r'(?<![A-Za-z\\])S(?![A-Za-z])',old));assert len(matches)==(20 if p==111 else 7)
        new=old
        for i,m in reversed(list(enumerate(matches,1))):
            if i in positions:new=new[:m.start()]+r'\underline{S}'+new[m.end():]
        new=new.replace(r'\times_\underline{S}',r'\times_{\underline{S}}')
        r.patch(p,layer,old,new,id,reason)
r.finding(batch,1,'Site S underlined; final-object and fiber S plain',
    'The complete pages give explicit occurrence maps on111 and112. On113 U above S and U=S refer to the plain object. The C_S fiber subscripts on112–115 remain plain; only their category C is underlined.',
    'All five pages, site/object convention',verdict='not applied and now applied',change='Apply the exact S maps on111–112 and preserve the inspected plain object/fiber occurrences.')
for p,letters in[(111,['a','b']),(112,['a']),(113,['b','c']),(115,['a','b'])]:
    id=f'ASTRA-I-ITEMS-{p:03d}';reason='The printed item letters are ordinary typed characters without bold strokes or underlines. Retain the separately marked statement prose and its heading.'
    r.own_finding(id,p,'Plain item letters',r'\textbf item labels','Plain item labels',reason,'All listed item labels',kind='font')
    for letter in letters:r.patch(p,'both',r'\textbf{'+letter+')}',letter+')',id,reason)
id='ASTRA-I-PARANUM-112';reason='The paragraph number3.0 is plain typed text, separate from the accepted statement-heading typography.'
r.own_finding(id,112,'Plain3.0.',r'\textbf{3.0.}','3.0.',reason,'Paragraph3.0',kind='font')
r.patch(112,'both',r'\textbf{3.0.}','3.0.',id,reason)
id='ASTRA-I-NOTE-112';reason='Both call and bottom note use the printed parenthesized asterisk. The note body is plain and remains outside the definition’s word rules.'
body="Nous introduisons cette notion ici à titre d'intermédiaire technique, la seule notion à retenir est celle de cohérence."
note=r'\SGAAuthorFootnote{*}{'+body+'}'
r.own_finding(id,112,'(*) author note, plain body',r'\footnote with automatic number',r'\SGAAuthorFootnote{*}',reason,'Definition3.1 call and bottom author note',kind='font')
r.patch(112,'both',r'\footnote{'+body+'}',note,id,reason)
for p,count in[(111,8),(112,4),(113,6),(115,13)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The inspected word groups are upright and underlined. Formulas retain their independent rules, and the definition’s plain terms remain outside the spans. Author-note text and the explicitly unruled references/abbreviation are protected.'
    r.own_finding(id,p,'Upright underlined word groups',r'\emph spans',r'\uline word groups',reason,'All emphasis spans')
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        plain=[note,'(1.2)'] if p==112 else ['i.e.'] if p==115 else []
        new,n=underline_words(old,plain);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)
for p,b,e,w in[(111,'le foncteur dérivé du produit tensoriel','D^−(S)_coh .',122),(112,'Exercice2.16.2. Soient S un topos','0→F→G→H; note(*) se termine par cohérence.',None),(113,'une suite exacte de C_S','G→H, bottom of the square',None),(114,'où les flèches horizontales','avec',None),(115,'F-prime∈ob C_0','et H^n(F) de type fini.',126)]:
    r.page(p,b,e,'Complete text, indices, degree bounds, all diagrams, punctuation and printed page boundary personally compared. The exact thin-stroke checks, grammatical correction and typography maps are recorded separately.',witness=w)
r.commit()
