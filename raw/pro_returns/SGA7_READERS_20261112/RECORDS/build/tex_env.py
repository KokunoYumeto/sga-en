"""Workspace-local TeX configuration; no system files are changed."""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def environment():
    env = os.environ.copy()
    # Discover the installed distribution instead of embedding machine paths.
    # Removing !! permits ordinary directory lookup when a runtime's ls-R
    # database is absent; the edition-local tree stays first in the search.
    trees = subprocess.run(['kpsewhich','-expand-var=$TEXMF'],env=env,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                           text=True,check=True).stdout.strip().replace('!!','')
    if trees.startswith('{') and trees.endswith('}'):
        trees=trees[1:-1]
    env['TEXMF'] = '{' + str(ROOT/'work/texmf') + ',' + trees + '}'
    env['TEXMFVAR'] = str(ROOT/'work/texmf-var')
    env['TEXMFCONFIG'] = str(ROOT/'work/texmf-config')
    env['TEXMFHOME'] = str(ROOT/'work/texmf-home')
    env['TEXFORMATS'] = str(ROOT/'work/texmf/web2c') + ':'
    env['TEXFONTMAPS'] = str(ROOT/'work/texmf/fonts/map') + '//:'
    env['SOURCE_DATE_EPOCH'] = '1794484800'
    env['FORCE_SOURCE_DATE'] = '1'
    return env


def setup():
    d = ROOT/'work/texmf/web2c'
    d.mkdir(parents=True, exist_ok=True)
    if not (d/'pdflatex.fmt').exists():
        r = subprocess.run(['pdftex','-ini','-interaction=nonstopmode','-halt-on-error','-jobname=pdflatex',
                            '-progname=pdflatex','-translate-file=cp227.tcx','*pdflatex.ini'],
                           cwd=d,env=environment(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (d/'format_setup.log').write_text(r.stdout)
        print(r.stdout[-3000:])
        if r.returncode: raise RuntimeError('Unable to generate the local pdfLaTeX format')


if __name__ == '__main__':
    setup()
