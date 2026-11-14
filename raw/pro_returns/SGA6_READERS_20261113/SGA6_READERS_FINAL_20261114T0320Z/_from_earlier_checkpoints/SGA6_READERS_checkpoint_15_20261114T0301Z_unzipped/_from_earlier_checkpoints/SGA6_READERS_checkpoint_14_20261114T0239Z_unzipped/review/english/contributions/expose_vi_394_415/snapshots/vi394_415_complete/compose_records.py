#!/usr/bin/env python3
"""Compose this isolated VI transfer; never writes shared or frozen records."""
from pathlib import Path
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE))
import contribution as c

def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def dump(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def decision(sid): return c.source_decision(sid)
def chk(block,n): return f'check/findings/findings_{block}.json#{n}'

pairs=json.loads((HERE/'lexical_math_pairs.json').read_text())
diffs=json.loads((HERE/'source_differences.json').read_text())
texts={p:(HERE/'translations'/f'{p}.tex').read_text() for p in range(394,416)}
units={p:json.loads((HERE/'source_packets'/str(p)/'units.json').read_text()) for p in texts}
def lexical(s,p,layer):
    for pair in pairs:
        if pair['page']==p and pair['layer'] in (layer,'both') and pair['French_literal_unit']==s:
            return pair['English_literal_unit']
    return s
def expand(s,p): return re.sub(r'@@M(\d+)@@',lambda m:lexical(units[p][int(m[1])],p,'current'),s)
page_texts={p:expand(t,p) for p,t in texts.items()}

fonts={
394:'ASTRA-VI-FLAG-OPERATORS-394',395:'ASTRA-VI-FLAG-OPERATORS-395',
396:'ASTRA-VI-DOUBLE-OPERATORS-396',397:'ASTRA-VI-DOUBLE-OPERATORS-397',
398:'ASTRA-VI-DOUBLE-OPERATORS-398',399:'ASTRA-VI-DOUBLE-OPERATORS-399',
400:'ASTRA-VI-DOUBLE-OPERATORS-400',401:'ASTRA-VI-DOUBLE-OPERATORS-401',
404:'ASTRA-VI-DOUBLE-OPERATORS-404'}
math_sources={
(395,31):'ASTRA-VI-BLOCK-SYMMETRIC-CONSTANTS-395',
(397,16):'ASTRA-VI-FLAG-LAST-INDEX-397',
(402,22):chk('401_405',9),
(403,6):'ASTRA-VI-GAMMA-SUBSTITUTION-403',
(406,0):chk('406_410',1),(406,1):chk('406_410',2),
(407,1):chk('406_410',8),
(411,12):'ASTRA-VI-TOTAL-COHOMOLOGY-411',
(412,20):chk('411_415',12),
(414,29):chk('411_415',22),
(415,0):'ASTRA-VI-BASIS-PRODUCT-415'}
repeated={
(394,20):'-scheme @@M20@@',(394,46):r'\uline{on} @@M46@@',
(397,24):'we then consider @@M24@@',(397,25):'and on @@M25@@',
(397,28):'structural morphism of @@M28@@',(397,30):'usual flag bundle @@M30@@',
(397,31):'over @@M31@@',(397,34):'factors through @@M34@@',
(397,35):'induction hypothesis applied to @@M35@@',
(397,37):'has as a basis over @@M37@@',(397,39):'moreover, @@M39@@',
(398,12):'usual flag bundle @@M12@@',(398,15):'It follows that @@M15@@',
(398,20):'on @@M20@@',(398,22):'is a subring of @@M22@@',
(398,27):'-algebra of @@M27@@',(398,30):'there is in @@M30@@',
(399,32):'denote by @@M32@@',(399,37):'the @@M37@@ form an inductive system',
(400,8):'their class in @@M8@@',(400,16):'By 4.8, @@M16@@',
(412,20):r'\uline{is a basis of} @@M20@@'}
variants=[];math_coverage=[]
def add(p,old,printed,sid,mode='text',related=None,**meta):
    assert old!=printed,(p,sid,'identical variant')
    assert page_texts[p].count(old)==1,(p,sid,'anchor count',page_texts[p].count(old),old)
    rec=dict(page=p,old=old,printed=printed,mode=mode,source=sid,**meta)
    if related:rec['related_sources']=related
    variants.append(rec)
    return rec

for row in diffs:
    p=row['page']
    for d in row['math_differences']:
        i=d['index'];token=f'@@M{i}@@'
        a=repeated.get((p,i),token)
        assert texts[p].count(a)==1,(p,i,a)
        old=expand(a,p);cur=lexical(d['current'],p,'current');dip=lexical(d['printed'],p,'diplomatic')
        assert old.count(cur)==1,(p,i,'unit count')
        printed=old.replace(cur,dip,1)
        sid=math_sources.get((p,i),fonts.get(p));related=[]
        if (p,i)==(394,24):related=['ASTRA-VI-PROJECTIVE-P-394']
        if p==397 and i in [24,25,26,28,31,34,37,39]:sid='ASTRA-VI-PROJECTIVE-OPERATORS-397'
        if (p,i)==(397,32):related=['ASTRA-VI-PROJECTIVE-OPERATORS-397']
        if (p,i)==(402,22):
            old='i.e. '+cur;printed='i.e.. '+dip;related=[chk('401_405',8)]
        if (p,i)==(414,29):
            old=cur+'-Modules';printed=dip+',-Modules'
        if (p,i)==(406,0):related=[chk('401_405',37)]
        if (p,i)==(406,1):related=[chk('401_405',38)]
        mode='display' if cur.startswith(('\\[','\\begin{')) else 'text'
        v=add(p,old,printed,sid,mode,related,math_unit_index=i,
              difference_scope='complete source mathematical unit; only the recorded source difference and individually approved internal lexical text are transported')
        math_coverage.append(dict(page=p,index=i,French_current=d['current'],French_printed=d['printed'],English_current=cur,English_printed=dip,source=sid))

add(395,r'\uline{isobaric relations deduced from the relation}:',r'\uline{isobaric relations deduced from the relation}::',chk('391_395',39))
add(396,r'\uline{being assigned weight}',r'\uline{being effected with weight}',chk('396_400',1),
    translation_alignment='The two French verbs effectués/affectés are rendered effected/assigned, preserving the observed lexical error rather than manufacturing an English spelling defect. The source weight assignment itself is unchanged.')
add(397,r'\uline{-Module locally free of rank}',r'\uline{-Module locally of rank}',chk('396_400',7))
add(397,r'(\uline{notation of} 4.5)',r'(\uline{notation of} 3.5)','ASTRA-VI-FLAG-NOTATION-REFERENCE-397')
add(397,'and Corollary 4.4','and Corollary 3.4','ASTRA-VI-FLAG-BASIS-REFERENCE-397')
add(398,'(notation of 4.5 and 4.7)','(notation of 3.5 and 3.7)','ASTRA-VI-FLAG-SPLITTING-REFERENCES-398')
add(400,r'\uline{there is an isomorphism}:',r'\uline{there is an isomorphism}.:',chk('396_400',21))
add(403,r'\uline{With the notation and hypotheses of} 5.1',r'\uline{With the notation and hypotheses of} 4.1',chk('401_405',22))
add(406,'by (5.2.3).','by (4.2.3).',chk('406_410',3),related=[chk('401_405',39)])
add(409,'The standard argument then reduces us to the case','The standard argument then reduces. us to the case','ASTRA-VI-STRAY-STOP-409',
    translation_alignment='The isolated printed stop after the finite verb permet is transported after the finite English verb reduces. English word order places then before that verb in both forms; the author clause otherwise remains intact.')
add(411,r'\uline{The filtration} 6.5',r'\uline{The filtration} 5.5',chk('411_415',5))
add(415,'Lecture Notes in Mathematics','Lectures notes in Mathematics',chk('411_415',30))

# Sort by the actual occurrence, and prove all apparatus anchors are disjoint.
variants.sort(key=lambda v:(v['page'],page_texts[v['page']].index(v['old'])))
for n,v in enumerate(variants,1):v['id']=f'EN-CONTRIB-VI394-{n:03}'
for p,t in page_texts.items():
    intervals=sorted((t.index(v['old']),t.index(v['old'])+len(v['old']),v['id']) for v in variants if v['page']==p)
    for a,b in zip(intervals,intervals[1:]):assert a[1]<=b[0],(p,'overlapping apparatus anchors',a,b)
    for v in (v for v in variants if v['page']==p):
        for sid in [v['source']]+v.get('related_sources',[]):assert decision(sid)['page']==p,(sid,p)
for r in math_coverage:
    r['English_variant']=next(v['id'] for v in variants if v['page']==r['page'] and v.get('math_unit_index')==r['index'])
dump('math_variant_coverage.json',math_coverage)

prose_sources={
394:[chk('391_395',21),chk('391_395',27)],395:[chk('391_395',39)],
396:[chk('396_400',1)]*2,
397:[chk('396_400',7),'ASTRA-VI-FLAG-NOTATION-REFERENCE-397','ASTRA-VI-FLAG-BASIS-REFERENCE-397'],
398:['ASTRA-VI-FLAG-SPLITTING-REFERENCES-398']*2,
399:[chk('396_400',15)]*2+[chk('396_400',16)],400:[chk('396_400',21)],
402:[chk('401_405',8)],403:[chk('401_405',22)],406:[chk('406_410',3)],
408:[chk('406_410',13),chk('406_410',14)],
409:['ASTRA-VI-STRAY-STOP-409',chk('406_410',17)],411:[chk('411_415',5)],
412:[chk('411_415',14)],414:[chk('411_415',22)],415:[chk('411_415',30)]*2}
prose_coverage=[]
for d in diffs:
    source_ids=prose_sources.get(d['page'],[])
    assert len(source_ids)==len(d['prose_differences']),(d['page'],'unattributed prose difference')
    for delta,sid in zip(d['prose_differences'],source_ids):
        mapped=[v['id'] for v in variants if sid in [v['source']]+v.get('related_sources',[])]
        prose_coverage.append(dict(page=d['page'],source_id=sid,**delta,English_variants=mapped,
            disposition='source difference explicitly carried by the listed English variant' if mapped else 'unchanged English rendering; exact French spelling/agreement disposition in transfer.jsonl'))
dump('prose_difference_coverage.json',prose_coverage)

notes=[]
same=[
(394,chk('391_395',21),'réprésentable / représentable','representable','French accent correction; the English lexical reading is unchanged.'),
(394,chk('391_395',27),'grassmanienne / grassmannienne','Grassmannian','French spelling correction; both French forms denote the same represented rank-r quotient functor and use the same English name.'),
(399,chk('396_400',15),"c'est homomorphisme / cet homomorphisme",'this homomorphism','French demonstrative/homophone correction. The homomorphism sends the specified lambda generators to the specified sheaf classes in both readings; English this homomorphism retains that exact map.'),
(399,chk('396_400',16),'grassmanienne / grassmannienne','Grassmannian','French spelling correction; the English name and every quotient-functor formula are unchanged.'),
(408,chk('406_410',13),'permet / permettent','reduce','French agreement with two coordinated subjects. English reduce already agrees with those same two subjects; no English singular verb is invented.'),
(408,chk('406_410',14),"d’éxistence / d’existence",'existence','French accent correction; English existence has the same meaning in both forms.'),
(409,chk('406_410',17),"c’êst-à-dire / c’est-à-dire",'that is','French accent correction; both English forms use that is.'),
(412,chk('411_415',14),'fans la famille / dans la famille','in the family','French one-letter typing error in the preposition. The indexed family is unchanged; English in the family introduces no invented English typo.')]
for p,sid,fr,en,reason in same:
    d=decision(sid)
    notes.append(dict(page=p,source_id=sid,French_readings=fr,English_both=en,decision='same English rendering; no reader variant',reason=reason,source_record=d))

restorations=[
(394,395,'Full flag-functor quotient data and Lemma 4.3 tuple restored','Retains every rank condition, quotient, alpha(j) tuple, symmetric-function relation and complete basis display from the reviewed French, including the separately adjudicated constant terms.'),
(397,397,'Inductive basis indices restored','The final basis monomial uses xi_(n−1) with exponent alpha_(n−1), as in the exact French unit. The native English xi_n variant is replaced; the source unit is retained literally in both branches.'),
(398,400,'Full general flag-bundle proof and transition-system construction restored','Restores the successive flag constructions, the common A/B module basis, the two lambda-algebra homomorphisms, all reference locators, and the quotient-by-last-factor transition morphism. The precise formulas and their paragraph positions are retained.'),
(401,403,'Complete definitions and pushforward computation in 5.1–5.3 restored','Restores x=1−xi^{-1}, x′=xi−1=xi x, the associated graded classes and Fil2 comparison; the negative-power basis in (5.2.1); all three equations (5.2.1–3); the sigma_n recurrence; and the complete gamma-substitution/quotient-lambda-algebra/induction proof. Each expression occupies its source paragraph rather than the native shortened argument.'),
(404,405,'Full Corollaries 5.5–5.8 and Proposition 5.9 restored','Retains all S/E_i hypotheses, the dual Chern relation, the cbar_i^j classes and total Chern formula, the k−r filtration target, and the i≥1 individual lambda^i(F) vanishing statement. Restores the coefficientwise bar-f_* definition and projection-formula argument.'),
(406,407,'Complete Proposition 5.10 computation restored','Restores the c_i dependence equation, the x′ expressions and all aligned gamma computations. Proposition 5.11 retains the exact c^r(F), c^{r+1}(E) and bar-x′ formulas.'),
(408,409,'Nilpotence proofs restored without compression','Restores the rank-clopen reduction, tensorized surjection, lambda^m equation, nilpotence calculation and all finitely generated lambda-ring steps. The source heading is Corollary 6.2; the native stable target prop.6-2 is preserved as an identifier. The module-finite assertion remains over R intersect H^0, with its explicit weight bound.'),
(410,410,'Exact coefficient ring and augmentation maps restored','The particular invertibility assertion uses Q as printed/reviewed, with Id_A and the exact augmentation homomorphisms preserved. The complete proof by the projection formula remains.'),
(411,412,'Complete support-defined filtration and proof restored','Restores the quantified closed subset Y, total-cohomology support, subscript filtration K_i, additive subgroup proof and tensor-support/codimension argument. The source all-degree current correction has its own explicit variant and proof packet; no additional author hypothesis is inserted.'),
(412,413,'Complete Lemmas 6.7–6.8 restored','Retains the closed-specialization choices, distinct maximal ideals, Chinese-remainder lifting, Nakayama isomorphisms, open-locus argument, and full twisting/extension construction. The unchanged for-every-p wording and its source scope audit remain separate.'),
(413,414,'Serre attribution and three-term complex restored','Restores the parenthetical attribution to J.P. Serre. The author proof includes the full three-term complex, all maps, support statement, finite-open decomposition and flag-pullback argument.'),
(415,415,'Basis product, problem and bibliography restored','Restores the explicit r-factor product in the current form, with printed r+1 factors in the diplomatic variant. Problem 6.10 retains the source inclusion Fil^k subset K_k, not the native equality. Bibliographic author order, titles, series and journal wording follow the source; only thesis (in preparation) is translated. Both continuation definition blocks remain at this boundary.')]
extra=[dict(record_type='native_English_restoration',first_page=a,last_page=b,title=title,reason=reason,source_reference='review/expose_vi/HANDOFF.md',status='complete prose and formula-placement comparison against the saved reviewed French pages; attributed source-image coverage') for a,b,title,reason in restorations]
extra.extend(dict(record_type='prose_difference_disposition',**r) for r in prose_coverage)
extra.append(dict(record_type='terminology_transport',pages=[408,410],French='nilidéal',English='nil ideal',
    reason='Matches the already selected English VII454 wording. The source ideal I is transported by the identity I→I, a↦a; the proof on408 gives nilpotence for each element E−epsilon(E), and the claim remains exactly the same elementwise nilpotence assertion. The separate nilpotent-ideal assertion in409 is preserved in its own sentence.'))

joins={
394:('colon to display','The canonical S-isomorphism statement ends in a colon; its display begins395.'),
395:('display to continuing item','The last display is followed by the parenthetical weight assignment within the same second item.'),
396:('new explanatory paragraph','After the theorem display,397 starts In other words as the source does.'),
397:('colon to display','The basis assertion ends in a colon; its display begins398.'),
398:('same sentence','The source compte / tenu is transferred as taking / into account; no blank line is inserted.'),
399:('same sentence','The source comme / quotient is transferred as as the / quotient; no blank line is inserted.'),
400:('colon to display','The last paragraph ends We may therefore write; the displayed quotient begins401.'),
401:('display to same paragraph','The canonical exact sequence continues with where f is the structural morphism on402.'),
402:('colon to display','The pushforward computation ends in a colon; its display begins403.'),
403:('new corollary','The proof ends before the new Corollary5.4 on404.'),
404:('display to statement continuation','The total Chern relation continues with where c is the total Chern class on405.'),
405:('colon to display','The coefficientwise projection-formula consequence ends in a colon; the display starts406.'),
406:('display to continuing proof','The dependence equations continue with Thus and its display on407.'),
407:('same sentence','We denote by / epsilon the augmentation homomorphism spans the boundary with no blank line.'),
408:('new corollary','Proposition6.1 concludes before Corollary6.2 on409.'),
409:('new corollary','Corollary6.2 proof concludes before Corollary6.3 on410.'),
410:('colon to display','The composite homomorphism starts as a display on411.'),
411:('continuing proof','The support containment appears at the start of412, followed by the next argument paragraph.'),
412:('same statement sentence','Then there is an / integer n continues Lemma6.8; the lexical rule groups are separately retained without a blank line.'),
413:('display to same sentence','The morphisms are followed by that are isomorphisms on414, preserving the proof sentence.'),
414:('colon to display','The basis element product is displayed at the start of415.')}
join_records=[]
for left,(kind,reason) in joins.items():
    lt=texts[left];rt=texts[left+1]
    row=dict(left_page=left,right_page=left+1,kind=kind,reason=reason,
             left_translation_tail=lt[-240:],right_translation_head=rt[:240],
             left_translation_sha256=sha(lt),right_translation_sha256=sha(rt),
             builder_join="''.join(page_segments)",added_separator_bytes='',
             source_left_current_sha256=sha((HERE/'source_packets'/str(left)/'current.tex').read_text()),
             source_right_current_sha256=sha((HERE/'source_packets'/str(left+1)/'current.tex').read_text()))
    join_records.append(row)
    extra.append(dict(record_type='source_folio_continuity',**row))
dump('folio_continuity.json',join_records)

native=(HERE/'native_span_394_415.tex').read_text()
macro_start=native.index(r'\providecommand{\Kosz}')
native_block=native[macro_start:]
reviewed415=(HERE/'source_packets'/'415'/'current.tex').read_text()
reviewed_block=reviewed415[reviewed415.index('% Expose VII additions'):]
extract=lambda s:[line for line in s.splitlines() if line.startswith('\\providecommand')]
assert extract(native_block)==extract(reviewed_block)
assert len(extract(native_block))==16
assert all(texts[415].count(line)==2 for line in extract(native_block))
macro_record=dict(record_type='continuation_macro_state',page=415,
    native_block=native_block,native_sha256=sha(native_block),reviewed_block=reviewed_block,
    reviewed_sha256=sha(reviewed_block),native_command_count=16,reviewed_command_count=16,
    command_payloads_equal=True,source_end_anchor=r'\sgaStableTarget{sga6.e07.expose}',
    decision='Both 16-command blocks are retained in source order at the end of415 before the VII heading. Every command is providecommand: an already defined control sequence retains its existing meaning, and an undefined one receives the same replacement text from the first block as from the second. Therefore the composite of these identical definition-state maps equals either map. No definition is moved before its original boundary.')
dump('boundary_macro_state.json',macro_record);extra.append(macro_record)

retained=[chk('396_400',20),chk('401_405',32),chk('406_410',4),chk('411_415',11),chk('411_415',15),chk('411_415',16),'ASTRA-VI-POWER-LOCUS-413']
config=dict(expose='VI',first=394,last=415,
    native_start=r'\sgaStableTarget{sga6.e06.sec.4}',native_end=r'\sgaStableTarget{sga6.e07.expose}',
    source='review/expose_vi/HANDOFF.md; reviewed_french exact page composition saved in reference_394_415_current.json and reference_394_415_diplomatic.json',
    reason='Complete English transfer of VI sections4–6 and its bibliography from the personally collated French source, preserving exact mathematical units, stable targets, source glyph distinctions, all paragraph and proof content, original folio boundaries, and both continuation macro blocks. The source-image evidence is attributed to review/expose_vi; this translation check does not claim a new image inspection.',
    variants=variants,notes=notes,extra_records=extra,retained_proof_audits=retained)
dump('batches.json',[config])
print(json.dumps(dict(variants=len(variants),mathematical_units=len(math_coverage),same_English_dispositions=len(notes),joins=len(join_records),continuation_commands=32)))
