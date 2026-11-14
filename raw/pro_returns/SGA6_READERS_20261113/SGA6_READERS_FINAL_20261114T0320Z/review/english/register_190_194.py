#!/usr/bin/env python3
"""Register the end of Exposé II's main text with twelve exact lexical pairs."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P190_194.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('\n\\[\n f_{i_0\\ldots i_p}:',native.index(r'\sgaStableTarget{sga6.e02.lem.2-4-8-1}'))
b=native.index(r'\sgaStableTarget{sga6.e02.appendix-i-a-counterexample-of-verdier}',a)
record=dict(id='EN-EXPOSE-II-190-194',page='190–194',
 place='Intersection inclusions in the proof of3.5.1 through the end of Proposition3.7',layer='both',
 old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/190–194/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl',
 reason='Restores the inline intersection inclusions, full resolutions and spectral-sequence arguments, unprimed source degree terms, exact references and bounds, the original numerical note on191, and the complete unbounded-derived-category adjunction argument. All differing formula units are twelve explicit translations of pour or pour tout; every mathematical character, command, delimiter and space outside those words is retained.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(records) if x['id']==record['id']]
assert len(hits)<=1
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))

current,ref=load_reviewed_pages(194)
diplomatic,dref=load_reviewed_pages(194,'diplomatic')
en=split(chunk)
newpairs=[]
for page in range(190,195):
 assert current[page]==diplomatic[page],(page,'unrecorded French branch difference')
 fu=Counter(m.group() for m in MATH.finditer(current[page]))
 eu=Counter(m.group() for m in MATH.finditer(en[page]))
 missing=fu-eu;extra=eu-fu
 assert sum(missing.values())==sum(extra.values())=={190:3,191:1,192:3,193:5,194:0}[page]
 for f,n in missing.items():
  e=f.replace(r'\text{pour tout }',r'\text{for every }').replace(r'\text{pour }',r'\text{for }')
  assert f!=e and extra[e]==n==1,(page,f,extra)
  newpairs.append(dict(page=page,layer='both',French_literal_unit=f,English_literal_unit=e,
   expected_multiplicity=1,
   status='confirmed exact lexical translation of pour to for or pour tout to for every; all mathematical characters, commands, punctuation, spaces and line breaks retained',
   scope='Only this complete literal mathematical unit and its exact multiplicity in both source forms are approved; no page-wide exception.'))
assert len(newpairs)==12
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=[x for x in json.loads(path.read_text()) if not 190<=x['page']<=194]+newpairs
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')

ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 if not raw.strip():continue
 p=json.loads(raw)
 if not 190<=p['page']<=194:continue
 decision='transferred in faithful English in both source forms'
 if p['source_id']=='fixes/RECONCILE_CODEX_6.json#253':
  decision='current-only deletion of inserted primes brings the French degree terms back to the printed unprimed reading; both English forms consequently use the same exact source resolution and terms, with no artificial variant'
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],
  decision=decision,patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),
  source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for layer,french,reference in [('current',current,ref),('diplomatic',diplomatic,dref)]:
 for page in range(190,195):
  counts={}
  for token in [r'\underline{O}',r'\underline{\underline{R}}',r'\phi',r'\coprod',
                r'\SGAAuthorFootMark{1}',r'\SGAAuthorFootText{1}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',
   decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts,
   reviewed_French_page_sha256=hashlib.sha256(french[page].encode()).hexdigest(),
   English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
ledger.extend([
 dict(page=190,source_id='reviewed proof3.5.1; fixes/RECONCILE_CODEX_6.json#253',decision='Restore the inline intersection inclusions, full T.F.II5.2 citation, bare coproducts and exact terminal baseline point, star abutment, headless comparison, E^bullet resolution and unprimed QE^n/E^n. The withdrawn prime insertion is not reproduced as a diplomatic/current difference.'),
 dict(page=191,source_id='ASTRA-II-UNDERLINE-191; ASTRA-II-NOTES-191',decision='Preserve the J.L.Verdier attribution, complete hypothesis and subcategory clauses, plain numerical reference and item labels, the exact source finite right resolution, and the complete original Tohoku3.6.5/Krull-dimension note with its raised numerical1 in the vanishing display.'),
 dict(page=192,source_id='ASTRA-II-R-192; ASTRA-II-UNDERLINE-192',decision='Keep the actual1°)/2°) case labels, the three separately ruled lexical terms, C^bullet rather than the inherited primed name, all seven double-underlined R letters, both composite isomorphisms and exact N,N-prime bounds. No functor subscript is invented.'),
 dict(page=193,source_id='ASTRA-II-R-193; reviewed cohomological-dimension proof',decision='Restore all three terms of(*), full [H]II7.18 and both parenthetical full-subcategory identifications, every vanishing formula and the printed weak bound at n(U). The seven double-underlined R letters and plain degree-indexed letters retain their separate observed forms.'),
 dict(page=194,source_id='ASTRA-II-R-194; ASTRA-II-PHI-194',decision='Retain [H]I5.3, the complete inline adjunction-functor statement, all five double-underlined R letters, four phi glyphs, headed isomorphism(1), ordinary arrow(2), star spectral-sequence abutment and complete closing proof. The appendix heading remains outside this replacement.'),
])
for pair in newpairs:
 ledger.append(dict(page=pair['page'],source_id='individually checked lexical formula pair',
  decision='only the specified French lexical text is translated; the complete mathematical unit is separately stored',
  French_literal_unit=pair['French_literal_unit'],English_literal_unit=pair['English_literal_unit'],
  expected_multiplicity=1,layer='both'))
(HERE/'EN_EXPOSE_II_TRANSFER_190_194.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv'
notes=[x for x in path.read_text().splitlines() if not x.startswith('191\t')]
notes.append('191\tCohomology-vanishing display in Proposition3.7\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTES-191\tearly reviewer direct scan comparison, main PDF205\tSGAAuthorFootMark{1}; SGAAuthorFootText{1}\tComplete original Tohoku3.6.5 and Krull-dimension qualification.')
path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk))
assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],new_source_variants=0,exact_lexical_pairs=len(newpairs),
 transfer_rows=len(ledger),stable_targets=len(ot)),ensure_ascii=False))
