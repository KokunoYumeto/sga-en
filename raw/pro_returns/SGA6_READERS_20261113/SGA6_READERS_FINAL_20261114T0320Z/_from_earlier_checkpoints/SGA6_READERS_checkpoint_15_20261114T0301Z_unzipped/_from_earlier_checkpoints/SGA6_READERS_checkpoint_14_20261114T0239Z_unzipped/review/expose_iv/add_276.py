"""Folio276: universal additive group, convention note and thick subcategory."""
from review_helpers import Review, ROOT, underline_statement
r=Review()
sid='ASTRA-IV-PHI-276'
r.own_finding(sid,276,'The homomorphism label has an open/cusped upper phi form with a descending stem',r'\varphi',r'Retain \varphi.',
 'The native witness and enlarged main region show the curled upper form with the central stem descending beneath it, without an upper protruding stem through a closed oval. The inherited varphi retains that observed local glyph. Its map is the displayed k(D_A^b(C))→k(A) defined by the preceding alternating cohomology class.',
 'Last displayed homomorphism',kind='symbol',verdict='retained',witness=287)
sid='ASTRA-IV-AUTHOR-NOTE-276';reason='The call after the parenthetical ambient-category explanation and the bottom note both show a raised numerical1 inside baseline parentheses. The following stop remains outside the call.'
r.own_finding(sid,276,'Explicit numerical author-note label1',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Convention note following1.5.2',kind='author_note_label',witness=287)
r.patch(276,'both',r'\footnote{La notation',r'\SGAAuthorFootnote{1}{La notation',sid,reason)
sid='ASTRA-IV-UNDERLINE-276';reason='Lemma1.6 has lexical lower rules throughout, including its explanatory i.e. parenthesis and the words où/est défini par after the display. The mathematical expressions and locators([V]I1.2.3)/(1.5.2) remain independent and plain. The proof label alone is underlined; all preceding continuation prose, proof prose and the full author note are plain.'
r.own_finding(sid,276,'Lemma1.6 word groups and the Preuve label','Plain lemma prose and emph proof label',r'Exact lexical uline groups',reason,'Lemma1.6 and proof label',kind='underline',witness=287)
t=(ROOT/'build/page_packets/276/diplomatic.tex').read_text();a=t.index('Soient ',t.index(r'\textbf{Lemme 1.6.}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
old=t[a:b];r.patch(276,'both',old,underline_statement(old,protected=(r'\(1\.5\.2\)',)),sid,reason)
r.patch(276,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason)
r.page(276,'induite par cl_{K^b(A)/K^{b,∅}(A)}(1.1) est une application additive universelle','varphi:k(D_A^b(C)) → k(A).',
 'Every body and author-note word, all three crossed-loop acyclic markers, the two numbered group definitions, each degree/subcategory index, the headed isomorphism in the lemma and the final proof maps were compared with both layers. The unindexed alternating sum and its final comma are printed as attached. Formula1.5.2 has no final punctuation, whereas1.5.3 has a stop. The note explicitly records the author’s change of k(A) convention and is preserved in full. Native witness287 and a main-scan detail resolve the local varphi and note label.',witness=287)
r.commit()
