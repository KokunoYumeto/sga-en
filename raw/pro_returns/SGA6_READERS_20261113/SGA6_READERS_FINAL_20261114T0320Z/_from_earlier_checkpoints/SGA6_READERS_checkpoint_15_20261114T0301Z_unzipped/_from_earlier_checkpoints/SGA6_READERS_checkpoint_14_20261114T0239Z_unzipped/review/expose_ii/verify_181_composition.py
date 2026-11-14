"""Verify the already observed folio181 patches compose after the middle replay."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
for layer in ('diplomatic','current'):
 text=(root/f'build/page_packets/181/{layer}.tex').read_text()
 count=0
 for owner in ('middle','expose_ii'):
  for row in (root/f'review/{owner}/patches.jsonl').read_text().splitlines():
   p=json.loads(row)
   if p['page']!=181 or p['layer'] not in ('both',layer):continue
   n=text.count(p['old']);assert n==p.get('expected_count',1),(owner,layer,p['source_id'],n)
   text=text.replace(p['old'],p['new']);count+=1
 assert text.count(r'\underline{\underline{R}}\Gamma_S')==2
 assert r'\mathbb R\Gamma_S' not in text
 assert r'\uline{Sous les hypothèses de}' in text
 assert r'\uline{induit un foncteur pleinement fidèle}' in text
 print(layer,count,'patches applied; two literal double-underlined R glyphs and statement rules retained')
