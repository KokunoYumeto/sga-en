#!/usr/bin/env python3
"""Copy frozen09 and amend only331; never include later live folios."""
from pathlib import Path
import hashlib,json,shutil
src=Path(__file__).resolve().parent;root=src.parents[1]
prior=root/'build/review_snapshots/expose_v_checkpoint09_through340'
dst=root/'build/review_snapshots/expose_v_checkpoint09_through340_integrated'
assert not dst.exists()
before=hashlib.sha256((prior/'snapshot_manifest.tsv').read_bytes()).hexdigest()
assert before=='b5e768d6bd1c7e35a2c3cb305bda20d34b617eda424807c5f980f6ebb93d210e'
dst.mkdir(parents=True)
for f in prior.iterdir():
 if f.is_file() and f.name not in ['snapshot_manifest.tsv','snapshot_status.json','FROZEN_HANDOFF.md']:
  shutil.copy2(f,dst/f.name)
def load(folder,name):return [json.loads(x) for x in (folder/name).read_text().splitlines() if x.strip()]
for name in ['decisions.jsonl','own_findings.jsonl','patches.jsonl','page_status.jsonl']:
 old=load(prior,name);live=load(src,name)
 # Preserve the frozen ordering and every record outside actual331 exactly.
 output=[];inserted=False
 for row in old:
  if int(row['page'])==331:
   if not inserted:output.extend(x for x in live if int(x['page'])==331);inserted=True
  else:output.append(row)
 assert len(output)==len(old),(name,len(output),len(old))
 assert [x for x in output if int(x['page'])!=331]==[x for x in old if int(x['page'])!=331]
 assert all(297<=int(x['page'])<=340 for x in output)
 f=dst/name;f.chmod(0o644);f.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in output))
for name in ['review_helpers.py','integration_amendment_331.json','integrate_snapshot_checkpoint09.py']:
 f=dst/name
 if f.exists():f.chmod(0o644)
 shutil.copyfile(src/name,f)
summary=json.loads((prior/'snapshot_status.json').read_text())
summary['snapshot']='build/review_snapshots/expose_v_checkpoint09_through340_integrated/'
summary['integration_amendment']={
 'page':331,
 'packet':'integration_amendment_331.json',
 'earlier_stream':'review/middle/patches.jsonl',
 'source_id':'fixes/MANUAL_6_findings/MANUAL_6_findings_326_330.json#1',
 'change':'The current plain-number patch now expects the undotted heading produced by the earlier middle replay. Both layers retain3.10 without a terminal stop.',
 'scope':'Only actual331 records and validation metadata differ from the first09 snapshot. No live341+ record or evidence has been added.',
 'prior_snapshot_manifest_sha256':before
}
summary['exact_calculation_and_claim_packets'].append('integration_amendment_331.json')
(dst/'snapshot_status.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
handoff=(prior/'FROZEN_HANDOFF.md').read_text()
handoff=handoff.replace('# Exposé V checkpoint 09 handoff','# Exposé V checkpoint 09 integrated handoff')
handoff+='''
## Exact integration amendment on 331

Use this separately named integrated snapshot for checkpoint 09. The first read-only snapshot remains unchanged. Its only revised source folio is 331: the earlier `review/middle/patches.jsonl` manual replay has already changed the current heading from `\\textbf{3.10.}` to `\\textbf{3.10}`. The local font patch now consumes that undotted heading and produces `3.10`, as in the diplomatic layer. The source/manual/checker records and the existing full-page metadata are aligned with this exact composition. No additional scan coverage is claimed.

`integration_amendment_331.json` gives the earlier patch and its line hash. The validation helper now composes the earlier middle stream and accepts only exact duplicate old/new pairs. The original incremental scripts remain historical evidence and are not an instruction to replay old decisions. The canonical JSONL streams are the merge inputs. No record or evidence from live folios 341 onward is included.
'''
(dst/'FROZEN_HANDOFF.md').write_text(handoff)
pages=load(dst,'page_status.jsonl');assert sorted(x['page'] for x in pages if x['fully_checked'])==list(range(297,341))
for name,n in [('decisions.jsonl',628),('own_findings.jsonl',102),('patches.jsonl',167),('page_status.jsonl',44)]:assert len(load(dst,name))==n
manifest=[]
for f in sorted(dst.iterdir()):
 if f.is_file():manifest.append(f'{hashlib.sha256(f.read_bytes()).hexdigest()}\t{f.stat().st_size}\t{f.name}\n')
(dst/'snapshot_manifest.tsv').write_text(''.join(manifest))
for f in dst.iterdir():f.chmod(0o444)
dst.chmod(0o555)
assert hashlib.sha256((prior/'snapshot_manifest.tsv').read_bytes()).hexdigest()==before
print(json.dumps(summary,ensure_ascii=False))
print('manifest_sha256='+hashlib.sha256((dst/'snapshot_manifest.tsv').read_bytes()).hexdigest())
print('manifest_entries='+str(len(manifest)))
