#!/usr/bin/env python3
"""Supply master-default PDFs after proving source and compilation identity."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output'
REC = OUT / 'records'
PAIRS = {
    'FR': ('SGA7_FR_master_annote', 'SGA7_FR_corrige_apparat'),
    'EN': ('SGA7_EN_annotated_master', 'SGA7_EN_corrected_apparatus'),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    results = []
    for lang, (master, corrected) in PAIRS.items():
        directory = OUT / lang.lower()
        source = directory / (corrected + '.tex')
        master_source = directory / (master + '.tex')
        pdf = directory / (corrected + '.pdf')
        master_pdf = directory / (master + '.pdf')
        status = json.loads((REC / 'compile' / (corrected + '.json')).read_text())
        assert master_source.read_bytes() == source.read_bytes(), (lang, 'Master selector/source differs')
        assert status['success'] and not status['errors'], (lang, 'Corrected compilation failed')
        assert len(status['passes']) >= 3 and all(p['exit_code'] == 0 for p in status['passes']), (lang, 'Three passes required')
        assert status['source_sha256'] == digest(source), (lang, 'Compiled source is stale')
        assert status['pdf_sha256'] == digest(pdf), (lang, 'Compiled PDF is stale')
        shutil.copy2(pdf, master_pdf)
        evidence = {
            'master': master_source.name,
            'default_form': 'corrected with apparatus',
            'source_identical_to': source.name,
            'source_sha256': digest(source),
            'pdf': master_pdf.name,
            'pdf_identical_to': pdf.name,
            'pdf_sha256': digest(pdf),
            'pages': status['pages'],
            'compile_status': 'compile/' + corrected + '.json',
            'proof': 'The two TeX files are byte-identical. The master PDF is the byte-identical PDF from the successful three-pass compilation of that source.'
        }
        (REC / (lang + '_MASTER_PDF_EQUIVALENCE.json')).write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
        results.append({'language': lang, 'master_pdf': master_pdf.name, 'pages': status['pages']})
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
