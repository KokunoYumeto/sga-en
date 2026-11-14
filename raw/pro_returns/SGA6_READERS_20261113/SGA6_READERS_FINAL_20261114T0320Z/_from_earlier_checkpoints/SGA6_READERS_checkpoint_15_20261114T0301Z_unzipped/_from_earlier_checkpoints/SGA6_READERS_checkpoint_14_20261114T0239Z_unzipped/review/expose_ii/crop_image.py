"""Reproducible crop utility: image-name output-name left top right bottom."""
from pathlib import Path
import sys
from PIL import Image
O=Path(__file__).resolve().parent
src,dest,*xy=sys.argv[1:]
Image.open(O/src).crop(tuple(map(int,xy))).save(O/dest)
