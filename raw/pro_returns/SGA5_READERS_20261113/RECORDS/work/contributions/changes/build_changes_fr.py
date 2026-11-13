#!/usr/bin/env python3
"""Write complete reversible French changes from the attached authoritative files.

No source text is edited. Before/after cells contain complete UTF-8 line hunks.
The original-byte ranges in `place` make every TSV comparison independently
replayable, including repeated text and zero-width insertions.
"""
from __future__ import annotations
import argparse
import bisect
import collections
import csv
import difflib
import hashlib
import importlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

csv.field_size_limit(sys.maxsize)

FIELDS = ['page', 'place', 'before', 'after', 'source']
MARKER = re.compile(r'%{5,}\s*scan idx\s+(\d+)\s*\|\s*folio\s+(\d+)\s*%+')
EMAIL = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
UNIX_PATH = re.compile(r'(?<![A-Za-z0-9_.])/(?:home|Users|workspace|root|tmp|mnt|var|opt|data|private|usr|etc)/[^\s"<>]+')
WINDOWS_PATH = re.compile(r'[A-Za-z]:[\\/](?:Users|Documents and Settings|Program Files|Windows|Temp|tmp|workspace|home)[\\/][^\s"<>]+', re.I)
PRIVACY_PATTERNS = [('email', EMAIL, '[email omitted]'),
                    ('local Unix path', UNIX_PATH, '[local source path omitted]'),
                    ('local Windows path', WINDOWS_PATH, '[local source path omitted]')]
RANGE = re.compile(r'old_bytes=(\d+):(\d+)')
IDENTIFIER = re.compile(r'\| id=([^ |]+)')


def sha(value):
    return hashlib.sha256(value.encode('utf-8') if isinstance(value, str) else value).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_tsv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def sanitize(text):
    """Only the three explicit privacy substitutions; no whitespace rewriting."""
    events = []
    value = text
    for kind, pattern, replacement in PRIVACY_PATTERNS:
        def replace(match):
            events.append({'kind': kind, 'line_1based_in_stage': value.count('\n', 0, match.start()) + 1,
                           'stage_character_range_0based': [match.start(), match.end()],
                           'removed_sha256': sha(match.group()), 'replacement': replacement})
            return replacement
        value = pattern.sub(replace, value)
    return value, events


def line_byte_offsets(lines):
    values = [0]
    for line in lines:
        values.append(values[-1] + len(line.encode('utf-8')))
    return values


def line_content_key(line):
    """Alignment key only: remove exactly one terminal CRLF, LF, or CR.

    Raw lines are never changed. Equal-key lines with different ending bytes
    are emitted as explicit line-ending change rows and replayed literally.
    """
    if line.endswith('\r\n'):
        return line[:-2]
    if line.endswith(('\n', '\r')):
        return line[:-1]
    return line


def complete_line_opcodes(before, after):
    opcodes = []
    alignment = difflib.SequenceMatcher(None, [line_content_key(x) for x in before],
                                       [line_content_key(x) for x in after], autojunk=False)
    for operation, i, j, k, l in alignment.get_opcodes():
        if operation != 'equal':
            opcodes.append((operation, i, j, k, l))
            continue
        start = 0
        while start < j - i:
            changed = before[i + start] != after[k + start]
            end = start + 1
            while end < j - i and (before[i + end] != after[k + end]) == changed:
                end += 1
            opcodes.append(('line-ending' if changed else 'equal', i + start, i + end, k + start, k + end))
            start = end
    return opcodes


def folios_per_line(lines):
    pages = []
    current = 0
    for line in lines:
        match = MARKER.search(line)
        if match:
            current = int(match.group(2))
        pages.append(current)
    return pages


def compact_pages(pages):
    pages = sorted(set(pages))
    parts = ['preamble'] if 0 in pages else []
    pages = [p for p in pages if p]
    i = 0
    while i < len(pages):
        end = i
        while end + 1 < len(pages) and pages[end + 1] == pages[end] + 1:
            end += 1
        parts.append(str(pages[i]) if end == i else f'{pages[i]}-{pages[end]}')
        i = end + 1
    return ','.join(parts) or 'preamble'


def begin_document_line(text):
    index = text.find(r'\begin{document}')
    return text.count('\n', 0, index) if index >= 0 else -1


