#!/usr/bin/env python3
"""Freeze the personally completed V297–319 review state for checkpoint07."""
from pathlib import Path
import hashlib,json,re,shutil

src=Path(__file__).resolve().parent
root=src.parents[1]
dst=root/'build/expose_v_checkpoint07_through319'
assert not dst.exists(), 'Immutable snapshot already exists'
dst.mkdir()
for f in sorted(src.iterdir()):
    if not f.is_file(): continue
    m=re.match(r'(?:page|witness|main|add)_(\d+)',f.name)
    if m and int(m.group(1))>319: continue
    shutil.copy2(f,dst/f.name)

def rows(name):
    return [json.loads(x) for x in (dst/name).read_text().splitlines() if x.strip()]
decisions=rows('decisions.jsonl')
own=rows('own_findings.jsonl')
patches=rows('patches.jsonl')
pages=rows('page_status.jsonl')
assert sorted(x['page'] for x in pages if x['fully_checked'])==list(range(297,320))
assert all(297<=int(x['page'])<=319 for group in (decisions,own,patches,pages) for x in group)
registry=json.loads((root/'build/registry.json').read_text())
ids={x['source_id'] for x in decisions}
required=[x for x in registry if x.get('page') is not None and str(x['page']).isdigit() and 297<=int(x['page'])<=319]
missing=[x['id'] for x in required if x['id'] not in ids]
summary={
 'scope':'Exposé V, printed297–319; actual full-page comparison completed for23 pages',
 'last_fully_checked_page':319,
 'source_decisions':len(decisions),'own_findings':len(own),
 'patch_records':len(patches),'fully_checked_pages':len(pages),
 'registry_rows_in_scope':len(required),'registry_ids_without_decision':missing,
 'live_source':'review/expose_v/',
 'snapshot':'build/expose_v_checkpoint07_through319/',
 'amended_proof':'identification_312.json; tuple expansion for separately multilinear operations',
 'ongoing_scopes':'The global script-G finding still awaits actual uses on345 and347; completed local occurrences have their own evidence. No page beyond319 is claimed checked.',
}
(dst/'snapshot_status.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
manifest=[]
for f in sorted(dst.iterdir()):
    if f.is_file():
        manifest.append(f'{hashlib.sha256(f.read_bytes()).hexdigest()}\t{f.stat().st_size}\t{f.name}\n')
(dst/'snapshot_manifest.tsv').write_text(''.join(manifest))
for f in dst.iterdir(): f.chmod(0o444)
dst.chmod(0o555)
print(json.dumps(summary,ensure_ascii=False))
print('manifest_sha256='+hashlib.sha256((dst/'snapshot_manifest.tsv').read_bytes()).hexdigest())
