from pathlib import Path
import csv,json
OUT=Path(__file__).resolve().parent
SRC=OUT.parents[1]/'source'
SOL={r['id']:r for r in csv.DictReader((SRC/'check/SOL_FINDINGS.tsv').open(),delimiter='\t')}
def append(name,obj):
 with (OUT/name).open('a',encoding='utf-8') as f:f.write(json.dumps(obj,ensure_ascii=False)+'\n')
def page(n,start_fr,ids,*,start_en='',overrides=None,reason='',own=None):
 overrides=overrides or {}; own=own or []
 for num in ids:
  ident=f'S45-SOL-{num:04}' if isinstance(num,int) else num
  r=SOL[ident];o=overrides.get(num,overrides.get(ident,{}))
  row=dict(id=ident,printed_page=str(n),pdf_page=n+5 if n<=109 else n+39,
   verdict='accepted',printed_reading=r['scan_reading'],image='scan/Number32.pdf',
   region=f'PDF page {n+5 if n<=109 else n+39}; '+r['where'],
   change_made=r['fix_new'] or r['corrected'],forms_affected='FR all; EN if translated content changes' if r['kind']!='misprint_in_print' else 'FR corrected/apparatus and reading; EN corrected/apparatus and reading if semantic',
   reason='Direct scan comparison at the cited locus confirms '+r['scan_reading']+'. '+r['note'],
   kind=r['kind'],fix_old=r['fix_old'],fix_new=r['fix_new'],corrected_reading=r['corrected'],tex_file=r['tex_file'],tex_lines=r['tex_lines'],codex_ids=[])
  row.update(o);append('decisions.jsonl',row)
 for item in own:append('own_findings.jsonl',dict(page=str(n),**item))
 append('pages.jsonl',dict(printed_page=str(n),pdf_page=n+5 if n<=109 else n+39,
  checked_against_scan=True,findings=len(ids)+len(own),start_fr=start_fr,start_en=start_en,
  reason=reason or 'Full printed page visually read against the French TeX; page beginning and end settled against the page image. Miller sheaf and functor conventions retained where they preserve the distinction in the print.'))
def variant(ident,page,old,printed,corrected,reason,*,english_applicability=False,place='',kind='misprint_in_print'):
 append('variants.jsonl',dict(id=ident,page=str(page),old=old,printed=printed,corrected=corrected,reason=reason,english_applicability=english_applicability,place=place,kind=kind))
def extra(ident,page,old,new,reason,kind='missing',place=''):
 append('patches.jsonl',dict(id=ident,page=str(page),old=old,new=new,reason=reason,kind=kind,place=place))