def comment_position(line):
    for i, char in enumerate(line):
        if char == '%':
            j = i - 1
            while j >= 0 and line[j] == '\\':
                j -= 1
            if (i - 1 - j) % 2 == 0:
                return i
    return None


def categories(lines, start, document_start, body_only=False):
    result = set()
    for offset, line in enumerate(lines):
        stripped = line.strip()
        if not body_only and start + offset < document_start:
            result.add('preamble')
        elif MARKER.fullmatch(stripped):
            result.add('folio marker')
        elif not stripped:
            result.add('whitespace')
        elif stripped.startswith('%'):
            result.add('source comment')
        elif stripped in [r'\begin{document}', r'\end{document}']:
            result.add('document delimiter')
        elif re.match(r'\\(?:providecommand|newcommand|renewcommand|DeclareMathOperator|newenvironment|renewenvironment|def|let)\b', stripped):
            result.add('macro or environment definition')
        elif re.match(r'\\(?:clearpage|newpage|pagebreak|setlength|vspace|hspace|centering)\b', stripped) or stripped in [r'\begin{center}', r'\end{center}']:
            result.add('layout command')
        else:
            result.add('body text or formula')
        if comment_position(line) is not None and not MARKER.fullmatch(stripped):
            result.add('source comment')
    return sorted(result)


def load_records(fr):
    by_page = collections.defaultdict(list)
    verified = []
    with (fr / 'MANIFEST.tsv').open(encoding='utf-8', newline='') as f:
        manifest = {r['path_in_zip']: r for r in csv.DictReader(f, delimiter='\t')}
    for name in ['FIXLOG_5_CURRENT.jsonl', 'HANDFIX_5.jsonl', 'MISPRINTS_5.json', 'FIXLOG_5.jsonl']:
        relative = 'fixes/' + name
        data = (fr / relative).read_bytes()
        assert sha(data) == manifest[relative]['sha256']
        assert len(data) == int(manifest[relative]['bytes'])
        verified.append({'path_in_zip': relative, 'bytes': len(data), 'sha256': sha(data), 'manifest_match': True})
        records = [json.loads(line) for line in data.decode('utf-8').splitlines() if line.strip()] if name.endswith('.jsonl') else json.loads(data)
        for ordinal, record in enumerate(records, 1):
            if name == 'HANDFIX_5.jsonl' and 'current' not in record.get('file', ''):
                continue
            page = record.get('page')
            if not isinstance(page, int):
                continue
            before = record.get('old', record.get('print', ''))
            after = record.get('new', record.get('correct', ''))
            if not isinstance(before, str) or not isinstance(after, str) or before == after:
                continue
            # Short punctuation alone supplies insufficient historical context.
            # Such hunks retain their explicit authoritative-source decision.
            if not before or not after or max(len(before), len(after)) < 12:
                continue
            before, _ = sanitize(before)
            after, _ = sanitize(after)
            by_page[page].append({'id': f'{relative}#{ordinal}', 'before': before, 'after': after})
    return by_page, verified


def corroborating_records(index, pages, before, after):
    result = []
    for page in sorted({q + d for q in pages for d in [-1, 0, 1] if q}):
        for record in index.get(page, []):
            if record['before'] in before and record['after'] in after:
                result.append({'id': record['id'], 'evidence': 'entire recorded old and new strings occur literally in the corresponding full hunk sides'})
    return result


def replay_tsv(source_bytes, rows):
    """Apply a comparison's literal TSV rows at original-source byte offsets."""
    edits = []
    for row in rows:
        match = RANGE.search(row['place'])
        assert match, 'Missing original-byte range'
        start, end = map(int, match.groups())
        before, after = row['before'].encode('utf-8'), row['after'].encode('utf-8')
        assert source_bytes[start:end] == before, 'TSV before cell does not match its original byte range'
        edits.append((start, end, after))
    edits.sort(key=lambda e: (e[0], e[1]))
    assert all(left[1] <= right[0] for left, right in zip(edits, edits[1:])), 'Overlapping change rows'
    result = source_bytes
    for start, end, after in reversed(edits):
        result = result[:start] + after + result[end:]
    return result


