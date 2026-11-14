"""Folio217: Banach-limit proof and the analytic-index definition."""
from review_helpers import Review
r=Review()
r.finding('216_220',5,'The single word compact is underlined',
 'The lower rule is confined to compact and ends before the stop. The existing emph span has the right extent.',
 'Sentence following the second displayed comparison',change='Render the already correct span with uline.',witness=228)
r.finding('216_220',6,'The projective-limit equality has no final punctuation',
 'The main page ends the display directly after its final parenthesis, and the attached layers already omit the extra stop.',
 'Projective-limit equality',change='Retain the display without a final stop.')
r.finding('216_220',7,'Soient S, X, E• begins an indented paragraph',
 'The attached layers already preserve the paragraph boundary after the author-note call and stop. This layout observation adds no content change under the governing prompt.',
 'Paragraph introducing the analytic index',verdict='layout observation accepted without further content patch',change='Retain the existing paragraph boundary.',witness=228)
sid=r.finding('216_220',8,'The R in Cℓ(Rp_*(E•)) has two horizontal lower rules',
 'The native witness plainly resolves two separate rules below R; the main scan agrees. Replace the earlier mathbb transcription with those literal strokes.',
 'Final analytic-index display',verdict='amended',change=r'Both layers: \mathbb{R} → \underline{\underline{R}}.',witness=228)
r.patch(217,'both',r'\mathbb{R}',r'\underline{\underline{R}}',sid,'Preserve the observed two horizontal lower rules beneath R.')
sid='ASTRA-II-GAMMA-217';reason='Both scans show a downturned right serif attached to the top bar of Γ, with no independently raised prime. Its construction matches the unprimed Γ_S letters in the directly inspected diagrams on176. The functor here takes the sheaf comparison F_p•→F_q• to the global-section map C(S,H_p•)→C(S,H_q•); no primed functor is printed or defined at this locus.'
r.own_finding(sid,217,'Unprimed Γ_S',r'\Gamma\prime_S',r'\Gamma_S',reason,'Proof, phrase le foncteur',kind='symbol',witness=228)
r.patch(217,'both',r"\Gamma'_S",r'\Gamma_S',sid,reason)
sid='ASTRA-II-FONTS-217';reason='Both structure-sheaf O letters have one individual lower rule; the coefficient-field C has two horizontal lower rules. Other C letters denote the displayed spaces of sections and have no such added rules.'
r.own_finding(sid,217,'Two singly underlined O letters and one doubly underlined coefficient C',r'\cO and \mathbb C',r'\underline{O} and \underline{\underline{C}}',reason,'Exactness statement and the module category in3.2.2',kind='font',witness=228)
r.patch(217,'both',r'\cO',r'\underline{O}',sid,reason,2)
r.patch(217,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason)
sid='ASTRA-II-AUTHOR-NOTE-217';reason='The call after correspondant and its author-note label both use raised numerical1 in baseline parentheses; the following stop belongs outside the call.'
r.own_finding(sid,217,'Numerical author-note label1',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Definition3.2.2 and bottom author note',kind='author_note_label',witness=228)
r.patch(217,'both',r'\footnote{voir (I 6.3). Pour une revue générale des foncteurs $K$, voir Exp.~IV.}',r'\SGAAuthorFootnote{1}{voir (I 6.3). Pour une revue générale des foncteurs $K$, voir Exp.~IV.}',sid,reason)
sid='ASTRA-II-UNDERLINE-217';reason='Only compact and the defining words indice analytique have lexical lower rules on this page; 3.2.2 is an ordinary unbold numbered paragraph, and the surrounding proof and definition prose are plain.'
r.own_finding(sid,217,'Two lexical emphasis groups and plain3.2.2','Emph spans and bold3.2.2',r'uline spans and ordinary numbered paragraph',reason,'Proof and index definition',kind='underline',witness=228)
r.patch(217,'both',r'\emph{compact}',r'\uline{compact}',sid,reason)
r.patch(217,'both',r'\emph{indice analytique}',r'\uline{indice analytique}',sid,reason)
r.patch(217,'both',r'\textbf{3.2.2.}',r'3.2.2.',sid,reason)
r.page(217,'C(Ū,C∞(V,F•)) → C(Ū,C²ʳ(V,F•))','ind.an(E•)=Cℓ(Rp_*(E•))∈K•(S).',
 'Every word and formula was compared in both layers, including the five displayed maps/equality, all closed-U accents, the degree-i versus complex-dot superscripts, the unprimed Γ_S, literal les applications linéaires continues, the EGA0_III13.2.3 locator, the plain class symbol Cℓ, and the final stop. The limit is lowercase with a leftward lower arrow. Native witness228 resolves the individual glyph rules and author-note geometry.',witness=228)
r.commit()
