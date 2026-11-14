from pathlib import Path
import re,json,sys,fitz,difflib
R=Path(__file__).resolve().parents[2]
O=R/'review/xiii'
pat=r'^%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+(\d+)[^\n]*'
def pages(rel):
 s=(R/rel).read_text(); ms=list(re.finditer(pat,s,re.M)); return {int(m.group(2)):s[m.start():ms[i+1].start() if i+1<len(ms) else len(s)] for i,m in enumerate(ms)}
D=pages('fr/sga6/diplomatic/main.tex'); C=pages('fr/sga6/current/main.tex')
p=int(sys.argv[1]); imgdir=O/'images'; imgdir.mkdir(exist_ok=True)
doc=fitz.open(R/'scan/SGA6_scan_360dpi.pdf'); pg=doc[p+13]
for n,(y0,y1) in enumerate([(20,355),(340,670)],1):
 pix=pg.get_pixmap(matrix=fitz.Matrix(3.5,3.5),clip=fitz.Rect(20,y0,430,y1)); pix.save(imgdir/f'p{p}_{n}.png')
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
