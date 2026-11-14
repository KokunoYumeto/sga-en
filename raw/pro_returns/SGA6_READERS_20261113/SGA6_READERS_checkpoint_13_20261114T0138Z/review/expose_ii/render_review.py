"""Render overlapping page strips and extract marker-delimited layer text.

Rendering prepares evidence only; it does not mark a page as reviewed.
Usage: python render_review.py FIRST LAST
"""
from pathlib import Path
import re,sys
import fitz
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
first,last=map(int,sys.argv[1:3])
pat=re.compile(r'^%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+(\d+)\s*%+.*$',re.M)
for layer in ['diplomatic','current']:
 s=(R/'fr/sga6'/layer/'main.tex').read_text();matches=list(pat.finditer(s))
 for i,m in enumerate(matches):
  p=int(m.group(2))
  if first<=p<=last:
   (O/f'page_{p:03}_{layer}.tex').write_text(s[m.start():matches[i+1].start() if i+1<len(matches) else len(s)])
d=fitz.open(R/'scan/SGA6_scan_360dpi.pdf')
for p in range(first,last+1):
 page=d[p+13];w,h=page.rect.width,page.rect.height
 for i in range(4):
  box=fitz.Rect(0,max(0,h*i/4-8),w,min(h,h*(i+1)/4+8))
  page.get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=box).save(O/f'page_{p:03}_s{i+1}.png')
print(f'Rendered and extracted folios {first}–{last}; no review status changed.')
