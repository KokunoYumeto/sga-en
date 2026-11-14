"""Folio214: exact Sobolev target map and parameter notation."""
from review_helpers import Review
r=Review()
reason='The u_r target prints C^r_2(V,F), while both the defining operator family immediately above and the final bundle map print C^{r−n}_2(V,F). Write H_E=C^r_2(V,E), H_F=C^{r−n}_2(V,F), and T(s)=phi_r(u(s))∈L(H_E,H_F). For a relatively compact open W⊂S, the actual induced presheaf map is a∈C(bar W,H_E)↦[s↦T(s)a(s)]∈C(bar W,H_F). Continuity follows from the displayed operator-norm-continuous family and continuous evaluation L(H_E,H_F)×H_E→H_F. This exact map identifies the corrected target C′(S,C^{r−n}_2(V,F)); retain the printed exponent r in diplomatic and the already corrected r−n in current.'
r.finding('211_215',10,'The u_r target has superscript r alone',reason,
 'Lower presheaf-map display',change='Retain diplomatic r and existing current r−n.',witness=225)
for sid in ['fixes/RECONCILE_CODEX_6.json#261','fixes/FIXLOG_6_CURRENT.jsonl#365']:
 r.source(sid,'The u_r target is printed C^r_2(V,F)',reason,'Lower presheaf-map display',page=214,change='Retain the existing current-only target shift correction.',witness=225)
sid='ASTRA-II-PHI-214';reason='All four phi map symbols have a closed loop crossed by a stem: the first phi u, its inline repetition, the displayed phi_r u and the final inline phi_r u.'
r.own_finding(sid,214,'Four closed-loop phi glyphs',r'\varphi',r'\phi',reason,'Two displayed and two inline operator-family symbols',kind='symbol',witness=225)
r.patch(214,'both',r'\varphi',r'\phi',sid,reason,4)
sid='ASTRA-II-Z-214';reason='The integer Z in r∈Z has two separate horizontal lower rules, resolved in the native witness.'
r.own_finding(sid,214,'One Z with double lower rules',r'\Z',r'\underline{\underline{Z}}',reason,'Sobolev-parameter range',kind='font',witness=225)
r.patch(214,'both',r'\Z',r'\underline{\underline{Z}}',sid,reason)
r.page(214,'Identifiant u, par(3.1.4), à une application continue ...','S×C^r_2(V,E)→S×C^{r−n}_2(V,F),',
 'Every prose word and all eight displayed map rows were compared, including every baseline restriction, direct/pullback index, infinity symbol, r−n shift and the final comma. The four C′ letters have an individual rule under C only, already represented in the sources. The parenthetical(3.1.3) beside the first operator map is retained with its existing mathematical tokens and punctuation; its tag placement is an accepted layout variation. No lexical emphasis occurs on this page. Native witness225 confirms the precise target-exponent variant, integer glyph and closed phi symbols.',witness=225)
r.commit()
