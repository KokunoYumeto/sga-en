"""Nearest-neighbour display enlargement of an existing scan crop; no new detail."""
from pathlib import Path
from PIL import Image
import sys
root=Path(__file__).resolve().parent
src,dest,factor=sys.argv[1:]
im=Image.open(root/src)
factor=int(factor)
im.resize((im.width*factor,im.height*factor),Image.Resampling.NEAREST).save(root/dest)
