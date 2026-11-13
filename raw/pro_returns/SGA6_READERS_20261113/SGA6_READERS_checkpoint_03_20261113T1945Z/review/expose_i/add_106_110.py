#!/usr/bin/env python3
import re,json
from review_helpers import Review,ROOT,HERE,underline_words
r=Review();batch='106_110'
observations={
1:('Unmatched closing parenthesis after F-prime≤n','The reference(2.10.b)) is already closed. The extra parenthesis after F-prime≤n has no opener. Keep it diplomatically and retain its existing current deletion.','Proof2.12 second line'),
2:('Proposition2.13 opening prose underlined by word groups','The text from Soit through et soit has the recorded rules. The references and mathematical expressions have their independent typography.','Proposition2.13 opening'),
3:('The cartesian-functor assertion is underlined by word groups','The rules cover the stated prose; the category and site letters have separate rules. The colon is after the final group.','Proposition2.13 second paragraph'),
5:('The last choice of * is the crossed-loop empty-set sign','The sign has a long slash through a loop and no upright b stem. The printed parameter choice names the unbounded derived category alongside + and −; preserve the crossed-loop glyph as varnothing.','Proposition2.13 parameter choices'),
6:('Statement(i) prose underlined','The words si, est, pseudo-cohérent and resp. have rules; the item label is plain.','Proposition2.13(i)'),
7:('C_{0S} with adjacent subscripts','There is no comma inside the subscript; the following comma belongs outside the membership formula.','Proposition2.13(i) membership'),
8:('No punctuation after the closing parenthesis of(i)','The line ends at the parenthesis, before the next item. The attached deletion of the added semicolon is correct.','Proposition2.13(i) end'),
9:('Statement(ii) prose underlined','The label is plain and the acyclicity word groups are underlined. The two bounds are >0 and >b.','Proposition2.13(ii)'),
10:('The conclusion uses the printed sup(m+b,n+a) and prose rules','All terms, the object identity S-prime=f^(−1)(S), both relative pseudo-coherence clauses and the final >n+b agree with the image.','Proposition2.13 conclusion'),
11:('The first parenthesis rel. à C_0 is plain; the final one is underlined','The exception in the first parenthesis is visible. Retain the existing split spans rather than extending the rule across that parenthesis.','Proposition2.13 En particulier paragraph'),
12:('Montrons d’abord que si, without comma after que','No mark is printed between que and si.','First line of proof2.13'),
14:('Page107 begins on a F=F^p[-p]','The previous page ends Si N=1,. The whole formula and its introductory on a belong on107.','Page107 first line'),
15:('Comma to the right of u(F), first triangle','All three arrows and the +1 edge agree; the comma is on the lower row.','First triangle on107'),
16:('Comma to the right of u(F), second triangle','The lower-row comma is present after the second triangle as well.','Second triangle on107'),
17:('Alors underlined at the top of108; colon outside','The actual location is the first line of108 after the marker repair. Retain the separated span and the plain colon.','Page108 first line'),
18:('Page108 begins Alors :','Page107 ends the opening hypothesis of Corollary2.14. The attached boundary correctly precedes Alors.','Page108 first line and preceding page ending'),
19:('Plain item label(i)','The first rule belongs to the category C_1 and to est localement, not to the item label.','Corollary2.14(i)'),
20:('Plain item label(ii)','The prose rule begins at Soient after the label.','Corollary2.14(ii)'),
21:('C_{1S}, no internal comma','The two subscripts are adjacent in the membership formula.','Proof2.14(i) first membership'),
22:('C_{0S}, no internal comma','The subscripts0 and S are adjacent after E-prime.','Proof2.14(i) second membership'),
24:('The two defined pseudo-coherence terms are underlined','Both the n-qualified term and the unqualified term have rules. The first n belongs to the rule, recorded below; the parenthetic resp. stays plain.','Example2.15 defined terms'),
25:('Typed hyphens in the compound indices','The source uses joining hyphens in n-C_0-coh, C_0-coh and n-coh. The attached text hyphens retain the labels without subtraction spacing.','Example2.15 three compound indices'),
26:('Plain item label(i)','The first independent rule is under the site S and the first word group.','Lemma2.15.1(i)'),
27:('The first parenthesis à gauche is plain','The witness clearly leaves this parenthesis outside the statement rule, although the later conclusion underlines its own à gauche. The attached split is faithful.','Lemma2.15.1(i), before projectifs'),
28:('Plain item label(ii)','The site letter in the pair has its independent rule; the item label does not.','Lemma2.15.1(ii)'),
29:('First Hom underlined, second Hom plain','The displayed arrow sends the stalk of the sheaf Hom to the Hom of the two stalks. The print gives the first operator its separate underline, exactly as the attached source.','Page110 top display'),
30:('Tilde over a single line, without arrowhead','The stalk isomorphism is printed as simeq, not a directed arrow.','Page110 first paragraph, stalks'),
31:('Tilde over a single line, without arrowhead','The restriction isomorphism also has no arrowhead. The restriction U is on the baseline.','Page110 first paragraph, restrictions'),
32:('Supposons(ii), Soit with a comma and capital S','Both scans show the comma tail. Retain that reading diplomatically and the existing full stop in current, which joins the two independent sentences correctly.','Page110 second paragraph opening'),
33:('End operator underlined, double-struck D subscript unruled','The operator has a short independent rule. Neither the argument D^n nor its subscript D inherits that rule.','Universal endomorphism functor'),
35:('Plain arrow i:P_n→M_n','The inclusion is drawn with an ordinary arrow and no hook. The attached source reproduces that arrow.','Universal projector subscheme'),
36:('One S in the factorization, with no added soit','The phrase goes directly from en to the displayed inline factorization S→P_n→M_n. There is no second S or intervening soit.','End of universal-projector paragraph'),
37:('Corollary2.16 opening word groups underlined','The underlines cover the prose through et before the tensor-product display. The functor letters, ring letters and site letters have separately observed marks.','Corollary2.16 before final display'),
}
for n,(printed,reason,region) in observations.items():
    r.finding(batch,n,printed,reason,region,witness=120 if n in[24,25,26,27,28] else 121 if n in[32,33] else None,actual_page=108 if n==17 else None)
