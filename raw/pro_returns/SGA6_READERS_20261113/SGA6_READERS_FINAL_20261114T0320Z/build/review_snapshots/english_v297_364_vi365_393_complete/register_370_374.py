#!/usr/bin/env python3
"""Register VI finite resolutions, filtration, and the projective relation."""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT,dump,build_records
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def units(p,layer):return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(p)/f'{layer}.tex').read_text())]
def english(s):
    for a,b in [(r'\uline{pour}',r'\uline{for}'),(r'\uline{pour tout}',r'\uline{for every}'),(r'\uline{est isomorphe comme}',r'\uline{is isomorphic as a graded}'),(r'\uline{-Module gradué à un}',r'\uline{-Module to a graded}'),(r'\uline{-Module gradué de la forme}',r'\uline{-Module of the form}'),(r'\uline{où}',r'\uline{where}'),(r'\uline{est un}',r'\uline{is an}'),(r'\uline{-Module localement libre de type fini}',r'\uline{-Module locally free of finite type}'),(r'\text{avec }',r'\text{with }')]:s=s.replace(a,b)
    return s
def variant(p,index,sid,mode,suffix='01'):
    c,d=english(units(p,'current')[index]),english(units(p,'diplomatic')[index]);assert c!=d
    if mode=='math':c,d=c[2:-2],d[2:-2]
    return dict(id=f'EN-CONTRIB-VI-{p}-{suffix}',page=p,old=c,printed=d,source=sid,mode=mode)
variants=[dict(id='EN-CONTRIB-VI-371-01',page=371,old='it is clear that it is surjective.',printed='it is clear that it surjective.',source='check/findings/findings_371_375.json#1',mode='text'),
    variant(372,17,'ASTRA-VI-SYZYGY-372','math'),
    variant(372,28,'ASTRA-VI-ALGEBRA-RULE-372','display','02'),
    variant(373,10,'ASTRA-VI-TARGET-RULE-373','display'),
    variant(374,21,'ASTRA-VI-RECIPROCAL-374','math')]
pairs=json.loads((HERE/'lexical_math_pairs.json').read_text());pairs=[p for p in pairs if p['page'] not in [372,374]]
for layer in ['current','diplomatic']:
    f=units(372,layer)[28];e=english(f);assert f!=e
    pairs.append(dict(page=372,layer=layer,French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='The full three-property filtration display. Only the eight ruled lexical phrases are translated; graded moves within those phrases for English syntax. Every formula, variable, bound, quotient, rule and punctuation mark retains its source branch.'))
f=units(374,'current')[15];e=english(f);assert f!=e and f in units(374,'diplomatic')
pairs.append(dict(page=374,layer='both',French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='The explicit sheaf-to-class relation: avec becomes with. Plain class E and ruled sheaf E, all exponents and syntax remain literal.'))
dump(HERE/'lexical_math_pairs.json',pairs)
extra=[];dest=HERE/'attributed_source_audits';dest.mkdir(exist_ok=True)
rel='review/expose_vi/independent_syzygy_audit_372.json';raw=(ROOT/rel).read_bytes();(dest/'independent_syzygy_audit_372.json').write_bytes(raw)
extra.append(dict(record_type='attributed_source_audit_packet',page=372,source_id='ASTRA-VI-SYZYGY-372',source_packet=rel,contribution_copy='review/english/contributions/exposes_v_vi/attributed_source_audits/independent_syzygy_audit_372.json',packet_sha256=hashlib.sha256(raw).hexdigest(),decision='Exact coordinator-supplied independent text and mathematical audit. It proves the minimal final subscript repair through the kernel inclusion and a chain map, retaining the true earlier i≥r+1 sentence. It does not make a new source-image claim.'))
for p,paragraph,reason in [
    (369,False,'The369 index lambda-prime clause continues with370 and a sheaf, exactly as the recorded source boundary specifies.'),
    (370,True,'Lemma1.5.1 and its proof end on370;371 opens the separately labelled Lemma1.5.2.'),
    (371,False,'The371 final Consequently,if continues with372 M has a global partial resolution.'),
    (372,False,'The372 phrase a homogeneous basis continues with373 of L have degrees.'),
    (373,False,'The373 introductory exact-sequence colon continues with the complete displayed resolution on374.')]:
    f=(HERE/'source_packets'/str(p)/'current.tex').read_text();g=(HERE/'source_packets'/str(p+1)/'current.tex').read_text();e=(HERE/'translations'/f'{p}.tex').read_text();n=(HERE/'translations'/f'{p+1}.tex').read_text()
    assert e.endswith('\n\n')==paragraph,(p,repr(e[-30:]));assert not n.startswith('\n')
    extra.append(dict(record_type='manually_compared_source_folio_join',after=p,before=p+1,paragraph_break=paragraph,source_tail=f[-400:],source_head=g[:400],English_tail=e[-250:],English_head=n[:250],source_page_sha256s={str(p):sha(f),str(p+1):sha(g)},reason=reason))
