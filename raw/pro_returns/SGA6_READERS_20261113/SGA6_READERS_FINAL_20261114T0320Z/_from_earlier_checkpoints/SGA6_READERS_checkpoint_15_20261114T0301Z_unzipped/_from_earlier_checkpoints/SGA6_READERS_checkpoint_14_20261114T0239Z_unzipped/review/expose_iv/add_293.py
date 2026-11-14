#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=293
for n,printed,region in [
 (13,'K^•(X)_naïf → lim→ K^•(Xi)_naïf, without a limit index.','first line'),
 (14,'lim→ K^•(Xi) → K^•(X), without a limit index.','display in 3.2.2'),
 (17,'lim→ K_•(Xi) → K_•(X), without a limit index.','display in 3.2.3'),
 (19,'que lim→ K_•(Xi) est muni, without a limit index.','module structure paragraph'),
 (20,'sur lim→ K^•(Xi)_naïf, without a limit index.','module structure paragraph')]:
 r.finding('291_295',n,printed,
  'The complete main page and the native notation/diagram crops show the rightward arrow directly below lim. The only i in each expression belongs to X, with no additional index beneath the operator. The attached source matches.',
  region,witness=304)
r.finding('291_295',15,'Lim has a capital L and a rightward arrow beneath it.',
 'The native crop resolves the capital L, lowercase im and the separate rightward arrow. The following Parf(Xi) is plain, with no lower rule; the attached operator form preserves that literal typography.',
 'localization paragraph in 3.2.2',witness=304)
r.finding('291_295',16,'noethériens and plats alone are underlined in the hypotheses.',
 'The two rules end before the comma and the opening parenthesis. The rest of the paragraph is plain. Explicit underline helpers below preserve those observed groups.',
 'opening of 3.2.3',witness=304)
reason=('Both displayed maps carry the printed tag (3.2.2.1). Let α be the vector-bundle limit map of (3.2.1.1), and let β:colim K_•(Xi)→K_•(X) be the flat-pullback map in 3.2.3, β(j_i[F_i])=[f_i^*F_i]. The final diagram has right vertical β and left vertical α⊗β. At a common index k, both routes send [V_k]⊗[F_k] to [f_k^*V_k⊗f_k^*F_k], by the canonical pullback/tensor isomorphism. This identifies the second tag and both following references with β. The perfect-complex map α_perf of 3.2.2 is related by the inclusion maps c_i:K^•(Xi)→K_•(Xi) and c_X:K^•(X)→K_•(X): β∘colim(c_i)=c_X∘α_perf, since both send a perfect complex E_i to its derived pullback class, and flat pullback computes that class here. The current relabelling (3.2.3.1) therefore follows the exact map used in the diagram; diplomatic preserves the duplicate tag and both printed references.')
r.finding('291_295',18,'The display in 3.2.3 repeats (3.2.2.1), and both later references use that same printed number.',reason,
 'second display tag and the two references before the final diagram',witness=304)
for id in ['fixes/FIXLOG_6_CURRENT.jsonl#395','fixes/FIXLOG_6_CURRENT.jsonl#396','fixes/FIXLOG_6_CURRENT.jsonl#397','fixes/RECONCILE_CODEX_6.json#292','fixes/RECONCILE_CODEX_6.json#293']:
 r.source(id,'Duplicate (3.2.2.1) for the map in 3.2.3 and its two later references.',reason,
  'second display tag and references to the diagram’s vertical maps',witness=304,page=p,
  change='Confirm the existing current tag (3.2.3.1) and its two current references; retain the printed numerals diplomatically.')
for n,which in [(21,'left'),(22,'right')]:
 r.finding('291_295',n,'A tilde over one horizontal bar stands to the right of the '+which+' downward arrow.',
  'The native diagram crop shows a separate bar below the tilde at both labels, matching the headless sign in K_•(X)≃K_•(X)_naïf above. The vertical arrows themselves have downward heads. The attached simeq label and its position agree.',
  which+' vertical arrow of the final diagram',witness=304)
r.own_finding('ASTRA-IV-UNDERLINE-293',p,'Only noethériens and plats are underlined; paragraph numbers 3.2.2. and 3.2.3. are plain.',
 r'\uline{noethériens}; \uline{plats}; ordinary paragraph numerals.',
 'Preserve the two observed rules and plain paragraph numbers.',
 'Both scans show these two local word rules and no emphasis elsewhere in the prose. The numerical headings have the same ordinary typed weight as their following text.',
 'paragraph headings and the two hypotheses',witness=304)
for word in ['noethériens','plats']:
 r.patch(p,'both',r'\emph{'+word+'}',r'\uline{'+word+'}','ASTRA-IV-UNDERLINE-293','Restore the actual word rule, leaving punctuation outside it.')
for n in ['3.2.2.','3.2.3.']:
 r.patch(p,'both',r'\textbf{'+n+'}',n,'ASTRA-IV-UNDERLINE-293','Preserve the plain typed paragraph number.')
r.own_finding('ASTRA-IV-NOTATION-293',p,'Nine raised round K dots, lower dots at every coherent-group occurrence, capital Lim in the category phrase, and plain Parf.',
 r'K^{\bullet}; K_{\bullet}; \mathop{\underrightarrow{\mathrm{Lim}}}; \Parf.',
 'Retain the directly inspected symbols.',
 'All occurrences were compared in the main strips and the native notation/diagram crops. The upper group-limit arrow is unlabelled; the coherent-group isomorphism has a centered tilde and a rightward head. The bottom diagram has two rightward and two downward headed arrows, three unindexed direct limits in its top row, and a final stop.',
 'all formulas and the final diagram',kind='symbol',verdict='confirmed',witness=304)
r.page(p,'elle définit donc un homomorphisme…','The final commutative module diagram, ending K_•(X).',
 'Every word, locator, nine raised K dots, all lower K dots, eight group-limit operators and the capital category Lim, two underlined hypotheses, duplicate tag and references, and all diagram arrows/labels compared. No author note. The corrected tag transfer is justified by the actual vertical maps and the perfect-to-coherent inclusion square.',
 witness='Native witness 304 notation and lower diagram regions; witness_293_notation.png and witness_293_diagram.png')
r.commit()
