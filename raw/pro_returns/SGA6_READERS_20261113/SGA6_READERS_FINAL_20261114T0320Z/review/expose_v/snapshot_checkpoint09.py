#!/usr/bin/env python3
"""Freeze the actual completed V297–340 state without altering earlier snapshots."""
from pathlib import Path
import hashlib,json,re,shutil
src=Path(__file__).resolve().parent
root=src.parents[1]
dst=root/'build/review_snapshots/expose_v_checkpoint09_through340'
assert not dst.exists(), 'Immutable snapshot already exists'
dst.mkdir(parents=True)
for f in sorted(src.iterdir()):
    if not f.is_file():continue
    m=re.match(r'(?:page|witness|main|add|identification|author_claim_issue)_(\d+)',f.name)
    if m and int(m.group(1))>340:continue
    shutil.copy2(f,dst/f.name)
def rows(name):
    return [json.loads(x) for x in (dst/name).read_text().splitlines() if x.strip()]
decisions=rows('decisions.jsonl');own=rows('own_findings.jsonl')
patches=rows('patches.jsonl');pages=rows('page_status.jsonl')
assert sorted(x['page'] for x in pages if x['fully_checked'])==list(range(297,341))
assert all(297<=int(x['page'])<=340 for group in (decisions,own,patches,pages) for x in group)
registry=json.loads((root/'build/registry.json').read_text())
ids={x['source_id'] for x in decisions}
required=[x for x in registry if str(x.get('page','')).isdigit() and 297<=int(x['page'])<=340]
missing=[x['id'] for x in required if x['id'] not in ids]
assert not missing,missing
packets=sorted(f.name for f in dst.iterdir() if f.is_file() and (f.name.startswith('identification_') or f.name.startswith('author_claim_issue_') or f.name=='amendment_after_checkpoint08_slash.json'))
summary={
 'scope':'Exposé V, printed297–340;44 complete pages personally compared',
 'last_fully_checked_page':340,
 'source_decisions':len(decisions),'own_findings':len(own),
 'patch_records':len(patches),'fully_checked_pages':len(pages),
 'registry_rows_in_scope':len(required),'registry_ids_without_decision':missing,
 'live_source':'review/expose_v/',
 'snapshot':'build/review_snapshots/expose_v_checkpoint09_through340/',
 'exact_calculation_and_claim_packets':packets,
 'post08_amendments':'Includes the exact current-only slash grouping amendments on325,326,327,329 and their full substitution maps. The08 snapshot itself remains unchanged.',
 'source_claims':'3364.12,3374.13 and cited inverse step,3384.15 intermediate equality,339 full-A injectivity are retained with explicit defects. The printed graded4.14, weight-filtration4.15 and5.2 divisibility statements have separate exact proofs in the packets.',
 'separate_rendering_repair':'The coordinator-owned review/expose_v_rendering directory supplies the314 control-word delimiter repair and remains separate.',
 'later_scope':'The global script-G finding still awaits its actual345 and347 occurrences. Codex297 product glyphs are occurrence-specific. No page beyond340 is marked fully checked.'
}
(dst/'snapshot_status.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(dst/'FROZEN_HANDOFF.md').write_text('''# Exposé V checkpoint 09 handoff

Printed pages 297–340 have been personally compared in full against the main scan, with the page-specific witness regions recorded in `page_status.jsonl`. This snapshot contains 44 fully checked pages, 628 source decisions, 102 own findings and 167 exact patch records. All 624 nominal registry rows in that range have decisions.

The merge inputs are `decisions.jsonl`, `own_findings.jsonl`, `patches.jsonl` and `page_status.jsonl`. The scripts and page evidence copied alongside them document this exact saved state. Apply the coordinator-owned `review/expose_v_rendering/` delimiter repair separately.

The snapshot includes the post-checkpoint-08 slash grouping amendments on pages 325, 326, 327 and 329, with the substitution and inverse maps in `amendment_after_checkpoint08_slash.json`. Checkpoint 08 has not been changed.

The explicit mathematical packets include the corrected coefficient-weight proof on 312, the numerator calculation on 327, the scalar parameter on 336, the dependent finite-tail defects on 336–338, the independent graded coefficient maps on 337 and quotient map on 338, and the full-domain injectivity obstruction with the restricted symmetric-polynomial proof on 339. Printed author claims are preserved; no replacement theorem is inserted.

The later script-G occurrences on pages 345 and 347 remain outside this frozen range. Product glyph decisions retain their exact inspected scope. No page after 340 is represented as fully checked.

`snapshot_status.json` gives machine-readable counts and packet names. `snapshot_manifest.tsv` records the SHA-256 hash and byte length of every other file in this snapshot. All files and the directory are made read-only after the manifest is written.
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
