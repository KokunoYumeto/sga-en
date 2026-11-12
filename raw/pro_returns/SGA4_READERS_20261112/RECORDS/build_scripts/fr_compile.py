"""Compile a generated standalone French reader with the installed TeX Live."""
from pathlib import Path
import sys,subprocess,json,re,shutil,hashlib
from tex_environment import tex_env
from fr_core import ROOT,sanitize
name=sys.argv[1] if len(sys.argv)>1 else 'SGA4_FR_diplomatique'
passes=int(sys.argv[2]) if len(sys.argv)>2 else 2
source=ROOT/'output'/'fr'
work=ROOT/'work_fr'/'compile'/name
work.mkdir(parents=True,exist_ok=True)
results=[]
source_hash=hashlib.sha256((source/(name+'.tex')).read_bytes()).hexdigest()
for number in range(1,passes+1):
    command=['xelatex','-interaction=nonstopmode']+([] if '--collect' in sys.argv else ['-halt-on-error'])+['-file-line-error',
             '-output-directory='+str(work),name+'.tex']
    result=subprocess.run(command,cwd=source,env=tex_env(),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (work/('pass'+str(number)+'.out')).write_text(result.stdout)
    print(name,'pass',number,'exit',result.returncode,flush=True)
    print(result.stdout[-3500:],flush=True)
    results.append({'pass':number,'returncode':result.returncode})
    if result.returncode:break
log=(work/(name+'.log')).read_text(errors='replace') if (work/(name+'.log')).exists() else result.stdout
summary={'reader':name,'source_sha256':source_hash,'passes':results,'errors':re.findall(r'^! [^\n]*|^.*:[0-9]+:.*(?:Error|Undefined control sequence|Missing .* inserted|Runaway argument|Extra .*|Use of .*doesn.t match).*',log,re.M),
         'warnings':re.findall(r'^(?:LaTeX(?: Font)?|Package [^\n]+) Warning:[^\n]+',log,re.M),
         'overfull':len(re.findall(r'Overfull \\hbox',log)),
         'underfull':len(re.findall(r'Underfull \\[hv]box',log)),
         'missing_characters':re.findall(r'Missing character:[^\n]+',log),
         'pdf_pages':(re.findall(r'Output written on .*?\((\d+) pages',log,re.S) or [None])[-1]}
if not result.returncode:summary['pdf_sha256']=hashlib.sha256((work/(name+'.pdf')).read_bytes()).hexdigest()
assert hashlib.sha256((source/(name+'.tex')).read_bytes()).hexdigest()==source_hash,'Source changed during compilation'
public=ROOT/'output'/'records'/'compile'
public.mkdir(parents=True,exist_ok=True)
(public/(name+'.json')).write_text(sanitize(json.dumps(summary,ensure_ascii=False,indent=2)))
publiclog=log.replace(str(ROOT)+'/', '').replace(str(ROOT),'BUILD_ROOT')
publiclog=re.sub(r'/usr/[^\s()]+','[TeX Live resource]',publiclog)
publiclog=re.sub(r'/opt/[^\s()]+','[runtime resource]',publiclog)
(public/(name+'.log')).write_text(sanitize(publiclog))
if not result.returncode:
    shutil.copy2(work/(name+'.pdf'),source/(name+'.pdf'))
sys.exit(result.returncode)
