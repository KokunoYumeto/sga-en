#!/usr/bin/env python3
"""Register English332–336, with the retained4.12 author-claim packet."""
from pathlib import Path
import json, sys, hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH, build_records, dump, ROOT
def units(page,layer):
    return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(page)/f'{layer}.tex').read_text())]
def variant(page,index,source,mode,suffix='01'):
    c,d=units(page,'current')[index],units(page,'diplomatic')[index];assert c!=d
    if mode=='math':c,d=c[2:-2],d[2:-2]
    return dict(id=f'EN-CONTRIB-V-{page}-{suffix}',page=page,old=c,printed=d,mode=mode,source=source)
vs=[variant(332,3,'check/findings/findings_331_335.json#4','math'),
    dict(id='EN-CONTRIB-V-334-01',page=334,old='and let '+units(334,'current')[11]+' be a family',printed='and let '+units(334,'diplomatic')[11]+' be a family',mode='text',source='check/findings/findings_331_335.json#8'),
    dict(id='EN-CONTRIB-V-334-02',page=334,old='as follows from relations 3.2.',printed='as follows from solutions 3.2.',mode='text',source='ASTRA-V-REFERENCE-334'),
    variant(334,50,'check/findings/findings_331_335.json#9','math','03'),
    dict(id='EN-CONTRIB-V-334-04',page=334,old=units(334,'current')[52]+'.',printed=units(334,'current')[52],mode='text',source='check/findings/findings_331_335.json#10'),
    variant(335,32,'check/findings/findings_331_335.json#12','text'),
    variant(336,30,'ASTRA-V-COEFFICIENT-PARAMETER-336','text'),
    variant(336,31,'ASTRA-V-COEFFICIENT-PARAMETER-336','text','02')]
packets=[]
dest=HERE/'attributed_source_audits';dest.mkdir(exist_ok=True)
for page,sid,name in [(334,'ASTRA-V-REFERENCE-334','identification_334.json'),(336,'ASTRA-V-COEFFICIENT-PARAMETER-336','identification_336.json'),(336,'ASTRA-V-AUTHOR-CLAIM-336','author_claim_issue_336.json')]:
    rel='review/expose_v/'+name;raw=(ROOT/rel).read_bytes();(dest/name).write_bytes(raw)
    packets.append(dict(record_type='attributed_source_audit_packet',page=page,source_id=sid,source_packet=rel,contribution_copy='review/english/contributions/exposes_v_vi/attributed_source_audits/'+name,packet_sha256=hashlib.sha256(raw).hexdigest(),decision='Exact copy of the frozen French proof audit,attributed to that source review. The334 inverse coefficient maps support its lexical relation-name correction;the336 augmentation map supports two parameter corrections;the separate4.12 counterexample is retained as an author-claim issue without replacing the author statement.'))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=332]
