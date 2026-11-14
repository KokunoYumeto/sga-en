"""Folio274: IV opening, Grothendieck group definition and lemma1.2."""
from review_helpers import Review, ROOT, underline_statement
r=Review()
r.finding('271_275',20,'EXPOSE IV without a stop, followed by the capitalized title with two lower rules',
 'The title and exposé label are on separate lines and their one-rule/two-rule constructions agree with the attached heading. The accents added to typed unaccented capitals follow the established convention.',
 'Opening exposé heading',change='Retain the existing heading and absence of a stop after IV.')
r.finding('271_275',21,'par L. ILLUSIE, the full line underlined',
 'The author surname is entirely capitalized and the rule spans par as well as the name. The current line preserves those features.',
 'Author line',change='Retain the current author line.')
r.finding('271_275',22,'triangulée is underlined in the opening definition',
 'The rule runs under that single word and ends before the stop. The attached emph span has the correct extent.',
 '1.1, opening sentence',change='Retain the grouping and render its inspected rule with uline.')
sid='ASTRA-IV-FONTS-274'
r.own_finding(sid,274,'Plain category C, lowercase ob and cl, and two compact heavy Z glyphs',
 r'Plain C, \Ob, \cl and \mathbb Z','Retain these occurrence-specific forms.',
 'The category letters C and C′ have no individual lower rules; the object and class operators are lowercase ob and cl. Both integer letters use the compact heavy/doubled-diagonal Z construction without added horizontal lower rules. Their existing mathbb transcription follows the accepted field-letter convention; no font-wide substitution is introduced.',
 'Definition1.1 and lemma1.2',kind='font',verdict='retained',witness=285)
sid='ASTRA-IV-UNDERLINE-274';reason='The defined words triangulée and additive and the Preuve label have lexical lower rules. Lemma1.2 has separately underlined word groups throughout its introduction and assertions(a),(b); all formulas, quantifiers, item letters and the mathematical coproduct keep their own glyphs. The number1.1 is plain. The named statement label and section heading retain the accepted heading convention.'
r.own_finding(sid,274,'Three lexical emphasis spans, full lemma word groups and plain1.1','Emph spans, plain lemma statement and bold1.1',r'Exact lexical uline groups and plain1.1',reason,'Definition, lemma1.2 and proof label',kind='underline',witness=285)
for word in ('triangulée','additive','Preuve.'):
    r.patch(274,'both',r'\emph{'+word+'}',r'\uline{'+word+'}',sid,reason)
r.patch(274,'both',r'\textbf{1.1.}','1.1.',sid,reason)
t=(ROOT/'build/page_packets/274/diplomatic.tex').read_text();a=t.index('Soient ',t.index(r'\textbf{Lemme 1.2.}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
old=t[a:b];r.patch(274,'both',old,underline_statement(old),sid,reason)
r.page(274,'EXPOSE IV; GROUPES DE GROTHENDIECK DES TOPOS ANNELES; par L.ILLUSIE','Pour b), il suffit de remarquer qu’on a',
 'Every definition and lemma word, exact triangle, primed object, homomorphism, sign exponent, coproduct index i≥0 and even shift2ni was compared with both layers. The two integer glyphs have no horizontal lower rules; C/C′ and object L are plain. The proof continues after the marker. The broad checker271_275#23 also mentions the next page, so its combined scope is recorded with the275 inspection rather than inferred here.',witness=285)
r.commit()
