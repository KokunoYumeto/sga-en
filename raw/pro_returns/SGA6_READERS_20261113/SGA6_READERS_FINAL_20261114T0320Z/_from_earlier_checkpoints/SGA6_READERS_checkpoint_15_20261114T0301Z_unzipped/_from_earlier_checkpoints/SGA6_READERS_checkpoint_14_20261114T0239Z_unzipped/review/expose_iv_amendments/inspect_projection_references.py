#!/usr/bin/env python3
"""Render regional reference evidence without modifying frozen IV or III."""
from pathlib import Path
from PIL import Image
import fitz
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
doc=fitz.open(ROOT/'scan/SGA6_scan_360dpi.pdf')
for page,rect in ((287,(15,320,435,470)),(289,(15,35,435,180)),(272,(20,260,425,300)),(273,(15,40,430,380))):
 doc[page+13].get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(rect),alpha=False).save(HERE/f'main_{page}_reference.png')
Image.open(ROOT/'review/expose_iv/witness_287.png').crop((30,1370,1970,2000)).save(HERE/'witness_287_reference.png')
Image.open(ROOT/'review/expose_iv/witness_289.png').crop((30,100,1970,780)).save(HERE/'witness_289_reference.png')
print('Rendered regional reference evidence; no page status changed.')
