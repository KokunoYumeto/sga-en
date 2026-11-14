#!/usr/bin/env python3
"""Package the final readers and cumulative records after the release gate.

The final archives are exclusive creations. Earlier checkpoint archives and
stages are read only. Generated historical PDFs are listed individually when
omitted; the final eight PDFs are always included.
"""
from pathlib import Path
import argparse,csv,hashlib,io,json,re,zipfile
ROOT=Path(__file__).resolve().parents[1]
FORM_NAMES={
 'FR':['SGA6_FR_master_annote','SGA6_FR_diplomatique','SGA6_FR_corrige_apparat','SGA6_FR_texte_de_lecture'],
 'EN':['SGA6_EN_annotated_master','SGA6_EN_diplomatic','SGA6_EN_corrected_apparatus','SGA6_EN_reading']}
EXTENSIONS={'.py','.json','.jsonl','.tsv','.csv','.tex','.md','.pdf','.txt','.diff'}
BINARY={'.pdf','.png','.jpg','.jpeg','.ppm'}
SOURCE_OMISSIONS={
 'review/publisher_notice_recovery/gabriel_ulmer1971.pdf':{
  'sha256':'aca30e69e4d239f098e5130538d8f64e1d4a1c4cef00ada846ce0e1663867278',
  'reason':'Downloaded third-party reference book omitted from redistribution. Its source URL, byte count, page count and SHA-256 remain in candidates_1971.json; the two publisher front-matter PDFs used for comparison remain included.'}}
PRIVATE=re.compile(r'(?:[A-Z]:\\(?:Users|work|home)\\|/(?:workspace/scratch|home/agent|root/\.codex)/[^\s]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})')

def digest(data):return hashlib.sha256(data).hexdigest()

def selected(base):
    result={}
    for top in ['scripts','records','readers','review']:
        if not (base/top).exists():continue
        for p in (base/top).rglob('*'):
            if not p.is_file():continue
            rel=p.relative_to(base)
            if any(part in ['__pycache__','images','build','rendered','compiled'] for part in rel.parts):continue
            if p.name.startswith('TEMP_') or p.suffix not in EXTENSIONS:continue
            result[rel.as_posix()]=p
    return result

def english_packet_files():
    """Return the complete original-manifest closure at its recorded paths."""
    catalog=json.loads((ROOT/'review/english/aggregate/INPUT_CATALOG.json').read_text())
    result={}
    for packet in catalog['packets']:
        directory=packet['directory'];folder=ROOT/directory
        mf=ROOT/packet['manifest']['path']
        assert digest(mf.read_bytes())==packet['manifest']['sha256']
        if mf.suffix=='.json':
            value=json.loads(mf.read_text());members=value if isinstance(value,list) else value['files']
        else:
            members=list(csv.DictReader(io.StringIO(mf.read_text()),delimiter='\t'))
        assert len(members)==packet['manifest']['verified_files']
        result[mf.relative_to(ROOT).as_posix()]=mf
        for row in members:
            part=Path(row['path']);assert not part.is_absolute() and '..' not in part.parts
            p=folder/part
            assert p.is_file() and digest(p.read_bytes())==row['sha256'],p.relative_to(ROOT).as_posix()
            result[p.relative_to(ROOT).as_posix()]=p
    return result

def glossary_capture_files():
    """Keep the exact captured glossary inputs, including their build subpaths."""
    base=ROOT/'review/english/terminology_final/input_snapshots'
    return {p.relative_to(ROOT).as_posix():p for p in base.rglob('*')
      if p.is_file() and p.suffix in EXTENSIONS and '__pycache__' not in p.parts}

def english_final_manifest_files():
    """Retain all sealed final records, including the four sanitized logs."""
    mf=ROOT/'review/english/final/MANIFEST.json'
    if not mf.exists():return {}
    seal=json.loads((mf.parent/'SEAL_RECEIPT.json').read_text())
    assert digest(mf.read_bytes())==seal['manifest']['sha256']
    result={}
    for row in json.loads(mf.read_text())['files']:
        p=ROOT/row['path'];data=p.read_bytes()
        assert len(data)==row['bytes'] and digest(data)==row['sha256'],row['path']
        result[row['path']]=p
    return result

