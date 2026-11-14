#!/usr/bin/env python3
"""Check literal math in both English source branches against reviewed French IV.

This checks exact TeX units, not mathematical equivalence or translation quality.
Prose transfers remain separately described in the manually prepared ledgers.
"""
from pathlib import Path
from collections import Counter
import difflib
import hashlib
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH, split, tsv

HERE=Path(__file__).resolve().parent
paths=sorted(HERE.glob('EN_EXPOSE_IV_P*.tex'))
assert paths
source=''.join(p.read_text() for p in paths)
last=max(split(source))
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[v for v in variants if 274<=v['page']<=last]
pairs=json.loads((HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json').read_text())
counts=[];differences=[];source_states={};branch_hashes={}
for layer,reading in [('current','corrected'),('diplomatic','printed')]:
 text=source
 for v in variants:
  a=text.index(v['scope_start'])
  b=text.index(v['scope_end'],a) if v.get('scope_end') else len(text)
  section=text[a:b]
  assert section.count(v['old'])==1,(layer,v['id'],section.count(v['old']))
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 branch_hashes[layer]=hashlib.sha256(text.encode()).hexdigest()
 en=split(text);fr,reference=load_reviewed_pages(last,layer)
 source_states[layer]=dict(bases=[x for x in reference['bases'] if x['page']>=274],
  applied_patches=[x for x in reference['applied_patches'] if x['page']>=274],
  baseline_differences=[x for x in reference['baseline_differences'] if x['page']>=274])
 for page in range(274,last+1):
  fu=Counter(m.group(0) for m in MATH.finditer(fr[page]));eu=Counter(m.group(0) for m in MATH.finditer(en[page]))
  missing=fu-eu;extra=eu-fu;approved={}
  for pair in pairs:
   if pair['page']!=page or pair.get('layer','both') not in (layer,'both'):continue
   f=pair['French_literal_unit'];e=pair['English_literal_unit'];n=pair['expected_multiplicity']
   if missing[f]==extra[e]==n:
    approved[('French',f)]=pair['status'];approved[('English',e)]=pair['status']
  for side,units in [('French',missing),('English',extra)]:
   for unit in units.elements():differences.append(dict(layer=layer,page=page,side=side,literal_unit=unit,status=approved.get((side,unit),'unreviewed literal difference')))
  counts.append(dict(layer=layer,page=page,French_math_units=sum(fu.values()),English_math_units=sum(eu.values()),
   unmatched_French_units=sum(missing.values()),unmatched_English_units=sum(extra.values()),
   English_variant_ids='; '.join(v['id'] for v in variants if v['page']==page)))
tsv(f'EN_EXPOSE_IV_FORM_MATH_COUNTS_274_{last:03}.tsv',list(counts[0]),counts)
tsv(f'EN_EXPOSE_IV_FORM_LITERAL_DIFFERENCES_274_{last:03}.tsv',['layer','page','side','literal_unit','status'],differences)
summary=dict(scope=f'printed274–{last}',literal_math_comparison='complete formula TeX units as multisets; no character, command or whitespace normalization',
 source_chunk_sha256s={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
 materialized_branch_sha256s=branch_hashes,variants=[v['id'] for v in variants],source_states=source_states,
 unexpected_difference_units=sum(d['status']=='unreviewed literal difference' for d in differences),
 approved_lexical_difference_side_units=len(differences),
 limitation='This exact source-form check does not establish full prose fidelity, mathematical correctness, PDF typography or completeness outside the stated interval.')
(HERE/f'EN_EXPOSE_IV_FORM_VERIFICATION_274_{last:03}.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['scope','unexpected_difference_units','approved_lexical_difference_side_units']},ensure_ascii=False))
for d in differences:
 if d['status']=='unreviewed literal difference':print(json.dumps(d,ensure_ascii=False))
if summary['unexpected_difference_units']:raise SystemExit(2)
