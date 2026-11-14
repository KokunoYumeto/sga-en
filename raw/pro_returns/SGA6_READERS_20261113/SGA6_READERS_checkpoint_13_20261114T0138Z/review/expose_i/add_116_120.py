#!/usr/bin/env python3
import re,json
from review_helpers import Review,ROOT,HERE,underline_words
r=Review();batch='116_120'
observations={
1:('Closing statement3.5 word groups underlined','The continuation starts En particulier and ends with the quantifier for every n. The mathematical expressions remain outside the word rules.','First two lines of116'),
2:('Proposition3.7(a) prose word groups underlined','The rule starts at Soit; i.e. is plain. The morphism is flat on the right and the displayed functor is f*=A-prime⊗_A with a baseline placeholder point, subsequently resolved and patched in ASTRA-I-DOT-116.','Proposition3.7(a) before display'),
4:('Typed hyphen on each of the three list items','All three bullets are short typed hyphens. Retain the existing single-hyphen label as a typography decision, without creating a corrected/diplomatic variant.','Examples3.6 list'),
6:('Continuation3.7(a) word groups underlined','The first sentence of117 finishes the assertion begun on116. The source preserves the isomorphism claim and the pseudo-coherence qualifier.','Page117 opening'),
7:('Statement3.7(b) starts underlined at Supposons','The opening and closing changes jointly delimit the full statement. The operator underlines and the unruled et between cohomology formulas are recorded independently.','Proposition3.7(b) opening'),
8:('Statement3.7(b) ends after Ext^i(F,G)','The word rules end at de before the separately underlined Ext operator. The following Preuve is a new paragraph.','Proposition3.7(b) ending'),
9:('Both H operators underlined; et between them plain','The witness shows two short rules beneath H alone. The connecting et has no rule; the separate proof occurrence H^i(G)=0 is plain. Preserve all three observations.','Proposition3.7(b) cohomology expressions'),
10:('Ext operator underlined','Only Ext has its own rule; the superscript, arguments and final period remain separate.','Proposition3.7(b) last formula'),
11:('Three Hom operators underlined; final R double-struck','The display contains exactly two ordinary sheaf-Hom terms and one derived term. Each Hom has a short rule, and the R of the last term has the doubled stem.','Proof3.7(a) first display'),
12:('Double-struck R and underlined Hom in the definition of T','The witness shows the two stem strokes and the separate Hom rule before the baseline placeholder.','Definition of T'),
13:('Double-struck R and underlined Hom in the definition of T-prime','The printed operator form agrees with the definition of T and the last term of the preceding display.','Definition of T-prime'),
14:('Baseline full-stop placeholder in Hom(.,G)','The witness places the dot level with the stop of resp., below the height of a multiplication dot. Retain the literal point.','Definition of T, first argument'),
15:('Baseline full-stop placeholder after f*','The dot is at the same baseline as the first placeholder and the adjoining punctuation. Retain the literal point after f*.','Definition of T-prime, first argument'),
16:('Double-struck R with independently underlined Hom','The witness resolves the doubled stem and the short rule beneath Hom.','Remark3.7.1'),
17:('Double-struck L before f*','The witness shows a second vertical stem inside L, distinct from the plain L used above tensor signs.','Remark3.7.1 final functor'),
18:('Tilde over a line, without an arrowhead','The stalk isomorphism sign in the statement is simeq. The directed isomorphisms in the proof have visible arrowheads.','Corollary3.7.2, E_s and F_s'),
19:('Tilde over a line, without an arrowhead','The restriction isomorphism has the same unheaded sign as the stalk isomorphism. The vertical bars and U remain baseline restrictions.','Corollary3.7.2, E|U and F|U'),
20:('The two sheaf-Hom operators are underlined, the two stalk Hom operators plain','The display passes from the stalk of each sheaf Hom to Hom between stalks. The independent rules occur only on the left sides of the two arrows.','Proof3.7.2 display'),
21:('Both sheaf-Hom operators underlined','The two source sheaves of the local sections have short Hom rules, with all arguments outside.','Proof3.7.2 local sections'),
23:('Soit underlined before the diagram','The word opens Corollary4.2; the continuation is at the top of120. The first diagram has only E→F and P→F.','Page119 final corollary'),
24:('Author-note call before the label’s full stop','The exact order is Lemme4.1, parenthesized raised star, then the stop. The attached punctuation placement is correct; the star label is restored separately.','Lemma4.1 label'),
25:('Corollary4.2 continuation starts with underlined un diagramme','The whole opening word-group sequence continues until the displayed diagram. The object and category notation has independent rules.','Top of120'),
26:('Word rule ends after telle que le diagramme','The rule precedes the diagram and does not run through its arrows or labels.','Corollary4.2 before diagram'),
27:('No comma after C(C_X)','The phrase continues directly with telle que. The attached deletion of the extra comma matches the print.','Corollary4.2 before diagram'),
28:('Diagonal u-arrow from P_X to E_X','The arrowhead is at E_X, and the preceding text explicitly gives u:P_X→E_X. The horizontal f_X then composes with u to give v_X in the homotopy category.','Corollary4.2 triangle'),
29:('Concluding word groups of4.2 underlined','The rules cover soit commutatif dans and est un raffinement de. The category formula and object S retain their separate forms.','Corollary4.2 after diagram'),
30:('Qis/F underlined inside its parentheses','The rule includes the slash and F but excludes the parentheses. The following fiber (Qis/F_X)^circle remains plain.','Scholium4.4 category'),
31:('Slash-S lowered after the underlined site S','The first S names the base site, with the whole /S as its lower index. The indexed S is the already fixed plain object.','Scholium4.4 base of the fibered category'),
32:('Page120 ends en disant que,;121 starts si F est','The complete120 image and the top of121 show the attached marker at the exact beginning si F est. The first line continues strictement parfait and the locally cofinal identity arrow.','Boundary120/121'),
}
for n,(printed,reason,region) in observations.items():
    r.finding(batch,n,printed,reason,region,witness=128 if 9<=n<=15 else 129 if 16<=n<=19 else None)
