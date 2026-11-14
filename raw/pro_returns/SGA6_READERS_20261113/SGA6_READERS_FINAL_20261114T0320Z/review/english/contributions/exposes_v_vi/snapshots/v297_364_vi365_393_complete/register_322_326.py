#!/usr/bin/env python3
"""Record English folios 322–326 and the internal323/324 macro boundary."""
from pathlib import Path
import json, sys, re, hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH, build_records, dump, ROOT
def units(page,layer):
    return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(page)/f'{layer}.tex').read_text())]
pairs=json.loads((HERE/'lexical_math_pairs.json').read_text())
pairs=[p for p in pairs if p['page'] not in [322,324,325]]
for layer in ['current','diplomatic']:
    fr=units(322,layer)[4]
    en=fr.replace(r'\text{ est sans torsion}',r'\text{ is torsion-free}').replace(r'\text{on a}',r'\text{we have}')
    assert en!=fr
    pairs.append(dict(page=322,layer=layer,French_literal_unit=fr,English_literal_unit=en,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='Complete two-condition display; only est sans torsion/on a are translated. The current binomial and diplomatic fraction remain distinct and every other literal character is preserved.'))
fr=units(324,'current')[6]
en=fr.replace(r"\text{d'après (2.3.2), donc :}",r'\text{by (2.3.2), hence:}')
assert en!=fr
pairs.append(dict(page=324,layer='both',French_literal_unit=fr,English_literal_unit=en,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='Complete first display; translate the lexical explanation with its unchanged2.3.2 locator. All mathematical characters and whitespace outside the lexical text are retained.'))
for layer in ['current','diplomatic']:
    fr=units(325,layer)[11];en=fr.replace(r'\text{\uline{donc}}',r'\text{\uline{hence}}')
    assert en!=fr
    pairs.append(dict(page=325,layer=layer,French_literal_unit=fr,English_literal_unit=en,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='Complete first substitution display; translate only the underlined donc as hence. Its local slash-grouping branch remains literal.'))
dump(HERE/'lexical_math_pairs.json',pairs)
def english_unit(page,layer,index):
    raw=units(page,layer)[index]
    return next((p['English_literal_unit'] for p in pairs if p['page']==page and p['layer'] in (layer,'both') and p['French_literal_unit']==raw),raw)
def variant(page,index,source,mode,suffix='01'):
    c,d=english_unit(page,'current',index),english_unit(page,'diplomatic',index)
    assert c!=d
    if mode=='math':c,d=c[2:-2],d[2:-2]
    return dict(id=f'EN-CONTRIB-V-{page}-{suffix}',page=page,old=c,printed=d,mode=mode,source=source)
vs=[variant(322,1,'check/findings/findings_321_325.json#8','display'),variant(322,4,'check/findings/findings_321_325.json#13','display','02'),
    dict(id='EN-CONTRIB-V-323-01',page=323,old=r'pre-\(\lambda\)-ring \(Z\)',printed=r'pre- -ring \(Z\)',mode='text',source='check/findings/findings_321_325.json#15'),
    dict(id='EN-CONTRIB-V-323-02',page=323,old=r'(2.5.a)) is a \(\lambda\)-ring;',printed='(2.5.a)) is a -ring;',mode='text',source='check/findings/findings_321_325.json#17')]
for num,index in enumerate([11,12,17,19,21],1):
    vs.append(variant(325,index,'ASTRA-V-SUBSTITUTION-325','display' if index in [11,12] else 'text',f'{num:02}'))
