#!/usr/bin/env python3
"""Inventory publishable record inputs and required final deliverables."""
from __future__ import annotations
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

from verify_source_rebuild import READERS

OUT = Path('work/contributions/packaging_audit')
SELF_REPORTS = {'FINAL_RECORD_INVENTORY.tsv', 'FINAL_RECORD_INVENTORY.json'}
ROOT_RECORDS = [
    'README.md', 'SOURCE_IDENTIFIERS.md', 'APPARATUS_COUNTS.md', 'BUILD_SUMMARY.json',
    'PLACES_98_DECIDED.tsv', 'OPEN_ITEMS_DECIDED.tsv', 'GLOSSARY_SGA5_FR_EN.tsv',
    'GLOSSARY_INCONSISTENCIES.md', 'CHANGES_FR.tsv', 'CHANGES_EN.tsv',
    'READER_ASSEMBLY_DECISIONS.tsv', 'COMPLETE_READER_CHANGELOG_RECONSTRUCTION.json',
    'COMPLETE_READER_CHANGELOG_REPORT.md', 'FR_SOURCE_WITNESSES.json', 'EN_variants_input.json',
    'rebuild.py', 'REBUILD.md',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    spec = importlib.util.spec_from_file_location('package_policy', 'work/build/scripts/package_deliverables.py')
    policy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(policy)
    rows, excluded = [], []

    def include(source, package, member, role, required=False):
        present = source.is_file()
        data = source.read_bytes() if present else None
        rows.append({'package': package, 'member': member, 'source': source.as_posix(), 'role': role,
                     'required': required, 'present': present, 'bytes': len(data) if present else '',
                     'sha256': sha(data) if present else ''})

    for lang, names in READERS.items():
        for name in names:
            for suffix in ['.tex', '.pdf']:
                include(Path('deliverables') / lang / (name + suffix), 'SGA5_READERS_' + lang + '.zip',
                        name + suffix, 'standalone reader or annotated master', True)
            for suffix in ['.json', '.log']:
                include(Path('deliverables/records/build_outputs') / (name + suffix), 'SGA5_READERS_RECORDS.zip',
                        'build_outputs/' + name + suffix, 'screened complete compiler evidence', True)
        for name in ['README.md', 'APPARATUS_COUNTS.md', 'BUILD_SUMMARY.json']:
            include(Path('deliverables') / lang / name, 'SGA5_READERS_' + lang + '.zip', name, 'language package documentation', True)

    for name in ROOT_RECORDS:
        source = Path('deliverables/records') / name
        if name in policy.ROOT_COPIES:
            source = Path('work/contributions') / policy.ROOT_COPIES[name]
        elif name == 'EN_variants_input.json':
            source = Path('work/build/prepared/EN_variants_input.json')
        elif name == 'REBUILD.md':
            source = OUT / name
        include(source, 'SGA5_READERS_RECORDS.zip', name, 'required root table, report, citation alias or rebuild entry point', True)

    for base in [Path('work/build/scripts'), Path('work/build/prepared'), Path('work/contributions')]:
        for path in sorted(base.rglob('*')):
            if not path.is_file():
                continue
            if path.name in SELF_REPORTS and path.parent == OUT:
                continue
            if any(part in policy.EXCLUDED for part in path.relative_to(base).parts) or path.suffix not in policy.EXTENSIONS:
                excluded.append({'path': path.as_posix(), 'reason': 'packaging exclusion policy'})
                continue
            if any(part.startswith('portable-check-') for part in path.parts):
                raise RuntimeError('Wait for compact-layout verification to finish before inventorying')
            role = ('implementation' if path.suffix == '.py' else
                    'scan evidence' if 'scans' in path.parts and path.suffix == '.png' else
                    'independent exact replay patch' if path.suffix == '.patch' else
                    'screened TeX token proof' if path.name == 'folio248_token_boundary_probe.log' else
                    'prepared source or variant catalogue' if 'prepared' in path.parts else
                    'decision, audit or reconstruction evidence')
            include(path, 'SGA5_READERS_RECORDS.zip', path.as_posix(), role)
    prompt = Path('upload/PROMPT(20261112-230204).md')
    include(prompt, 'SGA5_READERS_RECORDS.zip', prompt.as_posix(), 'attached instruction evidence for exact credits audit', True)
    fields = ['package', 'member', 'source', 'role', 'required', 'present', 'bytes', 'sha256']
    with (OUT / 'FINAL_RECORD_INVENTORY.tsv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    report = {
        'inventory_rows': len(rows), 'required_artifacts': sum(r['required'] for r in rows),
        'missing_required_artifacts': [r['source'] for r in rows if r['required'] and not r['present']],
        'present_bytes_counting_root_alias_copies': sum(r['bytes'] for r in rows if r['present']),
        'implementation_scripts': sum(r['role'] == 'implementation' for r in rows),
        'independent_patches': sum(r['role'] == 'independent exact replay patch' for r in rows),
        'screened_token_proof_retained': any(r['role'] == 'screened TeX token proof' and r['present'] for r in rows),
        'excluded_execution_artifacts': excluded,
        'original_input_policy': 'The three original source ZIPs and work/sources are external inputs; their private source_path manifest fields are not republished.',
        'runtime_policy': 'No machine-local environment, installed TeX tree, package downloads, font cache or raw compiler directory is copied. A complete standard TeX installation or equivalent active local environment is required.',
        'layout_policy': 'The records package retains work/build/scripts, work/build/prepared and work/contributions exactly; root aliases and SOURCE_IDENTIFIERS.md route short source citations.',
        'manifest_policy': 'package_deliverables.py generates each final MANIFEST.tsv from the staged bytes and rechecks every archived member. This inventory describes inputs before packaging; package manifests are authoritative for the final ZIP snapshots.',
        'self_reference_policy': 'These two inventory outputs are excluded from their own hash inventory and covered by the final package manifest.',
    }
    (OUT / 'FINAL_RECORD_INVENTORY.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['excluded_execution_artifacts']}, indent=2))
    assert not report['missing_required_artifacts'], 'Required delivery artifacts are absent'


if __name__ == '__main__':
    main()
