#!/usr/bin/env python3
"""Freeze the completed English V, XIII, front/rear and French typography pass."""
from pathlib import Path
import hashlib,json,os,shutil

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'sga6_checkpoint12_stage'
STAGE=ROOT.parent/'sga6_checkpoint13_stage'
assert BASE.is_dir() and not STAGE.exists()
skip=shutil.ignore_patterns('__pycache__','images','rendered','compiled','*.png','*.ppm','*.jpg','*.pyc','*.log','*.aux','*.out','*.toc')
shutil.copytree(BASE,STAGE,symlinks=True,ignore=skip)
for folder,dirs,files in os.walk(STAGE,followlinks=False):
    Path(folder).chmod(0o755)
    for name in files:
        p=Path(folder)/name
        if not p.is_symlink():p.chmod(0o644)
for name in ['scripts','records']:
    shutil.copytree(ROOT/name,STAGE/name,dirs_exist_ok=True,ignore=skip)
for directory in sorted((ROOT/'review').iterdir()):
    if directory.is_dir() and directory.name!='english':
        shutil.copytree(directory,STAGE/'review'/directory.name,dirs_exist_ok=True,ignore=skip)
    elif directory.is_file():shutil.copy2(directory,STAGE/'review'/directory.name)
for p in (ROOT/'readers/fr').glob('*.tex'):shutil.copy2(p,STAGE/'readers/fr'/p.name)
for p in (STAGE/'readers/fr').glob('*.pdf'):p.unlink() # Only the new staging copy.
for name in ['FR_current_revised.tex','FR_diplomatic_revised.tex']:
    shutil.copy2(ROOT/'build'/name,STAGE/'build'/name)
seals=[]
for source_name,destination in [
    ('english_v_complete297_364','exposes_v_vi/snapshots/v297_364'),
    ('english_xiii_complete616_666','expose_xiii/snapshots/xiii616_666'),
    ('english_front_rear_complete20','front_rear/snapshots/front_rear20')]:
    source=ROOT/'build/review_snapshots'/source_name
    target=STAGE/'review/english/contributions'/destination
    assert source.is_dir() and not target.exists()
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(source,target,ignore=skip)
    seals.append(dict(path=target.relative_to(STAGE).as_posix(),manifest_sha256=hashlib.sha256((source/'MANIFEST.json').read_bytes()).hexdigest()))
refresh=[]
for name in ['reviewed_french.py','EN_POST_REVIEW_LOADER_CHECK.json',
             'EN_XIII_HANDOFF.json','EN_FRONT_REAR_HANDOFF.json','EN_FRONT_REAR_METADATA_ERRATUM.json']:
    p=ROOT/'review/english'/name;target=STAGE/'review/english'/name
    previous=hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None
    if target.exists():target.chmod(0o644)
    shutil.copy2(p,target)
    refresh.append(dict(path=target.relative_to(STAGE).as_posix(),previous_sha256=previous,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
freeze=dict(checkpoint=13,base_checkpoint=12,
    state='New frozen input copy; French PDFs require the recorded fresh compile and selected rendering checks.',
    completed='EnglishV297–364, XIII616–666 and all20 original front/rear leaves are complete and separately sealed. The final French typography core has930 exact applications, with0blocked anchors and700numeric pages in each loader branch. All720 physical source leaves and all historical finding classes retain completed dispositions.',
    new_English_seals=seals,refreshed_helpers=refresh,
    unchanged='The original English1–296 book and prior VII–X/XII/XIV/index seals are preserved from checkpoint12.',
    pending='EnglishVI365–415, full aggregate/glossary, final source links and readable French apparatus, complete final layout and eight-PDF release checks.',
    final_release=False)
(STAGE/'records/CHECKPOINT13_FREEZE.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(stage=STAGE.name,new_English_seals=len(seals),refreshed_helpers=len(refresh))))
