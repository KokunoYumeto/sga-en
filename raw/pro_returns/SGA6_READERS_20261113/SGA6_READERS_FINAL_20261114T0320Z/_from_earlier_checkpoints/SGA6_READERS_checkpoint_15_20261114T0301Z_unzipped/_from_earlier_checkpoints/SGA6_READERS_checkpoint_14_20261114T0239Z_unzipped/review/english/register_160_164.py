#!/usr/bin/env python3
"""Register the faithful opening of Exposé II against its frozen scan review."""
from pathlib import Path
import hashlib
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH, split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P160_164.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e02.expose}')
b=native.index('whence the first assertion.',a)
record=dict(id='EN-EXPOSE-II-160-164',page='160–164',
 place='ExposéII opening through the final164 isomorphism in the proof of Lemma2.1.2',
 layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/160–164/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl; review/expose_ii/frozen_manifest.tsv',
 reason='Restores the underlined Exposé heading and double-ruled title, source category/site letters, full statement and proof text, D-minus memberships, crossed-loop acyclic superscripts, exact citations, presentation orders p-to-q and I-to-J, the original Ext-star abutment, internal Hom/Ext rules and complete numerical author note164. The two distinct printed/current163 rules are explicitly branched. Plain defined descriptions and plain If on161 remain independent of statement underlining.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl'
rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

variants=[
 dict(id='EN-VAR-111',page=163,old=r'$S$ \uline{is} quasi-compact',
  printed=r'$\underline{S}$ \uline{is} quasi-compact',
  corrected=r'$S$ \uline{is} quasi-compact',mode='text',
  source='ASTRA-II-OBJECT-S-163; review/expose_ii/add_163.py',
  reason='Both scans give the object S a rule in this sentence. The preceding declaration selects S as an object of the underlined site, and each displayed covering arrow S_i to S has that same object as codomain. The identity of this declared object S identifies the two typographical occurrences. Current removes only this isolated object-letter rule; diplomatic preserves it. No object or covering morphism is changed.',
  scope_start=r'\sgaStableTarget{sga6.e02.lem.2-1-1}',
  scope_end=r'\sgaStableTarget{sga6.e02.lem.2-1-2}',
  scan_image='scan/SGA6_scan_360dpi.pdf#page=177; scan/SGA6_witness_300dpi.djvu#page=174',
  scan_region='Lemma2.1.1, quasi-compactness hypothesis'),
 dict(id='EN-VAR-112',page=163,old=r"$\underline{C}'_S$",
  printed=r"$C'_S$",corrected=r"$\underline{C}'_S$",mode='text',
  source='check/findings/findings_161_165.json#9; review/expose_ii/add_163.py',
  reason='The introduced C-prime has no rule in either scan at this occurrence. Its specified inclusion into C_S identifies it with the same category that is individually underlined throughout164, including the domain of Gamma_S and the exact-sequence hypothesis. The identity functor of this explicitly included subcategory gives that identification. Current supplies the rule only here; diplomatic retains the observed plain letter.',
  scope_start=r'\sgaStableTarget{sga6.e02.lem.2-1-2}',
  scope_end='%%%%%%%%%%  scan idx 177  |  folio 164',
  scan_image='scan/SGA6_scan_360dpi.pdf#page=177; scan/SGA6_witness_300dpi.djvu#page=174',
  scan_region='Lemma2.1.2, introduced full subcategory')
]
path=HERE/'EN_VARIANTS.jsonl'
old=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants}
old=[v for v in old if v['id'] not in ids]+variants
old.sort(key=lambda v:int(v['id'].rsplit('-',1)[1]))
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in old))

