"""Folio187: the coherer adjunction and its finite-cover construction."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('186_190',10,'The inclusion functor uses closed-loop phi',
    'The loop and crossing stem are visible in Lemma3.2. The attached phi form already matches.',
    'Lemma3.2 statement')
r.finding('186_190',11,'Formula(1) uses a wave over a straight bar',
    'Both ends of the lower bar are plain. The attached simeq preserves the printed sign, and the full Hom arguments and final stop match.',
    'Formula(1)')
r.finding('186_190',12,'Q(F|U)→g_*Q(F|V) is inline, with its final stop before Par suite',
    'The attached inline form already agrees. Layout alone does not require a content correction: the same mathematical token sequence Q(F|U)→g_*Q(F|V) and sentence stop are retained.',
    'Transition between formulas(2) and(3)',change='Retain the attached formula and punctuation; no new layout-only patch.')
r.finding('186_190',13,'The tilde lies over Γ, with S as its subscript',
    'The tilde’s base letter is Γ in the affine coherer formula; S remains an ordinary lower index. The attached widetilde{Γ}_S has this observed scope.',
    'Opening of the second proof')
sid='ASTRA-II-UNDERLINE-187';reason='The lemma underlines Le foncteur, a un adjoint à droite and appelé. The defined word cohéreur is plain, confirmed in the native witness. Both Preuve headings are underlined; the proof bodies and remark are plain. Mathematical units remain independent.'
r.own_finding(sid,187,'Underlined lemma words with plain cohéreur','Plain lemma prose',r'\uline on the inspected lexical groups',reason,'Lemma3.2 and both proof headings',kind='underline',witness=198)
old=(ROOT/'build/page_packets/187/diplomatic.tex').read_text()
a=old.index('Le foncteur',old.index(r'\textbf{Lemme 3.2.}'));b=old.index(r'\emph{Preuve.}',a)
new=old[:a]+underline_statement(old[a:b],[r'cohéreur'])+old[b:]
new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
r.patch(187,'both',old,new,sid,reason)
r.page(187,'Preuve. L’assertion relative aux générateurs','on obtient, compte tenu de(1), un',
    'All proof and remark prose, adjunction statement, cover indices, all three numbered formulas, baseline restrictions and placeholder point were compared. The four printed object abbreviations are lowercase ob, agreeing with the continuation macro. Witness198 confirms the plain defined word cohéreur.',witness=198)
r.commit()
