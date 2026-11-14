#!/usr/bin/env python3
"""Load the exact French text used by the English passage comparison.

Exposé 0 uses the supplied current source plus the early reviewer's patches.
Later exposés use the coordinator's baseline page packets, which include recorded
TeX syntax repairs, plus the exact reviewed patches in their review directories.
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


def load_reviewed_pages(end, layer='current', start=1):
    assert 1 <= start <= end
    supplied = full_pages((ROOT / f'fr/sga6/{layer}/main.tex').read_text())
    # Consume only explicitly certified, text-empty numeric leaves.  Source
    # folio690 has no marker in the supplied main file; its separate scan
    # certificate is authoritative.  This does not redistribute the existing
    # folio689 continuation macros or infer any other missing page.
    declared_blanks = {}
    blank_path = ROOT / 'review/expose_xiv_amendments/new_pages.jsonl'
    if blank_path.exists():
        for line in blank_path.read_text().splitlines():
            row = json.loads(line)
            page = row.get('page')
            if not isinstance(page, int) or not start <= page <= end or page in supplied:
                continue
            if row.get('layer') not in [layer, 'both']:
                continue
            text = row['text']
            marker = MARKER.fullmatch(text.strip())
            if not row.get('source_blank') or marker is None or int(marker.group(1)) != page:
                raise ValueError(f'Declared missing page{page} is not a certified blank numeric leaf')
            if page in declared_blanks:
                raise ValueError(f'Duplicate declared missing page{page}')
            declared_blanks[page] = (text, row, hashlib.sha256(line.encode()).hexdigest())
    pages = {}
    bases = []
    baseline_diffs = []
    blank_records = []
    for page in range(start, end + 1):
        relative = f'fr/sga6/{layer}/main.tex'
        if page in declared_blanks:
            text, row, row_sha = declared_blanks[page]
            relative = str(blank_path.relative_to(ROOT))
            pages[page] = text
            bases.append(dict(page=page, base=relative,
                              base_page_sha256=hashlib.sha256(text.encode()).hexdigest(),
                              declared_source_blank=True, source_id=row['source_id'],
                              declaration_record_sha256=row_sha))
            blank_records.append(dict(page=page, source_id=row['source_id'],
                                      declaration=relative, declaration_record_sha256=row_sha,
                                      source_blank=True, evidence=row.get('evidence'),
                                      pdf_page=row.get('pdf_page'), witness_page=row.get('witness_page'),
                                      insert_before=row.get('insert_before')))
            continue
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
    already_present = []
    exact_applied = set()
    patch_sets = [(ROOT / 'review/early/patches.jsonl', 1, 77),
                  (ROOT / 'review/expose_i/patches.jsonl', 78, 159),
                  (ROOT / 'review/middle/patches.jsonl', 160, 221),
                  (ROOT / 'review/expose_ii/patches.jsonl', 160, 221),
                  (ROOT / 'review/expose_ii_amendments/patches.jsonl', 160, 221)]
    # Later disjoint translation contributions use the same recorded order as
    # the French assembler: late/middle first, then review directories sorted
    # by name. Page filtering keeps the previously frozen1–221 composition
    # unchanged. The existence of a patch stream makes no coverage assertion;
    # translators must separately check the reviewer page-status/handoff data.
    if end > 221:
        primary = ['front', 'early', 'late', 'middle']
        extra = sorted(p.name for p in (ROOT / 'review').iterdir()
                       if p.is_dir() and p.name not in primary)
        for directory in ['late', 'middle'] + extra:
            path = ROOT / 'review' / directory / 'patches.jsonl'
            if path.exists():
                patch_sets.append((path, 222, end))
    # These exact anchors were recorded after all ordinary source reviews.
    # They are applied last, including to the earlier numbered exposés.
    for directory in sorted((ROOT/'review').iterdir()):
        path=directory/'post_review_patches.jsonl'
        if directory.is_dir() and path.exists():patch_sets.append((path,1,end))
    for path, lo, hi in patch_sets:
        for line in path.read_text().splitlines():
            patch = json.loads(line)
            page = patch['page']
            if not isinstance(page, int) or not start <= page <= end or not lo <= page <= hi or patch['layer'] not in [layer, 'both']:
                continue
            if page <= 77 and patch.get('kind') == 'marker':
                continue
            n = pages[page].count(patch['old'])
            expected = patch.get('expected_count', 1)
            identity = (page, layer, patch['old'], patch['new'])
            if n == 0 and identity in exact_applied:
                assert pages[page].count(patch['new']) >= expected
                already_present.append(dict(page=page, source_id=patch['source_id'], layer=patch['layer'],
                                            patch_record_sha256=hashlib.sha256(line.encode()).hexdigest(),
                                            reason='Identical old/new patch already applied in this ordered composition.'))
                continue
            if n != expected:
                raise ValueError(f"{patch['source_id']} page{page}: anchor count {n}, expected {expected}")
            pages[page] = pages[page].replace(patch['old'], patch['new'])
            exact_applied.add(identity)
            applied.append(dict(page=page, source_id=patch['source_id'], layer=patch['layer'],
                                occurrence_count=expected,
                                patch_record_sha256=hashlib.sha256(line.encode()).hexdigest()))
    result = {}
    for page, text in pages.items():
        marker = MARKER.search(text)
        assert marker and int(marker.group(1)) == page
        result[page] = text[marker.end():]
        bases[page - start]['reviewed_page_sha256'] = hashlib.sha256(text.encode()).hexdigest()
    return result, dict(scope=f'printed{start}–{end}', layer=layer, bases=bases,
                        applied_patches=applied, already_present_exact_patches=already_present,
                        baseline_differences=baseline_diffs,
                        declared_blank_pages=blank_records)