r.finding(batch,3,'Derived R in both terms, with underlined Hom',
    'Both scans give short independent Hom rules. The right R has a clear doubled stem. The left stem is heavily inked and filled in both scans; its width and contour agree with the neighboring derived R letters on117, and the map is the derived-Hom pullback map, with the same right-derived operator on both sides. Retain the double-struck reconstruction and record the filled stroke explicitly.',
    'Proposition3.7(a) final display',witness=127)
id=r.finding(batch,22,'D’après(2.22 a))',
    'The numbered section2 ends at2.16.2 before3.0; the required statement is3.7(a), immediately preceding this corollary. Apply its map s*RHom(E,F)→RHom(s*E,s*F) to the point morphism s. The inverse-image functor at a point is exact, E is pseudo-coherent by membership in D^b_coh, and F is bounded below. Thus3.7(a) gives this isomorphism; taking degree-zero cohomology gives exactly Hom(E,F)_s→Hom(E_s,F_s), and exchanging E,F gives the second displayed map.',
    'Proof3.7.2 citation',verdict='not applied and now applied',change='Current only: reference(2.22 a))→(3.7 a)).',witness=129)
r.patch(118,'current',"D'après (2.22 a)), on a","D'après (3.7 a)), on a",id,'The actual preceding proposition supplies both displayed stalk-Hom isomorphisms via the point morphism and H^0.')
id='ASTRA-I-SGA4-118';reason='The main scan and native witness print SGAA. The cited definition is present in SGA4, ExposéVIII,7.8: a point is a morphism from the punctual topos, described by a fiber functor preserving arbitrary colimits and finite limits. The external primary-text edition was checked at the exact numbered paragraph; the bibliographic record is external_sga4_118.json. Correct only the mistaken volume letter and its spacing, retaining VIII7.8.'
r.own_finding(id,118,'SGAA VIII7.8','SGAA VIII 7.8','Current only: SGA 4 VIII 7.8',reason,'Corollary3.7.2 reference defining a point',kind='misprint_in_print',witness=129)
r.patch(118,'current','SGAA VIII 7.8','SGA 4 VIII 7.8',id,reason)
for p,count in[(116,3),(119,9),(120,13)]:
    id=f'ASTRA-I-C-{p:03d}';reason='Each occurrence represented by this command has a short rule under a typed C. Its indices and primes are outside that rule.'
    r.own_finding(id,p,'Underlined typed category C',r'\mathcal C',r'\underline{C}',reason,'All category C occurrences')
    r.patch(p,'both',r'\mathcal C',r'\underline{C}',id,reason,count)