r.finding(batch,4,'The u-functor formula is in the running sentence',
    'The formula occupies the start of a text line continued by un foncteur cartésien. Keep its attached inline setting as layout only; the empty-set glyph is adjudicated separately.',
    'Proposition2.13 functor formula',verdict='amended',change='Retain inline formula; classify the display/inline difference as layout.')
id=r.finding(batch,23,'Unmatched closing parenthesis after the final C_1',
    'The full sentence contains no opening parenthesis for this final closer: both numbered references have already closed. Remove this single stray character in current, preserving all parameter substitutions and the diplomatic reading.',
    'Proof2.14(ii) last character before full stop',verdict='not applied and now applied',change='Current only: remove the unmatched closing parenthesis.')
r.patch(108,'current',r'remplacées respectivement par \(\mathcal C_0\) et \(\mathcal C_1\)).',r'remplacées respectivement par \(\mathcal C_0\) et \(\mathcal C_1\).',id,'All preceding reference parentheses are already balanced.')
id=r.finding(batch,34,'Capital U_n defines the universal matrix; three later uses print u_n',
    'The witness confirms the capital at the definition. The matrix(T_ij) determines one universal endomorphism of O_{M_n}^n. The morphism s is defined by s*(u_n)=p, and s=i∘s-prime gives the exact same map p=s-prime* i*(u_n). All three lowercase uses therefore refer to the uniquely defined matrix endomorphism; current names it u_n at its definition as well.',
    'Definition of the universal endomorphism',verdict='not applied and now applied',change='Current only: U_n→u_n at its definition.',witness=121)
