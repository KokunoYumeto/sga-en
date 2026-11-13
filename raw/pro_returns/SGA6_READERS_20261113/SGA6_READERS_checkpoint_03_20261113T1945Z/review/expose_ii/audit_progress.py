"""Report saved coverage and inherited-record gaps; never assign scan verdicts."""
from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[2];here=root/'review/expose_ii'
end=int(sys.argv[1]) if len(sys.argv)>1 else 190
rows={}
for name in ('decisions','own_findings','patches','page_status'):
 rows[name]=[json.loads(x) for x in (here/(name+'.jsonl')).read_text().splitlines() if x]
 print(name,len(rows[name]))
status={x['page']:x for x in rows['page_status'] if x.get('fully_checked')}
print('fully_checked_range',min(status),max(status),'missing',[p for p in range(160,end+1) if p not in status])
seen={x['source_id'] for x in rows['decisions']}
registry=json.loads((root/'build/registry.json').read_text())
gaps=[x for x in registry if isinstance(x.get('page'),int) and 160<=x['page']<=end and x['id'] not in seen and x['id'].replace(':entries#','#') not in seen]
print('registry_gaps',json.dumps(gaps,ensure_ascii=False))
# The cumulative middle replay precedes this agent's patches.
for page in (181,190):
 if page>end:continue
 for layer in ('diplomatic','current'):
  text=(root/f'build/page_packets/{page}/{layer}.tex').read_text()
  for owner in ('middle','expose_ii'):
   for raw in (root/f'review/{owner}/patches.jsonl').read_text().splitlines():
    p=json.loads(raw)
    if p['page']!=page or p['layer'] not in ('both',layer):continue
    n=text.count(p['old']);assert n==p.get('expected_count',1),(owner,page,layer,p['source_id'],n)
    text=text.replace(p['old'],p['new'])
  if page==181:assert text.count(r'\underline{\underline{R}}\Gamma_S')==2
  if page==190:
   assert r'QE^n\simeq E^n' in text
   assert "E'{}^n" not in text
  print('composes',page,layer)
