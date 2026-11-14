#!/usr/bin/env python3
import json
from review_helpers import Review,HERE,read
r=Review();p=295
reason=('Set A=k[ε]/(ε²), S=Spec A, X1=Y1=Spec k, X2=Y2=S, and f1,f2 equal to the respective identity maps. Both required pairs (X1,X2) and (Y1,Y2) are Tor-independent over S because Tor_i^A(k,A)=0 for i>0. Their products X and Y are Spec k and f=f1×_Sf2=id_Spec k. Take E1=k in degree0 on X1 and E2=k in degree0 on S. E1 is perfect relative to f1 with amplitude[0,0]. The free resolution P with P^n=A for n≤0 and every differential in negative degree multiplication by ε is exact in negative degrees, since ker(ε)=εA=im(ε), and H^0(P)=k. Its finite free approximations prove E2 pseudo-coherent; its own cohomology is concentrated in degree0. Thus the two input objects satisfy the printed hypotheses. In the exact construction of III1.6, pr1=id_Spec k and pr2:Spec k→Spec A, so Lpr1^*E1⊗^L_k Lpr2^*E2 = k⊗^L_k(k⊗^L_A k). The resolution identifies this with k⊗_A P, whose differentials are all zero and whose term in every degree n≤0 is k. Hence H^n=k for every n≤0. The inclusion J:D^b(k)_coh→D^−(k)_coh sends a bounded object to a complex with vanishing cohomology in all sufficiently negative degrees, so the displayed tensor object is not isomorphic to an object in its essential image. The advertised first pairing therefore does not land in D^b(f)_coh, and cannot induce the first stated Grothendieck homomorphism by the displayed tensor functor. The printed text is retained; no replacement theorem or assertion about all abstract group pairings is made. See author_claim_issue_295.json.')
r.own_finding('ASTRA-IV-AUTHOR-CLAIM-295',p,
 'Sous les hypothèses de (III 4.7), le foncteur ⊗^L_S définit des accouplements D(f1)_parf×D^b(f2)_coh→D^b(f)_coh,… qui induisent des homomorphismes K^•(f1)⊗K_•(f2)→K_•(f),…',
 'The attached first category pairing and its first asserted induced group map are faithful to both scans.',
 'Retain the source claim in both layers; attach the explicit derived-tensor obstruction separately.',
 reason,'first category pairing and first induced Grothendieck map in 3.3.3',
 kind='author_claim_issue',verdict='source reading decided and retained; author claim contradicted by the recorded tensor calculation',witness=306)
