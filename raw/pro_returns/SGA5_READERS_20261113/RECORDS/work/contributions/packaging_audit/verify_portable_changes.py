#!/usr/bin/env python3
"""Recheck both independent change utilities in their documented portable layouts."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    base = Path.cwd()
    reports = []
    for language in ['FR', 'EN']:
        output = base / ('work/contributions/changes' if language == 'FR' else 'work/contributions/changes_en')
        names = ([
            'CHANGES_FR.tsv', 'CHANGES_FR_REPRESENTATION.tsv', 'FR_DIFF_DECISIONS.tsv',
            'FR_CHANGELOG_RECONSTRUCTION.json', 'FR_REPRESENTATION_RULES.json', 'FR_CHANGELOG_REPORT.md',
            *[f'patches/{part}_to_corrected.patch' for part in ['BASELINE_O', 'BASELINE_C5', 'BASELINE_C4', 'CURRENT', 'REPRESENTATION']],
        ] if language == 'FR' else [
            'CHANGES_EN.tsv', 'CHANGES_EN_REPRESENTATION.tsv', 'EN_DIFF_DECISIONS.tsv',
            'EN_COMMON_CHANGE_LINKS.tsv', 'EN_PORT_CHANGE_LINKS.tsv', 'EN_PROJECTION_CHANGE_LINKS.tsv',
            'EN_CHANGELOG_RECONSTRUCTION.json', 'EN_REPRESENTATION_RULES.json', 'EN_CHANGELOG_REPORT.md',
            'patches/RELEASE_to_corrected.patch', 'patches/REPRESENTATION_to_corrected.patch',
        ])
        scripts = (['work/contributions/changes/build_changes_fr.py', 'work/build/scripts/prepare_french.py',
                    'work/build/scripts/sga5_common.py'] if language == 'FR' else
                   ['work/contributions/changes_en/build_changes_en.py', 'work/contributions/changes/build_changes_fr.py'])
        with tempfile.TemporaryDirectory(prefix='portable-check-', dir=output) as tmp:
            root = Path(tmp)
            (root / 'scripts').mkdir()
            (root / 'sources').mkdir()
            for script in scripts:
                shutil.copy2(base / script, root / 'scripts' / Path(script).name)
            (root / 'sources' / ('SGA5_' + language)).symlink_to(base / 'work/sources' / ('SGA5_' + language), target_is_directory=True)
            (root / 'prepared').symlink_to(base / 'work/build/prepared', target_is_directory=True)
            if language == 'FR':
                (root / 'audit').symlink_to(base / 'work/contributions/audit', target_is_directory=True)
                command = ['python', 'scripts/build_changes_fr.py', '--fr', 'sources/SGA5_FR', '--prepared', 'prepared',
                           '--source-edit-audit', 'audit/SOURCE_TO_PREPARED_FR.tsv', '--build-scripts', 'scripts', '--output', 'changes']
                output_dir = 'changes'
                inputs = ['sources/SGA5_FR', 'prepared', 'audit']
            else:
                (root / 'english').symlink_to(base / 'work/contributions/english', target_is_directory=True)
                command = ['python', 'scripts/build_changes_en.py']
                output_dir = 'changes_en'
                inputs = ['sources/SGA5_EN', 'english', 'prepared']
            result = subprocess.run([sys.executable, *command[1:]], cwd=root, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(language + ' portable change utility failed')
            compared = []
            for name in names:
                original = (output / name).read_bytes()
                rebuilt = (root / output_dir / name).read_bytes()
                compared.append({'path': name, 'sha256': sha(original), 'rebuilt_sha256': sha(rebuilt),
                                 'byte_identical': original == rebuilt})
            report = {'command': command, 'working_directory': 'records root', 'scripts': scripts,
                      'script_sha256': {s: sha((base / s).read_bytes()) for s in scripts},
                      'input_directories': inputs, 'output_directory': output_dir,
                      'exit_code': result.returncode, 'all_11_artifacts_byte_identical': all(r['byte_identical'] for r in compared),
                      'artifacts': compared}
            (output / f'{language}_PORTABLE_REPRODUCTION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
            assert report['all_11_artifacts_byte_identical'], language + ' portable artifacts differ'
            reports.append({'language': language, 'artifacts': len(compared), 'all_byte_identical': True})
    print(json.dumps(reports, indent=2))


if __name__ == '__main__':
    main()
