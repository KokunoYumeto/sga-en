from __future__ import annotations
import argparse, collections, json, os, re, shutil, subprocess
from pathlib import Path
from sga5_common import write_json,redact,digest

def sanitize_log(s):
    # TeX diagnostics contain system and execution paths. Keep file basenames.
    s=redact(s)
    s=re.sub(r'/(?:usr|etc|var|opt|home|root|workspace|tmp)/[^\s()<>\[\]]+',lambda m:'[TeX file '+m[0].split('/')[-1]+']',s)
    s=re.sub(r'[A-Za-z]:\\(?:Users|Documents and Settings|Program Files|Windows|Temp|workspace|home)\\[^\s()<>\[\]]+','[local path omitted]',s,flags=re.I)
    return s

def compile_one(tex,build,passes=3):
    tex=Path(tex);name=tex.stem;d=Path(build)/name;d.mkdir(parents=True,exist_ok=True)
    runs=[];env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1794528000';env['FORCE_SOURCE_DATE']='1'
    for n in range(1,passes+1):
        p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory='+str(d),str(tex)],capture_output=True,text=True,env=env)
        (d/f'pass_{n}.stdout').write_text(p.stdout+p.stderr)
        runs.append({'pass':n,'exit_code':p.returncode})
        if p.returncode:break
    log=(d/(name+'.log')).read_text(errors='replace') if (d/(name+'.log')).exists() else p.stdout+p.stderr
    errors=[l for l in log.splitlines() if l.startswith('!') or re.search(r'\.tex:\d+:',l)]
    warnings=[l for l in log.splitlines() if 'Warning:' in l or 'Overfull ' in l or 'Underfull ' in l or 'Missing character:' in l]
    pages=re.search(r'Output written on .*?\((\d+) pages?',log,re.S)
    result={'file':tex.name,'source_sha256':digest(tex.read_bytes()),'runs':runs,'errors':errors,'error_count':len(errors),'warning_count':len(warnings),'warnings':warnings,'overfull_hboxes':len(re.findall(r'Overfull \\hbox',log)),'underfull_hboxes':len(re.findall(r'Underfull \\hbox',log)),'missing_characters':len(re.findall(r'Missing character:',log)),'pages':int(pages[1]) if pages else None,'success':p.returncode==0}
    result=json.loads(sanitize_log(json.dumps(result,ensure_ascii=False)))
    if result['success']:
        pdf=d/(name+'.pdf');shutil.copy2(pdf,tex.with_suffix('.pdf'));result['pdf_bytes']=pdf.stat().st_size;result['pdf_sha256']=digest(pdf.read_bytes())
        info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,check=True).stdout
        result['pages']=int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1])
    output=Path('deliverables/records/build_outputs');output.mkdir(parents=True,exist_ok=True)
    (output/(name+'.log')).write_text(sanitize_log(log))
    write_json(output/(name+'.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k!='warnings'},ensure_ascii=False))
    if not result['success']:print(sanitize_log('\n'.join(log.splitlines()[-38:])))
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('files',nargs='+');ap.add_argument('--build',default='work/build/latex');ap.add_argument('--passes',type=int,default=3);a=ap.parse_args()
    for f in a.files:
        r=compile_one(f,a.build,a.passes)
        if not r['success']:raise SystemExit(1)

if __name__=='__main__':main()
