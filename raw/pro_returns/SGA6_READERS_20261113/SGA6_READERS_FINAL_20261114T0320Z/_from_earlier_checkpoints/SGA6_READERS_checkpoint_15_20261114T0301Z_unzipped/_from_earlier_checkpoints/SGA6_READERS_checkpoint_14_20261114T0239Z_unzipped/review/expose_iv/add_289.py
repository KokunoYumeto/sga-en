#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=289
r.finding('286_290',15,'Both parf terms underlined in Rf_*:D(X)_parf→D(Y)_parf.',
 'The native upper crop shows separate short rules beneath parf at both endpoints. The attached two uparf terms match.', 'first paragraph',witness=300)
reason=('Both scans leave the parenthesis opened before resp. unclosed. The first branch allows y in K_•(Y), the alternative allows y in K^•(Y), and x belongs to K^•(X) in both branches. The supplied closer after K^•(Y) therefore delimits exactly the alternative y-domain. It changes neither the pullback maps (2.12.1)/(2.7.1) nor the product and pushforward in (2.12.4). Diplomatic retains the omission and current supplies that single closer.')
r.finding('286_290',16,'pour y∈K_•(Y) (resp. K^•(Y) et x∈K^•(X),…',reason,'before (2.12.4)',witness=300)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#394','Missing closer after the alternative K^•(Y).',reason,'before (2.12.4)',witness=300,change='Confirm the existing current-only closing parenthesis.')
r.source('fixes/RECONCILE_CODEX_6.json#290','Missing closer after the alternative K^•(Y).',reason,'before (2.12.4)',witness=300,page=289,change='Confirm the existing current-only closing parenthesis.')
r.own_finding('ASTRA-IV-NOTATION-289',p,'Ten raised round K marks; genuine prime after 3 in (2.12.3′); two parf rules and one ordinary R in Rf_*.',
 'K^{\\bullet}; prime in the displayed tag and its reference; uparf; plain R.', 'Retain the inspected notation.',
 'The native lower crop directly compares the round K marks with the narrow, higher prime in the tag and its prose reference. All prose on this page is plain. The subordinate label (2.12.3.1), displayed comma after (2.12.4), and final stops are preserved.',
 'all formulas and the final two paragraphs',kind='symbol',verdict='confirmed',witness=300)
r.page(p,'Supposons maintenant qu’on soit dans la situation (2.11.1)…','sorites de Exp. I à Exp. IV.',
 'All prose, hypotheses and locators, ten raised K marks, actual prime tag and reference, two parf rules, four formulas and their punctuation compared. No author footnote and no new patch.',witness='Native witness 300 opening/alternative-domain and lower tag regions; witness_289_top.png and witness_289_lower.png')
r.commit()
