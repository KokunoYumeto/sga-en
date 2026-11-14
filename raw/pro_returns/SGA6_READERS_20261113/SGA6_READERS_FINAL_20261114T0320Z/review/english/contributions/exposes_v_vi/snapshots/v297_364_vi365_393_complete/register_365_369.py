#!/usr/bin/env python3
"""Register the full opening VI argument, preserving its exact notation."""
from pathlib import Path
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT,dump,build_records
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def units(p,layer):return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(p)/f'{layer}.tex').read_text())]
def variant(p,index,sid,mode,suffix='01'):
    c,d=units(p,'current')[index],units(p,'diplomatic')[index];assert c!=d
    if mode=='math':c,d=c[2:-2],d[2:-2]
    return dict(id=f'EN-CONTRIB-VI-{p}-{suffix}',page=p,old=c,printed=d,source=sid,mode=mode)
variants=[variant(365,8,'ASTRA-VI-PROJECTIVE-P-365','math'),
    dict(id='EN-CONTRIB-VI-365-02',page=365,old=units(365,'current')[24]+'-Module '+units(365,'current')[25]+' of finite presentation',printed=units(365,'diplomatic')[24]+'-Module module '+units(365,'diplomatic')[25]+' of finite presentation',source='check/findings/findings_361_365.json#36',mode='text'),
    dict(id='EN-CONTRIB-VI-365-03',page=365,old='see EGA II 8.12.1).',printed='see EGA II 8.12.1.',source='check/findings/findings_361_365.json#37',mode='text'),
    variant(366,33,'ASTRA-VI-TARGET-RULE-366','display'),
    dict(id='EN-CONTRIB-VI-368-01',page=368,old='do not depend on the decomposition.',printed='do not depend on the decomposition',source='check/findings/findings_366_370.json#7',mode='text'),
    variant(369,7,'ASTRA-VI-PROJECTIVE-P-369','math'),
    variant(369,9,'ASTRA-VI-BASE-SHEAF-369','math','02'),
    variant(369,31,'ASTRA-VI-PROJECTIVE-P-369','math','03')]
pairs=json.loads((HERE/'lexical_math_pairs.json').read_text());pairs=[p for p in pairs if p['page'] not in [366,368]]
f=units(366,'current')[15];e=f.replace(r'\text{pour tout }',r'\text{for every }');assert f!=e and f in units(366,'diplomatic')
pairs.append(dict(page=366,layer='both',French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='The graded-shift definition: pour tout becomes for every. All source indices, parentheses, rules and terminal punctuation remain literal.'))
f=units(368,'current')[15];e=f.replace(r'\uline{pour}',r'\uline{for}').replace(r'\uline{est localement libre de type fini sur}',r'\uline{is locally free of finite type on}').replace(r'\uline{est un}',r'\uline{is a graded}').replace(r'\uline{-Module gradué de présentation finie}',r'\uline{-Module of finite presentation}')
assert f!=e and f in units(368,'diplomatic')
pairs.append(dict(page=368,layer='both',French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='The complete three-property display: translate only its ruled lexical words, moving graded into the preceding ruled phrase for English grammar. Every formula, index, inequality, module rule, label, space outside those lexical arguments and punctuation remains exact.'))
dump(HERE/'lexical_math_pairs.json',pairs)
extra=[]
for p,paragraph,reason in [
    (364,True,'The bibliography and both continuation blocks end Exposé V; the next source page opens the separately titled Exposé VI.'),
    (365,True,'The complete a–c plan ends on365;366 begins the distinct second numbered plan item.'),
    (366,True,'The definition1.2.2 ends on366;367 begins a new paragraph Let M be a free graded module.'),
    (367,True,'The complete induction proof ends on367;368 begins its separate consequence for homogeneous bases.'),
    (368,False,'The368 final comparison ends with a comma and continues with369 and hence such that.')]:
    f=(HERE/'source_packets'/str(p)/'current.tex').read_text();g=(HERE/'source_packets'/str(p+1)/'current.tex').read_text();e=(HERE/'translations'/f'{p}.tex').read_text();n=(HERE/'translations'/f'{p+1}.tex').read_text()
    assert e.endswith('\n\n')==paragraph,(p,repr(e[-30:]));assert not n.startswith('\n')
    extra.append(dict(record_type='manually_compared_source_folio_join',after=p,before=p+1,paragraph_break=paragraph,source_tail=f[-400:],source_head=g[:400],English_tail=e[-250:],English_head=n[:250],source_page_sha256s={str(p):sha(f),str(p+1):sha(g)},reason=reason))
