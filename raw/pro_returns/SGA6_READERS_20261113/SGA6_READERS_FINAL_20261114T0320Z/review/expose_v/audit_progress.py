#!/usr/bin/env python3
"""Audit saved record coverage only; generate no scan verdicts."""
from pathlib import Path
import json,sys
here=Path(__file__).resolve().parent
root=here.parents[1]
last=int(sys.argv[1])
def read(name):return [json.loads(x) for x in (here/name).read_text().splitlines() if x.strip()]
dec=read('decisions.jsonl');own=read('own_findings.jsonl');patch=read('patches.jsonl');pages=read('page_status.jsonl')
ids={x['source_id'] for x in dec}
registry=json.loads((root/'build/registry.json').read_text())
req=[x for x in registry if str(x.get('page','')).isdigit() and 297<=int(x['page'])<=last]
out={
 'scope':[297,last],
 'source_decisions':sum(297<=int(x['page'])<=last for x in dec),
 'own_findings':sum(297<=int(x['page'])<=last for x in own),
 'patch_records':sum(297<=int(x['page'])<=last for x in patch),
 'fully_checked_pages':[x['page'] for x in pages if 297<=x['page']<=last and x['fully_checked']],
 'required_registry_rows':len(req),
 'missing_registry_ids':[x['id'] for x in req if x['id'] not in ids],
 'note':'Coverage reflects saved personal image comparisons only. Aggregate findings can explicitly defer occurrences beyond this range; no later image verdict is inferred.',
}
assert sorted(out['fully_checked_pages'])==list(range(297,last+1))
(here/f'coverage_through_{last}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False))
