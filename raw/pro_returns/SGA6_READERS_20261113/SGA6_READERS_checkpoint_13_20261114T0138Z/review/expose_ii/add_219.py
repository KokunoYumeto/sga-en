"""Folio219: fixed-order parameter space, index remarks and target correction."""
from review_helpers import Review
r=Review()
r.finding('216_220',17,'Ell has an individually underlined superscript n at the start of219',
 'The source finding was keyed to218 before its marker was moved. Direct inspection places this complete Ell term and de on the first line of219; the short lower rule is clearly separate beneath the superscript.',
 'Top line of219, Ell term',change='Retain the existing underlined superscript and corrected marker location.',witness=230,actual_page=219)
r.finding('216_220',18,'219 begins Ell^n(F) de Comp.diff^n(F)',
 'The preceding folio ends after Le sous-ensemble and this one begins with the Ell term. Both attached layers already put the marker between those phrases.',
 'Top boundary',change='Retain the current marker placement.',witness=230)
for index,printed,region in [(19,'The superscript n of Comp.diff has one individual lower rule','First line, Comp.diff term'),(20,'The order n after d’ordre has one individual lower rule','First line, elliptic order'),(21,'The superscript n of Ell in3.2.4 has one individual lower rule','3.2.4, target parameter space')]:
    r.finding('216_220',index,printed,
      'The main scan and native witness resolve the short lower rule beneath this sequence symbol. Its attached TeX grouping is already faithful and leaves the surrounding operator name and parentheses outside.',
      region,change='Retain the existing individually underlined n.',witness=230)
r.finding('216_220',22,'F_r• in3.2.5 is plain; F_r• in the class display above is singly underlined',
 'The source prints the bundle complex without a lower rule in3.2.5 and the section-sheaf complex with a rule in3.2.4. The explicit sections construction F_r•↦underline F_r• used in216 relates these occurrences, and the current transcription preserves their respective glyphs.',
 '3.2.5, sentence beginning Alors',change='Retain the current plain bundle F and underlined sheaf F in their exact occurrences.',witness=230)
reason='Both scans print [S,I(S)] in the later comparison, while the same paragraph defines I(H) as the index-operator subspace of L(H,H) and explicitly describes [S,I(H)] as classes of maps S→I(H). The represented element is the homotopy class [φ] of such a map φ, with homotopies S×[0,1]→I(H); its target remains the defined operator space I(H). The existing corrected occurrence therefore restores that H while the diplomatic layer retains the printed S. No relation between this group and K•(S) is added.'
r.finding('216_220',23,'Later [S,I(S)] after earlier [S,I(H)]',reason,
 '3.2.5, comparison of the two indices',change='Retain the existing diplomatic I(S) / corrected I(H) variant.',witness=230)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#366','Printed later I(S), corrected I(H)',reason,
 '3.2.5, comparison of the two indices',change='Retain the existing corrected I(H).',witness=230)
r.source('fixes/RECONCILE_CODEX_6.json#262','Printed later I(S), corrected I(H)',reason,
 '3.2.5, comparison of the two indices',change='Retain the accepted correction with the explicit map-target justification.',witness=230,page=219)
sid='ASTRA-II-AUTHOR-NOTE-219';reason='The call within pour simplifier and the bottom note both show raised numerical1 inside baseline parentheses. The outer parenthesis of pour simplifier remains separate.'
r.own_finding(sid,219,'Numerical author-note label1',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'3.2.4 and the bottom author note',kind='author_note_label',witness=230)
r.patch(219,'both',r'\footnote{pour le cas général, utiliser la notion de «~fibré hilbertien faible~» ou champ continu d\'espaces de Hilbert de [12].}'.replace("\\'","'"),r"\SGAAuthorFootnote{1}{pour le cas général, utiliser la notion de «~fibré hilbertien faible~» ou champ continu d'espaces de Hilbert de [12].}",sid,reason)
sid='ASTRA-II-PARAGRAPHS-219';reason='The two numbered paragraphs3.2.4 and3.2.5 and all surrounding prose are ordinary print without lexical lower rules or bold emphasis. The mathematical sequence and sheaf rules remain independently preserved.'
r.own_finding(sid,219,'Plain numbered paragraphs3.2.4 and3.2.5','Bold paragraph numbers','Ordinary paragraph numbers',reason,'Two numbered paragraphs',kind='font',witness=230)
r.patch(219,'both',r'\textbf{3.2.4.}','3.2.4.',sid,reason)
r.patch(219,'both',r'\textbf{3.2.5.}','3.2.5.',sid,reason)
r.page(219,'Ell^n(F) de Comp.diff^n(F) formé des complexes elliptiques d’ordre n est ouvert','Shih[17], ou à un travail en préparation de M.F.Atiyah et I.M.Singer.',
 'Every word, mathematical symbol and author-note word was compared with both layers. All four order-sequence rules, the singly underlined F only in the class display, the plain Hilbert-bundle F, the two distinct printed targets I(H)/I(S), the literal historical uncertainty statements, and the comma after the index display were checked. No extra mathematical comparison theorem or replacement for the printed historical questions is supplied. Native witness230 resolves the small superscript rules and note label.',witness=230)
r.commit()
