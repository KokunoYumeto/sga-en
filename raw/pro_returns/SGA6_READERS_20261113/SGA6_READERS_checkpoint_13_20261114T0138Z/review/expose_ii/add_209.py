"""Folio209: boundary, local triviality statements and a printed singular noun."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('206_210',5,'The first line begins de s tel que and contains the restriction isomorphism',
 'The complete preceding page ends voisinage S′. This page starts de s tel que, followed by the map and soit un isomorphisme. Both attached chunks already put the marker before de.',
 'Complete first line',change='Retain the existing marker before de s tel que.')
sid=r.finding('206_210',6,'forment un système fondamental de voisinage de Z_s',
 'The main scan and native witness print singular voisinage. The plural subject is the family of opens Z|S′, and the same neighborhood-basis terminology in the governing hypotheses on208 uses voisinages. Correct the noun ending in current while preserving the literal singular in diplomatic; the indexed family and its maps do not change.',
 'Proof of Corollary2.8',verdict='confirmed; current correction now applied',change='Current alone: système fondamental de voisinage de Z_s becomes ...voisinages de Z_s.',witness=220)
r.patch(209,'current','système fondamental de voisinage de $Z_s$','système fondamental de voisinages de $Z_s$',sid,'Restore the plural noun for the displayed family of neighborhood opens in current only.')
sid='ASTRA-II-O-209';reason='Both structure-sheaf O letters in Corollary2.10 have one lower rule, with their X indices outside it.'
r.own_finding(sid,209,'Two individually underlined O letters',r'\cO',r'\underline{O}',reason,'Corollary2.10, real and complex module structures',kind='font',witness=220)
r.patch(209,'both',r'\cO',r'\underline{O}',sid,reason,2)
sid='ASTRA-II-C-209';reason='The coefficient C in Corollary2.10 has two distinct horizontal lower rules, visible independently of the preceding tensor glyph.'
r.own_finding(sid,209,'One C with two horizontal lower rules',r'\mathbb C',r'\underline{\underline{C}}',reason,'Corollary2.10, complex module structure',kind='font',witness=220)
r.patch(209,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason)
sid='ASTRA-II-NOTE-209';reason='The call after immersion ouverte and the matching complete author note show raised numerical1 in baseline parentheses.'
r.own_finding(sid,209,'Explicit numerical1 author note',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'First proof call and sole author note',kind='author_footnote',witness=220)
r.patch(209,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',sid,reason)
sid='ASTRA-II-UNDERLINE-209';reason='The continuation line has separate word rules on de, tel que and soit un isomorphisme. Both complete corollaries underline their lexical groups, including resp. and the final projection explanation in2.10; references(2.5) remain plain. The three Preuve labels are underlined. All proof prose and the final set-valued Hom words remain plain, apart from the already-underlined Hom sheaf in the final proof sentence.'
r.own_finding(sid,209,'Continuation and corollary word rules; three Preuve labels','Plain statement prose and emph labels',r'Exact lexical uline groups',reason,'First line, both complete corollaries and proof labels',kind='underline',witness=220)
t=(ROOT/'build/page_packets/209/diplomatic.tex').read_text()
for p in r.patches:
 if p['layer']=='both':t=t.replace(p['old'],p['new'])
a=t.index('de $s$ tel que');b=t.index('\n\n',a)
old=t[a:b];r.patch(209,'both',old,underline_statement(old),sid,reason)
for label in ('Corollaire 2.9.','Corollaire 2.10.'):
 a=t.index('Soient ',t.index(r'\textbf{'+label+'}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
 old=t[a:b];r.patch(209,'both',old,underline_statement(old,protected=(r'\(2\.5\)',)),sid,reason)
r.patch(209,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason,3)
r.page(209,'de s tel que f|X|S′:X|S′→Y|S′ soit un isomorphisme.','The final induction map Hom(i_s^{-1}E,i_s^{-1}F)→Hom(i_s^*E,i_s^*F); note ends(SGA1 I5.1).',
 'Every proof and statement word, each baseline restriction bar, diagonal map, inverse-image exponent and final Hom argument was compared. The sole author note is complete. Native witness220 confirms the singular voisinage, the two O rules, double lower C rules and all statement lexical extents. The final display has no added punctuation.',witness=220)
r.commit()