author=HERE/'author_notes.tsv';lines=author.read_text().splitlines();lines=[l for l in lines if not l.startswith('374\t')]
lines.append('374\t*\tAfter the final K^bullet(S) and before its sentence stop\tComplete author text: This proof is due to J.P. Jouanolou.\tASTRA-VI-AUTHOR-NOTE-374')
author.write_text('\n'.join(lines)+'\n')
extra.append(dict(record_type='original_author_note_transfer',page=374,source_id='ASTRA-VI-AUTHOR-NOTE-374',label='*',helper=r'\SGAAuthorFootnote{*}',call_position='After the final K^bullet(S), before the full stop.',French_text='Cette démonstration est due à J.P. Jouanolou.',English_text='This proof is due to J.P. Jouanolou.',geometry='Baseline parenthesized star, as specified by the shared author-label helper and the completed source decision.',decision='Restore the original note and its call; remove the native body-level attribution paragraph and unprinted1.10–1.11 heading while retaining its stable target at the actual introductory sentence.'))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=370]
batches.append(dict(expose='VI',first=370,last=374,native_start=r'\sgaStableTarget{sga6.e06.cor.1-4}',native_end=r'\sgaStableTarget{sga6.e06.lem.1-10}',
    source='review/expose_vi/HANDOFF.md; reviewed French370–374 in both forms',
    reason='Restore the actual continuation of1.3 before Corollary1.4, both resolution lemmas and the full1.6–1.7 proofs, all1.8 computations, the exact1.9 relation and original Jouanolou author note. All nine native stable targets remain in their corresponding order.',variants=variants,
    notes=[
        dict(page=370,source_id='check/findings/findings_366_370.json#14;check/findings/findings_366_370.json#15;check/findings/findings_366_370.json#16;ASTRA-VI-GLYPHS-370;ASTRA-VI-WORD-RULES-370',English_rendering='full limit-proof conclusion, Corollary1.4 and Lemma1.5.1',decision='Restore the lambda-prime and lambda-double-prime stages, both primed u maps with their source and target, the finite-presentation flatness descent, and all clauses of the corollary. Keep the sheaf rules only before Lemma1.5.1; its ring-case A,B,M and all tilded letters remain plain. Restore its complete projectivity argument, all degree bounds, every localization, the Tor vanishing and the actual plain Bourbaki locator.'),
        dict(page=370,source_id='check/findings/findings_366_370.json#17',English_rendering='All the hypotheses are satisfied',decision='French singular vérifiée/current plural vérifiées has the same English participle satisfied. The identical list of1.3 hypotheses is retained without an artificial English agreement error.'),
        dict(page=371,source_id='ASTRA-VI-GLYPHS-371;ASTRA-VI-WORD-RULES-371;check/findings/findings_371_375.json#4;check/findings/findings_371_375.json#1',English_rendering='complete1.5.2 and1.6, followed by the graded-surjection construction',decision='Restore every hypothesis, residue-field expression, projective-dimension bound, resolution term and ruled lexical group. Preserve plain ring-case letters in1.5.2, with ruled sheaf letters beginning only in1.6. The L direct-sum construction and its semicolon are literal. The omitted copula is represented directly by it surjective in diplomatic and it is surjective currently; no other clause changes.'),
        dict(page=372,source_id='ASTRA-VI-SYZYGY-372',English_rendering='complete global syzygy construction and exact truncation',decision='Restore the full finite-generation and finite-presentation argument, S-flatness, and all steps omitted in native English. Branch only the final Z_(r+1)/Z_r instruction. The short exact kernel sequences give Ext^1(Z_r,N)=Ext^(r+2)(M,N)=0 from pd(M)≤r+1. The first differential is Z_r→L_r, and the original L_(r+1) map factors through Z_r; identities below it give the comparison chain map. The copied B=k[t], M=B/(t), r=0 example has Z0=(t) and Z1=0, proving the printed instruction fails for the stated exact tail. The earlier i≥r+1 clause stays unchanged.'),
        dict(page=372,source_id='ASTRA-VI-ALGEBRA-RULE-372;ASTRA-VI-WORD-RULES-372;ASTRA-VI-GLYPHS-372',English_rendering='full Proposition1.7 and its three filtration properties',decision='Restore the quotient defining gr^m, both separate B-Module clauses and every quantified word in the display. The first plain B versus ruled B is explicitly branched; the algebra comparison is id_B and the quotient action is b·[l]=[bl]. The remaining B letters keep their directly observed rules. The beginning of the proof retains its homogeneous-basis phrase across the next source marker.'),
        dict(page=373,source_id='ASTRA-VI-TARGET-RULE-373;ASTRA-VI-GLYPHS-373;ASTRA-VI-PARAGRAPH-NUMBER-373;check/findings/findings_371_375.json#7;check/findings/findings_371_375.json#8',English_rendering='complete induction and actual ordinary1.8 paragraph',decision='Restore the N=0 case, both canonical maps, the N>0 cokernel argument, all n0/n1 bounds and the precise direct summand. Keep the author’s M names in this proof; no silent L substitution is made. The second target M alone has a plain/ruled branch, identified by its degreewise multiplication map. Remove the native added Generation by the powers heading while retaining its target at the actual1.8 label. Restore the entire exact-sequence introduction.'),
        dict(page=374,source_id='ASTRA-VI-GLYPHS-374;check/findings/findings_371_375.json#9;check/findings/findings_371_375.json#10;check/findings/findings_371_375.json#11;ASTRA-VI-PARAGRAPH-NUMBER-374',English_rendering='all projective-image and class computations, then the complete dependence proof',decision='Restore the complete Proj resolution, the full filtration sum with no added terminal punctuation, the explicit pullback identification and both rows of the coefficient calculation. The source distinguishes ruled sheaf E from plain class E by E=cl(underlined E); retain that exact class map and f-star compatibility. Preserve the actual (-1)^(r+1−i) sign and factor order in1.9.1, the prior convolution display and the plain1.9 label. No comma is added after K^bullet(S).'),
        dict(page=374,source_id='ASTRA-VI-RECIPROCAL-374;ASTRA-VI-AUTHOR-NOTE-374',English_rendering='paired formal inverse and full original author note',decision='The denominator is grouped only currently. The pre-lambda addition law gives lambda_t(−xi)lambda_t(xi)=1, and the unique inverse of1+xi t is its formal geometric series. For P0 over a field with xi=1, the ungrouped source expression fails that product identity. Preserve the source slash form diplomatically. Restore the baseline-star note at the exact final call position with J.P. initials, separately from editorial apparatus.'),
        dict(page=374,source_id='review/expose_vi/page_status.jsonl#pages370-374',English_rendering='five complete source pages, nine native targets and one original note',decision='All prose, formula placement, reference locators, local underlines and author-note contents have been compared with both reviewed French forms. Five source joins are explicit. This English transfer does not claim a new full-page image review or PDF rendering.')
    ],extra_records=extra))
dump(HERE/'batches.json',batches);build_records()