def plan():
    files={}
    completed_stages=sorted(ROOT.parent.glob('sga6_checkpoint[0-9][0-9]_stage'))
    base=completed_stages[-1] if completed_stages else ROOT.parent/'sga6_checkpoint13_stage'
    if base.exists():files.update(selected(base))
    files.update(selected(ROOT))
    packets=english_packet_files()
    files.update(packets)
    files.update(glossary_capture_files())
    files.update(english_final_manifest_files())
    for name in ['FR_current_revised.tex','FR_diplomatic_revised.tex']:
        p=ROOT/'build'/name
        assert p.exists();files['build/'+name]=p
    archives={'FR':{},'EN':{},'RECORDS':{}};omitted=[]
    final_paths={}
    for language,names in FORM_NAMES.items():
        directory='readers/fr/final' if language=='FR' else 'review/english/final'
        for name in names:
            for suffix in ['.tex','.pdf']:
                rel=directory+'/'+name+suffix;p=ROOT/rel
                assert p.is_file(),rel
                final_paths[rel]=language
    for rel,p in sorted(files.items()):
        if rel in SOURCE_OMISSIONS:
            assert digest(p.read_bytes())==SOURCE_OMISSIONS[rel]['sha256']
        elif rel in final_paths:archives[final_paths[rel]][rel]=p
        elif rel in packets:archives['EN'][rel]=p
        elif p.suffix=='.pdf' and not rel.startswith('review/publisher_notice_recovery/'):
            omitted.append(dict(path=rel,reason='Earlier working/checkpoint/probe rendering. The eight final PDFs are supplied; corresponding retained source/evidence and immutable checkpoint archives preserve the earlier work.'))
        else:archives['RECORDS'][rel]=p
    assert set(final_paths)<=set(files)
    return archives,omitted

