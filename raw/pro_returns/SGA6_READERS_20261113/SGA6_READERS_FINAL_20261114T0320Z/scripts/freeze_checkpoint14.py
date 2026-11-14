#!/usr/bin/env python3
"""Freeze the four finished French books and the completed English VI seals."""
from pathlib import Path
import collections,hashlib,json,os,shutil
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'sga6_checkpoint13_stage'
STAGE=ROOT.parent/'sga6_checkpoint14_stage'
assert BASE.is_dir() and not STAGE.exists()
skip=shutil.ignore_patterns('__pycache__','images','rendered','compiled','*.png','*.ppm','*.jpg','*.pyc','*.log','*.aux','*.out','*.toc')
names=['SGA6_FR_master_annote','SGA6_FR_diplomatique','SGA6_FR_corrige_apparat','SGA6_FR_texte_de_lecture']
compiles=[]
for name in names:
    row=json.loads((ROOT/'records'/('COMPILE_'+name+'.json')).read_text())
    assert row['exit_code']==0 and row['passes']==2 and row['source_unchanged_during_compile']
    assert row['source_sha256']==hashlib.sha256((ROOT/row['file']).read_bytes()).hexdigest()
    assert row['pdf_sha256']==hashlib.sha256((ROOT/row['pdf']).read_bytes()).hexdigest()
    compiles.append(row)
assert json.loads((ROOT/'records/FR_FINAL_RENDERED_QA.json').read_text())['passed']
assert json.loads((ROOT/'records/FR_FINAL_SOURCE_INVARIANTS.json').read_text())['source_links_complete']
shutil.copytree(BASE,STAGE,symlinks=True,ignore=skip)
for folder,dirs,files in os.walk(STAGE,followlinks=False):
    Path(folder).chmod(0o755)
    for name in files:
        p=Path(folder)/name
        if not p.is_symlink():p.chmod(0o644)
for name in ['scripts','records']:
    shutil.copytree(ROOT/name,STAGE/name,dirs_exist_ok=True,ignore=skip)
for directory in sorted((ROOT/'review').iterdir()):
    if directory.is_dir() and directory.name!='english':shutil.copytree(directory,STAGE/'review'/directory.name,dirs_exist_ok=True,ignore=skip)
    elif directory.is_file():shutil.copy2(directory,STAGE/'review'/directory.name)
shutil.copytree(ROOT/'readers/fr/final',STAGE/'readers/fr/final',ignore=skip)
for name in ['FR_current_revised.tex','FR_diplomatic_revised.tex']:
    shutil.copy2(ROOT/'build'/name,STAGE/'build'/name)
seals=[]
for source_name,destination in [
    ('english_v297_364_vi365_393_complete','exposes_v_vi/snapshots/v297_364_vi365_393_complete'),
    ('english_vi394_415_complete','expose_vi_394_415/snapshots/vi394_415_complete')]:
    source=ROOT/'build/review_snapshots'/source_name
    target=STAGE/'review/english/contributions'/destination
    assert source.is_dir() and not target.exists()
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,target,ignore=skip)
    seals.append(dict(path=target.relative_to(STAGE).as_posix(),manifest_sha256=hashlib.sha256((source/'MANIFEST.json').read_bytes()).hexdigest()))
for name in ['reviewed_french.py','EN_POST_REVIEW_LOADER_CHECK.json']:
    shutil.copy2(ROOT/'review/english'/name,STAGE/'review/english'/name)
freeze=dict(checkpoint=14,base_checkpoint=13,final_release=False,
    completed='Four finished French books, including the readable 970-entry sourced apparatus, exact source/marker invariants and fresh two-pass PDFs. English VI 365–415 is now completely translated and sealed, completing all 700 numeric folios plus 20 original front/rear leaves in reviewed source packets.',
    new_English_seals=seals,French_compiles=compiles,
    pending='Final complete English assembly/glossary and its four finished PDFs, final combined release validation and the three requested archives.',
    preservation='Checkpoint 13 and all earlier checkpoint files remain unchanged. This new stage retains their prior sealed material and adds the completed work.')
