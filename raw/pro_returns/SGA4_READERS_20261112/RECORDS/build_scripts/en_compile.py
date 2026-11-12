"""Compile one generated English reader, recording sanitized diagnostics."""
from pathlib import Path
import argparse, json, shutil, subprocess, hashlib, re
from en_common import ROOT, RECORDS, sanitize
from tex_environment import tex_env

def main():
    p=argparse.ArgumentParser();p.add_argument('form',choices=['diplomatic','corrected_apparatus','reading']);p.add_argument('--passes',type=int,default=1);p.add_argument('--no-pdf',action='store_true');a=p.parse_args()
    name='SGA4_EN_'+a.form
    output=ROOT/'output/en';work=ROOT/'tmp/en_compile'/a.form
    work.mkdir(parents=True,exist_ok=True)
    src=output/(name+'.tex');dst=work/(name+'.tex')
    clean=not dst.exists() or src.read_bytes()!=dst.read_bytes()
    status=work/'STATUS.json'
    if status.exists() and json.loads(status.read_text())[-1]['returncode']!=0:clean=True
    if clean:
        for ext in ['.aux','.toc','.out']:
            p=work/(name+ext)
            if p.exists():p.unlink()
    shutil.copyfile(src,dst)
    source_sha256=hashlib.sha256(dst.read_bytes()).hexdigest()
    results=[]
    for i in range(a.passes):
        command=['xelatex','-interaction=nonstopmode','-halt-on-error','-no-shell-escape']
        if a.no_pdf:command.append('-no-pdf')
        command.append(name+'.tex')
        proc=subprocess.run(command,cwd=work,env=tex_env(),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (work/('console-%d.txt'%(i+1))).write_text(proc.stdout)
        results.append(dict(pass_number=i+1,returncode=proc.returncode,source_sha256=source_sha256))
        print(name,'pass',i+1,'exit',proc.returncode,flush=True)
        if proc.returncode:
            print(sanitize(proc.stdout[-2200:]),flush=True);break
    log=work/(name+'.log')
    if log.exists():
        public=RECORDS/'compile_logs';public.mkdir(exist_ok=True)
        publiclog=log.read_text(errors='replace').replace(str(ROOT)+'/', '').replace(str(ROOT),'BUILD_ROOT')
        publiclog=re.sub(r'/usr/[^\s()]+','[TeX Live resource]',publiclog)
        publiclog=re.sub(r'/opt/[^\s()]+','[runtime resource]',publiclog)
        (public/(name+'.log')).write_text(sanitize(publiclog))
    if results[-1]['returncode']==0 and not a.no_pdf:
        shutil.copyfile(work/(name+'.pdf'),output/(name+'.pdf'))
        report=dict(reader=name,source_sha256=source_sha256,pdf_sha256=hashlib.sha256((output/(name+'.pdf')).read_bytes()).hexdigest(),passes=results,returncode=0)
        (RECORDS/'compile_logs'/(name+'.json')).write_text(json.dumps(report,indent=2)+'\n')
    (work/'STATUS.json').write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
