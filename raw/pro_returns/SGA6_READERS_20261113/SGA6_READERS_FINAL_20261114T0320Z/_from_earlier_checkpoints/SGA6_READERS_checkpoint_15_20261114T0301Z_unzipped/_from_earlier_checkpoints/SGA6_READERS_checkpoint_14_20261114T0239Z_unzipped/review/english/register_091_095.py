#!/usr/bin/env python3
"""Register the manually translated 91–95 passage and source variants."""
from pathlib import Path
import json
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P091_095.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
anchor=r'\emph{Proof.} The procedure is as follows: first one shows that \(r\) and \(s\) may be chosen locally so as to make \(\Ho^{n+1}(u)\) injective; one verifies '
a=native.index(anchor)+len(anchor)
b=native.index(r'\sgaStableTarget{sga6.e01.prop.2-2}',a)
record=dict(id='EN-EXPOSE-I-091-095',page='91–95',place='Exposé I extension lemma proof and beginning of pseudo-coherence',layer='both',
 old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/91–95/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Fresh faithful translation restores the omitted equality H^(n+1)(u′)=H^(n+1)(u_X), marked exact sequence and its explicit reference, literal octahedron and punctuation, statement word-group underlines, plain definition terms and source placements. Every mathematical unit is compared exactly. Explicit current variants supply the arrowhead92, two category rules93, transition composite94 and correct fiber index95.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

current,ref=load_reviewed_pages(95)
diplomatic,dref=load_reviewed_pages(95,'diplomatic')
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if not 79<=int(x['id'].rsplit('-',1)[1])<=83]
new=[]
def variant(number,page,corrected,printed,source,reason,region,mode='text'):
 assert chunk.count(corrected)==1,(number,chunk.count(corrected))
 new.append(dict(id=f'EN-VAR-{number:03}',page=page,old=corrected,printed=printed,corrected=corrected,mode=mode,
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<95 else None,
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
diagram=[m.group(0) for m in MATH.finditer(current[92]) if r'\begin{tikzpicture}' in m.group(0)]
assert len(diagram)==1
variant(79,92,diagram[0],diagram[0].replace(r"\draw[->] (Ep) -- node[below] {$u'$} (FX);",r"\draw (Ep) -- node[below] {$u'$} (FX);"),
 'check/findings/findings_091_095.json#5; review/expose_i/decisions.jsonl',
 "The printed u' segment has no arrowhead. The preceding text defines u':E'→F_X and G' as its cone, which fixes the arrow direction toward F_X. Current adds that head; diplomatic retains the bare segment.", 'octahedron bottom edge', 'display')
text=r'\textbf{Lemma 1.4.2.} \uline{Let} \(\underline{C}\)'
variant(80,93,text,text.replace(r'\underline{C}','C'),
 'check/findings/findings_091_095.json#9',
 'The first declared category C has no printed underline. Its occurrence inside the derived category D(C) is underlined in the same sentence; current supplies the same category rule here.', 'Lemma1.4.2 category declaration')
text=r'\uline{a morphism of complexes of} \(\underline{C}\)'
variant(81,93,text,text.replace(r'\underline{C}','C'),
 'check/findings/findings_091_095.json#9',
 'The second category C has no printed underline. It is the category of the complexes E and F and the argument of D(C), whose C is individually underlined; current supplies its missing rule.', 'Lemma1.4.2 category of the complexes')
variant(82,94,r'v^j=(v_i v_{i+1}\ldots v_{n-1})^j',r'v^j=(v_i)^j',
 'ASTRA-I-COMPOSITION-094; review/expose_i/add_094_composition.py; EN_INDEPENDENT_SOURCE_ASSESSMENTS.jsonl',
 "The transitions have domains E→E'_(n-1) and E'_(i+1)→E'_i. Their composite V_i=v_i...v_(n-1) has domain E, and its degree-j component stabilizes for i≤j because the lower transitions are identities in that degree. The printed isolated v_i has domain E'_(i+1), so the composite is required to define v:E→E'. The u' formula remains unchanged.", 'last displayed definition of v and u-prime', 'math')
variant(83,95,r'E^i\in\Ob\underline{C}_{0X}',r'E^i\in\Ob\underline{C}_{0S}',
 'check/findings/findings_091_095.json#19; review/expose_i/decisions.jsonl',
 'The definition places E in the fiber C_X at its arbitrary object X. Its components therefore belong to C_X and the specified strictly full subcategory is C_(0X). Current changes the printed subscript S to X.', 'Definition2.1 membership condition','math')
new[-1]['scope_end']=r'\sgaStableTarget{sga6.e01.lem.2-1-1}'
variants.extend(new);variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))

path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=[x for x in json.loads(path.read_text()) if x['page']!=94]
for layer,pages in [('current',current),('diplomatic',diplomatic)]:
 for unit in [m.group(0) for m in MATH.finditer(pages[94]) if r'\text{pour }' in m.group(0)]:
  pairs.append(dict(page=94,layer=layer,French_literal_unit=unit,English_literal_unit=unit.replace(r'\text{pour }',r'\text{for }'),expected_multiplicity=1,
   status='confirmed exact lexical translation inside displayed formula; every mathematical token retained',
   scope='Only this complete literal pair, specified form and exact occurrence multiplicity are approved; no page-wide exception.'))
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')

ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 91<=p['page']<=95 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English; printed/current differences independently represented by explicit variants',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(91,96):
 a=chunk.index(f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}')
 b=chunk.index(f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}') if page<95 else len(chunk)
 body=chunk[a:b];counts={}
 for command in (r'\underline{C}',r'\underline{S}',r'\underline{O}'):
  counts[command]=dict(French=current[page].count(command),English=body.count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
for v in new:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
ledger.extend([
 dict(page=92,source_id='reviewed French proof paragraph after octahedron',decision='restore full omitted English clause and literal sequence label',English_anchor=r"\(\Ho^{n+1}(u')=\Ho^{n+1}(u_X)\)",reason='The native English lacked this equality and the explicit reference to sequence(.).'),
 dict(page=93,source_id='review/expose_i/decisions.jsonl; reviewed French Definition1.4.3',decision='n-quasi-isomorphism and n-isomorphism remain plain within individually underlined statement words'),
 dict(page=95,source_id='review/expose_i/decisions.jsonl; reviewed French Definition2.1',decision='strictly and all three defined terms remain plain within the observed underlined statement groups'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_091_095.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
print(json.dumps(dict(passage=record['id'],variants=[v['id'] for v in new],transfer_rows=len(ledger)),ensure_ascii=False))
