#!/usr/bin/env python3
"""Register the complete arbitrary graded-Module construction and its derived functor."""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT,dump,build_records
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def units(p,layer):return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(p)/f'{layer}.tex').read_text())]
def variant(p,index,sid,mode,suffix='01',related=()):
    c,d=units(p,'current')[index],units(p,'diplomatic')[index];assert c!=d
    if mode=='math':
        assert (c.startswith(r'\(') and d.startswith(r'\(')) or (c.startswith('$') and d.startswith('$'))
        c,d=(c[2:-2],d[2:-2]) if c.startswith(r'\(') else (c[1:-1],d[1:-1])
    result=dict(id=f'EN-CONTRIB-VI-{p}-{suffix}',page=p,old=c,printed=d,source=sid,mode=mode)
    if related:result['related_sources']=list(related)
    return result
variants=[
    variant(380,9,'ASTRA-VI-PROJECTIVE-P-380','math'),
    variant(382,1,'ASTRA-VI-ADJOINT-TARGET-382','display'),
    variant(382,39,'check/findings/findings_381_385.json#14','math','02'),
    variant(383,3,'check/findings/findings_381_385.json#17','display',related=['ASTRA-VI-ALGEBRA-RULES-383']),
    variant(384,5,'ASTRA-VI-FUNCTOR-ARG-RULE-384','display'),
    variant(384,8,'ASTRA-VI-DERIVED-R-384','display','02'),
    variant(384,17,'ASTRA-VI-MAP-ARG-RULE-384','math','03')]
extra=[]
for p,paragraph,reason in [
    (379,False,'The final379 colon introduces equation1.13.2 at the top of380.'),
    (380,True,'The final notation sentence ends380;381 opens the separately numbered2.3 paragraph.'),
    (381,False,'The final381 colon introduces the adjunction-source isomorphism at the top of382.'),
    (382,False,'The final382 colon introduces the gluing triangle at the top of383.'),
    (383,False,'The final383 words the functor continue with Projz at the top of384.')]:
    f=(HERE/'source_packets'/str(p)/'current.tex').read_text();g=(HERE/'source_packets'/str(p+1)/'current.tex').read_text();e=(HERE/'translations'/f'{p}.tex').read_text();n=(HERE/'translations'/f'{p+1}.tex').read_text()
    assert e.endswith('\n\n')==paragraph,(p,repr(e[-30:]));assert not n.startswith('\n')
    extra.append(dict(record_type='manually_compared_source_folio_join',after=p,before=p+1,paragraph_break=paragraph,source_tail=f[-400:],source_head=g[:400],English_tail=e[-250:],English_head=n[:250],source_page_sha256s={str(p):sha(f),str(p+1):sha(g)},reason=reason))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=380]
