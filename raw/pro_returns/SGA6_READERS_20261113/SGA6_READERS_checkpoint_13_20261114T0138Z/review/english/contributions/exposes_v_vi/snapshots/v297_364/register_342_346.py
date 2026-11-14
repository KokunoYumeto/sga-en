#!/usr/bin/env python3
"""Register full342–346,including the native/reviewed346 continuation blocks."""
from pathlib import Path
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT,dump,build_records
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def units(p,layer):return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(p)/f'{layer}.tex').read_text())]
def lexical(s):
    return s.replace(r'\text{car }',r'\text{since }').replace(r'\text{, et on applique }',r'\text{, and we apply }').replace(r'\text{ et on applique }',r'\text{ and we apply }')
def variant(p,index,sid,mode,suffix='01',dindex=None):
    c,d=lexical(units(p,'current')[index]),lexical(units(p,'diplomatic')[index if dindex is None else dindex]);assert c!=d
    if mode=='math':c,d=c[2:-2],d[2:-2]
    return dict(id=f'EN-CONTRIB-V-{p}-{suffix}',page=p,old=c,printed=d,source=sid,mode=mode)
variants=[variant(342,11,'check/findings/findings_341_345.json#9','math'),
          variant(342,15,'ASTRA-V-GAMMA-EXPONENT-342','display','02'),
          dict(variant(342,29,'check/findings/findings_341_345.json#10','display','03'),related_sources=['check/findings/findings_341_345.json#11','check/findings/findings_341_345.json#13']),
          variant(345,0,'check/findings/findings_341_345.json#21','display'),
          variant(345,19,'check/findings/findings_341_345.json#23','math','02'),
          dict(id='EN-CONTRIB-V-345-03',page=345,old='admits (1,1) as its unit',printed='admits (1.1) as its unit',source='check/findings/findings_341_345.json#25',mode='text'),
          variant(346,6,'check/findings/findings_346_350.json#3','text'),
          dict(id='EN-CONTRIB-V-346-02',page=346,old=r'defines a morphism of functors on \(\mathcal G\):',printed=r'defines a morphism of functors on\qquad:',source='check/findings/findings_346_350.json#5',mode='text'),
          variant(346,9,'check/findings/findings_346_350.json#6','display','03',dindex=8)]
