"""Folio192: finite-cover resolution, derived composites and proof emphasis."""
from review_helpers import Review
r=Review()
for i,region in [(7,'Opening definition of the resolution'),(8,'First case, its components'),(9,'Length assertion before the final vanishing display'),(10,'Second case, its components')]:
 r.finding('191_195',i,'C with a raised dot, followed by(E)',
 'The small raised complex dot is visible at this exact occurrence. It is retained as C^bullet(E); the separately printed length symbol N′ retains its prime.',region,witness=203 if i in (7,8) else None)
for i,printed,region in [(11,'séparé has a word rule','First case heading'),(12,'noethérien has a word rule','Second case heading'),(13,'The final séparé has a word rule','Last paragraph, description of the quasi-compact open')]:
 r.finding('191_195',i,printed,'The existing lexical scope matches the source. Preserve the precise word with a literal underline helper; neighboring proof words remain plain.',region,change='Use uline for the same inspected word group.')
for i,region,n in [(14,'First derived-composite display',4),(15,'Second derived-composite display',3)]:
 r.finding('191_195',i,f'{n} R letters with two horizontal lower rules, and two wave-over-headless-bar signs',
 'Every listed R has two separate rules beneath it in both scans. The attached headless relations, composed functors, pullbacks and arguments agree. Preserve the observed horizontal rules literally, independently of the plain R^n forms below.',
 region,verdict='amended',change=r'Retain the headless relations and replace the inspected mathbb R forms by \underline{\underline{R}}.',witness=203)
r.finding('191_195',16,'R^nQ(f_*f^*E) ≃ f_*R^nQ(f^*E), for n≥0',
 'The lower relation stroke has no arrowheads. Both R letters in this degree-n formula are plain, as attached; all functor stars and the degree bound agree.',
 'Third display')
sid='ASTRA-II-R-192';reason='All four R letters in the first composite and all three in the second have two horizontal rules below R. Those seven occurrences were separately compared in both scans. The four later R^n letters remain plain.'
r.own_finding(sid,192,'Seven literal double-underlined R letters',r'\mathbb R',r'\underline{\underline{R}}',reason,'First and second derived-composite displays',kind='font',witness=203)
r.patch(192,'both',r'\mathbb R',r'\underline{\underline{R}}',sid,reason,7)
sid='ASTRA-II-O-192';reason='The opening structure-sheaf O has a single horizontal rule beneath O alone, with S outside it.'
r.own_finding(sid,192,'One underlined structure-sheaf O',r'\mathcal O',r'\underline{O}',reason,'Opening line',kind='font',witness=203)
r.patch(192,'both',r'\mathcal O',r'\underline{O}',sid,reason)
sid='ASTRA-II-UNDERLINE-192';reason='The only proof-word emphasis spans are séparé at the first case heading, noethérien at the second, and séparé at the end of the final open-set description. Their existing groups match the three observed rules exactly.'
r.own_finding(sid,192,'Three single-word underlines',r'Three \emph groups',r'Three matching \uline groups',reason,'Both case headings and final paragraph',kind='underline')
r.patch(192,'both',r'\emph{',r'\uline{',sid,reason,3)
r.page(192,'affines. Soit E un O_S-Module acyclique','Comme dans le cas1°), on a',
 'Every proof word, all four resolution dots, the two length-prime symbols, every R and functor star, all five displays and the final open-set description were compared. Native witness203 confirms the first two complex dots and the exact seven double-underlined R letters. The degree-n R letters and proof text outside the three observed word rules remain plain.',witness=203)
r.commit()