fr,ref=load_reviewed_pages(164)
df,dref=load_reviewed_pages(164,'diplomatic')
en=split(chunk)
funit=next(m.group(0) for m in MATH.finditer(fr[164]) if r'\text{\uline{pour tout} }' in m.group(0))
eunit=funit.replace(r'\text{\uline{pour tout} }',r'\text{\uline{for every} }')
assert eunit in en[164]
pair=dict(page=164,layer='both',French_literal_unit=funit,English_literal_unit=eunit,
 expected_multiplicity=1,status='confirmed exact lexical translation of the inspected underlined pour tout to for every; all mathematical characters, punctuation, spaces and line breaks retained',
 scope='Only this complete literal displayed formula pair and exact multiplicity are approved.')
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=json.loads(path.read_text())
pairs=[p for p in pairs if not (p['page']==164 and p['French_literal_unit']==funit)]+[pair]
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')

ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if not 160<=p['page']<=164:continue
 decision='transferred in faithful English with explicit variants for the two163 source rules'
 if p['source_id']=='check/findings/findings_161_165.json#3':
  decision='English unchanged: both un suite exacte and corrected une suite exacte render an exact sequence; no artificial English grammar variant'
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],
  decision=decision,patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),
  source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))

for layer,reading,reference,french in [('current','corrected',ref,fr),('diplomatic','printed',dref,df)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a)
  section=text[a:b]
  assert section.count(v['old'])==1
  text=text[:a]+section.replace(v['old'],v[reading])+text[b:]
 pages=split(text)
 for page in range(160,165):
  counts={}
  for token in [r'\underline{C}',r'\underline{S}',r'\underline{\Hom}',r'\underline{\Ext}',
                r'\varnothing',r'\mathrm D^{-}',r'\Ext^{*}',r'\SGAAuthorFootnote{1}']:
   counts[token]=dict(French=french[page].count(token),English=pages[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',
   decision='literal command multiplicities agree in each materialized source branch',
   source=reference['bases'][page-1],counts=counts))

ledger.extend([
 dict(page=160,source_id='ASTRA-II-UNDERLINE-160; ASTRA-II-UNDERLINE-161',
  decision='The continuous acyclic-complexes phrase is translated across the original160/161 boundary without splitting the English word',
  French_boundary='formée des com- | plexes acycliques',English_boundary='formed by | acyclic complexes',
  reason='The same phrase and all its symbols remain within the same statement; the marker locates the paragraph passage rather than asserting a word-for-word bilingual boundary.'),
 dict(page=161,source_id='ASTRA-II-UNDERLINE-161; ASTRA-II-UNDERLINE-162',
  decision='The split source hypo- | thèses is rendered make the | hypotheses across161/162; source hypothesis(ii) in its resp. case retained. Plain If at the start of the161 continuation remains plain.'),
 dict(page=160,source_id='reviewed Proposition1.1',decision='Restore I2.3 for pseudo-coherence, D-minus in partc and each varnothing acyclic-category superscript; the unqualified native delta and omitted minus have no source basis.'),
 dict(page=163,source_id='check/findings/findings_161_165.json#8; ASTRA-II-UNDERLINE-163',
  decision='No comma after EGA0_I; quasi-compact and generated by its sections remain plain inside the otherwise underlined statement. The c)/d) paragraph division is retained.'),
 dict(page=164,source_id='reviewed Lemma2.1.2',decision='Retain the exact finite presentation A_S^p→A_S^q→F and arbitrary presentation A_S^(I)→A_S^(J)→F; restore each complete Gamma_S source/target occurrence, C-prime exact-sequence category, I1.2 reference, literal Ext-star spectral-sequence target and independent Hom/Ext rules.'),
 dict(page=164,source_id='ASTRA-II-NOTE-164',decision='Restore the entire original numerical1 author note and both sources SGA4VI1.2 and T.FII3.10.1. Source lowercase opening is retained in English; the note is outside the statement underline.'),
])
for v in variants:
 ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',
                    English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
manifest=ROOT/'review/expose_ii/frozen_manifest.tsv'
ledger.append(dict(page=164,source_id='review/expose_ii/frozen_manifest.tsv',
 decision='Frozen French ExposéII handoff used without replaying old incremental scripts',
 manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest()))
(HERE/'EN_EXPOSE_II_TRANSFER_160_164.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))

path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv'
notes=[x for x in path.read_text().splitlines() if not x.startswith('164\t')]
notes.append('164\tLemma2.1.2(b)(ii), after filtered inductive limits\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTE-164\tearly reviewer direct scan comparison, main PDF178 and witness175\tSGAAuthorFootnote{1}\tComplete original note and citations restored.')
path.write_text('\n'.join(notes)+'\n')
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),transfer_rows=len(ledger),
 stable_targets=len(old_targets),French_frozen_manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest()),ensure_ascii=False))