def source_edits(audit_path, original, final):
    """Locate new build decisions exactly using the inheritance audit offsets."""
    with audit_path.open(encoding='utf-8', newline='') as f:
        edits = [r for r in csv.DictReader(f, delimiter='\t') if r['layer'] == 'current']
    edits.sort(key=lambda r: int(r['source_start_character_0based']))
    delta = 0
    result = []
    reconstructed = original
    for edit in reversed(edits):
        start = int(edit['source_start_character_0based'])
        end = int(edit['source_end_character_0based'])
        before, after = json.loads(edit['before_json']), json.loads(edit['after_json'])
        assert reconstructed[start:end] == before
        reconstructed = reconstructed[:start] + after + reconstructed[end:]
    assert reconstructed == final, 'Source-edit audit must be regenerated for the current prepared source'
    for edit in edits:
        start = int(edit['source_start_character_0based'])
        before, after = json.loads(edit['before_json']), json.loads(edit['after_json'])
        final_start = start + delta
        assert final[final_start:final_start + len(after)] == after
        ident = edit['decision_id']
        source = ('PLACES_98_DECIDED.tsv:' + ident) if ident.startswith('R98-') else 'OPEN_ITEMS_DECIDED.tsv:' + ('OPEN-H75' if ident == 'H75' else ident)
        result.append({'id': ident, 'source': source, 'page': int(edit['folio']),
                       'target_byte_range': [len(final[:final_start].encode('utf-8')), len(final[:final_start + len(after)].encode('utf-8'))]})
        delta += len(after) - len(before)
    return result


def write_patch(path, before, after, before_label, after_label):
    assert not before or before.endswith('\n'), 'Patch emitter requires a source final newline'
    assert not after or after.endswith('\n'), 'Patch emitter requires a target final newline'
    content = ''.join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                        fromfile=before_label, tofile=after_label, n=3, lineterm='\n'))
    path.write_text(content, encoding='utf-8')
    return sha(content)


def verify_patch(patch_path, before, after, temporary_root):
    executable = shutil.which('patch')
    assert executable, 'GNU patch is required for the independent patch replay check'
    with tempfile.TemporaryDirectory(prefix='patch-check-', dir=temporary_root) as temp:
        temp = Path(temp)
        original, result = temp / 'input.tex', temp / 'result.tex'
        original.write_bytes(before.encode('utf-8'))
        run = subprocess.run([executable, '--batch', '--silent', '--output', str(result), str(original), '-i', str(patch_path.resolve())],
                             capture_output=True, text=True)
        assert run.returncode == 0, 'Unified-patch replay failed'
        exact = result.read_bytes() == after.encode('utf-8')
        assert exact, 'Unified-patch replay differs from target'
        return {'method': 'GNU patch applied to an isolated copy', 'returncode': run.returncode, 'exact_target_bytes': exact}


