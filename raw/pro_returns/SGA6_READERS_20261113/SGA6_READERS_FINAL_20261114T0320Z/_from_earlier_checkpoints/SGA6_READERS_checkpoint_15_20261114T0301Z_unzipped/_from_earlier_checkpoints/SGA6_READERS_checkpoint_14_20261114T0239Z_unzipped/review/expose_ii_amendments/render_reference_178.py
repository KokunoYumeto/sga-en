#!/usr/bin/env python3
from pathlib import Path
import os,subprocess
from PIL import Image
import fitz
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
doc=fitz.open(ROOT/'scan/SGA6_scan_360dpi.pdf')
page=doc[178+13]
page.get_pixmap(matrix=fitz.Matrix(5,5),clip=fitz.Rect(25,255,418,400)).save(HERE/'main_178_reference.png')
env=os.environ.copy();env['LD_LIBRARY_PATH']=str(ROOT/'build/apt/local/usr/lib/x86_64-linux-gnu')
ppm=HERE/'witness_178.ppm'
subprocess.run([str(ROOT/'build/apt/local/usr/bin/ddjvu'),'-format=ppm','-page=189','-scale=300',str(ROOT/'scan/SGA6_witness_300dpi.djvu'),str(ppm)],env=env,check=True)
im=Image.open(ppm);im.save(HERE/'witness_178.png');im.crop((80,1080,1920,1760)).save(HERE/'witness_178_reference.png');ppm.unlink()
