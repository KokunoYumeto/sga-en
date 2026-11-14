#!/usr/bin/env python3
"""Register the exact 131–135 translation and its one printed citation variant."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P131_135.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('in the case of the category of modules of a ringed topos',native.index(r'\sgaStableTarget{sga6.e01.para.5-0}'))
b=native.index('Here is now a particular case of',a)
record=dict(id='EN-EXPOSE-I-131-135',page='131–135',place='Exposé I5.0 continuation through Lemma5.8.2 proof',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/131–135/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Fresh faithful translation restores the exact source triangle and baseline functor-slot point131, both different bounds m≤n and m<n, underlined H, original site/category and left/right module notation, full SGA4 appendix reference, double-struck derived operators, plain defined flat-amplitude phrase, original numbered author notes134/135 and complete tensor–Hom formulas. The sole printed/current citation difference is explicitly branched.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(135)
diplomatic,dref=load_reviewed_pages(135,'diplomatic')
en=split(chunk)
assert en[135].count('(2.15)')==1
new=dict(id='EN-VAR-105',page=135,old='(2.15)',printed='(2,15)',corrected='(2.15)',mode='text',
 source='fixes/MISPRINTS_6.json#136; check/findings/findings_131_135.json#31',
 reason='The printed reference has a comma. Paragraph 2.15 defines the pseudo-coherence of Modules used in this corollary. Diplomatic preserves the observed comma; current uses the paragraph number 2.15.',
 scope_start='%%%%%%%%%%  scan idx 148  |  folio 135',scope_end=r'\sgaStableTarget{sga6.e01.lem.5-8-2}',
 scan_image='scan/SGA6_scan_360dpi.pdf#page=149; scan/SGA6_witness_300dpi.djvu#page=146',scan_region='Corollary 5.8.1, pseudo-coherence reference')
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if x['id']!=new['id']];variants.append(new)
variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))
ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 131<=p['page']<=135 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English; every printed/current difference is explicitly branched',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(131,136):
 counts={}
 for command in (r'\underline{S}',r'\underline{\Ho}',r'\underline{\Hom}',r'\mathbb L',r'\mathbb R',r'\mathrm L',r'\mathbb Z_S'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
ledger.append(dict(page=135,source_id=new['source'],decision='explicit English printed/corrected variant',English_variant=new['id'],printed=new['printed'],corrected=new['corrected']))
ledger.extend([
 dict(page=131,source_id='ASTRA-I-BOUND-131',decision='m≤n retained in the proposition in both forms; later proof parenthetical m<n remains strict',reason='The coordinator re-viewed both native scans and distinguished the two source glyphs. The rejected checker reading m<n at the first occurrence is not transferred.'),
 dict(page=131,source_id='ASTRA-I-DOT-131; reviewed source Lemma5.1.1',decision='baseline period retained in the tensor functor slot; the actual triangle orientation and +1 label are copied without rotating the source diagram'),
 dict(page=132,source_id='ASTRA-I-TERMS-132; ASTRA-I-SITE-132',decision='defined flat amplitude remains plain; the exact right-module source, left-module source and Z-sheaf target of the tensor functor are restored'),
 dict(page=133,source_id='reviewed source5.6',decision='full reference SGA4 IV App. II retained; no omitted appendix numeral'),
 dict(page=133,source_id='reviewed source133–134 boundary',decision='continuous phrase crosses the printed-page marker with English adjective order',French_boundary='amplitude | plate',English_boundary='flat | amplitude',reason='Both lexical elements and the continuous parenthetical sentence are preserved. The marker records the source folio boundary, without claiming a word-for-word bilingual page split.'),
 dict(page=134,source_id='ASTRA-I-NOTE-134',decision='numeric label1 and its repeated call restored explicitly, with one footnote text giving the final object of the underlined topos'),
 dict(page=134,source_id='ASTRA-I-SITE-134; ASTRA-I-TERMS-134',decision='plain final-object S in all exercise categories and Hom-functor arguments retained; derived R is double-struck and the internal Hom rule independent'),
 dict(page=135,source_id='ASTRA-I-NOTE-135',decision='numeric label1 sits in the starred display before its terminal period; full author note is outside the display via the split Mark/Text helpers'),
 dict(page=135,source_id='reviewed source Lemma5.8.2',decision='every Hom underline, tensor base, ordered argument, equation tag and module side retained in all four displayed formulas; the original reference to Cartan is preserved'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_131_135.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith(('134\t','135\t'))]
notes.extend([
 '134\tExercises5.7(a) and repeated call5.7(b)\traised numerical1 inside baseline parentheses\t2\tASTRA-I-NOTE-134\tcoordinator direct scan comparison, main PDF148 and witness145\tSGAAuthorFootnote{1}; SGAAuthorFootMark{1}\tOne original note text and both explicit calls; the final-object S remains plain.',
 '135\tLemma5.8.2 proof, display(*) after G before period\traised numerical1 inside baseline parentheses\t1\tASTRA-I-NOTE-135\tcoordinator direct scan comparison, main PDF149 and witness146\tSGAAuthorFootMark{1}; SGAAuthorFootText{1}\tFull final-object and constant-sheaf explanation outside the equation.'
])
path.write_text('\n'.join(notes)+'\n')
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[new['id']],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