local_commands='\\renewcommand{\\Sym}{\\mathbf{S}}\n\\renewcommand{\\Projz}{\\underline{\\operatorname{Proj}}_0}\n'
assert local_commands in (HERE/'source_packets/365/current.tex').read_text()
assert local_commands in (HERE/'source_packets/365/diplomatic.tex').read_text()
assert local_commands in (HERE/'translations/365.tex').read_text()
extra.append(dict(record_type='reviewed_local_macro_scope',page=365,source_id='check/findings/findings_361_365.json#39;ASTRA-VI-GLYPHS-365',commands=local_commands,commands_sha256=sha(local_commands),decision='Preserve the two exact local renewals after the title, following the complete364 continuation blocks. Sym uses the explicitly accepted NOTE6 transport; Projz retains its lower rule and plain subscript. The separately branched projective P operators are literal occurrences, not a global macro rule.'))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=365]
batches.append(dict(expose='VI',first=365,last=369,native_start=r'\sgaStableTarget{sga6.e06.expose}',native_end=r'\sgaStableTarget{sga6.e06.cor.1-4}',
    source='review/expose_vi/HANDOFF.md; reviewed French365–369 in both forms',
    reason='Restore the complete opening title and credit, theorem, three-part plan, graded-module definitions, Proposition1.2.3 and its full induction, and Proposition1.3 through the actual369 limit argument. The inherited English had shortened and reordered this proof; its native span is consumed to the next target, while the restored source proof continues on370 before that target.',variants=variants,
    notes=[
        dict(page=365,source_id='check/findings/findings_361_365.json#32;check/findings/findings_361_365.json#33;ASTRA-VI-WORD-RULES-365;ASTRA-VI-GLYPHS-365;ASTRA-VI-PROJECTIVE-P-365',English_rendering='complete title, credit, theorem and proof plan',decision='Restore all title words, their recorded lower-rule geometry, Pierre BERTHELOT, the exact raised-dot K units, inline f and f-star maps, and every theorem word-rule group. Preserve the three individual plan items and all a–c clauses, including the symmetric-algebra explanation and exact EGA locator omitted by native English. The projective P variant maps each quotient E_T→L to itself, with inverse itself; its symmetric algebra and degree-zero chart maps are induced by id_E, exactly as the source audit proves.'),
        dict(page=365,source_id='check/findings/findings_361_365.json#36;check/findings/findings_361_365.json#37;check/findings/findings_361_365.json#35',English_rendering='graded Module module alternative and original parenthesis',decision='The duplicated noun is represented by Module module in diplomatic and Module currently, keeping the capital distinction and the identical graded sheaf. The absent closing parenthesis after EGA II8.12.1 is separately branched. Preserve the complete inline resolution with low dots and every index on the L and N sheaves; no application-of-Proj paragraph is added to the source plan.'),
        dict(page=366,source_id='ASTRA-VI-PARAGRAPH-NUMBERS-366;ASTRA-VI-GLYPHS-366;ASTRA-VI-TARGET-RULE-366',English_rendering='complete1.2,1.2.1 and1.2.2 definitions',decision='Move the retained native sec.1.2 target to the actual ordinary1.2 label, after the two remaining plan items; omit the unprinted native Plan of the proof heading there. Restore both local definitions with every neighborhood and exact presentation, the canonical component map, and the full homogeneous-degree definition. The target M rule has a literal branch: x in M_n tensor a in B_(k−n) maps to a.x in the same M_k. The source comma and following capital Pour are retained by the corresponding comma and capital For; no unadjudicated punctuation correction is introduced.'),
        dict(page=367,source_id='check/findings/findings_366_370.json#4;check/findings/findings_366_370.json#5;check/findings/findings_366_370.json#6;ASTRA-VI-GLYPHS-367;ASTRA-VI-WORD-RULES-367',English_rendering='Proposition1.2.3 and its complete induction proof',decision='Restore the actual label1.2.3 while retaining the native prop.1-2 stable target. The two headless isomorphism symbols and the headed comparison arrow remain distinct literal forms. Restore all degree bounds, both rank comparisons, the lowest-degree direct summands and the quotient induction; remove the native inserted restriction asserting B_0=O_S, which does not occur in this paragraph.'),
        dict(page=368,source_id='check/findings/findings_366_370.json#7;check/findings/findings_366_370.json#8;check/findings/findings_366_370.json#9;check/findings/findings_366_370.json#10;ASTRA-VI-WORD-RULES-368;ASTRA-VI-GLYPHS-368',English_rendering='complete homogeneous-basis consequence and Proposition1.3 noetherian proof',decision='Restore both endpoint nonvanishing conditions and branch the missing paragraph-ending stop. All three proposition properties, their ruled lexical words, and the literal (1.2) reference are retained. Restore the source reduction by the maximum of local bounds, separate i/ii arguments, EGA II3.4.5 construction, complete Gamma-star expression with its exact nonparenthesized Projz argument, the TN-isomorphism, and the truncated direct-sum comparison. The damaged EGA glyph reading is attributed to the completed source decision, not newly claimed here.'),
        dict(page=369,source_id='ASTRA-VI-BASE-SHEAF-369;ASTRA-VI-PROJECTIVE-P-369;check/findings/findings_366_370.json#13;ASTRA-VI-GLYPHS-369',English_rendering='complete Cartesian base change and limit construction in source order',decision='Restore the square before the general-limit paragraph, all arrow labels and their sides, every sheaf, bound, transition map and named scheme. The two projective-P occurrences receive separate literal variants from the same source proof. The coefficient sheaf O_X/O_(X0) is independently branched: g-star F0 is O_X tensor over g-inverse O_(X0) with g-inverse F0, so F0 is a module over the displayed target’s O_(X0). Preserve the unfinished final index at the369 marker; its next source clause will be restored on370.'),
        dict(page=369,source_id='check/findings/findings_366_370.json#11;check/findings/findings_366_370.json#12',English_rendering='noetherian; where',decision='The French duplicated n in noethériennnes and the relative ou/où accent repair have unchanged English renderings noetherian and where. The same base schemes and base-change morphisms occur in both forms.'),
        dict(page=369,source_id='review/expose_vi/page_status.jsonl#pages365-369',English_rendering='five complete source pages and eight native stable targets',decision='All prose, mathematical units, original rule endpoints and placement have been manually compared with the two reviewed French forms. Five joins are separately recorded. There are no original author notes in these pages. Source images and proof reasons remain attributed to the coordinator’s completed French review; no new image or PDF review is claimed.')
    ],extra_records=extra))
dump(HERE/'batches.json',batches);build_records()