def compare(label, prefix, before, after, before_label, after_label, index, build_edits, output, body_only=False, extra_sources=None):
    old_lines, new_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
    old_offsets, new_offsets = line_byte_offsets(old_lines), line_byte_offsets(new_lines)
    pages = folios_per_line(new_lines)
    old_document, new_document = begin_document_line(before), begin_document_line(after)
    rows, metadata, decisions = [], [], []
    ops = complete_line_opcodes(old_lines, new_lines)
    for operation, i, j, k, l in ops:
        if operation == 'equal':
            continue
        ordinal = len(rows) + 1
        ident = f'FRDIFF-{prefix}-{ordinal:05d}'
        old, new = ''.join(old_lines[i:j]), ''.join(new_lines[k:l])
        scope = pages[k:l] or [pages[min(k, len(pages) - 1)]]
        scope = sorted(set(scope))
        types = sorted(set(categories(old_lines[i:j], i, old_document, body_only) + categories(new_lines[k:l], k, new_document, body_only)))
        if operation == 'line-ending':
            assert [line_content_key(x) for x in old_lines[i:j]] == [line_content_key(x) for x in new_lines[k:l]]
            types.append('explicit line-ending conversion')
        linked = corroborating_records(index, scope, old, new) if not body_only and operation != 'line-ending' else []
        new_decisions = [edit['source'] for edit in build_edits
                         if operation != 'line-ending' and new_offsets[k] < edit['target_byte_range'][1]
                         and edit['target_byte_range'][0] < new_offsets[l]]
        reason = ('Retain the exact final corrected reading supplied by the authoritative current layer and the enumerated new build decisions. This row records every byte of this full-line difference; it introduces no further textual emendation.'
                  if not body_only else
                  'Record the complete literal change produced by the verified document-body preparation: source-comment processing, scoped macro expansion, protected one-token arguments, or explicit font-argument braces. Exact reconstruction and the named preparation function supply the reproducible mapping.')
        if operation == 'line-ending':
            reason = ('Record the exact line-ending bytes present in the authoritative final source. Removing exactly one terminal CRLF, LF, or CR from each paired line yields identical ordered content keys; the full before/after cells retain and replay every changed ending byte. No other character changes in this row.')
        sources = [f'FR_DIFF_DECISIONS.tsv:{ident}', before_label, after_label]
        if not body_only:
            sources += ['fr/sga5/current/s5.tex']
        sources += [r['id'] for r in linked] + new_decisions + (extra_sources or [])
        sources = list(dict.fromkeys(sources))
        place = (f'{label} | id={ident} | old_bytes={old_offsets[i]}:{old_offsets[j]}'
                 f' | new_bytes={new_offsets[k]}:{new_offsets[l]}'
                 f' | old_lines_0based={i}:{j} | new_lines_0based={k}:{l}'
                 f' | category={"; ".join(types)}')
        rows.append({'page': compact_pages(scope), 'place': place, 'before': old, 'after': new, 'source': '; '.join(sources)})
        metadata.append({'id': ident, 'operation': operation, 'pages': scope, 'categories': types,
                         'old_byte_range_0based_half_open': [old_offsets[i], old_offsets[j]],
                         'new_byte_range_0based_half_open': [new_offsets[k], new_offsets[l]],
                         'old_line_range_0based_half_open': [i, j], 'new_line_range_0based_half_open': [k, l],
                         'before_sha256': sha(old), 'after_sha256': sha(new),
                         'line_content_key_sequences_equal': operation == 'line-ending',
                         'corroborating_records': linked, 'new_build_decisions': new_decisions})
        decisions.append({'id': ident, 'comparison': label, 'page': compact_pages(scope), 'categories': '; '.join(types),
                          'decision': 'record the exact source-to-final difference', 'reason': reason,
                          'source_path': before_label, 'target_path': after_label,
                          'record_links': '; '.join(r['id'] for r in linked), 'new_build_decisions': '; '.join(new_decisions)})
    assert replay_tsv(before.encode('utf-8'), rows) == after.encode('utf-8')
    patch_path = output / 'patches' / f'{prefix}_to_corrected.patch'
    patch_hash = write_patch(patch_path, before, after, before_label, after_label)
    patch_verification = verify_patch(patch_path, before, after, output)
    report = {'comparison': label, 'source_path': before_label, 'target_path': after_label,
              'source_bytes': len(before.encode('utf-8')), 'target_bytes': len(after.encode('utf-8')),
              'source_sha256': sha(before), 'target_sha256': sha(after), 'rows': len(rows),
              'operation_counts': dict(collections.Counter(r['operation'] for r in metadata)),
              'category_row_counts': dict(collections.Counter(t for r in metadata for t in r['categories'])),
              'rows_with_literal_record_pair_support': sum(bool(r['corroborating_records']) for r in metadata),
              'patch_path': 'patches/' + patch_path.name, 'patch_sha256': patch_hash,
              'patch_verification': patch_verification, 'in_memory_tsv_reconstruction_exact': True,
              'hunks': metadata}
    return rows, decisions, report


