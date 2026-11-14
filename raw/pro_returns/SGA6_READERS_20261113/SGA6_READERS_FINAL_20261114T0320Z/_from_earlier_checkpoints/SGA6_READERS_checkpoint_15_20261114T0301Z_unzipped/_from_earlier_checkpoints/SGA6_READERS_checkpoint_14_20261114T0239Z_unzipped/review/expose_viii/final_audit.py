"""Verify exact VIII ledger coverage; the records separately document image review."""
from pathlib import Path
import collections
import hashlib
import json
import re

R = Path(__file__).resolve().parents[2]
O = R / 'review/expose_viii'
read = lambda p: [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
D, P, OWN, S = [read(O / name) for name in
                 ('decisions.jsonl', 'patches.jsonl', 'own_findings.jsonl', 'page_status.jsonl')]
seen = {x['source_id'] for x in D}
assert len(seen) == len(D), 'duplicate decision source IDs'
inside = lambda x: isinstance(x.get('page'), int) and 466 <= x['page'] <= 497
expected = collections.defaultdict(list)
for path in sorted((R / 'check/findings').glob('*.json')):
    for i, x in enumerate(json.loads(path.read_text()), 1):
        if inside(x):
            expected['checker'].append(str(path.relative_to(R)) + f'#{i}')
for name in ('fixes/FIXLOG_6.jsonl', 'fixes/FIXLOG_6_CURRENT.jsonl'):
    for i, x in enumerate(read(R / name), 1):
        if inside(x):
            expected[name].append(f'{name}#{i}')
for i, x in enumerate(json.loads((R / 'fixes/MISPRINTS_6.json').read_text()), 1):
    if inside(x):
        expected['misprint'].append(f'fixes/MISPRINTS_6.json#{i}')
C = json.loads((R / 'fixes/RECONCILE_CODEX_6.json').read_text())['entries']
core = {x['id'] for x in C if x.get('expose') == 'VIII'}
for i, x in enumerate(C, 1):
    if x['id'] in core:
        expected['codex_including_tags'].append(f'fixes/RECONCILE_CODEX_6.json#{i}')
expected['hold_true_VIII_loci'] = [
    f'fr/codex/HOLD_VS_CORR.json#{i}' for i in range(46, 51)
]
missing = [sid for ids in expected.values() for sid in ids if sid not in seen]
assert not missing, missing
assert {sid for ids in expected.values() for sid in ids} == seen

root_owned = ['fixes/MANUAL_6_findings/MANUAL_6_findings_481_485.json#1']
root_rows = {x['source_id']: x for x in read(R / 'review/middle/decisions.jsonl')}
for sid in root_owned:
    assert sid in root_rows and sid not in seen
assert [x['page'] for x in S] == list(range(466, 498))
assert all(x['checked_against_scan'] for x in S)
own_ids = {x['source_id'] for x in OWN}
assert len(own_ids) == len(OWN)
assert not (own_ids & seen)
for x in D + P + OWN + S:
    text = json.dumps(x, ensure_ascii=False)
    assert '/workspace/' not in text
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', text)
    if 'image' in x:
        assert x['image'].startswith('scan/')
for x in P:
    assert x['source_id'] in seen or x['source_id'] in own_ids

supplement_id = 'ASTRA-IX-PRODUCT-DOTS-499-502'
ix_rows = read(R / 'review/expose_ix/own_findings.jsonl')
assert any(x['source_id'] == supplement_id for x in ix_rows)
product = next(x for x in D if x['source_id'] == 'check/findings/findings_496_500.json#6')
assert product['scope_pages'] == [496, 497]
assert product['related_record'] == supplement_id
assert 'produit semi-direct de son radical' in (
    R / 'build/page_packets/515/diplomatic.tex').read_text()
assert 'fr/codex/HOLD_VS_CORR.json#51' not in seen

retained_scope = [
    dict(page=467, source_id='ASTRA-VIII-0015',
         note='The unrestricted quasi-compactness sentence has an explicit infinite-disjoint-union counterexample. The local affine refinement gives the precise faithfully flat quasi-compact descent used in the proof; author body retained without a new hypothesis.'),
    dict(page=469, source_id='ASTRA-VIII-0016',
         note='The claimed closed graph is constructed after the local affine/separated restriction already allowed by the argument.'),
    dict(page=470, source_id='ASTRA-VIII-0017',
         note='The Koszul vanishing statement is recorded in its positive-degree scope; H_0 is the displayed quotient sheaf.'),
    dict(page=471, source_id='ASTRA-VIII-0033',
         note='The printed U-prime flatness is retained through the exact localization maps, separately from the assumed flatness of U.'),
    dict(page=494, source_id='ASTRA-VIII-0077',
         note='The earlier g notation is retained with the structural extension to V, the universal-derivation isomorphism, and its restriction to Z; the distinct Euler-sequence formula receives its separately proved f correction.'),
    dict(page=496, affected_pages=[496, 497], source_id='ASTRA-VIII-0091',
         note='The formal-series unit, nilpotent evaluation and inverse parameter substitution justify the unchanged residue calculation.')
]
result = dict(
    expose='VIII', range=[466, 497], decisions=len(D), patches=len(P),
    own_findings=len(OWN), page_statuses=len(S), fully_checked=32,
    partial_pages=[], coverage_counts={k: len(v) for k, v in expected.items()},
    missing_source_ids=missing,
    root_owned_records=[dict(source_id=sid, page=root_rows[sid]['page'],
                             review_file='review/middle/decisions.jsonl') for sid in root_owned],
    cross_expose_finding=dict(source_id=product['source_id'], own_scope=[496, 497],
                             supplement=supplement_id,
                             supplement_file='review/expose_ix/own_findings.jsonl'),
    redirected_packet_records=[
        dict(source_id='fr/codex/HOLD_VS_CORR.json#51', actual_page=515,
             assigned_review='review/expose_ix',
             reason='The exact G/U torseur paragraph is in the515 packet; no VIII image adjudication is claimed for it.')
    ],
    retained_scope_notes=retained_scope,
    validation='write_reviews.py replayed every ordered exact-anchor patch against both attached page layers, after root-owned middle patches. This audit verifies source-ID coverage and provenance; direct full-page image comparisons are separately recorded. Full French-reader compilation belongs to coordinator integration.',
    hashes={name: hashlib.sha256((O / name).read_bytes()).hexdigest() for name in
            ('write_reviews.py', 'decisions.jsonl', 'patches.jsonl',
             'own_findings.jsonl', 'page_status.jsonl')}
)
(O / 'final_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: result[k] for k in
                  ('decisions', 'patches', 'own_findings', 'fully_checked',
                   'coverage_counts', 'missing_source_ids')}, ensure_ascii=False))
