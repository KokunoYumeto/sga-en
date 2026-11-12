#!/usr/bin/env python3
"""Audit the delivered source forms, folios, privacy and compiled artifacts."""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from audit_fr import projection

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output'
REC = OUT / 'records'
PRIVATE_PATH = re.compile(r'/(?:Users|home|root|workspace|mnt|tmp|usr|opt|var)/(?:[^\s<>]*)|[A-Z]:[\\/](?:Users|home|Desktop|Documents)[\\/]')
EMAIL = re.compile(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}')
FORMS = {
    'fr': ('SGA7_FR_master_annote', [
        ('SGA7_FR_diplomatique', 0), ('SGA7_FR_corrige_apparat', 1),
        ('SGA7_FR_texte_de_lecture', 2)]),
    'en': ('SGA7_EN_annotated_master', [
        ('SGA7_EN_diplomatic', 0), ('SGA7_EN_corrected_apparatus', 1),
        ('SGA7_EN_reading', 2)])}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--require-pdfs', action='store_true')
    args = ap.parse_args()
    checks = []
    errors = []
    source_results = []
    pdf_results = []

    def check(name, value, detail=None):
        row = {'check': name, 'passed': bool(value)}
        if detail is not None:
            row['detail'] = detail
        checks.append(row)
        if not value:
            errors.append(row)

    for lang, (master_name, forms) in FORMS.items():
        master_path = OUT / lang / (master_name + '.tex')
        master = master_path.read_text()
        check(lang + ': one master selector', len(re.findall(r'^\\SGAform=1$',master,re.M)) == 1)
        source_results.append({'file': master_path.relative_to(OUT).as_posix(),
                               'bytes': master_path.stat().st_size, 'sha256': digest(master_path)})
        for name, mode in forms:
            path = OUT / lang / (name + '.tex')
            text = path.read_text()
            check(name + ': exact master form', text == master.replace('\\SGAform=1\n', '\\SGAform=' + str(mode) + '\n', 1))
            dependencies = re.findall(r'(?<!\\)\\(?:input|include|includegraphics|bibliography)\s*\{[^}]+\}', text)
            check(name + ': standalone source content', not dependencies, dependencies)
            source_results.append({'file': path.relative_to(OUT).as_posix(),
                                   'bytes': path.stat().st_size, 'sha256': digest(path)})
            # Inspect actual rendered-source projection, not just the staging
            # data. Apparatus quotations escape TeX commands and cannot create
            # spurious source folio macros here.
            body = text.split('\\mainmatter', 1)[1]
            selected = projection(body, mode != 0)
            markers = re.findall(r'\\SGApage\{(I|II)\}\{([^{}]+)\}', selected)
            if lang == 'fr':
                for vol, total in [('I', 528), ('II', 438)]:
                    seq = [int(p) for v, p in markers if v == vol and p.isdigit()]
                    check(name + ': ordered ' + vol + ' folios', seq == list(range(1, total + 1)), {'count': len(seq), 'expected': total})
                check(name + ': introduction folios', [p for v, p in markers if v == 'I' and p in ['V', 'VI', 'VII']] == ['V', 'VI', 'VII'])
            else:
                invalid = []
                for vol, pg in markers:
                    numbers = re.findall(r'\d+', pg)
                    if numbers and not (1 <= int(numbers[-1]) <= (528 if vol == 'I' else 438)):
                        invalid.append([vol, pg])
                check(name + ': source folios in range', not invalid, {'anchors': len(markers), 'invalid': invalid})
                for pg in ['525', '526', '527', '528']:
                    check(name + ': catalogue folio ' + pg, ('I', pg) in markers)
            if not args.require_pdfs:
                continue
            status_path = REC / 'compile' / (name + '.json')
            pdf = path.with_suffix('.pdf')
            check(name + ': PDF and diagnostics present', pdf.exists() and status_path.exists())
            if not (pdf.exists() and status_path.exists()):
                continue
            status = json.loads(status_path.read_text())
            check(name + ': compile success', status['success'] and not status['errors'])
            check(name + ': three successful passes', len(status['passes']) >= 3 and all(x['exit_code'] == 0 for x in status['passes']))
            check(name + ': matching compiled source hash', status['source_sha256'] == digest(path))
            check(name + ': matching PDF hash', status['pdf_sha256'] == digest(pdf))
            check(name + ': no missing glyphs', not status['missing_characters'])
            log = (REC / 'compile' / (name + '.log')).read_text()
            unresolved = re.findall(r'^.*(?:undefined references|undefined citations|multiply defined|Rerun to get cross-references right|Rerun to get outlines right|pdfTeX warning).*$' , log, re.M | re.I)
            check(name + ': stable references', not unresolved, unresolved)
            import fitz
            document = fitz.open(pdf)
            outside = []
            pdf_privacy = []
            for kind, pattern in [('email', EMAIL), ('environment path', PRIVATE_PATH)]:
                if pattern.search(json.dumps(document.metadata, ensure_ascii=False)):
                    pdf_privacy.append({'location': 'PDF metadata', 'kind': kind})
            for page_index, page in enumerate(document):
                visible_text = page.get_text('text')
                for kind, pattern in [('email', EMAIL), ('environment path', PRIVATE_PATH)]:
                    if pattern.search(visible_text):
                        pdf_privacy.append({'pdf_page': page_index + 1, 'kind': kind})
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines', []):
                        for span in line['spans']:
                            x0, y0, x1, y1 = span['bbox']
                            if x0 < -0.5 or y0 < -0.5 or x1 > page.rect.width + 0.5 or y1 > page.rect.height + 0.5:
                                outside.append({'pdf_page': page_index + 1, 'bbox': span['bbox'], 'text': span['text'][:80]})
            check(name + ': no text outside page', not outside, outside)
            check(name + ': PDF text and metadata privacy', not pdf_privacy, pdf_privacy)
            check(name + ': reported page count', len(document) == status['pages'])
            pdf_results.append({'file': pdf.relative_to(OUT).as_posix(), 'pages': len(document),
                                'bytes': pdf.stat().st_size, 'sha256': digest(pdf),
                                'text_spans_outside_page': outside,
                                'overfull_boxes': status['overfull_boxes'], 'warnings': status['warnings']})

        if args.require_pdfs:
            corrected_name = next(name for name, mode in forms if mode == 1)
            corrected_pdf = OUT / lang / (corrected_name + '.pdf')
            master_pdf = OUT / lang / (master_name + '.pdf')
            proof_path = REC / (lang.upper() + '_MASTER_PDF_EQUIVALENCE.json')
            check(master_name + ': PDF and equivalence proof present', master_pdf.exists() and proof_path.exists())
            if master_pdf.exists() and proof_path.exists() and corrected_pdf.exists():
                proof = json.loads(proof_path.read_text())
                corrected_status = json.loads((REC / 'compile' / (corrected_name + '.json')).read_text())
                check(master_name + ': identical default source', master_path.read_bytes() == (OUT / lang / (corrected_name + '.tex')).read_bytes())
                check(master_name + ': identical compiled PDF', master_pdf.read_bytes() == corrected_pdf.read_bytes())
                check(master_name + ': current equivalence hashes', proof['source_sha256'] == digest(master_path) and proof['pdf_sha256'] == digest(master_pdf))
                pdf_results.append({'file': master_pdf.relative_to(OUT).as_posix(),
                                    'pages': corrected_status['pages'], 'bytes': master_pdf.stat().st_size,
                                    'sha256': digest(master_pdf),
                                    'identical_to': corrected_pdf.relative_to(OUT).as_posix(),
                                    'verification': proof_path.name})

    # These records describe genuine differences. Alternative readings without
    # a body difference live in the separate unresolved-note register.
    manifests = json.loads((REC / 'INPUT_VERIFICATION.json').read_text())
    known_source_members = {row['path_in_zip'] for archive in manifests for row in archive['files']}
    known_record_members = {p.relative_to(REC).as_posix() for p in REC.rglob('*') if p.is_file()}
    for lang in ['FR', 'EN']:
        entries = json.loads((REC / (lang + '_APPARATUS.json')).read_text())
        ids = [e['id'] for e in entries]
        check(lang + ': unique apparatus identifiers', len(ids) == len(set(ids)))
        check(lang + ': every entry has differing readings', all(e['before'] != e['after'] for e in entries))
        check(lang + ': every entry has a source', all(e.get('source') and e.get('source_ref') for e in entries))
        unresolved_members = []
        for entry in entries:
            for reference in entry['source_ref'].split(';'):
                member = reference.strip().split('#', 1)[0]
                if member not in known_source_members and member not in known_record_members:
                    unresolved_members.append({'id': entry['id'], 'reference': reference.strip()})
        check(lang + ': source references identify supplied members or delivered records', not unresolved_members, unresolved_members)

    privacy = []
    # Match actual environment locations, not mathematical expressions such as
    # i:\\Ext. The Windows expression requires an actual directory component.
    examined = 0
    paths = list(OUT.rglob('*')) + list((ROOT / 'work').glob('*.json'))
    for path in paths:
        if not path.is_file() or path.suffix not in {'.tex', '.md', '.json', '.tsv', '.log'}:
            continue
        if path.name == 'FINAL_AUDIT.json':
            continue
        examined += 1
        text = path.read_text(errors='replace')
        for kind, pattern in [('email', EMAIL), ('environment path', PRIVATE_PATH)]:
            match = pattern.search(text)
            if match:
                privacy.append({'file': path.relative_to(ROOT).as_posix(), 'kind': kind,
                                'offset': match.start()})
    check('Delivered text and frozen data contain no emails or environment paths', not privacy, {'files_examined': examined, 'exceptions': privacy})
    output = {'schema_version': 1, 'pdfs_required': args.require_pdfs,
              'checks': checks, 'checks_passed': len(checks) - len(errors),
              'checks_failed': len(errors), 'source_artifacts': source_results,
              'pdf_artifacts': pdf_results,
              'scope': 'Exact source-form identity, actual projected folios, standalone inputs, artifact hashes, compile/reference/glyph status, page geometry and privacy. Representative visual inspection is separately documented; no exhaustive scan comparison is claimed.'}
    (REC / 'FINAL_AUDIT.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'checks': len(checks), 'passed': len(checks) - len(errors), 'failures': errors}, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
