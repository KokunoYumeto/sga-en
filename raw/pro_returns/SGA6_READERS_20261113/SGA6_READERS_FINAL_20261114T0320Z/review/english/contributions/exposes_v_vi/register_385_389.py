#!/usr/bin/env python3
"""Register the complete perfect-complex proof through the389 induction opening."""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT,dump,build_records
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def units(p,layer):return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(p)/f'{layer}.tex').read_text())]
def english(s):
    return s.replace(r'\uline{est un isomorphisme de}',r'\uline{is an isomorphism in}').replace(r'\uline{Le morphisme canonique}',r'\uline{The canonical morphism}').replace(r'\uline{-parfait}',r'\uline{-perfect}').replace(r'\uline{est}',r'\uline{is}').replace(r'\text{car }',r'\text{since }').replace(r'\text{ et }',r'\text{ and }').replace(r'\text{ pour }',r'\text{ for }').replace(r'\text{pour }',r'\text{for }')
def variant(p,index,sid,mode,suffix='01',related=()):
    c,d=english(units(p,'current')[index]),english(units(p,'diplomatic')[index]);assert c!=d
    if mode=='math':
        assert (c.startswith(r'\(') and d.startswith(r'\(')) or (c.startswith('$') and d.startswith('$'))
        c,d=(c[2:-2],d[2:-2]) if c.startswith(r'\(') else (c[1:-1],d[1:-1])
    result=dict(id=f'EN-CONTRIB-VI-{p}-{suffix}',page=p,old=c,printed=d,source=sid,mode=mode)
    if related:result['related_sources']=list(related)
    return result
variants=[
    variant(385,12,'ASTRA-VI-DEGREE-385','math'),
    variant(385,21,'ASTRA-VI-DERIVED-R-385','display','02'),
    variant(385,25,'ASTRA-VI-PROJECTIVE-P-385','math','03',related=['ASTRA-VI-PROJECTIVE-ARG-RULE-385']),
    variant(385,26,'check/findings/findings_381_385.json#32','math','04'),
    variant(386,0,'ASTRA-VI-DERIVED-R-386','display'),
    variant(386,18,'ASTRA-VI-DERIVED-R-386','display','02'),
    variant(387,0,'check/findings/findings_386_390.json#5','display'),
    variant(389,3,'ASTRA-VI-DERIVED-R-389','math'),
    variant(389,6,'ASTRA-VI-DERIVED-R-389','math','02'),
    variant(389,13,'ASTRA-VI-DERIVED-L-389','math','03'),
    dict(id='EN-CONTRIB-VI-389-04',page=389,old='where the '+units(389,'current')[19]+' are the perfect complexes',printed='where the '+units(389,'diplomatic')[19]+' are the perfect complexes',source='check/findings/findings_386_390.json#11',mode='text')]
pairs=json.loads((HERE/'lexical_math_pairs.json').read_text());pairs=[p for p in pairs if p['page'] not in [386,389]]
for layer in ['current','diplomatic']:
    f=units(386,layer)[0];e=english(f);assert f!=e
    pairs.append(dict(page=386,layer=layer,French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='Translate the four exact ruled prose groups in the complete two-item proposition display. Both literal derived-R occurrences retain their respective diplomatic/current forms, and all item labels, formula tokens, punctuation and word-rule boundaries remain unchanged.'))
for index in [33,34]:
    f=units(389,'current')[index];e=english(f);assert f!=e and f in units(389,'diplomatic')
    pairs.append(dict(page=389,layer='both',French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='Translate only car,et,pour as since,and,for in the complete direct-image calculation. Keep the two plain R^i symbols, their actual parentheses, all inequalities, all sheaf rules and the exact terminal punctuation.'))
dump(HERE/'lexical_math_pairs.json',pairs)
extra=[]
for p,paragraph,reason in [
    (384,False,'The384 last display and comma continue with it suffices on385, in the same beta-construction sentence.'),
    (385,False,'The385 proposition ends with the colon introducing the two-item display at the top of386.'),
    (386,False,'The final386 colon introduces the complete beta isomorphism display on387.'),
    (387,True,'The387 finite-covering and common lower-degree-bound paragraph ends before the388 canonical cone construction.'),
    (388,True,'The388 cone argument ends with corresponding complex is acyclic;389 starts the separately numbered2.8 paragraph.')]:
    f=(HERE/'source_packets'/str(p)/'current.tex').read_text();g=(HERE/'source_packets'/str(p+1)/'current.tex').read_text();e=(HERE/'translations'/f'{p}.tex').read_text();n=(HERE/'translations'/f'{p+1}.tex').read_text()
    assert e.endswith('\n\n')==paragraph,(p,repr(e[-30:]));assert not n.startswith('\n')
    extra.append(dict(record_type='manually_compared_source_folio_join',after=p,before=p+1,paragraph_break=paragraph,source_tail=f[-400:],source_head=g[:400],English_tail=e[-250:],English_head=n[:250],source_page_sha256s={str(p):sha(f),str(p+1):sha(g)},reason=reason))
