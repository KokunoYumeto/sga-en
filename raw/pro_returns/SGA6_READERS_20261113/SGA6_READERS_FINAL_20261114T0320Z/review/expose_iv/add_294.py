#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=294
r.finding('291_295',23,'3.3. Groupes de Grothendieck relatifs, with no final stop.',
 'The native heading crop shows the rule beneath the lexical title ending at relatifs, with no stop after it. The attached wording already matches.', 'heading 3.3',witness=305)
reason=('Both scans print the singular morphisme. The displayed triangle contains f:X→Y, g:Y→S and h:X→S with g∘f=h, and the following text treats their local-finite-type properties. The current plural supplies the grammatical number for this explicit three-arrow diagram; it changes no arrow, composition or hypothesis. Diplomatic retains the source singular.')
r.finding('291_295',25,'un triangle commutatif de morphisme localement de type fini de schémas.',reason,
 'sentence immediately after the triangle',witness=305)
for id in ['fixes/FIXLOG_6_CURRENT.jsonl#398','fixes/RECONCILE_CODEX_6.json#294']:
 r.source(id,'de morphisme, singular, after the three-arrow triangle.',reason,'sentence after the triangle',
  witness=305,page=p,change='Confirm the existing current plural morphismes; retain singular diplomatically.')
r.finding('291_295',26,'Ordinary typed L above the tensor sign, with Y below.',
 'The native lower crop shows a single-stroke L, not an underlined or doubled letter. The attached mathrm L matches the ordinary glyph.', 'derived tensor functor in 3.3.2.2',witness=305)
r.own_finding('ASTRA-IV-UNDERLINE-294',p,'The lexical heading Groupes de Grothendieck relatifs is underlined; its number and paragraph numbers are plain.',
 r'3.3. \uline{Groupes de Grothendieck relatifs}; 3.3.1.; 3.3.2.',
 'Use the observed title rule and plain paragraph numerals.',
 'The native top crop confirms the uninterrupted rule under the lexical title only. All prose on the page is otherwise plain. The lower numbered items are also plain; their shared enumeration helper is checked together with its continuation on 295 before changing that helper.',
 'heading and paragraph numbers',witness=305)
r.patch(p,'both',r'\textbf{3.3. Groupes de Grothendieck relatifs}',r'3.3. \uline{Groupes de Grothendieck relatifs}','ASTRA-IV-UNDERLINE-294','Restore the observed title rule without a rule under its number.')
for n in ['3.3.1.','3.3.2.']:
 r.patch(p,'both',r'\textbf{'+n+'}',n,'ASTRA-IV-UNDERLINE-294','Preserve the plain typed paragraph number.')
r.own_finding('ASTRA-IV-NOTATION-294',p,'Fifteen raised round K marks; six separate parf rules; coh plain; ordinary L; all three triangle arrows headed.',
 r'K^{\bullet}; underlined parf; plain coh; \mathrm L.',
 'Retain the inspected mathematical symbols and the six local parf rules.',
 'The two definitions, subsequent relative notation, tensor-product expressions, equality pairs and four final pairing displays were compared occurrence by occurrence. The native top and lower crops resolve all six parf rules and show that the coh letters have no underline. The broad checker finding covering 294–295 is completed only after the latter page is compared.',
 'all formulas and the commutative triangle',kind='symbol',verdict='confirmed',witness=305)
r.page(p,'3.3. Groupes de Grothendieck relatifs','K^•(f)⊗K^•(g)→K^•(h).',
 'All prose and locators, fifteen raised K marks, lower K marks, six parf rules, ordinary L, relative definitions, the three-arrow triangle and its labels, two numbered items and four pairing displays compared. No author note. The singular/plural source variant is recorded separately.',
 witness='Native witness 305 top and lower regions; witness_294_top.png and witness_294_lower.png')
r.commit()
