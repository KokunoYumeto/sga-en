"""Folio194: derived adjunction, arrowheads and literal derived-functor letters."""
from review_helpers import Review
r=Review()
sid=r.finding('191_195',23,'Preuve de is underlined and b). is plain',
 'The rule ends before b). The attached emphasis has the correct lexical scope, preserved as a literal word rule.',
 'Proof heading',change=r'\uline{Preuve de} b).')
r.patch(194,'both',r'\emph{Preuve de}',r'\uline{Preuve de}',sid,'Preserve the directly inspected heading rule and plain item label.')
for i,region in [(24,'First display, definition of the unbounded derived coherer'),(25,'Inline restriction comparison'),(26,'Formula(1)'),(27,'Formula(2)'),(28,'Inline adjunction statement')]:
 r.finding('191_195',i,'The indicated R has two horizontal rules below the letter',
 'The two lower rules are visible at this exact occurrence. Preserve them literally. The arrow in(1) has its visible arrowhead; the inline maps in the adjunction sentence retain the same complete token sequences and punctuation. No new content edit is introduced solely for their layout.',
 region,verdict='amended',change=r'Use \underline{\underline{R}} for the observed R; retain all adjoining maps and punctuation.')
sid='ASTRA-II-R-194';reason='The definition, inline restriction comparison, formulas(1),(2), and inline adjunction statement contain five R letters with two horizontal lower rules. This page-specific patch preserves exactly those five glyphs. The two degree-indexed R letters in the spectral sequence stay plain.'
r.own_finding(sid,194,'Five literal double-underlined R glyphs',r'\mathbb R',r'\underline{\underline{R}}',reason,'The five derived-coherer occurrences',kind='font')
r.patch(194,'both',r'\mathbb R',r'\underline{\underline{R}}',sid,reason,5)
sid='ASTRA-II-PHI-194';reason='The four functor symbols have closed loops crossed by a stroke: the ordinary adjunction clause, the displayed-in-prose inclusion functor, the full-faithfulness clause, and the final essential-image clause. Use phi for these four observed symbols.'
r.own_finding(sid,194,'Four closed-loop phi symbols',r'\varphi',r'\phi',reason,'Ordinary and derived adjunction argument',kind='symbol')
r.patch(194,'both',r'\varphi',r'\phi',sid,reason,4)
sid='ASTRA-II-ARROWS-194';reason='Both the arrow in(1), E→RQ(E), and the inline arrow E^i→Q(E^i) have a wave above a shaft with a visible right arrowhead. The attached xrightarrow{sim} forms retain both the source shape and the named adjunction maps.'
r.own_finding(sid,194,'Two over-arrow isomorphisms retain visible right arrowheads',r'Two \xrightarrow{\sim} forms','Retain both exact over-arrow forms',reason,'Formula(1) and the following componentwise adjunction map',kind='symbol',verdict='confirmed')
r.page(194,'ce qui achève la démonstration de a).','Cela prouve b) et achève la démonstration de(3.7).',
 'All prose, functor arguments, both numbered adjunction maps, all four phi occurrences, the spectral sequence and final conclusion were compared. The five derived R glyphs have literal double lower rules; both isomorphism arrows have heads. Only the Preuve de heading has a lexical rule.')
r.commit()
