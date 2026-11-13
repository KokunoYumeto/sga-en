"""Stage and package the three final archives with content-hash manifests."""
from pathlib import Path
import argparse,csv,hashlib,json,shutil,zipfile

ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT/'work/final_package'
TEXT={'.json','.jsonl','.tsv','.csv','.tex','.py','.sh','.md','.txt','.sty','.bib','.diff'}
WORK=['arcata','rapport_cycle','sommes','finitude_verdier','common','records','build','glossary','verification','tex_infrastructure_test','reproducibility','checkpoint_diffs']
ARCHIVES={k:'SGA4HALF_READERS_'+k+'.zip' for k in ['FR','EN','RECORDS']}

def excluded(relative):
    p=Path(relative);parts=p.parts
    if '__pycache__' in parts:return 'Generated Python bytecode cache.'
    if p.suffix in {'.log','.aux','.out','.toc','.fmt','.map'}:return 'Raw runtime/cache output; sanitized logs and validation reports replace it.'
    if 'layout_review' in parts and (p.suffix=='.tex' or p.name.startswith('baseline_') and p.name.endswith('.log.txt')):
        return 'Temporary full-book layout baseline/trial, superseded by the eight final reader artifacts and FINAL_LAYOUT_VALIDATION.json.'
    if len(parts)>2 and parts[:2]==('work','build') and p.name.startswith('layout_trial'):
        return 'Temporary full-book layout trial diagnostics; final reader compile logs and the retained layout validation replace them.'
    if len(parts)>3 and parts[:2]==('work','reproducibility'):
        return 'Temporary isolated replay/extraction tree; the retained reproducibility reports give its verified results.'
    return ''

def collect():
    result={k:{} for k in ARCHIVES}
    for lang in ['FR','EN']:
        for p in sorted((ROOT/'deliverables'/lang).glob('SGA4HALF_*')):
            if p.suffix in {'.tex','.pdf'}:result[lang][p.relative_to(ROOT).as_posix()]=p
        assert len(result[lang])==8,(lang,'expected four TeX/PDF pairs')
    for p in (ROOT/'scripts').rglob('*'):
        if p.is_file() and p.suffix in TEXT and not excluded(p.relative_to(ROOT).as_posix()):result['RECORDS'][p.relative_to(ROOT).as_posix()]=p
    for folder in WORK:
        for p in (ROOT/'work'/folder).rglob('*'):
            if not p.is_file():continue
            rel=p.relative_to(ROOT).as_posix()
            allowed=p.suffix in TEXT or folder=='build' and 'visual_qa' in p.parts and p.suffix=='.png'
            if allowed and not excluded(rel):result['RECORDS'][rel]=p
    p=ROOT/'work/manifest_verification.json';result['RECORDS'][p.relative_to(ROOT).as_posix()]=p
    requirements=ROOT/'requirements-rebuild.txt'
    if requirements.exists():result['RECORDS'][requirements.name]=requirements
    # Principal tables and reports also appear at the root for quick inspection.
    for p in (ROOT/'work/records').iterdir():
        if p.is_file() and p.suffix in {'.tsv','.json','.md'}:result['RECORDS'][p.name]=p
    for name in ['GLOSSARY_SGA4HALF_FR_EN.tsv','GLOSSARY_INCONSISTENCIES.md','GLOSSARY_ATTESTATIONS.tsv','GLOSSARY_CANDIDATES.tsv','GLOSSARY_SOURCE_CENSUS.json']:
        result['RECORDS'][name]=ROOT/'work/glossary'/name
    for p in (ROOT/'work/records/diffs').glob('*.diff'):result['RECORDS']['diffs/'+p.name]=p
    rebuild=ROOT/'work/reproducibility/REBUILD.md'
    if rebuild.exists():result['RECORDS']['REBUILD.md']=rebuild
    return result

def stage_files():
    mapping=collect()
    if STAGE.exists():shutil.rmtree(STAGE)
    for group,items in mapping.items():
        for name,source in items.items():
            dest=STAGE/group/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        if group!='RECORDS':
            (STAGE/group/('READERS_'+group+'.md')).write_text('# SGA 4½ '+group+' readers\n\nThe deliverables folder contains the diplomatic, corrected with apparatus, reading, and annotated master source/PDF pairs. Each TeX file is standalone. Extract all three final archives into one project directory for the full audit and rebuild project; consult README.md in the records archive. The original printed text pages III–IV and 1–312 are all included. The master PDF shows the corrected apparatus form.\n')
    summary={}
    for group in mapping:
        base=STAGE/group;rows=[]
        for p in sorted(base.rglob('*')):
            if p.is_file():rows.append(dict(path_in_zip=p.relative_to(base).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),role='reader' if group!='RECORDS' else 'audit/build evidence'))
        with (base/('MANIFEST_'+group+'.tsv')).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['path_in_zip','bytes','sha256','role'],delimiter='\t');w.writeheader();w.writerows(rows)
        summary[group]=dict(files=len(rows),bytes=sum(x['bytes'] for x in rows),manifest_excludes_itself=True)
    return summary

def pack():
    result={}
    for group,name in ARCHIVES.items():
        base=STAGE/group;target=ROOT/'output'/name
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in sorted(base.rglob('*')):
                if p.is_file():z.write(p,p.relative_to(base))
        assert target.stat().st_size<100_000_000,('Archive exceeds100MB',name)
        with zipfile.ZipFile(target) as z:
            assert z.testzip() is None
            with z.open('MANIFEST_'+group+'.tsv') as raw:
                import io
                rows=list(csv.DictReader(io.TextIOWrapper(raw,encoding='utf-8'),delimiter='\t'))
            for row in rows:
                data=z.read(row['path_in_zip']);assert len(data)==int(row['bytes']) and hashlib.sha256(data).hexdigest()==row['sha256'],row['path_in_zip']
        result[group]=dict(filename=name,bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),manifest_entries=len(rows))
    (ROOT/'output/FINAL_ARCHIVES.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--stage-only',action='store_true');parser.add_argument('--pack-staged',action='store_true')
    args=parser.parse_args()
    if not args.pack_staged:print(json.dumps({'staged':stage_files()},indent=2))
    if not args.stage_only:print(json.dumps({'archives':pack()},indent=2))
