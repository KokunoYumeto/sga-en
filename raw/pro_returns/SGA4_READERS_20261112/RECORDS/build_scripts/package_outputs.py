"""Package the deliverables and incremental, reproducible checkpoints."""
from pathlib import Path
import argparse, json, hashlib, zipfile

ROOT=Path(__file__).resolve().parents[1]
DELIVERY=ROOT/'deliverables'

def include_file(z,path,arcname):
    if path.name.endswith(('.pyc','.xdv','.aux','.out','.toc','.synctex.gz')):return
    if '__pycache__' in path.parts:return
    z.write(path,str(arcname))

def checkpoint(number):
    DELIVERY.mkdir(exist_ok=True)
    destination=DELIVERY/f'SGA4_READERS_checkpoint_{number}.zip'
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for folder in ['build_scripts','output']:
            for path in sorted((ROOT/folder).rglob('*')):
                if path.is_file():include_file(z,path,path.relative_to(ROOT))
        # Inputs remain the three supplied ZIPs; their checked hashes are included.
        for name in ['PROMPT.md']:
            path=ROOT/'upload'/name
            if path.exists():include_file(z,path,'instructions/'+name)
    return destination

def final():
    DELIVERY.mkdir(exist_ok=True)
    files=[]
    for language in ['FR','EN']:
        destination=DELIVERY/f'SGA4_READERS_{language}.zip'
        with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for path in sorted((ROOT/'output'/language.lower()).glob('*')):
                if path.is_file() and path.suffix in ['.tex','.pdf']:include_file(z,path,path.name)
            readme=ROOT/'output/records/README.md'
            if readme.exists():include_file(z,readme,'README.md')
        files.append(destination)
    destination=DELIVERY/'SGA4_READERS_RECORDS.zip'
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for folder,prefix in [('output/records',''),('build_scripts','build_scripts'),('output/shared','shared')]:
            for path in sorted((ROOT/folder).rglob('*')):
                if path.is_file():include_file(z,path,Path(prefix)/path.relative_to(ROOT/folder))
    files.append(destination)
    return files

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--checkpoint',type=int);p.add_argument('--final',action='store_true');a=p.parse_args()
    paths=[checkpoint(a.checkpoint)] if a.checkpoint is not None else final() if a.final else []
    for path in paths:print(json.dumps({'file':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
