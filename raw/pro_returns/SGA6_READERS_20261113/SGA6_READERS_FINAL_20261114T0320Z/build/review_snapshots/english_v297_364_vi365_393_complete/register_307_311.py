#!/usr/bin/env python3
"""Record the manually translated and placed English folios 307–311."""
from pathlib import Path
import json, sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from contribution import MATH, build_records, dump

def units(page, layer):
    return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(page)/f'{layer}.tex').read_text())]

pairs=json.loads((HERE/'lexical_math_pairs.json').read_text())
pairs=[p for p in pairs if p['page']!=311]
fr=units(311,'current')[9]
assert fr.count(r'\text{où }')==1
pairs.append(dict(page=311,layer='both',French_literal_unit=fr,English_literal_unit=fr.replace(r'\text{où }',r'\text{where }'),expected_multiplicity=1,status='individually reviewed lexical translation only',scope='Complete inverse-limit display in Remark1.14; only où is translated as where. The limit operator, its arrow, product, bounds, punctuation and all other literal characters remain unchanged.'))
dump(HERE/'lexical_math_pairs.json',pairs)
c,d=units(311,'current')[4],units(311,'diplomatic')[4]
assert c!=d
batches=json.loads((HERE/'batches.json').read_text())
batches=[b for b in batches if b['first']!=307]
batches.append(dict(expose='V',first=307,last=311,
    native_start='is an isomorphism.\n\nTo see that it is injective,',
    native_end='in \\hyperlink{sga6.e05.para.1-7}{1.7} that',
    source='review/expose_v/FROZEN_HANDOFF.md; reviewed French307–311 in both forms',
    reason='Complete passage comparison of Lemma1.9 proof,Theorem1.10,1.11,Lemma1.12,Theorem1.13,Remark1.14,and the opening of1.15. The six native stable targets remain in order at the matching passages. Every formula and diagram is transferred from the reviewed French without notation substitutions.',
    variants=[dict(id='EN-CONTRIB-V-311-01',page=311,old=c,printed=d,mode='display',source='check/findings/findings_311_315.json#2')],
    notes=[
        dict(page=307,source_id='ASTRA-V-GRAMMAR-307',English_rendering='To see that it is injective',decision='The French redundant-object grammar repair Pour le voir/Pour voir has the same idiomatic English purpose clause in both forms. No invented English grammatical error is introduced.'),
        dict(page=307,source_id='ASTRA-V-UNDERLINE-307;ASTRA-V-ABFIL-307',English_rendering='complete lemma conclusion, proof, and first theorem segment',decision='Retain the initial lexical underline and every separately ruled theorem phrase. Restore the exact anonymous morphism Ghat→H∘g, capital Phi diagram labels, source H∘g(A) object syntax,and comma ending the second Hom chain. The proof uses coarse filtration consistently with the earlier attested terminology.'),
        dict(page=308,source_id='ASTRA-V-UNDERLINE-308;ASTRA-V-ABFIL-308;ASTRA-V-FONT-308',English_rendering='all of1.10 continuation and1.11',decision='Restore the inclusive n≥1 bound, source semicolons, plain1.11 label,and absent final stop after cf.1.7. The script G category replaces the inherited English C_g notation at every occurrence; the source separately states the actual functor j and the epsilon isomorphism. Preserve literal Id,completion hats,and the product bound i=0.'),
        dict(page=309,source_id='ASTRA-V-PLACEHOLDER-309;ASTRA-V-G-309;ASTRA-V-UNDERLINE-309;ASTRA-V-ABFIL-309',English_rendering='coefficient-class map, kernel, quotient isomorphism, and full Lemma1.12',decision='Retain all six baseline placeholder dots, the source graded category, all three separately underlined Ab/fil names, source punctuation,and the exact factorization claim. The inverse construction is translated as a morphism in the opposite direction, matching the printed source before its inverse property is proved on310. No extra unnamed diagram labels or argument parentheses are introduced.'),
        dict(page=310,source_id='ASTRA-V-PLACEHOLDER-310;ASTRA-V-G-310;ASTRA-V-UNDERLINE-310;ASTRA-V-ABFIL-310',English_rendering='entire shifted-generator proof and Theorem1.13 opening',decision='Restore the literal coefficient map X_i↦the(i−1)-th coefficient of chi,the parenthesized generator notation K[(X_i)] in all diagram objects,the source semicolon after the diagram,and the placeholder in the quotient functor omitted by inherited English. All word-level theorem rules remain separate from mathematical expressions and punctuation.'),
        dict(page=311,source_id='ASTRA-V-PLACEHOLDER-311;ASTRA-V-FONT-311;ASTRA-V-ABFIL-311',English_rendering='full Theorem1.13 continuation,Remark1.14,and opening1.15',decision='Retain the plain of between the first two formulas,source script G,all low placeholder dots,and all three ruled category targets. The inverse-limit statement keeps its actual headed isomorphism and underleftarrow Lim operator. The missing comma in the first polynomial list is explicitly branched; the other four complete lists remain unchanged.'),
        dict(page=311,source_id='review/expose_v/page_status.jsonl#pages307-311',English_rendering='five exact page boundaries, six native stable targets,and no author notes',decision='All prose clauses and formula positions were manually compared with the reviewed French. The two theorem statements and the filtered-algebra construction retain their actual page splits;311 ends with We have seen before the312 continuation. There is no author-note call/text or native continuation macro block in this batch.')
    ],retained_proof_audits=[]))
dump(HERE/'batches.json',batches)
build_records()