pairs=json.loads((HERE/'lexical_math_pairs.json').read_text());pairs=[p for p in pairs if p['page']!=342]
for layer in ['current','diplomatic']:
    f=units(342,layer)[29];e=lexical(f);assert f!=e
    pairs.append(dict(page=342,layer=layer,French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed translation of lexical text only',scope='The complete5.6 multirow calculation:car→since,and et on applique→and we apply. Every formula token,source punctuation branch and space outside those lexical text strings is unchanged.'))
dump(HERE/'lexical_math_pairs.json',pairs)
packets=[];dest=HERE/'attributed_source_audits';dest.mkdir(exist_ok=True)
for p,sid,name in [(342,'ASTRA-V-GAMMA-EXPONENT-342;ASTRA-V-UNIVERSAL-INJECTION-342','identification_342.json'),(343,'ASTRA-V-AUTHOR-CLAIM-343;ASTRA-V-LOCAL-CALCULATION-343;ASTRA-V-AUTHOR-CLAIM-CONTINUATION-344','author_claim_issue_343.json'),(345,'check/findings/findings_341_345.json#23;check/findings/findings_341_345.json#25','identification_345.json'),(346,'check/findings/findings_346_350.json#3;check/findings/findings_346_350.json#5;check/findings/findings_346_350.json#6','identification_346.json')]:
    rel='review/expose_v/'+name;raw=(ROOT/rel).read_bytes();(dest/name).write_bytes(raw)
    packets.append(dict(record_type='attributed_source_audit_packet',page=p,source_id=sid,source_packet=rel,contribution_copy='review/english/contributions/exposes_v_vi/attributed_source_audits/'+name,packet_sha256=hashlib.sha256(raw).hexdigest(),decision='Exact copy of the frozen French mathematical audit. Source corrections and retained author-claim issues are transferred with their precise coefficient maps,augmentation comparison,scalar inclusion and quotient descent;no proof claim is inferred from the automated unit check.'))
native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
start=r'In fact, when \(A\) is a \(\lambda\)-ring,';end=r'\sgaStableTarget{sga6.e05.expose.occ2}'
a=native.index(start);b=native.index(end,a)
native_block=re.search(r'(?:\\providecommand[^\n]*\n){12}',native[a:b]).group()
fr346=(HERE/'source_packets/346/current.tex').read_text()
reviewed_block=fr346[fr346.index('% Local macros for Exposé V, §§6--7'):].strip('\n')+'\n'
translated=(HERE/'translations/346.tex').read_text()
assert native_block in translated and reviewed_block in translated
assert translated.index(native_block)<translated.index(reviewed_block)
assert len(re.findall(r'\\(?:provide|renew)command',reviewed_block))==12
packets.append(dict(record_type='continuation_macro_boundary',page=346,next_page=347,source_id='fixes/FIXLOG_6.jsonl#342',native_block=native_block,reviewed_block=reviewed_block,native_block_sha256=sha(native_block),reviewed_block_sha256=sha(reviewed_block),decision='Preserve all twelve native definitions and all twelve reviewed continuation definitions at the actual346/347 boundary after the complete6.1 construction. The reviewed id renewal follows the native provide,with every other command unchanged. This is a scoped implementation continuation;it does not claim printed id usage on346.'))
for p,newpara,reason in [(341,False,'The341 by continues with342 sending in the same homomorphism construction.'),(342,True,'The source begins a new indented paragraph with Donc after the preceding display;checker341_345#14 confirms that break.'),(343,False,'The343 X0 continues with344 to x,and the filtration-compatibility conclusion remains the same sentence.'),(344,False,'The two functor morphisms announced at the344 colon are the first two345 displays.'),(345,True,'The345 scalar-action formula is followed by the separate346 paragraph constructing the lambda-algebra structure.')]:
    f=(HERE/'source_packets'/str(p)/'current.tex').read_text();g=(HERE/'source_packets'/str(p+1)/'current.tex').read_text()
    e=(HERE/'translations'/f'{p}.tex').read_text();n=(HERE/'translations'/f'{p+1}.tex').read_text()
    assert e.endswith('\n\n')==newpara
    assert not n.startswith('\n')
    packets.append(dict(record_type='manually_compared_source_folio_join',after=p,before=p+1,paragraph_break=newpara,source_tail=f[-400:],source_head=g[:400],English_tail=e[-250:],English_head=n[:250],source_page_sha256s={str(p):sha(f),str(p+1):sha(g)},reason=reason))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=342]
batches.append(dict(expose='V',first=342,last=346,native_start=start,native_end=end,
    source='review/expose_v/FROZEN_HANDOFF.md;reviewed French342–346 in both forms',
    reason='Complete reconstruction of the universal injection,the gamma coefficient calculation,all5.6 series manipulations,the literal5.7 proposition and proof,and the entire6.1 Chern-ring construction omitted by the native English. All seven native stable targets and the original continuation macro block remain in their corresponding passages.',variants=variants,
    notes=[
        dict(page=342,source_id='ASTRA-V-UNIVERSAL-INJECTION-342;ASTRA-V-GAMMA-EXPONENT-342;check/findings/findings_341_345.json#9',English_rendering='full universal injection and exact gamma-operation definition',decision='Restore the map sending(1,0) to1 and(0,x) to xD,its lambda compatibility,and the source injectivity proof. Its exact universal-case verification is copied separately. Restore the entire binomial sum,with Lambda/A and exponent i/p−i independently branched;the coefficient map[t^p] applied to(1+t)^(p−1)lambda_t(z) and the p=1,z=0 test justify the latter. The native target named5-5-2 accompanies source formula5.5.4,retaining the actual printed source number.'),
        dict(page=342,source_id='check/findings/findings_341_345.json#10;check/findings/findings_341_345.json#11;check/findings/findings_341_345.json#13;ASTRA-V-LOW-DOTS-342;ASTRA-V-PARAGRAPH-LABEL-342',English_rendering='the full5.6 universal-ring calculation',decision='Restore the three generators,both finite-degree constraints,the defining identity,and every row of the full series calculation. A complete display branch records separately the printed fraction-stop/current comma,the two-dot/three-dot denominator ending,and the doubled/single multiplication dot. Each has its own source audit and exact series identity;only the lexical explanation inside text is translated. Preserve the ordinary5.6 label and all other low product marks.'),
        dict(page=343,source_id='check/findings/findings_341_345.json#15;check/findings/findings_341_345.json#16;ASTRA-V-LOW-MARKS-343',English_rendering='the exact finite geometric sum and full ruled5.7 statement',decision='Preserve1+lowdots+L^(k−1),the unnumbered source series display,and the exact statement underline spans. The native5-6-1 stable target is retained without its invented printed label. Restore the complete universal weight-filtration paragraph,all separate generators,bounds and augmentation arrows,and the proof calculations.'),
        dict(page=343,source_id='ASTRA-V-AUTHOR-CLAIM-343;ASTRA-V-LOCAL-CALCULATION-343',English_rendering='the literal5.7 statement and its full printed proof',decision='Keep the unrestricted hypotheses and both unprimed N0 factors in the author body. The source audit exhibits K=A=Z,N=0,d=1,x=1,p=2,where the claimed value1 lies outside Fil^1Z=0,and the exact specialization U→−1 sends universal−U to1 while failing augmentation compatibility. Its nonlinear sign calculation also distinguishes the printed expression from both the exact expression and a prime-only replacement. No replacement theorem or isolated prime repair is inserted into English.'),
        dict(page=344,source_id='ASTRA-V-AUTHOR-CLAIM-CONTINUATION-344;ASTRA-V-FORMS-344;ASTRA-V-PLACEHOLDER-344',English_rendering='the literal proof conclusion and complete opening6.1 functor construction',decision='Keep the source conclusion linked to the same failed filtration transport. Restore the category C,actual G-hat restriction through i,all three restricted and all three extended functor morphisms,the distinct g and g-nabla subscripts,the full polynomial names,and the canonical map to the completed associated graded object. Remove the inherited added opening qualifier in the section title while preserving its stable target.'),
        dict(page=344,source_id='ASTRA-V-BINOMIAL-344',English_rendering='binomial ring',decision='French binomial/binomial-with-circumflex renders as the same English adjective binomial. The base ring and all named binomial operations are unchanged.'),
        dict(page=345,source_id='check/findings/findings_341_345.json#21;check/findings/findings_341_345.json#23;check/findings/findings_341_345.json#25;ASTRA-V-LOW-DOTS-345;ASTRA-V-SCRIPT-G-345',English_rendering='all of the multiplication,scalar action and augmented-ring formulas6.1.1–6.1.3',decision='Restore the two descended morphisms,the exact value of the star multiplication,the P-double-prime and R polynomial descriptions,the addition law,the full product and scalar-action formulas,and the augmentation ideal. The duplicated object-placeholder,the A/K scalar-domain quantifier,and(1.1)/(1,1) unit are separately branched. The actual projection pi(a,phi)=a,scalar inclusion j(a)=(a,1),kernel inclusion and two-sided unit computation are copied in identification_345.json.'),
        dict(page=345,source_id='check/findings/findings_341_345.json#22',English_rendering='composition laws defined by',decision='French definie/definies agreement leaves the English participle defined unchanged in both branches.'),
        dict(page=346,source_id='check/findings/findings_346_350.json#3;check/findings/findings_346_350.json#5;check/findings/findings_346_350.json#6;ASTRA-V-LOW-MARKS-346',English_rendering='the complete descended gamma-prime construction and6.1.4',decision='Restore both full functor morphisms,the coefficient definition Q-double-prime,the extension by K and its lambda-structure,the complete operation formula,and the final commutative-diagram verification. The completion hat,the source blank/category G,and the bare prime/gamma-prime label are independently branched. Their exact q_A map,homogeneous isomorphism and natural-transformation descent are copied separately.'),
        dict(page=346,source_id='ASTRA-V-COEFFICIENT-AGREEMENT-346',English_rendering='and will be denoted by',decision='French notee/note agreement has the same English participle denoted in both forms;the coefficient identification is unchanged.'),
        dict(page=346,source_id='review/expose_v/page_status.jsonl#pages342-346',English_rendering='five complete source pages,seven native targets,and exact continuation definitions',decision='Every prose clause,formula and placement was manually compared with the reviewed French. The five new joins are explicitly recorded. There is no original author note in this batch. The complete native and reviewed twelve-command blocks remain after346;the added inherited completion heading begins outside this replacement span and will be handled with347.')
    ],extra_records=packets,retained_proof_audits=['ASTRA-V-UNIVERSAL-INJECTION-342','ASTRA-V-AUTHOR-CLAIM-343','ASTRA-V-LOCAL-CALCULATION-343','ASTRA-V-AUTHOR-CLAIM-CONTINUATION-344']))
dump(HERE/'batches.json',batches);build_records()
