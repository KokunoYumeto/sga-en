#!/usr/bin/env python3
"""Seal the completed, audited Exposé V review for checkpoint11."""
from pathlib import Path
import hashlib,json,shutil
src=Path(__file__).resolve().parent
root=src.parents[1]
dst=root/'build/review_snapshots/expose_v_checkpoint11_completed_364'
assert not dst.exists(),'Immutable snapshot already exists'
audit=json.loads((src/'FINAL_AUDIT.json').read_text())
assert audit['scope']==[297,364] and audit['fully_checked_pages']==68
assert not audit['missing_registry_ids']
dst.mkdir(parents=True)
for f in sorted(src.iterdir()):
 if f.is_file():shutil.copy2(f,dst/f.name)
status=dict(audit)
status.update(snapshot='build/review_snapshots/expose_v_checkpoint11_completed_364/',
 live_source='review/expose_v/',last_fully_checked_page=364,
 state='completed source review;immutable snapshot',
 external_streams=['review/middle/patches.jsonl','review/expose_v_rendering/patches.jsonl'])
(dst/'snapshot_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
manifest=[]
for f in sorted(dst.iterdir()):
 if f.is_file():manifest.append(f'{hashlib.sha256(f.read_bytes()).hexdigest()}\t{f.stat().st_size}\t{f.name}\n')
(dst/'snapshot_manifest.tsv').write_text(''.join(manifest))
for f in dst.iterdir():f.chmod(0o444)
dst.chmod(0o555)
print(json.dumps({'snapshot':status['snapshot'],'fully_checked_pages':68,
 'source_decisions':audit['source_decisions'],'own_findings':audit['own_findings'],
 'patch_records':audit['patch_records'],'registry_rows':audit['nominal_registry_rows'],
 'manifest_entries':len(manifest),
 'manifest_sha256':hashlib.sha256((dst/'snapshot_manifest.tsv').read_bytes()).hexdigest()},ensure_ascii=False))
