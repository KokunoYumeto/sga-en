"""Create immutable progress archives; raw inputs and regenerable rasters omitted."""
from pathlib import Path
import zipfile,json,re,hashlib,argparse
from archive_preflight import module as privacy
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--milestone',default='Progress checkpoint')
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
owners=['arcata','rapport_cycle','sommes','finitude_verdier']
existing=list(OUT.glob('SGA4HALF_READERS_checkpoint_*.zip'))
n=1+max([int(p.stem.rsplit('_',1)[1]) for p in existing],default=0)
target=OUT/f'SGA4HALF_READERS_checkpoint_{n:02}.zip'
counts={}
for owner in owners:
    counts[owner]={}
    for name in ['pages','decisions','own_findings','variants']:
        p=ROOT/'work'/owner/(name+'.jsonl')
        counts[owner][name]=len(p.read_text().splitlines()) if p.exists() else 0
include=[]
include.extend(p for p in (ROOT/'scripts').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for owner in owners+['common','records','build','glossary','verification','tex_infrastructure_test','reproducibility']:
    include.extend(p for p in (ROOT/'work'/owner).rglob('*') if p.is_file() and p.suffix in {'.json','.jsonl','.tsv','.csv','.tex','.py','.md','.txt','.sty','.bib'} and '__pycache__' not in p.parts)
include.append(ROOT/'work/manifest_verification.json')
include.append(ROOT/'requirements-rebuild.txt')
for folder in ['deliverables']:
    include.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in {'.tex','.pdf','.md','.tsv','.json','.py','.sty','.bib','.sh'} and '__pycache__' not in p.parts)
privacy_failures=[]
for p in sorted(set(include)):
    if p.exists() and p.suffix!='.pdf':
        data=p.read_text(errors='replace')
        if privacy.LOCAL_PATH.search(data) or privacy.EMAIL.search(data):privacy_failures.append(p.relative_to(ROOT).as_posix())
assert not privacy_failures,('Privacy preflight rejected unpublished candidate',privacy_failures)
counts['milestone']=args.milestone
visual=ROOT/'work/verification/FINAL_VISUAL_QA.json'
if visual.exists():counts['completed_reader_visual_checks']=json.loads(visual.read_text()).get('readers',0)
with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(set(include)):
        if p.exists():z.write(p,p.relative_to(ROOT))
    z.writestr('CHECKPOINT_STATUS.json',json.dumps(counts,indent=2))
    z.writestr('CHECKPOINT_README.md','# SGA 4½ reader project: work in progress\n\nThis is an immutable progress checkpoint, not a completed edition. Only pages explicitly recorded as checked have been directly reviewed. The four original input ZIPs remain necessary to reproduce this work. Generated scan rasters and tool transfer helpers are excluded because they are reproducible operational material. No complete-volume verification is implied. The final three ZIPs will supersede this checkpoint.\n\n'+json.dumps(counts,indent=2)+'\n')
print(json.dumps({'filename':target.name,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'counts':counts}))
