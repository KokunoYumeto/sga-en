"""Folio200: mixed varieties, source emphasis, glyphs and page boundary."""
from review_helpers import Review
r=Review()
r.finding('196_200',19,'The final printed words are On a des isomorphismes canoniques',
 'The complete lower part of200 contains no following canonical-isomorphism display. Both attached layer chunks end after canoniques, so the previously misplaced display is already outside this page.',
 'Last two printed lines',change='Retain the attached boundary immediately after canoniques.')
for i,old,new,region in [(20,r'\emph{variété mixte de classe}',r'\uline{variété mixte de classe}','Definition of a mixed variety'),(21,r"\emph{parties principales à l'ordre}",r"\uline{parties principales à l'ordre}",'Paragraph1.2.1')]:
 sid=r.finding('196_200',i,'The specified lexical words have lower rules; their following mathematical term is plain',
  'The main image and witness show the exact lexical extent already isolated in the attached emphasis group. The following C^r or n has no rule. Typeset the observed lexical rule explicitly, retaining the adjacent formula unchanged.',
  region,verdict='confirmed with literal underline formatter',change='Retain the existing group boundary and typeset its words with uline.',witness=211)
 r.patch(200,'both',old,new,sid,'Preserve the exact inspected lexical rule and leave the following mathematical token independent.')
r.finding('196_200',22,'où U′ (resp. V′) est un ouvert de U (resp. V)',
 'The first explanatory line has the same parenthesis and abbreviated resp. as the attached text. The earlier line-break repair is already present and preserves all tokens.',
 'First explanatory line after the opening display',change='Retain the attached inline parenthesis and resp.')
sid='ASTRA-II-O-200';reason='All ten structure-sheaf O letters carry one individual lower rule, in the two displays, the three local-model or fibre expressions, and the four algebra/module occurrences in1.2.1. Their left superscripts and right subscripts remain outside the rule.'
r.own_finding(sid,200,'Ten singly underlined structure-sheaf O letters',r'\cO',r'\underline{O}',reason,'Complete page, ten explicit O occurrences',kind='font',witness=211)
r.patch(200,'both',r'\cO',r'\underline{O}',sid,reason,10)
sid='ASTRA-II-N-200';reason='Both natural-number N letters, in the mixed-variety definition and in1.2.1, have two horizontal lower rules. The native witness shows both rules distinctly.'
r.own_finding(sid,200,'Two N letters with two horizontal lower rules',r'\N',r'\underline{\underline{N}}',reason,'Definition and paragraph1.2.1',kind='font',witness=211)
r.patch(200,'both',r'\N',r'\underline{\underline{N}}',sid,reason,2)
sid='ASTRA-II-PARAGRAPH-200';reason='The identifier1.2.1. is plain typed numerals followed by a stop. Keep the stop and remove the attached bold styling at this inspected paragraph identifier.'
r.own_finding(sid,200,'Plain paragraph identifier1.2.1.',r'\textbf{1.2.1.}','1.2.1.',reason,'Opening of the final paragraph',kind='font',witness=211)
r.patch(200,'both',r'\textbf{1.2.1.}','1.2.1.',sid,reason)
r.page(200,'Γ(U′×V′, {}^r O_{U′×V′})=C(U′,C^r(V′)),','On a des isomorphismes canoniques',
 'Every printed word, projection and inclusion map, prime, superscript, subscript, comma and stop was compared. The two defined lexical groups have exact underlines with their following formulas plain. Native witness211 confirms both double-underlined N letters and the individual O rules. The page ends before the canonical-isomorphism display.',witness=211)
r.commit()
