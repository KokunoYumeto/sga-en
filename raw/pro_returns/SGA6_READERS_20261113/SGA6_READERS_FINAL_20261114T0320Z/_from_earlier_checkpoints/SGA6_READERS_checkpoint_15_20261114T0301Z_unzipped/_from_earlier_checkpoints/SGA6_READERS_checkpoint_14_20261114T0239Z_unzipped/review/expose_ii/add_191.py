"""Folio191: unbounded coherer proposition, exact glyphs and author note."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
sid=r.finding('191_195',1,'The R in E→RQE→E has two horizontal lower rules',
 'Both rules are visible in the main scan and native witness. Preserve those two literal strokes while retaining the complete unit-counit composite.',
 'Opening composite',verdict='amended',change=r'Use \underline{\underline{R}}QE in both layers.',witness=202)
r.patch(191,'both',r'\mathbb R',r'\underline{\underline{R}}',sid,'Preserve the two directly observed horizontal rules beneath the composite’s R.')
r.finding('191_195',2,'The raised numerical1 call lies after i>N and before the display stop',
 'The attached split call/text placement agrees. The call and matching complete author note use explicit numerical1 between baseline parentheses.',
 'Proposition3.7 vanishing display and author note',change='Retain the printed placement and give both call and note explicit label1.',witness=202)
r.finding('191_195',3,'The tilde is over Γ alone; S is the lower index',
 'The base of the handwritten tilde is Γ. The attached widetilde{Γ}_S preserves this exact scope.',
 'Opening of proof(a)')
r.finding('191_195',4,'Preuve de is underlined, while a). is plain',
 'The observed rule ends before the item label. The existing emphasis scope agrees and is preserved with a literal word-rule helper.',
 'Proof heading',change=r'\uline{Preuve de} a).')
r.finding('191_195',5,'The finite right resolution is E with a raised dot',
 'The raised round dot after E is visible. The final N′ on the page has a separate vertical prime. Retain the attached E^bullet for the complex and N′ for the number of affine opens.',
 'Proof(a), finite right resolution')
r.finding('191_195',6,'Soit(U_i) follows the preceding parenthetical in the same paragraph',
 'The scan continues directly in the same line after the stop. Both attached layers already have the same paragraph continuity.',
 'Last body line')
sid='ASTRA-II-PHI-191';reason='The inclusion functor in Proposition3.7(b) is marked by a closed loop with a crossing stem, confirmed in the native witness. Use the phi glyph for this inspected occurrence.'
r.own_finding(sid,191,'Closed-loop phi in the inclusion functor',r'\varphi',r'\phi',reason,'Proposition3.7(b) display',kind='symbol',witness=202)
r.patch(191,'both',r'\varphi',r'\phi',sid,reason)
sid='ASTRA-II-O-191';reason='The structure-sheaf O in the acyclic-module clause has one lower rule beneath O alone. Its S index remains outside.'
r.own_finding(sid,191,'One underlined structure-sheaf O',r'\mathcal O',r'\underline{O}',reason,'Proof(a), final paragraph',kind='font')
r.patch(191,'both',r'\mathcal O',r'\underline{O}',sid,reason)
sid='ASTRA-II-NOTES-191';reason='The display call and matching author-note label both show a raised numerical1 within baseline parentheses. Their exact formula placement and complete note text are retained.'
r.own_finding(sid,191,'Explicit numerical1 call and label',r'\footnotemark and \footnotetext',r'\SGAAuthorFootMark{1} and \SGAAuthorFootText{1}',reason,'Proposition3.7 display and page foot',kind='author_footnote',witness=202)
r.patch(191,'both',r'\footnotemark',r'\SGAAuthorFootMark{1}',sid,reason)
r.patch(191,'both',r'\footnotetext{',r'\SGAAuthorFootText{1}{',sid,reason)
sid='ASTRA-II-UNDERLINE-191';reason='All lexical groups of the proposition are underlined, including de between the category expressions in(b). The reference(3.5), mathematical units, the word pour inside the vanishing display, author note and item labels are plain. Only Preuve de is underlined in the proof heading; proof and remark prose are plain.'
r.own_finding(sid,191,'Proposition word rules with independently typed math and note','Plain proposition prose',r'\uline on the inspected lexical groups',reason,'Proposition3.7 and proof heading',kind='underline')
old=(ROOT/'build/page_packets/191/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
a=old.index("Sous l'hypothèse",old.index(r'\textbf{Proposition 3.7.}'));b=old.index(r'\[',a)
new=old[:a]+underline_statement(old[a:b],[r'\(3\.5\)'])+old[b:]
a=new.index('Alors :');b=new.index(r'\emph{Preuve de}',a)
new=new[:a]+underline_statement(new[a:b])+new[b:]
new=new.replace(r'\emph{Preuve de}',r'\uline{Preuve de}')
r.patch(191,'both',old,new,sid,reason)
r.page(191,'on se ramène aussitôt au cas où E∈ob Qcoh(S).','Soit(U_i) un recouvrement fini de S par N′ ouverts; note ends dimension de Krull≤N.',
 'All proof and remark prose, the complete proposition, every degree bound, both complex and numerical-index symbols, and the complete numerical author note were compared. Native witness202 confirms the literal double-underlined R, closed phi and call placement. The vanishing display’s lexical pour is plain.',witness=202)
r.commit()
