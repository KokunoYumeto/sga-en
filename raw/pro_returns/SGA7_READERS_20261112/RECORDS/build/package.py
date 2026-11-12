#!/usr/bin/env python3
"""Create the requested self-contained language/records archives and checkpoints."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
ARCH=ROOT/'deliverables'


def add(z,p,arc):
    info=zipfile.ZipInfo(str(arc),date_time=(2026,11,12,12,0,0))
    info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=0o644<<16
    z.writestr(info,p.read_bytes())


def checkpoint(n):
    ARCH.mkdir(exist_ok=True)
    p=ARCH/f'SGA7_READERS_checkpoint_{n}.zip'
    with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for d in [ROOT/'output',ROOT/'build']:
            for f in sorted(d.rglob('*')):
                if f.is_file() and '__pycache__' not in f.parts and f.suffix not in ['.pyc']:
                    add(z,f,f.relative_to(ROOT))
        for f in sorted((ROOT/'work').glob('*.tex')):
            if f.name.startswith(('frontmatter','unresolved')):add(z,f,Path('work')/f.name)
        for f in sorted((ROOT/'work').glob('*.json')):
            add(z,f,Path('work')/f.name)
        z.writestr('CHECKPOINT.md',f'# SGA 7 readers: checkpoint {n}\n\nThis archive preserves all generated reader sources, completed PDFs, editorial records and build scripts available at this checkpoint. Compile statuses are in output/records/compile. The original three source archives remain the immutable rebuild inputs. Work in progress is not represented as finished.\n')
    return p


def final(require_complete=True):
    if require_complete:
        audit=json.loads((OUT/'records/FINAL_AUDIT.json').read_text())
        assert audit['pdfs_required'] and audit['checks_failed']==0,'Run the complete final audit before packaging.'
        for item in audit['source_artifacts']+audit['pdf_artifacts']:
            assert hashlib.sha256((OUT/item['file']).read_bytes()).hexdigest()==item['sha256'],('Artifact changed after final audit',item['file'])
    ARCH.mkdir(exist_ok=True);result=[]
    for lang in ['FR','EN']:
        p=ARCH/f'SGA7_READERS_{lang}.zip'
        with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for f in sorted((OUT/lang.lower()).glob('*')):
                if f.is_file() and f.suffix in ['.tex','.pdf']:add(z,f,f.name)
            add(z,OUT/'records/README.md','README.md')
        result.append(p)
    p=ARCH/'SGA7_READERS_RECORDS.zip'
    with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted((OUT/'records').rglob('*')):
            if f.is_file():add(z,f,f.relative_to(OUT/'records'))
        for f in sorted((ROOT/'build').glob('*')):
            if f.is_file() and f.suffix in ['.py','.md','.sh','.json','.tsv']:add(z,f,Path('build')/f.name)
        for f in sorted((ROOT/'work').glob('*.tex')):
            if f.name.startswith(('frontmatter','unresolved')):add(z,f,Path('work')/f.name)
        for f in sorted((ROOT/'work').glob('*.json')):
            add(z,f,Path('work')/f.name)
    result.append(p)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--checkpoint',type=int)
    ap.add_argument('--allow-incomplete',action='store_true',help='Package a source-only rebuild without asserting finished PDFs')
    a=ap.parse_args()
    paths=[checkpoint(a.checkpoint)] if a.checkpoint is not None else final(not a.allow_incomplete)
    print(json.dumps([{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],indent=2))
