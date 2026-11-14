"""Folio218: comparison of Grothendieck groups and fixed-order parameters."""
from review_helpers import Review
r=Review()
r.finding('216_220',9,'The folio begins Si S est compact',
 'The whole opening phrase lies at the top of218. Both attached marker-delimited layers now put Si S est after the218 marker.',
 'Top-of-page continuation',change='Retain the existing corrected marker position.')
r.finding('216_220',10,'compact alone is underlined, before a plain comma',
 'The main scan and witness confine the lexical rule to compact. The attached emph span already has that extent.',
 'First line',change='Render the correct existing span with uline.',witness=229)
r.finding('216_220',11,'A crossed-loop superscript after b in the denominator category',
 'Both scans show the crossed loop, matching the previously inspected notation on174. The inclusion K^{b,∅}(Loclib(S))→K^b(Loclib(S)) is the full inclusion of acyclic complexes, and the displayed quotient maps to perfect complexes by sending a bounded complex to its derived object. Thus the existing varnothing transcription records the printed notation at exactly this acyclic-subcategory occurrence.',
 'First paragraph, quotient category',change=r'Retain K^{b,\varnothing}.',witness=229)
r.finding('216_220',12,'The lowercase projective-limit sign has a leftward lower arrow and no index',
 'The display leaves the area below the arrow empty. The following sentence supplies the compact A indexing family; the attached unindexed limit is faithful.',
 'Completed-group display',change='Retain the unindexed limit and final comma.')
r.finding('216_220',13,'The sequence symbol n in n=(n_i) has one lower rule',
 'The individual sequence letter is underlined; the component n_i inside parentheses is plain. The attached grouping preserves exactly that distinction.',
 '3.2.3, definition of the order sequence',change='Retain the existing individually underlined n.',witness=229)
r.finding('216_220',14,'The superscript order n of Comp.diff has a short lower rule touching its base',
 'The native witness resolves the short horizontal stroke along the bottom of the small superscript n. Its scope is the sequence symbol alone, not the operator name or its argument.',
 '3.2.3, definition of Comp.diff',change='Retain the individually underlined superscript n.',witness=229)
r.finding('216_220',15,'The sequence n after d’ordre has an individual lower rule',
 'The lower rule stops under n before the comma. The nearby component n_i in each product has no added rule.',
 '3.2.3, fixed-order condition',change='Retain the existing underlined n.',witness=229)
r.finding('216_220',16,'le sous espace fermé, with no hyphen',
 'Both scans omit the hyphen in this later occurrence, although the earlier un sous-espace on this same page contains it. The attached diplomatic layer preserves the omission and the corrected layer already supplies the hyphen.',
 'Last paragraph, defining equations',change='Retain the existing diplomatic/current sous espace/sous-espace variant.',witness=229)
sid='ASTRA-II-FONTS-218';reason='The structure-sheaf O has one lower rule, while the coefficient C and the integer Z indexing the family F each have two horizontal lower rules. These are separately observed occurrences.'
r.own_finding(sid,218,'One singly underlined O, one doubly underlined C and one doubly underlined Z',r'\cO, \mathbb C, \Z',r'Literal individual lower rules',reason,'Module category and the integer-indexed family in3.2.3',kind='font',witness=229)
r.patch(218,'both',r'\cO',r'\underline{O}',sid,reason)
r.patch(218,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason)
r.patch(218,'both',r'\Z',r'\underline{\underline{Z}}',sid,reason)
sid='ASTRA-II-UNDERLINE-218';reason='The opening word compact has a lexical lower rule; all later prose is plain. The numbered paragraph3.2.3 is printed without bold weight or a lower rule.'
r.own_finding(sid,218,'One lexical compact rule and plain paragraph3.2.3','Emph compact and bold3.2.3',r'uline compact and plain3.2.3',reason,'Opening word and numbered paragraph',kind='underline',witness=229)
r.patch(218,'both',r'\emph{compact}',r'\uline{compact}',sid,reason)
r.patch(218,'both',r'\textbf{3.2.3.}',r'3.2.3.',sid,reason)
r.page(218,'Si S est compact, ind.an(E•) définit canoniquement un élément','(l’espace ∏Diff^{n_i}(F^i,F^{i+1}) est un espace de Fréchet). Le sous-ensemble',
 'Every word and symbol was compared in both layers, including the two nested quotient-category parentheses, its crossed-loop acyclic marker, both locators II2.3.2(a)/I6.4, the displayed comparison and completed group, all three sequence-order underlines, the two products and equation d^{i+1}d^i=0, and the literal lowercase l’espace after the stop. The page ends after Le sous-ensemble; the following Ell notation belongs to219 and will be decided there.',witness=229)
r.commit()
