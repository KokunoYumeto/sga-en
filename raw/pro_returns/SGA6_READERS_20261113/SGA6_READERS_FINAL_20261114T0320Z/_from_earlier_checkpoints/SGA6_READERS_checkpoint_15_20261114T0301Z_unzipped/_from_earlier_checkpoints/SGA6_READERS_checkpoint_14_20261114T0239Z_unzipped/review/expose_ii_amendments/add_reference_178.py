#!/usr/bin/env python3
"""Post-checkpoint05 regional reference amendment; frozen II is read-only."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
id='ASTRA-II-REF-178-POST05'
reason=('Both scans explicitly print 1.2.1. The actual Proposition 1.2 heading is on 161; clauses b), c), d) are on 162 and their proof ends on 163. Clause b supplies a bounded representative with the stated amplitude, c supplies the canonical fully faithful homotopy-to-derived functor and its perfect essential image, and d supplies an actual quasi-isomorphism and removes the acyclic quotient under relevability. These are precisely the three operations in 2.3.2(c). The accompanying identification packet proves the specialization through Loclib and explicit contractible stabilization; it does not identify local finite free modules with local direct summands. Correct only the locator in current and retain the source locator in diplomatic. The printed C_0=Lib wording remains unchanged, with its required additional argument documented separately.')
row=dict(source_id=id,page=178,record_type='own_finding',kind='misprint_in_print',verdict='not applied and now applied',printed_reading='L’assertion c) résulte de (1.2.1 b),c),d)), où C=Mod et C_0=Lib.',tex='Both frozen layers retain (1.2.1 b),c),d)).',change='Current locator 1.2.1 → 1.2 only; diplomatic retains the extra .1.',image='scan/SGA6_scan_360dpi.pdf#page=192; scan/SGA6_witness_300dpi.djvu#page=189; scan/SGA6_scan_360dpi.pdf#pages=175-177,191',region='Proof of 2.3.2(c); matched Proposition 1.2 heading and clauses b–d',reason=reason,forms='French current; corresponding English corrected variant. Diplomatic source reading preserved.',amendment_stage='After frozen checkpoint05',regional_review_only=True,discovered_by='English transfer review')
patch=dict(page=178,layer='current',old="L'assertion c) résulte de (1.2.1 b),c),d)),",new="L'assertion c) résulte de (1.2 b),c),d)),",source_id=id,reason=reason,expected_count=1,apply_after='review/expose_ii/patches.jsonl')
t=(ROOT/'build/page_packets/178/current.tex').read_text()
for p in map(json.loads,(ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines()):
 if p['page']==178 and p['layer'] in ('current','both'):
  assert t.count(p['old'])==p.get('expected_count',1)
  t=t.replace(p['old'],p['new'])
assert t.count(patch['old'])==1
(HERE/'own_findings.jsonl').write_text(json.dumps(row,ensure_ascii=False)+'\n')
(HERE/'patches.jsonl').write_text(json.dumps(patch,ensure_ascii=False)+'\n')
packet={
 'source_id':id,'page':178,'status':'Source reading decided; locator correction supported; source specialization wording preserved',
 'evidence':[
  {'path':'review/expose_ii_amendments/main_178_reference.png','inspection':'Directly viewed enlarged source reference and its C=Mod, C_0=Lib wording.'},
  {'path':'review/expose_ii_amendments/witness_178_reference.png','inspection':'Directly viewed native witness 189; agrees with the extra .1.'},
  {'path':'review/expose_ii/page_161_s4.png','inspection':'Directly viewed Proposition 1.2 heading.'},
  {'path':'review/expose_ii/page_162_s1.png','inspection':'Directly viewed definition of C_1 and clause b.'},
  {'path':'review/expose_ii/page_162_s2.png','inspection':'Directly viewed canonical quotient functor c and quasi-isomorphism clause d.'},
  {'path':'review/expose_ii/page_163_s1.png','inspection':'Directly viewed conclusion of proof 1.2, then the §2 heading.'},
  {'path':'review/expose_ii/page_163_s2.png','inspection':'Directly viewed Lib/Loclib definition: free versus locally direct summands of free, of finite type.'},
  {'path':'review/expose_ii/page_177_s3.png','inspection':'Directly viewed the quasi-isomorphism, degree conditions and canonical functor to which the reference applies.'}
 ],
 'fixed_setting':'The S and A of Proposition 2.3.2: S compact, A a soft sheaf of rings; use the already proved clause (a).',
 'identifications':[
  'Take C(U)=Mod(U) and P(U)=Loclib(U). P is locally closed under kernels of epimorphisms: an epimorphism onto a local direct summand of a finite free module splits locally, and its kernel is again a local direct summand. Local lifting follows the same split-epimorphism property (I 1.3.1).',
  'The category called C_1S in 1.2, for C_0=P, equals Loclib(S): local membership in the locally defined direct-summand class is the same property. The identification functor is the identity on each A-module and on each A-linear morphism.',
  'Global relevability is 2.3.2(a). The finite-presentation branch of 1.1(ii) follows because the relevant modules are finite type, softness supplies global sections, and compactness plus 2.1.1(b) supplies an epimorphism A_S^N→M. Thus the global type-finite condition holds with P as well.',
  'The amplitude notion in I 4.8 uses local finite direct summands. Its local complexes and those for P have identical terms after refining the finite collection of trivializing covers, so the identity on complexes gives the same derived object and amplitude interval.'
 ],
 'clause_mapping':{
  '1.2(b)':'Applied with P, produces a representative G in degrees [m,n] with every term in Loclib(S).',
  '1.2(d)':'Global relevability upgrades this to a quasi-isomorphism u:G→E. It also makes the acyclic subcategory of K^b(Loclib(S)) zero.',
  '1.2(c)':'The canonical functor sends each bounded Loclib complex and each chain-map class to the same complex/map in D(S). After 1.2(d), no quotient remains. Its image is the objects with finite perfect amplitude; compactness turns locally bounded amplitude into one interval using a finite subcover.'
 },
 'free_term_construction':[
  'Every P in Loclib(S) is a global direct summand of finite free A_S^N: choose A_S^N→P using softness, finite type, and compactness; split it using 2.3.2(a). Write A_S^N=P⊕Q. Q is again in Loclib(S).',
  'Starting at degree n and descending through m+1, choose a complement Q to the current degree-i term G^i. Add the disk D_i(Q), with Q in degrees i−1 and i and differential id_Q; all other terms and differentials of this disk are zero.',
  'The new degree-i term G^i⊕Q is finite free; the degree-(i−1) term remains in Loclib(S). The already treated higher terms are unchanged. Repetition gives F supported in [m,n], finite free in every degree above m, and in Loclib(S) in degree m.',
  'For each addition, projection π:G⊕D_i(Q)→G and inclusion j:G→G⊕D_i(Q) are chain maps with πj=id. The homotopy h^i=id_Q:Q→Q in degree i→i−1 gives dh+hd=id−jπ. Thus π is a homotopy equivalence. The composite F→G→E is the required quasi-isomorphism.'
 ],
 'scope_limit':'This packet corrects only the extra .1 in the locator. It retains the printed C_0=Lib phrase and supplies the explicit intermediate construction; it does not silently equate Lib and Loclib or rewrite Proposition 1.2. No page is newly marked fully checked by this regional amendment.',
 'frozen_files':'review/expose_ii and checkpoint05 remain unchanged.'
}
(HERE/'reference_178_identification.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'new_current_patch':1,'new_own_finding':1,'frozen_ii_unchanged':True}))
