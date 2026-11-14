#!/usr/bin/env python3
"""Check every retained PDF and bind the result to exact PDF bytes."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

import fitz

from package_release import PRIVATE, plan

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inspect_pdf(archive, relative_path, data):
    doc = fitz.open(stream=data, filetype='pdf')
    row = {
        'archive': archive, 'path': relative_path, 'bytes': len(data),
        'sha256': sha(data), 'pages': len(doc), 'unreviewed_matches': [],
        'embedded_file_count': doc.embfile_count(),
    }

    def check(value, kind, page=None):
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
        for match in PRIVATE.finditer(text):
            context = text[max(0, match.start() - 70):min(len(text), match.end() + 70)]
            row['unreviewed_matches'].append({
                'location': kind, 'pdf_page': page,
                'matched_token_sha256': sha(match.group().encode()),
                'context_sha256': sha(context.encode()),
            })

    check(doc.metadata or {}, 'document_metadata')
    check(doc.get_xml_metadata() or '', 'xmp_metadata')
    check(doc.get_toc(simple=False), 'outline')
    for name in doc.embfile_names():
        check(name, 'embedded_file_name')
        check(doc.embfile_info(name), 'embedded_file_metadata')
    for number, page in enumerate(doc, 1):
        check(page.get_text(), 'page_text', number)
        for link in page.get_links():
            check(link, 'link', number)
        for annotation in page.annots() or []:
            check(annotation.info, 'annotation_info', number)
        for widget in page.widgets() or []:
            check({'name': widget.field_name, 'value': widget.field_value,
                   'label': widget.field_label}, 'widget', number)
    doc.close()
    row['passed'] = not row['unreviewed_matches'] and not row['embedded_file_count']
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', action='store_true', help='Read exact planned PDF payloads before ZIP creation.')
    args = parser.parse_args()
    rows = []
    planned = plan()[0] if args.plan else None
    for kind in ['FR', 'EN', 'RECORDS']:
        archive = 'SGA6_READERS_' + kind + '.zip'
        if planned is not None:
            for name, path in sorted(planned[kind].items()):
                if name.lower().endswith('.pdf'):
                    rows.append(inspect_pdf(archive, name, path.read_bytes()))
        else:
            with zipfile.ZipFile(ROOT.parent / archive) as z:
                for name in sorted(z.namelist()):
                    if name.lower().endswith('.pdf'):
                        rows.append(inspect_pdf(archive, name, z.read(name)))
    report = {
        'scope': 'Every retained PDF payload, bound to exact bytes and its final archive/member name: extractable page text, standard metadata, XMP, outlines, link dictionaries, annotation information, widget names/values/labels and embedded-file inventory. Embedded files would require a separate review and fail this gate.',
        'pdf_files': len(rows),
        'pdf_pages': sum(row['pages'] for row in rows),
        'unreviewed_match_count': sum(len(row['unreviewed_matches']) for row in rows),
        'files': rows,
        'passed': len(rows) == 20 and all(row['passed'] for row in rows),
    }
    target = ROOT / 'records/RELEASE_PDF_PRIVACY.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['pdf_files', 'pdf_pages', 'unreviewed_match_count', 'passed']}, indent=2))
    assert report['passed'], 'Retained PDF privacy review has unresolved items.'


if __name__ == '__main__':
    main()
