#!/usr/bin/env python3
"""Report this contribution's saved manual-comparison and local-check state."""
from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent
def lines(name):return [json.loads(s) for s in (HERE/name).read_text().splitlines() if s.strip()]
def main():
    batches=json.loads((HERE/'batches.json').read_text());first=min(b['first'] for b in batches);last=max(b['last'] for b in batches)
    variants=lines('variants.jsonl');ledger=lines('transfer.jsonl');spans=lines('translation_spans.jsonl')
    check=json.loads((HERE/'literal_math_verification.json').read_text());star=json.loads((HERE/'starred_math_verification.json').read_text())
    assert check['scope']==star['scope']==f'printed{first}–{last}'
    assert check['unexpected_difference_units']==star['unexpected_differences']==0
    target_count=sum(len(re.findall(r'\\sgaStableTarget(?:Inline)?\{',s['new'])) for s in spans)
    old_joins=json.loads((HERE/'paragraph_join_audit_297_341.json').read_text())['joins']
    joins=old_joins+[r for r in ledger if r.get('record_type')=='manually_compared_source_folio_join']
    assert len({(j['after'],j['before']) for j in joins})==len(joins)
    assert {(j['after'],j['before']) for j in joins}=={(p,p+1) for p in range(first,last)},'unrecorded source-folio join'
    macro=[r for r in ledger if r.get('record_type')=='continuation_macro_boundary']
    macro_text='; '.join(f"{r['page']}/{r['next_page']}" for r in macro)
    files=list((HERE/'attributed_source_audits').glob('*.json'))
    endpoint='The assigned source range is complete through393; the separate contributor continues394–415.' if last==393 else f'The next source page is {last+1}.'
    boundary='stops' if last==393 else 'will stop'
    status=f'''# English Exposés V–VI contribution

Assigned source scope: printed pages 297–393, following the coordinator's explicit partition at the opening of VI §4 on394. The completed V source review is frozen in `review/expose_v/` and its checkpoint 11 snapshot. Exposé VI source records are owned by the coordinator; the separate late-VI contribution covers394–415.

Pages {first}–{last} have been reconstructed and manually compared in full with the reviewed French. The {len(batches)} raw chunks, contiguous exact native replacement spans, all {target_count} native stable targets, source hashes, patch transfers, terminology candidates and lexical dispositions are saved. There are {len(variants)} explicit English variant records and {len(ledger)} transfer records.

Both local branches pass the main mathematical-unit comparison with zero unexpected differences. There are {check['approved_lexical_difference_side_units']} approved lexical difference side-units across the branches. Complete `equation*` and `align*` displays are checked separately in `starred_math_verification.json`, because the main matcher does not include those environment names: {sum(r['French_starred_units'] for r in star['counts'])} starred units across the two branches, with exact ordered equality. These checks do not certify prose, images, macro expansion or PDF rendering; the manual passage comparison is recorded separately.

Every internal source-folio join through {last} has been compared explicitly: {len(joins)} joins, of which {sum(j['paragraph_break'] for j in joins)} are source paragraph boundaries. The remaining joins are continuous. The first 44 are in `paragraph_join_audit_297_341.json`; subsequent joins are in the transfer ledger. The maker concatenates explicit translated line endings without adding a folio separator and reuses an existing newline after an inline page-marker placeholder. All current chunk hashes and native replacement spans include these transport decisions.

Source proof packets are hash-linked, and {len(files)} exact copies are retained in `attributed_source_audits`. The author body preserves every retained source claim; the precise counterexamples, coefficient maps, augmentation comparisons and verified identifications remain separately attributed. French spelling and agreement repairs with unchanged English renderings are recorded without artificial English errors.

The recorded continuation blocks are retained at {macro_text}, with their literal text and hashes in the ledger. Both native and reviewed blocks are present at323/324,346/347 and364/365. At389/390 the nine native commands are retained; the reviewed French has no corresponding block, and no paragraph break is added to the continuing sentence. The separate late-VI contributor will preserve the actual415/416 continuation. The supplied IV296→V297 macro state is retained from the English assembly owner's boundary packet. This contribution's final native span {boundary} immediately before `sga6.e06.sec.4` on394.

This contribution is prepared and locally checked. Its contributor has not run shared registration, compilation or PDF visual inspection, and has not edited shared English assembly records or frozen source/checkpoint records. The assembly owner tracks subsequent integration separately. {endpoint}
'''
    (HERE/'STATUS.md').write_text(status)
    print(json.dumps(dict(first=first,last=last,chunks=len(batches),targets=target_count,variants=len(variants),transfer_records=len(ledger),joins=len(joins))))
if __name__=='__main__':main()
