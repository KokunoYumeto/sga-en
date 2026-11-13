"""Render a context-only reference page; this never certifies its full review."""
import sys
from pathlib import Path
import fitz
here=Path(__file__).resolve().parent
root=here.parents[1]
folio=int(sys.argv[1]);name=sys.argv[2]
doc=fitz.open(root/'scan/SGA6_scan_360dpi.pdf')
doc[folio+13].get_pixmap(matrix=fitz.Matrix(2,2)).save(here/name)
