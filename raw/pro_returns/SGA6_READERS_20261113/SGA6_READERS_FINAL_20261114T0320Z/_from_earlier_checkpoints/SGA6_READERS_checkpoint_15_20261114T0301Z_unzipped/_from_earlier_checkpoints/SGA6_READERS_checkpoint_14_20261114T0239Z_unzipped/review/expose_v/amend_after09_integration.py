#!/usr/bin/env python3
"""Reconcile exact earlier middle replays; never overwrite a frozen snapshot."""
from review_helpers import Review,HERE,ROOT,read
import hashlib,json
r=Review()
reason=('The physical331 header was directly compared in the completed review and prints3.10 without a terminal stop. '
 'The coordinator middle stream already applies the actual331 manual replay to current, changing textbf{3.10.} to textbf{3.10}. '
 'The local font patch must then remove textbf from that exact cumulative undotted form. '
 'The earlier local record kept the baseline current dot despite this accepted replay; that integration reading is amended. '
 'Both layers now retain the observed undotted numeral. No new scan coverage is claimed.')
r.finding('331_335',2,'The actual331 opening numeral is3.10, without a final full stop.',reason,
 'actual331 opening paragraph numeral',verdict='printed reading confirmed; current integration amended',
 change='Both forms retain3.10 without a terminal stop; the middle manual replay precedes the local font patch.',witness=342,actual_page=331)
for sid in ['check/findings/findings_326_330.json#34','fixes/MANUAL_6_findings/MANUAL_6_findings_326_330.json#1']:
 r.source(sid,'Actual331 opens with3.10, without a terminal stop.',reason,
  'actual331 opening paragraph numeral',verdict='confirmed at actual331; ordered replay incorporated',
  change='Retain the undotted numeral in both layers; use the exact middle replay before removing textbf.',witness=342,page=331)
r.own_finding('ASTRA-V-PARAGRAPH-331',331,
 'The opening paragraph number3.10 has ordinary typed weight, no rule and no terminal stop.',
 r'Both layers use3.10 after the ordered middle replay; remove \textbf from the undotted numeral.',
 'Amend the current font-patch anchor to the already replayed undotted form and retain that punctuation.',
 reason,'paragraph number3.10',kind='font',verdict='current integration amended; printed numeral retained in both forms',witness=342)
r.patch(331,'diplomatic',r'\textbf{3.10}','3.10','ASTRA-V-PARAGRAPH-331','Preserve plain weight and the observed undotted numeral.')
r.patch(331,'current',r'\textbf{3.10}','3.10','ASTRA-V-PARAGRAPH-331','Apply after the exact middle manual replay removes the unprinted stop; preserve plain weight.')
# The same ordered composition exposed a second live-only duplicate. Keep the
# exact old/new pair of that regional replay, permitting only exact deduplication.
r.patch(341,'current',r"(nn',nx'+n'x+x\cdot_N x').",r"(nn',nx'+n'x+x\cdot_N x')",'check/findings/findings_341_345.json#5','Exact duplicate of the earlier middle REPLAY_MANUAL#9 pair; remove only the unprinted stop.')
# Keep this exact replay before the already saved low-dot transformation of
# that same row. Replacing a source group appends it, so carry the two later
# page-local formatting groups together in their original relative order.
r.patches.extend(p for p in read('patches.jsonl') if p['page']==341 and p['source_id']!='check/findings/findings_341_345.json#5')
r.source('fixes/REPLAY_MANUAL_6.json#9','The multiplication row ends with a closing parenthesis and no stop.',
 'The earlier middle replay applies the full corrected x-prime row before the V stream. The V patch now records the identical full-row old/new pair, which the ordered loader recognizes as exactly already applied. No narrower overlapping suffix replay remains.',
 '341 multiplication-row punctuation',verdict='confirmed and applied by exact earlier middle replay',
 change='Keep the exact whole-row replay pair, with the corrected x-prime operand unchanged.',witness=352,page=341)
middle=[]
for line in (ROOT/'review/middle/patches.jsonl').read_text().splitlines():
 if not line.strip():continue
 p=json.loads(line)
 if p.get('page')==331:middle.append({'patch':p,'line_sha256':hashlib.sha256(line.encode()).hexdigest()})
packet={
 'record_type':'post_checkpoint08_integration_amendment','page':331,
 'source_ids':['ASTRA-V-PARAGRAPH-331','check/findings/findings_331_335.json#2','check/findings/findings_326_330.json#34','fixes/MANUAL_6_findings/MANUAL_6_findings_326_330.json#1','fixes/FIXLOG_6.jsonl#1412','fixes/MISPRINTS_6.json#282'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=345','scan/SGA6_witness_300dpi.djvu#page=342'],
 'printed_reading':'3.10, ordinary type with no terminal stop.',
 'responsible_earlier_transformations':middle,
 'failed_local_current_anchor':r'\textbf{3.10.}',
 'actual_cumulative_current_anchor':r'\textbf{3.10}',
 'amended_local_current_result':'3.10',
 'reason':reason,
 'snapshot_disposition':'The first checkpoint09-through340 read-only snapshot remains unchanged. A distinct integrated snapshot supplies the amended331 records for checkpoint09 assembly.',
 'validation_change':'Live Review.commit now composes the earlier middle patches before the V stream and accepts only an exact already-applied old/new pair.'
}
(HERE/'integration_amendment_331.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
page331=next(x.copy() for x in read('page_status.jsonl') if x['page']==331)
page331['notes']=page331['notes'].replace('the exact paragraph-number variant','the exact undotted paragraph number (current integration subsequently aligned with the earlier middle replay)')
r.pages.append(page331)
r.commit()
