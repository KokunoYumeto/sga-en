"""Folio180: final Stein-lemma clause, proof and explicit author note."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('176_180',22,'The page begins c) Posons A=Γ(S,O_S)',
    'The item label c) and the declaration are on the first printed line. Both attached markers already precede the item command.',
    'First line',change='Retain the existing marker before item(c).')
r.finding('176_180',23,'Hom alone has an underline in Hom(G,E)',
    'The rule covers the three operator letters and leaves the arguments outside. Both attached layers already preserve that exact grouping.',
    'First proof paragraph')
r.finding('176_180',24,'The body ends with the starred-arrow factorization and a comma',
    'The complete displayed factorization belongs to180; the subsequent où Lib(A) phrase is absent above the footnote. Both attached boundaries already end the body after this display.',
    'Last display and page boundary',change='Retain the existing boundary after the displayed factorization.')
sid='ASTRA-II-C-180';reason='The five category C letters in the proof have individual rules. The two primes and all zero/S indices remain outside those rules.'
r.own_finding(sid,180,'Five individually underlined category C letters',r'\mathcal C',r'\underline{C}',reason,'Full proof of2.4.3',kind='font')
r.patch(180,'both',r'\mathcal C',r'\underline{C}',sid,reason,5)
sid='ASTRA-II-O-180';reason='The structure-sheaf O in the opening definition of A has an individual rule; its S index remains outside.'
r.own_finding(sid,180,'One underlined structure-sheaf O',r'\mathcal O',r'\underline{O}',reason,'Opening declaration A=Γ(S,O_S)',kind='font')
r.patch(180,'both',r'\mathcal O',r'\underline{O}',sid,reason)
sid='ASTRA-II-NOTE-180';reason='The call after the Lib/Loclib alternative and the author-note label both use numerical1 raised inside baseline parentheses. The complete note and its reference(I2.15.1) were compared.'
r.own_finding(sid,180,'Parenthesized raised1 at call and author note',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Second proof assertion and page foot',kind='other')
r.patch(180,'both',r'\footnote{Lib et Loclib',r'\SGAAuthorFootnote{1}{Lib et Loclib',sid,reason)
sid='ASTRA-II-UNDERLINE-180';reason='Every lexical group of item(c), including the parenthetical description of pseudo-coherence, is underlined. The formulas and category names remain independently typed. The proof and author note are plain except the Preuve heading. This completes the page180 occurrences of checker176–180#7.'
r.own_finding(sid,180,'Underlined words of item(c) and Preuve','Plain statement prose',r'\uline on inspected lexical groups',reason,'Statement continuation and proof heading',kind='underline')
old=(ROOT/'build/page_packets/180/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
start=old.index('\n')+1;end=old.index(r'\emph{Preuve.}')
new=old[:start]+underline_statement(old[start:end])+old[end:]
new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
r.patch(180,'both',old,new,sid,reason)
r.page(180,'c) Posons A=Γ(S,O_S)','K^−(Lib(S))→(*)K^−(Lib(A))→(**)D(A),; author note ends d’après(I2.15.1).',
    'All statement and proof words, functors, references, underlined Hom, arrow labels and the complete numerical author note were compared. The printed branch abbreviation respée is retained.')
r.commit()
