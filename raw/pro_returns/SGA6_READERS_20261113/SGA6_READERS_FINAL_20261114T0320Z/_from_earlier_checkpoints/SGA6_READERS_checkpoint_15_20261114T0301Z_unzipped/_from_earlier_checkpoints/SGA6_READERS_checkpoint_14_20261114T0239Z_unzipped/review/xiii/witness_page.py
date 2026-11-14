from pathlib import Path
import subprocess,os,sys
from PIL import Image
R=Path(__file__).resolve().parents[2]; O=R/'review/xiii/images';p=int(sys.argv[1]); env=os.environ.copy(); env['LD_LIBRARY_PATH']=str(R/'build/apt/local/usr/lib/x86_64-linux-gnu')
out=O/f'w{p}.ppm'; subprocess.run([str(R/'build/apt/local/usr/bin/ddjvu'),'-format=ppm',f'-page={p+11}','-scale=300',str(R/'scan/SGA6_witness_300dpi.djvu'),str(out)],env=env,check=True)
im=Image.open(out); print(im.size); w,h=im.size
for n,(a,b) in enumerate([(0,.52),(.48,1)],1): im.crop((0,int(h*a),w,int(h*b))).resize((int(w*.7),int(h*(b-a)*.7))).save(O/f'w{p}_{n}.png')
