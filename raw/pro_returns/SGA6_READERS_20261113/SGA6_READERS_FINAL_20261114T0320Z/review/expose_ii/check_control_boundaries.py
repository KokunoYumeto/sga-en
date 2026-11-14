"""Detect new TeX control words introduced by the local patch sequence."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[2];here=root/'review/expose_ii'
patches=[json.loads(x) for x in (here/'patches.jsonl').read_text().splitlines() if x]
allowed={'uline','underline','phi','SGAAuthorFootnote','SGAAuthorFootMark','SGAAuthorFootText','simeq','operatorname'}
issues=[]
for page in sorted({x['page'] for x in patches}):
 for layer in ('diplomatic','current'):
  before=(root/f'build/page_packets/{page}/{layer}.tex').read_text();after=before
  for p in patches:
   if p['page']==page and p['layer'] in ('both',layer):
    assert after.count(p['old'])==p.get('expected_count',1),(page,layer,p['source_id'])
    after=after.replace(p['old'],p['new'])
  pre=set(re.findall(r'\\([A-Za-z@]+)',before));post=set(re.findall(r'\\([A-Za-z@]+)',after))
  for command in sorted(post-pre-allowed):issues.append({'page':page,'layer':layer,'command':command})
  assert not re.search(r'\\Ob[A-Z]',after),(page,layer,'joined object command')
print(json.dumps({'unexpected_new_controls':issues,'pages_checked':len({x['page'] for x in patches})},ensure_ascii=False))
