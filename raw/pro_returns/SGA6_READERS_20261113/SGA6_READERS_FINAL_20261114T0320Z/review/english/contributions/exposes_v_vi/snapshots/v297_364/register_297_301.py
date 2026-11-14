#!/usr/bin/env python3
"""Record the manually compared English297–301 passage and lexical math pair."""
from pathlib import Path
import json
here=Path(__file__).resolve().parent
units=json.loads((here/'source_packets/299/units.json').read_text())
f=units[19]
e=f
for a,b in [
 (r'\text{ est séparé et complet}',r'\text{ is separated and complete}'),
 (r'\text{Si }',r'\text{If }'),
 (r'\text{ est une }',r'\text{ is a graded }'),
 (r'\text{-algèbre graduée, munie de la filtration}',r'\text{-algebra, endowed with the filtration}'),
 (r'\text{associée à sa graduation, et si }',r'\text{associated with its grading, and if }'),
 (r'\text{ est un groupe fini opérant sur }',r'\text{ is a finite group acting on }'),
 (r'\text{par morphismes gradués, alors }',r'\text{by graded morphisms, then }'),
 (r"\text{(l'exposant }",r'\text{(the exponent }'),
 (r'\text{ désignant les invariants sous }',r'\text{ denoting invariants under }')]:
 assert e.count(a)==1,(a,e.count(a));e=e.replace(a,b)
pairs=[dict(page=299,layer='both',French_literal_unit=f,English_literal_unit=e,
 expected_multiplicity=1,status='individually reviewed lexical translation;every nonlexical character and mathematical token retained',
 scope='1.3,the two conditions on H and the parenthetical explanation of G-invariants')]
(here/'lexical_math_pairs.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
configs=[dict(expose='V',first=297,last=301,
 native_start=r'\sgaStableTarget{sga6.e05.expose}',
 native_end='\\[\n  \\theta=\\xi(1+Xt).\n\\]\nWe show',
 source='review/expose_v/FROZEN_HANDOFF.md;reviewed French297–301 in both forms',
 reason='Complete passage reconstruction from the frozen French source,including title/byline form,actual page boundaries,all hypotheses and formulas,and the exact lexical underlines. The native mathematical abbreviations and added/omitted units are replaced by the literal reviewed units;all twelve native stable targets are retained in their corresponding passages.',
 variants=[],
 notes=[
  dict(page=297,source_id='check/findings/findings_296_300.json#10',English_rendering='has the advantage',decision='French à/a spelling repair gives the same English finite-verb construction in both forms;no invented English spelling variant.'),
  dict(page=300,source_id='check/findings/findings_296_300.json#24;fixes/RECONCILE_CODEX_6.json#307',English_rendering='the former',decision='French permier/premier typographic transposition has the same English reading in both forms.'),
  dict(page=301,source_id='check/findings/findings_301_305.json#3',English_rendering='subgroup',decision='French sous groupe/sous-groupe compound spelling has the same English rendering in both forms.'),
  dict(page=297,source_id='ASTRA-V-FONT-297',English_rendering='title and byline underlines;plain1.1',decision='Preserve the inspected title and byline case/rules and ordinary paragraph label;the native title had omitted those source distinctions.'),
  dict(page=298,source_id='review/expose_v/page_status.jsonl#page298',English_rendering='entire representability paragraph and the unique homomorphism continued onto299',decision='All literal reviewed formulas are restored,including the semicolon in1.1.1,the plain indexing N,the underlined functor categories,and closed phi. The final homomorphism is prose with its exact source page split,not the native added membership-arrow display.'),
  dict(page=299,source_id='review/expose_v/page_status.jsonl#page299',English_rendering='complete1.3 conditions,examples,and1.4 opening',decision='The explicit G-invariant explanation remains inside the conditions display with its original headed arrow. The native added series-definition display in example3 is omitted because it has no corresponding reviewed French unit. The distinct Ab.fil. and separately ruled Ab fil occurrences remain literal.'),
  dict(page=299,source_id='en/glossaries/GLOSSARY_SGA4_FR_EN.tsv#grossière',English_rendering='coarse filtration;g,the initial of grossière',decision='Use the attested English adjective coarse;retain the quoted French word in the explanation of the initial g so that the stated letter remains exact.'),
  dict(page=300,source_id='review/expose_v/page_status.jsonl#page300',English_rendering='the i-th symmetric function;full invariant-ring comparison',decision='Remove native elementary,which the reviewed source does not print,and restore the intermediate H(K[T]^{S_n}) object and its headed isomorphism. Fraktur symmetric-group letters and every formula token are literal. The source-only nonprinting transcription comment is retained in the reference packet,not copied into the translated author body.'),
  dict(page=301,source_id='ASTRA-V-UNDERLINE-301;ASTRA-V-ELLIPSES-301',English_rendering='full1.6 statement and first proof through and put',decision='Restore the precise word-rule groups,ordinary item labels,Ghat_K arguments,capital Phi morphism,n>=1 bound,printed mod. notation,low ellipses,and the complete diagram. The native xi substitutions and shortened invariant target are removed by direct source transfer.'),
  dict(page=297,source_id='review/expose_v/page_status.jsonl#pages297-301',English_rendering='all five source page boundaries and all twelve stable targets',decision='Every prose clause and formula position was compared against the corresponding reviewed French page. The split category-of-groups/that-are-abelian phrase keeps the original conceptual boundary while providing grammatical English. There are no author footnotes in these five personally checked source pages.')
 ],retained_proof_audits=[])]
(here/'batches.json').write_text(json.dumps(configs,ensure_ascii=False,indent=2)+'\n')
