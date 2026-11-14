"""Folio173: the ample-family category and three quotient functors."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
sid=r.finding('171_175',8,'Six L letters naming L(S) are individually underlined',
    'The introduced category, its occurrence in(a), the relative-coherence clause, the two quotient terms and F^i∈ob L(S) all carry rules under L alone. The generating invertible sheaves L_i are plain. This decision covers the six actual page173 occurrences; the continuation is recorded page by page.',
    'Lemma2.2.8, all six L(S) occurrences',verdict='not applied and now applied',change='Underline exactly these six category L letters in both layers.')
r.patch(173,'both','L(S)',r'\underline{L}(S)',sid,'Restore the individual category-letter rule at the six inspected occurrences.',6)
sid='ASTRA-II-O-173';reason='All five sheaf O letters are individually underlined: two in the opening isomorphism, two in its consequence and one in the lemma hypothesis. The origin labels O_1,O_2 stay plain.'
r.own_finding(sid,173,'Five underlined structure-sheaf O letters',r'\mathcal O',r'\underline{O}',reason,'Opening argument and lemma hypothesis',kind='font')
r.patch(173,'both',r'\mathcal O',r'\underline{O}',sid,reason,5)
sid='ASTRA-II-ACYCLIC-173';reason='The denominators in both bounded-above quotients and the bounded quotient carry the same crossed-loop superscript read on160. They are the acyclic subcategories included in the corresponding K categories; localization sends each acyclic complex to the zero object of D(Qcoh(S)). Retain the attached varnothing notation for this specified kernel.'
r.own_finding(sid,173,'Crossed-loop superscripts on all three quotient denominators',r'\varnothing',r'Retain \varnothing',reason,'The three quotient-functor displays',kind='font',verdict='confirmed')
sid='ASTRA-II-UNDERLINE-173';reason='All lexical groups of Lemma2.2.8 and its three items are underlined, including both resp. clauses and the et joining the first two displays. The references, mathematical units, item labels and newly restored category rules remain independent. The proof continuation above the lemma is plain.'
r.own_finding(sid,173,'Underlined lemma and item prose','Plain lemma and item prose',r'\uline on inspected lexical groups',reason,'Lemma2.2.8 and items(a)–(c)',kind='underline')
old=(ROOT/'build/page_packets/173/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
start=old.index('Soient ',old.index(r'\textbf{Lemme 2.2.8.}'))
new=old[:start]+underline_statement(old[start:],[r'\(2\.2\.[15]\)',r'\(2\.0\)',r'\(I [12]\.[23]\)'])
r.patch(173,'both',old,new,sid,reason)
r.page(173,'inversible sur S est trivial.','K^b(Loclib(S))/K^{b,∅}(Loclib(S))→D(Qcoh(S))',
    'The doubled-origin conclusion, entire lemma hypothesis and all three items were compared, including the tensor signs, interval endpoints, kernel symbols and final unpunctuated quotient display.')
r.commit()
