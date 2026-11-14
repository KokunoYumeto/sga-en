#!/usr/bin/env python3
"""Pair every printed terminology/notation index row by its exact reference."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from lexical_inventory import pages,read,prose_view,MATH

HERE=Path(__file__).resolve().parent

def index_rows(text):
    # Every data row has two alignment columns and an explicit row terminator.
    # The one wrapped label on695 is retained with its actual internal newline.
    rows=[];pending=''
    for line in text.splitlines():
        if line.lstrip().startswith(('\\SGAPrintPage','\\sgaStableTarget','\\section','\\begin','\\end','\\toprule','\\midrule','\\bottomrule','\\newpage')):continue
        pending += ('\n' if pending else '')+line
        if '\\\\' not in line:continue
        raw,pending=pending.split('\\\\',1)
        if raw.count('&')!=2:continue
        label,expose,section=[v.strip() for v in raw.split('&')]
        if not label:continue
        # Wrappers can precede the first label after the header.
        label=re.sub(r'^.*?\\endhead\s*','',label,flags=re.S)
        if '\\hyperlink' in section:
            m=re.fullmatch(r'\\hyperlink\{([^{}]+)\}\{([^{}]+)\}',section)
            assert m,section
            target,section=m.groups()
        else:target=None
        rows.append(dict(label=label,expose=expose,section=section,target=target))
    return rows

def main():
    f=pages(read('build/FR_current_revised.tex'));e=pages(read('review/english/aggregate/SGA6_EN_raw_current.tex'))
    out=[];ditto=None;ditto_id=None
    for page in range(691,701):
        fr,en=index_rows(f[str(page)]['text']),index_rows(e[str(page)]['text'])
        assert len(fr)==len(en),(page,len(fr),len(en))
        for i,(a,b) in enumerate(zip(fr,en),1):
            # The source references were independently reviewed by the source
            # and index contributors. This pairing preserves that exact state.
            assert a['section']==b['section'],(page,i,a,b)
            assert a['expose']==b['expose'],(page,i,a,b)
            fm=[m.group() for m in MATH.finditer(a['label'])]
            em=[m.group() for m in MATH.finditer(b['label'])]
            assert Counter(fm)==Counter(em),(page,i,'index formula differs',a,b)
            repeat=bool(re.fullmatch(r"\\qquad\s*''(?:\s*\\hspace\{8em\}\s*'')?",a['label']))
            if repeat:
                assert ditto
                assert a['label']==b['label']
                af,bf=ditto
            else:
                af,bf=a['label'],b['label'];ditto=(af,bf);ditto_id=f'EN-TERM-INDEX-{page}-{i:02d}'
            out.append(dict(id=f'EN-TERM-INDEX-{page}-{i:02d}',page=page,row=i,index='terminology' if page<696 else 'notation',
                French_literal_label=a['label'],English_literal_label=b['label'],French_resolved_label=af,English_resolved_label=bf,
                repeated_label=repeat,repeated_label_source=ditto_id if repeat else None,expose=a['expose'],section=a['section'],English_target=b['target'],mathematical_units_identical=True,
                evidence=[f'build/FR_current_revised.tex#folio{page}',f'review/english/aggregate/SGA6_EN_raw_current.tex#folio{page}',
                          'build/review_snapshots/english_xiv_indexes_complete667_700'],
                scope='Exact paired index label and its unchanged source definition locator; no new interpretation of the indexed theorem.'))
    (HERE/'PRINTED_INDEX_PAIRS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(rows=len(out),terminology_rows=sum(r['index']=='terminology' for r in out),notation_rows=sum(r['index']=='notation' for r in out),ditto_rows=sum(r['repeated_label'] for r in out))))

if __name__=='__main__':main()
