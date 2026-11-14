#!/usr/bin/env python3
"""Read-only review of release selection and exact English packet dependencies."""
from pathlib import Path
from collections import Counter
import csv, hashlib, importlib.util, io, json, re, zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def put(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    source = ROOT / 'scripts/package_release.py'
    spec = importlib.util.spec_from_file_location('release_selection_under_review', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # plan() reads the tree. main(), which writes release records/archives,
    # is deliberately never called by this audit.
    archives, omitted = module.plan()
    selected = {rel:p for files in archives.values() for rel,p in files.items()}
    catalog_path = ROOT / 'review/english/aggregate/INPUT_CATALOG.json'
    catalog = json.loads(catalog_path.read_text())
    packets = []
    dependencies = {}
    for packet in catalog['packets']:
        directory = ROOT / packet['directory']
        manifest_path = ROOT / packet['manifest']['path']
        assert digest(manifest_path.read_bytes()) == packet['manifest']['sha256']
        if manifest_path.suffix == '.tsv':
            entries = list(csv.DictReader(manifest_path.open(), delimiter='\t'))
        else:
            entries = json.loads(manifest_path.read_text())
            entries = entries if isinstance(entries, list) else entries['files']
        rows = []
        for entry in entries:
            file = directory / entry['path']
            data = file.read_bytes()
            assert digest(data) == entry['sha256'], file.relative_to(ROOT).as_posix()
            rows.append((file, data, 'sealed packet manifest member'))
        rows.append((manifest_path, manifest_path.read_bytes(), 'original immutable packet manifest'))
        additions = []
        extension_counts = Counter()
        extension_bytes = Counter()
        for file, data, role in rows:
            rel = file.relative_to(ROOT).as_posix()
            extension_counts[file.suffix] += 1
            extension_bytes[file.suffix] += len(data)
            selected_path = selected.get(rel)
            included = bool(selected_path and digest(selected_path.read_bytes()) == digest(data))
            record = dict(path=rel, bytes=len(data), sha256=digest(data), role=role,
                          included_by_current_plan=included, packet=packet['label'])
            dependencies[rel] = record
            if not included:
                additions.append(record)
        packets.append(dict(label=packet['label'], directory=packet['directory'],
                            manifest=packet['manifest'], required_files=len(rows),
                            required_bytes=sum(len(data) for _,data,_ in rows),
                            missing_files=len(additions), missing_bytes=sum(r['bytes'] for r in additions),
                            extension_counts=dict(extension_counts), extension_bytes=dict(extension_bytes)))
    missing = [row for row in dependencies.values() if not row['included_by_current_plan']]
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for row in sorted(missing, key=lambda r:r['path']):
            archive.writestr(row['path'], (ROOT / row['path']).read_bytes())
    compressed = len(stream.getvalue())
    # Required captured terminology inputs have independent hash manifests.
    glossary_inputs = []
    for name in ['INPUT_MANIFEST.json','SUPPLEMENTAL_INPUT_MANIFEST.json','FINAL_MACRO_INPUT_MANIFEST.json']:
        path = ROOT / 'review/english/terminology_final' / name
        if not path.exists():
            continue
        rows = json.loads(path.read_text())
        rows = rows['files'] if isinstance(rows, dict) else rows
        for row in rows:
            rel = row['snapshot']
            file = ROOT / rel
            data = file.read_bytes()
            assert digest(data) == row['sha256']
            if rel not in selected:
                glossary_inputs.append(dict(path=rel,bytes=len(data),sha256=digest(data),
                                            required_by='review/english/terminology_final/'+name))
    glossary_inputs = list({r['path']:r for r in glossary_inputs}.values())
    # Do not reproduce private values in the review record. Record only the
    # portable file path, line and category when a value trips the release gate.
    privacy = []
    for relative, path in selected.items():
        if path.suffix == '.pdf':
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            privacy.append(dict(path=relative,category='non-UTF8 text selected by UTF8-only packaging gate'))
            continue
        match = module.PRIVATE.search(text)
        if match:
            privacy.append(dict(path=relative,line=text.count('\n',0,match.start())+1,
                                category='selected textual content matches the release private-metadata expression'))
    report = dict(record_type='independent_release_packaging_review',
                  reviewed_script='scripts/package_release.py', reviewed_script_sha256=digest(source.read_bytes()),
                  English_catalog='review/english/aggregate/INPUT_CATALOG.json', catalog_sha256=digest(catalog_path.read_bytes()),
                  selected_archive_file_counts={k:len(v) for k,v in archives.items()},
                  packets=packets, missing_immutable_packet_files=len(missing),
                  missing_immutable_packet_bytes=sum(r['bytes'] for r in missing),
                  missing_packet_zip_deflate9_bytes=compressed,
                  missing_captured_terminology_inputs=glossary_inputs,
                  release_private_metadata_gate_findings=privacy,
                  source_files_changed=False, release_archives_written=False,
                  exact_failure='collect_english_aggregate.verify_packet requires each listed original manifest member and verifies its SHA256. An absent packet manifest or member prevents exact sealed-span reconstruction. build_english_aggregate.apply_layout silently skips absent packet rendering_repairs.jsonl files, so building from the retained aggregate raw source alone can also omit recorded layout repairs.',
                  derivative_policy='The original manifests include PNG/PDF/log derivatives in packets VII and XIII. Omitting these members requires an explicit separately recorded transport of the verifier and an exact omission list, preserving the immutable original manifest and its digest; copying only text members does not satisfy the current verifier.',
                  counts_scope='ZIP size is an exact in-memory ZIP_DEFLATED level9 archive of the missing immutable packet files alone, not an estimate of the combined final RECORDS archive.')
    put('REQUIRED_ENGLISH_PACKET_FILES.json', list(dependencies.values()))
    put('MISSING_ENGLISH_PACKET_FILES.json', missing)
    put('PACKAGE_RELEASE_REVIEW.json', report)
    print(json.dumps({k:report[k] for k in ['missing_immutable_packet_files','missing_immutable_packet_bytes',
                                          'missing_packet_zip_deflate9_bytes','release_private_metadata_gate_findings']},ensure_ascii=False))
    print(json.dumps(dict(missing_captured_terminology_input_files=len(glossary_inputs),
                          missing_captured_terminology_input_bytes=sum(r['bytes'] for r in glossary_inputs))))


if __name__ == '__main__':
    main()
