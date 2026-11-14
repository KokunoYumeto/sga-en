"""Folio196: Verdier’s Koszul example, exact source defects and citation repair."""
from review_helpers import Review,ROOT
import json
r=Review()
r.finding('196_200',1,'The page begins tel que, the transition map, and soit nul.',
 'The full first line was inspected in both scans. The attached marker already puts all three units on196. The display-layout variation preserves the map tokens and stop; the lexical rules are restored separately.',
 'First printed line',change='Retain the boundary and mathematical token sequence; restore the two observed lexical rules.',witness=207)
r.finding('196_200',2,'The definition continues comma A la B-algèbre, with no et',
 'Both scans give the same comma followed directly by A. The attached text already removes the extra conjunction.',
 'Definition of A',witness=207)
reason='Both scans leave the relation slot blank between n and0. Current supplies n>0, the positive-index direct sum. The projection and zero inclusion canonically identify the sums over n≥0 and n>0: the n=0 summand is B/(1,1)=0 because f=(x,y). Thus this precise completion preserves the module constructed in the proof. Diplomatic retains the visible blank.'
r.finding('196_200',3,'The coproduct index is n blank 0',reason,'Definition of M',change='Retain the diplomatic blank and the current positive-index completion n>0.',witness=207)
r.finding('196_200',4,'The numerical1 call follows the first display stop',
 'Both scans put the raised1 call at the right of the complete formula, after its stop. The attached split call/text location agrees; explicit author label1 is supplied separately.',
 'First display and complete author note',change='Keep the location and wording; use explicit numerical1 helpers.',witness=207)
r.finding('196_200',5,'The direct-sum decomposition display has no final punctuation',
 'The scan continues into mais without a punctuation mark after its last H_2 term. The attached text agrees.',
 'Display after On a d’autre part')
r.finding('196_200',6,'mais H_2^B(f^n,B)=0 puisque, with no comma after0',
 'The inline expression and its adjoining words have this exact token sequence. Both attached layers already omit the unprinted comma.',
 'Sentence using regularity of f')
r.finding('196_200',7,'The following display ends with a comma, before capitalized On a enfin',
 'The comma is visible. Diplomatic preserves it; current supplies a sentence stop before the next independent capitalized sentence, leaving the isomorphism unchanged.',
 'Display before On a enfin',change='Retain diplomatic comma and current sentence stop.')
reason='The SGA6 scan prints EGA II1.1.3.3. The primary EGA III, Première partie, printed p.83, formula(1.1.3.3), identifies H^i(f,M) with H_{r−i}(f,M). For the displayed two-element sequence(x^n,y^n), the r=2,i=0 map sends(e_1∧e_2)⊗m to m in the common annihilator of x^n and y^n, exactly the H_2→H^0 identification used here. Correct only the Roman chapter numeral to III. The primary PDF text was retrieved at https://www.numdam.org/item/PMIHES_1961__11__5_0.pdf; no EGA image inspection is claimed.'
sid=r.finding('196_200',8,'The citation is printed(EGA II1.1.3.3)',reason,
 'Citation immediately before the Koszul H_2/H^0 identification',verdict='not applied and now applied',change='Current changes EGA II to EGA III; diplomatic keeps II.')
r.patch(196,'current','(EGA II 1.1.3.3)','(EGA III 1.1.3.3)',sid,reason)
for i,region in [(9,'Description of the annihilator submodule'),(10,'Right member of formula(*)')]:
 r.finding('196_200',i,'M is on the baseline and(f^n) is its lower left index',
 'The native witness aligns M with the adjoining baseline text or H_2 expression, and places(f^n) below and to its left. The attached left-subscript form agrees.',
 region,witness=207)
reason='The scan omits the closing parenthesis after A in the left member of(*). The current closing delimiter gives H_2^A(f^n,A), the same Koszul module appearing in the first display and the transition maps. It balances that existing argument list without adding a new term. Diplomatic preserves the missing delimiter.'
r.finding('196_200',11,'H_2^A(f^n,A lacks its closing parenthesis in(*)',reason,'Formula(*)',change='Retain the existing current closing parenthesis and diplomatic omission.',witness=207)
for sid in ['fixes/RECONCILE_CODEX_6.json#254','fixes/FIXLOG_6_CURRENT.jsonl#361']:
 r.source(sid,'The closing parenthesis is absent in the printed left member of(*)',reason,'Formula(*)',page=196,change='Keep the existing current-only insertion of the closing parenthesis.',witness=207)
