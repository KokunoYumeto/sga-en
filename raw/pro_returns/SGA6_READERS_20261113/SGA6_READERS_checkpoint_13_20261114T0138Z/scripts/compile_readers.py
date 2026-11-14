#!/usr/bin/env python3
"""Compile reader candidates and export path-free diagnostics.

Raw engine transcripts stay in build/. The exported JSON reports actual exit
codes, errors, warning counts, and PDF metadata without declaring collation done.
"""
import argparse
import concurrent.futures
import hashlib
import json
import re
import subprocess
from pathlib import Path
import fitz
from tex_environment import tex_environment, ROOT

def compile_one(rel):
    src=ROOT/rel
    source_hash=hashlib.sha256(src.read_bytes()).hexdigest()
    build=ROOT/'build/compiled'/src.stem
    build.mkdir(parents=True,exist_ok=True)
    logs=[];code=None
    for number in range(1,3):
        p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
          '-output-directory='+str(build),str(src)],cwd=ROOT,env=tex_environment(),capture_output=True,text=True)
        (build/f'pass{number}.stdout.txt').write_text(p.stdout+p.stderr)
        logs.append(p.stdout+p.stderr);code=p.returncode
        if code:break
    text=logs[-1] if logs else ''
    sanitized=text.replace(str(ROOT)+'/', '')
    sanitized=re.sub(r'/(?:workspace|home|root|usr|opt)/[^\s\)\]]+','[runtime file]',sanitized)
    errors=[];warnings=[]
    lines=sanitized.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('!') or 'Fatal error' in line or (': ' in line and ('Error:' in line or 'Undefined control sequence' in line)):
            errors.append('\n'.join(lines[i:min(len(lines),i+4)]))
        if 'Warning:' in line or 'pdfTeX warning' in line or 'Overfull ' in line or 'Underfull ' in line:
            warnings.append(line)
    pdf=build/(src.stem+'.pdf')
    source_hash_after=hashlib.sha256(src.read_bytes()).hexdigest()
    info={'file':rel,'exit_code':code,'passes':len(logs),'errors':errors,'warnings':warnings,
      'source_sha256':source_hash,'source_unchanged_during_compile':source_hash==source_hash_after,
      'warning_count':len(warnings),'collation_status':'independent from compilation; see PAGES_CHECKED.tsv'}
    if code==0 and pdf.exists():
        data=pdf.read_bytes();target=src.with_suffix('.pdf');target.write_bytes(data)
        doc=fitz.open(pdf)
        info.update({'pdf':target.relative_to(ROOT).as_posix(),'pdf_pages':len(doc),'pdf_bytes':len(data),
          'pdf_sha256':hashlib.sha256(data).hexdigest()})
    (ROOT/'records'/('COMPILE_'+src.stem+'.json')).write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    return info

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('files',nargs='+');parser.add_argument('--jobs',type=int,default=2)
    args=parser.parse_args()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for result in pool.map(compile_one,args.files):
            print(json.dumps(result,ensure_ascii=False),flush=True)
