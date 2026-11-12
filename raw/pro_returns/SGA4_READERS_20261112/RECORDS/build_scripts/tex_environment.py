"""Use the installed TeX Live tree even when its generated databases are absent.

The six standalone readers need no special environment on a standard TeX Live.
This helper repairs the isolated build environment without modifying system files.
"""
from pathlib import Path
import os, shutil, subprocess
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]

@lru_cache(maxsize=1)
def distribution_tree():
    value=subprocess.check_output(['kpsewhich','-var-value=TEXMFDIST'],text=True).strip()
    if not value:raise RuntimeError('TeX Live did not report its distribution tree')
    return Path(value)

def tex_env(force_local=False):
    env = os.environ.copy()
    local = ROOT / 'tmp' / 'texmf'
    # A standard TeX Live uses its own installed formats, font configuration,
    # and search paths. The optional isolated repair is selected only when
    # its complete prepared configuration is present.
    if not force_local and (not (local/'fontconfig.xml').exists() or not (local/'web2c/xelatex.fmt').exists()):
        return env
    local.mkdir(parents=True, exist_ok=True)
    dist=distribution_tree();extra=dist.parent.parent/'texmf'
    env.update(TEXMF='{'+str(local)+','+str(extra)+','+str(dist)+'}',
               TEXMFVAR=str(local), TEXMFCONFIG=str(local),
               TEXFORMATS=str(local/'web2c')+'//:',
               FONTCONFIG_FILE=str(local/'fontconfig.xml'),
               DVIPDFMXINPUTS=str(dist/'dvipdfmx')+'//:',
               OSFONTDIR=str(local/'fonts/opentype')+'//:'+str(extra/'fonts/opentype')+'//:')
    return env

def prepare():
    env = tex_env(force_local=True)
    local = ROOT/'tmp'/'texmf'
    config = local/'tex'/'generic'/'config'
    config.mkdir(parents=True, exist_ok=True)
    source = distribution_tree()/'tex/generic/config/language.us'
    content = source.read_text()
    if (config/'loadhyph-fr.tex').exists():
        content += '\nfrench loadhyph-fr.tex\n'
    (config/'language.dat').write_text(content)
    output = local/'web2c'
    output.mkdir(parents=True, exist_ok=True)
    command = ['xetex','-ini','-etex','-no-parse-first-line','-jobname=xelatex',
               '-progname=xelatex','-interaction=nonstopmode','-halt-on-error','xelatex.ini']
    proc = subprocess.run(command, cwd=output, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Raw engine diagnostics are private intermediates, not deliverable logs.
    (ROOT/'tmp'/'format-bootstrap.out').write_text(proc.stdout)
    if proc.returncode:
        raise RuntimeError('XeLaTeX format bootstrap failed; inspect temporary diagnostics')
    return env

if __name__ == '__main__':
    prepare()
    print('Local XeLaTeX format prepared from installed TeX Live; English and French hyphenation loaded.')
