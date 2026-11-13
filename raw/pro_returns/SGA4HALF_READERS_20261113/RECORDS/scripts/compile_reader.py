"""Compile a selected flattened reader and retain privacy-safe diagnostics."""
from pathlib import Path
import os,re,json,subprocess,sys,shutil,time,hashlib
ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'work/tex_runtime';RUNTIME.mkdir(parents=True,exist_ok=True)
LOGS=ROOT/'work/build';LOGS.mkdir(parents=True,exist_ok=True)

def environment():
    env=os.environ.copy()
    fmt=subprocess.run(['kpsewhich','pdflatex.fmt'],capture_output=True,text=True).stdout.strip()
    if not fmt:
        dist=Path(subprocess.check_output(['kpsewhich','-var-value=TEXMFDIST'],text=True).strip())
        share=dist.parent.parent
        trees=[dist,share/'texmf']
        env['TEXMF']='{'+','.join(str(p) for p in trees if p.exists())+'}'
        env['TEXMFVAR']=str(RUNTIME);env['TEXMFCONFIG']=str(RUNTIME)
        env['TEXFORMATS']=str(RUNTIME)+'//:';env['TEXFONTMAPS']=str(RUNTIME)+'//:'
        if not (RUNTIME/'pdflatex.fmt').exists():
            r=subprocess.run(['pdftex','-ini','-etex','-interaction=nonstopmode','-halt-on-error','-jobname=pdflatex','-progname=pdflatex',r'\pdfoutput=1 \input latex.ltx'],cwd=RUNTIME,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            (RUNTIME/'format_build_raw.log').write_bytes(r.stdout)
            if r.returncode:raise RuntimeError('Could not initialize the local pdfLaTeX format')
        if not (RUNTIME/'pdftex.map').exists():
            wanted=['lm.map','cm.map','cmextra.map','cyrillic.map','euler.map','latxfont.map','symbols.map','rsfs.map','xypic.map']
            entries={}
            for tree in trees:
                for name in wanted:
                    for p in tree.glob('fonts/map/**/'+name):
                        for line in p.read_text().splitlines():
                            if line.strip() and not line.startswith('%'):entries.setdefault(line.split()[0],line)
            (RUNTIME/'pdftex.map').write_text('\n'.join(entries.values())+'\n')
    return env

def sanitize(s):
    # pdfTeX wraps embedded font filenames across lines inside angle brackets.
    # Redact the whole token before the ordinary single-line path filter.
    def font_token(match):
        compact=re.sub(r'\s+','',match.group())
        return '<runtime font file>' if re.search(r'/(?:home|root|workspace|mnt|usr|var|etc|opt)/',compact) else match.group()
    s=re.sub(r'<[^<>]*>',font_token,s,flags=re.S)
    s=s.replace(str(ROOT),'[project]')
    s=re.sub(r'(?:/(?:home|root|workspace|mnt|usr|var|etc|opt)/[^\s)\]<>]+)','[runtime file]',s)
    s=re.sub(r'[A-Za-z]:\\Users\\[^\s]+','[private path omitted]',s)
    s=re.sub(r'[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}','[address omitted]',s)
    return s

def run(path,passes=1):
    path=path.resolve();env=environment();runs=[]
    for n in range(1,passes+1):
        start=time.monotonic()
        r=subprocess.run(['pdflatex','-interaction=nonstopmode','-file-line-error',path.name],cwd=path.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout=r.stdout.decode(errors='replace');raw=path.with_suffix('.log').read_text(errors='replace') if path.with_suffix('.log').exists() else stdout
        (LOGS/(path.stem+f'.pass{n}.log.txt')).write_text(sanitize(raw))
        errors=re.findall(r'^! .*|^'+re.escape(path.name)+r':\d+:.*',raw,re.M)
        if not errors:errors=re.findall(r'^\./'+re.escape(path.name)+r':\d+:.*',raw,re.M)
        warnings=re.findall(r'^(?:(?:LaTeX|Package [^\s]+) Warning:|pdfTeX [Ww]arning(?: \([^)]*\))?:).*?(?=\n\s*\n|\n\[|\Z)',raw,re.M|re.S)
        overfull=re.findall(r'Overfull \\[hv]box \(([^)]*)\).*',raw)
        underfull=re.findall(r'Underfull \\[hv]box \(([^)]*)\).*',raw)
        item=dict(pass_number=n,exit_code=r.returncode,seconds=round(time.monotonic()-start,2),errors=errors,warnings=warnings,overfull=overfull,underfull_count=len(underfull),pdf_exists=path.with_suffix('.pdf').exists())
        runs.append(item)
        print(json.dumps(dict(reader=path.stem,pass_number=n,exit_code=r.returncode,seconds=item['seconds'],errors=errors[:12],
                              error_count=len(errors),warning_count=len(warnings),overfull_count=len(overfull),underfull_count=len(underfull),pdf_exists=item['pdf_exists']),ensure_ascii=False),flush=True)
        if r.returncode:break
    result=dict(reader=path.stem,runs=runs,final=runs[-1],tex_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                pdf_sha256=hashlib.sha256(path.with_suffix('.pdf').read_bytes()).hexdigest() if path.with_suffix('.pdf').exists() else None)
    (LOGS/(path.stem+'.compile.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':
    result=run(ROOT/sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 1)
    sys.exit(result['final']['exit_code'])