def manifest(rows):
    buf=io.StringIO();w=csv.writer(buf,delimiter='\t',lineterminator='\n')
    w.writerow(['path','source','bytes','sha256','role'])
    for rel,data in rows:
        role='final reader or annotated master' if rel.endswith(('.tex','.pdf')) and '/final/' in rel else ('sealed English reconstruction/evidence packet' if '/review_snapshots/' in rel or '/snapshots/' in rel else 'build/review/decision record')
        w.writerow([rel,'This source-collated edition',len(data),digest(data),role])
    return buf.getvalue().encode()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--plan',action='store_true');parser.add_argument('--write',action='store_true');args=parser.parse_args()
    archives,omitted=plan()
    included=set().union(*(set(paths) for paths in archives.values()))|{'README.md','MANIFEST.tsv'}
    historical={}
    for checkpoint_manifest in sorted((ROOT/'records/checkpoint_history').glob('checkpoint_*_CHECKPOINT_MANIFEST.tsv')):
        for row in csv.DictReader(io.StringIO(checkpoint_manifest.read_text()),delimiter='\t'):
            if row['path'] not in included:
                historical.setdefault(row['path'],[]).append(checkpoint_manifest.name.split('_')[1])
    listed={row['path'] for row in omitted}
    historical_omissions=[dict(path=rel,checkpoints=checkpoints,
      reason=(SOURCE_OMISSIONS[rel]['reason'] if rel in SOURCE_OMISSIONS else 'Earlier generated PDF; see omitted_generated_PDFs.' if rel in listed else
       'Historical checkpoint artifact retained in the named immutable checkpoint archives. The complete final sources, current decision records and their reconstruction evidence are included in this release.'))
      for rel,checkpoints in sorted(historical.items())]
    report={'archives':{key:{'files':len(value),'uncompressed_bytes':sum(p.stat().st_size for p in value.values())} for key,value in archives.items()},
      'omitted_generated_PDFs':omitted,
      'omitted_supplementary_source_PDFs':[dict(path=rel,**record) for rel,record in SOURCE_OMISSIONS.items()],
      'historical_paths_not_in_final_archives':historical_omissions,
      'historical_version_policy':'At an unchanged relative path, the current reviewed file is included. Prior byte versions remain in their immutable numbered checkpoint archives; checkpoint manifests and archive hashes are retained under records/checkpoint_history/.',
      'English_packet_distribution':'The entire original-manifest closure of all ten English catalog packets is in SGA6_READERS_EN.zip at the exact recorded relative paths. This includes their historical probe PDFs, rendered images and sanitized diagnostic logs. No packet member or manifest is altered or omitted; the original collector remains unchanged. Extract all three archives together.',
      'English_packet_files':len(english_packet_files()),
      'glossary_captured_input_files':len(glossary_capture_files()),
      'sealed_English_final_manifest_members':len(english_final_manifest_files()),
      'other_omissions':[{'path':'Original supplied archives and extracted input trees','reason':'Source inputs remain in the four original attachments. Their validated manifests and input hashes are retained; the final records and scripts reconstruct the derived work.'},
       {'path':'Earlier checkpoint ZIP archives','reason':'Never nested. They remain separately preserved and immutable.'},
       {'path':'Runtime packages, caches, raw engine logs, auxiliary files, generated scan crops and contact sheets outside the ten exact English catalog packets','reason':'Reproducible runtime/inspection derivatives; source-image page/region evidence and sanitized compile diagnostics are retained. All members of the ten sealed English packets are included to preserve their original manifest verification.'}]}
    (ROOT/'records/RELEASE_PACKAGING_PLAN.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if not args.write:
        print(json.dumps({'archives':report['archives'],'omitted_generated_PDFs':len(omitted)},indent=2));return
    gate=json.loads((ROOT/'records/RELEASE_VALIDATION.json').read_text())
    assert gate['passed'] is True,'Release validation must pass before packaging.'
    for row in gate['final_files']:
        assert digest((ROOT/row['path']).read_bytes())==row['sha256'],row['path']
    readme=ROOT/'README.md';assert readme.exists()
    # Re-read the plan record in its just-written final form.
    archives['RECORDS']['records/RELEASE_PACKAGING_PLAN.json']=ROOT/'records/RELEASE_PACKAGING_PLAN.json'
    outputs=[]
    for kind,paths in archives.items():
        dest=ROOT.parent/('SGA6_READERS_'+kind+'.zip')
        assert not dest.exists(),'Final archive already exists: '+dest.name
        rows=[]
        for rel,p in sorted(paths.items()):
            data=p.read_bytes()
            if p.suffix not in BINARY:assert not PRIVATE.search(data.decode('utf-8')),'Private metadata in '+rel
            rows.append((rel,data))
        readme_bytes=readme.read_bytes()
        assert not PRIVATE.search(readme_bytes.decode('utf-8')),'Private metadata in README.md'
        rows.append(('README.md',readme_bytes))
        with zipfile.ZipFile(dest,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for rel,data in rows:z.writestr(rel,data)
            z.writestr('MANIFEST.tsv',manifest(rows))
        assert dest.stat().st_size<105_000_000,(dest.name,'archive size exceeds the requested approximate100MB limit')
        with zipfile.ZipFile(dest) as z:
            assert z.testzip() is None
            for row in csv.DictReader(io.StringIO(z.read('MANIFEST.tsv').decode()),delimiter='\t'):
                data=z.read(row['path']);assert len(data)==int(row['bytes']) and digest(data)==row['sha256'],row['path']
        outputs.append(dict(archive=dest.name,files=len(rows)+1,bytes=dest.stat().st_size,sha256=digest(dest.read_bytes()),manifest_verified=True))
    (ROOT/'records/FINAL_ARCHIVE_RECEIPTS.json').write_text(json.dumps({'archives':outputs},indent=2)+'\n')
    print(json.dumps({'archives':outputs},indent=2))

if __name__=='__main__':main()