extra.append(dict(record_type='legacy_stable_target_formula_mapping',page=385,stable_target='sga6.e06.eq.2-5-2',native_formula_number='2.5.2',source_formula_number='2.5.3',source_id='ASTRA-VI-DERIVED-R-385;review/expose_vi/page_status.jsonl#page385',decision='The native target named eq.2-5-2 was attached to the derived natural transformation Projz composed with RF_k→Id. Preserve that target at the same mathematical map, now bearing the actual source number2.5.3. Restore the distinct section map Gamma(V,M)_(s)→Gamma(D_+(V,s),F) with its actual number2.5.2 earlier on the page. No legacy target is reassigned to the section map, and no source formula is omitted.'))
name='independent_sections_audit_385.json';rel='review/expose_vi/'+name;raw=(ROOT/rel).read_bytes();dest=HERE/'attributed_source_audits'/name;dest.write_bytes(raw)
extra.append(dict(record_type='attributed_source_audit_packet',page=385,source_id='ASTRA-VI-DEGREE-385;ASTRA-VI-SECTION-EQUALITY-385',source_packet=rel,contribution_copy='review/english/contributions/exposes_v_vi/attributed_source_audits/'+name,packet_sha256=hashlib.sha256(raw).hexdigest(),decision='Exact source proof packet retained separately: the graded alpha component, the explicit P1 restriction map and both truncation examples, and the well-defined map z/s^n→a^(-n)rho(j_nd(z)). The source section-space equality is retained in both English bodies.'))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=385]
batches.append(dict(expose='VI',first=385,last=389,native_start=r'\sgaStableTarget{sga6.e06.eq.2-5-2}',native_end=r'\providecommand{\Sym}{\operatorname{Sym}}',
    source='review/expose_vi/HANDOFF.md; reviewed French385–389 in both forms',
    reason='Restore the complete beta localization construction, both source formulas2.5.2/2.5.3, the full local perfection and acyclicity proof of2.6, the entire finite cone construction in2.7 and every generation/dependence/independence calculation in2.8 through the389 sentence boundary. Six native stable targets remain in their original order. The native continuation macro block immediately following this span is reserved for the390–393 chunk.',variants=variants,
    notes=[
        dict(page=385,source_id='check/findings/findings_381_385.json#29;check/findings/findings_381_385.json#30;ASTRA-VI-DEGREE-385;ASTRA-VI-SECTION-EQUALITY-385',English_rendering='full adjunction, section map and fraction formula',decision='Restore the f_(U,s)*O_X-linearity, every open-set quantifier, the entire section map2.5.2, and the exact alpha definition inline. The alpha_d/alpha_nd source difference has its own branch: graded multiplication sends s^n to degree nd and alpha_nd(s^n)=alpha_d(s)^n, the invertible trivialization of O_X(nd) on D_+(V,s). The printed section-space equality remains literal in both bodies. For the recorded P1 example the restriction sends a x0^2+b x0x1+c x1^2 to(a+bt+ct^2)x0^2; t^3 x0^2 is outside its image. The exact actual fraction map and the separate truncation example are preserved in the attributed audit, without a replacement author passage.'),
        dict(page=385,source_id='ASTRA-VI-DERIVED-R-385;ASTRA-VI-PROJECTIVE-P-385;ASTRA-VI-PROJECTIVE-ARG-RULE-385;check/findings/findings_381_385.json#32;ASTRA-VI-WORD-RULES-385',English_rendering='derived beta and the complete proposition introduction',decision='Retain the actual2.5.3 number, capital Id and full domain. The literal two lower R rules and current mathbb R refer to F_k applied to the identical injective resolution, with the identity chain comparison. The full projective expression branches both the double-ruled P and the plain E argument: id_E induces id on every symmetric power and Proj chart, and the represented quotient functor sends each quotient to itself. The baseline stop after L is separately branched to the raised complex dot, with identity in each complex degree. Preserve the separate quasi/compact rules and their intervening unruled hyphen, the plain final X, and every quantified hypothesis.'),
        dict(page=386,source_id='check/findings/findings_386_390.json#1;ASTRA-VI-WORD-RULES-386;ASTRA-VI-DERIVED-R-386;ASTRA-VI-GLYPHS-386',English_rendering='complete local perfection justification and proof of Proposition2.6',decision='Restore the entire four-rule two-item statement, the fibered-category explanation, its I4.0 and1.5.1 axioms argument, and the reduction via global resolutions II2.2.9. Retain the leftward isomorphism from the strictly perfect resolution to L and both D_parf occurrences. Restore the full injective-acyclicity argument, the exact RF_k=F_k display, the common k0 bound and its1.3/1.6 references. The two displayed R conventions are explicit branch records, applying the same F_k to the same resolution; no plain higher-derived R^i elsewhere is changed.'),
        dict(page=387,source_id='check/findings/findings_386_390.json#5;check/findings/findings_386_390.json#6;ASTRA-VI-GLYPHS-387;ASTRA-VI-PARAGRAPH-NUMBER-387',English_rendering='complete2.6 conclusion and2.7 graded component construction',decision='The separated second comma in the first display is retained diplomatically and one comma remains currently. Restore the tensoring functor and its explicit source category before2.7.2. Preserve every triangle vertex, arrow orientation, four literal baseline stops and following comma; keep the source single d in the inline twist rather than the native added d_i. Restore the exact finite-covering complex M_U-prime, its common d0 bound and Comp_d vanishing. No unprinted decomposition heading is added.'),
        dict(page=388,source_id='check/findings/findings_386_390.json#7;check/findings/findings_386_390.json#8;ASTRA-VI-GLYPHS-388',English_rendering='entire cone and finite-termination argument',decision='Restore the full first canonical morphism, all reasons its cone is C0-perfect, the commutative square with both headless vertical comparisons and right-side rotated tildes, and every local complex/degree statement. Keep the source Comp_n in the explanatory tensor expression. Restore the d0→d0+1 induction and the reduction to the finite filtration of each term in1.7; native English had condensed this to a few sentences. Every mathematical token and its displayed/inline placement is literal.'),
        dict(page=389,source_id='ASTRA-VI-DERIVED-R-389;ASTRA-VI-DERIVED-L-389;check/findings/findings_386_390.json#11;check/findings/findings_386_390.json#12;ASTRA-VI-GLYPHS-389;ASTRA-VI-PARAGRAPH-NUMBER-389',English_rendering='all generation, dependence and independence calculations',decision='Restore the exact derived-category argument, tensor/pullback equality and its flatness parenthesis, every class-map factor and the naive-to-perfect map H→[H[0]]. Preserve both plain R^i cohomological symbols and all their parentheses. Total R and derived L receive their occurrence-specific branches; flat pullback is represented by the exact functor O_X tensor_(f^-1O_S) f^-1(−), with its resolution comparison. The prose K_i without/with raised dot is branched under the identity on the complex with its existing differential. Restore both complete vanishing displays, the exact final relation and the first coefficient extraction; the source induction continues on390 after the terminal word we.'),
        dict(page=386,source_id='check/findings/findings_381_385.json#31;check/findings/findings_386_390.json#2',English_rendering='in the case where; which allows us',decision='The French accent repair ou/où on385 and relative-expression repair de/ce on386 have the same English relative clauses in both forms. The former clause refers to the same quasi-coherent F; the latter refers to the identical displayed strict-resolution isomorphism. No unrelated English spelling or grammatical error is invented.'),
        dict(page=389,source_id='review/expose_vi/page_status.jsonl#pages385-389',English_rendering='five complete source pages and six native stable targets',decision='All prose, local underline groups, formula placement, source punctuation and eleven branch records were manually compared with both reviewed French forms. All five joins are explicit. The source author-claim audit is separately attributed and hash-linked. There is no original author note on these pages, no new full-page scan claim and no English PDF inspection.')
    ],extra_records=extra,retained_proof_audits=['ASTRA-VI-SECTION-EQUALITY-385']))
dump(HERE/'batches.json',batches);build_records()
