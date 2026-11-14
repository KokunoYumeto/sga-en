"""Direct image comparison of Proposition1.2 and its first proof paragraphs."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('161_165',5,'Folio162 begins thèses (1.1 (i) et (ii) respée).',
    'The preceding folio ends hypo-, and the new folio begins thèses. Both attached layers already keep hypo% above the marker and thèses below it. Respée is visibly printed and is retained.',
    'First line and previous folio boundary',change='Retain the exact existing hypo-/thèses split.')
r.finding('161_165',6,'Three baseline ellipsis dots in the truncated complex',
    'The three typed stops are below the arrow midline. Both attached ldots forms preserve their baseline position.',
    'Proof b), truncated-complex display')
sid='ASTRA-II-C-162';reason='All twenty-eight category C letters on the inspected folio are typed letters with individual underlines. Their fiber subscripts remain outside the rule. The functor letters D and K retain their separate plain forms.'
r.own_finding(sid,162,'Twenty-eight underlined category C letters',r'\mathcal C',r'\underline{C}',reason,'All category letters',kind='font')
r.patch(162,'both',r'\mathcal C',r'\underline{C}',sid,reason,28)
sid='ASTRA-II-SITE-162';reason='The single standalone S in où l’on prend pour S le site ponctuel has a visible underline. It denotes the punctual site in this proof invocation; the object S in fiber subscripts remains unchanged.'
r.own_finding(sid,162,'Underlined site S in the proof parenthesis',r'pour $S$ le site',r'pour $\underline{S}$ le site',reason,'Proof a), final parenthesis',kind='font')
r.patch(162,'both',r'pour $S$ le site',r'pour $\underline{S}$ le site',sid,reason)
sid='ASTRA-II-UNDERLINE-162';reason='All lexical groups in the continued statement and items a)–d) carry rules. The printed reference numbers, enumeration/item references b) and c), and mathematical units carry their own typography and are excluded. The proof heading Preuve is underlined, while its body is plain. The formatter verifies literal token identity after removing its newly added wrappers.'
r.own_finding(sid,162,'Underlined proposition word groups and Preuve heading','Plain proposition prose; emph Preuve',r'\uline on the inspected words',reason,'Statement through item d), then proof heading',kind='underline')
old=(ROOT/'build/page_packets/162/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
start=old.index('\n')+1;end=old.index(r'\end{enumerate}')+len(r'\end{enumerate}')
statement=old[start:end]
new=old[:start]+underline_statement(statement,[r'\(I [^)]+\)',r'\(1\.1 \(i\)',r'\(ii\)',r'(?<![A-Za-z])(?:b|c)\)'])+old[end:]
assert new.count(r'\emph{Preuve.}')==1
new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
r.patch(162,'both',old,new,sid,reason)
r.page(162,'thèses (1.1 (i) et (ii) respée).','ce qui démontre l’assertion.',
    'Complete statement, proof, quotient, truncation sequence and page boundary compared. All displayed cohomological degrees and category subscripts were inspected.')
r.commit()
