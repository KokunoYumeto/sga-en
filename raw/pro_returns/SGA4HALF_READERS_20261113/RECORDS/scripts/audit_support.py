"""Reproducible source lookup and scan rendering; no automatic verdicts."""
from pathlib import Path
import csv, json, re, difflib
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source'
SOL=list(csv.DictReader((SOURCE/'check/SOL_FINDINGS.tsv').open(encoding='utf-8-sig'),delimiter='\t'))
SOL_BY_ID={r['id']:r for r in SOL}
INDEX={r['printed_page']:r for r in csv.DictReader((SOURCE/'scan/PAGE_INDEX.tsv').open(),delimiter='\t') if r['printed_page'].isdigit() or r['printed_page'] in ('III','IV')}
PAGES={r['label']:r for r in json.loads((SOURCE/'check/PAGES.json').read_text())}
CODEX=list(csv.DictReader((SOURCE/'fr/codex_records/dec.csv').open(encoding='utf-8-sig')))

def render(page, dpi=220):
    import fitz
    name=str(page); target=ROOT/'work/scan_pages'/f'p{name}.png'
    target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():
        doc=fitz.open(SOURCE/'scan/Number32.pdf')
        p=doc[int(INDEX[name]['pdf_page'])-1]
        p.get_pixmap(dpi=dpi,colorspace=fitz.csGRAY).save(target)
    return target

def page_text(page):
    name=str(page)
    if name not in PAGES:
        if name in ('1','2','3'): return (SOURCE/'fr/codex_dip/ariane.tex').read_text()
        if name=='5': return (SOURCE/'fr/codex_dip/toc-i.tex').read_text()
        return 'No source transcription: transcribe from scan.'
    p=PAGES[name]; basename=Path(p['tex']).name
    old=(SOURCE/'fr/miller_src'/basename).read_text().splitlines(True)
    new=(SOURCE/'fr/codex_dip'/basename).read_text().splitlines(True)
    a,b=p['lines']; a-=1
    mapper=difflib.SequenceMatcher(None,old,new,autojunk=False)
    covered=[]
    for kind,i,j,k,l in mapper.get_opcodes():
        if j>a and i<b:
            if kind=='equal': covered.extend(new[k+max(a-i,0):k+min(b-i,j-i)])
            else: covered.extend(new[k:l])
    return ''.join(covered)

def packet(pages):
    for page in pages:
        name=str(page); print('\n### PRINTED PAGE',name,'PDF',INDEX[name]['pdf_page'])
        print('IMAGE',str(render(name).relative_to(ROOT)))
        print('CODEX DIPLOMATIC TEXT\n'+page_text(name))
        print('SOL FINDINGS')
        for r in SOL:
            if r['printed_page']==name: print(json.dumps({k:r[k] for k in ('id','kind','where','scan_reading','tex_reading','fix_old','fix_new','corrected','note')},ensure_ascii=False))

def append_jsonl(path, rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a') as f:
        for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')

def decide(owner, choices):
    """Explicit observed choices only: mapping numeric id -> verdict/reason/overrides."""
    path=ROOT/'work'/owner/'decisions.jsonl'
    existing={r['id'] for r in (json.loads(l) for l in path.read_text().splitlines())} if path.exists() else set()
    rows=[]
    for number,choice in choices.items():
        sid=number if isinstance(number,str) and number.startswith('S45-') else f'S45-SOL-{int(number):04d}'
        if sid in existing: raise ValueError('Duplicate decision '+sid)
        s=SOL_BY_ID[sid]; verdict,reason,*override=choice
        r={'id':sid,'printed_page':s['printed_page'],'pdf_page':s['pdf_page'],'verdict':verdict,'printed_reading':s['scan_reading'],'image':'scan/Number32.pdf','region':s['where'],'change_made':s['fix_new'] or s['corrected'],'forms_affected':'FR all; EN where content changes' if s['kind']!='misprint_in_print' else 'FR corrected and reading; EN corrected and reading where English changes','reason':reason,'kind':s['kind'],'fix_old':s['fix_old'],'fix_new':s['fix_new'],'corrected_reading':s['corrected'],'codex_ids':[]}
        if verdict=='rejected':r['change_made']='';r['forms_affected']='none'
        if override:r.update(override[0])
        rows.append(r)
    append_jsonl(path,rows)

if __name__=='__main__':
    import sys
    packet(sys.argv[1:])
