#!/usr/bin/env python3
"""Run standard TeX Live binaries using the optional isolated package tree.

On a complete TeX Live installation no environment override is needed.
The isolated tree is an execution aid and is not required by the readers.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def tex_environment():
    env = dict(os.environ)
    local = ROOT/'build/texlive'
    dist = local/'usr/share/texlive/texmf-dist'
    if not dist.is_dir():
        return env
    var = ROOT/'build/texmf-var'
    config = ROOT/'build/texmf-config'
    var.mkdir(exist_ok=True)
    config.mkdir(exist_ok=True)
    env.update({
        'TEXMFDIST':str(dist),
        'TEXMFROOT':str(local/'usr/share/texlive'),
        'TEXMFLOCAL':str(local/'usr/share/texmf'),
        'TEXMFVAR':str(var),
        'TEXMFSYSVAR':str(var),
        'TEXMFCONFIG':str(config),
        'TEXMFSYSCONFIG':str(config),
        'TEXMF':'{'+str(config)+','+str(var)+','+str(local/'usr/share/texmf')+','+str(dist)+'}',
        'TEXFORMATS':str(var)+'/web2c//:',
        'TEXFONTMAPS':str(var)+'/fonts/map//:'+str(dist)+'/fonts/map//:'+str(local/'usr/share/texmf')+'/fonts/map//:',
    })
    return env

if __name__=='__main__':
    if len(sys.argv)<2:
        raise SystemExit('Usage: tex_environment.py command [args]')
    raise SystemExit(subprocess.run(sys.argv[1:],env=tex_environment()).returncode)
