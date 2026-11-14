#!/usr/bin/env python3
"""Render and display review inputs, without producing any verdict."""
import difflib,json,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'images';OUT.mkdir(exist_ok=True)
registry=json.loads((ROOT/'build/registry.json').read_text())
doc=fitz.open(ROOT/'scan/SGA6_scan_360dpi.pdf')
for page in map(int,sys.argv[1:]):
    doc[page+13].get_pixmap(matrix=fitz.Matrix(3,3)).save(OUT/f'p{page}.png')
    d=(ROOT/f'build/page_packets/{page}/diplomatic.tex').read_text()
    c=(ROOT/f'build/page_packets/{page}/current.tex').read_text()
    print(f'FOLIO {page} DIPLOMATIC\n{d}\nCURRENT DIFFERENCES')
    for tag,a,b,x,y in difflib.SequenceMatcher(None,d,c,autojunk=False).get_opcodes():
        if tag!='equal':print(repr(d[max(0,a-45):b+45]),'→',repr(c[max(0,x-45):y+45]))
    records=[r for r in registry if r.get('page')==page]
    fixes=[r['data']['fix'] for r in records if r['type']=='finding' and r['data'].get('fix')]
    print('FINDINGS AND NON-DUPLICATE SOURCE RECORDS')
    for r in records:
        if r['type']=='misprint':continue
        if r['type']=='fixlog' and any(r['data'].get('old')==f['old'] and r['data'].get('new')==f['new'] for f in fixes):continue
        print(json.dumps(r,ensure_ascii=False))