r.patch(110,'current',r"l'endomorphisme \(U_n\)",r"l'endomorphisme \(u_n\)",id,'The pullback identity and explicit matrix identify this endomorphism with the three later u_n occurrences.')
nil_id='ASTRA-I-RADICAL-109'
nil_reason='Both scans print the nilpotence-only alternative. It is an example offered for the already stated hypothesis that finite projective stalk modules are free. For A=k×k, J=rad(A)=0 is nilpotent, and P=k×0 is the image of the idempotent e(a,b)=(a,0). Tensoring along the two projections A→k gives dimensions(1,0) for P and(r,r) for A^r, so P is not free. The valid preceding residue-division-ring example remains: for a finite projective P over the stated A with D=A/J a division ring, lift a D-basis of P/JP to define f:A^r→P. Nakayama makes f surjective; projectivity splits A^r=P⊕K. Modulo J, D^r=(P/JP)⊕(K/JK) with the first summand already of dimension r, so K/JK=0. The finitely generated direct summand K is zero by Nakayama, hence f is an isomorphism. The cited Bourbaki II§3no.2, cor.2 of prop.5 keeps A/J a field as a standing assumption; finite presentation and nilpotence are its additional alternatives. Finite projectivity already gives finite presentation here. Delete the unsupported nilpotence disjunct from the example, without changing the lemma’s actual hypothesis. External source particulars are recorded in external_bourbaki_109.json.'
r.own_finding(nil_id,109,'un corps ou si radical(A_s) est nilpotent',r'un corps ou si \(\operatorname{radical}(A_s)\) est nilpotent','Current only: delete the nilpotence-only disjunct',nil_reason,'Lemma2.15.1(i), offered algebraic example',kind='misprint_in_print',witness=120)
r.patch(109,'current',r'un corps ou si \(\operatorname{radical}(A_s)\) est nilpotent.',r'un corps.',nil_id,nil_reason)
id='ASTRA-I-DEFINEDN-109';reason='The rule under the first defined term begins under its n and continues through pseudo-cohérent; the witness clearly separates the unruled parenthetic resp. from the second defined term.'
r.own_finding(id,109,'Initial n underlined within the first defined term',r'\emph{\(n\)-pseudo-cohérent}',r'Underline n independently while retaining its adjoining word rule',reason,'Example2.15 first defined term',witness=120)
r.patch(109,'both',r'\emph{\(n\)-pseudo-cohérent}',r'\emph{\(\underline{n}\)-pseudo-cohérent}',id,reason)
for p,count in[(106,21),(107,9),(108,29),(109,9)]:
    id=f'ASTRA-I-C-{p:03d}';reason='All occurrences represented by this category command are typed C with individual short rules in the complete image; primes and indices remain outside the rule.'
    r.own_finding(id,p,'Underlined typed category C',r'\mathcal C',r'\underline{C}',reason,'Every category C occurrence')
    r.patch(p,'both',r'\mathcal C',r'\underline{C}',id,reason,count)
id='ASTRA-I-O-110';reason='The structure sheaves O_T and O_{M_n} are plain typed O with short rules. The native witness confirms the non-script outlines and the separate underlines.'
r.own_finding(id,110,'Underlined plain O in both structure-sheaf occurrences',r'\mathcal O',r'\underline{O}',reason,'Universal matrix paragraph',witness=121)
r.patch(110,'both',r'\mathcal O',r'\underline{O}',id,reason,2)
id='ASTRA-I-RADICALRULE-109';reason='The word radical has its own short rule in both displayed inline operators. The argument A_s and the slash do not inherit that rule.'
r.own_finding(id,109,'Both radical operators underlined',r'\operatorname{radical}',r'\underline{\operatorname{radical}}',reason,'Lemma2.15.1(i), both radical operators',witness=120)
for layer,count in [('diplomatic',2),('current',1)]:
    r.patch(109,layer,r'\operatorname{radical}',r'\underline{\operatorname{radical}}',id,reason,count)
site_positions={106:[1,2,3,4,5,6,7,8,9,11],107:[1],108:[2,8,9,10,11,12,13,14],109:[1,3,7,8,9,10,11,12,13,14,15],110:[1,2,3,4,5,8,9,10,11,12,13,14,15,16,17]}
site_counts={106:19,107:1,108:14,109:15,110:17}
for p,positions in site_positions.items():
    id=f'ASTRA-I-SITE-{p:03d}';reason='The specified occurrences name the site/topos or its fibered category and have visible short S rules. Object S, the final-object fiber subscript and the two global-section arguments on110 stay plain where printed. On108 the witness resolves the faint S rule inside D(S,A). On109 the explicit equality D(C_S)=D(_A S) uses the plain final object, while the surrounding fibered-category notations use the underlined site.'
    r.own_finding(id,p,'Underlined site S at the recorded occurrences',r'Plain S commands',f'Underline S positions{positions}; preserve all others',reason,'Every S inspected with its local definition',witness=119 if p==108 else 120 if p==109 else None)
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        matches=list(re.finditer(r'(?<![A-Za-z\\])S(?![A-Za-z])',old));assert len(matches)==site_counts[p],(p,len(matches))
        new=old
        for i,m in reversed(list(enumerate(matches,1))):
            if i in positions:new=new[:m.start()]+r'\underline{S}'+new[m.end():]
        r.patch(p,layer,old,new,id,reason)
