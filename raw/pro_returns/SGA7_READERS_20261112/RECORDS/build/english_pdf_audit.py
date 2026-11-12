#!/usr/bin/env python3
"""Verify final English PDF text against the edition's apparatus policy."""
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'output/records'


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def pdf_text(path):
    return subprocess.run(['pdftotext', '-layout', '-enc', 'UTF-8', str(path), '-'],
                          check=True, capture_output=True, text=True).stdout


def main():
    notes = json.loads((REC / 'EN_INHERITED_EDITORIAL_NOTES.json').read_text())
    expected_notes = {n['id'] for n in notes}
    parts = json.loads((ROOT / 'work/en_variant_data.json').read_text())
    baseline_path = ROOT / 'work/en_pre_attribution_snapshot.json'
    baseline = json.loads(baseline_path.read_text()) if baseline_path.exists() else {}
    previous_text = baseline.get('pdf_text_sha256', {})
    phrases = ['The last printed implication', 'The ink beside the vertical arrow',
               'Both printed citations', 'This paragraph prints']
    results = []
    for form in ['diplomatic', 'reading', 'corrected_apparatus']:
        name = 'SGA7_EN_' + form
        pdf = ROOT / 'output/en' / (name + '.pdf')
        text = pdf_text(pdf)
        flat = re.sub(r'\s+', ' ', text)
        ids = re.findall(r'EN-NOTE-\d{3}', text)
        headings = text.count('Critical apparatus')
        phrase_counts = {p: flat.count(p) for p in phrases}
        assert 'geometric geometric' not in flat, (name, 'duplicated geometric qualifier')
        if form == 'corrected_apparatus':
            assert headings == len(parts), (name, 'apparatus headings', headings)
            assert len(ids) == len(expected_notes) and set(ids) == expected_notes, (name, 'inherited note identifiers')
            assert all(n == 1 for n in phrase_counts.values()), (name, 'editorial note preservation', phrase_counts)
        else:
            assert headings == 0 and not ids, (name, 'apparatus in a plain body reader')
            assert not any(phrase_counts.values()), (name, 'editorial note remains in authorial body', phrase_counts)
        source_hash = sha(pdf.with_suffix('.tex').read_bytes())
        pdf_hash = sha(pdf.read_bytes())
        status = json.loads((REC / 'compile' / (name + '.json')).read_text())
        assert status['source_sha256'] == source_hash and status['pdf_sha256'] == pdf_hash, (name, 'stale compilation record')
        text_hash = sha(text)
        row = {'reader': name, 'source_sha256': source_hash, 'pdf_sha256': pdf_hash,
               'pdf_text_sha256': text_hash, 'critical_apparatus_headings': headings,
               'inherited_note_ids': len(ids), 'unexpected_editorial_body_phrases': phrase_counts,
               'duplicate_geometric_phrase': False}
        if pdf.name in previous_text:
            row['pdf_text_identical_to_pre_attribution_snapshot'] = text_hash == previous_text[pdf.name]
            if form != 'corrected_apparatus':
                assert row['pdf_text_identical_to_pre_attribution_snapshot'], (name, 'plain reader PDF text changed in metadata-only update')
        results.append(row)
    (REC / 'EN_PDF_TEXT_QA.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
