"""Render an explicitly chosen main-scan region; never changes review status."""
import sys
from pathlib import Path
import fitz
here=Path(__file__).resolve().parent;root=here.parents[1]
folio=int(sys.argv[1]);name=sys.argv[2]
box=fitz.Rect(*map(float,sys.argv[3:7]));scale=float(sys.argv[7]) if len(sys.argv)>7 else 6
doc=fitz.open(root/'scan/SGA6_scan_360dpi.pdf')
doc[folio+13].get_pixmap(matrix=fitz.Matrix(scale,scale),clip=box).save(here/name)
