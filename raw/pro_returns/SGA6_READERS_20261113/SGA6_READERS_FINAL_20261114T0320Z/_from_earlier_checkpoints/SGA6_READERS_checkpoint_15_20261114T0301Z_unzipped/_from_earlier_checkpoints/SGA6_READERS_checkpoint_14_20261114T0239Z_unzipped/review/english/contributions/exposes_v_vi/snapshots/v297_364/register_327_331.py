#!/usr/bin/env python3
"""Register the complete English transfer of folios327–331."""
from pathlib import Path
import json, sys, hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH, build_records, dump, ROOT
def units(page,layer):
    return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(page)/f'{layer}.tex').read_text())]
pairs=json.loads((HERE/'lexical_math_pairs.json').read_text());pairs=[p for p in pairs if p['page']!=331]
for index in [6,12]:
    fr=units(331,'current')[index]
    en=fr.replace(r'\text{avec }',r'\text{with }').replace(r'\text{et }',r'\text{and }')
    assert fr!=en
    pairs.append(dict(page=331,layer='both',French_literal_unit=fr,English_literal_unit=en,expected_multiplicity=1,status='individually reviewed lexical translation only',scope=f'Complete generator equation,unit{index};only avec/et are translated as with/and. Every weight bound,quantifier,low ellipsis,index,augmentation glyph,and other character is preserved.'))
dump(HERE/'lexical_math_pairs.json',pairs)
def variant(page,index,source,mode,suffix='01'):
    c,d=units(page,'current')[index],units(page,'diplomatic')[index];assert c!=d
    if mode=='math':c,d=c[2:-2],d[2:-2]
    return dict(id=f'EN-CONTRIB-V-{page}-{suffix}',page=page,old=c,printed=d,mode=mode,source=source)
packets=[]
for page,sid in [(327,'ASTRA-V-NUMERATOR-327'),(331,'ASTRA-V-GENERATION-331')]:
    rel=f'review/expose_v/identification_{page}.json';path=ROOT/rel
    packets.append(dict(record_type='attributed_mathematical_identification',page=page,source_id=sid,packet=rel,packet_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),decision='Preserve the full source-linked calculation separately from the translated author body. The327 packet supports its explicit numerator variant;the331 packet proves the exact generation assertion,including negative integral coefficients,while retaining the printed unsigned-sum shorthand.'))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=327]
batches.append(dict(expose='V',first=327,last=331,
    native_start=r'\sgaStableTarget{sga6.e05.eq.3-5-1}',
    native_end=r'\sgaStableTarget{sga6.e05.prop.3-11}',
    source='review/expose_v/FROZEN_HANDOFF.md; reviewed French327–331 in both forms',
    reason='Complete reconstruction of the transported-product calculation,the full lambda-prime construction and its relations,the two structure diagrams,the rank augmentation example,and the filtration definition and proof. All nineteen native targets remain in order. The source font and map distinctions are transferred occurrence by occurrence,without replacing the original proof shorthand.',
    variants=[variant(327,0,'ASTRA-V-NUMERATOR-327','display'),variant(327,16,'ASTRA-V-UNIT-DENOMINATOR-327','math','02'),variant(328,0,'check/findings/findings_326_330.json#13','display'),variant(329,7,'check/findings/findings_326_330.json#25','display'),variant(329,10,'ASTRA-V-SLASH-329','display','02')],
    notes=[
        dict(page=327,source_id='ASTRA-V-NUMERATOR-327;ASTRA-V-PRODUCT-GLYPHS-327;ASTRA-V-PARAGRAPH-327;ASTRA-V-UNIT-DENOMINATOR-327',English_rendering='the complete product calculation and transported-operations definition',decision='Keep rho without an inserted t in3.5.1,restore the coefficient ring,the total-variable weight statement and symmetry clause,the n∈N quantifier,and the underlined unit. Branch only the justified extra inner1+ and denominator grouping. Restore the complete lambda-prime composite omitted by native English. The observed nabla signs are related to the prior printed v by the exact map rho∘m∘(rho^{-1}×rho^{-1}),with each local glyph retained.'),
        dict(page=328,source_id='check/findings/findings_326_330.json#13;ASTRA-V-INTEGER-FONT-328;ASTRA-V-PARAGRAPH-328',English_rendering='all five rows of the lambda-prime computation and full3.7 opening',decision='Restore the entire omitted calculation,including every circle/nabla unit subscript and the rho_u inverse. Its missing rho is explicitly branched. Preserve plain Z in the coefficient ring and reinforced N in3.6.3,the actual source series,and the isomorphism rho justification. The two functor names retain their literal source subscripts and macros rather than native substitutions.'),
        dict(page=329,source_id='check/findings/findings_326_330.json#22',English_rendering='commutative',decision='French commumatif/commutatif has the same English adjective in both forms; the exact composites are preserved by the full source diagrams.'),
        dict(page=329,source_id='check/findings/findings_326_330.json#25;ASTRA-V-SLASH-329;ASTRA-V-PRODUCT-GLYPHS-329',English_rendering='both exact structure diagrams and complete scalar-product calculation',decision='Preserve the source placement of o/nabla subscripts on the literal nested functor arguments. The missing gamma_t arrowhead and unparenthesized unit denominator are separately branched. Restore the full unnumbered rho_t calculation preceding3.8.2 and every explicit variable or locator omitted from the native summary.'),
        dict(page=330,source_id='check/findings/findings_326_330.json#32;review/expose_v/page_status.jsonl#page330',English_rendering='complete augmented-algebra definition and rank construction',decision='French entraine/entraîne renders identically as implies. Restore the explicit K-linear lambda-homomorphism definition,the commutative locally ringed hypothesis,the referenced local-free/direct-summand explanation,the binomial coefficient-ring assertion,and the full separate F/F-prime construction on each sign range of n. Preserve all K-bullet and underlined integer-sheaf symbols,all zero boundaries,and the final rank-additivity argument. The source map A→K is not given an added epsilon label in Definition3.9.'),
        dict(page=331,source_id='ASTRA-V-PARAGRAPH-331;check/findings/findings_331_335.json#2;ASTRA-V-ELLIPSES-331;ASTRA-V-GENERATION-331',English_rendering='full filtration definition and generation proof',decision='Retain the undotted plain3.10 label after the integrated middle/local patch stream,the inclusive n≥0 bound,the full alpha∈I and epsilon quantifiers,and all four low ellipses. Restore the entire proof omitted by native English,including the unparenthesized source sums exactly as printed. The independent signed-coefficient proof is linked separately;no additional coefficients are inserted into the author body. Restore the concluding convention about which filtration is meant unless expressly stated otherwise.'),
        dict(page=331,source_id='review/expose_v/page_status.jsonl#pages327-331',English_rendering='five exact page boundaries,nineteen native targets,and no author notes',decision='Every prose clause,formula,diagram and its placement was manually compared with the reviewed French. The3.7 sentence retains its328/329 continuation. No original author-note call/text or macro continuation block occurs in this batch.')
    ],extra_records=packets,retained_proof_audits=['ASTRA-V-GENERATION-331']))
dump(HERE/'batches.json',batches);build_records()
