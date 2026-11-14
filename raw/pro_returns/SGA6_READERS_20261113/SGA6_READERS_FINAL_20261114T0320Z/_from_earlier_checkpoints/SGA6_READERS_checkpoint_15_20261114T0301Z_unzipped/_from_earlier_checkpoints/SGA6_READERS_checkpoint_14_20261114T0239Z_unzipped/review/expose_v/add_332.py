#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=332
r.finding('331_335',3,'Item i) ends at0 without a semicolon; item ii) has its terminal full stop.',
 'The native343 top crop resolves clear space after the first zero and the distinct dot after y_i-1 in the next item. The supplied punctuation agrees at both places.',
 'Proposition3.11 item endings',witness=343)
r.finding('331_335',4,'The index list is literally i=1,..,n, with two low dots between the commas.',
 'The native top crop shows the two isolated dots and both commas separately. The supplied diplomatic two-dot/current three-dot pair agrees with the observed omission and its local repair.',
 'Proposition3.11 opening index list',witness=343)
r.finding('331_335',5,'The final gamma_t product equality is inline after de ce que and ends with a full stop; the product has n above and i=1 below.',
 'Main and native scans agree on the formula, both bounds and the final punctuation. The supplied inline form already agrees. Layout alone requires no further content correction.',
 'end of Proposition3.11 proof',verdict='formatting observed; mathematical tokens confirmed',witness=343)
r.own_finding('ASTRA-V-STATEMENT-RULES-332',p,
 'Twelve lexical spans are underlined in Proposition3.11: Soient; un; et; des elements de; tels que; pour; On pose; alors; pour in i); pour in ii); est la; fonction symetrique des. The words anneau, on a and k-ieme are plain.',
 'Use uline for the twelve inspected word groups, leaving formulas, indices, punctuation and the stated plain exceptions independent.',
 'Restore only the twelve directly observed word rules.',
 'The native343 top crop resolves each rule and its endpoint. The rule after the mathematical k starts at fonction, leaving the connecting hyphen and ieme plain; the first item underlines pour alone. The proposition label retains the accepted statement-label typesetting.',
 'Proposition3.11 statement and two items',witness=343)
for layer in ['diplomatic','current']:
 text=(HERE/f'page_332_{layer}.tex').read_text()
 old=text[text.index(r'\textbf{Proposition'):text.index(r'\end{enumerate}')+len(r'\end{enumerate}')]
 new=old
 pairs=[
  ('Soient ',r'\uline{Soient} '),
  (r'\(A\) un ',r'\(A\) \uline{un} '),
  (r'anneau, et ',r'anneau, \uline{et} '),
  (' des éléments de ',' '+r'\uline{des éléments de} '),
  (' tels que ',' '+r'\uline{tels que} '),
  (' pour ',' '+r'\uline{pour} '),
  ('On pose ',r'\uline{On pose} '),
  ('alors :',r'\uline{alors} :'),
  (' est la ',' '+r'\uline{est la} '),
  (' fonction symétrique des ',' '+r'\uline{fonction symétrique des} '),
 ]
 for a,b in pairs:
  assert a in new,(layer,a)
  new=new.replace(a,b)
 assert new.count(r'\uline{')==12,(layer,new)
 r.patch(p,layer,old,new,'ASTRA-V-STATEMENT-RULES-332','Restore the twelve individually inspected lexical rules and preserve the layer-specific ellipsis.')
r.own_finding('ASTRA-V-PARAGRAPH-332',p,'The paragraph number4.1. is plain typed text.',
 r'4.1. replaces \textbf{4.1.}.','Preserve the inspected paragraph-number weight.',
 'Both native and main middle images show the numeral group with no rule or added weight.',
 'paragraph number4.1',kind='font',witness=343)
r.patch(p,'both',r'\textbf{4.1.}','4.1.','ASTRA-V-PARAGRAPH-332','Preserve the directly observed plain paragraph number.')
r.page(p,'Proposition3.11. Soient A un lambda-anneau','lambda_u et Ghat^u(lambda_t) sont des lambda-homomorphismes.',
 'Full comparison of all four main strips and native343 top/lower completed: twelve word rules and plain exceptions; two-dot list; both items and punctuation; all superscripts and bounds in the gamma/lambda proof; full product bounds; section title and calligraphic C_0; complete polynomial algebra and indexing; both unbarred arrows; both parts of4.1.1 including lower n>=2 and no upper bound; final commutative-diagram argument with all references and labels. No author note.',
 witness='Native343 top/lower: witness_332_top.png and witness_332_lower.png.')
r.commit()
