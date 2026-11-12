#!/usr/bin/env python3
"""Prove the final historical-attribution update preserves English readings.

The baseline is the frozen, fully audited English snapshot taken immediately
before the shared French attribution review. This report is independent of the
reviewed reconstruction proposals and does not regenerate or alter them.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work'
REC = ROOT / 'output/records'


def read(path):
    return json.loads(path.read_text())


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def operation_audit(fr_rows):
    frozen = read(WORK / 'en_pre_attribution_operations.json')
    expected = {'ED-EN-NONMATH-I-' + n for n in
                ['004', '013', '017', '018', '025', '027', '028', '030', '035', '045', '046', '049', '055', '056', '057', '060',
                 'II26', 'IX340', 'IX512', 'VII177', 'VIII232']}
    expected |= {'ED-EN-NONMATH-G' + n for n in
                 ['007', '020', '029', '033', '034', '036', '037', '038', '039', '040', '042', '044', '050']}
    diagnostic_keys = {'prior_exact_printed_present', 'component_projection_check'}
    metadata = []
    diagnostics = []
    for path, old in frozen['inputs'].items():
        new = read(ROOT / path)
        a = old if isinstance(old, list) else [old]
        b = new if isinstance(new, list) else [new]
        assert len(a) == len(b), ('operation count changed', path)
        for x, y in zip(a, b):
            difference = {k: {'before': x.get(k), 'after': y.get(k)} for k in set(x) | set(y) if x.get(k) != y.get(k)}
            assert set(difference) <= {'source', 'source_ref'} | diagnostic_keys, ('operative field changed', path, x.get('id'), difference)
            identity = x.get('id', x.get('index'))
            d = {k: v for k, v in difference.items() if k in diagnostic_keys}
            if d:
                diagnostics.append({'input': path, 'id': identity, 'fields': d})
            m = {k: v for k, v in difference.items() if k not in diagnostic_keys}
            if not m:
                continue
            assert identity in expected, ('unreviewed operation metadata change', path, identity)
            assert set(m) == {'source'}, (identity, 'unexpected source_ref change')
            ids = x.get('french_apparatus_ids') or list(dict.fromkeys(re.findall(r'F7II-[IVX]+-\d+\.\d+', x['source'])))
            related = [fr_rows[i] for i in ids]
            assert any(r['metadata_changed'] for r in related), (identity, 'no changed French ancestry')
            for prefix, operation in [('old', x), ('new', y)]:
                if 'body_patch' in path:
                    citation = '; '.join(sorted({r[prefix + '_source'] for r in related} | {r[prefix + '_source_ref'] for r in related}))
                elif 'editorial' in path:
                    citation = '; '.join(sorted({r[prefix + '_source'] for r in related}) + sorted({r[prefix + '_source_ref'] for r in related}))
                else:
                    assert len(related) == 1, identity
                    r = related[0]
                    citation = f"{identity}; {r['id']}; {r[prefix + '_source']}; fr/sga7ii/{{diplomatic,current}}/expose_{r['expose']}_body.tex; folio {r['page']}"
                assert operation['source'] == citation, (identity, 'source does not exactly reproduce French ancestry', prefix)
            metadata.append({'input': path, 'id': identity, 'component': x['component'], 'fields': m,
                             'french_ancestry': [{'id': r['id'], 'status': r['status'], 'metadata_changed': r['metadata_changed'],
                                                'old_source': r['old_source'], 'new_source': r['new_source'],
                                                'old_source_ref': r['old_source_ref'], 'new_source_ref': r['new_source_ref']} for r in related]})
    assert {r['id'] for r in metadata} == expected, ('reviewed ancestry footprint changed', {r['id'] for r in metadata} ^ expected)
    for path, digest in frozen['proposal_sha256'].items():
        assert sha((ROOT / path).read_bytes()) == digest, ('frozen proposal changed', path)
    return metadata, diagnostics


def verify_inherited_source(old, new, operations):
    """Replace exact old/new citation strings by the same stable operation ID."""
    linked = []
    for r in sorted(operations, key=lambda z: -len(z['fields']['source']['before'])):
        a = r['fields']['source']['before']
        b = r['fields']['source']['after']
        if a in old and b in new:
            marker = '<attribution:' + r['id'] + '>'
            old = old.replace(a, marker)
            new = new.replace(b, marker)
            linked.append(r['id'])
    assert linked and old == new, ('English citation change lacks exact operation ancestry', old, new, linked)
    return linked


def main(source_only=False):
    baseline = read(WORK / 'en_pre_attribution_snapshot.json')
    final = read(WORK / 'en_variant_data.json')
    french_rows = {r['id']: r for r in read(REC / 'FR_ATTRIBUTION_AUDIT.json')['rows'] if r['scope'] == 'apparatus'}
    operation_metadata, operation_diagnostics = operation_audit(french_rows)
    assert [(r['volume'], r['expose']) for r in baseline['parts']] == [(r['volume'], r['expose']) for r in final]
    permitted = {'source', 'source_ref', 'kind', 'source_match'}
    parts = []
    changes = []
    for old, new in zip(baseline['parts'], final):
        body_hashes = {}
        for branch in ['diplomatic', 'corrected', 'annotated']:
            assert old[branch] == new[branch], ('body changed during attribution update', old['expose'], branch)
            body_hashes[branch] = sha(new[branch])
        assert [r['id'] for r in old['entries']] == [r['id'] for r in new['entries']], ('apparatus IDs changed', old['expose'])
        for a, b in zip(old['entries'], new['entries']):
            difference = {k: {'before': a.get(k), 'after': b.get(k)} for k in set(a) | set(b) if a.get(k) != b.get(k)}
            assert set(difference) <= permitted, ('non-attribution apparatus change', a['id'], difference)
            if difference:
                if old['expose'] == 'VI':
                    ancestor = french_rows[a['id']]
                    for key, value in difference.items():
                        assert value == {'before': ancestor['old_' + key], 'after': ancestor['new_' + key]}, (a['id'], key, 'shared attribution mismatch')
                    ancestry = ['FR_ATTRIBUTION_AUDIT.json#' + a['id']]
                else:
                    assert set(difference) == {'source'}, ('non-shared entry metadata beyond source', a['id'])
                    candidates = [r for r in operation_metadata if a['source_ref'].endswith(r['component'])]
                    ancestry = verify_inherited_source(a['source'], b['source'], candidates)
                changes.append({'id': a['id'], 'volume': old['volume'], 'expose': old['expose'], 'page': a['page'],
                                'fields': difference, 'exact_ancestry': ancestry})
        parts.append({'volume': old['volume'], 'expose': old['expose'], 'entries': len(new['entries']),
                      'all_projected_bodies_and_annotated_text_byte_identical': True, 'body_sha256': body_hashes})
    apparatus = read(REC / 'EN_APPARATUS.json')
    assert len(baseline['apparatus']) == len(apparatus)
    for a, b in zip(baseline['apparatus'], apparatus):
        assert {k: v for k, v in a.items() if k not in permitted} == {k: v for k, v in b.items() if k not in permitted}, a['id']
    csv.field_size_limit(10000000)
    current_changes = list(csv.DictReader((REC / 'CHANGES_EN.tsv').open(), delimiter='\t'))
    previous_changes = baseline['changes_en_before_nonmath_propagation']
    assert len(previous_changes) == len(current_changes), 'CHANGES_EN row count changed'
    change_sources = []
    for number, (a, b) in enumerate(zip(previous_changes, current_changes), 1):
        assert {k: v for k, v in a.items() if k != 'source'} == {k: v for k, v in b.items() if k != 'source'}, ('CHANGES_EN substantive row changed', number)
        if a['source'] != b['source']:
            ancestry = verify_inherited_source(a['source'], b['source'], operation_metadata)
            change_sources.append({'row': number, 'page': a['page'], 'place': a['place'], 'before_source': a['source'],
                                   'after_source': b['source'], 'exact_ancestry': ancestry})
    files = []
    for name, previous in baseline['files'].items():
        if not name.endswith('.tex'):
            continue
        path = ROOT / 'output/en' / name
        current = sha(path.read_bytes())
        row = {'file': name, 'before_source_sha256': previous, 'after_source_sha256': current, 'source_changed': previous != current}
        if 'annotated_master' not in name and not source_only:
            status_path = REC / 'compile' / (path.stem + '.json')
            pdf_path = path.with_suffix('.pdf')
            if not status_path.exists() or not pdf_path.exists():
                row['compile_evidence'] = 'not available in this source-only output tree'
                files.append(row)
                continue
            status = read(status_path)
            row['compile_status_matches_current_source'] = status['source_sha256'] == current
            row['successful_passes'] = sum(r['exit_code'] == 0 for r in status['passes'])
            row['pages'] = status['pages']
            row['pdf_sha256'] = sha(pdf_path.read_bytes())
            row['pdf_matches_compile_status'] = row['pdf_sha256'] == status['pdf_sha256']
        files.append(row)
    result = {'baseline': 'work/en_pre_attribution_snapshot.json', 'parts': parts, 'parts_verified': len(parts),
              'apparatus_entries': len(apparatus), 'metadata_changed_entries': len(changes),
              'metadata_change_scope': sorted(set(r['expose'] for r in changes)), 'permitted_changed_fields': sorted(permitted),
              'projected_body_changes': 0, 'apparatus_id_or_reading_changes': 0, 'metadata_changes': changes,
              'operation_source_changes': operation_metadata, 'operation_diagnostic_refreshes': operation_diagnostics,
              'operative_fields_preserved': True, 'frozen_proposal_hashes_preserved': True,
              'changes_en_rows_verified': len(current_changes), 'changes_en_snapshot_note': baseline['changes_en_snapshot_note'],
              'changes_en_order_place_before_after_preserved': True, 'changes_en_source_changes': change_sources,
              'reader_files': files, 'source_only': source_only,
              'reproduction': 'python build/english_attribution_audit.py' + (' --source-only' if source_only else '')}
    (REC / 'EN_ATTRIBUTION_UPDATE.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['parts_verified', 'apparatus_entries', 'metadata_changed_entries',
                     'metadata_change_scope', 'projected_body_changes', 'apparatus_id_or_reading_changes', 'reader_files']}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-only', action='store_true', help='Verify source invariance without reading PDF or compiler records')
    main(parser.parse_args().source_only)
