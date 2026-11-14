"""Folio208: induction limit, local isomorphisms and statement rules."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('206_210',4,'Lim has a capital L and no arrow; its lower index is S′∋s',
 'Both scans show the capitalized operator directly above the membership condition, with no arrow in the intervening space. The attached operatorname*{Lim} and its index already agree. The right-hand Hom is plain and the left sheaf-Hom has its own underline.',
 'Display in the proof of Corollary2.6',change='Retain the attached capitalized arrowless Lim.',witness=219)
sid='ASTRA-II-O-208';reason='The sole structure-sheaf O in the opening proof has one individual lower rule.'
r.own_finding(sid,208,'One singly underlined O_X',r'\cO_X',r'\underline{O}_X',reason,'Opening proof after the first display',kind='font')
r.patch(208,'both',r'\cO',r'\underline{O}',sid,reason)
sid='ASTRA-II-UNDERLINE-208';reason='All lexical groups of Corollary2.6 and Proposition2.7 have word rules, with the numerical reference(2.5) plain. Corollary2.8 continues this pattern, including its three resp. abbreviations and the explanatory parenthesis. Each of the three Preuve labels is underlined; proof prose and the words pour/ouvert inside proof displays are plain. The native witness resolves the three lower resp. rules individually.'
r.own_finding(sid,208,'Exact word rules in three statements and three Preuve labels','Plain statement prose; emph proof labels',r'Lexical uline groups',reason,'Three statement portions and proof labels',kind='underline',witness=219)
t=(ROOT/'build/page_packets/208/diplomatic.tex').read_text()
for p in r.patches:t=t.replace(p['old'],p['new'])
for label in ('Corollaire 2.6.','Proposition 2.7.'):
 a=t.index('Soient ',t.index(r'\textbf{'+label+'}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
 old=t[a:b];r.patch(208,'both',old,underline_statement(old,protected=(r'\(2\.5\)',)),sid,reason)
a=t.index('Soient ',t.index(r'\textbf{Corollaire 2.8.}'))
old=t[a:];r.patch(208,'both',old,underline_statement(old),sid,reason)
r.patch(208,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason,3)
r.page(208,'Preuve. D’après(T.F.II4.17.1), on a','Il existe alors un voisinage S′',
 'All words, display punctuation, the baseline restrictions X|S′ and Y|S′, each membership and inverse-image index, the plain degree-indexed R and the capitalized arrowless Lim were compared. The source comma after que in the second proof is visible and retained. Native witness219 confirms the limit form and exact final corollary word rules, including all three resp. abbreviations.',witness=219)
r.commit()
