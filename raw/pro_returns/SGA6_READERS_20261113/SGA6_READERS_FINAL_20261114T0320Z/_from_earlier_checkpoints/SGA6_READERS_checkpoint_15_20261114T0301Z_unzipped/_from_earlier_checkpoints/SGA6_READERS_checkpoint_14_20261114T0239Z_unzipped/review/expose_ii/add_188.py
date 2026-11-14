"""Folio188: coherer adjunctions and occurrence-specific source typography."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
for i,printed,region in [
 (14,'Hom(E,F) ≃ Hom(E,QF), followed by a stop','Opening display'),
 (15,'The derived R in RQ:D⁺(S)→D⁺(Qcoh(S)) has two lower rules','Lemma3.3 b), first display'),
 (16,'The derived R before Hom_Mod in(i) has two lower rules','Formula(i), first member'),
 (17,'A wave over a headless bar, followed by double-marked R Hom_Qcoh','Formula(i), relation and second member'),
 (18,'The R in the argument RQ(F) of(i) has two lower rules','Formula(i), second argument'),
 (19,'The relation in(ii) is a wave over a headless bar','Formula(ii), relation'),
 (20,'The R in the argument RQ(F) of(ii) has two lower rules','Formula(ii), second argument'),
 (24,'Qf_*(E) ≃ f_*Q(E), followed by a stop','Lemma3.4 display')]:
 if i in (15,16,17,18,20):
  r.finding('186_190',i,printed,'The main scan and native witness show two separate horizontal rules below each indicated R. Preserve those rules literally; the associated Hom arguments and the headless relation in(i) already agree.',region,verdict='amended',change=r'Replace the inspected mathbb R representations by \underline{\underline{R}}; retain the other observed tokens.',witness=199)
 else:
  r.finding('186_190',i,printed,'The main scan and native witness agree. The attached symbol and all its displayed arguments already reproduce the observed reading.',region,witness=199)
for i in (21,22,23):
 r.finding('186_190',i,'A raised numerical1 within baseline parentheses is placed after formula(i); the complete matching note is at the foot of the page',
 'The attached split call and text already have the printed placement. An explicit author label preserves this particular call and matching note independently of automatic numbering.',
 'Formula(i) call and complete author note',change='Retain the placement and note text; replace automatic note helpers by explicit label1.',witness=199)
sid='ASTRA-II-UNDERLINE-188';reason='All lexical words of Lemma3.3 a), Notons, and the following statement are underlined except the conjunction et between the two displayed object-membership expressions. The native witness confirms that et is plain. The words of Lemma3.4 and the Preuve heading are underlined; formulas and proof body remain independently marked.'
r.own_finding(sid,188,'Statement word rules, with plain et between E and F memberships','Plain statement prose',r'\uline on the exact inspected word groups',reason,'Both lemmas and the proof heading',witness=199)
old=(ROOT/'build/page_packets/188/diplomatic.tex').read_text();new=old
for begin,end,protected in [
 ('Le cohéreur est',r'\item Notons',()),
 ('Notons',r'\[',()),
 ('le dérivé droit',r'\begin{align}',(r'\bet\b',)),
 ('Soit $f:X',r'\[',())]:
 a=new.index(begin);b=new.index(end,a)
 new=new[:a]+underline_statement(new[a:b],protected)+new[b:]
new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
r.patch(188,'both',old,new,sid,reason)
sid='ASTRA-II-NOTES-188';reason='Both actual marks show the same raised numerical1 between baseline parentheses. The call remains in formula(i), and the full note remains separate from the statement.'
r.own_finding(sid,188,'Formula(i) and footnote use explicit numerical1',r'\footnotemark and \footnotetext',r'\SGAAuthorFootMark{1} and \SGAAuthorFootText{1}',reason,'Formula(i) and author-note label',kind='author_footnote',witness=199)
r.patch(188,'both',r'\footnotemark',r'\SGAAuthorFootMark{1}',sid,reason)
r.patch(188,'both',r'\footnotetext{',r'\SGAAuthorFootText{1}{',sid,reason)
sid='ASTRA-II-R-188';reason='The five R letters in the definition of RQ, the two RHom expressions in(i), and the RQ(F) arguments in(i) and(ii) each have two horizontal rules beneath the letter. Both scans were directly inspected. This page-specific replacement preserves those five literal glyphs.'
r.own_finding(sid,188,'Five individually double-underlined derived R letters',r'\mathbb R',r'\underline{\underline{R}}',reason,'Lemma3.3 b), its definition and formulas(i),(ii)',kind='font',witness=199)
r.patch(188,'both',r'\mathbb R',r'\underline{\underline{R}}',sid,reason,5)
r.page(188,'isomorphisme fonctoriel en E :','Qf_*(E) ≃ f_*Q(E).; note ends D(Qcoh(S)).',
 'Both lemmas, the complete proof, all adjunction expressions, every Hom subscript and the complete author note were compared. Native witness199 confirms all five double-marked derived R occurrences, the four headless isomorphism signs, the plain conjunction et in3.3 b), and the explicit author label1.',witness=199)
r.commit()
