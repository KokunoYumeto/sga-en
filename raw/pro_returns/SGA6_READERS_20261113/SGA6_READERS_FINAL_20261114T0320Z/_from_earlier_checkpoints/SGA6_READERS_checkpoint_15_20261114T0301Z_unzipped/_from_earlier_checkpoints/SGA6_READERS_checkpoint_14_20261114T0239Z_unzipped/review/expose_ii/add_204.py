"""Folio204: fibre restriction and the opening rigidity notation."""
from review_helpers import Review
r=Review()
r.finding('201_205',13,'Les variétes mixtes: the second e has no accent',
 'The native witness shows an accent above the first e and no accent above the second. The attached diplomatic/current spellings already preserve the printed form and the corrected French plural respectively.',
 'Second paragraph of2.0',change='Retain diplomatic variétes and current variétés.',witness=215)
sid='ASTRA-II-O-204';reason='The one O_X in the first prose paragraph has its own single lower rule. Preserve the subscript separately.'
r.own_finding(sid,204,'One individually underlined O_X',r'\cO_X',r'\underline{O}_X',reason,'First prose paragraph',kind='font')
r.patch(204,'both',r'\cO',r'\underline{O}',sid,reason)
sid='ASTRA-II-PARAGRAPH-204';reason='The numerical paragraph identifier2.0. uses plain typed numerals with a final stop. The named Notations label is covered separately by the accepted statement-label convention.'
r.own_finding(sid,204,'Plain2.0.',r'\textbf{2.0.}','2.0.',reason,'Opening rigidity paragraph',kind='font')
r.patch(204,'both',r'\textbf{2.0.}','2.0.',sid,reason)
r.page(204,'i_s^*(P^n_{X/S})≃P^n_{X_s},','The induction morphism(2.1.1) ends with a comma.',
 'Every word and symbol in the restriction paragraph, both rigidity paragraphs, and the complete notation definition was compared. The opening isomorphism has a headless sign. In2.1 the set-valued Hom words are plain and the four sheaf-Hom occurrences have independent lower rules, already represented explicitly. The section-title and Notations-label styles follow the accepted conventions. Native witness215 resolves the two e accents in variétes. The unquantified-x Codex item concerns the following proof and is not present on this page.',witness=215)
r.commit()
