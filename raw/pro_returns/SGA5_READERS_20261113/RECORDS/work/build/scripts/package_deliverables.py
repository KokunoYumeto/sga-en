"""Stage the three delivery archives with relative paths and integrity manifests."""
from __future__ import annotations
import csv,hashlib,json,shutil,zipfile
from pathlib import Path

DEST=Path('deliverables')
RECORDS=DEST/'records'
EXCLUDED={'__pycache__','compile_check','runtime_check','flat_compile_check','compile_tmp','latex','private'}
EXTENSIONS={'.py','.tex','.pdf','.json','.jsonl','.tsv','.md','.txt','.log','.png','.diff','.patch'}
POST_PACKAGE_REPORTS={'FINAL_PACKAGE_PRIVACY_AUDIT.json','FINAL_PACKAGE_PRIVACY_REPORT.md'}
ROOT_COPIES={
 'PLACES_98_DECIDED.tsv':'scans/PLACES_98_DECIDED.tsv',
 'OPEN_ITEMS_DECIDED.tsv':'decisions/OPEN_ITEMS_DECIDED.tsv',
 'GLOSSARY_SGA5_FR_EN.tsv':'english/GLOSSARY_SGA5_FR_EN.tsv',
 'GLOSSARY_INCONSISTENCIES.md':'english/GLOSSARY_INCONSISTENCIES.md',
 'CHANGES_FR.tsv':'reader_changes/CHANGES_FR.tsv',
 'CHANGES_EN.tsv':'reader_changes/CHANGES_EN.tsv',
 'READER_ASSEMBLY_DECISIONS.tsv':'reader_changes/READER_ASSEMBLY_DECISIONS.tsv',
 'COMPLETE_READER_CHANGELOG_RECONSTRUCTION.json':'reader_changes/COMPLETE_READER_CHANGELOG_RECONSTRUCTION.json',
 'COMPLETE_READER_CHANGELOG_REPORT.md':'reader_changes/COMPLETE_READER_CHANGELOG_REPORT.md',
 'FR_SOURCE_WITNESSES.json':'validation_fr/FR_SOURCE_WITNESSES.json',
 'CHECKPOINTS.md':'packaging_audit/CHECKPOINTS.md',
}

def digest(data):return hashlib.sha256(data).hexdigest()

def copy_tree(source,target):
    for p in sorted(source.rglob('*')):
        if not p.is_file() or any(x in EXCLUDED or x.startswith(('portable-check-','patch-check-')) for x in p.relative_to(source).parts):continue
        if p.name in POST_PACKAGE_REPORTS:continue
        if p.suffix not in EXTENSIONS:continue
        q=target/p.relative_to(source);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)

def manifest(root):
    rows=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p==root/'MANIFEST.tsv':continue
        data=p.read_bytes();rows.append({'path':p.relative_to(root).as_posix(),'bytes':len(data),'sha256':digest(data)})
    with (root/'MANIFEST.tsv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['path','bytes','sha256'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    return rows

def archive(root,destination):
    rows=manifest(root)
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if not p.is_file():continue
            info=zipfile.ZipInfo(p.relative_to(root).as_posix(),date_time=(2026,11,13,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(destination) as z:
        assert z.testzip() is None
        for row in rows:
            data=z.read(row['path']);assert len(data)==row['bytes'] and digest(data)==row['sha256']
    return {'file':destination.name,'bytes':destination.stat().st_size,'sha256':digest(destination.read_bytes()),'manifest_entries':len(rows),'archive_integrity_verified':True}

def main():
    RECORDS.mkdir(parents=True,exist_ok=True)
    # Replace only the staged generated tree; source artifacts remain intact.
    if (RECORDS/'work').exists():shutil.rmtree(RECORDS/'work')
    for p in [Path('work/build/scripts'),Path('work/build/prepared'),Path('work/contributions')]:
        copy_tree(p,RECORDS/p)
    for name,source in ROOT_COPIES.items():
        p=Path('work/contributions')/source
        if name=='CHECKPOINTS.md' and not p.exists():continue
        shutil.copy2(p,RECORDS/name)
    shutil.copy2(Path('work/build/prepared/EN_variants_input.json'),RECORDS/'EN_variants_input.json')
    prompt=Path('upload/PROMPT(20261112-230204).md')
    (RECORDS/'upload').mkdir(exist_ok=True);shutil.copy2(prompt,RECORDS/'upload'/prompt.name)
    driver=Path('work/contributions/packaging_audit/rebuild.py')
    guide=Path('work/contributions/packaging_audit/REBUILD.md')
    assert driver.exists() and guide.exists(),'Portable rebuild driver and guide must be completed'
    (RECORDS/'rebuild.py').write_text('''"""Run the included rebuild driver from the records project root."""
import runpy
import sys
from pathlib import Path
driver=Path("work/contributions/packaging_audit/rebuild.py")
sys.path.insert(0,str(driver.parent))
runpy.run_path(str(driver),run_name="__main__")
''')
    shutil.copy2(guide,RECORDS/'REBUILD.md')
    for lang in ['FR','EN']:
        shutil.copy2(RECORDS/'APPARATUS_COUNTS.md',DEST/lang/'APPARATUS_COUNTS.md')
        # Source identities give each language package a compact local inventory.
        summary=json.loads((RECORDS/'BUILD_SUMMARY.json').read_text())
        local={'language':lang,'builds':[b for b in summary['builds'] if b['language']==lang],'apparatus_entries':summary['apparatus_entries'][lang]}
        (DEST/lang/'BUILD_SUMMARY.json').write_text(json.dumps(local,ensure_ascii=False,indent=2)+'\n')
    packages=[]
    for lang in ['FR','EN']:packages.append(archive(DEST/lang,DEST/f'SGA5_READERS_{lang}.zip'))
    packages.append(archive(RECORDS,DEST/'SGA5_READERS_RECORDS.zip'))
    result={'packages':packages,'all_under_100_MB':all(p['bytes']<100_000_000 for p in packages)}
    (DEST/'PACKAGE_INTEGRITY.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
