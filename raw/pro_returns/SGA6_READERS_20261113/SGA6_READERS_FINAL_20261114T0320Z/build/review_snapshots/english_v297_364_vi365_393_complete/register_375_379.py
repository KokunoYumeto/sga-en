#!/usr/bin/env python3
"""Register the full independence proof and the two following remarks."""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT,dump,build_records
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def units(p,layer):return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(p)/f'{layer}.tex').read_text())]
def english(s):
    return s.replace(r'\uline{sont localement libres de type fini sur}',r'\uline{are locally free of finite type on}').replace(r'\text{ sont localement libres de type fini.}',r'\text{ are locally free of finite type.}').replace(r'\text{pour tout }',r'\text{for every }')
def variant(p,index,sid,mode,suffix='01'):
    c,d=english(units(p,'current')[index]),english(units(p,'diplomatic')[index]);assert c!=d
    if mode=='math':c,d=c[2:-2],d[2:-2]
    return dict(id=f'EN-CONTRIB-VI-{p}-{suffix}',page=p,old=c,printed=d,source=sid,mode=mode)
variants=[variant(375,21,'check/findings/findings_371_375.json#12','display'),
    variant(376,0,'check/findings/findings_376_380.json#1','display'),
    dict(id='EN-CONTRIB-VI-376-02',page=376,old='By 1.3, for sufficiently large',printed='By 1.2, for sufficiently large',source='ASTRA-VI-REFERENCE-376',mode='text'),
    variant(377,21,'check/findings/findings_376_380.json#13','display'),
    variant(378,0,'check/findings/findings_376_380.json#15','display'),
    variant(379,7,'check/findings/findings_376_380.json#21','math'),
    variant(379,26,'ASTRA-VI-PROJECTIVE-P-379','math','02')]
pairs=json.loads((HERE/'lexical_math_pairs.json').read_text());pairs=[p for p in pairs if p['page'] not in [375,376,377]]
for p,index in [(375,6),(376,3)]:
    f=units(p,'current')[index];e=english(f);assert f!=e and f in units(p,'diplomatic')
    pairs.append(dict(page=p,layer='both',French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='Translate only the local-freeness words in this complete display. Preserve the actual presence or absence of word underlines, all five sheaves where present, and every mathematical token and punctuation mark.'))
for layer in ['current','diplomatic']:
    f=units(377,layer)[21];e=english(f);assert f!=e
    pairs.append(dict(page=377,layer=layer,French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='In the complete Koszul relation, pour tout becomes for every. The rho/p subscript and every other token remain literal in the respective branch.'))
dump(HERE/'lexical_math_pairs.json',pairs)
extra=[]
for p,paragraph,reason in [
    (374,True,'The final independence introduction and its author note end on374;375 begins the separately labelled Lemma1.10.'),
    (375,False,'The375 final colon introduces the complete direct-image free-group equality at the top of376.'),
    (376,True,'The377 opening Or begins at the same indented position as the following Par ailleurs paragraph, separately verified in the saved primary image p377.png.'),
    (377,True,'The377 statement of the induction task ends with its parenthetical sentence;378 begins the separate calculation By1.11.3.'),
    (378,False,'Remark1.12 ends378 with a colon and continues with equation1.12.1 on379.')]:
    f=(HERE/'source_packets'/str(p)/'current.tex').read_text();g=(HERE/'source_packets'/str(p+1)/'current.tex').read_text();e=(HERE/'translations'/f'{p}.tex').read_text();n=(HERE/'translations'/f'{p+1}.tex').read_text()
    assert e.endswith('\n\n')==paragraph,(p,repr(e[-30:]));assert not n.startswith('\n')
    extra.append(dict(record_type='manually_compared_source_folio_join',after=p,before=p+1,paragraph_break=paragraph,source_tail=f[-400:],source_head=g[:400],English_tail=e[-250:],English_head=n[:250],source_page_sha256s={str(p):sha(f),str(p+1):sha(g)},reason=reason))
