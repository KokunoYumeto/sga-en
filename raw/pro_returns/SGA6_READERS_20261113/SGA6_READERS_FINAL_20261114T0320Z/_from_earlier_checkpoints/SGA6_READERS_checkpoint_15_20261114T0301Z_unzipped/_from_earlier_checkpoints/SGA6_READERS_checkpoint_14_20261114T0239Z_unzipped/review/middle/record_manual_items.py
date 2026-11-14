#!/usr/bin/env python3
"""Seven manual-item decisions based on personally viewed scan regions."""
import json
from pathlib import Path
from record_open_items import merge_file

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
rows=[]

def add(batch,page,verdict,printed,change,reason,region,other=None):
    rows.append(dict(source_id=f'fixes/MANUAL_6_findings/MANUAL_6_findings_{batch}.json#1',
      page=page,type='manual',verdict=verdict,printed_reading=printed,
      image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}'+
        (f'; scan/SGA6_scan_360dpi.pdf#page={other+14}' if other else ''),
      region=region,change=change,forms='French layers and corresponding English transfer',reason=reason))

add('191_195',196,'reverted',r'tel que H_i(underlined f^{n′},A)→H_i(underlined f^n,A) soit nul.',
    'Retain the equation tokens and the current display placement; no content patch for this item.',
    'The first printed line does place the map inline, between tel que and soit nul. The proposed edit moves only the same formula from display to inline; layout is accepted under NOTE_6. The folio196 marker is already before tel que in both layers. This item does not adjudicate the separate font convention for f.',
    'First body line of printed196, main216dpi top crop')
add('241_245',245,'confirmed','ob in E∈ob D(X) on245 and246',
    r'Keep the existing \renewcommand{\Ob}{\operatorname{ob}} at the folio245 end.',
    'The lower-case o is visible in Corollary3.5.2 on245 and Proposition3.6 on246, immediately across this macro boundary. Both source layers already define the macro with lower-case ob. This is a local definition check; it does not certify every later occurrence cited only from prior OCR in the old record.',
    '245 Corollary3.5.2 and246 Proposition3.6, E∈ob D(X)',other=246)
add('326_330',331,'not applied and now applied','3.10 followed by Soit, with no terminal stop',
    r'Current \textbf{3.10.} becomes \textbf{3.10}; diplomatic already agrees.',
    'The first body line on331 has a space after the zero and no terminal period. The filed page330 was the earlier misplaced source heading; both current markers now place the heading on331, but only the diplomatic layer lost the extra stop.',
    'First body heading on331, main216dpi top crop')
add('451_455',456,'confirmed','4.7. On revient à la situation de3.7',
    'Already present as 4.7. after the folio456 marker in both layers.',
    'A full stop is clearly printed after7 in the first body heading. Both supplied source layers retain it at the correct page break, so no further replacement is needed.',
    'First body heading on456, main216dpi top crop')
add('481_485',485,'confirmed','485 ends est commutatif.;486 begins La démonstration du théorème3.6',
    'Keep the extra Suite de la démonstration heading absent from both layers.',
    'The inspected foot of485 and head of486 are consecutive text regions without that heading. The two source layers already meet at exactly those sentences; there is no heading to remove again.',
    '485 final sentence and486 first paragraph, main216dpi crops',other=486)
add('631_635',630,'confirmed',r'Σ_{i=0}^r a_i^{(m)} binom(n+i,i)=Σ_{j=0}^r a_j binom(mn+j,j), with no trailing punctuation',
    'Already present without the trailing comma, before folio631, in both layers.',
    'The last display on630 ends after the final right parenthesis with blank space to its right and below. Both layers have removed the comma and place the formula before the631 marker. The record’s earlier631 location is superseded by the observed folio630.',
    'Final display on630, main216dpi lower crop')
add('641_645',646,'confirmed',r'χ(F⊗L)=χ(F), with no trailing punctuation',
    'Already present without a semicolon immediately after the646 marker in both layers.',
    'The first printed formula on646 ends at the closing parenthesis. The next printed line starts item(iii). Both supplied layers already omit the proposed extra semicolon at that boundary.',
    'First display and following item(iii) on646, main216dpi top crop')

patch=dict(page=331,layer='current',old=r'\textbf{3.10.}',new=r'\textbf{3.10}',
    expected_count=1,source_id=rows[2]['source_id'],reason=rows[2]['reason'])

if __name__=='__main__':
    t=(ROOT/'build/page_packets/331/current.tex').read_text();assert t.count(patch['old'])==1
    merge_file('decisions.jsonl',rows)
    merge_file('patches.jsonl',[patch])
    print(json.dumps({'manual_items_decided':len(rows),'new_patches':1,'whole_pages_certified':0}))
