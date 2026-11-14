#!/usr/bin/env python3
"""Seal the prepared V contribution without replacing any earlier snapshot."""
from pathlib import Path
import json,hashlib,re,shutil
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def rows(name):return [json.loads(s) for s in (HERE/name).read_text().splitlines() if s.strip()]
batches=json.loads((HERE/'batches.json').read_text())
assert [p for b in batches for p in range(b['first'],b['last']+1)]==list(range(297,365))
spans=rows('translation_spans.jsonl');variants=rows('variants.jsonl');ledger=rows('transfer.jsonl')
math=json.loads((HERE/'literal_math_verification.json').read_text());star=json.loads((HERE/'starred_math_verification.json').read_text())
assert math['scope']==star['scope']=='printed297–364'
assert math['unexpected_difference_units']==star['unexpected_differences']==0
for name,digest in math['source_chunk_sha256s'].items():assert sha(HERE/name)==digest,name
all_text=''.join(s['new'] for s in spans)
assert '@@' not in all_text
assert [int(p) for p in re.findall(r'\\SGAPrintPage\{(\d+)\}',all_text)]==list(range(297,365))
assert len(variants)==70 and len({r['id'] for r in variants})==70
assert len(re.findall(r'\\sgaStableTarget(?:Inline)?\{',all_text))==156
joins=json.loads((HERE/'paragraph_join_audit_297_341.json').read_text())['joins']+[r for r in ledger if r.get('record_type')=='manually_compared_source_folio_join']
assert {(j['after'],j['before']) for j in joins}=={(p,p+1) for p in range(297,364)} and len(joins)==67
macro=[r for r in ledger if r.get('record_type')=='continuation_macro_boundary']
assert [(r['page'],r['next_page']) for r in macro]==[(323,324),(346,347),(364,365)]
notes=[r for r in ledger if r.get('record_type')=='page_transfer_inventory']
assert all(not r['French_author_notes'] and not r['English_author_notes'] for r in notes)
counts=dict(source_folios=68,raw_chunks=14,provisional_variant_groups=70,transfer_records=len(ledger),native_stable_targets=156,math_units={layer:sum(r['French_math_units'] for r in math['counts'] if r['layer']==layer) for layer in ['current','diplomatic']},starred_units_per_branch=2,unexpected_math_units=0,lexical_complete_unit_pairs=len(json.loads((HERE/'lexical_math_pairs.json').read_text())),approved_lexical_difference_side_units=math['approved_lexical_difference_side_units'],source_folio_joins=67,paragraph_boundary_joins=sum(j['paragraph_break'] for j in joins),original_author_notes=0,selected_term_pairs=len((HERE/'terms.tsv').read_text().splitlines())-1,attributed_source_audit_copies=len(list((HERE/'attributed_source_audits').glob('*.json'))))
limitations=['The contributor has not compiled or visually inspected an English PDF for this packet. The assembly owner handles aggregate rendering and original macro expansion.','Literal mathematical-unit comparisons certify only their documented matchers; the two align-star displays are checked separately in exact order. Complete prose and placement comparison is a recorded manual task.','Term pairs are source-anchored candidates, not a claim of final cross-volume semantic glossary coverage.','Source-image evidence is attributed to the frozen French review; this translation pass does not make a new full-page image-collation claim.']
handoff=dict(scope='Prepared English Exposé V297–364, complete',counts=counts,first_native_target='sga6.e05.expose',next_native_target='sga6.e06.expose',source_reference='Both exact reviewed French branches in source_packets,per-patch hashes in reference files,and frozen source audit copies.',mathematical_branch_status='Both primary matchers pass with zero unexpected units; complete starred displays have exact ordered equality.',paragraph_status='All67 source-folio joins explicitly compared;20 are paragraph boundaries and47 are continuations.',macro_boundaries=[dict(page=r['page'],next_page=r['next_page'],native_sha256=r['native_block_sha256'],reviewed_sha256=r.get('reviewed_block_sha256',r.get('reviewed_French_block_sha256'))) for r in macro],final_variant_scope='When integrated, bound the final V variant scope by the actual VI365 marker or e06.expose target; the empty local scope_end means this packet end only.',author_body='Every retained source claim is preserved,with its exact proof issue or identification in separately attributed records. No replacement theorem is added.',rendering_status='Prepared and locally exact-checked; no contributor English PDF compile or view.',next_assigned_scope='VI365–393;stop before sga6.e06.sec.4. A separate contributor owns394–415 including415/416 continuation.',limitations=limitations)
put(HERE/'HANDOFF_V.json',handoff)
(HERE/'HANDOFF_V.md').write_text('''# Prepared English transfer: Exposé V297–364

All68 source folios have a complete manual prose and formula-placement comparison with both reviewed French forms. Consume the14 exact native replacement spans in `translation_spans.jsonl` in order, from `sga6.e05.expose` to immediately before `sga6.e06.expose`. All156 native stable targets are retained. The70 provisional variant groups carry exact source IDs,scanned-reading attribution and the source proof reasons. The873 transfer records preserve every consumed patch hash and source branch,unchanged English lexical dispositions,local glyph inventories,and separately attributed author-argument audits.

The current and diplomatic primary comparisons pass with2136 and2134 units respectively. The two complete `align*` displays on340 are separately checked in exact order in each branch; the primary matcher does not include their starred environment name. There are zero unexpected units in either check. Approved lexical substitutions alter only the explicitly listed words inside complete mathematical units. This exact comparison does not replace the separately recorded manual prose and formula-placement comparison.

Every internal folio join is explicitly recorded:67 joins,20 source paragraph boundaries and47 continuations. The maker adds no extra folio newline. The complete native/reviewed macro blocks are retained at323/324,346/347 and364/365,with exact hashes;the final block has20 definitions in each source and the reviewed scoped `id` renewal follows the native provide. V contains no original author-note call in this inspected source scope. Source Chern-class and filtration defects remain in the author body with their concrete coefficient maps,counterexamples and scope limitations separately attributed.

This packet has not been compiled or visually inspected as an English PDF by its contributor. It is ready for the assembly owner's global numbering,registration,macro checks,rendering and glossary work. The final local variant scope must stop at VI365 when assembled. Frozen French sources and earlier checkpoints remain unchanged.

The next assigned interval is VI365–393,ending before `sga6.e06.sec.4`;a separate contributor owns394–415 and its415/416 macro continuation. Live work may continue in the contribution directory after this immutable V snapshot. The snapshot fixes all V chunks,record hashes and checks before that continuation.
''')
deps=[]
for rel in ['review/english/EN_PARALLEL_TRANSFER_HANDOFF.md','review/english/SGA6_EN_native_flattened_UNVERIFIED.tex','review/english/reviewed_french.py','review/english/verify_reviewed_english.py','review/english/check_contribution.py','review/expose_v/FROZEN_HANDOFF.md','review/expose_v/decisions.jsonl','review/expose_v/own_findings.jsonl','review/expose_v/patches.jsonl','review/expose_v/page_status.jsonl','review/expose_v_rendering/patches.jsonl','review/middle/patches.jsonl']:
    p=ROOT/rel;deps.append(dict(path=rel,sha256=sha(p),bytes=p.stat().st_size))
put(HERE/'EXTERNAL_INPUT_HASHES_V.json',deps)
snapshot=ROOT/'build/review_snapshots/english_v_complete297_364'
assert not snapshot.exists(),'Never overwrite a sealed snapshot'
snapshot.parent.mkdir(parents=True,exist_ok=True)
def ignored(directory,names):return [n for n in names if n=='__pycache__' or n.endswith(('.aux','.out'))]
shutil.copytree(HERE,snapshot,ignore=ignored)
files=[dict(path=p.relative_to(snapshot).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(snapshot.rglob('*')) if p.is_file()]
put(snapshot/'MANIFEST.json',dict(scope='Immutable prepared English V297–364 contribution',files=files,file_count=len(files),counts=counts,limitations=limitations))
manifest_sha=sha(snapshot/'MANIFEST.json')
for p in snapshot.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
snapshot.chmod(0o555)
receipt=dict(snapshot=snapshot.relative_to(ROOT).as_posix(),manifest_sha256=manifest_sha,manifested_files=len(files),counts=counts)
put(HERE/'SEAL_V_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
