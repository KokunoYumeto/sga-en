"""Validate source-ID coverage and freeze metadata, without claiming image review."""
from pathlib import Path
import collections, hashlib, json, re

R = Path(__file__).resolve().parents[2]
O = R / 'review/expose_x'
read = lambda p: [json.loads(x) for x in p.read_text().splitlines()]
D = read(O / 'decisions.jsonl')
P = read(O / 'patches.jsonl')
OWN = read(O / 'own_findings.jsonl')
S = read(O / 'page_status.jsonl')
seen = {x['source_id'] for x in D}
assert len(seen) == len(D)
expected = collections.defaultdict(list)
inside = lambda x: isinstance(x.get('page'), int) and 519 <= x['page'] <= 594
for path in sorted((R / 'check/findings').glob('*.json')):
    for i, x in enumerate(json.loads(path.read_text()), 1):
        if inside(x): expected['checker'].append(str(path.relative_to(R)) + f'#{i}')
for name in ('fixes/FIXLOG_6.jsonl', 'fixes/FIXLOG_6_CURRENT.jsonl'):
    for i, x in enumerate(read(R / name), 1):
        if inside(x): expected[name].append(f'{name}#{i}')
for i, x in enumerate(json.loads((R / 'fixes/MISPRINTS_6.json').read_text()), 1):
    if inside(x): expected['misprint'].append(f'fixes/MISPRINTS_6.json#{i}')
C = json.loads((R / 'fixes/RECONCILE_CODEX_6.json').read_text())['entries']
core = {x['id'] for x in C if re.match(r'^X(?:\b|[, .])', x.get('expose', ''))}
for i, x in enumerate(C, 1):
    if x['id'] in core: expected['codex_including_tags'].append(f'fixes/RECONCILE_CODEX_6.json#{i}')
expected['hold_true_X_loci'] = [f'fr/codex/HOLD_VS_CORR.json#{i}' for i in range(52, 77)]
missing = [sid for ids in expected.values() for sid in ids if sid not in seen]
assert not missing, missing
owners = {}
for path in (R / 'review').glob('*/decisions.jsonl'):
    for x in read(path):
        owners.setdefault(x['source_id'], []).append(dict(file=str(path.relative_to(R)), page=x['page']))
redirected = []
for i in range(77, 103):
    sid = f'fr/codex/HOLD_VS_CORR.json#{i}'
    assert sid in owners
    assert all(x['page'] >= 595 for x in owners[sid])
    redirected.append(dict(source_id=sid, actual_review=owners[sid], reason='The historical packet folio was inferred from outdated TeX line positions; the actual text belongs to XII or XIII.'))
root_replay = 'fixes/REPLAY_MANUAL_6.json#13'
assert any(x['file'] == 'review/middle/decisions.jsonl' for x in owners[root_replay])
assert [x['page'] for x in S] == list(range(519, 595))
assert [x['page'] for x in S if not x['checked_against_scan']] == [549]
for x in D + P + OWN + S:
    text = json.dumps(x, ensure_ascii=False)
    assert '/workspace/' not in text
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', text)
result = dict(
    expose='X', range=[519, 594], decisions=len(D), patches=len(P), own_findings=len(OWN),
    page_statuses=len(S), fully_checked=sum(x['checked_against_scan'] for x in S), partial_pages=[549],
    coverage_counts={k: len(v) for k, v in expected.items()}, missing_source_ids=missing,
    redirected_packet_records=redirected, root_owned_replay=dict(source_id=root_replay, reviews=owners[root_replay]),
    unresolved=[
        dict(page=549, type='source_damage', note='Last-line lower strokes are absent in all three observed facsimiles; full-page certification withheld.'),
        dict(page=590, affected_pages=[590, 591, 592], source_id='ASTRA-X-0123', type='established_mathematical_source_error', note='Explicit colimit-preserving counterexample recorded; author body retained and emendation unresolved.')
    ],
    validation='write_reviews.py successfully replayed every ordered exact-anchor patch against both attached page layers, after root-owned middle patches. This audit verifies record coverage only; image evidence is recorded separately per decision/page.',
    hashes={name: hashlib.sha256((O / name).read_bytes()).hexdigest() for name in ('write_reviews.py', 'decisions.jsonl', 'patches.jsonl', 'own_findings.jsonl', 'page_status.jsonl')}
)
(O / 'final_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ('decisions', 'patches', 'own_findings', 'fully_checked', 'partial_pages', 'coverage_counts', 'missing_source_ids')}, ensure_ascii=False))
