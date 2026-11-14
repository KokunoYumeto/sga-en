#!/usr/bin/env python3
"""Register duality and trace text151–155 with observed local glyph choices."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P151_155.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\emph{Proof.} Define the arrow by resolving',native.index(r'\sgaStableTarget{sga6.e01.prop.7-2}'))
b=native.index('One may interpret',native.index(r'\sgaStableTarget{sga6.e01.para.8-2}',a))
record=dict(id='EN-EXPOSE-I-151-155',page='151–155',place='Exposé I7.2 proof through8.2 opening data',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/151–155/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Exact reconstruction restores the empty Hom argument, both forms of the parf index, three distinct Cartan Hom rule patterns with source plain R, all three derived tensor products in7.4, the contrast of ordinary statement R and double-struck proof R in7.6, three headless isomorphisms, original raised-star author footnote, every bare sum, the coproduct over i and sum over j, underlined cohomology H, plain tensor in8.1.2, and gamma in8.2. Both reviewed French layers agree on this packet; no additional English variant is introduced.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(155)
diplomatic,dref=load_reviewed_pages(155,'diplomatic')
en=split(chunk)
for page in range(151,156):assert current[page]==diplomatic[page],page
ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 151<=p['page']<=155 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in both English forms; reviewed French layers agree exactly on this packet',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(151,156):
 counts={}
 for command in (r'\underline{S}',r'\underline{\mathrm{parf}}',r'\underline{\Hom}',r'\mathrm R',r'\mathbb{R}',r'\RHom',r'\otL',r'\otimes',r'\underline{H}',r'\gamma'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
ledger.extend([
 dict(page=151,source_id='check/findings/findings_151_155.json#4/#5',decision='empty first Hom argument retained as source quad; no added point or dash; first parf index plain and second underlined'),
 dict(page=151,source_id='check/findings/findings_151_155.json#7/#8/#9',decision='Cartan three-row display copied literally:3 Hom rules in first row, only the innermost rule in rows2 and3, all source R letters plain, all three source tensor products derived'),
 dict(page=152,source_id='check/findings/findings_151_155.json#12/#14',decision='no extra full stop after Lemma7.5 target F or before the comma in Proposition7.6 opening data'),
 dict(page=152,source_id='check/findings/findings_151_155.json#19/#21/#22',decision='statement R letters plain, proof R double-struck; source tensor functor has no added leading placeholder'),
 dict(page=153,source_id='ASTRA-I-TERMS-153; check/findings/findings_151_155.json#39/#40/#41',decision='quoted punctuation, i.e., references and final parentheses remain outside prose rules; all three aligned isomorphism signs stay headless'),
 dict(page=154,source_id='ASTRA-I-NOTE-154',decision='full author note restored to the footnote layer with the observed raisedstar label before the final stop; native English had moved its content into the body'),
 dict(page=154,source_id='ASTRA-I-SITE-154; check/findings/findings_151_155.json#46/#47',decision='only site U-in-ob-S is ruled; baseline point in H^0(U,.) retained; outer H and global Hom_D(U) remain plain'),
 dict(page=155,source_id='check/findings/findings_151_155.json#49/#50/#51/#54/#55',decision='five bare sums retained without inherited added indices; the separate coproduct_i sum_j expression is copied exactly'),
 dict(page=155,source_id='check/findings/findings_151_155.json#52/#53/#57',decision='cohomology H retains its observed rule; evaluation tensor retains no L superscript; source gamma replaces inherited English chi in both forms, with the same source and target'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_151_155.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('154\t')]
notes.append('154\tTrace homomorphism definition8.1, before final stop\traised star inside baseline parentheses\t1\tASTRA-I-NOTE-154\tcoordinator direct scan comparison, main PDF168 and witness165\tSGAAuthorFootnote{raisedstar}\tFull finite-tor-dimension caveat and reference8.5 restored as an original author footnote.')
path.write_text('\n'.join(notes)+'\n')
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