packet={
 'source_id':'ASTRA-IV-AUTHOR-CLAIM-295','page':295,
 'status':'Source reading fully decided and retained; separate author-claim issue; no proposed replacement',
 'affected_claims':[
  r'\otimes_S^{\mathrm L}:D(f_1)_{\parf}\times D^b(f_2)_{\coh}\longrightarrow D^b(f)_{\coh}',
  r'K^{\bullet}(f_1)\otimes K_{\bullet}(f_2)\longrightarrow K_{\bullet}(f), asserted to be induced by that tensor functor'
 ],
 'printed_scope':'3.3.3 expressly invokes the hypotheses of III4.7. The first category pairing, first induced homomorphism, and that reference agree in the main image and native witness.',
 'image_evidence':[
  {'path':'review/expose_iv/page_295_s3.png','scope':'Directly compared 3.3.3, its reference and first category pairing.'},
  {'path':'review/expose_iv/page_295_s4.png','scope':'Directly compared the first asserted induced Grothendieck homomorphism.'},
  {'path':'review/expose_iv/witness_295_lower.png','scope':'Native witness306 confirms the category targets D^b and first group target K_•.'},
  {'path':'review/expose_iv/main_231_external_tensor.png','scope':'Regional direct view of the exact III1.6 definition via the two derived pullbacks.'},
  {'path':'review/expose_iv/main_256_external_hypotheses.png','scope':'Regional direct view of III4.7 hypotheses and part(a), including both Tor-independent pairs and the asserted cohomology bound.'}
 ],
 'example':{
  'ring':'A=k[ε]/(ε²), for a fixed field k; S=Spec A.',
  'schemes':'X1=Y1=Spec k and X2=Y2=Spec A, all with their indicated A-structures.',
  'morphisms':'f1=id_Spec k and f2=id_Spec A. These are S-morphisms locally of finite type.',
  'products':'X=X1×_SX2=Spec(k⊗_A A)=Spec k and Y=Y1×_SY2=Spec k. Under these canonical ring identifications f=f1×_Sf2 is id_Spec k.',
  'tor_independence':'For both pairs (X1,X2) and (Y1,Y2), the relevant higher Tor modules are Tor_i^A(k,A)=0, since A is free of rank one over itself. These are exactly the two pairs printed in III4.7.',
  'inputs':'E1=k[0] on X1 and E2=k[0] on X2. E1 has perfect amplitude [0,0] relative to the identity f1. E2 has bounded cohomology in degree0 and is pseudo-coherent relative to the identity f2.',
  'pseudo_coherence_proof':'Let P^n=A for n≤0, P^n=0 for n>0, and d^n=ε for n<0. The augmentation P^0=A→k is the quotient. Because ε²=0 and ker(A --ε→ A)=εA=im(A --ε→ A), H^n(P)=0 for n<0 and H^0(P)=k. Thus P→k[0] is a free resolution. Every term has rank one; truncating sufficiently far to the left gives a finite-free approximation in any prescribed upper range, proving pseudo-coherence of k[0].'
 },
 'exact_derived_tensor_calculation':[
  'On X=Spec k, pr1:X→X1 is the identity and pr2:X→X2 corresponds to A→k. Hence Lpr1^*E1 is k[0], and Lpr2^*E2 is k⊗^L_A k.',
  'The definition in III1.6 gives E1⊗^L_S E2=(Lpr1^*E1)⊗^L_{O_X}(Lpr2^*E2). The unit isomorphism k⊗^L_k(−)→(−) identifies it with k⊗^L_A k. Using the explicit free resolution P, this is represented by k⊗_A P.',
  'Multiplication by ε becomes zero after tensoring with k. Thus k⊗_A P has term k in every degree n≤0 and zero differential. It follows directly that H^n(k⊗^L_A k)=k for every n≤0.',
  'The output is a bounded-above pseudo-coherent complex over k, but it has no lower cohomology bound. For the exact inclusion J:D^b(k)_coh→D^−(k)_coh, every object in its essential image has a lower cohomology bound. Cohomology is invariant under derived isomorphism, so this explicit output cannot be isomorphic to J(B) for any B in D^b(k)_coh.',
  'Consequently the first displayed tensor functor does not have the asserted bounded target for these inputs. The first Grothendieck map is not supplied by that advertised functor. This conclusion concerns the specific tensor construction, and makes no claim that no abstract bilinear map between the underlying groups can exist.'
 ],
 'relation_to_the_projection_domain_decision':'The separate correction in identification_295.json concerns 3.3.2.3. Its second branch uses E perfect relative to X→S itself, so E has finite S-amplitude. In the present example E1 is perfect relative to id_Spec k, while its S-amplitude is unbounded: the same Tor computation gives Tor_i^A(k,k)=k in every degree. The identity of the underlying complex does not identify these two relative-amplitude conditions. The explicit structural map Spec k→Spec A and its derived pullback compute their relationship.',
 'textual_action':'No patch to 3.3.3. Preserve both printed category pairings and group homomorphism displays in diplomatic and current forms, and carry this author-claim note into the editorial apparatus.',
 'scope_limit':'The counterexample proves failure of the first bounded category pairing and its stated functor-induced group map. It does not claim a defect in the second perfect/perfect pairing, and no replacement theorem is proposed. The regional views of III231 and III256 add no full-page status.'
}
(HERE/'author_claim_issue_295.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
old=next(x for x in read('page_status.jsonl') if x['page']==295)
suffix=' The first external tensor pairing in 3.3.3 is faithfully transcribed but has a separate author-claim obstruction, ASTRA-IV-AUTHOR-CLAIM-295; see author_claim_issue_295.json. No textual replacement is made.'
if suffix not in old['notes']:old['notes']+=suffix
r.pages.append(old)
r.commit()