id='ASTRA-I-O-116';reason='Both structure sheaves in the scheme and complex-analytic examples use a plain typed O with a short independent rule. The base S is the plain underlying space.'
r.own_finding(id,116,'Two plain underlined structure-sheaf O',r'\mathcal O',r'\underline{O}',reason,'Examples3.6, second and third bullets')
r.patch(116,'both',r'\mathcal O',r'\underline{O}',id,reason,2)
site_positions={116:[1,2,3,6,9,10,11],118:[1,2,4],119:[1,3,4,5],120:[13]}
site_counts={116:13,118:4,119:6,120:15}
for p,positions in site_positions.items():
    id=f'ASTRA-I-SITE-{p:03d}';reason='The selected occurrences have short S rules. The explicitly named objects and underlying schemes/spaces remain plain. The witness confirms that the derived-category arguments in3.7(a),(b) and3.7.2 are plain S; their adjacent topos names are underlined. The section4 definition explicitly distinguishes the site from its fixed object, and the map preserves that distinction.'
    r.own_finding(id,p,'Underlined S at the exact selected occurrences','Plain S commands',f'Underline S positions{positions}; preserve all others',reason,'All site/object S occurrences',witness=127 if p==116 else 129 if p==118 else None)
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        matches=list(re.finditer(r'(?<![A-Za-z\\])S(?![A-Za-z])',old));assert len(matches)==site_counts[p]
        new=old
        for i,m in reversed(list(enumerate(matches,1))):
            if i in positions:new=new[:m.start()]+r'\underline{S}'+new[m.end():]
        r.patch(p,layer,old,new,id,reason)
r.finding(batch,5,'Site S rules at the recorded occurrences; derived-category and object S plain where printed',
    'Complete pages116–120 were compared, with witness127–129 resolving the plain S arguments of D(_AS), D^±(S) and D^b(_AS). The maps on116,118,119,120 restore the visible rules. Both S occurrences on117 and all plain object/fiber subscripts remain unchanged.',
    'All five pages, site/object notation',verdict='not applied and now applied',change='Apply four exact occurrence maps; retain the inspected plain occurrences.',witness=128)
for p,letter in[(116,'a'),(117,'b')]:
    id=f'ASTRA-I-ITEMS-{p:03d}';reason='The printed item letter is plain and outside the word rules.'
    r.own_finding(id,p,'Plain item letter',r'\textbf{'+letter+')}','Plain item label',reason,'Proposition3.7 item label',kind='font')
    r.patch(p,'both',r'\textbf{'+letter+')}',letter+')',id,reason)
