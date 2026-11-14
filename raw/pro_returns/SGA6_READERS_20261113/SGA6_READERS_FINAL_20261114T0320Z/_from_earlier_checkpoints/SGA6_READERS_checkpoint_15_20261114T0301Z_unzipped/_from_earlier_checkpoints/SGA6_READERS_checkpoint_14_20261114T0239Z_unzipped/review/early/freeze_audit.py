"""Audit the completed Exposé 0 evidence without inferring scan decisions.

This script counts and cross-links decisions already made from images. It never
marks a page as read or creates a reading from source metadata.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess
import sys

O=Path(__file__).resolve().parent
R=O.parents[1]
def read_json(path): return json.loads(path.read_text())
def read_rows(path): return [json.loads(s) for s in path.read_text().splitlines()]
def save_json(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

# The three tagged records refer explicitly to the same source passages as their
# queue records. Preserve independent stable IDs and the exact shared evidence.
extra=read_json(O/'extra_decisions.json')
existing={r['source_id'] for r in extra}
records=read_rows(O/'decisions.jsonl')
by_id={r['source_id']:r for r in records}
for tagged,queue in [(314,165),(315,166),(316,167)]:
    sid=f'fixes/RECONCILE_CODEX_6.json#{tagged}'
    qid=f'fixes/RECONCILE_CODEX_6.json#{queue}'
    if sid not in existing:
        row=dict(by_id[qid])
        row.update(source_id=sid,related_finding=qid,
                   region='same inspected passage as queue record; corresponding SGA-SRC tag',
                   reason=row['reason']+' The tagged passage in each Codex tree was compared with its queue record and carries the identical corrected reading.')
        extra.append(row)
save_json(O/'extra_decisions.json',extra)
subprocess.run([sys.executable,str(O/'record_review.py')],check=True)
subprocess.run([sys.executable,str(O/'validate_review.py')],check=True)
records=read_rows(O/'decisions.jsonl')
ids={r['source_id'] for r in records}
expected={}
def add_group(label,path,rows,predicate):
    wanted=[str(path.relative_to(R))+f'#{i}' for i,x in enumerate(rows,1) if predicate(x)]
    expected[label]={'expected':len(wanted),'decided':sum(s in ids for s in wanted),
                     'missing':[s for s in wanted if s not in ids], 'source_ids':wanted}
def early(x): return isinstance(x.get('page'),int) and 1<=x['page']<=77
finding_ids=[]
for path in sorted((R/'check/findings').glob('findings_*.json')):
    finding_ids.extend(str(path.relative_to(R))+f'#{i}' for i,x in enumerate(read_json(path),1) if early(x))
expected['checker']={'expected':len(finding_ids),'decided':sum(s in ids for s in finding_ids),'missing':[s for s in finding_ids if s not in ids],'source_ids':finding_ids}
for name in ['FIXLOG_6.jsonl','FIXLOG_6_CURRENT.jsonl','MISPRINTS_6.json','REPLAY_MANUAL_6.json']:
    path=R/'fixes'/name
    a=read_rows(path) if path.suffix=='.jsonl' else read_json(path)
    add_group(name,path,a,early)
manual_ids=[]
for path in sorted((R/'fixes/MANUAL_6_findings').glob('*.json')):
    manual_ids.extend(str(path.relative_to(R))+f'#{i}' for i,x in enumerate(read_json(path),1) if early(x))
expected['hand_placed_findings']={'expected':len(manual_ids),'decided':sum(s in ids for s in manual_ids),'missing':[s for s in manual_ids if s not in ids],'source_ids':manual_ids}
path=R/'fixes/RECONCILE_CODEX_6.json'
entries=read_json(path)['entries']
early_codex_ids={x['id'] for x in entries if x.get('expose')=='0'}
add_group('Codex queue and tagged records',path,entries,lambda x:x['id'] in early_codex_ids)
hold_ids=[f'fr/codex/HOLD_VS_CORR.json#{i}' for i in range(4,35)]
expected['HOLD actual early passages']={'expected':len(hold_ids),'decided':sum(s in ids for s in hold_ids),'missing':[s for s in hold_ids if s not in ids],'source_ids':hold_ids}

pages=read_rows(O/'page_status.jsonl')
patches=read_rows(O/'patches.jsonl')
errors=[{'missing_group':k,'ids':v['missing']} for k,v in expected.items() if v['missing']]
if [p['page'] for p in pages]!=list(range(1,78)): errors.append('Page statuses are not exactly 1–77 in order.')
if not all(p['fully_checked'] for p in pages): errors.append('A page in the frozen range is not fully checked.')
for row in records+patches+pages:
    value=json.dumps(row,ensure_ascii=False)
    if re.search(r'(?:/workspace/|/home/|/Users/|[A-Za-z]:\\|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,})',value):
        errors.append({'private_reference':row.get('source_id',row.get('page'))})
audit={'scope':'Exposé 0 and appendix, printed folios 1–77',
       'main_scan':'scan/SGA6_scan_360dpi.pdf; physical PDF page=folio+14',
       'witness':'scan/SGA6_witness_300dpi.djvu; physical page=folio+11; only regions specified in individual records were compared',
       'fully_checked_pages':[p['page'] for p in pages],
       'witness_used_on_folios':[p['page'] for p in pages if p['witness_viewed']],
       'counts':{'decisions':len(records),'patches':len(patches),'fully_checked_pages':len(pages),
                 'record_types':dict(Counter(r['record_type'] for r in records)),
                 'patch_layers':dict(Counter(r['layer'] for r in patches)),
                 'verdicts':dict(Counter(r['verdict'] for r in records))},
       'source_coverage':expected,
       'out_of_scope_mappings':[{'source_id':'fr/codex/HOLD_VS_CORR.json#35','nominal_packet':75,'actual_folio':85,'disposition':'Referred to Exposé I reviewer, who reports a separate source-linked decision.'}],
       'unresolved_in_scope':[],
       'errors':errors}
save_json(O/'coverage_audit.json',audit)
if errors:
    print(json.dumps({'errors':errors},ensure_ascii=False));raise SystemExit(1)
names=['decisions.jsonl','patches.jsonl','page_status.jsonl','coverage_audit.json','validation.json',
       'record_review.py','validate_review.py','freeze_audit.py','extra_decisions.json',
       'extra_patches.json','extra_pages.json','record_overrides.json']
names+=sorted(p.name for p in O.glob('evidence_*.json'))
names+=sorted(p.name for p in O.glob('add_batch_*.py'))
names+=['add_author_labels_001_060.py','render_review.py','render_witness.py','crop_image.py']
if (O/'FROZEN_HANDOFF.md').exists(): names.append('FROZEN_HANDOFF.md')
manifest=['path\tbytes\tsha256']
for name in names:
    p=O/name
    manifest.append(f'{p.relative_to(R)}\t{p.stat().st_size}\t{hashlib.sha256(p.read_bytes()).hexdigest()}')
(O/'frozen_manifest.tsv').write_text('\n'.join(manifest)+'\n')
print(json.dumps({'frozen':True,'counts':audit['counts'],'coverage_errors':0},ensure_ascii=False))
