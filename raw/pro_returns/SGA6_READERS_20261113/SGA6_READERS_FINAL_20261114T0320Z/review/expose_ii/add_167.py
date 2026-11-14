"""Folio167: category notation, derived R, and the raised-star author note."""
from review_helpers import Review,ROOT
from source_emphasis import underline_words
r=Review()
obs={
11:('The first line starts 0→L_1→L_0→L→0. D’après','The displayed-on-the-line short sequence belongs at the beginning of167, and both attached markers precede it. The D’% source join does not alter D’après.','First line'),
12:('The first derived R has a double underline; Hom is plain','The two parallel rules under R encode the double-struck derived-functor form. The attached mathbb R preserves that distinction from the plain Hom.','First member of the derived-Hom display'),
13:('The second derived R has the same double underline','The two R letters have matching rules. Both attached mathbb R forms match.','Second member of the derived-Hom display'),
14:('Soit, un schéma noethérien, Le foncteur canonique are underlined','The complete final word canonique is on this folio, above the author note. Both attached emphasis spans cover the observed lexical groups and leave S independently typed.','Proposition2.2.2 opening')}
for n,(printed,reason,region) in obs.items():r.finding('166_170',n,printed,reason,region)
sid='ASTRA-II-AB-167';reason='The three A letters and one B in Remarques2.1.3.1 are ordinary typed capitals. They are the same abelian categories introduced on165; the identity of their objects is preserved while their printed plain form is restored. The source scope continues the typography finding166–170#10.'
r.own_finding(sid,167,'Three plain category A letters and one plain B',r'\mathcal A, \mathcal B','A, B',reason,'Remarks and D^−(A), D^+(A)',kind='font')
r.patch(167,'both',r'\mathcal A','A',sid,reason,3)
r.patch(167,'both',r'\mathcal B','B',sid,reason)
sid='ASTRA-II-PHI-167';reason='All six phi occurrences have the closed-loop form crossed by a stroke: four in the opening argument and two in the derived-Hom display. Use phi for these observed glyphs in both layers.'
r.own_finding(sid,167,'Six closed phi glyphs',r'\varphi',r'\phi',reason,'Opening comparison maps and derived-Hom arguments',kind='symbol')
r.patch(167,'both',r'\varphi',r'\phi',sid,reason,6)
sid='ASTRA-II-O-167';reason='The structure-sheaf O in O_S-Modules is a plain typed O with an individual underline. Its subscript S is outside the rule. Preserve this exact inspected form.'
r.own_finding(sid,167,'Underlined O_S',r'\mathcal O_S',r'\underline{O}_S',reason,'Notations2.2.1, first paragraph',kind='font')
r.patch(167,'both',r'\mathcal O',r'\underline{O}',sid,reason)
sid='ASTRA-II-NOTE-167';reason='The call after Proposition2.2.2 and the label at the foot both show a high star inside baseline parentheses. Preserve the raisedstar geometry and the complete author text, independently of editorial notes.'
r.own_finding(sid,167,'Raised star within baseline parentheses at call and note',r'\footnote',r'\SGAAuthorFootnote{raisedstar}',reason,'Proposition label and author-note label',kind='other')
r.patch(167,'both',r'\footnote{Ce résultat',r'\SGAAuthorFootnote{raisedstar}{Ce résultat',sid,reason)
sid='ASTRA-II-UNDERLINE-167';reason='The two retained emphasis spans are the underlined opening of Proposition2.2.2. The notation paragraph and its pseudo-coherence descriptions are plain and stay outside the formatter. Its mathematical units and the explicit author note are preserved.'
r.own_finding(sid,167,'Two underlined proposition word groups',r'\emph groups',r'\uline on the inspected words',reason,'Final proposition opening',kind='underline')
old=(ROOT/'build/page_packets/167/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
new,stats=underline_words(old);assert stats['inspected_emphasis_groups']==2
r.patch(167,'both',old,new,sid,reason)
r.page(167,'0→L_1→L_0→L→0. D’après ce qu’on a vu plus haut','Le foncteur canonique; author note ends en première lecture.',
    'All proof prose, remarks, displays, notation definitions and the complete author note directly compared. The final word canonique is on167, before the folio168 display.')
r.commit()
