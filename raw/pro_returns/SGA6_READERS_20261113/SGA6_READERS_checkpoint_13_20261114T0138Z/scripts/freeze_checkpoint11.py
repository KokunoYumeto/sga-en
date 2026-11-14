#!/usr/bin/env python3
"""Freeze completed V, all numbered French folios, and sealed English contributions."""
import argparse,hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--english',type=Path,required=True);args=parser.parse_args()
STAGE=ROOT.parent/'sga6_checkpoint11_stage'
assert not STAGE.exists(),'The checkpoint11 stage already exists.'
english=args.english.resolve();assert (english/'EN_FROZEN296_HANDOFF.json').is_file()
STAGE.mkdir()
ignore=shutil.ignore_patterns('__pycache__','images','rendered','build','*.png','*.ppm','*.jpg','*.pyc','*.log','*.aux','*.out','*.toc')
for name in ['fr','en','check','fixes','conventions','scan']:
 (STAGE/name).symlink_to(ROOT/name,target_is_directory=True)
for name in ['scripts','records']:
 shutil.copytree(ROOT/name,STAGE/name,ignore=ignore)
(STAGE/'review').mkdir();(STAGE/'build').mkdir();(STAGE/'readers/fr').mkdir(parents=True)
for name in ['apt','texlive','texmf-var','texmf-config','page_packets','registry.json']:
 (STAGE/'build'/name).symlink_to(ROOT/'build'/name,target_is_directory=(ROOT/'build'/name).is_dir())
include=['backmatter','early','expose_i','expose_ii','expose_ii_amendments','expose_iii','expose_iv','expose_iv_amendments','expose_v','expose_v_rendering','expose_vi','expose_vii','expose_vii_amendments','expose_viii','expose_ix','expose_x','expose_x_amendments','expose_x_supplement','expose_xii','expose_xiv_amendments','front','front_amendments','late','middle','xiii']
snapshots={'expose_v':'expose_v_checkpoint11_completed_364'}
for name in include:
 source=ROOT/'build/review_snapshots'/snapshots[name] if name in snapshots else ROOT/'review'/name
 shutil.copytree(source,STAGE/'review'/name,ignore=ignore)
for path in (ROOT/'review').iterdir():
 if path.is_file():shutil.copy2(path,STAGE/'review'/path.name)
shutil.copytree(english,STAGE/'review/english',ignore=ignore)
(STAGE/'review/english').chmod(0o755)  # New staging copy; the sealed source stays read-only.
# Preserve the separately sealed later English exposés without counting them
# as part of the contiguous1–296 aggregate.
parallel=[]
for name in ['viii466_497','ix498_518','x519_594']:
 source=ROOT/'review/english/contributions/exposes_viii_x/snapshots'/name
 destination=STAGE/'review/english/contributions/exposes_viii_x/snapshots'/name
 destination.parent.mkdir(parents=True,exist_ok=True)
 shutil.copytree(source,destination,ignore=ignore)
 parallel.append(destination.relative_to(STAGE).as_posix())

source=ROOT/'build/review_snapshots/english_vii_complete416_465'
destination=STAGE/'review/english/contributions/expose_vii/snapshots/vii416_465'
destination.parent.mkdir(parents=True,exist_ok=True)
shutil.copytree(source,destination,ignore=ignore)
parallel.append(destination.relative_to(STAGE).as_posix())

source=ROOT/'build/review_snapshots/english_xii_complete595_615'
destination=STAGE/'review/english/contributions/exposes_xii_xiv/snapshots/xii595_615'
destination.parent.mkdir(parents=True,exist_ok=True)
shutil.copytree(source,destination,ignore=ignore)
parallel.append(destination.relative_to(STAGE).as_posix())

handoff=json.loads((english/'EN_FROZEN296_HANDOFF.json').read_text());bad=[]
for row in handoff['required_external_inputs']:
 p=STAGE/row['path']
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:bad.append(row['path'])
assert not bad,bad
counts={}
for name,a,b in [('expose_v',297,364),('expose_vi',365,415),('expose_vii',416,465),('expose_viii',466,497),('expose_ix',498,518)]:
 rows=[json.loads(s) for s in (STAGE/f'review/{name}/page_status.jsonl').read_text().splitlines() if s]
 assert {r['page'] for r in rows}==set(range(a,b+1)),name
 assert all(r.get('fully_checked',r.get('checked_against_scan',False)) is True for r in rows),name
 counts[name]=len(rows)
freeze={
 'checkpoint':11,'state':'Frozen inputs; French regeneration and selected output verification pending.',
 'boundaries':{'expose_0':[1,77],'expose_i':[78,159],'expose_ii':[160,221],'expose_iii':[222,273],'expose_iv':[274,296],'expose_v':[297,364],'expose_vi':[365,415],'expose_vii':[416,465],'expose_viii':[466,497],'expose_ix':[498,518],'expose_x':[519,594],'expose_xii':[595,615],'expose_xiii':[616,666],'expose_xiv_indices':[667,700],'english':[1,296]},
 'exclude_new_work':['English297 onward in the contiguous aggregate; only the explicitly sealed contribution snapshots are included separately'],
 'english_external_inputs_verified':len(handoff['required_external_inputs']),
 'separate_sealed_english_contributions':parallel,
 'completed_at_this_checkpoint':'Exposé V297–364 is complete and sealed. The clipped X549 notation is explicitly reconstructed with exact class/rank maps; X566 punctuation and X580 locator amendments are included. VII430 and XIV author-note label transports and the front catalogue volume6 transcription correction are included. English1–296 is unchanged; complete English VIII, IX and XII contributions are separately sealed.',
 'reviewed_not_finished':'The covered inside-cover publisher notice, remaining English transfer, final notation audit and final readable apparatus remain unfinished. ExposéXI has no printed body; the contents mark it Non rédigé.'}
(STAGE/'records/CHECKPOINT11_FREEZE.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'stage':STAGE.name,'review_directories':len(include)+1,'page_counts':counts,'English_external_inputs_verified':len(handoff['required_external_inputs'])}))
