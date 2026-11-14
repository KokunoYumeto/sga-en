#!/usr/bin/env python3
"""Finish Exposé I with the source trace square and complete bibliography."""
from pathlib import Path
import hashlib
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH,split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P156_159.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('One may interpret',native.index(r'\sgaStableTarget{sga6.e01.para.8-2}'))
b=native.index(r'\sgaStableTarget{sga6.e02.expose}',a)
record=dict(id='EN-EXPOSE-I-156-159',page='156–159',place='Exposé I8.2 continuation through bibliography and following macro-state declarations',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/156–159/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Faithful completion restores the original author footnote, source linear map from the tensor product, plain construction E(C), underlined categorical A, exact source/target parf rules in the extension of trace, every source diagram label and the complete eight-entry bibliography with MULT and historical publication wording. The omitted L on the square left edge is explicitly branched with the contraction morphism that justifies it. The exact27 ordered source macro declarations after159 are retained.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(159)
diplomatic,dref=load_reviewed_pages(159,'diplomatic')
en=split(chunk)
diagrams=[m.group(0) for m in MATH.finditer(en[157]) if '\\begin{tikzcd}[column sep=\nlarge' in m.group(0)]
assert len(diagrams)==1
diagram=diagrams[0]
old_arrow=r'''\arrow[d,"\Id\otL\tau_F"']'''
printed_arrow=r'''\arrow[d,"\Id\otimes\tau_F"']'''
assert diagram.count(old_arrow)==1
new=dict(id='EN-VAR-110',page=157,old=diagram,printed=diagram.replace(old_arrow,printed_arrow),corrected=diagram,mode='display',
 source='check/findings/findings_156_160.json#12; review/expose_i/add_156_159.py',
 reason='The square left edge lacks the L that is printed on the same contraction in the parallel triangle. Its map is beta=id_(E-dual) tensor^L (ev_F composed with c_(F,F-dual)) tensor^L id_E, from E-dual tensor^L F tensor^L F-dual tensor^L E to E-dual tensor^L E. Here c exchanges the middle factors, ev_F:F-dual tensor^L F to A is the evaluation used in8.1, and the unit isomorphisms remove the A factor. Current restores the omitted derived-tensor exponent; diplomatic retains the ordinary tensor label. All other source cells, labels and arrows are identical.',
 scope_start='%%%%%%%%%%  scan idx 170  |  folio 157',scope_end='%%%%%%%%%%  scan idx 171  |  folio 158',
 scan_image='scan/SGA6_scan_360dpi.pdf#page=171; scan/SGA6_witness_300dpi.djvu#page=168',scan_region='Proof8.3, square left edge')
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if x['id']!=new['id']];variants.append(new)
variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))
ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 156<=p['page']<=159 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English; the one printed/current mathematical difference is explicitly branched',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(156,160):
 counts={}
 for command in (r'\underline{S}',r'\underline{C}',r'\underline A',r'\underline{\parf}',r'\mathbb{R}',r'\underline{\Hom}',r'\otL',r'\otimes',r'\gamma'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
ledger.append(dict(page=157,source_id=new['source'],decision='explicit English printed/corrected variant',English_variant=new['id'],printed=new['printed'],corrected=new['corrected']))
macro_pattern=r'^\\(?:providecommand|renewcommand)\{[^\n]+'
frmacros=re.findall(macro_pattern,current[159],re.M);enmacros=re.findall(macro_pattern,en[159],re.M)
assert len(frmacros)==27 and frmacros==enmacros,(len(frmacros),len(enmacros))
ledger.extend([
 dict(page=156,source_id='reviewed source8.2',decision='the stated H^0(U,A)-linear map from the tensor product is retained',formula='u tensor v ↦ gamma composed with (u tensor^L v)',reason='This is the explicitly displayed linear map. Its values on simple tensors give the preceding pairing; no unproved change of its source is made.'),
 dict(page=156,source_id='ASTRA-I-NOTE-156',decision='raisedstar call before the stop; lowercase-opening note has no added final stop; native body prose returned to the author-note layer'),
 dict(page=157,source_id='check/findings/findings_156_160.json#8/#9/#10/#11',decision='both complete triangles occur after the157marker; their L exponents and the square top L remain in both forms; source label order retained'),
 dict(page=157,source_id='check/findings/findings_156_160.json#14/#15/#19/#21',decision='all construction E letters are plain typed E; no inherited script E; exact underlined/ordinary parf index difference retained'),
 dict(page=157,source_id='reviewed source157–158 boundary',decision='continuous phrase crosses the marker in English adjective order',French_boundary='homomorphisme | trace',English_boundary='trace | homomorphism',reason='Both lexical elements remain in the same continuous sentence; the source-page marker does not claim a word-for-word bilingual split.'),
 dict(page=158,source_id='check/findings/findings_156_160.json#22/#23/#24',decision='continued extension target is underlined A; plain parf in its source; both Parf operators remain plain, all four site S and both C_0 letters have source rules'),
 dict(page=159,source_id='check/findings/findings_156_160.json#25/#27/#28/#29/#30/#31/#32/#33/#34',decision='all eight bibliography entries retained in source order; titles plain, exact initials J-L., abbreviated publisher North Holl. Pub. Comp., key MULT, and historical to-appear/in-preparation statements preserved',English_translation_scope='Only connecting French words are translated; bibliographic titles and historical data remain as supplied and scan-confirmed.'),
 dict(page=159,source_id='reviewed source159 unprinted notation block',decision='all27 macro definitions copied in original order',ordered_macro_definitions=frmacros,ordered_block_sha256=hashlib.sha256('\n'.join(frmacros).encode()).hexdigest()),
])
(HERE/'EN_EXPOSE_I_TRANSFER_156_159.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('156\t')]
notes.append('156\tCup-product definition8.2, before final stop\traised star inside baseline parentheses\t1\tASTRA-I-NOTE-156\tcoordinator direct scan comparison, main PDF170 and witness167\tSGAAuthorFootnote{raisedstar}\tLowercase opening and no added final stop in the complete author note.')
path.write_text('\n'.join(notes)+'\n')
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[new['id']],transfer_rows=len(ledger),stable_targets=len(old_targets),ordered_macro_definitions=len(frmacros)),ensure_ascii=False))
