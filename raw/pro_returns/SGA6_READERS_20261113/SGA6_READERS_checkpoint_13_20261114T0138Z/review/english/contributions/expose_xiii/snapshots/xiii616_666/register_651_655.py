from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from contribution import make_chunk
u=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
pair=dict(page=653,layer='both',French_literal_unit=u(653)[9],English_literal_unit=u(653)[9].replace('\\text{et}','\\text{and}'),expected_multiplicity=1,status='Exact complete-unit lexical translation: et becomes and between the two coefficient definitions; all mathematical commands, indices, bounds, arguments, punctuation and whitespace remain literal.',source='reviewed XIII6.1 coefficient definitions')
lp=json.loads((H/'lexical_math_pairs.json').read_text());lp=[p for p in lp if p['page']!=653];lp.append(pair)
(H/'lexical_math_pairs.json').write_text(json.dumps(lp,ensure_ascii=False,indent=2)+'\n')
make_chunk('XIII',651,655)
b=json.loads((H/'batches.json').read_text());b=[x for x in b if x['first']!=651]
v=[]
def add(p,old,printed,s,mode='text'):v.append(dict(id=f'EN-CONTRIB-XIII-{len(v)+31:03}',page=p,old=old,printed=printed,source=s,mode=mode))
add(651,r'K\"unneth',r'K\"Unneth','fixes/MISPRINTS_6.json#620')
add(652,u(652)[9],u(652)[9].replace('_{\\rm num}','_{\\rm mum}'),'fixes/MISPRINTS_6.json#622')
add(654,u(654)[6],u(654)[6].replace('I(p)))','I(p))'),'fixes/MISPRINTS_6.json#624')
add(655,u(655)[29],u(655)[29].replace('{O}_P','{O}_X'),'ASTRA-XIII-0042')
end='Since $s\\geq1$, one has $G\'\\ne0$; hence '
s=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text();assert s.count(end)==1
b.append(dict(expose='XIII',first=651,last=655,native_start=b[-1]['native_end'],native_end=end,source='Both exact reviewed French651–655 packets and frozen XIII source/proof decisions.',reason='Restore full Néron–Severi finite-rank argument, numerical-cycle pairing, Betti interpretation, all universal-polynomial definitions and the complete regularity diagrams/proofs. Preserve source mixed dot/comma pairing and the supported a-coefficient specialization. The coefficient-display conjunction alone has an exact lexical pair.',variants=v,notes=[dict(page=651,topic='Mixed intersection notation',decision='MISPRINT621 and Codex88 are rejected: the exact bilinear map (b,a)↦deg(b·a) identifies the product-dot and comma-separated bracket expressions. Both printed forms are retained without a consistency rewrite.'),dict(page=652,topic='French participle accent',decision='MISPRINT623 dûe/due both translate due with the same explicit IGUSA attribution; no English lexical error is created.'),dict(page=654,topic='Permitted coefficient specialization',decision='Codex89 is rejected: choosing c=a in Lemma6.2 gives c_(m,i)=a_(m,i) by the exact6.1 sums, and hence the printed p=P_r(a_(m,0),...,a_(m,r)). Both English forms retain the source a arguments, independently from the earlier c_i=b_i−a_i used to choose m.'),dict(page=655,topic='French misplaced accent',decision='MISPRINT625 graĉe/grâce translates by in both forms; the reference1.6.2 and mathematical conclusion are unchanged.'),dict(page=653,topic='Complete-unit lexical translation',decision='Only et between the two coefficient definitions becomes and, through lexical_math_pairs.json; every mathematical byte outside that word is identical.'),dict(page=655,topic='Proof and diagram placement',decision='Both full commutative diagrams retain every row/column, source O form, exact trailing point placement and all arrows. The655/656 boundary is immediately after the second complete diagram, before the ensuing proof paragraph.')]))
(H/'batches.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
