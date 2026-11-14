#!/usr/bin/env python3
"""Verify attached archives and create an auditable, initially unreviewed ledger.

Run from the directory containing fr/, en/, check/, scan/, and conventions/.
Input archive paths are command-line arguments; exported records use archive paths.
No source verification status is inferred from a previous checker's confidence.
"""
import argparse
import bisect
import csv
import hashlib
import io
import json
import re
import zipfile
from collections import Counter
from pathlib import Path

MARKER = re.compile(r'(?m)^%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+([^%\n]+?)\s*%+.*$')

def write_tsv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k,v in row.items()})

def split_pages(text):
    markers = list(MARKER.finditer(text))
    if not markers:
        return {'front': text}, {'front': 0}
    pages = {'front': text[:markers[0].start()]}
    offsets = {'front': 0}
    for i, m in enumerate(markers):
        label = m[2].strip()
        page = int(label) if label.isdigit() else label
        assert page not in pages, 'Duplicate printed-page marker: ' + str(page)
        pages[page] = text[m.start():markers[i+1].start() if i+1 < len(markers) else len(text)]
        offsets[page] = m.start()
    return pages, offsets

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archives', nargs='*', default=[])
    args = parser.parse_args()
    root = Path.cwd()
    records = root / 'records'
    records.mkdir(exist_ok=True)
    manifest_rows = []
    for archive in args.archives:
        p = Path(archive)
        with zipfile.ZipFile(p) as z:
            rows = list(csv.DictReader(io.StringIO(z.read('MANIFEST.tsv').decode('utf-8')), delimiter='\t'))
            for r in rows:
                data = z.read(r['path'])
                actual_hash = hashlib.sha256(data).hexdigest()
                ok = len(data) == int(r['bytes']) and actual_hash == r['sha256']
                manifest_rows.append({'archive':p.name, 'path':r['path'], 'bytes':len(data), 'sha256':actual_hash, 'verified':str(ok).lower(), 'role':r['role']})
                if not ok:
                    raise ValueError('Manifest mismatch: ' + p.name + ':' + r['path'])
    if manifest_rows:
        write_tsv(records/'INPUT_MANIFEST_VERIFIED.tsv', manifest_rows, ['archive','path','bytes','sha256','verified','role'])

    registry = []
    for path in sorted((root/'check/findings').glob('findings_*.json')):
        for i, data in enumerate(read_json(path), 1):
            registry.append({'id':path.relative_to(root).as_posix()+f'#{i}', 'type':'finding', 'page':data['page'], 'data':data})
    for rel in ['fixes/FIXLOG_6.jsonl','fixes/FIXLOG_6_CURRENT.jsonl']:
        for i,line in enumerate((root/rel).read_text().splitlines(),1):
            data=json.loads(line)
            registry.append({'id':rel+f'#{i}','type':'fixlog','page':data['page'],'data':data})
    for rel,kind in [('fixes/MISPRINTS_6.json','misprint'),('fixes/REPLAY_MANUAL_6.json','replay')]:
        for i,data in enumerate(read_json(root/rel),1):
            registry.append({'id':rel+f'#{i}','type':kind,'page':data['page'],'data':data})
    for path in sorted((root/'fixes/MANUAL_6_findings').glob('*.json')):
        for i,data in enumerate(read_json(path),1):
            registry.append({'id':path.relative_to(root).as_posix()+f'#{i}','type':'manual','page':data.get('page',''),'data':data})

    src=(root/'fr/sga6/current/main.tex').read_text()
    pages,offsets=split_pages(src)
    marker_locs=[(src.count('\n',0,m.start())+1,int(m[2])) for m in MARKER.finditer(src)]
    marker_lines=[x[0] for x in marker_locs]
    def line_folio(line):
        i=bisect.bisect_right(marker_lines,line)-1
        return marker_locs[i][1] if i>=0 else 'front'
    for i,data in enumerate(read_json(root/'fr/codex/HOLD_VS_CORR.json'),1):
        registry.append({'id':f'fr/codex/HOLD_VS_CORR.json#{i}','type':'hold_difference','page':line_folio(data['corr_lines'][0]),'data':data})
    reconciliation=read_json(root/'fixes/RECONCILE_CODEX_6.json')
    for key,value in reconciliation.items():
        if isinstance(value,list):
            for i,data in enumerate(value,1):
                if isinstance(data,dict) and data.get('status')=='rejected':
                    page=data.get('page','')
                    registry.append({'id':f'fixes/RECONCILE_CODEX_6.json:{key}#{i}','type':'rejected_codex','page':page,'data':data})
    # This internal registry preserves source data for review. Only sanitized
    # decision exports belong in a release or checkpoint.
    (root/'build/registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
    counts=Counter(x['type'] for x in registry)
    source_counts=Counter(x['data'].get('kind','') for x in registry if x['type']=='finding')
    summary={'manifest_entries_verified':len(manifest_rows),'records_by_type':dict(counts),'findings_by_kind':dict(source_counts),'source_markers':len(offsets)-1,'missing_source_folios':sorted(set(range(1,701))-set(k for k in offsets if isinstance(k,int))),'scan_checks_inferred_from_intake':0}
    (records/'INTAKE_COUNTS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    # Review packets retain one-based source identifiers and exact source text.
    for page,text in pages.items():
        dest=root/'build/page_packets'/str(page)
        dest.mkdir(parents=True,exist_ok=True)
        (dest/'current.tex').write_text(text)
        diplomatic,_=split_pages((root/'fr/sga6/diplomatic/main.tex').read_text()) if page=='front' else (None,None)
        rows=[x for x in registry if x['page']==page]
        (dest/'records.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    diplomatic,_=split_pages((root/'fr/sga6/diplomatic/main.tex').read_text())
    for page,text in diplomatic.items():
        (root/'build/page_packets'/str(page)/'diplomatic.tex').write_text(text)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
