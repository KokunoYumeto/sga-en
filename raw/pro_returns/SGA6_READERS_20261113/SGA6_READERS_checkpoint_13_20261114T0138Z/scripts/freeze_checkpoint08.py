#!/usr/bin/env python3
"""Freeze the explicitly agreed checkpoint08 scope without changing live review."""
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT.parent/'sga6_checkpoint08_stage'
assert not STAGE.exists(),'The checkpoint08 stage already exists.'
STAGE.mkdir()
ignore=shutil.ignore_patterns('__pycache__','images','rendered','build','*.png','*.ppm','*.jpg','*.pyc','*.log','*.aux','*.out','*.toc')
for name in ['fr','en','check','fixes','conventions','scan']:
 (STAGE/name).symlink_to(ROOT/name,target_is_directory=True)
for name in ['scripts','records']:
 shutil.copytree(ROOT/name,STAGE/name,ignore=ignore)
(STAGE/'review').mkdir();(STAGE/'build').mkdir();(STAGE/'readers/fr').mkdir(parents=True)
for name in ['apt','texlive','texmf-var','texmf-config','page_packets','registry.json']:
 (STAGE/'build'/name).symlink_to(ROOT/'build'/name,target_is_directory=(ROOT/'build'/name).is_dir())
include=['backmatter','early','expose_i','expose_ii','expose_ii_amendments','expose_iii','expose_iv','expose_v','expose_v_rendering','expose_vi','expose_vii','expose_x','expose_x_supplement','expose_xii','front','late','middle','xiii']
for name in include:
 source=ROOT/'review'/name
 if name=='expose_v':source=ROOT/'build/review_snapshots/expose_v_checkpoint08_through328'
 shutil.copytree(source,STAGE/'review'/name,ignore=ignore)
for path in (ROOT/'review').iterdir():
 if path.is_file():shutil.copy2(path,STAGE/'review'/path.name)
english=ROOT.parent/'sga6_checkpoint08_english240_stage/review/english'
assert english.is_dir()
shutil.copytree(english,STAGE/'review/english',ignore=ignore)
handoff=json.loads((english/'EN_FROZEN240_HANDOFF.json').read_text())
bad=[]
for row in handoff['required_external_inputs']:
 p=STAGE/row['path']
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:bad.append(row['path'])
assert not bad,bad
vi=[json.loads(s) for s in (STAGE/'review/expose_vi/page_status.jsonl').read_text().splitlines() if s]
assert {r['page'] for r in vi}==set(range(365,406))
vii=[json.loads(s) for s in (STAGE/'review/expose_vii/page_status.jsonl').read_text().splitlines() if s]
assert {r['page'] for r in vii}==set(range(416,466))
freeze={
 'checkpoint':8,'state':'Frozen inputs; French regeneration and selected output verification pending.',
 'boundaries':{'expose_0':[1,77],'expose_i':[78,159],'expose_ii':[160,221],'expose_iii':[222,273],'expose_iv':[274,296],'expose_v':[297,328],'expose_vi':[365,405],'expose_vii':[416,465],'expose_x':[519,594],'expose_x_partial':[549],'expose_xii':[595,615],'expose_xiii':[616,666],'expose_xiv_indices':[667,700],'english':[1,240]},
 'exclude_new_work':['ExposéV329 onward','ExposéVI406 onward apart from explicitly read nominal405 source aliases','ExposéVIII466 onward','English241 onward'],
 'english_external_inputs_verified':len(handoff['required_external_inputs']),
 'reviewed_not_finished':'The remaining source review, English transfer, final notation audit and final readable apparatus are unfinished. ExposéXI has no printed body; the contents mark it Non rédigé.'}
(STAGE/'records/CHECKPOINT08_FREEZE.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'stage':STAGE.name,'review_directories':len(include)+1,'VI_full_pages':len(vi),'VII_full_pages':len(vii),'English_external_inputs_verified':len(handoff['required_external_inputs'])}))
