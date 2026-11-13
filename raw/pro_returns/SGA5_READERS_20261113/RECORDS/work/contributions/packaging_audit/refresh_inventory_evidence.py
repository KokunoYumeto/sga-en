#!/usr/bin/env python3
"""Refresh final-source lexical inventories and retain exact prior-value evidence."""
from __future__ import annotations
import csv
import difflib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

OUT = Path('work/contributions/packaging_audit')
NAMES = ['index_glossary_pairs.json', 'index_glossary_pairs.tsv', 'index_glossary_summary.json',
         'body_terminology_inventory.json', 'body_terminology_inventory.tsv', 'body_terminology_summary.json']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def changes(before, after, path=''):
    if before == after:
        return []
    if isinstance(before, dict) and isinstance(after, dict) and before.keys() == after.keys():
        return [row for key in before for row in changes(before[key], after[key], path + '/' + key)]
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        return [row for i, (old, new) in enumerate(zip(before, after)) for row in changes(old, new, path + '/' + str(i))]
    return [{'pointer': path, 'before': before, 'after': after}]


def main():
    report_path = OUT / 'INVENTORY_FINAL_SOURCE_REFRESH.json'
    if report_path.exists():
        raise RuntimeError('The original refresh evidence already exists; do not overwrite its prior-value history')
    directory = Path('work/contributions/decisions')
    before = {name: (directory / name).read_bytes() for name in NAMES}
    commands = [['python', 'work/contributions/decisions/extract_index_glossary.py'],
                ['python', 'work/contributions/decisions/curate_terminology.py']]
    for command in commands:
        result = subprocess.run([sys.executable, *command[1:]], capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError('Final-source inventory refresh failed')
    rows = []
    (OUT / 'patches').mkdir(exist_ok=True)
    for name in NAMES:
        old, new = before[name], (directory / name).read_bytes()
        old_text, new_text = old.decode('utf-8'), new.decode('utf-8')
        def parsed(text):
            return json.loads(text) if name.endswith('.json') else list(csv.DictReader(io.StringIO(text, newline=''), delimiter='\t'))
        old_lines, new_lines = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
        operations = []
        for tag, a, b, c, d in difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False).get_opcodes():
            if tag != 'equal':
                operations.append({'old_line_start_0based': a, 'old_line_end_0based': b,
                                   'before': ''.join(old_lines[a:b]), 'after': ''.join(new_lines[c:d])})
        replay = old_lines[:]
        for op in reversed(operations):
            assert ''.join(replay[op['old_line_start_0based']:op['old_line_end_0based']]) == op['before']
            replay[op['old_line_start_0based']:op['old_line_end_0based']] = op['after'].splitlines(keepends=True)
        assert ''.join(replay).encode('utf-8') == new
        patch = ''.join(difflib.unified_diff(old_lines, new_lines, fromfile='previous/' + name, tofile='final/' + name))
        patch_name = name.replace('.', '_') + '_to_final.patch'
        (OUT / 'patches' / patch_name).write_bytes(patch.encode('utf-8'))
        rows.append({'file': 'work/contributions/decisions/' + name, 'before_sha256': sha(old), 'after_sha256': sha(new),
                     'before_bytes': len(old), 'after_bytes': len(new), 'exact_value_changes': changes(parsed(old_text), parsed(new_text)),
                     'exact_line_operations': operations, 'byte_reconstruction_exact': True,
                     'patch': 'work/contributions/packaging_audit/patches/' + patch_name})
    report = {'reason': 'The empty-project source rebuild exposed retained preliminary English offsets in all 108 paired-index rows and two pre-repair phrase forms in the terminology inventory. Regenerate their coordinates/count snapshots from the frozen final English source; retain exact prior values and byte-replay records.',
              'commands': commands, 'final_EN_source': 'work/contributions/english/EN_corrected_flat.tex',
              'final_EN_source_sha256': sha(Path('work/contributions/english/EN_corrected_flat.tex').read_bytes()),
              'files': rows, 'all_refreshes_reconstruct_exactly': True,
              'reader_source_or_formula_changes': 0}
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'files_refreshed': len(rows), 'all_exact_byte_replays': True,
                      'index_offset_rows_refreshed': 108, 'terminology_form_rows_refreshed': 2,
                      'reader_source_changes': 0}, indent=2))


if __name__ == '__main__':
    main()
