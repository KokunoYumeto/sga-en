#!/usr/bin/env python3
"""Register rank and duality passages146–150 with exact source macro state."""
from pathlib import Path
import hashlib
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH,split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P146_150.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('(the two on the left being homomorphisms of presheaves of rings)',native.index(r'\sgaStableTarget{sga6.e01.para.6-9}'))
b=native.index(r'\emph{Proof.} Define the arrow by resolving',a)
record=dict(id='EN-EXPOSE-I-146-150',page='146–150',place='Exposé I6.9 continuation through Proposition7.2 statement',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/146–150/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Complete reconstruction restores the underlined locally constant rank parameter, exact category C_0 in the6.14 proof, all operator/site rules and plain final-object S, exact D(S) domain7.1, the full spectral sequence and its Ext coproduct omitted from native English, and the headless duality sign. All36 ordered macro definitions after146 are copied from the reviewed French. No printed/current mathematical difference exists in this packet; both layers use the same passage, with two exact lexical si/if display pairs.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(150)
diplomatic,dref=load_reviewed_pages(150,'diplomatic')
en=split(chunk)
for page in range(146,151):assert current[page]==diplomatic[page],page
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=[x for x in json.loads(path.read_text()) if x['page']!=146]
units=[m.group(0) for m in MATH.finditer(current[146]) if r'\text{si }' in m.group(0)]
assert len(units)==2
for unit in units:
 translated=unit.replace(r'\text{si }',r'\text{if }')
 assert en[146].count(translated)==1
 pairs.append(dict(page=146,layer='both',French_literal_unit=unit,English_literal_unit=translated,expected_multiplicity=1,
  status='confirmed exact lexical si-to-if translation in the rank definition; all mathematical tokens, punctuation and spacing retained',
  scope='Only this complete literal formula pair and exact multiplicity are approved.'))
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 146<=p['page']<=150 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in both English forms; reviewed French layers agree exactly on this packet',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(146,151):
 counts={}
 for command in (r'\underline{S}',r'\underline{C}',r'\underline n',r'\underline{\Parf}',r'\underline{\Hom}',r'\underline{\Ho}',r'\underline{\Ext}',r'\mathbb L',r'\mathbb{L}',r'\mathbb{R}'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
macro_pattern=r'^\\(?:providecommand|renewcommand)\{[^\n]+'
frmacros=re.findall(macro_pattern,current[146],re.M);enmacros=re.findall(macro_pattern,en[146],re.M)
assert len(frmacros)==36 and frmacros==enmacros,(len(frmacros),len(enmacros))
ledger.extend([
 dict(page=146,source_id='reviewed source146 unprinted notation blocks',decision='all36 macro definitions copied in original order',ordered_macro_definitions=frmacros,ordered_block_sha256=hashlib.sha256('\n'.join(frmacros).encode()).hexdigest(),reason='This preserves actual Ob and Im renewals and providecommand semantics. The unprinted macro definitions are excluded from source-glyph assertions.'),
 dict(page=146,source_id='ASTRA-I-TERMS-146; check/findings/findings_146_150.json#2/#4/#5/#6',decision='defined rank and rg remain plain; the second we-have phrase remains plain; L on u-star is double-struck and L on tensor plain; final colon and stop lie outside the prose rule'),
 dict(page=147,source_id='reviewed source6.13; check/findings/findings_146_150.json#8',decision='every locally constant n keeps its independent rule; integer n stays plain; source A_X^n has no added direct-sum sign, general L tensor has no added base A; original .). punctuation and continuous paragraph retained'),
 dict(page=148,source_id='reviewed source proof6.14',decision='all four exact category C_0 occurrences restored from French in both forms, replacing the inherited English C_1 occurrences; composition remains literal juxtaposition'),
 dict(page=148,source_id='ASTRA-I-SITE-148; ASTRA-I-PARF-148',decision='plain final-object S retained; only the second Parf on this page is ruled; Proposition7.1 begins E in D(S)_parf with no inherited minus superscript added'),
 dict(page=149,source_id='check/findings/findings_146_150.json#18/#19/#20/#21/#25/#26/#27',decision='entire7.1(b) prose is plain; all exact bounds and unruled outer H are retained; full E_2^{pq} spectral sequence, Ext coproduct indexed i_2-i_1=i and vanishing statement are restored without shortening the proof'),
 dict(page=150,source_id='check/findings/findings_146_150.json#30/#43',decision='headed top isomorphism and headless duality isomorphism retain their distinct observed strokes; all arguments, double-struck derived letters and operator rules copied exactly'),
 dict(page=150,source_id='ASTRA-I-SITE-150; check/findings/findings_146_150.json#47',decision='only the two base-site S letters are ruled; the final and before F=A remains plain'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_146_150.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[],transfer_rows=len(ledger),stable_targets=len(old_targets),ordered_macro_definitions=len(frmacros)),ensure_ascii=False))