batches.append(dict(expose='V',first=332,last=336,
    native_start=r'\sgaStableTarget{sga6.e05.prop.3-11}',
    native_end=r'writing the generators of \(\Fil^kB\) as products of \(\gamma\)-operations',
    source='review/expose_v/FROZEN_HANDOFF.md; reviewed French332–336 in both forms',
    reason='Complete reconstruction of Proposition3.11,the free lambda-ring construction,all universal properties and quotient arguments,the bounded-generator proof,and the exact Lemma4.11/Proposition4.12 passage. All seventeen native stable targets remain in order. Every source formula and proof paragraph is retained;the source author-claim issue is recorded outside the author body.',
    variants=vs,
    notes=[
        dict(page=332,source_id='ASTRA-V-STATEMENT-RULES-332;ASTRA-V-PARAGRAPH-332;check/findings/findings_331_335.json#4',English_rendering='the exact lambda-vanishing hypothesis and complete3.11 proof',decision='Restore lambda^j(y_i)=0 rather than the native gamma substitution,the separate i=1,...,n family list,and the full expansion proving gamma^j(y_i−1)=0. Its two-dot list is explicitly branched. Preserve each observed lexical rule,including plain ring,on a/we have,and the ordinal suffix. Restore the category C_0 sentence and the full4.1 ring-map construction and commutativity check,using the source lambda^n X_i variable names.'),
        dict(page=333,source_id='ASTRA-V-STATEMENT-RULES-333;ASTRA-V-PRODUCT-DOT-333;ASTRA-V-PRODUCT-GLYPH-333;ASTRA-V-INK-333',English_rendering='complete universal-property proof,gamma construction,and lambda-ideal definition',decision='Restore all omitted maps and equality tests,the literal gamma^n X_i variables,the low product dot and local nabla index,the full comparison of the two universal properties,and the positive bound n≥1. Preserve the exact lexical emphasis on named definitions,with mathematical symbols and defined terms separately plain. The visibly broken f stem is not assigned an added underline. Restore the quotient composite and its continuation onto334.'),
        dict(page=334,source_id='check/findings/findings_331_335.json#8;check/findings/findings_331_335.json#9;check/findings/findings_331_335.json#10;ASTRA-V-REFERENCE-334;ASTRA-V-STATEMENT-RULES-334',English_rendering='all relation-evaluation definitions and the full quotient universal property',decision='Restore the ordinary ideal generated by lambda^n(x_i),the explicit relation families and substitutions,the gamma-stability argument,and the factorization proof. The inner family prime,solutions/relations noun,the missing f-prime label,and final sentence stop each have independent branches. The source gives the quotient map f-prime(a+J)=f(a) and the inverse triangular lambda/gamma transformations as the exact identifications supporting those repairs.'),
        dict(page=335,source_id='check/findings/findings_331_335.json#12;ASTRA-V-STATEMENT-RULES-335;ASTRA-V-PARAGRAPHS-335;ASTRA-V-PHI-335',English_rendering='complete finite-degree proof and all of4.9.1',decision='Restore the full composite through Ghat(B),the literal image1 and equality lambda^k(phi)=1,the elementary-symmetric polynomial-ring embedding,and the entire three-member lambda_u product. The omitted first product upper n is explicitly branched;the following two bounds remain literal. Preserve the source small unit rule,open varphi,and all low ellipses. Restore the gamma alternative,the n_i≥2 hypothesis,and the precise indexed coefficient ring omitted by the native summary.'),
        dict(page=336,source_id='check/findings/findings_336_340.json#2',English_rendering='an augmented K-lambda-algebra structure',decision='French augmentés/augmentée agreement has the same English adjective augmented in both forms;no artificial English agreement error is introduced.'),
        dict(page=336,source_id='ASTRA-V-COEFFICIENT-PARAMETER-336;ASTRA-V-LOW-DOTS-336;ASTRA-V-PARENTHESIS-INK-336',English_rendering='exact monomial grading,Lemma4.11,and its full proof',decision='Restore M_k as monomials of weight exactly k and the source lemma on gamma^k(aX)=P-prime_k(gamma^i(a),gamma^j X),with coefficient filtration k−n. Native English instead described a different x+X expression;that substitution is removed. Both R parameters are separately branched from bare a to epsilon(a),using the actual scalar-exponent map A→K. Preserve all low product stops and the identified parenthesis strokes;no extra ink token is inserted.'),
        dict(page=336,source_id='ASTRA-V-AUTHOR-CLAIM-336',English_rendering='the exact printed4.12 equality and proof opening',decision='Retain B.M_(k+1) and the source exact-weight definition in both English forms. The evaluation B=Z[X,Y2,Y3,...]→Z[T],Y3↦T and all other displayed generators↦0,separates gamma^3 X in Fil^1B from ZX+B(X²,Y2). This complete obstruction is transferred as an attributed audit;no replacement theorem or altered tail is proposed. The native nonprinting4.12.1 target remains beside the source inline assertion without adding a printed equation number.'),
        dict(page=336,source_id='review/expose_v/page_status.jsonl#pages332-336',English_rendering='five exact boundaries,seventeen native targets,and no author notes',decision='Every prose clause,formula and its placement was manually compared with the reviewed French. The333/334 quotient sentence,the334/335 f-prime conclusion,and the335/336 augmentation construction retain their exact source continuations. The336 proof ends with these elements before its337 continuation. There is no original author note or macro continuation block in this batch.')
    ],extra_records=packets,retained_proof_audits=['ASTRA-V-AUTHOR-CLAIM-336']))
dump(HERE/'batches.json',batches);build_records()
