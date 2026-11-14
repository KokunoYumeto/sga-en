#!/usr/bin/env python3
"""Copy the personally completed V297–328 state; never change an older snapshot."""
from pathlib import Path
import hashlib,json,re,shutil
src=Path(__file__).resolve().parent
root=src.parents[1]
dst=root/'build/review_snapshots/expose_v_checkpoint08_through328'
assert not dst.exists(), 'Immutable snapshot already exists'
dst.mkdir(parents=True)
for f in sorted(src.iterdir()):
    if not f.is_file():continue
    m=re.match(r'(?:page|witness|main|add)_(\d+)',f.name)
    if m and int(m.group(1))>328:continue
    shutil.copy2(f,dst/f.name)
def rows(name):
    return [json.loads(x) for x in (dst/name).read_text().splitlines() if x.strip()]
decisions=rows('decisions.jsonl');own=rows('own_findings.jsonl')
patches=rows('patches.jsonl');pages=rows('page_status.jsonl')
assert sorted(x['page'] for x in pages if x['fully_checked'])==list(range(297,329))
assert all(297<=int(x['page'])<=328 for group in (decisions,own,patches,pages) for x in group)
registry=json.loads((root/'build/registry.json').read_text())
ids={x['source_id'] for x in decisions}
required=[x for x in registry if str(x.get('page','')).isdigit() and 297<=int(x['page'])<=328]
missing=[x['id'] for x in required if x['id'] not in ids]
assert not missing, missing
summary={
 'scope':'Exposé V, printed297–328;32 complete pages personally compared',
 'last_fully_checked_page':328,
 'source_decisions':len(decisions),'own_findings':len(own),
 'patch_records':len(patches),'fully_checked_pages':len(pages),
 'registry_rows_in_scope':len(required),'registry_ids_without_decision':missing,
 'live_source':'review/expose_v/',
 'snapshot':'build/review_snapshots/expose_v_checkpoint08_through328/',
 'exact_calculation_packets':['identification_312.json','identification_327.json'],
 'separate_rendering_repair':'The coordinator-owned review/expose_v_rendering directory supplies the314 control-word delimiter repair; it is deliberately separate from this review snapshot.',
 'open_later_occurrences':'Global script-G finding still awaits actual uses on345 and347. Codex297 later product glyphs are occurrence-specific and have no verdict beyond the saved inspected scope. No page beyond328 is claimed fully checked.',
}
(dst/'snapshot_status.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
manifest=[]
for f in sorted(dst.iterdir()):
    if f.is_file():
        manifest.append(f'{hashlib.sha256(f.read_bytes()).hexdigest()}\t{f.stat().st_size}\t{f.name}\n')
(dst/'snapshot_manifest.tsv').write_text(''.join(manifest))
for f in dst.iterdir():f.chmod(0o444)
dst.chmod(0o555)
print(json.dumps(summary,ensure_ascii=False))
print('manifest_sha256='+hashlib.sha256((dst/'snapshot_manifest.tsv').read_bytes()).hexdigest())
