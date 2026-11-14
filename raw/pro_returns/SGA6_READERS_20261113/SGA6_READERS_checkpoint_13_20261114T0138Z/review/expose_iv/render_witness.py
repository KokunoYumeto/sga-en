"""Render native-resolution witness pages; no review verdicts are generated."""
from pathlib import Path
import os,subprocess,sys
from PIL import Image
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
env=os.environ.copy();env['LD_LIBRARY_PATH']=str(R/'build/apt/local/usr/lib/x86_64-linux-gnu')
for p in map(int,sys.argv[1:]):
 ppm=O/f'witness_{p:03}.ppm'
 subprocess.run([str(R/'build/apt/local/usr/bin/ddjvu'),'-format=ppm',f'-page={p+11}','-scale=300',str(R/'scan/SGA6_witness_300dpi.djvu'),str(ppm)],env=env,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 im=Image.open(ppm);im.save(O/f'witness_{p:03}.png');ppm.unlink()
 print(f'Rendered witness physical page{p+11} for folio{p}.')
