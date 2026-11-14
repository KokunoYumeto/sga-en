#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=323
r.finding('321_325',15,'The first paragraph prints pré- -anneau with a blank between the two hyphens.',
 'The native top crop resolves the clear unfilled interval. The explicit locator2.5.a) identifies the structure λ^i(n)=binom(n,i) on the integer ring, and the surrounding sentence identifies its defining relations2.4.2. These exact operations supply the missing λ in the corrected reading; retain the blank diplomatically.',
 'first paragraph, pré- -anneau',witness=334)
r.finding('321_325',16,'The Z before(2.5.a)) is an ordinary typed letter with one diagonal; the later underlined Z in H^0 is visibly reinforced/doubled.',
 'The native top crop directly compares the two local glyphs. The locator2.5.a) identifies the integer ring by the identity n↦n, preserving1, addition, multiplication and λ^i(n)=binom(n,i). That exact identification requires no extra stroke in this occurrence’s letter. Retain the observed plain Z in both forms, and amend the inherited classification as a mathematical misprint; the two missing λ symbols are separately established from the cited operations.',
 'first paragraph, integer-ring Z',verdict='diplomatic font confirmed; corrected font amended to the same observed form',change={'diplomatic':r'Z','current':r'Z'},witness=334)
for row in r.decisions:
 if row.get('source_id')=='check/findings/findings_321_325.json#16' or row.get('related_finding')=='check/findings/findings_321_325.json#16':
  row['kind']='font'
  row['classification']='observed font variation; no mathematical emendation'
r.patch(p,'current',r'\(\mathbb Z\) (2.5.a))',r'\(Z\) (2.5.a))','check/findings/findings_321_325.json#16','Preserve the directly observed plain Z while retaining its exact integer-ring identification.')
r.finding('321_325',17,'The same line prints est un -anneau with a blank before the hyphen.',
 'The native top crop resolves the blank. The immediately cited2.5.a) proves that its prescribed operations satisfy2.4.2, exactly the λ-anneau assertion invoked here. Retain the blank diplomatically and the attached λ currently.',
 'first paragraph, est un -anneau',witness=334)
r.finding('321_325',18,'The definition underlines On appelle; un anneau vérifiant les conditions; et; muni de la structure de; anneau définie par.',
 'The native top crop resolves five lexical groups. The defined words anneau binômial, references2.6.i),ii),2.6.1, the λ sign and its following hyphen remain plain. The statement-label word has its separate rule, covered by the accepted bold-label convention.',
 'Définition2.7 statement',verdict='not applied and now applied',change='Restore the five inspected lexical rules only.',witness=334)
old=r'On appelle anneau binômial un anneau vérifiant les conditions 2.6.i) et ii), muni de la structure de \(\lambda\)-anneau définie par 2.6.1.'
new=r'\uline{On appelle} anneau binômial \uline{un anneau vérifiant les conditions} 2.6.i) \uline{et} ii), \uline{muni de la structure de} \(\lambda\)-\uline{anneau définie par} 2.6.1.'
r.patch(p,'both',old,new,'check/findings/findings_321_325.json#18','Preserve the five directly inspected lexical underline spans.')
r.finding('321_325',19,'The sheaf letter before le faisceau is a typed K with one short rule underneath.',
 'The native top crop resolves its straight vertical and oblique strokes and the separate horizontal rule. The source explicitly identifies it as the sheafification of the constant presheaf with value K. The attached underlined typed K agrees.',
 'Exemple2.8, sheaf introduced',witness=334)
r.finding('321_325',20,'The K argument of H^0(X,K) is the same underlined typed letter.',
 'The native top crop resolves the short rule within the parentheses and the same straight K strokes. The attached form preserves the sheaf just defined; the superscript small o is handled by the stated zero convention.',
 'Exemple2.8, first H^0 expression',witness=334)
r.finding('321_325',21,'En effet starts a separate indented paragraph after the example statement.',
 'The native top crop shows the new line, indentation and spacing. The attached break preserves the printed words and punctuation.',
 'paragraph after Exemple2.8',verdict='formatting observed; no content error',witness=334)
