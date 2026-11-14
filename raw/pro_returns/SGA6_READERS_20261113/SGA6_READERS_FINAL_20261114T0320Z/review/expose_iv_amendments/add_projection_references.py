#!/usr/bin/env python3
"""Post-freeze IV reference amendments; no frozen review file is modified."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
reason=('Both source loci explicitly print5.9 b). The directly inspected III272 heading is Remarques5.8; '
 'its clause b starts273 and contains the analytic canonical projection arrow Rf_*(E) tensor^L M→Rf_*(E tensor_Y^L M), '
 'followed by its isomorphism statement and the bibliography, with no intervening5.9. '
 'The arrow is the adjoint of Lf^*(Rf_*E tensor^L M)≅Lf^*Rf_*E tensor^L Lf^*M→E tensor^L Lf^*M, '
 'the last map being counit_E tensor identity_M. This is exactly the morphism invoked in IV, with no change of functor or arguments. '
 'On287, restrict to an open set carrying a bounded finite locally free representative of the perfect M; '
 'the bounded coherent E and this M satisfy the displayed5.8(b) domains, and the local projection maps are the restrictions of that same adjunction map. '
 'On289, the cited analytic ingredient is the same projection comparison, together with Grauert finiteness and the stated finite tor-dimension. '
 'Correct only the locator5.9→5.8 in current; retain the printed locator in diplomatic. Full map and scope details are in projection_reference_identification.json.')
rows=[];patches=[]
for page,old,new,region in (
 (287,'(III 5.9 b))','(III 5.8 b))','2.11.2, analytic projection-formula reference'),
 (289,'(III 4.8.1 et 5.9 b))','(III 4.8.1 et 5.8 b))','opening2.12 paragraph, perfect direct-image reference')):
 id=f'ASTRA-IV-REF-{page}-POSTFREEZE'
 rows.append(dict(source_id=id,page=page,record_type='own_finding',kind='misprint_in_print',
  verdict='not applied and now applied',printed_reading=old,tex='Both frozen layers retain the printed5.9 locator.',
  change='Current5.9→5.8 only; diplomatic retains5.9.',
  image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}; scan/SGA6_scan_360dpi.pdf#page=286; scan/SGA6_scan_360dpi.pdf#page=287',
  region=region,reason=reason,forms='French current and corresponding English corrected branch; diplomatic source preserved.',
  amendment_stage='After frozen IV/checkpoint06',regional_review_only=True,discovered_by='English transfer review'))
 patch=dict(page=page,layer='current',old=old,new=new,source_id=id,reason=reason,expected_count=1,apply_after='review/expose_iv/patches.jsonl')
 t=(ROOT/f'build/page_packets/{page}/current.tex').read_text()
 for p in map(json.loads,(ROOT/'review/expose_iv/patches.jsonl').read_text().splitlines()):
  if p['page']==page and p['layer'] in ('current','both'):
   assert t.count(p['old'])==p.get('expected_count',1),(page,p['source_id'])
   t=t.replace(p['old'],p['new'])
 assert t.count(old)==1,(page,old)
 patches.append(patch)
(HERE/'own_findings.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
(HERE/'patches.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in patches))
packet={
 'record_type':'reference_identification','source_ids':[r['source_id'] for r in rows],
 'pages':[287,289],'status':'Source digits decided; corrected locator5.8(b) identified by its exact canonical map.',
 'evidence':[
  {'path':'review/expose_iv/page_287_s3.png','inspection':'Directly viewed5.9 b) in main PDF301.'},
  {'path':'review/expose_iv_amendments/witness_287_reference.png','inspection':'Directly viewed native witness298; digit9 and clause b are unambiguous.'},
  {'path':'review/expose_iv/page_289_s1.png','inspection':'Directly viewed5.9 b) alongside4.8.1 in main PDF303.'},
  {'path':'review/expose_iv/witness_289_top.png','inspection':'Directly viewed native witness300; agrees with both locators.'},
  {'path':'review/expose_iii/images/p272.png','inspection':'Directly viewed heading Remarques5.8 and clause a at the chapter end.'},
  {'path':'review/expose_iii/images/p273.png','inspection':'Directly viewed clause b, the analytic projection formula, its complete explanatory text and immediate bibliography.'},
  {'path':'review/expose_iv_amendments/main_273_reference.png','inspection':'Directly viewed enlarged clause b and canonical arrow; source unmatched close is separately preserved by III review.'}
 ],
 'actual_target':{
  'locator':'III5.8(b), heading272 and clause273.',
  'printed_hypotheses':'f:X→Y analytic; X has bounded dimension; E belongs to D^-(X), M to D^-(Y)_coh.',
  'printed_map':'alpha_(E,M):Rf_*(E) tensor^L M→Rf_*(E tensor_Y^L M).',
  'position':'Clause b is followed by the bibliography; there is no numbered5.9 between this clause and the end of ExposéIII.'},
 'exact_map':{
  'relative_tensor':'E tensor_Y^L M means E tensor_(O_X)^L Lf^*M.',
  'adjoint':'alpha_(E,M) is adjoint under Lf^*⊣Rf_* to Lf^*(Rf_*E tensor_(O_Y)^L M)≅Lf^*Rf_*E tensor_(O_X)^L Lf^*M→E tensor_(O_X)^L Lf^*M.',
  'last_arrow':'counit_E tensor identity_(Lf^*M).',
  'identification':'IV287 uses the identical f,E,M and this alpha; no conjugation by another functor or replacement of tensor products is involved.',
  'local_perfect_specialization':'For the perfect M in IV287, choose each local bounded finite locally free representative. Its image is in D^-(U)_coh, and E restricted to f^(-1)U is bounded coherent, hence in D^-. The alpha supplied by III5.8(b) on U is the restriction of the same global adjunction-defined alpha. These local isomorphisms give the claimed projection isomorphism and therefore the equality of its K-classes.',
  'IV289_use':'The analytic branch of the perfect direct-image assertion cites the same alpha. With local finite tor-amplitude of f and a bounded locally free representative of E, E tensor_Y^L M has a fixed bounded degree range for coherent modules M in degree0. The finite cohomological dimension stated in5.8(b) bounds the range after Rf_*, and alpha identifies that object with Rf_*E tensor^L M. Grauert supplies the coherent direct-image cohomology. Thus the reference points to precisely the projection comparison used in the existing finite-amplitude argument; the algebraic companion locator4.8.1 is left untouched.'},
 'prior_coverage':'The frozen IV records confirmed the literal page text and glyphs but had no separate mathematical adjudication of these two locators. This amendment supplies that missing reference decision.',
 'scope_limit':'Only two current locator digits are changed. No new theorem or hypothesis is inserted. No page is newly marked fully checked by this regional amendment.',
 'frozen_files':'review/expose_iv, review/expose_iii and existing checkpoints remain unchanged.'
}
(HERE/'projection_reference_identification.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_own_findings':2,'new_current_patches':2,'frozen_iv_unchanged':True}))
