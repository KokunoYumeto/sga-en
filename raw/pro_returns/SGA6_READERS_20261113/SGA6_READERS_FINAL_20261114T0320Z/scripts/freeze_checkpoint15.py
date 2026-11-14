#!/usr/bin/env python3
"""Freeze the completed English books as an immutable delta over checkpoint14.

The stage is complete. The archive carries every new or changed file, and
verifies that overlaying it on checkpoint14 recovers the full release plan.
No earlier archive or stage is modified.
"""
from pathlib import Path
import csv,hashlib,io,json,os,shutil,zipfile
from package_release import plan,PRIVATE,BINARY,digest

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'sga6_checkpoint14_stage'
STAGE=ROOT.parent/'sga6_checkpoint15_stage'
ARCHIVE=ROOT.parent/'SGA6_READERS_checkpoint_15.zip'
PREVIOUS=ROOT.parent/'SGA6_READERS_checkpoint_14.zip'

def main():
    assert BASE.is_dir() and PREVIOUS.is_file() and not STAGE.exists() and not ARCHIVE.exists()
    gate=json.loads((ROOT/'records/RELEASE_VALIDATION.json').read_text())
    assert gate['passed'] and len(gate['final_files'])==16
    for row in gate['final_files']:assert digest((ROOT/row['path']).read_bytes())==row['sha256']
    archives,omitted=plan()
    selected={}
    for paths in archives.values():
        assert not (set(selected)&set(paths))
        selected.update(paths)
    old_hash=digest(PREVIOUS.read_bytes())
    expected=json.loads((ROOT/'records/CHECKPOINT14_SAVE.json').read_text())
    assert expected['sha256']==old_hash
    with zipfile.ZipFile(PREVIOUS) as z:
        baseline={r['path']:r for r in csv.DictReader(io.StringIO(z.read('CHECKPOINT_MANIFEST.tsv').decode()),delimiter='\t')}
    shutil.copytree(BASE,STAGE,symlinks=True)
    for folder,dirs,files in os.walk(STAGE,followlinks=False):
        Path(folder).chmod(0o755)
        for name in files:
            p=Path(folder)/name
            if not p.is_symlink():p.chmod(0o644)
    for rel,p in selected.items():
        dest=STAGE/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,dest)
    freeze=dict(checkpoint=15,base_checkpoint=14,base_archive=PREVIOUS.name,base_sha256=old_hash,
      archive_format='Exact new/changed-file delta. Extract checkpoint14, then checkpoint15; the full immutable checkpoint15 stage has been independently assembled.',
      completed='Four complete English books and their full original-manifest packet closure, final glossary and all combined release gates. Together with checkpoint14, all eight final TeX/PDF pairs are fixed.',
      release_gate_sha256=digest((ROOT/'records/RELEASE_VALIDATION.json').read_bytes()),
      final_files=gate['final_files'],source_payload_paths=len(selected),
      final_three_archive_packaging='The requested three final release archives are assembled separately; no checkpoint ZIP is nested.',
      preservation='All earlier checkpoint ZIPs and frozen stages remain unchanged.')
    content=json.dumps(freeze,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'records/CHECKPOINT15_FREEZE.json').write_text(content)
    (STAGE/'records/CHECKPOINT15_FREEZE.json').write_text(content)
    selected['records/CHECKPOINT15_FREEZE.json']=STAGE/'records/CHECKPOINT15_FREEZE.json'
    readme=('# SGA6 checkpoint15 — completed English and combined release gates\n\n'
      'This numbered archive is an exact delta over SGA6_READERS_checkpoint_14.zip. '
      'Extract checkpoint14 first, then checkpoint15 into the same directory. '
      'The overlay supplies every file needed by the completed release plan. '
      'Both archives and their manifests are immutable. The final three release ZIPs are also delivered separately.\n\n'
      'The following shared release documentation describes the completed books and their evidence.\n\n'
      +(ROOT/'README.md').read_text())
    (STAGE/'README.md').write_text(readme);selected['README.md']=STAGE/'README.md'
    delta=[]
    for rel,p in sorted(selected.items()):
        data=(STAGE/rel).read_bytes()
        assert data==p.read_bytes(),rel
        previous=baseline.get(rel)
        if not previous or previous['sha256']!=digest(data):
            if p.suffix not in BINARY:assert not PRIVATE.search(data.decode('utf-8')),rel
            delta.append((rel,data))
    changed={rel:digest(data) for rel,data in delta}
    for rel,p in selected.items():
        recovered=changed.get(rel,baseline.get(rel,{}).get('sha256'))
        assert recovered==digest(p.read_bytes()),rel
    manifest='path\tbytes\tsha256\n'+''.join(f'{rel}\t{len(data)}\t{digest(data)}\n' for rel,data in delta)
    with zipfile.ZipFile(ARCHIVE,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel,data in delta:z.writestr(rel,data)
        z.writestr('CHECKPOINT_MANIFEST.tsv',manifest)
    # The approximately100MB limit applies to each of the three final release
    # archives. This additional immutable recovery checkpoint retains its full
    # delta even when that historical/recovery payload is larger.
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        for row in csv.DictReader(io.StringIO(z.read('CHECKPOINT_MANIFEST.tsv').decode()),delimiter='\t'):
            data=z.read(row['path']);assert len(data)==int(row['bytes']) and digest(data)==row['sha256']
    assert digest(PREVIOUS.read_bytes())==old_hash
    receipt=dict(checkpoint=ARCHIVE.name,bytes=ARCHIVE.stat().st_size,sha256=digest(ARCHIVE.read_bytes()),
      files=len(delta)+1,format='delta over checkpoint14',base_sha256=old_hash,
      exact_release_overlay_verified=True,overlay_payload_paths=len(selected),manifest_verified=True,
      final_TeX_PDF_pairs=8,stage=STAGE.name,save_pending=True)
    (ROOT/'records/CHECKPOINT15_BUILD.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
