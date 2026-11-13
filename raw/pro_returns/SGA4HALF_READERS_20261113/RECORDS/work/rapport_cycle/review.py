from pathlib import Path
import csv,json,sys,fitz,difflib
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SRC=ROOT/'source'
FIND=list(csv.DictReader((SRC/'check/SOL_FINDINGS.tsv').open(),delimiter='\t'))
PAGES=json.loads((SRC/'check/PAGES.json').read_text())
def review(n):
 p=next((p for p in PAGES if p['label']==str(n) and p['tome']=='1'),None)
 print('\nPRINTED PAGE',n)
 if p:
  print('BASE LINES',p['lines'],p['tex'])
  a=(SRC/'fr/codex_dip'/Path(p['tex']).name).read_text().splitlines()
  lo,hi=p['lines'];print('\n'.join(f'{i+1}: {a[i]}' for i in range(max(0,lo-1),min(len(a),hi))))
 for r in FIND:
  if r['printed_page']==str(n):
   print(json.dumps({k:r[k] for k in ['id','kind','where','scan_reading','tex_reading','fix_old','fix_new','corrected','note']},ensure_ascii=False))
 pdfno=n+5 if n<=109 else n+39
 dst=OUT/'images'/f'p{n:03}.png'
 if not dst.exists():
  doc=fitz.open(SRC/'scan/Number32.pdf');page=doc[pdfno-1]
  pix=page.get_pixmap(matrix=fitz.Matrix(2.4,2.4),alpha=False)
  pix.save(dst)
 print('IMAGE',dst)
if __name__=='__main__':
 for n in map(int,sys.argv[1:]):review(n)