def representation_proof(source, expected_body, scripts):
    """Evaluate the exact shipped preparation mapping and identify its version."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(scripts))
    preparation = importlib.import_module('prepare_french')
    preamble, body, log = preparation.expand_document(source, 'current')
    assert body == expected_body, 'Actual reader body does not equal the recorded preparation mapping'
    begin_token, end_token = r'\begin{document}', r'\end{document}'
    start = source.index(begin_token) + len(begin_token)
    end = source.rindex(end_token)
    raw_body = source[start:end]
    assert len(preamble) == start - len(begin_token)
    mapping = {
        'implementation': 'scripts/prepare_french.py:expand_document; scripts/sga5_common.py:split_document,strip_comments',
        'implementation_sha256': {name: sha((scripts / name).read_bytes()) for name in ['prepare_french.py', 'sga5_common.py']},
        'raw_body_extraction': {'start_character_0based_in_current_source': start, 'end_character_0based_in_current_source': end,
                                'start_byte_0based_in_current_source': len(source[:start].encode('utf-8')),
                                'end_byte_0based_in_current_source': len(source[:end].encode('utf-8')),
                                'delimiter_policy': 'Exact substring after the first begin-document token and before the last end-document token; no trimming.'},
        'raw_body_sha256': sha(raw_body), 'prepared_body_sha256': sha(expected_body),
        'mapping_reproduces_prepared_body_exactly': True,
        'macro_expansion_events': len(log), 'literal_macro_occurrences_expanded': sum(r.get('occurrences', 0) for r in log),
        'operations': [
            'Extract the document body by the exact delimiter slices recorded above.',
            'Retain full folio-marker comment lines. For every other unescaped percent sign, remove it and the rest of its physical line, including the line ending.',
            'Track scoped R and uRHom definitions and expand the listed zero-argument macros with their current source definitions.',
            'Protect a zero-argument macro passed as an unbraced token to an accent or font command by inserting braces before expanding it.',
            'Keep macro/environment definition lines apart from scoped definitions handled explicitly.',
            'Replace a font macro followed by whitespace and one alphanumeric argument token with the same macro and that token in braces.'
        ],
        'macros_expanded': sorted({r['macro'] for r in log}),
        'qualification': 'The exact literal mapping and all before/after hunks are established here. This report makes no additional visual comparison claim.'}
    return raw_body, mapping


def write_report(output, summary):
    lines = ['# Complete French change logs', '',
             'Every comparison is a complete sequence of full-line UTF-8 hunks. Applying the TSV rows at their recorded original byte ranges reproduces the target bytes exactly. The exported unified patches independently reproduce the same targets with GNU patch. No before/after cell is shortened.', '',
             '## Comparisons', '',
             '| Comparison | Complete change rows | Source SHA-256 | Target SHA-256 | TSV replay | Patch replay |',
             '|---|---:|---|---|---|---|']
    for comparison in summary['comparisons']:
        lines.append(f"| `{comparison['comparison']}` | {comparison['rows']:,} | `{comparison['source_sha256']}` | `{comparison['target_sha256']}` | exact | exact |")
    lines += ['', '`CHANGES_FR.tsv` contains the four source comparisons, with exactly the columns `page`, `place`, `before`, `after`, and `source`. The first text in `place` identifies `baseline:o`, `baseline:c5`, `baseline:c4`, or `current`. `CHANGES_FR_REPRESENTATION.tsv` contains the separate body-preparation comparison. Reader front matter, contents, apparatus wrappers, and final page-marker display are handled by the main reader build and are outside these source/body comparisons.', '',
              '## Scope and source attribution', '',
              'All source differences are included: body text and formulas, punctuation, source comments, folio-marker additions, macro/environment definitions, preamble, document delimiters, layout commands, and whitespace. A hunk can carry several categories because a changed full line can contain both text and a comment, or because a replacement crosses a structural boundary. These labels describe source structure; they do not assign mathematical significance.', '',
              'The August files contain mixed physical line endings, including 15,341 CRLF endings in `o`, 15,319 in `c5`, and 15,283 in `c4`; final current uses LF. For alignment only, each line is mapped to the string obtained by removing exactly one terminal CRLF, LF, or CR. The raw lines remain untouched. Paired equal-content lines with unequal ending bytes become separate, fully recorded `line-ending` rows, and all other non-equal alignment spans become complete source-change rows. This explicit mapping makes textual changes inspectable while retaining every line-ending change. No line ending is silently discarded.', '',
              'Folios come from the final French marker sequence. A deletion with an empty target span is assigned the final folio at that insertion position. A hunk spanning markers lists every touched folio. The August files contain no folio markers, so this target alignment is explicit. `preamble` identifies material before the first folio.', '',
              'Every row has its own stable diff decision in `FR_DIFF_DECISIONS.tsv`, the exact source and target artifact paths, and a reason to retain the authoritative final reading. Where an entire logged old string and new string are both literally present on the corresponding sides of a hunk, the related fix-log, hand-record, or misprint identifiers are added. These links are corroborating literal-pair evidence within a complete hunk; they are not represented as proof that one historical record accounts for every difference in that hunk. Rows without such a pair remain sourced by the exact authoritative files and their explicit diff decision. No historical attribution is fabricated.', '',
              'The individually located new build decisions are linked by exact target-byte overlap with the full hunk: 32 R98 decisions, OPEN-H75, SOL-EN-084, and GLOBAL-98b. The current comparison therefore accounts for all 35 changes from the supplied current layer, even when several edits lie on one changed line. `FR_CHANGELOG_RECONSTRUCTION.json` records the complete edit-location mapping and every hunk range/hash.', '',
              '## Exact privacy policy', '',
              'Before diffing, the script applies only three declared substitutions: email addresses become `[email omitted]`; absolute paths under the explicitly enumerated Unix directories become `[local source path omitted]`; Windows drive paths under the explicitly enumerated user/system directories receive the same path placeholder. The regular expressions and stage-by-stage event counts are stored in `FR_CHANGELOG_RECONSTRUCTION.json`, and the implementation is in `build_changes_fr.py`. No whitespace, line endings, TeX notation, prose, or punctuation is otherwise rewritten for the comparisons.', '',
              f"The actual inputs produced **{sum(len(v['events']) for v in summary['privacy']['inputs'])} privacy substitutions**. Their sanitized bytes therefore coincide with their original bytes. All final TSV, JSON, Markdown, and patch outputs were checked with the same privacy detectors. Only archive-relative source paths and relative build-artifact labels are written.", '',
              '## Body representation mapping', '',
              'The raw body is extracted as the exact substring after `\\begin{document}` and before `\\end{document}`, without trimming. Evaluating the shipped `prepare_french.expand_document` function on the final current source reproduces `prepared/FR_corrected_body.tex` byte for byte. The report pins the SHA-256 of that implementation and its shared helper. The separate representation log records every literal difference caused by the mapping, including source-comment removal and joining, scoped macro expansion, protection of one-token arguments, and explicit braces around font arguments. Its rules, source/body offsets, macro names, and event counts are supplied in `FR_REPRESENTATION_RULES.json`.', '',
              f"The preparation mapping records {summary['representation']['macro_expansion_events']:,} macro-expansion events covering {summary['representation']['literal_macro_occurrences_expanded']:,} literal macro occurrences. This changelog establishes the exact transformation and byte reconstruction. Visual equivalence is assessed by the main reader build; no new visual verification is claimed here.", '',
              '## Reproduction', '',
              'From the build workspace:', '', '```sh', 'python work/contributions/changes/build_changes_fr.py', '```', '',
              'The script accepts `--fr`, `--prepared`, `--source-edit-audit`, `--build-scripts`, and `--output`. It first verifies input manifests and the source-edit audit, then emits the logs, reloads the written TSVs, replays every comparison, and independently applies every unified patch. A failed identity, range check, or reconstruction stops the script.', '',
              'In the records layout, place `build_changes_fr.py`, `prepare_french.py`, and `sga5_common.py` in `scripts/`, keep the prepared layers under `prepared/` and the inheritance edit table under `audit/`, and extract the attached French ZIP under `sources/SGA5_FR`. All inputs are configurable relative paths:', '',
              '```sh', 'python scripts/build_changes_fr.py --fr sources/SGA5_FR --prepared prepared --source-edit-audit audit/SOURCE_TO_PREPARED_FR.tsv --build-scripts scripts --output changes', '```', '',
              'To replay one table directly, select rows whose `place` starts with the desired comparison label plus ` |`, encode their `before` and `after` cells as UTF-8, verify `before` at `old_bytes=start:end`, and replace the ranges in descending offset order. Byte ranges are zero-based and half-open. The script exposes this operation as `replay_tsv`. TSV quoting preserves embedded tabs, quotes, and newlines; read with a TSV/CSV parser, not by splitting physical lines.', '',
              'Files: `CHANGES_FR.tsv`, `CHANGES_FR_REPRESENTATION.tsv`, `FR_DIFF_DECISIONS.tsv`, `FR_CHANGELOG_RECONSTRUCTION.json`, `FR_REPRESENTATION_RULES.json`, `FR_CHANGELOG_REPORT.md`, the five files in `patches/`, and `build_changes_fr.py`.', '']
    (output / 'FR_CHANGELOG_REPORT.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fr', type=Path, default=Path('work/sources/SGA5_FR'))
    parser.add_argument('--prepared', type=Path, default=Path('work/build/prepared'))
    parser.add_argument('--source-edit-audit', type=Path, default=Path('work/contributions/audit/SOURCE_TO_PREPARED_FR.tsv'))
    parser.add_argument('--build-scripts', type=Path, default=Path('work/build/scripts'))
    parser.add_argument('--output', type=Path, default=Path('work/contributions/changes'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'patches').mkdir(exist_ok=True)
    with (args.fr / 'MANIFEST.tsv').open(encoding='utf-8', newline='') as f:
        manifest = {r['path_in_zip']: r for r in csv.DictReader(f, delimiter='\t')}
    source_inputs = [('baseline:o', 'BASELINE_O', 'fr_baseline_aug2026/sga5/o/s5.tex'),
                     ('baseline:c5', 'BASELINE_C5', 'fr_baseline_aug2026/sga5/c5/s5.tex'),
                     ('baseline:c4', 'BASELINE_C4', 'fr_baseline_aug2026/sga5/c4/s5.tex'),
                     ('current', 'CURRENT', 'fr/sga5/current/s5.tex')]
    sources, checks, privacy_inputs = {}, [], []
    for label, prefix, relative in source_inputs:
        raw = (args.fr / relative).read_bytes()
        assert sha(raw) == manifest[relative]['sha256'] and len(raw) == int(manifest[relative]['bytes'])
        sources[label], events = sanitize(raw.decode('utf-8'))
        checks.append({'path_in_zip': relative, 'bytes': len(raw), 'sha256': sha(raw), 'manifest_match': True,
                       'line_endings': {'CRLF': raw.count(b'\r\n'), 'LF_without_CR': raw.count(b'\n') - raw.count(b'\r\n'),
                                        'CR_without_LF': raw.count(b'\r') - raw.count(b'\r\n')}})
        privacy_inputs.append({'path': relative, 'original_sha256': sha(raw), 'sanitized_sha256': sha(sources[label]), 'events': events})
    target_raw = (args.prepared / 'FR_current_source.tex').read_bytes()
    body_raw = (args.prepared / 'FR_corrected_body.tex').read_bytes()
    target, target_events = sanitize(target_raw.decode('utf-8'))
    body, body_events = sanitize(body_raw.decode('utf-8'))
    privacy_inputs += [{'path': 'prepared/FR_current_source.tex', 'original_sha256': sha(target_raw), 'sanitized_sha256': sha(target), 'events': target_events},
                       {'path': 'prepared/FR_corrected_body.tex', 'original_sha256': sha(body_raw), 'sanitized_sha256': sha(body), 'events': body_events}]
    # The inspected inputs have no private substitutions, so the original audit
    # character offsets transfer exactly. A future sanitized input must carry
    # an explicit coordinate map before this source-decision step is reused.
    assert not any(v['events'] for v in privacy_inputs), 'Input sanitization changed coordinates; explicit coordinate transport is required'
    new_edits = source_edits(args.source_edit_audit, sources['current'], target)
    index, record_checks = load_records(args.fr)
    all_rows, all_decisions, comparisons = [], [], []
    inputs_by_label = {}
    for label, prefix, relative in source_inputs:
        rows, decisions, report = compare(label, prefix, sources[label], target, relative, 'prepared/FR_current_source.tex',
                                          index, new_edits, args.output)
        all_rows += rows
        all_decisions += decisions
        comparisons.append(report)
        inputs_by_label[label] = (sources[label], target)
    raw_body, representation = representation_proof(target, body, args.build_scripts)
    rep_rows, rep_decisions, rep_report = compare('representation:current-body', 'REPRESENTATION', raw_body, body,
        'prepared/FR_current_source.tex:document-body', 'prepared/FR_corrected_body.tex', {}, [], args.output, body_only=True,
        extra_sources=['scripts/prepare_french.py:expand_document', 'scripts/sga5_common.py:strip_comments', 'FR_REPRESENTATION_RULES.json'])
    all_decisions += rep_decisions
    comparisons.append(rep_report)
    inputs_by_label['representation:current-body'] = (raw_body, body)
    write_tsv(args.output / 'CHANGES_FR.tsv', all_rows, FIELDS)
    write_tsv(args.output / 'CHANGES_FR_REPRESENTATION.tsv', rep_rows, FIELDS)
    write_tsv(args.output / 'FR_DIFF_DECISIONS.tsv', all_decisions, list(all_decisions[0]))
    for filename, selected in [('CHANGES_FR.tsv', comparisons[:-1]), ('CHANGES_FR_REPRESENTATION.tsv', comparisons[-1:])]:
        with (args.output / filename).open(encoding='utf-8', newline='') as f:
            written_rows = list(csv.DictReader(f, delimiter='\t'))
        for comparison in selected:
            label = comparison['comparison']
            chosen = [r for r in written_rows if r['place'].startswith(label + ' |')]
            before, after = inputs_by_label[label]
            reconstructed = replay_tsv(before.encode('utf-8'), chosen)
            assert reconstructed == after.encode('utf-8')
            assert len(chosen) == comparison['rows']
            comparison['written_tsv_reconstruction_exact'] = True
            comparison['reconstructed_sha256'] = sha(reconstructed)
    current_report = next(c for c in comparisons if c['comparison'] == 'current')
    covered_decisions = {ref for hunk in current_report['hunks'] for ref in hunk['new_build_decisions']}
    expected_decisions = {edit['source'] for edit in new_edits}
    assert covered_decisions == expected_decisions, 'Current change hunks must cite every enumerated new decision'
    summary = {'source_manifest_verification': checks, 'record_manifest_verification': record_checks,
               'required_tsv_columns': FIELDS, 'changes_fr_rows': len(all_rows), 'representation_rows': len(rep_rows),
               'diff_decisions': len(all_decisions), 'new_build_decisions': new_edits,
               'new_build_decisions_covered_by_current_hunks': {'expected_count': len(expected_decisions),
                   'covered_count': len(covered_decisions), 'all_covered': True, 'uncovered': []},
               'privacy': {'policy': 'Apply only the exact regular expressions below, in the listed order; do not trim or rewrite any other byte.',
                           'patterns': [{'kind': name, 'regular_expression': pattern.pattern, 'replacement': replacement} for name, pattern, replacement in PRIVACY_PATTERNS],
                           'inputs': privacy_inputs},
              'comparison_unit': 'Complete original physical lines including their line endings. Alignment key removes exactly one terminal CRLF, LF, or CR; SequenceMatcher has autojunk disabled. Every non-equal alignment opcode is retained. Equal-key runs with unequal ending bytes are retained as explicit line-ending rows.',
               'coordinate_definition': 'All byte and line ranges are zero-based half-open ranges in the unmodified sanitized side identified by the comparison.',
               'representation': representation, 'comparisons': comparisons,
               'all_written_tsv_reconstructions_exact': all(c['written_tsv_reconstruction_exact'] for c in comparisons),
               'all_unified_patches_reconstruct_exactly': all(c['patch_verification']['exact_target_bytes'] for c in comparisons)}
    write_json(args.output / 'FR_REPRESENTATION_RULES.json', representation)
    write_json(args.output / 'FR_CHANGELOG_RECONSTRUCTION.json', summary)
    write_report(args.output, summary)
    files = [args.output / name for name in ['CHANGES_FR.tsv', 'CHANGES_FR_REPRESENTATION.tsv', 'FR_DIFF_DECISIONS.tsv',
             'FR_REPRESENTATION_RULES.json', 'FR_CHANGELOG_RECONSTRUCTION.json', 'FR_CHANGELOG_REPORT.md']]
    files += sorted((args.output / 'patches').glob('*.patch'))
    for path in files:
        text = path.read_text(encoding='utf-8')
        # The declared detector regexes are provenance, not private values.
        if path.name == 'FR_CHANGELOG_RECONSTRUCTION.json':
            value = json.loads(text)
            value['privacy']['patterns'] = []
            text = json.dumps(value, ensure_ascii=False)
        for kind, pattern, replacement in PRIVACY_PATTERNS:
            assert not pattern.search(text), 'Private value in generated ' + path.name + ': ' + kind
    print(json.dumps({'changes_fr_rows': len(all_rows), 'representation_rows': len(rep_rows),
                      'comparisons': {c['comparison']: c['rows'] for c in comparisons},
                      'all_written_tsv_reconstructions_exact': summary['all_written_tsv_reconstructions_exact'],
                      'all_unified_patches_reconstruct_exactly': summary['all_unified_patches_reconstruct_exactly'],
                      'privacy_substitutions': sum(len(v['events']) for v in privacy_inputs)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
