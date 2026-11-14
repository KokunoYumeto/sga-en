"""Folio211: boundary, Hilbert-bundle abbreviation and two technical lemmas."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('211_215',1,'The page begins(loc.cit.) before the projective-limit display',
 'The complete opening and preceding folio endpoint were inspected. Both sources now put(loc.cit.) after the211 marker, followed by the entire display, so the reported boundary is already repaired.',
 'First printed line and opening display',change='Retain the existing marker before(loc.cit.).')
sid=r.finding('211_215',2,'des O_S rep. O_S⊗C-Modules',
 'The main scan and witness both show rep. here. The same sentence pairs real and complex Hilbert bundles using resp.; its target module pair has the same respective correspondence under E↦the sheaf of continuous sections. Restore the missing s of that abbreviation in current, retaining rep. diplomatically.',
 'Paragraph3.0.5, target module categories',verdict='confirmed; current correction now applied',change='Current alone: rep. becomes resp.',witness=222)
r.patch(211,'current',r'$\cO_S$ rep. $\cO_S',r'$\cO_S$ resp. $\cO_S',sid,'Restore the missing s in the abbreviation for the displayed real/complex correspondence.')
sid='ASTRA-II-O-211';reason='The two O_S letters in3.0.5 each have one individual lower rule.'
r.own_finding(sid,211,'Two singly underlined O letters',r'\cO',r'\underline{O}',reason,'Paragraph3.0.5',kind='font',witness=222)
r.patch(211,'both',r'\cO',r'\underline{O}',sid,reason,2)
sid='ASTRA-II-C-211';reason='The coefficient C in3.0.5 and the field C in Lemma3.1.2 have two lower rules each. The C′ presheaf letters and C sheaf letter of Lemma3.1.1 each have one rule, already correctly restricted to the letter rather than the prime. The section-sheaf E likewise has one existing rule.'
r.own_finding(sid,211,'Two field C letters with double lower rules',r'\mathbb C',r'\underline{\underline{C}}',reason,'Paragraph3.0.5 and Lemma3.1.2',kind='font',witness=222)
r.patch(211,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason,2)
sid='ASTRA-II-PARAGRAPH-211';reason='The identifier3.0.5. has plain typed numerals and a final stop.'
r.own_finding(sid,211,'Plain3.0.5.',r'\textbf{3.0.5.}','3.0.5.',reason,'Hilbert-bundle paragraph opening',kind='font')
r.patch(211,'both',r'\textbf{3.0.5.}','3.0.5.',sid,reason)
sid='ASTRA-II-UNDERLINE-211';reason='Both lemmas underline their complete lexical groups. In3.1.1 the reference(3.0.1) is plain. In3.1.2 the field-choice parenthesis and both resp. clauses have lexical rules. The sole Preuve label is underlined; C’est immédiat is plain. The witness resolves the precise prime and word-rule extents.'
r.own_finding(sid,211,'Exact word rules in Lemmas3.1.1 and3.1.2; Preuve label','Plain statement prose and emph proof label',r'Lexical uline groups',reason,'Both complete lemmas and proof label',kind='underline',witness=222)
t=(ROOT/'build/page_packets/211/diplomatic.tex').read_text()
for p in r.patches:
 if p['layer']=='both':t=t.replace(p['old'],p['new'])
a=t.index('Soient ',t.index(r'\textbf{Lemme 3.1.1.}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
old=t[a:b];r.patch(211,'both',old,underline_statement(old,protected=(r'\(3\.0\.1\)',)),sid,reason)
a=t.index('Soient ',t.index(r'\textbf{Lemme 3.1.2.}'))
old=t[a:];r.patch(211,'both',old,underline_statement(old),sid,reason)
r.patch(211,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason)
r.page(211,'(loc.cit.)','induite par u est continue(resp.continue et d’image dense).',
 'Every word, projective-limit index, sheaf and presheaf underline, prime, closure bar and final induced map was compared. The complete Hilbert-bundle paragraph and both lemmas are accounted for. Native witness222 confirms the printed rep., the exact single-rule E and C′ forms, double-rule field C letters, and complete statement lexical extents.',witness=222)
r.commit()
