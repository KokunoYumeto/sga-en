#!/usr/bin/env python3
"""Register the manually compared VII 442–446 translation, within this contribution."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH
def units(page,layer='current'):
    text=(HERE/'source_packets'/str(page)/f'{layer}.tex').read_text()
    return [m.group() for m in MATH.finditer(text)]
variants=[]
def add(n,page,old,printed,source,mode='text',related=None):
    d=dict(id=f'EN-CONTRIB-VII-{n:03}',page=page,old=old,printed=printed,mode=mode,source=source)
    if related:d['related_sources']=related
    variants.append(d)
c,d=units(442),units(442,'diplomatic')
add(38,442,c[7],d[7],'check/findings/findings_441_445.json#16')
add(39,442,c[17],d[17],'check/findings/findings_441_445.json#18',related=['check/findings/findings_441_445.json#19'])
add(40,442,c[18],d[18],'ASTRA-VII-0075')
c,d=units(443),units(443,'diplomatic')
add(41,443,c[2],d[2],'ASTRA-VII-0076')
add(42,443,'On '+c[9]+' we obtain','On '+d[9]+' we obtain','ASTRA-VII-0076')
add(43,443,'so these are locally free of finite type','so these are free of finite type','ASTRA-VII-0084')
add(44,443,'over '+c[13]+'. We can therefore','over '+d[13]+'. We can therefore','ASTRA-VII-0076')
add(45,443,c[17],d[17],'ASTRA-VII-0076')
c,d=units(444),units(444,'diplomatic')
add(46,444,c[5],d[5],'check/findings/findings_441_445.json#24','display')
add(47,444,'hence the middle one is also an isomorphism.','hence the middle one is also an isomorphism','fixes/MISPRINTS_6.json#413')
add(48,445,'(VI 5.9), which gives the result.','(VI 5.9) which gives the result.','fixes/MISPRINTS_6.json#414')
c,d=units(445),units(445,'diplomatic')
add(49,445,c[21],d[21],'fixes/RECONCILE_CODEX_6.json#197','display')
c,d=units(446),units(446,'diplomatic')
add(50,446,c[16],d[16],'fixes/RECONCILE_CODEX_6.json#198')
config=dict(expose='VII',first=442,last=446,
    native_start=r"if \(f:X'\to X\) is projective and perfect,",
    native_end=r"Therefore coherent modules on \(X'\) with support in \(Y'\) are perfect.",
    source='review/expose_vii/HANDOFF.md and final_audit.json; exact reviewed French442–446',
    reason='Restores the entire high-twist lemma and both descending-induction arguments, every graded-presentation and direct-image comparison, and the full statement and kernel proof of3.7. Each observed local R/P/S change and every corrected source reading has an explicit branch. The printed all-n assertion and diagram remain with the exact separate defect audit.',
    variants=variants,retained_proof_audits=['ASTRA-VII-0085'],notes=[
      dict(page=442,source_id='complete recalled lemma and descending-induction proof',decision='Restore the full unnumbered lemma with independently ruled complex L and literal acyclicity bounds, the application to O_X-prime, both higher-image vanishings, all exact sequences and the beginning of the complete graded algebra construction. Three R glyphs and one projective P have explicit variants038–040; the two R glyphs in one formula share an atomic complete-unit branch and separate source rows.'),
      dict(page=443,source_id='ASTRA-VII-0084 and ASTRA-VII-0085',decision='Restore the complete finite graded presentation, both Proj sheaves, exact two-row diagram, structural map, degree components, high-twist kernel arguments and equality of direct images. The current localement insertion is explicit043 with its basis/trivialization proof. The printed assertion for every n and both tilde labels stay in both forms; the counterexample 0→A at n=0 is separately attributed, with no replacement range or theorem. All four projective P occurrences have distinct explicit branches041/042/044/045. The source absence of a rightmost vertical zero arrow is preserved.'),
      dict(page=444,source_id='complete descending comparison and Proposition3.6',decision='Restore the full second diagram, exact J-adic quotient identity, all three-arrow isomorphism arguments, proposition statement and entire projection-formula proof. The symmetric-algebra S glyph and missing terminal stop have explicit046/047. The native3.6.1 target remains at the unnumbered source display; no added equation tag is retained.'),
      dict(page=445,source_id='complete Theorem3.7 and first proof steps',decision='Restore both theorem clauses, all quantified domains, the left inverse, full proof of injectivity, the exact computation of v composed with u, and the kernel inclusion setup. Preserve the source i arrow-label side and baseline multiplication points. The native3.7.0/u/v/2 targets remain on the corresponding unnumbered source formulas. The missing comma and printed x in i_*(x) are explicit048/049.'),
      dict(page=446,source_id='complete kernel calculation and regular-local-ring proof',decision='Restore every equality used to prove3.7.1, both applications of3.4/3.6, the complete intersection-of-kernels argument usingVI5.10, and the regular-local-ring quotient argument with EGA0_IV17.1.8. The missing minus is explicit050. French nécéssairement/nécessairement and entraine/entraîne both translate necessarily and gives without artificial English spelling branches. The native inline target sga6.e07.eq.3-7-1 is moved immediately before the same equation, preserving its literal printed tag and destination; ordered target comparison now inventories both command forms. No source formula bytes change.')
    ])
path=HERE/'batches.json';configs=json.loads(path.read_text());configs=[x for x in configs if x['first']!=442];configs.append(config);configs.sort(key=lambda x:x['first']);path.write_text(json.dumps(configs,ensure_ascii=False,indent=2)+'\n')
print('Registered VII442–446:13 source-variant groups; exact source author issue retained separately.')
