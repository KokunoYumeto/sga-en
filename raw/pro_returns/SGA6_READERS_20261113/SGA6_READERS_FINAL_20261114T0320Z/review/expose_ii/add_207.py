"""Folio207: corollary continuation, baseline placeholder and lexical rules."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('206_210',3,'H^0(A,.) has a baseline stop in its second argument',
 'The native witness resolves the comma and the following baseline point separately. The attached H^0(A,.) already matches; a raised centered dot is not printed.',
 'Proof of Corollary2.4',change='Retain the existing baseline placeholder.',witness=218)
sid='ASTRA-II-O-207';reason='All six O letters in the two corollaries and the intervening proof have one individual lower rule, with every X or X_s subscript outside it.'
r.own_finding(sid,207,'Six individually underlined O letters',r'\cO',r'\underline{O}',reason,'Complete page',kind='font',witness=218)
r.patch(207,'both',r'\cO',r'\underline{O}',sid,reason,6)
sid='ASTRA-II-UNDERLINE-207';reason='The lexical groups in both corollaries have word rules. In2.4 the reference(2.2) is plain. In2.5 the entire explanatory parenthesis has lexical rules as well; the word pour inside the final formula is plain. Each of the two Preuve labels is underlined, and all following proof prose is plain. Mathematical units remain independent.'
r.own_finding(sid,207,'Exact word rules in Corollaries2.4,2.5 and both Preuve labels','Plain corollary prose; two emph proof labels',r'Lexical uline groups',reason,'Both complete statements and proof labels',kind='underline',witness=218)
t=(ROOT/'build/page_packets/207/diplomatic.tex').read_text()
for p in r.patches:t=t.replace(p['old'],p['new'])
a=t.index('Sous les hypothèses',t.index(r'\textbf{Corollaire 2.4.}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
old=t[a:b];r.patch(207,'both',old,underline_statement(old,protected=(r'\(2\.2\)',)),sid,reason)
a=t.index('Soient ',t.index(r'\textbf{Corollaire 2.5.}'))
old=t[a:];r.patch(207,'both',old,underline_statement(old),sid,reason)
r.patch(207,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason,2)
sid='ASTRA-II-AUTHOR-CLAIM-207';reason='The first proof explicitly applies2.2 with A=empty and then takes S=s. This directly confirms that the preceding general Hom-sheaf softness assertion includes a one-point base and has no additional target hypothesis. The exact annular-germ obstruction and restriction map are recorded in review/expose_ii/author_claim_issue_206.json. Preserve the proof as printed; this is a source-reading decision and supplies no replacement theorem.'
r.own_finding(sid,207,'The proof states A=empty, then prenant S=s','Attached proof has those same two specializations','Retain the printed proof and link its author-claim issue to206.',reason,
 'First proof, continuation of Corollary2.3',kind='author_claim_issue',verdict='source reading decided and retained')
r.page(207,'Preuve. Le fait que i_s^{-1}Hom(X,Y) soit mou ...','R^i p_*(E)_s=0 pour i>0.',
 'All words and symbols, the two first-proof specializations, the exact baseline placeholder, every tensor and inverse-image index, and all five displays were compared. The derived R in the last display is plain, and pour there is also plain. Native witness218 confirms the lower corollary’s complete lexical rules and the proof placeholder. The first proof’s relation to the separate206 author-claim issue is recorded without altering its text.',witness=218)
r.commit()
