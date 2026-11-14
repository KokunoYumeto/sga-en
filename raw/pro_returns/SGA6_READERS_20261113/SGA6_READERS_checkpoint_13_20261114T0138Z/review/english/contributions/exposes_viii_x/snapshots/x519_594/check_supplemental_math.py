#!/usr/bin/env python3
"""Literal checks for starred math environments and the split1.3.9 display."""
from pathlib import Path
import json,re,hashlib,collections
H=Path(__file__).resolve().parent
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunks=[]
for p in H.glob('EN_*_P*.tex'):
    m=re.fullmatch(r'EN_.*_P(\d+)_(\d+)\.tex',p.name)
    if m:chunks.append((int(m[1]),int(m[2]),p))
chunks.sort();first=chunks[0][0];last=chunks[-1][1]
raw=''.join(p.read_text() for _,_,p in chunks)
variants=[json.loads(x) for x in (H/'variants.jsonl').read_text().splitlines()]
star=re.compile(r'\\begin\{(align\*|equation\*|gather\*|multline\*)\}.*?\\end\{\1\}',re.S)
rows=[]
for layer,key in [('current','corrected'),('diplomatic','printed')]:
    en=raw
    for v in variants:
        a=en.index(v['scope_start']);b=en.index(v['scope_end'],a) if v['scope_end'] else len(en)
        part=en[a:b];assert part.count(v['old'])==1
        en=en[:a]+part.replace(v['old'],v[key],1)+en[b:]
    fr=''.join((H/'source_packets'/str(p)/(layer+'.tex')).read_text() for p in range(first,last+1))
    for unit,n in collections.Counter(m.group() for m in star.finditer(fr)).items():
        actual=sum(m.group()==unit for m in star.finditer(en));assert actual==n,(layer,'starred math',actual,n)
        rows.append(dict(layer=layer,kind='complete starred environment',literal_unit=unit,sha256=sha(unit),French_count=n,English_count=actual))
    assert collections.Counter(m.group() for m in star.finditer(fr))==collections.Counter(m.group() for m in star.finditer(en))
    if first<=526 and last>=527:
        source=''.join((H/'source_packets'/str(p)/(layer+'.tex')).read_text() for p in [526,527])
        clean=re.sub(r'^%%%%%%%%%%[^\n]+\n','',en,flags=re.M)
        clean=re.sub(r'\\SGAPrintPage\{\d+\}%\n','',clean)
        pattern=re.compile(r'\\begin\{equation\}\\tag\{1\.3\.9\}.*?\\end\{equation\}',re.S)
        f=pattern.search(source).group();e=pattern.search(clean).group();assert e==f,(layer,repr(f),repr(e))
        rows.append(dict(layer=layer,kind='complete equation across526–527',literal_unit=f,sha256=sha(f),visible_marker_position='after the closing equation command, before where',decision='Only the source-folio comment lies between the expression and its closing command. Removing that nonprinting comment leaves the complete formula byte-identical to the two concatenated reviewed French page fragments.'))
result=dict(scope=[first,last],status='pass; exact supplemental math blocks only, no rendering claim',rows=rows)
(H/'supplemental_math_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(scope=[first,last],supplemental_checks=len(rows),status='pass')))
