#!/usr/bin/env python3
"""Freeze the actually completed V297–351 records for checkpoint10."""
from pathlib import Path
import hashlib,json,re,shutil
src=Path(__file__).resolve().parent
root=src.parents[1]
dst=root/'build/review_snapshots/expose_v_checkpoint10_through351'
assert not dst.exists(), 'Immutable snapshot already exists'
dst.mkdir(parents=True)
for f in sorted(src.iterdir()):
    if not f.is_file():continue
    m=re.match(r'(?:page|witness|main|add|identification|author_claim_issue)_(\d+)',f.name)
    if m and int(m.group(1))>351:continue
    shutil.copy2(f,dst/f.name)
def rows(name):return [json.loads(x) for x in (dst/name).read_text().splitlines() if x.strip()]
decisions=rows('decisions.jsonl');own=rows('own_findings.jsonl')
patches=rows('patches.jsonl');pages=rows('page_status.jsonl')
assert sorted(x['page'] for x in pages if x['fully_checked'])==list(range(297,352))
assert all(297<=int(x['page'])<=351 for group in (decisions,own,patches,pages) for x in group)
registry=json.loads((root/'build/registry.json').read_text())
required=[x for x in registry if str(x.get('page','')).isdigit() and 297<=int(x['page'])<=351]
ids={x['source_id'] for x in decisions}
missing=[x['id'] for x in required if x['id'] not in ids]
assert not missing,missing
packets=sorted(f.name for f in dst.iterdir() if f.is_file() and (f.name.startswith(('identification_','author_claim_issue_','integration_amendment_')) or f.name=='amendment_after_checkpoint08_slash.json'))
summary={
 'scope':'Exposé V, printed297–351;55 complete pages personally compared',
 'last_fully_checked_page':351,'source_decisions':len(decisions),'own_findings':len(own),
 'patch_records':len(patches),'fully_checked_pages':len(pages),'registry_rows_in_scope':len(required),
 'registry_ids_without_decision':missing,'live_source':'review/expose_v/',
 'snapshot':'build/review_snapshots/expose_v_checkpoint10_through351/',
 'exact_calculation_and_claim_packets':packets,
 'earlier_amendments':'Includes the current-only slash grouping amendments on325,326,327,329 and the331 cumulative-stream integration amendment. Prior snapshots remain unchanged.',
 'new_calculations':'Includes the341 unitization counterexample,342 exact coefficient exponent,343 augmented-map obstruction,345 scalar map,346 completed target and coefficient gender,349 coefficient and ink observations,350 Chern character zero constant term and rational modulus maps.',
 'aggregate_scope':'Script-G observation is closed through its last actual347 occurrence. The351–355 underlining aggregate is decided for the actual351 portion only; later portions are outside this snapshot.',
 'separate_rendering_repair':'The coordinator-owned review/expose_v_rendering directory supplies the314 control-word delimiter repair.',
 'later_scope':'No page beyond351 is marked fully checked. The separately stored IV287/289 locator amendments are external merge inputs, not V records.'
}
(dst/'snapshot_status.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(dst/'FROZEN_HANDOFF.md').write_text('''# Exposé V checkpoint 10 handoff

Printed pages 297–351 have been personally compared in full. The page-specific native witness regions are recorded in `page_status.jsonl`. This immutable snapshot contains 55 fully checked pages, 794 inherited source decisions, 135 own findings and 215 exact patch records. All 785 nominal registry rows in that range have a saved decision; the multipage underlining record explicitly limits its completed scope to page 351.

Merge `decisions.jsonl`, `own_findings.jsonl`, `patches.jsonl` and `page_status.jsonl`. Compose the earlier `review/middle/patches.jsonl` stream before these exact patches. Apply the separate coordinator-owned `review/expose_v_rendering/` delimiter repair as documented there. The IV287/289 post-freeze locator amendments are separate inputs in `review/expose_iv_amendments/`.

All earlier current-only slash amendments and the page331 integration amendment are included. Previous snapshots have not been changed. The current scripts validate cumulative exact patch composition against the middle stream.

The proof and identification packets include exact maps, coefficient comparisons, concrete examples and separately retained author-claim defects. In particular, `identification_350.json` reproduces the preceding Chern-character and unit/rank definitions, proves the zero constant term of its restriction, compares the unitized product, and gives the degree-three rational coefficient example for the corrected modulus. Page349's small additional ink mark is recorded without assigning an unsupported extra punctuation token or a physical cause.

The script-G aggregate has been completed through the final actual347 occurrence. No page after351 is represented as fully checked. The local live review may continue beyond this frozen boundary independently.

`snapshot_status.json` contains counts and packet names. `snapshot_manifest.tsv` lists the SHA-256 hash and byte length of every other file in the snapshot. The files and directory are made read-only after that manifest is written.
''')
manifest=[]
for f in sorted(dst.iterdir()):
    if f.is_file():manifest.append(f'{hashlib.sha256(f.read_bytes()).hexdigest()}\t{f.stat().st_size}\t{f.name}\n')
(dst/'snapshot_manifest.tsv').write_text(''.join(manifest))
for f in dst.iterdir():f.chmod(0o444)
dst.chmod(0o555)
print(json.dumps(summary,ensure_ascii=False))
print('manifest_sha256='+hashlib.sha256((dst/'snapshot_manifest.tsv').read_bytes()).hexdigest())
print('manifest_entries='+str(len(manifest)))
