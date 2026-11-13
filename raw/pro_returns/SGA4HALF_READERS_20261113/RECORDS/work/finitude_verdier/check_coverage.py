"""Check every late-part finding against the final annotated FR/EN components.

Manual witnesses are exact, page-scoped excerpts selected by human review.
Missing or obsolete witnesses remain unresolved; the script never invents one.
"""
from pathlib import Path
import sys,json,re,csv,collections
W=Path(__file__).resolve().parent
ROOT=W.parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from edition_tex import commands

def rows(name):return [json.loads(s) for s in (W/name).read_text().splitlines() if s.strip()]
def norm(s):return re.sub(r'\s+',' ',s).strip()
def select(s,mode):
    for v in reversed(commands(s,'var',3,optional=True)):
        s=s[:v['start']]+v['args'][0 if mode==0 else 1]+s[v['end']:]
    return s

FILES={};PAGES={}
for lang in ['fr','en']:
    FILES[lang]={};PAGES[lang]={}
    for part in ['7','8','erratum']:
        p=W/lang/(f'sga4.5-{part}.tex' if lang=='fr' else f'sga4half_{part}_en.tex')
        s=p.read_text();FILES[lang][part]=(p,s)
        marks=list(re.finditer(r'\\(?:PrintPage|MathPage)\{(\d+)\}',s))
        for i,m in enumerate(marks):
            end=marks[i+1].start() if i+1<len(marks) else len(s)
            PAGES[lang][int(m[1])]={'source_file':p.relative_to(ROOT).as_posix(),'text':s[m.start():end]}

D=rows('decisions.jsonl');O=rows('own_findings.jsonl');V={r['id']:r for r in rows('variants.jsonl')}
OPS=json.loads((W/'operations.json').read_text())
REPORT=json.loads((W/'build_report.json').read_text())
WITNESSES={}
for p in W.glob('coverage_witnesses_*.json'):
    data=json.loads(p.read_text())
    lang='en' if '_en' in p.stem else 'fr'
    for sid,entry in data.items():
        if (lang,sid) in WITNESSES:raise ValueError(('duplicate witness',lang,sid,p))
        WITNESSES[lang,sid]=entry

def context(text,witness):
    a=norm(text);b=norm(witness);i=a.find(b)
    return a[max(0,i-100):i+len(b)+160] if i>=0 else ''

def literal_evidence(lang,page,witness,mode=1):
    text=PAGES[lang][page]['text'];chosen=select(text,mode)
    if norm(witness) not in norm(chosen):return None
    return dict(page=page,form='diplomatic' if mode==0 else 'corrected/reading',witness=witness,context=context(chosen,witness))

def repair_evidence(lang,page,after):
    text=PAGES[lang][page]['text'];variants=commands(text,'var',3,optional=True);evidence=[]
    for mode in [0,1]:
        candidate=select(after,mode)
        ev=literal_evidence(lang,page,candidate,mode)
        if ev is None:
            # A later, separately recorded print correction can alter a portion
            # of an earlier shared repair; project that explicit variant only.
            for v in variants:
                a,b,_=v['args'];old,new=(b,a) if mode==0 else (a,b)
                if old and old in candidate:candidate=candidate.replace(old,new)
            ev=literal_evidence(lang,page,candidate,mode)
        if ev is None:return None
        evidence.append(ev)
    return evidence

coverage=[]
for finding in D+O:
    sid=finding['id'];page=int(finding.get('printed_page',finding.get('page')))
    verdict=finding.get('verdict','own finding')
    for lang in ['fr','en']:
        row=dict(id=sid,source_id=sid,printed_page=page,language=lang,status='unresolved',classification='',verdict=verdict,kind=finding['kind'],source_file=PAGES[lang][page]['source_file'],evidence=[],reason=finding.get('reason',''))
        op_reports=[r for r in REPORT if r['id']==sid and r['lang']==lang]
        if op_reports:
            row['classification']='reviewed source operation'
            ok=True
            for op in op_reports:
                op_page=int(op.get('page',page))
                if op['status']!='applied':ok=False;row['evidence'].append(dict(error='operation failed',operation=op));continue
                before=op.get('before','');after=op.get('after','')
                if after:
                    ev=repair_evidence(lang,op_page,after)
                    if ev is None:ok=False;row['evidence'].append(dict(error='final operation reading not found',after=after))
                    else:row['evidence'].extend(ev)
                else:
                    texts=[select(PAGES[lang][op_page]['text'],m) for m in [0,1]]
                    absent=all(norm(before) not in norm(t) for t in texts)
                    if not absent:ok=False
                    row['evidence'].append(dict(page=op_page,form='all three forms',deleted_reading=before,absent=absent))
            if sid in V and V[sid].get('english_applicable',False) or sid in V and lang=='fr':row['classification']='single-source printed/corrected variant'
            if ok:row['status']='covered'
        else:
            manual=WITNESSES.get((lang,sid))
            if manual:
                row['classification']=manual.get('classification','existing reading already expresses the print')
                row['witness_explanation']=manual.get('explanation','')
                evidence=manual.get('evidence') or [dict(page=manual.get('page',page),witness=manual['witness'])]
                ok=True
                for e in evidence:
                    p=int(e.get('page',page));w=e['witness']
                    for mode in e.get('modes',[0,1]):
                        ev=literal_evidence(lang,p,w,mode)
                        if ev is None:ok=False;row['evidence'].append(dict(error='manual witness not found',page=p,witness=w,mode=mode))
                        else:row['evidence'].append(ev)
                if ok:row['status']='covered'
            else:row['evidence'].append(dict(error='manual witness pending'))
        coverage.append(row)

unresolved=[dict(id=r['id'],language=r['language'],page=r['printed_page'],classification=r['classification'],errors=[e for e in r['evidence'] if 'error' in e]) for r in coverage if r['status']!='covered']
status=dict(sol_ids=len(D),own_ids=len(O),language_checks=len(coverage),covered_count=len(coverage)-len(unresolved),unresolved_count=len(unresolved),unresolved=unresolved,classification_counts=dict(collections.Counter(r['classification'] for r in coverage)))
(W/'accepted_fix_coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
(W/'accepted_fix_coverage_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
with (W/'accepted_fix_coverage.tsv').open('w',newline='') as f:
    fields=['id','source_id','printed_page','language','status','classification','verdict','kind','source_file','evidence','witness_explanation','reason']
    writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t');writer.writeheader()
    for r in coverage:
        r=dict(r);r['evidence']=json.dumps(r['evidence'],ensure_ascii=False);writer.writerow(r)
print(json.dumps({k:v for k,v in status.items() if k!='unresolved'},ensure_ascii=False,indent=2))