r.finding('196_200',12,'le pro-objet and n’est pas nul have separate word rules',
 'The intervening degree-indexed Koszul expression is independent of the two lexical rules. The attached groups already have the exact observed boundaries.',
 'Nonvanishing conclusion',change='Use literal uline for the same two word groups.',witness=207)
sid='ASTRA-II-F-196';reason='All24 system-f letters on this page were compared: both top transition arguments; the system and direct-sum definition; all Koszul terms; the regular-sequence name; both annihilator indices and their ideal; the final transition and multiplier; and the pro-object term. Each typed f has one individual lower rule. Exponents and parentheses remain outside it.'
r.own_finding(sid,196,'Twenty-four individually underlined system-f letters',r'\mathbf f',r'\underline{f}',reason,'All24 system symbols on196',kind='font',witness=207)
r.patch(196,'both',r'\mathbf f',r'\underline{f}',sid,reason,24)
sid='ASTRA-II-NOTES-196';reason='The first display’s call and the matching complete author-note label both use raised numerical1 inside baseline parentheses, with the call after the stop.'
r.own_finding(sid,196,'Explicit numerical1 call and label',r'\footnotemark and \footnotetext',r'\SGAAuthorFootMark{1} and \SGAAuthorFootText{1}',reason,'First display and author note',kind='author_footnote',witness=207)
r.patch(196,'both',r'\footnotemark',r'\SGAAuthorFootMark{1}',sid,reason)
r.patch(196,'both',r'\footnotetext{',r'\SGAAuthorFootText{1}{',sid,reason)
sid='ASTRA-II-PARAGRAPH-196';reason='The native witness shows the plain numeral1.2 with no following stop. Remove the attached extra stop and bold wrapper while retaining the same paragraph identifier.'
r.own_finding(sid,196,'Plain1.2 with no terminal stop',r'\textbf{1.2.}','1.2',reason,'Paragraph identifier',kind='punctuation',witness=207)
r.patch(196,'both',r'\textbf{1.2.}','1.2',sid,reason)
sid='ASTRA-II-UNDERLINE-196';reason='The lemma continuation underlines tel que and soit nul, with its math independently marked. In the later proof, exactly le pro-objet and n’est pas nul have lexical rules. All remaining proof prose and the author note are plain.'
r.own_finding(sid,196,'Four exact lexical underline groups','Two missing rules and two emphasis groups',r'\uline for tel que, soit nul, le pro-objet, n’est pas nul',reason,'First line and nonvanishing conclusion',kind='underline',witness=207)
r.patch(196,'both','\ntel que\n','\n'+r'\uline{tel que}'+'\n',sid,reason)
r.patch(196,'both','soit nul.\n'+r'\end{enumerate}',r'\uline{soit nul}.'+'\n'+r'\end{enumerate}',sid,reason)
r.patch(196,'both',r'\emph{',r'\uline{',sid,reason,2)
r.page(196,'tel que H_i(f^{n′},A)→H_i(f^n,A) soit nul.','la projection Spec(A)→Spec(B) est un homéomorphisme,; note ends complexe de Koszul.',
 'Every word, all24 system symbols, each Koszul subscript/superscript, both annihilator indices, all isomorphism signs, all defects and the complete author note were compared. Native witness207 resolves the blank sum-index slot, plain unstopped paragraph label, lower-left annihilator indices and missing parenthesis. The EGA citation correction is supported by separately retrieved primary text, not an EGA scan comparison.',witness=207)
evidence={'record_type':'external_reference_verification','related_source_id':'check/findings/findings_196_200.json#8','primary_url':'https://www.numdam.org/item/PMIHES_1961__11__5_0.pdf','title':'Éléments de géométrie algébrique III, Première partie','publication':'Publications Mathématiques de l’IHÉS11(1961)','locator':'Printed p.83, formula(1.1.3.3); adjoining formula(1.1.3.4)','retrieval':'Primary PDF text retrieved through web open/find; screenshot request rejected because the20MB PDF exceeded the endpoint limit. No image-verdict claim.','verified_result':'H^i(f,M)≃H_{r−i}(f,M). At r=2,i=0, (e1∧e2)⊗m maps to m in the annihilator of(x^n,y^n).','correction':'SGA6 folio196 current-only EGA II1.1.3.3→EGA III1.1.3.3'}
(ROOT/'review/expose_ii/external_reference_ega_iii_1_1_3_3.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
r.commit()
