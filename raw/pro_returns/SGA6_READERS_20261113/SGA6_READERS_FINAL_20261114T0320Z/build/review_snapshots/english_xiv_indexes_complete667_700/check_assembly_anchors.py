#!/usr/bin/env python3
"""Check exact sequential apparatus anchors without writing shared readers."""
from pathlib import Path
import json,re,hashlib
H=Path(__file__).resolve().parent
chunks=[]
for path in H.glob('EN_*_P*.tex'):
    m=re.fullmatch(r'EN_.*_P(\d{3})_(\d{3})\.tex',path.name)
    if m:chunks.append((int(m[1]),int(m[2]),path))
chunks.sort();text=''.join(p.read_text() for _,_,p in chunks);raw=text
rows=[]
for v in map(json.loads,(H/'variants.jsonl').read_text().splitlines()):
    a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v['scope_end'] else len(text)
    part=text[a:b];n=part.count(v['old']);assert n==1,(v['id'],n)
    if v['mode']=='display':
        replacement=('% SGA display variant '+v['id']+'\n'
            +r'\SGACaptureAppState{'+v['id']+'}%\n'
            +r'\ifnum\SGAReaderForm=1\relax\SGAAppMark{'+v['id']+r'}\fi'+'\n'
            +r'\ifnum\SGAReaderForm=0\relax'+'\n'+v['printed']+'\n'
            +r'\else'+'\n'+v['corrected']+'\n'+r'\fi')
    else:replacement=r'\var{'+v['printed']+'}{'+v['corrected']+'}{'+v['id']+'}'
    text=text[:a]+part.replace(v['old'],replacement,1)+text[b:]
    rows.append(dict(id=v['id'],page=v['page'],mode=v['mode'],exact_anchor_count=n))
result=dict(scope=[chunks[0][0],chunks[-1][1]],raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),status='all exact sequential apparatus anchors pass; no PDF compilation claimed',variants=rows)
(H/'assembly_anchor_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(scope=result['scope'],variant_anchors=len(rows),status='pass')))