(STAGE/'records/CHECKPOINT14_FREEZE.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
variants=json.loads((STAGE/'records/FR_VARIANTS.json').read_text())
from checkpoint import exposure,EXPOSES
counts=collections.Counter(exposure(v['page']) for v in variants)
lines=['# Apparatus counts — checkpoint14','',
    'All 970 French entries have exact adjudicated source links. The diplomatic and reading forms have zero apparatus entries; the corrected form and annotated-master PDF contain the same 970 entries.','',
    '| Exposé or matter | FR diplomatic | FR corrected apparatus | FR reading | FR master |','|---|---:|---:|---:|---:|']
for exp in ['Front matter']+[r[0] for r in EXPOSES]+['Rear publisher matter']:
    lines.append(f'| {exp} |0|{counts[exp]}|0|{counts[exp]}|')
lines+=['','Exposé XI has no printed body (Non rédigé) and creates no apparatus entry. English final counts will be supplied after the complete final aggregate gate.','']
(STAGE/'records/APPARATUS_COUNTS.md').write_text('\n'.join(lines))
readme=['# SGA6 checkpoint14','',
    'This immutable checkpoint contains the four finished French TeX/PDF books and the separately sealed completion of English ExposéVI. Final English assembly, glossary and publication packaging continue; this checkpoint is not the three-archive final release.','',
    '## Completed review','',
    'All 720 original physical leaves have recorded review dispositions. All 3,751 checker findings, 5,513 FIXLOG rows, 724 historical misprint records, 20 replay records, 7 manual findings, 141 rejected Codex records and 119 HOLD differences are decided. The original 111 author-note labels are retained. The seven required GLOBAL_ISSUES decisions, six NOTE_6 supplements, and the 49 normal-weight numeric-heading occurrences have explicit evidence.','',
    '## French books','',
    'The final files are in readers/fr/final/. The common annotated master generates the three forms by the SGAform switch. Both literal branches reconstruct the revised source exactly, all 720 source markers agree in order, and every one of 970 variant entries is linked to adjudicated source records. Original author text deliberately retained at the documented source-error/blank-reference passages is described in the edition preface and review/final_dispositions/.','',
    '| File | PDF pages | Errors | Warnings |','|---|---:|---:|---:|']
for row in compiles:readme.append(f"| {Path(row['file']).name} | {row['pdf_pages']} | {len(row['errors'])} | {row['warning_count']} |")
readme+=['','Fresh two-pass compile receipts, final exact branch/source checks and direct rendered-page observations are in records/. The complete source changes are in CHANGES_FR.tsv; its author-text projection and final reader-source hunks are separately identified and exactly reconstruct their targets.','',
    '## English completion seals','',
    'English V 297–364 and VI 365–393 are preserved together in the new immutable contribution snapshot; the companion snapshot supplies VI 394–415 through the native 416 boundary. These complete the English source coverage. Earlier sealed front/rear, VII–X, XII–XIV and index material is retained. The old incomplete 1–296 book remains a historical checkpoint artifact; the final full-volume English files are still being prepared.','',
    '## Reproduction and retained material','',
    'Extract the four original supplied archives, then this checkpoint. The scripts rebuild reviewed French layers, source-linked annotations and records. Standard TeX Live compiles each final French source as one standalone file. Source scan crops, raw runtime logs, caches and runtime packages are omitted; exact scan/page/region evidence and sanitized diagnostics are retained. The original archives and earlier checkpoint ZIPs are never nested. All prior immutable checkpoints remain available separately.','',
    'The publisher-notice restitution is explicitly attributed to the matching 1971 LNM 228 template; hidden physical strokes have not been recovered. Copy-specific labels, stamps, handwritten marks and nontextual logos are omitted. The 188 rear catalogue entries and two ISBN lines are retained.','']
(STAGE/'README.md').write_text('\n'.join(readme))
print(json.dumps(dict(stage=STAGE.name,French_books=4,new_English_seals=len(seals),ready_for_checkpoint_zip=True)))