r.finding(batch,13,'Site S underlined, object S plain at the inspected occurrences',
    'Complete pages106–110 and native witnesses119–121 were read. The occurrence maps in ASTRA-I-SITE-106 through110 implement the printed distinction. In particular,109 explicitly names the final object S and then writes its fiber D(C_S) using the plain letter, while the surrounding category over the site uses underlined S.',
    'All five pages, site/object notation',verdict='not applied and now applied',change='Apply the five explicit occurrence maps; no global S substitution.')
id='ASTRA-I-NOTE-110';reason='The call and the footnote both use a baseline parenthesized asterisk. Preserve this author note with its explicit printed label, independently of other note counters.'
r.own_finding(id,110,'(*) author-note call and label',r'\footnote with automatic numbering',r'\SGAAuthorFootnote{*}',reason,'First paragraph and bottom note',kind='font')
old=r'\footnote{i.e. tel que \(\underline{S}_{/U}\).}'
# The full body contains the words se factorise à travers.
old=r'\footnote{i.e. tel que \(s\) se factorise à travers \(\underline{S}_{/U}\).}'
new=r'\SGAAuthorFootnote{*}{i.e. tel que \(s\) se factorise à travers \(\underline{S}_{/U}\).}'
r.patch(110,'both',old,new,id,reason)
plain={106:['(2.0)','([G] I 1.4)','i.e.'],107:[],108:['(1.2)'],109:['(SGA 4 IV 6.4)',r'(BOURBAKI Alg. Comm. chap. II \S~3 n\textsuperscript{o}~2 cor.~2 de la prop. 5)','[1]'],110:[]}
for p,count in[(106,8),(107,1),(108,4),(109,8),(110,1)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The statement words are upright and underlined. Inline formulas retain their independent letter/operator rules. The specifically inspected reference strings and i.e. are left outside the word rules, and the source’s plain parenthetical exceptions remain plain.'
    r.own_finding(id,p,'Upright underlined statement word groups',r'\emph spans',r'\uline groups with separately observed exceptions',reason,'All existing emphasis spans')
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        new,n=underline_words(old,plain[p]);assert n==count
        r.patch(p,layer,old,new,id,reason)
for p,b,e,w in[(106,'donc H^n(F′≤n)','Si N=1,',None),(107,'on a F=F^p[-p]','est C_0-pseudo-cohérent.',None),(108,'Alors :','ou D(_A S) (pour',119),(109,"suggérer qu’il s’agit de A-Modules à gauche)",'la flèche canonique',120),(110,'Hom(E,F)_s→Hom(E_s,F_s)','D^−(_A′ S′); note(*) se factorise à travers S_/U.',121)]:
    r.page(p,b,e,'All text, operators, primes, bounds, diagrams, punctuation and author-note matter compared. Exact source-specific corrections and typography maps are recorded separately.',witness=w)
r.commit()
(HERE/'external_bourbaki_109.json').write_text(json.dumps({
 'purpose':'Bibliographic control of the algebraic example in printed SGA6 I2.15.1(i), folio109',
 'original_reference':'N. Bourbaki, Algèbre commutative, chapitreII, §3, no.2, corollaire2 de la proposition5',
 'publisher_record':'https://link.springer.com/book/10.1007/978-3-540-33976-2',
 'consulted_primary_text_mirror':'https://pdfcoffee.com/commutative-algebra-bourbaki-pdf-free.html',
 'text_identification':'Published 1972 English translation, Commutative Algebra, chapterII §3.2; corollary2 following proposition5.',
 'verified_content_summary':'The residue quotient by the Jacobson radical is assumed to be a division ring. Finite presentation of the module and nilpotence of the radical are additional alternatives. The cited corollary does not make nilpotence a substitute for the residue-division-ring assumption.',
 'proof_record':nil_id,
 'method':'The original SGA6 words were read in mainPDF123 and witnessDjVu120. The bibliographic text was separately read in the published-book mirror; the mathematical decision also has the explicit projection counterexample and basis-lifting isomorphism recorded in the finding.'
},ensure_ascii=False,indent=2)+'\n')