extra.append(dict(record_type='regional_source_paragraph_verification',page=377,source_id='EN-VI-JOIN-376-377',image='review/expose_vi/images/p377.png',region='First line Or and comparison with the next indented Par ailleurs line',observation='The opening Or is indented from the body margin and aligns with the following paragraph opener. Preserve a paragraph boundary after376.',limitation='Only paragraph placement was checked regionally here; no new full-page mathematical collation or English PDF inspection is claimed.'))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=375]
batches.append(dict(expose='VI',first=375,last=379,native_start=r'\sgaStableTarget{sga6.e06.lem.1-10}',native_end='\\[\n  x^{r+1}=0.\n\\]',
    source='review/expose_vi/HANDOFF.md; reviewed French375–379 in both forms',
    reason='Restore Lemma1.10 and its complete free-group proof, the entire1.11 argument including the Koszul complex and differential, both finite-sum calculations and descending induction, then all source definitions and formulas in Remarks1.12–1.13. Seven native stable targets remain in their original order.',variants=variants,
    notes=[
        dict(page=375,source_id='ASTRA-VI-GLYPHS-375;ASTRA-VI-WORD-RULES-375;check/findings/findings_371_375.json#12',English_rendering='complete lemma and free abelian groups A,B,A-prime',decision='Restore the full class equality with its subscript, both lemma conclusions, all exact sequences and integer coefficients, the twist automorphism and the direct-image generator map. The plain free-group names remain distinct in typography from the ruled sheaf generators. The missing n_i in the twisted equality has a complete display branch: T_n sends each generator H to H tensor O_X(n), has inverse T_(-n), and preserves every integer coefficient by Z-linearity.'),
        dict(page=376,source_id='check/findings/findings_376_380.json#1;ASTRA-VI-REFERENCE-376;ASTRA-VI-GLYPHS-376;ASTRA-VI-PARAGRAPH-NUMBER-376',English_rendering='complete direct-image calculation and the initial1.11 construction',decision='Restore all five local-freeness terms, every quantified vanishing condition, exact sequence, free-group relation and the two explicit F/F-prime direct sums. The first generator parenthesis is separately branched under the map (H)→(f_*H). The reference1.2/1.3 is also explicit: substitute the finite family L_i,M_i,N_i,F,G into1.3 and take the maximum twist bound; the long exact sequence gives the stated direct-image exactness. Keep the ordinary1.11 label and actual j-indexed formula rather than the native i substitution.'),
        dict(page=377,source_id='check/findings/findings_376_380.json#8;check/findings/findings_376_380.json#9;check/findings/findings_376_380.json#11;check/findings/findings_376_380.json#12;check/findings/findings_376_380.json#13;check/findings/findings_376_380.json#14;ASTRA-VI-GLYPHS-377',English_rendering='complete direct-image projection calculation and Koszul complex',decision='Restore the two unindexed direct sums, the full complex, its unindexed differential sum and all seven low ellipses, without inserting a terminal stop after the differential. Every wedge, hat and tensor factor is literal. Restore the grading explanation, local polynomial-algebra identification and regular sequence proof. The sigma subscript rho−i/p−i has an explicit branch: the degree-p term is wedge^i(E) tensor Sym^(p−i)(E), giving exactly the corrected alternating class sum. The plain class E inside lambda remains separate from ruled sheaf E.'),
        dict(page=378,source_id='check/findings/findings_376_380.json#15;ASTRA-VI-GLYPHS-378',English_rendering='all finite-sum steps of the descending induction',decision='Restore the first zero equation, p(j) hypotheses and substitution, the interchange of finite sums, each vanishing argument and the reduction by the invertible top exterior class. The first equation is unlabelled diplomatically and carries1.11.4 currently; substituting p(j)=n0+r+j and removing the vanishing terms identifies it with both subsequent references. Preserve the actual product stop and all n0 bounds. Restore the explicit n=−r calculation, sigma0=1, the descending j argument and the complete opening definition of sigma_t in Remark1.12.'),
        dict(page=379,source_id='check/findings/findings_376_380.json#21;ASTRA-VI-GLYPHS-379;ASTRA-VI-PROJECTIVE-P-379',English_rendering='complete symmetric-power identity and hyperplane-class remarks',decision='Restore the printed1.12.1 label and colon, the entire shifted-power discussion, both exact sequences including the dual one, the gamma vanishing and gamma relation1.13.1, and the x-prime paragraph omitted by native English. The basis endpoint branches k+r+1/k+r: multiplication by xi^k with inverse multiplication by xi^(−k) sends the proved basis exactly to the corrected list; at r=0 the printed list(1,1) has kernel vector(1,−1). All checked sheaves retain their letter rules with checks outside, while checked class E/F stay plain. The final projective-P occurrence is independently branched through the recorded identity on the quotient functor.'),
        dict(page=379,source_id='check/findings/findings_376_380.json#20;check/findings/findings_376_380.json#22',English_rendering='homomorphism; linearly independent',decision='French homomorpnisme/homomorphisme and the missing plural s in indépendant have unchanged English renderings. The same symmetric-power homomorphism and the same shifted basis vectors are retained; no artificial English spelling or agreement error is introduced.'),
        dict(page=379,source_id='review/expose_vi/page_status.jsonl#pages375-379',English_rendering='five complete source pages and seven native stable targets',decision='Every prose clause, original formula and its placement, local underline and source alternative has been manually compared with the two reviewed French forms. All five joins are explicit. The377 first-line paragraph indentation was regionally checked in the saved primary image; other image evidence remains attributed to the coordinator. These pages contain no original author note and no new English PDF inspection is claimed.')
    ],extra_records=extra))
dump(HERE/'batches.json',batches);build_records()
