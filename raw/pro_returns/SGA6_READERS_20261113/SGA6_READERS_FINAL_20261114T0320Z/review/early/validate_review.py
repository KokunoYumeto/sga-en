"""Check evidence structure and exact anchors against unmodified page extracts."""
from pathlib import Path
from collections import Counter
import json
O=Path(__file__).resolve().parent
rows=[json.loads(s) for s in (O/'decisions.jsonl').read_text().splitlines()]
patches=[json.loads(s) for s in (O/'patches.jsonl').read_text().splitlines()]
pages=[json.loads(s) for s in (O/'page_status.jsonl').read_text().splitlines()]
errors=[]
for sid,n in Counter(r['source_id'] for r in rows).items():
 if n>1:errors.append({'duplicate_id':sid,'count':n})
for p in patches:
 for layer in ['diplomatic','current'] if p['layer']=='both' else [p['layer']]:
  text=(O/f"page_{p['page']:03d}_{layer}.tex").read_text()
  n=text.count(p['old'])
  if n!=p.get('expected_count',1):errors.append({'page':p['page'],'layer':layer,'id':p['source_id'],'expected':p.get('expected_count',1),'actual':n,'old':p['old']})
result={'decision_rows':len(rows),'patch_rows':len(patches),'page_rows':len(pages),'last_fully_checked':max(p['page'] for p in pages if p['fully_checked']),'errors':errors}
(O/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(bool(errors))
