"""Folio 216: three proof labels, the assertion typography and printed plural."""
from review_helpers import Review, ROOT, underline_statement
r=Review()
for index,label in [(1,'(b)'),(2,"(a')"),(3,'(a)')]:
    r.finding('216_220',index,'Preuve de is underlined; '+label+'. remains plain',
      'Both scans show the lexical rule ending after de. The attached grouping already leaves the assertion label and stop outside it.',
      'Proof label '+label,change='Retain the grouping; render the inspected lexical rule with uline.',witness=227)
sid=r.finding('216_220',4,"En d'autre termes",
 'The main scan and native witness both print autre without final s before plural termes. Preserve that reading diplomatically and supply the agreeing plural autres in the corrected layer.',
 "Proof of (a'), sentence beginning En d'autre termes",verdict='not applied and now applied',
 change="Current only: En d'autre termes → En d'autres termes.",witness=227)
r.patch(216,'current',"En d'autre termes", "En d'autres termes",sid,'Supply the plural s in the corrected layer; retain the source spelling diplomatically.')
sid='ASTRA-II-Z-216';reason='The integer Z in assertion(b) has two horizontal lower rules, independently of the lexical assertion rules and the singly underlined sheaf F.'
r.own_finding(sid,216,'One Z with two horizontal lower rules',r'\Z',r'\underline{\underline{Z}}',reason,'Assertion(b), parameter r',kind='font',witness=227)
r.patch(216,'both',r'\Z',r'\underline{\underline{Z}}',sid,reason)
sid='ASTRA-II-AUTHOR-NOTE-216';reason='The call after Th.6 and its bottom-of-page note both show a raised numerical1 inside baseline parentheses.'
r.own_finding(sid,216,'Explicit numerical author-note label1',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Proof of(b), citation and author note',kind='author_note_label',witness=227)
r.patch(216,'both',r'\footnote{qui se généralise aisément aux complexes elliptiques.}',r'\SGAAuthorFootnote{1}{qui se généralise aisément aux complexes elliptiques.}',sid,reason)
sid='ASTRA-II-UNDERLINE-216';reason='The opening continuation has lexical rules through cohomologie, including i.e.; the words of assertions(b) and(a′) are underlined with their formulas independently marked. All three Preuve de labels have lexical rules, while the labels(b),(a′),(a) and the surrounding proof prose remain plain.'
r.own_finding(sid,216,'Opening continuation, two assertion word groups and three Preuve de rules','Plain assertions and emph labels',r'Exact lexical uline groups',reason,'Opening two assertions and the three proof labels',kind='underline',witness=227)
t=(ROOT/'build/page_packets/216/diplomatic.tex').read_text()
for p in r.patches:
    if p['layer']=='both':t=t.replace(p['old'],p['new'])
a=t.index('est un\nquasi-isomorphisme');b=t.index('\n\n(b)',a)
old=t[a:b];r.patch(216,'both',old,underline_statement(old),sid,reason)
a=t.index('(b) Pour ')+len('(b) ');b=t.index('\n\n'+r'\emph',a)
old=t[a:b];r.patch(216,'both',old,underline_statement(old),sid,reason)
a=t.index("(a') Pour ")+len("(a') ");b=t.index('\n\n'+r'\emph',a)
old=t[a:b];r.patch(216,'both',old,underline_statement(old),sid,reason)
r.patch(216,'both',r'\emph{Preuve de}',r'\uline{Preuve de}',sid,reason,3)
r.own_finding('ASTRA-II-ARROW-216',216,'Headed rightward arrow with a detached wavy upper head stroke',r'\longrightarrow','Retain the unlabelled headed arrow.',
 'At ten pixels per PDF point the detached upper stroke occupies the upper branch of the right-hand head and ends at the same right edge as the shaft and lower branch. It has no independently centered tilde above the shaft. The nearby prose arrows have the same rightward head construction. The second scan and the coordinator’s independent regional reading agree; retain the existing unlabelled arrow.',
 'Assertion(a′), displayed comparison of sheaf complexes',kind='symbol',verdict='retained',witness=227)
r.page(216,"C′(S,C∞(V,F•)) → C′(S,C²ʳ(V,F•))","Preuve de(a). Il s’agit de montrer que, pour tout ouvert relativement compact U de S, le morphisme",
 'Every word and formula was compared in both layers. The C′ rules stop before the primes; the sheaf F and M rules leave their subscripts and raised complex dots outside. The first assertion and the cone argument retain headed comparison arrows. Both [12]2.3 in the first proof and [11]2.3 in the later proof are the printed locators. The author note and missing plural s were checked in the native witness. The final morphism begins on the next folio.',witness=227)
r.commit()