batches.append(dict(expose='VI',first=380,last=384,native_start='\\[\n  x^{r+1}=0.\n\\]',native_end=r'\sgaStableTarget{sga6.e06.eq.2-5-2}',
    source='review/expose_vi/HANDOFF.md; reviewed French380–384 in both forms',
    reason='Restore the complete labelled Remark1.14, Theorem2.1, the three abelian-category definitions, every paragraph of the arbitrary graded-Module construction and gluing proof, the full acyclicity argument and the beginning of the beta construction. All fourteen native stable targets remain in their original order. The native condensed beta paragraph is consumed up to its derived-map anchor; the source construction continues on385.',variants=variants,
    notes=[
        dict(page=380,source_id='ASTRA-VI-GLYPHS-380;ASTRA-VI-WORD-RULES-380;ASTRA-VI-PROJECTIVE-P-380;check/findings/findings_376_380.json#25;check/findings/findings_376_380.json#26;check/findings/findings_376_380.json#27',English_rendering='complete Remark1.14, Theorem2.1 and2.2 notation',decision='Restore the actual Remark1.14 label and its reference[3], the separate non-use paragraph, the theorem word rules, the inline basis, and all three abelian-category assertions. The categories remain mathcal C,C0,C-prime rather than the native G substitutions. The twist is defined in prose with the exact source inline complex, without adding the native equality or a display. The projective-P occurrence has an explicit diplomatic/current branch under the recorded identity on the quotient functor. Ordinary paragraph labels are preserved without invented headings.'),
        dict(page=381,source_id='check/findings/findings_381_385.json#1;check/findings/findings_381_385.json#2;check/findings/findings_381_385.json#3;check/findings/findings_381_385.json#4;check/findings/findings_381_385.json#5;ASTRA-VI-GLYPHS-381',English_rendering='full affine inverse-image construction',decision='Retain the headed first isomorphism and the exact absent comma and full stop in2.3.1.1 and2.3.1.2, every adjunction category, the tensor formula, and the separate flatness and quasi-coherence paragraphs. French fibre is rendered stalk in these two local sheaf checks. On an affine chart S=Spec R with A associated to an R-algebra B, Y=Spec B, y corresponding to q and s to p, the displayed sheaf homomorphism at y is B tensor_R R_p→B_q, the localization map. For a B-module N the corresponding map (N tensor_R R_p) tensor_(B tensor_R R_p) B_q→N_q sends n tensor b/u to bn/u; its inverse sends n/u to n tensor1/u. This is the exact localization identification used by the author, with no change to the mathematical units.'),
        dict(page=382,source_id='ASTRA-VI-ADJOINT-TARGET-382;check/findings/findings_381_385.json#7;check/findings/findings_381_385.json#10;check/findings/findings_381_385.json#11;check/findings/findings_381_385.json#12;check/findings/findings_381_385.json#13;check/findings/findings_381_385.json#14;ASTRA-VI-GLYPHS-382',English_rendering='adjunction map and every graded localization/gluing definition',decision='The target of the adjunction map is explicitly branched without/with tilde: under Hom_Y(barf-star M,tilde M)=Hom_(S,A)(M,barf_* tilde M), the displayed M→barf_* tilde M maps to the corrected adjoint. Retain every baseline restriction bar, degree-zero subscript, the headless affine-chart isomorphism, the plain geometric Proj and ruled functor Projz. Keep the comma at the end of the local Projz definition and its continuous following prose. The printed degree e>o has an explicit e>0 branch using the exact parameter replacement (s,d)→(t,e) in the already stated positive-degree chart construction.'),
        dict(page=383,source_id='check/findings/findings_381_385.json#15;check/findings/findings_381_385.json#16;check/findings/findings_381_385.json#17;ASTRA-VI-ALGEBRA-RULES-383;check/findings/findings_381_385.json#18;check/findings/findings_381_385.json#19;check/findings/findings_381_385.json#20;check/findings/findings_381_385.json#21;check/findings/findings_381_385.json#22;check/findings/findings_381_385.json#23;check/findings/findings_381_385.json#24;ASTRA-VI-GLYPHS-383',English_rendering='complete gluing triangle and three comparison displays',decision='Restore the centered three-column triangle with the open-immersion hook and retain the two Modules inline. One full-display branch preserves the two plain B glyphs and the inner i-inverse-image subscript diplomatically. The corrected comparison follows f_(U,st)=f_(U,s) composed with i, hence i-inverse-image composed with f_(U,s)-inverse-image=f_(U,st)-inverse-image; on stalks the identification is the identity on M_(f(y)). The two ruled B substitutions identify each localized algebra element b/s^m with itself and preserve multiplication and the tensor structure. Every remaining restriction, localization fraction and punctuation token remains literal. Restore the separate quasi-coherence paragraph and the full derived-category conclusion.'),
        dict(page=384,source_id='ASTRA-VI-FUNCTOR-ARG-RULE-384;ASTRA-VI-DERIVED-R-384;ASTRA-VI-MAP-ARG-RULE-384;check/findings/findings_381_385.json#25;check/findings/findings_381_385.json#26;check/findings/findings_381_385.json#27;check/findings/findings_381_385.json#28;ASTRA-VI-GLYPHS-384',English_rendering='tensor compatibility, F_k, derived F_k and the start of beta',decision='Preserve the continuation of the383 sentence, the source quantifier order k then L, the enough-injectives justification, the entire acyclicity argument through the composite-functor spectral sequence, and all local formulas defining beta. Each of the two observed plain L arguments has its own branch; the identity on the same Module and on each twist identifies the arguments. The literal two lower rules on derived R remain diplomatic and the reviewed mathbb R is current: both apply F_k to the same injective resolution L→I, with the identity chain map. Keep ordinary2.4/2.5 labels and restore the source formulas omitted by native English. The construction continues across384/385.'),
        dict(page=384,source_id='review/expose_vi/page_status.jsonl#pages380-384',English_rendering='five complete source pages and fourteen native stable targets',decision='All prose, formula placement, local underline groups, punctuation and seven source alternatives were manually compared with both reviewed French forms. The five joins are explicit. Source image evidence remains attributed to the coordinator; there is no new full-page scan claim or English PDF inspection. These pages contain no original author note.')
    ],extra_records=extra))
dump(HERE/'batches.json',batches);build_records()
