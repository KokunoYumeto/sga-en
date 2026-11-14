#!/usr/bin/env python3
import json
from review_helpers import Review, HERE
r=Review();p=312
packet={
 'record_type':'mathematical_identification',
 'source_id':'ASTRA-V-POINT-312',
 'page':312,
 'source_passage':'le k-ième polynôme universel de Φ a des composantes isobares dont le poids varie entre k et [line break, isolated low dot] km : ceci résulte immédiatement du mode de calcul exposé plus haut, et du théorème des fonctions symétriques.',
 'source_images':['scan/SGA6_scan_360dpi.pdf#page=326','scan/SGA6_witness_300dpi.djvu#page=323','review/expose_v/witness_312_marks.png','review/expose_v/witness_312_km.png'],
 'physical_observation':'A detached round low dot stands immediately left of the k in the final-line km. Its shape and baseline placement agree with the lower point of the following colon and with the sentence-final stop on this page. The other lowercase k forms in k-ième and entre k et do not have a left dot. Both independent scans retain the mark.',
 'notation_key':'Use r for the number of source arguments (called k in the preceding paragraph) and d for the coefficient index; the final source clause specializes d to its printed k. This renaming only separates two roles in the calculation.',
 'source_references':['Exposé V1.5, printed300: elementary-symmetric injection and invariants','Exposé V1.6 proof, printed301–304: evaluation after splitting into factors1+Tt','Exposé V1.15, printed312: the explicit universal-polynomial calculation and stated coefficient weights'],
 'graded_map':{
  'source':'R_N=K[X_j^(a) | 1≤j≤N,1≤a≤r], wt(X_j^(a))=j',
  'target':'S_N=K[T_l^(a) | 1≤l≤N,1≤a≤r], wt(T_l^(a))=1',
  'formula':'ι_N(X_j^(a))=e_j(T_1^(a),…,T_N^(a))',
  'identification':'The elementary-symmetric theorem identifies R_N with S_N^{(S_N)^r}; ι_N is injective and preserves the displayed weights. Here (S_N)^r in the superscript denotes the product of r symmetric groups on N letters, not the polynomial ring named S_N.'
 },
 'factor_maps':{
  'universal_element':'θ=Φ(1+U_1t,…,1+U_rt)',
  'specialization':'For J=(j_1,…,j_r)∈{1,…,N}^r, σ_J:K[U_1,…,U_r]→S_N sends every U_a↦T_(j_a)^(a).',
  'source_factorization':'The ath input coordinate factors as ∏_(l=1)^N(1+T_l^(a)t). The maps of1.7 are Z-multilinear, that is, group homomorphisms in each argument separately. Expanding successively in all r arguments therefore yields one image factor for each tuple J=(j_1,…,j_r).',
  'image_identification':'Naturality and the iterated separate group-homomorphism identities give Φ(∏_l(1+T_l^(1)t),…,∏_l(1+T_l^(r)t))=∏_Jσ_J(θ) in the multiplicative series examples, and the corresponding Σ_Jσ_J(θ) in the additive series example.'
 },
 'weight_calculation':[
  'The source stipulates that every isobaric component of the coefficient of t^q in θ has weight between q and mq. Every σ_J sends each degree-one U_a to a degree-one root variable, preserving the monomial weights.',
  'A contribution to the coefficient of t^d in the product has indices q_J≥0 with Σ_Jq_J=d. The coefficient at q=0 is the multiplicative identity. Each surviving monomial has weight W=Σ_Jw_J, hence d=Σ_Jq_J≤W≤Σ_Jm q_J=md.',
  'For the additive target, each summand in degree d has its original weight between d and md, so the same bounds hold.',
  'The resulting coefficient is separately symmetric in each root family. The injective graded elementary-symmetric map descends it to the universal polynomial without altering its weights. The filtration passage used in1.6 fixes each finite coefficient and hence these bounds.',
  'At the coefficient index printed k in the final clause, the endpoint is m·k=km. The preceding isolated baseline dot is surplus punctuation before this product; the calculation introduces no additional scalar or operation.'
 ],
 'decision':'Preserve the observed leading dot in the diplomatic layer; keep the corrected endpoint km. No replacement mathematical claim is introduced.',
 'forms':{'diplomatic':r'\(\mathord{.}km\)','current':r'\(km\)'}
}
# Use an unambiguous symmetric-group notation in the recorded identification.
packet['graded_map']['identification']='The elementary-symmetric theorem identifies R_N with S_N^{(𝔖_N)^r}; ι_N is injective and preserves the displayed weights, with 𝔖_N the symmetric group on N letters.'
(HERE/'identification_312.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.own_finding('ASTRA-V-POINT-312',p,'A separate round baseline dot precedes km on the final mathematical line: .km : ceci résulte…',
 r'Diplomatic \(\mathord{.}km\); corrected \(km\).',
 'Restore the physically printed dot in the diplomatic layer and retain the corrected product km.',
 'Both scans show the detached low dot. The native marks crop compares it directly with the following colon, the sentence-final full stop, and two other lowercase k forms. The calculation in review/expose_v/identification_312.json uses X_j^(a)↦e_j(T_1^(a),…,T_N^(a)) and the separately multilinear root expansion indexed by J=(j₁,…,j_r), with σ_J(U_a)=T_(j_a)^(a). Each degree-d coefficient term has Σ_Jq_J=d and d≤Σ_Jw_J≤mΣ_Jq_J=md. The graded injection preserves these weights on descent. Setting d=k proves the stated endpoint km and justifies treating the preceding dot as surplus punctuation.',
 'final paragraph, low dot immediately before km',kind='misprint_in_print',witness=323)
r.own[-1]['forms']='French diplomatic retains observed dot; corrected omits it; corresponding English source variant with the same endpoint.'
r.patch(p,'diplomatic',r'entre \(k\) et \(km\)',r'entre \(k\) et \(\mathord{.}km\)','ASTRA-V-POINT-312','Preserve the observed leading low dot, with the corrected km justified by the explicit weight calculation.')
r.page(p,'(1.7) que Φ est déterminé par sa valeur sur l’élément','du théorème des fonctions symétriques.',
 'Both complete paragraphs compared: all tuple indices and the three two-stop ranges, capital/lowercase Greek forms, hatted functors and g/a indices, completion placeholder, doubled stops, exact defined-term underline including n, all split-root expressions and product bounds, substitutions a_j^(i) into X_j^(i), the two weight intervals, and final punctuation. The isolated dot before km is preserved diplomatically with its exact weight calculation recorded separately. No author note.',
 witness='Native witness323 top/lower crops and marks comparison; witness_312_top.png, witness_312_lower.png, witness_312_marks.png, witness_312_km.png')
r.commit()