vs.extend([variant(326,18,'ASTRA-V-SUBSTITUTION-326','math'),variant(326,30,'check/findings/findings_326_330.json#4','display','02')])
native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
start=native.index(r'\sgaStableTarget{sga6.e05.eq.2-9-2}')
end=native.index(r'\sgaStableTarget{sga6.e05.continuation-of-2-9}',start)
native_block='\n'.join(re.findall(r'(?m)^\\(?:provide|renew)command.*$',native[start:end]))+'\n'
fr323=(HERE/'source_packets/323/current.tex').read_text()
reviewed_block='\n'.join(re.findall(r'(?m)^\\(?:provide|renew)command.*$',fr323))+'\n'
translation=(HERE/'translations/323.tex').read_text()
assert len(native_block.splitlines())==len(reviewed_block.splitlines())==11
assert translation.count(native_block)==translation.count(reviewed_block)==1
assert native_block.replace(r'\providecommand{\id}',r'\renewcommand{\id}')==reviewed_block
sha=lambda x:hashlib.sha256(x.encode()).hexdigest()
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=322]
batches.append(dict(expose='V',first=322,last=326,
    native_start='which are checked by \\hyperlink{sga6.e05.thm.1-10}{1.10} on the elements',
    native_end=r'\sgaStableTarget{sga6.e05.eq.3-5-1}',
    source='review/expose_v/FROZEN_HANDOFF.md; reviewed French322–326 in both forms',
    reason='Complete reconstruction of the binomial-ring examples and the introduction and proof of the gamma operations,retaining every source clause,formula,and explicit transport map. All eighteen native stable targets are retained. The complete native and reviewed eleven-command continuation blocks stay at323/324;the native added continuation heading is removed while its target remains.',
    variants=vs,
    notes=[
        dict(page=322,source_id='check/findings/findings_321_325.json#8;check/findings/findings_321_325.json#13;ASTRA-V-PARAGRAPH-322',English_rendering='complete diagrams verification and the binomial coefficient construction',decision='Both source defects are explicitly branched:the missing1+ in the first product factor and fraction x/n versus binomial(x,n). Restore all underlined units,full application parentheses,the literal coefficient ring(K tensor_Z Q)[[t]],the tensor base in the later injection,and the exact2.6.i) locator. The source quantifier words on a remain present as we have inside the conditions display.'),
        dict(page=323,source_id='check/findings/findings_321_325.json#15;check/findings/findings_321_325.json#16;check/findings/findings_321_325.json#17;ASTRA-V-INK-323',English_rendering='integer specialization,binomial definition,sheaf example,and exponentiation',decision='The two missing lambda symbols have independent text branches,retaining the actual gaps and hyphens in diplomatic English. Plain Z remains plain in both branches under the exact identity n↦n from2.5.a). Restore the separately underlined sheaf K and integer sheaf,all statement underline groups,the full two-variable phi/psi argument,and the source semicolons. The overstruck separator and isolated tiny ink mark remain documented in the French evidence packet without added English formula tokens.'),
        dict(page=324,source_id='check/findings/findings_321_325.json#24;ASTRA-V-PARAGRAPH-324',English_rendering='new operations',decision='French oérations/opérations has the same English noun operations in both forms. Restore the complete3.1 author paragraph,including its qualification about later conditions and its quoted justification,without replacing its class expression by the native added direct-sum construction.'),
        dict(page=324,source_id='review/expose_v/page_status.jsonl#page324',English_rendering='a in K,the scalar-operation map,and the full K-lambda-algebra definition',decision='Restore the actual assumption a∈K,the Ghat(K[X]) source of the universal element,the source citation inside the first display,and the full explanation that a K-lambda-algebra is a lambda-ring with a lambda-homomorphism K→A. The native extra Continuation of2.9 heading is omitted from printed body;its stable target remains at the beginning of324.'),
        dict(page=325,source_id='ASTRA-V-ACCENT-325;ASTRA-V-PROOF-RULE-325;ASTRA-V-INK-325',English_rendering='interpreted;Proof;full coefficient calculation',decision='The French interprêtera/interprétera accent difference gives the same quoted English verb interpreted. Restore the exact class(cl(E)−d)+n and substitution x=cl(E)−d,the source inline quantified identity,the underlined Proof label,the omitted intermediate binomial expansion,and both final sums with only their printed lower bound. No extra formula token is inferred from the isolated small ink mark.'),
        dict(page=325,source_id='ASTRA-V-SUBSTITUTION-325',English_rendering='all five slash forms as separate explicit branches',decision='Each observed unparenthesized source denominator is preserved diplomatically. Current uses the exact rho_minus substitution t↦t/(1−t),its inverse t↦t/(1+t),and lambda_t(−1)=(1+t)^{-1} established in the frozen source record. The translated underlined hence is registered separately in both complete display forms.'),
        dict(page=326,source_id='check/findings/findings_326_330.json#3;ASTRA-V-PARAGRAPHS-326',English_rendering='By Definition3.2.ii)',decision='The French article le/la repair renders identically in English. Restore the source starting hypotheses K,K-prime lambda-rings with f a ring homomorphism,the quantification in x,and the literal Gg(f)∘gamma_t(x) formula. The three paragraph labels remain plain.'),
        dict(page=326,source_id='ASTRA-V-SUBSTITUTION-326;check/findings/findings_326_330.json#4;check/findings/findings_326_330.json#5',English_rendering='complete transport-of-structure argument and new multiplication v',decision='Restore the full naturality and transport paragraph,the explicit gamma_t=rho_t∘lambda_t display,and the universal input pair. Keep the source Latin v at this occurrence and the arrow labels rho without an inserted t. The rho substitution denominator and the pair-label stop/comma have separate branches,each supported by the actual inverse-substitution or Cartesian-product map.'),
        dict(page=326,source_id='review/expose_v/page_status.jsonl#pages322-326',English_rendering='five source boundaries,eighteen native targets,and no author notes',decision='Every prose clause and mathematical placement was manually compared with the reviewed source. The322 page closes the preceding enumerate;the Chern-class quotation spans324/325 at the original semantic boundary. There is no original author-note call or text in this batch. The internal continuation macro block is recorded separately below.')
    ],
    extra_records=[dict(record_type='continuation_macro_boundary',page=323,next_page=324,source_id='fixes/FIXLOG_6.jsonl#341',native_block=native_block,native_block_sha256=sha(native_block),reviewed_French_block=reviewed_block,reviewed_French_block_sha256=sha(reviewed_block),English_order='native block,then reviewed French block,then folio324',decision='Both complete eleven-command blocks are retained at their actual source boundary. The reviewed id renewal is effective after the native provide. This records scoped TeX state only;the frozen source audit explicitly reports no printed id/Id occurrence on323. No definition is moved to an earlier folio.')],
    retained_proof_audits=[]))
dump(HERE/'batches.json',batches);build_records()
