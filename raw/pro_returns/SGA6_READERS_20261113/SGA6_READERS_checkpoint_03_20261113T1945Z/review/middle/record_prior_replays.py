#!/usr/bin/env python3
"""Independently recheck the four previously resolved replay items."""
import json
from record_open_items import merge_file

entries=[
 (10,402,'amended',r'Inline chain ending x̄′=−x̄, without final punctuation',
  'Keep the existing inline placement; diplomatic retains −x̄ and current retains x̄.',
  'The main scan’s opening paragraph prints the chain inline and ends with the minus sign. Inline/display placement is accepted layout. The separate sign correction follows exactly from x′−x=(ξ−1)x∈Fil², using the printed definitions x=1−ξ⁻¹ and x′=ξ−1; the quotient map Fil¹→Fil¹/Fil² therefore sends x′ and x to the same class.',
  'Opening paragraph, definitions of x,x′ and final congruence'),
 (11,412,'confirmed',r"x'_i\in\overline{\{x_i\}}",
  'Keep the closure bar already present in both layers.',
  'The horizontal bar over the point in braces is clear in the proof of Lemma6.7. Both layer expressions include that bar. No further insertion is needed.',
  'Proof of Lemma6.7, first sentence after Posons M'),
 (12,433,'confirmed',r'\underline{\Tor}_1^{O_X}(O_Y,O_Z)',
  'Keep the underline already present in the display before(2.5.3).',
  'The Tor word immediately below En particulier is underlined in the scan. Both layers already retain that rule, so the earlier placement is confirmed. The separate exponent n/p and later Tor index corrections are outside this replay’s scope.',
  'Lower display after En particulier, on trouve pour i=1'),
 (13,585,'confirmed',r'B_i=A_{i\,m_i}, no parentheses around A_i',
  r'Keep the current \bar A_{i\,\mathfrak m_i} and diplomatic A_{i\,\mathfrak m_i} localization forms.',
  'The upper paragraph prints i and m_i directly below A without parentheses around A_i. Both supplied layers have that localization layout. This confirms the replay placement while retaining the separately recorded missing-bar correction in current.',
  '7.16 first paragraph, et soit B_i=...')
]
rows=[]
for n,page,verdict,printed,change,reason,region in entries:
    rows.append(dict(source_id=f'fixes/REPLAY_MANUAL_6.json#{n}',page=page,type='replay',verdict=verdict,
      printed_reading=printed,change=change,reason=reason,
      image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',region=region+'; main180dpi page image',
      forms='French layers and corresponding English transfer'))

if __name__=='__main__':
    merge_file('decisions.jsonl',rows)
    print(json.dumps({'prior_resolved_replays_independently_read':4,'new_patches':0,'whole_pages_certified':0}))
