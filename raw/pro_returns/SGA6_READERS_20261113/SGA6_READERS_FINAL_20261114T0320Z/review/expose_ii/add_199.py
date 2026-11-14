"""Folio199: second appendix opening, author label and literal glyph rules."""
from review_helpers import Review
r=Review()
sid=r.finding('196_200',18,'APPENDICE II / DÉFINITION DE L’INDICE ANALYTIQUE D’UN COMPLEXE ELLIPTIQUE RELATIF; no stop after II',
 'The complete two-part title was compared. The inherited extra Exposé II is already removed. A stop after II remains in the attached title although neither printed title line has it; remove that punctuation while preserving all title words. Section-heading styling follows the accepted convention.',
 'Complete appendix title',verdict='confirmed and supplemented',change='Keep the earlier removal of Exposé II; remove the remaining unprinted stop after II.')
r.patch(199,'both',r'\section*{Appendice II. Définition',r'\section*{Appendice II\\ Définition',sid,'Remove the unprinted stop after II; the line break preserves the two-part title without adding punctuation.')
sid='ASTRA-II-O-199';reason='The O_S in the paragraph defining continuous functions and the O in the final expression with left superscript r each have one horizontal lower rule. The native witness resolves the short rule before the U×V subscript.'
r.own_finding(sid,199,'Two individually underlined O letters',r'\cO',r'\underline{O}',reason,'Definition of O_S and final line',kind='font',witness=210)
r.patch(199,'both',r'\cO',r'\underline{O}',sid,reason,2)
sid='ASTRA-II-FIELDS-199';reason='The real-coordinate R and both natural-number N letters have two separate horizontal rules below the typed letter. The witness clearly separates those rules from the letter stems. Use the literal construction only at these three inspected occurrences.'
r.own_finding(sid,199,'One R and two N glyphs, each with two lower rules',r'\R and \N',r'\underline{\underline{R}} and \underline{\underline{N}}',reason,'Definition1.1, last two paragraphs',kind='font',witness=210)
r.patch(199,'both',r'\R^n',r'\underline{\underline{R}}^n',sid,reason)
r.patch(199,'both',r'\N',r'\underline{\underline{N}}',sid,reason,2)
sid='ASTRA-II-NOTES-199';reason='The call after structure mixte and its matching complete footnote each use a raised numerical1 within baseline parentheses. All words of the note were checked.'
r.own_finding(sid,199,'Author note with explicit numerical1',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Second paragraph call and sole footnote',kind='author_footnote',witness=210)
r.patch(199,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',sid,reason)
r.page(199,'APPENDICE II / DÉFINITION DE L’INDICE ANALYTIQUE D’UN COMPLEXE ELLIPTIQUE RELATIF','le faisceau d’anneaux sur U×V défini par; author note ends de les sauter.',
 'The complete title, every introductory word and citation, all symbols in the definitions, the projective-limit expression and the complete author note were compared. The displayed projective-limit formula preserves the printed tokens and stop despite its layout. Section-title word rules are covered by the accepted heading convention. Native witness210 confirms the individual O rules, the double lower rules on R and both N letters, and the note label.',witness=210)
r.commit()
