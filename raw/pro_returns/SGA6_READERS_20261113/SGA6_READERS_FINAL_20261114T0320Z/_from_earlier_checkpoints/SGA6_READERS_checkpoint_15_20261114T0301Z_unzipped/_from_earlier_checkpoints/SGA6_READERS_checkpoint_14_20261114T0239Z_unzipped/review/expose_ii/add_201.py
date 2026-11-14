"""Folio201: principal parts, three printed variants, and explicit word rules."""
from review_helpers import Review
r=Review()
r.finding('201_205',1,'The page begins with the two canonical-isomorphism rows P^0≃O_X and P^1≃O_X⊕Ω^1',
 'The first display and its two final commas are at the top of201. The attached chunks put the entire display after the201 marker, following canoniques on200. Both adjacent complete pages were inspected.',
 'Opening display',change='Retain the already-corrected page boundary before the opening display.')
reason='The second occurrence prints où with an accent. The phrase supplies a second name for the same sheaf Ω^1_{X/S}: its relative-differential name and its relative-cotangent name are identified by the same displayed symbol. The connective ou expresses that printed naming construction. Keep the accented diplomatic reading and the existing unaccented current reading.'
r.finding('201_205',2,'par rapport à S où faisceau cotangent relatif',reason,'First prose paragraph',change='Retain diplomatic où and existing current ou.',witness=212)
for sid in ['fixes/RECONCILE_CODEX_6.json#257','fixes/FIXLOG_6_CURRENT.jsonl#362']:
 r.source(sid,'The second connective is printed où',reason,'First prose paragraph',page=201,change='Retain the existing current-only ou correction.',witness=212)
reason='The later operator definition prints f^{-1}(O_X), whereas the earlier universal operator on this page prints f^{-1}(O_S). For f:X→S the specified structure map is f^#:f^{-1}O_S→O_X. In principal parts, the two O_X actions u_1,u_2 agree on this image because both projections are over S. The map d^n(E):e↦1⊗e therefore satisfies d^n(E)(ae)=u_2(a)(1⊗e)=u_1(a)(1⊗e) for a from f^{-1}O_S. Composing with an O_X-linear h gives D(ae)=aD(e). This exact factorization proves the required base-linearity and supports the existing current O_S reading. Preserve the actual X in the diplomatic layer.'
r.finding('201_205',3,'The operator definition prints f^{-1}(O_X)-linéaire',reason,'Paragraph1.2.2, operator definition',change='Retain diplomatic O_X and existing current O_S.',witness=212)
for sid in ['fixes/RECONCILE_CODEX_6.json#258','fixes/FIXLOG_6_CURRENT.jsonl#363']:
 r.source(sid,'The second inverse-image expression has subscript X',reason,'Paragraph1.2.2, operator definition',page=201,change='Retain the existing current-only O_S correction.',witness=212)
r.finding('201_205',4,'The principal-parts expression prints a circled plus between P^n and E',
 'The main scan and native witness show a vertical and a horizontal bar inside the circle, matching the direct-sum sign in the opening display. The following words explicitly specify produit tensoriel using the second O_X action. The corresponding balanced construction sends e to1⊗e and imposes (p·a)⊗e=p⊗ae, which is the factorization used in the printed bijection(1.2.2.1). Preserve the circled plus diplomatically and the existing tensor-product sign in current.',
 'Paragraph1.2.2, definition of P^n(E)',change='Retain the existing diplomatic oplus/current otimes variant.',witness=212)
sid='ASTRA-II-O-201';reason='Each of the thirteen O letters in the displays, module structures, inverse-image expressions and final Hom subscript has one individual lower rule. The rule applies to O alone and leaves the inspected layer-specific X or S index unchanged.'
r.own_finding(sid,201,'Thirteen individually underlined O letters',r'\cO',r'\underline{O}',reason,'Complete page',kind='font',witness=212)
r.patch(201,'both',r'\cO',r'\underline{O}',sid,reason,13)
sid='ASTRA-II-UNDERLINE-201';reason='The six defined lexical spans carry the word rules shown in the main scan and witness: faisceau cotangent relatif; faisceau tangent relatif; fibré tangent; cotangent; relatif; opérateur différentiel universel d’ordre. The intervening resp. and the following n are plain. Preserve exactly those groups.'
r.own_finding(sid,201,'Six separately underlined lexical spans','Six existing emph groups',r'uline on the same exact six groups',reason,'Definitions in the first two prose paragraphs',kind='underline',witness=212)
for text in ['faisceau cotangent relatif','faisceau tangent relatif','fibré tangent','cotangent','relatif',"opérateur différentiel universel d'ordre"]:
 r.patch(201,'both',r'\emph{'+text+'}',r'\uline{'+text+'}',sid,reason)
sid='ASTRA-II-PARAGRAPH-201';reason='The paragraph identifier1.2.2. has plain typed numerals and its final stop. Retain those characters with plain styling.'
r.own_finding(sid,201,'Plain1.2.2.',r'\textbf{1.2.2.}','1.2.2.',reason,'Middle paragraph identifier',kind='font',witness=212)
r.patch(201,'both',r'\textbf{1.2.2.}','1.2.2.',sid,reason)
r.page(201,'P^0_{X/S}≃O_X, / P^1_{X/S}≃O_X⊕Ω^1_{X/S},','où Diff^n(E,F) désigne l’ensemble des opérateurs différentiels de E',
 'All words, six defined lexical spans, structure-sheaf indices, principal-parts expressions and display punctuation were compared. The first two isomorphism signs are headless; the final bijection has a visible arrowhead, retained. Native witness212 confirms the accented où, the printed X in the later inverse image, the circled plus, and the exact word rules. Existing current variants are supported by the explicit principal-parts maps recorded above.',witness=212)
r.commit()
