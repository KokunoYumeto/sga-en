#!/usr/bin/env python3
"""Apply a freshly verified exact source map to EN variant metadata only.

The input master and both branch bodies must have the audited hashes. Call IDs,
before/after readings, and every file outside EN_variants.json are unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prepared', required=True, type=Path)
    ap.add_argument('--audit', required=True, type=Path)
    args = ap.parse_args()
    report = json.loads((args.audit / 'INDEPENDENT_EN_MASTER_AUDIT.json').read_text())
    assert report['body_and_original_variation_preservation_passed']
    assert report['operator_and_script_boundary_summary']['no_operator_argument_interference']
    for key, name in [('master', 'EN_annotated_body.tex'),
                      ('prepared_corrected', 'EN_corrected_body.tex'),
                      ('prepared_diplomatic', 'EN_diplomatic_body.tex'),
                      ('master_variants', 'EN_variants.json'),
                      ('copied_input_variants', 'EN_variants_input.json')]:
        assert digest((args.prepared / name).read_text()) == report['input_hashes'][key], name
    variants = json.loads((args.prepared / 'EN_variants.json').read_text())
    resolutions = json.loads((args.audit / 'EN_MASTER_RESOLVED_SOURCES.json').read_text())
    by_id = {v['id']: v for v in resolutions}
    assert len(by_id) == len(variants) and set(by_id) == {v['id'] for v in variants}
    old_readings = [(v['id'], v['before'], v['after']) for v in variants]
    for v in variants:
        exact = by_id[v['id']]
        v['source'] = exact['source']
        v['page'] = exact['page']
        v['pages'] = exact['pages']
        v['expose'] = '; '.join(x for x in exact['exposes'] if x is not None)
        v['source_component'] = exact['component_id']
        v['source_input_ids'] = exact['input_ids']
        v['page_basis'] = 'Folios explicitly recorded on the original source variants in this exact replay component; no interpolated English folio claim.'
        if len(v['pages']) > 1:
            v['source'] += '; Source component spans recorded folios ' + ', '.join(str(p) for p in v['pages']) + '; the grouped source citation retains this range.'
    assert old_readings == [(v['id'], v['before'], v['after']) for v in variants]
    (args.prepared / 'EN_variants.json').write_text(json.dumps(variants, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'exact_source_metadata_applied': len(variants),
                      'multiple_recorded_folios': sum(len(v['pages']) > 1 for v in variants),
                      'body_bytes_and_call_ids_preserved': True}))


if __name__ == '__main__':
    main()
