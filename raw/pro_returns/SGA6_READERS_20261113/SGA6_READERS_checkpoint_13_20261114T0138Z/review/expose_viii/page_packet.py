from pathlib import Path
import re,json,sys,fitz,difflib
R=Path(__file__).resolve().parents[2]
O=R/'review/expose_viii'
pat=r'^%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+(\d+)[^\n]*'
def pages(rel):
 s=(R/rel).read_text(); ms=list(re.finditer(pat,s,re.M)); return {int(m.group(2)):s[m.start():ms[i+1].start() if i+1<len(ms) else len(s)] for i,m in enumerate(ms)}
D={int(q.parent.name):q.read_text() for q in (R/'build/page_packets').glob('*/diplomatic.tex') if q.parent.name.isdigit()}; C={int(q.parent.name):q.read_text() for q in (R/'build/page_packets').glob('*/current.tex') if q.parent.name.isdigit()}
p=int(sys.argv[1]); imgdir=O/'images'; imgdir.mkdir(exist_ok=True)
doc=fitz.open(R/'scan/SGA6_scan_360dpi.pdf'); pg=doc[p+13]
for n,(y0,y1) in enumerate([(0,355),(340,pg.rect.height)],1):
 pix=pg.get_pixmap(matrix=fitz.Matrix(3.5,3.5),clip=fitz.Rect(0,y0,pg.rect.width,y1)); pix.save(imgdir/f'p{p}_{n}.png')
print('DIPLOMATIC\n'+D.get(p,'NO MARKER'))
print('CURRENT DIFFERENCES')
for op,a,b,c,e in difflib.SequenceMatcher(None,D.get(p,''),C.get(p,''),autojunk=False).get_opcodes():
 if op!='equal': print(repr(D.get(p,'')[max(a-30,0):b+30]),' -> ',repr(C.get(p,'')[max(c-30,0):e+30]))
print('RECORDS')
for path in sorted((R/'check/findings').glob('*.json')):
 for i,x in enumerate(json.loads(path.read_text()),1):
  if x.get('page')==p: print(json.dumps({'id':str(path.relative_to(R))+'#'+str(i),**x},ensure_ascii=False))
for name in ['fixes/MISPRINTS_6.json','fixes/REPLAY_MANUAL_6.json']:
 path=R/name; xs=[json.loads(x) for x in path.read_text().splitlines()] if path.suffix=='.jsonl' else json.loads(path.read_text())
 for i,x in enumerate(xs,1):
  if x.get('page')==p: print(json.dumps({'id':name+'#'+str(i),**x},ensure_ascii=False))
