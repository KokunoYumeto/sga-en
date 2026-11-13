"""Reproducible scan-verdict journal; called only for manually inspected pages."""
from pathlib import Path
import json,csv,re
W=Path(__file__).parent
SOL={r['id']:r for r in json.loads((W/'sol_input.json').read_text())}
D=[]; P=[]; O=[]; V=[]; OPS=[]
def key(n):return f'S45-SOL-{n:04d}'
def dec(n,reason,verdict='accepted',reading=None,new=None):
 r=SOL[key(n)]
 d=dict(id=r['id'],printed_page=r['printed_page'],pdf_page=r['pdf_page'],verdict=verdict,printed_reading=reading or r['scan_reading'],image=f"scan/Number32.pdf#page={r['pdf_page']}",region=r['where'],change_made=(new if new is not None else (r['corrected'] if r['kind']=='misprint_in_print' else r['fix_new'])) if verdict!='rejected' else '',forms_affected='French and English: diplomatic/corrected/reading as applicable',reason=reason,kind=r['kind'],fix_old=r['fix_old'],fix_new=new if new is not None else r['fix_new'],codex_ids=[])
 D.append(d)
 if verdict!='rejected' and r['fix_old'] and r['kind']!='page_cut':
  OPS.append(dict(lang='fr',page=int(r['printed_page']),id=r['id'],old=r['fix_old'],new=new if new is not None else r['fix_new'],mode='repair'))
 return d

def page(p,fr,en,reason='',math=False,after_fr=None,after_en=None):
 P.append(dict(printed_page=str(p),pdf_page=p+39,checked_against_scan=True,findings=sum(1 for d in D if int(d['printed_page'])==p)+sum(1 for o in O if o['page']==p),start_fr=fr,start_en=en,reason=reason or 'Full printed page read against the French source; page start located directly from the scan.',math=math,after_fr=after_fr,after_en=after_en))

def variant(n,old,printed,corrected,en_old=None,en_printed=None,en_corrected=None,reason=None,prefix=''):
 sid=key(n) if isinstance(n,int) else n
 d=next((d for d in D if d['id']==sid),None)
 p=int(d['printed_page']) if d else next(o['page'] for o in O if o['id']==sid)
 V.append(dict(id=sid,source=sid,page=p,place=d['region'] if d else next(o['place'] for o in O if o['id']==sid),printed=printed,corrected=corrected,reason=reason or (d['reason'] if d else next(o['reason'] for o in O if o['id']==sid)),kind='misprint_in_print',english_applicable=en_old is not None,english_printed=en_printed,english_corrected=en_corrected))
 OPS.append(dict(lang='fr',page=p,id=sid,old=old,new=prefix+'\\var{'+printed+'}{'+corrected+'}{'+sid+'}',mode='variant'))
 if en_old is not None: OPS.append(dict(lang='en',page=p,id=sid,old=en_old,new=prefix+'\\var{'+en_printed+'}{'+en_corrected+'}{'+sid+'}',mode='variant'))

def en(n,old,new,page=None):
 sid=key(n) if isinstance(n,int) else n
 if page is None:page=int(SOL[sid]['printed_page'])
 OPS.append(dict(lang='en',page=page,id=sid,old=old,new=new,mode='repair'))

def own(p,place,printed,tex,change,kind,reason,fr_old=None,fr_new=None,en_old=None,en_new=None):
 sid=f'S45-ASTRA-V-{len(O)+1:04d}'
 O.append(dict(id=sid,page=p,place=place,printed_reading=printed,tex_reading=tex,change=change,kind=kind,reason=reason))
 if fr_old is not None:OPS.append(dict(lang='fr',page=p,id=sid,old=fr_old,new=fr_new,mode='repair'))
 if en_old is not None:en(sid,en_old,en_new,page=p)
 return sid

def save():
 for page_row in P:
  p=int(page_row['printed_page'])
  page_row['findings']=sum(int(d['printed_page'])==p for d in D)+sum(o['page']==p for o in O)
 for d in D:
  ops=[o for o in OPS if o['id']==d['id']]
  vv=next((v for v in V if v['id']==d['id']),None)
  if d['verdict']=='rejected':d['forms_affected']='none'
  elif d['kind'] in ['marker','page_cut']:
   d['forms_affected']='FR and EN: page-boundary markers in all three forms'
  elif vv:
   d['forms_affected']='FR: diplomatic retains printed; corrected and reading correct'
   d['forms_affected']+=('; EN: diplomatic retains printed; corrected and reading correct' if vv['english_applicable'] else '; EN: no semantic difference')
  else:d['forms_affected']='FR: all three forms'+('; EN: all three forms' if any(o['lang']=='en' for o in ops) else '; EN: existing translation already expresses the print')
 for v in V:
  if v['id']=='S45-SOL-1035':
   for k in ['printed','corrected','english_printed','english_corrected']:v[k]=v[k].replace(r'\item ','')
 for name,rows in [('decisions',D),('pages',P),('own_findings',O),('variants',V)]:
  (W/(name+'.jsonl')).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
 (W/'operations.json').write_text(json.dumps(OPS,ensure_ascii=False,indent=2))
 print('SAVED',len(D),'decisions',len(P),'pages',len(O),'own findings',len(V),'variants',len(OPS),'operations')
