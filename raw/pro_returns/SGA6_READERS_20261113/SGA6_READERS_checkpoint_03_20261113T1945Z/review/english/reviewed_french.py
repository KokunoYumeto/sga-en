#!/usr/bin/env python3
"""Load the exact French text used by the English passage comparison.

Exposé 0 uses the supplied current source plus the early reviewer's patches.
Exposé I uses the coordinator's baseline page packets, which include recorded
TeX syntax repairs, plus the exact current/both patches in review/expose_i.
Whole-page patches keep their marker comments during application. Baseline
differences from the supplied source and all hashes are recorded explicitly.
"""
from pathlib import Path
import difflib
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MARKER = re.compile(r'%%%%%%%%%%\s+scan idx\s+\d+\s*\|\s*folio\s+(\d+)\s+%%%%%%%%%%')


def full_pages(text):
    matches = list(MARKER.finditer(text))
    return {int(m.group(1)): text[m.start():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
            for i, m in enumerate(matches)}


def load_reviewed_pages(end, layer='current'):
    supplied = full_pages((ROOT / f'fr/sga6/{layer}/main.tex').read_text())
    pages = {}
    bases = []
    baseline_diffs = []
    for page in range(1, end + 1):
        relative = f'fr/sga6/{layer}/main.tex'
        text = supplied[page]
        if page >= 78:
            relative = f'build/page_packets/{page}/{layer}.tex'
            text = (ROOT / relative).read_text()
            for tag, a, b, c, d in difflib.SequenceMatcher(None, supplied[page], text, autojunk=False).get_opcodes():
                if tag != 'equal':
                    baseline_diffs.append(dict(page=page, supplied_fragment=supplied[page][a:b],
                                               reference_fragment=text[c:d],
                                               basis='coordinator baseline page packet before scan-review patches'))
        pages[page] = text
        bases.append(dict(page=page, base=relative,
                          base_page_sha256=hashlib.sha256(text.encode()).hexdigest()))
    applied = []
    patch_sets = [(ROOT / 'review/early/patches.jsonl', 1, 77),
                  (ROOT / 'review/expose_i/patches.jsonl', 78, 159)]
    for path, lo, hi in patch_sets:
        for line in path.read_text().splitlines():
            patch = json.loads(line)
            page = patch['page']
            if page > end or not lo <= page <= hi or patch['layer'] not in [layer, 'both']:
                continue
            if page <= 77 and patch.get('kind') == 'marker':
                continue
            n = pages[page].count(patch['old'])
            expected = patch.get('expected_count', 1)
            if n != expected:
                raise ValueError(f"{patch['source_id']} page{page}: anchor count {n}, expected {expected}")
            pages[page] = pages[page].replace(patch['old'], patch['new'])
            applied.append(dict(page=page, source_id=patch['source_id'], layer=patch['layer'],
                                occurrence_count=expected,
                                patch_record_sha256=hashlib.sha256(line.encode()).hexdigest()))
    result = {}
    for page, text in pages.items():
        marker = MARKER.search(text)
        assert marker and int(marker.group(1)) == page
        result[page] = text[marker.end():]
        bases[page - 1]['reviewed_page_sha256'] = hashlib.sha256(text.encode()).hexdigest()
    return result, dict(scope=f'printed1–{end}', layer=layer, bases=bases,
                        applied_patches=applied, baseline_differences=baseline_diffs)
