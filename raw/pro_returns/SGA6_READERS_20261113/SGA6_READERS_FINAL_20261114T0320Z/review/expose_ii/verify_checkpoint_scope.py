"""Assert cumulative patch anchors and TeX delimiters within the checkpoint scope."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[2]
patches=[]
for owner in ('middle','expose_ii'):
 patches.extend((owner,json.loads(x)) for x in (root/f'review/{owner}/patches.jsonl').read_text().splitlines() if x)
n=0;duplicates=[]
for page in range(160,188):
 for layer in ('diplomatic','current'):
  text=(root/f'build/page_packets/{page}/{layer}.tex').read_text()
  for owner,p in patches:
   if p['page']!=page or p['layer'] not in ('both',layer):continue
   found=text.count(p['old'])
   if found==0 and text.count(p['new'])==p.get('expected_count',1):
    duplicates.append({'page':page,'layer':layer,'source_id':p['source_id']});continue
   assert found==p.get('expected_count',1),(owner,page,layer,p['source_id'],found)
   text=text.replace(p['old'],p['new']);n+=1
  assert not re.search(r'\\(?:Ob[A-Z]|simeq[A-Za-z])',text),(page,layer)
print(json.dumps({'scope':[160,187],'cumulative_applications':n,'already_present_exact':duplicates,'blocked':0,'joined_commands':0}))
