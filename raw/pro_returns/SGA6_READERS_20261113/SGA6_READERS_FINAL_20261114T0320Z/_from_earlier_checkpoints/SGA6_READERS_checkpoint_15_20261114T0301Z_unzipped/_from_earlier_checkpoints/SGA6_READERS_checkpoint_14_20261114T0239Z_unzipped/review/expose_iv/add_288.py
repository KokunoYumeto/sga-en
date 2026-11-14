#!/usr/bin/env python3
import json
from review_helpers import Review,HERE
r=Review();p=288
reason=('The source formula is f*(ay)=a f*(y). Section 2.10 on 286 expressly makes K_•(X) a K^•(Y)-module via α=f*:K^•(Y)→K^•(X). Writing ρ_X for the K^•(X) action, its stated restricted action is β=ρ_X∘(α tensor id), so β(a,f*(y))=ρ_X(f*(a),f*(y)). The inherited expanded right side is therefore the very same action written out. The printed notation is justified by the explicit preceding definition and requires no source correction. Restore the printed formula in current; retain the expansion only in the explanatory identification packet.')
for id in ['fixes/FIXLOG_6_CURRENT.jsonl#393','fixes/RECONCILE_CODEX_6.json#289']:
 r.source(id,'(2.12.2) f*(ay)=a f*(y).',reason,'2.12.2; linked module-action definition in 2.10 on 286',verdict='amended',change='Undo the inherited expansion in current and retain the valid printed action notation in both layers.',witness=299,page=288)
 for row in r.decisions:
  if row['source_id']==id:row['image']+='; scan/SGA6_scan_360dpi.pdf#page=300; scan/SGA6_witness_300dpi.djvu#page=297'
r.patch(p,'current',r'f^*(ay)=f^*(a)f^*(y).',r'f^*(ay)=a f^*(y).','fixes/RECONCILE_CODEX_6.json#289',reason)
packet={
 'source_id':'fixes/RECONCILE_CODEX_6.json#289','page':288,'verdict':'Printed formula retained; expansion proved equivalent under the expressly defined action',
 'printed_formula':r'f^*(ay)=a f^*(y)',
 'source_action_passage':{'page':286,'section':'2.10','text':'on peut regarder K_•(X) comme un K^•(Y)-module via l’homomorphisme f*:K^•(Y)→K^•(X)','images':['scan/SGA6_scan_360dpi.pdf#page=300','scan/SGA6_witness_300dpi.djvu#page=297','review/expose_iv/witness_286_top.png']},
 'formula_images':['scan/SGA6_scan_360dpi.pdf#page=302','scan/SGA6_witness_300dpi.djvu#page=299','review/expose_iv/witness_288_lower.png'],
 'maps':{
  'alpha':'f*:K^•(Y)→K^•(X), the ring map of 2.7',
  'psi':'f*:K_•(Y)→K_•(X), the finite-tor-dimension map (2.12.1)',
  'rho_Y':'K^•(Y) tensor K_•(Y)→K_•(Y), tensor action (2.10.1)',
  'rho_X':'K^•(X) tensor K_•(X)→K_•(X), tensor action (2.10.1)',
  'beta':'rho_X composed with (alpha tensor identity):K^•(Y) tensor K_•(X)→K_•(X), expressly defined in 2.10'
 },
 'equality':'psi(rho_Y(a,y)) = beta(a,psi(y)) = rho_X(alpha(a),psi(y)). The middle expression is the printed right side a f*(y); the last is the proposed f*(a) f*(y).',
 'complex_realization':'For a=[M] and y=[E], the source compatibility comes from the canonical derived tensor comparison Lf*(M tensor^L E) ≅ Lf*M tensor^L Lf*E. Both right-side notations take the class of that same tensor complex; additivity gives the stated group maps.',
 'decision':'The comparison proves that the existing source notation already expresses the claimed module compatibility. No replacement expression is needed. Current is returned to the printed formula; diplomatic is unchanged.'
}
(HERE/'identification_288.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
id='ASTRA-IV-O-288'
r.own_finding(id,p,'O with one lower rule, X index outside.',r'\mathcal O_X',r'\underline{O}_X',
 'The native upper crop resolves the short rule under O in the first paragraph.', 'complexes O_X-linéaires',kind='font',witness=299)
r.patch(p,'both',r'\mathcal O_X',r'\underline{O}_X',id,'Observed individual O rule.')
id='ASTRA-IV-UNDERLINE-288'
r.own_finding(id,p,'Plain 2.12 and two lexical title rules ending before the K symbols.',
 'Whole numbered heading bold.', 'Use explicit rules on Variances inhabituelles de and et only.',
 'The formula symbols and final full stop are separate from the rules in both scans. All ensuing prose is plain.', '2.12 heading',witness=299)
r.patch(p,'both',r'\textbf{2.12. Variances inhabituelles de \(K^{\bullet}\) et \(K_{\bullet}\).}',r'2.12. \uline{Variances inhabituelles de} \(K^{\bullet}\) \uline{et} \(K_{\bullet}\).',id,'Observed lexical title rules.')
r.own_finding('ASTRA-IV-NOTATION-288',p,'Four raised round K marks; bottom display label is exactly (2.12.1.1).',
 'Attached raised-dot K and subordinate label.', 'Retain the inspected notation and printed label order.',
 'The main strips and native lower crop show all four raised marks, both pullback orders, and the complete subordinate label following (2.12.2). The label attaches the transitivity relation to (2.12.1); no renumbering is made.',
 '2.12 and all three numbered displays',kind='symbol',verdict='confirmed',witness=299)
r.page(p,'paraît surtout adaptée aux besoins de la Géométrie Algébrique et de la','(2.12.1.1) f*g*=(gf)*.',
 'All prose, references, finite tor-dimension hypothesis, source/target coefficient rings, four raised K marks and three displayed formulas compared. Printed module-action notation retained with its explicit restriction-of-scalars map. No author footnote.',witness='Native witness 299 upper O and lower formula regions; witness_288_O.png and witness_288_lower.png')
r.commit()
