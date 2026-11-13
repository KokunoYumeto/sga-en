#!/usr/bin/env python3
"""Map inspected print markers to source lines and actual built PDF pages.

This is a marker-location table. It does not claim that each printed page fits
on one reflowed PDF page, or that a marker search verifies paragraph fidelity.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MARKER = re.compile(r'%%%%%%%%%%\s+scan idx\s+\d+\s*\|\s*folio\s+(\d+)\s+%%%%%%%%%%')


def bounds(text, end_marker=None):
    markers = list(MARKER.finditer(text))
    result = {}
    end = text.index(end_marker) if end_marker else len(text)
    for i, marker in enumerate(markers):
        stop = markers[i + 1].start() if i + 1 < len(markers) else end
        result[int(marker.group(1))] = (
            text.count('\n', 0, marker.start()) + 1,
            text.count('\n', 0, stop))
    return result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    master = HERE / 'DRAFT_SGA6_EN_annotated_master.tex'
    pdf = HERE / 'DRAFT_SGA6_EN_corrected_apparatus.pdf'
    source = master.read_text()
    en = bounds(source, '% SGA_END_REVIEWED_EN_BODY')
    fr = bounds((ROOT / 'fr/sga6/current/main.tex').read_text())
    pdf_markers = {}
    doc = fitz.open(pdf)
    for i, page in enumerate(doc, 1):
        for num in re.findall(r'\[print\s+(\d+)\]', page.get_text()):
            pdf_markers.setdefault(int(num), []).append(i)
    patch_for = {}
    for line in (HERE / 'EN_TRANSLATION_PATCHES.jsonl').read_text().splitlines():
        patch = json.loads(line)
        m = re.fullmatch(r'(\d+)[–-](\d+)', str(patch.get('page', '')))
        if m:
            for page in range(int(m.group(1)), int(m.group(2)) + 1):
                patch_for[page] = patch['id']
    rows = []
    for page, (start, end) in sorted(en.items()):
        rows.append(dict(
            printed_folio=page, main_scan_PDF_page=page + 14,
            native_witness_page=page + 11,
            supplied_French_current_start_line=fr[page][0],
            supplied_French_current_end_line=fr[page][1],
            generated_English_master_start_line=start,
            generated_English_master_end_line=end,
            corrected_PDF_pages_containing_start_marker=','.join(map(str, sorted(set(pdf_markers.get(page, []))))),
            translation_record=patch_for.get(page, ''),
            status='inspected printed-page marker; reflowed PDF content may continue on later pages'))
    with (HERE / 'EN_REVIEWED_ALIGNMENT_HINTS.tsv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    result = dict(
        scope='printed1–' + str(max(en)),
        generated_master_sha256=digest(master), corrected_PDF_sha256=digest(pdf),
        corrected_PDF_page_count=len(doc),
        marker_count=len(rows),
        markers_absent_from_PDF=[r['printed_folio'] for r in rows if not r['corrected_PDF_pages_containing_start_marker']],
        line_numbers='one-based; start includes the source page-marker comment; end precedes the next source marker',
        limitation='PDF column locates the printed-page start marker only. No page-span or whole-volume alignment claim.')
    (HERE / 'EN_ALIGNMENT_HINTS_STATUS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
