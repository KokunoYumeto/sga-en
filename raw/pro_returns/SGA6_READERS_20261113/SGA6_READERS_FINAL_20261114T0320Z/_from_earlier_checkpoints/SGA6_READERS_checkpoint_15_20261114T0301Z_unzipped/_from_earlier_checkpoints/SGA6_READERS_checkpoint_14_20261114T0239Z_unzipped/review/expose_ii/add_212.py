"""Folio212: differential-operator topologies and literal field glyphs."""
from review_helpers import Review
r=Review()
sid=r.finding('211_215',3,'In item(i), only continues has a lexical lower rule',
 'The main scan and native witness show a rule below continues, with les, sont and the following parenthesis plain. The attached emphasis group already isolates that exact word; use the literal rule formatter.',
 'Last body line, item(i)',verdict='confirmed with literal underline formatter',change='Use uline on the existing isolated continues group.',witness=223)
r.patch(212,'both',r'\emph{continues}',r'\uline{continues}',sid,'Preserve the isolated lower rule on continues.')
sid='ASTRA-II-C-212';reason='All fourteen coefficient-field C letters have two horizontal lower rules: ten in the tensor-product proof and four as Diff subscripts. The function-space C letters remain plain. Explicit script braces keep each changed Diff subscript a single mathematical field.'
r.own_finding(sid,212,'Fourteen coefficient C letters with double lower rules',r'\mathbb C',r'\underline{\underline{C}}',reason,'Opening tensor-product proof and four Diff subscripts',kind='font',witness=223)
r.patch(212,'both',r'_\mathbb C',r'_{\underline{\underline{C}}}',sid,reason,4)
r.patch(212,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason,10)
sid='ASTRA-II-NZ-212';reason='The N in the differential-order parameter and the Z in the Sobolev-order parameter each have two horizontal lower rules.'
r.own_finding(sid,212,'One N and one Z with double lower rules',r'\N and \Z',r'\underline{\underline{N}} and \underline{\underline{Z}}',reason,'Paragraph3.1.3, two parameter ranges',kind='font',witness=223)
r.patch(212,'both',r'\N',r'\underline{\underline{N}}',sid,reason)
r.patch(212,'both',r'\Z',r'\underline{\underline{Z}}',sid,reason)
sid='ASTRA-II-PHI-212';reason='The two displayed map labels and the final item’s phi_r have closed loops crossed by stems. Use phi at these three inspected occurrences.'
r.own_finding(sid,212,'Three closed-loop phi glyphs',r'\varphi',r'\phi',reason,'Two operator maps and item(i)',kind='symbol',witness=223)
r.patch(212,'both',r'\varphi',r'\phi',sid,reason,3)
sid='ASTRA-II-NOTE-212';reason='The call after complexes and the sole complete author note have raised numerical1 within baseline parentheses.'
r.own_finding(sid,212,'Explicit numerical1 author note',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Paragraph3.1.3 call and complete author note',kind='author_footnote',witness=223)
r.patch(212,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',sid,reason)
sid='ASTRA-II-PARAGRAPH-212';reason='The numerical identifier3.1.3. has plain typed numerals with its printed stop.'
r.own_finding(sid,212,'Plain3.1.3.',r'\textbf{3.1.3.}','3.1.3.',reason,'Middle paragraph opening',kind='font')
r.patch(212,'both',r'\textbf{3.1.3.}','3.1.3.',sid,reason)
sid='ASTRA-II-PREUVE-212';reason='The opening Preuve label has a lower word rule; its following proof prose is plain.'
r.own_finding(sid,212,'Underlined Preuve',r'\emph{Preuve.}',r'\uline{Preuve.}',reason,'Opening proof label',kind='underline')
r.patch(212,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason)
r.page(212,'Preuve. Il est clair que u_X est continue.','(i) les phi_r sont continues(l’espace d’arrivée est un espace de Banach; author note ends dans le cas réel).',
 'Every word, finite-rank tensor expression, differential order, Sobolev shift r−n, map label and display punctuation was compared, together with the entire author note. The Hom-to-C-infinity comparison has a headless sign, resolved in the enlarged main region and witness; the sheaf Hom alone is underlined. The wording extension des scalaires is printed literally and retained. Native witness223 confirms all coefficient and parameter glyph rules, the three closed phi forms and isolated continues emphasis.',witness=223)
r.commit()