r.finding('321_325',22,'En particulier starts another separate indented paragraph.',
 'The native top crop shows the indentation after the completed phrase limite inductive. The attached break agrees without a content change.',
 'En particulier paragraph',verdict='formatting observed; no content error',witness=334)
r.finding('321_325',23,'The Z in the final H^0 expression is reinforced/double-stroked and has a separate underline.',
 'The native top crop resolves the thick double-stroke body and the independent low horizontal rule. This is the constant integer sheaf, obtained by the same sheafification construction with K=Z; the attached underlined blackboard form follows the accepted reinforced-letter convention.',
 'En particulier, H^0(X,Z)',witness=334)
for id in ['fixes/FIXLOG_6.jsonl#341','fixes/FIXLOG_6_CURRENT.jsonl#306']:
 r.source(id,'No printed id/Id token occurs on323; the page’s body ends at2.9.2.',
  'This row replaces providecommand by renewcommand in the source-only continuation-macro block after2.9.2, making its lowercase operator definition effective. It is a scoped TeX implementation decision, not a claim about a printed323 glyph. A source-token search finds no body use of this macro between this reset and the next reset on346; that source audit does not mark any later page visually checked.',
  'source-only macro block after the printed page body',verdict='scoped implementation retained; no printed occurrence claimed',change='Retain the explicit renewal syntax; adjudicate any printed operator at its actual usage locus.',witness=334,page=p)
r.own_finding('ASTRA-V-PARAGRAPH-323',p,'The paragraph number2.9. is ordinary typed text with no rule or added weight.',
 r'2.9. replaces \textbf{2.9.}.',
 'Preserve the directly observed plain paragraph-number form.',
 'The main lower strip and native crop agree on the ordinary numeral strokes. The separate named labels Définition and Exemple retain the accepted bold-label convention.',
 'paragraph number2.9',kind='font',witness=334)
r.patch(p,'both',r'\textbf{2.9.}','2.9.','ASTRA-V-PARAGRAPH-323','Preserve the inspected plain paragraph number.')
r.own_finding('ASTRA-V-INK-323',p,'The separator between φ and ψ before ∈Ĝ(A) is heavily overstruck; its strokes do not resolve an additional character. A separate tiny short mark is visible between Σ and the binomial in2.9.1.',
 r'Retain \varphi,\psi\in\Ghat(A) and the existing summation token sequence.',
 'Retain the contextual comma reading and record the damaged ink without inventing another symbol.',
 'The actual crops witness_323_phi_pair.png and main_323_phi_pair.png show the overstrike, independently reviewed by the coordinator. The final identity uses the two inputs through m(φ,ψ)=φψ and F_a(φ)=φ^a, namely F_a∘m=m∘(F_a×F_a); this supplies the explicit two-variable context for the retained comma. The isolated mark in witness_323_sum.png is much smaller than the typed comma after2.9.1 and is recorded physically without an assigned extra mathematical token. All fourteen φ shapes have an open upper-left curl and descending stem, supporting the attached varphi forms.',
 'quantifier before2.9.2 and the summation in2.9.1',kind='damaged_print',verdict='source reading retained with explicit ink observation',witness=334)
r.page(p,'égalités2.4.2 sont des polynômes','φ^aψ^a=(φψ)^a.',
 'Complete polynomial-specialization paragraph, both unfilled λ positions and plain Z, all five definition word rules and plain defined term, both underlined typed K letters and underlined reinforced Z, paragraph breaks, plain2.9, fourteen open-curl φ forms and every ψ, all exponents/braces/binomial/sum bounds in2.9.1, capital Log and closing comma, exact modulo torsion wording, damaged separator retained with explicit observation, all three2.9.2 identities and semicolons/final stop compared. Source-only continuation macros separately classified. No author note.',
 witness='Native witness334 top/lower and tight damaged-ink crops, plus main tight separator crop; witness_323_top.png, witness_323_lower.png, witness_323_phi_pair.png, witness_323_sum.png and main_323_phi_pair.png')
r.commit()
