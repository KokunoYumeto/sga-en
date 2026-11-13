#!/usr/bin/env python3
"""Compile English candidates and preserve path-free diagnostic summaries."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
WRAPPER=ROOT/'scripts/tex_environment.py'


def diagnostics(text):
    lines=text.splitlines()
    rows=[]
    for i,l in enumerate(lines):
        if l.startswith('!') or 'Warning:' in l or 'warning (' in l or l.startswith(('Overfull \\','Underfull \\')) or "I can't find" in l:
            block=[l]
            j=i+1
            while j<len(lines) and j<i+10 and lines[j].strip():
                block.append(lines[j]);j+=1
            # Source excerpts are kept only without local filesystem paths.
            block=[x for x in block if not re.search(r'(?:/workspace/|/home/|/usr/|/opt/|/tmp/|/root/)',x)]
            rows.append('\n'.join(block))
    return rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('forms',nargs='*',default=['corrected_apparatus','diplomatic','reading','annotated_master']);args=ap.parse_args()
    result={}
    for form in args.forms:
        stem='DRAFT_SGA6_EN_'+form
        tex=HERE/(stem+'.tex')
        source=tex.read_text()
        source_hash=hashlib.sha256(tex.read_bytes()).hexdigest()
        runs=[]
        for n in range(1,3):
            command=[sys.executable,str(WRAPPER),'pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory=review/english','review/english/'+stem+'.tex']
            p=subprocess.run(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            ds=diagnostics(p.stdout)
            summary=next((l for l in p.stdout.splitlines() if l.startswith('Output written on ')), '')
            entry={'run':n,'exit_code':p.returncode,'diagnostics':ds,'output':summary}
            runs.append(entry)
            # Standard TeX .log files contain system paths. Replace after each
            # run with the retained diagnostic-only report.
            (HERE/(stem+'.log')).write_text('Diagnostic-only build report. TeX package-loading paths omitted.\n'+json.dumps(entry,ensure_ascii=False,indent=2)+'\n')
            if p.returncode:
                break
        pdf=HERE/(stem+'.pdf')
        result[form]={'runs':runs,'pdf_present':pdf.exists(),'scan_collation_complete':False,
                      'source_sha256':source_hash,
                      'source_unchanged_during_compile':hashlib.sha256(tex.read_bytes()).hexdigest()==source_hash,
                      'compiled_printed_markers':[int(x) for x in re.findall(r'\\SGAPrintPage\{(\d+)\}',source)],
                      'compiled_variant_ids':re.findall(r'\\csname SGAAppNumber@(EN-VAR-\d+)\\endcsname',source)}
        if pdf.exists() and not runs[-1]['exit_code']:
            result[form]['pdf_sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest()
        print(form,json.dumps(result[form],ensure_ascii=False),flush=True)
        (HERE/'EN_CANDIDATE_BUILD_STATUS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        if runs[-1]['exit_code']:
            break


if __name__=='__main__':
    main()