id='ASTRA-I-PARANUM-119';reason='The paragraph number4.0 is ordinary typed text, separate from the section title and lemma heading.'
r.own_finding(id,119,'Plain4.0.',r'\textbf{4.0.}','4.0.',reason,'Paragraph4.0',kind='font')
r.patch(119,'both',r'\textbf{4.0.}','4.0.',id,reason)
for p,label,body,reason in[
 (116,'*','Conformément aux nouvelles conventions, nous dirons «~schéma~» pour «~préschéma~», et «~schéma séparé~» pour «~schéma~».','The call and bottom label use a central star in baseline parentheses. Preserve the entire author note explaining the scheme terminology.'),
 (119,'raisedstar','Ce lemme a été communiqué au rédacteur par D. Ferrand.','The star sits high inside baseline parentheses at both the label and bottom note. Preserve the exact attribution to D. Ferrand and the full stop after the call.')]:
    id=f'ASTRA-I-NOTE-{p:03d}'
    r.own_finding(id,p,'Printed parenthesized-star author note',r'Automatically numbered \footnote',r'Explicit SGAAuthorFootnote label '+label,reason,'Author-note call and note body',kind='font')
    r.patch(p,'both',r'\footnote{'+body+'}',r'\SGAAuthorFootnote{'+label+'}{'+body+'}',id,reason)
plain_et=r'\(\underline{\Ho}^i(F)\) et \(\underline{\Ho}^i(G)\)'
for p,count in[(116,3),(117,3),(118,2),(119,3),(120,5)]:
    id=f'ASTRA-I-TERMS-{p:03d}';reason='The inspected prose groups are upright and underlined, with inline formulas separately marked. Preserve the plain abbreviation i.e., the et between the two underlined-H formulas on117, and the unruled numbered references.'
    r.own_finding(id,p,'Upright underlined word groups',r'\emph spans',r'\uline groups with exact plain exceptions',reason,'All emphasis spans')
    for layer in ['diplomatic','current']:
        old=(ROOT/f'build/page_packets/{p}/{layer}.tex').read_text()
        for patch in r.patches:
            if patch['page']==p and patch['layer'] in['both',layer]:old=old.replace(patch['old'],patch['new'])
        plain={116:['i.e.'],117:[plain_et],118:['(SGAA VIII 7.8)','(SGA 4 VIII 7.8)'],119:['(2.1)'],120:[]}[p]
        new,n=underline_words(old,plain);assert n==count,(p,n,count)
        r.patch(p,layer,old,new,id,reason)
for p,b,e,w in[(116,'En particulier, pour que F','RHom(f*(F),f*(G)); note(*) termine par schéma.',127),(117,'Celle-ci est un isomorphisme','et TF-double-prime et T-primeF-double-prime sont',128),(118,'acycliques en degré≤a−n','au-dessus de U, cqfd.',129),(119,'4. Complexes parfaits','diagram E→F←P; note de D. Ferrand.',None),(120,'un diagramme de C(C_S)','en disant que,',None)]:
    r.page(p,b,e,'All words, bounds, operators, morphisms, diagram arrows, punctuation, author notes and page boundaries personally compared. Witness details and the two current reference corrections are recorded separately.',witness=w)
r.commit()
(HERE/'external_sga4_118.json').write_text(json.dumps({
 'purpose':'Verify the printed reference SGAA VIII7.8 in SGA6 I3.7.2, folio118',
 'source_title':'M. Artin, A. Grothendieck, J.-L. Verdier, Théorie des topos et cohomologie étale des schémas, SGA4, tome2',
 'consulted_edition':'F. Orgogozo digital transcription, version2015-04-27, ExposéVIII paragraph7.8, printed page226, PDF page230',
 'primary_text_url':'https://www.cmls.polytechnique.fr/perso/orgogozo/SGA4/tomes/tome2.pdf',
 'verified_content_summary':'Paragraph7.8 defines a point of a topos through a morphism from the punctual topos, equivalently its inverse-image fiber functor preserving arbitrary colimits and finite limits.',
 'scan_evidence':'scan/SGA6_scan_360dpi.pdf#page=132; scan/SGA6_witness_300dpi.djvu#page=129',
 'decision':'ASTRA-I-SGA4-118; current SGAA→SGA4, with VIII7.8 retained',
 'method':'The SGA6 printed glyphs were read directly in both scans. The external numbered primary-text paragraph was read separately for the bibliographic identification.'
},ensure_ascii=False,indent=2)+'\n')
