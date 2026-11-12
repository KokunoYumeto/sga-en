#!/usr/bin/env python3
"""Compile a standalone reader, retaining a privacy-clean diagnostic record."""
import argparse
import collections
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from tex_env import ROOT,environment,setup


def sanitize(s):
    # TeX wraps embedded font paths at its log line width, sometimes through
    # the directory name itself. Remove the complete wrapped resource path.
    s=re.sub(r'<(/[^<>]+)>',
             lambda m:'<TEXLIVE/'+Path(re.sub(r'\s+','',m.group(1))).name+'>',s)
    s=s.replace(str(ROOT)+'/','')
    s=re.sub(r'/(?:usr/share|usr/lib|var/lib|opt/codex|home/agent|root)/[^\s()<>]+',
             lambda m:'TEXLIVE/'+Path(m.group()).name,s)
    s=re.sub(r'[A-Za-z]:[\\/][^\s<>]*','[private source path omitted]',s)
    s=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}','[email omitted]',s)
    return s


def warning_messages(log):
    # TeX hard-wraps a warning, including numbers or control words, at its log
    # line width. Keep the complete paragraph through its separating blank
    # line so that the record does not truncate the input-line number or the
    # continuation of a package warning.
    return re.findall(
        r'^(?:(?:LaTeX|Package [\w.-]+|Class [\w.-]+)(?: Font)? Warning:|pdfTeX warning)[^\n]*(?:\n[^\n]+)*',
        log, re.M | re.I)


def compile_one(tex,passes=3,system_tex=False):
    tex=Path(tex).resolve();name=tex.stem
    wd=ROOT/'work/compile'/name;wd.mkdir(parents=True,exist_ok=True)
    logdir=ROOT/'output/records/compile';logdir.mkdir(parents=True,exist_ok=True)
    if not system_tex:setup()
    texenv=dict(os.environ) if system_tex else environment()
    texenv['SOURCE_DATE_EPOCH']='1794484800'
    texenv['FORCE_SOURCE_DATE']='1'
    runs=[]
    for n in range(1,passes+1):
        p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                          '-output-directory='+str(wd),tex.name],cwd=tex.parent,env=texenv,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace')
        (wd/f'pass{n}.console').write_text(p.stdout)
        runs.append({'pass':n,'exit_code':p.returncode})
        if p.returncode:break
    log=(wd/(name+'.log')).read_text(errors='replace') if (wd/(name+'.log')).exists() else p.stdout
    clean=sanitize(log)
    (logdir/(name+'.log')).write_text(clean)
    errors=[x for x in clean.splitlines() if x.startswith('!') or re.search(r':\d+:.*(?:Error|Undefined control|Missing|Extra|Emergency)',x)]
    warnings=warning_messages(clean)
    overfull=re.findall(r'Overfull \\[hv]box \(([^\n]+)',clean)
    underfull=re.findall(r'Underfull \\[hv]box[^\n]*',clean)
    missing=[x for x in clean.splitlines() if 'Missing character:' in x]
    pdf=wd/(name+'.pdf');pages=None
    success=p.returncode==0 and pdf.exists()
    if success:
        shutil.copy2(pdf,tex.with_suffix('.pdf'))
        q=subprocess.run(['pdfinfo',str(pdf)],stdout=subprocess.PIPE,text=True)
        m=re.search(r'^Pages:\s*(\d+)',q.stdout,re.M);pages=int(m.group(1)) if m else None
    version=subprocess.run(['pdflatex','--version'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace')
    engine=version.stdout.splitlines()[0] if version.stdout else 'pdfLaTeX'
    status={'reader':tex.name,'engine':engine,'passes':runs,'success':success,
            'pages':pages,'pdf_bytes':pdf.stat().st_size if success else None,'errors':errors,
            'warnings':warnings,'overfull_boxes':len(overfull),'underfull_boxes':len(underfull),
            'largest_overfull_pt':max([float(m.group(1)) for x in overfull if (m:=re.match(r'([\d.]+)pt',x))],default=0),
            'missing_characters':missing,'source_sha256':hashlib.sha256(tex.read_bytes()).hexdigest(),
            'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest() if success else None}
    (logdir/(name+'.json')).write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(status,ensure_ascii=False,indent=2))
    if not success:print(sanitize(p.stdout[-4500:]))
    return success


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('tex');p.add_argument('--passes',type=int,default=3)
    p.add_argument('--system-tex',action='store_true',help='Use the ordinary installed TeX Live configuration')
    a=p.parse_args()
    raise SystemExit(0 if compile_one(a.tex,a.passes,a.system_tex) else 1)
