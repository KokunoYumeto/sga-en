"""Folio203: symbols, elliptic-complex definition and literal parentheses."""
from review_helpers import Review
r=Review()
for i,region in [(9,'First sheaf Hom in the symbol description'),(10,'Parenthetical complex-coefficient sheaf Hom')]:
 r.finding('201_205',i,'Hom has its own underline, independently of the O subscript rule',
  'Both Hom words visibly carry a rule below all three letters. The attached underline{Homop} is already correct. The O and coefficient C rules are treated independently below.',region,change='Retain the existing individual Hom underline.',witness=214)
sid=r.finding('201_205',11,'complexe elliptique is underlined; d’ordre is plain; the sequence n has its own rule',
 'The main image and witness confirm the three separate treatments. The attached group boundaries and underline{n} already preserve the distinction. Replace only the lexical emphasis formatter with its literal word-rule form.',
 'Definition in1.2.5',verdict='confirmed with literal underline formatter',change='Use uline on complexe elliptique; retain plain d’ordre and the independent underline{n}.',witness=214)
r.patch(203,'both',r'\emph{complexe elliptique}',r'\uline{complexe elliptique}',sid,'Preserve the directly observed rule on these two words only.')
sid=r.finding('201_205',12,'(considérée comme monomorphisme d’espaces annelés) cf.(1.1)).',
 'The witness confirms the closing parenthesis after annelés and two closing parentheses after1.1. The opening before considérée is already closed after annelés, while the opening before1.1 is closed by the first following parenthesis. The remaining final parenthesis has no opening partner. Remove that single unmatched character in current, preserving all printed word order, the closed considered-clause, the reference and the stop. Diplomatic retains the complete printed punctuation.',
 'Final paragraph1.2.6',verdict='amended; current correction now applied',change='In current alone, cf.~(1.1)). becomes cf.~(1.1).',witness=214)
r.patch(203,'current','cf.~(1.1)).','cf.~(1.1).',sid,'Delete only the unmatched final closing parenthesis; all other printed punctuation remains.')
sid='ASTRA-II-O-203';reason='The four O letters, including both sheaf-Hom subscripts, each have one lower rule. The independent rules under Hom are already present and remain unchanged.'
r.own_finding(sid,203,'Four individually underlined O letters',r'\cO',r'\underline{O}',reason,'First two prose paragraphs',kind='font',witness=214)
r.patch(203,'both',r'\cO',r'\underline{O}',sid,reason,4)
sid='ASTRA-II-FIELDS-203';reason='The coefficient C in the complex sheaf-Hom subscript and the N in the last paragraph each have two horizontal lower rules, resolved separately in the two witness regions.'
r.own_finding(sid,203,'One C and one N with two horizontal lower rules',r'\mathbb C and \N',r'\underline{\underline{C}} and \underline{\underline{N}}',reason,'First and final paragraphs',kind='font',witness=214)
r.patch(203,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason)
r.patch(203,'both',r'\N',r'\underline{\underline{N}}',sid,reason)
sid='ASTRA-II-SYMBOLE-203';reason='The defined word symbole has a lower word rule, ending before the semicolon. The attached group isolates precisely that word.'
r.own_finding(sid,203,'Underlined symbole',r'\emph{symbole}',r'\uline{symbole}',reason,'First paragraph, definition of sigma_n',kind='underline',witness=214)
r.patch(203,'both',r'\emph{symbole}',r'\uline{symbole}',sid,reason)
sid='ASTRA-II-PARAGRAPHS-203';reason='The identifiers1.2.5. and1.2.6. have plain typed numerals and their printed stops.'
r.own_finding(sid,203,'Plain1.2.5. and1.2.6.','Bold identifiers','Plain identifiers',reason,'Two numbered paragraph openings',kind='font',witness=214)
for num in ('1.2.5.','1.2.6.'):
 r.patch(203,'both',r'\textbf{'+num+'}',num,sid,reason)
r.page(203,'(Si X est paracompact et O_X mou ...','Pour n∈N, on a un isomorphisme canonique',
 'Every word, both symbol-composition formulas, all nested i+1 indices, the independent underlined sequence n, both sheaf-Hom rules and the exact final parentheses were compared. Native witness214 confirms the lexical rules, coefficient-field and N glyph constructions, and the unmatched closing parenthesis. Both references[4] and[16] and the complete page ending are preserved.',witness=214)
r.commit()
