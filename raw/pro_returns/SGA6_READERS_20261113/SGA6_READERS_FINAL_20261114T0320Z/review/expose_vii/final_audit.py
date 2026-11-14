"""Verify exact ledger coverage; image review is documented by the reviewer records."""
from pathlib import Path
import collections, hashlib, json, re

R = Path(__file__).resolve().parents[2]
O = R / 'review/expose_vii'
read = lambda p: [json.loads(x) for x in p.read_text().splitlines()]
D, P, OWN, S = [read(O / name) for name in
                 ('decisions.jsonl', 'patches.jsonl', 'own_findings.jsonl', 'page_status.jsonl')]
seen = {x['source_id'] for x in D}
assert len(seen) == len(D), 'duplicate decision source IDs'
expected = collections.defaultdict(list)
inside = lambda x: isinstance(x.get('page'), int) and 416 <= x['page'] <= 465
for path in sorted((R / 'check/findings').glob('*.json')):
    for i, x in enumerate(json.loads(path.read_text()), 1):
        if inside(x): expected['checker'].append(str(path.relative_to(R)) + f'#{i}')
for name in ('fixes/FIXLOG_6.jsonl', 'fixes/FIXLOG_6_CURRENT.jsonl'):
    for i, x in enumerate(read(R / name), 1):
        if inside(x): expected[name].append(f'{name}#{i}')
for i, x in enumerate(json.loads((R / 'fixes/MISPRINTS_6.json').read_text()), 1):
    if inside(x): expected['misprint'].append(f'fixes/MISPRINTS_6.json#{i}')
C = json.loads((R / 'fixes/RECONCILE_CODEX_6.json').read_text())['entries']
core = {x['id'] for x in C if x.get('expose') == 'VII'}
for i, x in enumerate(C, 1):
    if x['id'] in core: expected['codex_including_tags'].append(f'fixes/RECONCILE_CODEX_6.json#{i}')
expected['hold_true_VII_loci'] = [f'fr/codex/HOLD_VS_CORR.json#{i}' for i in (44, 45)]
missing = [sid for ids in expected.values() for sid in ids if sid not in seen]
assert not missing, missing
assert set(sid for ids in expected.values() for sid in ids) == seen

root_owned = ['fixes/REPLAY_MANUAL_6.json#12',
              'fixes/MANUAL_6_findings/MANUAL_6_findings_451_455.json#1']
root_rows = {x['source_id']: x for x in read(R / 'review/middle/decisions.jsonl')}
for sid in root_owned:
    assert sid in root_rows and sid not in seen
assert [x['page'] for x in S] == list(range(416, 466))
assert all(x['checked_against_scan'] for x in S)
assert len({x['source_id'] for x in OWN}) == len(OWN)
assert not ({x['source_id'] for x in OWN} & seen)
for x in D + P + OWN + S:
    text = json.dumps(x, ensure_ascii=False)
    assert '/workspace/' not in text
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', text)
    if 'image' in x: assert x['image'].startswith('scan/')
for x in P:
    assert x['source_id'] in seen or x['source_id'] in {y['source_id'] for y in OWN}

redirected = []
for i, pg, anchor in [(46, 472, "un schéma lisse sur $W$"),
                       (47, 472, 'Proposition 1.6.'),
                       (48, 472, 'au cas ou $f$'),
                       (49, 477, "les immersions $i',j,j'$ sont régulières"),
                       (50, 477, 'cela entrainera que le mapping cylinder')]:
    assert anchor in (R / f'build/page_packets/{pg}/diplomatic.tex').read_text()
    sid = f'fr/codex/HOLD_VS_CORR.json#{i}'
    assert sid not in seen
    redirected.append(dict(source_id=sid, actual_page=pg, assigned_review='review/expose_viii',
        status='pending direct VIII image adjudication',
        reason='The nominal VII packet folio came from outdated TeX line offsets; exact text is in the indicated VIII source packet. This relocation alone makes no scan-reading claim.'))

unresolved = [
    dict(page=431, affected_pages=[430, 431], source_id='ASTRA-VII-0036',
         type='established_mathematical_source_error',
         note='The unqualified square-zero parenthesis fails for the unit and for the stated rank-four even-degree example. Source body retained; exact emendation unresolved.'),
    dict(page=440, source_id='check/findings/findings_436_440.json#56',
         type='unfinished_source_reference',
         note='Printed reference stops at(IV. Candidate IV2.12.3 was directly inspected, but an exact omitted locator is not recoverable.'),
    dict(page=443, source_id='ASTRA-VII-0085', type='established_mathematical_source_error',
         note='The split graded presentation gives a degree-zero vertical map0→A, contradicting the printed all-n isomorphism assertion. No range hypothesis is added.'),
    dict(page=449, source_id='ASTRA-VII-0099', type='retained_wording_ambiguity',
         note='The explicit conormal quotient and chart trivialization support the retained noun phrase. Its literal ambient-ideal interpretation is separately disproved at stalks.'),
    dict(page=464, source_id='ASTRA-VII-0136', type='unfinished_source_references',
         note='Three numerical locators after IV/X/X are blank in print and remain blank in both forms.'),
    dict(page=465, source_id='check/findings/findings_461_465.json#25',
         type='unfinished_source_reference',
         note='The IV locator remains blank; current restores the independently missing closing parenthesis.'),
    dict(page=465, source_id='ASTRA-VII-0137', type='unresolved_integral_lift_strength',
         note='The exact tensorized localization construction proves the rational conclusion. No additional integral-choice body emendation is established.')
]
result = dict(expose='VII', range=[416, 465], decisions=len(D), patches=len(P),
              own_findings=len(OWN), page_statuses=len(S), fully_checked=50,
              partial_pages=[], coverage_counts={k: len(v) for k, v in expected.items()},
              missing_source_ids=missing, redirected_packet_records=redirected,
              root_owned_records=[dict(source_id=sid, page=root_rows[sid]['page'],
                                       review_file='review/middle/decisions.jsonl') for sid in root_owned],
              unresolved=unresolved,
              validation='write_reviews.py replayed every ordered exact-anchor patch against both attached page layers, after root-owned middle patches. This audit verifies ledger coverage and provenance; the image comparisons are documented per page and decision. A full French-reader compile belongs to the coordinator integration step.',
              hashes={name: hashlib.sha256((O / name).read_bytes()).hexdigest() for name in
                      ('write_reviews.py', 'decisions.jsonl', 'patches.jsonl', 'own_findings.jsonl', 'page_status.jsonl')})
(O / 'final_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ('decisions', 'patches', 'own_findings', 'fully_checked',
                                      'coverage_counts', 'missing_source_ids')}, ensure_ascii=False))
