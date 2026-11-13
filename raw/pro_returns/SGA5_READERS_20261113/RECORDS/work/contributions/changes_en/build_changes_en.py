#!/usr/bin/env python3
"""Complete, reversible English release and reader-body change logs.

Keep this script beside build_changes_fr.py in the records/scripts directory.
The latter supplies shared UTF-8, TSV, exact-range, and patch utilities only.
Inputs and output are explicit relative CLI paths; sources are never modified.
"""
from __future__ import annotations
import argparse
import bisect
import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
try:
    import build_changes_fr as common
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).parent.parent / 'changes'))
    import build_changes_fr as common

csv.field_size_limit(sys.maxsize)
RELEASE = 'en/release_source/sources/native/SGA5/SGA5_English_sync_workpass.tex'
PORTED = 'en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex'
CORRECTED = 'english/EN_corrected_flat.tex'
BODY = 'prepared/EN_corrected_body.tex'
FOLIO = re.compile(r'%{5,}[ \t]*scan idx[ \t]+(\d+)[ \t]*\|[ \t]*folio[ \t]+(\d+)[ \t]*%+[ \t]*')


def sha(value):
    return common.sha(value)


def safe(value):
    return common.sanitize(str(value))[0]


def char_offsets(lines):
    result = [0]
    for line in lines:
        result.append(result[-1] + len(line))
    return result


def apply_traced(text, start, end, replacement, reference, events, add_event=True):
    """Transport previous operation intervals through an exact replacement.

    An intersected interval becomes the smallest interval containing the
    retained interval parts and the later replacement. This is an explicitly
    recorded provenance envelope, not a claim that its whole string was
    written by the earlier operation alone.
    """
    difference = len(replacement) - (end - start)
    for event in events:
        a, b = event['start'], event['end']
        if b <= start:
            continue
        if a >= end:
            event['start'] += difference
            event['end'] += difference
            continue
        event['start'] = min(a, start)
        event['end'] = max(start + len(replacement), b + difference if b > end else start + len(replacement))
        event['later_operations'].append(reference)
    if add_event:
        events.append({'reference': reference, 'start': start, 'end': start + len(replacement), 'later_operations': []})
    return text[:start] + replacement + text[end:]


def reconstruct_corrected(ported_raw, target, operations, hom_rows, variants):
    # This exact mapping is the universal-newline read used by the source
    # builder. The release comparison separately retains every ending byte.
    text = ported_raw.replace('\r\n', '\n').replace('\r', '\n')
    starting_hash = sha(text)
    hom = {row['id']: row for row in hom_rows}
    events, checked_operations, references = [], [], {}
    for number, record in enumerate(operations, 1):
        reference = f'english/EN_common_corrections.json#{number}'
        references[reference] = {'kind': 'common correction', 'record_number_1based': number,
                                 'id': record['id'], 'source': safe(record.get('source', '')),
                                 'reason': safe(record.get('reason', ''))}
        old, new = record['old'], record['new']
        if record['id'] == 'EN-III-URHOM-SCOPE':
            a, b = text.index('Exposé III ---'), text.index('Exposé V ---')
            locations = [(a + m.start(), a + m.end()) for m in re.finditer(r'\\uRHom(?![A-Za-z])', text[a:b])]
        elif record['id'].startswith('EN-III-HOM-'):
            row = hom[record['id']]
            locations = [(row['start'], row['end'])]
        else:
            assert old
            locations = [(m.start(), m.end()) for m in re.finditer(re.escape(old), text)]
        assert len(locations) == record['applied_count'], ('Recorded occurrence count differs', reference)
        for start, end in reversed(locations):
            assert text[start:end] == old, ('Recorded source text differs', reference)
            text = apply_traced(text, start, end, new, reference, events)
        checked_operations.append({'reference': reference, 'id': record['id'], 'recorded_occurrences': record['applied_count'],
                                   'verified_occurrences': len(locations), 'result_sha256': sha(text)})
    before_variants_hash = sha(text)
    changed_variants = []
    numbered = list(enumerate(variants, 1))
    for number, variant in reversed(sorted(numbered, key=lambda pair: (pair[1]['start'], pair[1]['end']))):
        start, end = variant['start'], variant['end']
        old, new = variant.get('original', variant['after']), variant['after']
        assert text[start:end] == old, ('Variant original differs', variant['id'])
        reference = f'english/EN_variants.json#{number}'
        references[reference] = {'kind': 'French/scan projection', 'record_number_1based': number,
                                 'id': variant['id'], 'source': safe(variant.get('source', '')),
                                 'reason': safe(variant.get('reason', 'The exact corrected reading follows the identified French or scan projection.'))}
        if old != new:
            text = apply_traced(text, start, end, new, reference, events)
            changed_variants.append(reference)
    assert text == target, 'Complete common-operation and variant replay does not reconstruct corrected English'
    for number, variant in enumerate(variants, 1):
        assert target[variant['start_corrected']:variant['end_corrected']] == variant['after'], variant['id']
    proof = {'ported_initial_newline_mapping': 'Replace every CRLF pair with LF, then every remaining CR with LF; no other character changes at this stage.',
             'ported_original_sha256': sha(ported_raw), 'ported_after_newline_mapping_sha256': starting_hash,
             'common_operation_count': len(operations), 'verified_common_occurrences': sum(r['verified_occurrences'] for r in checked_operations),
             'all_recorded_common_counts_match': True, 'common_operations': checked_operations,
             'after_common_operations_sha256': before_variants_hash, 'input_variants': len(variants),
             'variants_changing_corrected_text': len(changed_variants), 'changed_variant_references': changed_variants,
             'final_sha256': sha(text), 'exact_corrected_reconstruction': True,
             'interval_transport_definition': 'Intervals before an edit stay fixed; intervals after it shift by replacement length minus removed length; intersecting intervals become the smallest interval containing retained interval parts and the replacement. Later-operation IDs are recorded for every intersection.'}
    return proof, events, references


def validated_anchors(alignment, target):
    result = []
    for number, row in enumerate(alignment, 1):
        position = row['position_corrected']
        assert 0 <= position < len(target)
        result.append({'reference': f'english/EN_ALIGNMENT.json#{number}', 'folio': int(row['folio']),
                       'position': position, 'kind': row['kind'], 'confidence': safe(row.get('confidence', '')),
                       'record_source': safe(row.get('source', ''))})
    assert all(a['position'] <= b['position'] for a, b in zip(result, result[1:]))
    assert all(a['folio'] <= b['folio'] for a, b in zip(result, result[1:]))
    assert len(result) == 793
    return result


def anchor_bounds(anchors, start, end):
    positions = [a['position'] for a in anchors]
    left_index = bisect.bisect_right(positions, start) - 1
    right_index = bisect.bisect_left(positions, end)
    left = anchors[left_index] if left_index >= 0 else None
    right = anchors[right_index] if right_index < len(anchors) else None
    # Empty insertions at a validated anchor have that exact point as both bounds.
    if start == end and left and left['position'] == start:
        right = left
    if left is None and right is not None and end <= anchors[0]['position']:
        label = 'preamble / original front matter'
    elif left is None:
        label = f'front matter to {right["folio"]} (validated anchor bounds)'
    elif right is None:
        label = f'{left["folio"]} onward (last validated anchor)'
    elif left['folio'] == right['folio']:
        label = f'{left["folio"]} (bounded by validated anchors)'
    else:
        label = f'{left["folio"]}-{right["folio"]} (validated anchor bounds)'
    proof = {'left': left, 'right': right,
             'policy': 'Surrounding validated anchors only; no interpolated exact folio for intervening text.'}
    return label, proof


def overlaps(event, start, end):
    a, b = event['start'], event['end']
    if a == b:
        return start <= a <= end
    return start < b and a < end


def body_mapping(target, alignment, prepared_body):
    events = [(r['position_corrected'], f'%\n%%%%%%%%%%  scan idx {int(r["folio"]) + 11}  |  folio {int(r["folio"])}  %%%%%%%%%%\n') for r in alignment]
    pieces, last = [], 0
    for position, marker in sorted(events, key=lambda item: item[0]):
        assert position >= last
        pieces.extend([target[last:position], marker])
        last = position
    pieces.append(target[last:])
    marked = ''.join(pieces)
    preamble, document_body = marked.split(r'\begin{document}', 1)
    document_body, tail = document_body.rsplit(r'\end{document}', 1)
    first = FOLIO.search(document_body)
    assert first and int(first.group(2)) == 1
    unprocessed = document_body[first.start():]
    lines = []
    comments_removed = 0
    for line in unprocessed.splitlines(keepends=True):
        if FOLIO.fullmatch(line.rstrip('\n')):
            lines.append(line)
            continue
        index = 0
        while index < len(line):
            if line[index] == '\\':
                index += 2
                continue
            if line[index] == '%':
                line = line[:index]
                comments_removed += 1
                break
            index += 1
        lines.append(line)
    generated = ''.join(lines)
    assert generated == prepared_body, '793-anchor injection and comment mapping differ from prepared English body'
    first_position = min(r['position_corrected'] for r in alignment)
    end_position = target.rfind(r'\end{document}')
    raw_body = target[first_position:end_position]
    matches = list(FOLIO.finditer(prepared_body))
    assert len(matches) == len(alignment) == 793
    assert [int(m.group(2)) for m in matches] == [int(r['folio']) for r in alignment]
    anchors = [{'reference': f'english/EN_ALIGNMENT.json#{number}', 'folio': int(row['folio']),
                'position': match.start(), 'kind': row['kind'], 'confidence': safe(row.get('confidence', '')),
                'record_source': safe(row.get('source', ''))}
               for number, (row, match) in enumerate(zip(alignment, matches), 1)]
    rules = {'implementation': 'scripts/build_changes_en.py:body_mapping',
             'source_mapping_correspondence': 'scripts/prepare_english_master.py:inject/main; scripts/sga5_common.py:split_document,strip_comments',
             'raw_body_slice': {'start_character_0based': first_position, 'end_character_0based': end_position,
                                'start_byte_0based': len(target[:first_position].encode('utf-8')),
                                'end_byte_0based': len(target[:end_position].encode('utf-8')),
                                'start_basis': 'first verified Exposé I anchor in EN_ALIGNMENT.json',
                                'end_basis': 'start of final end-document token; no trimming'},
             'raw_body_sha256': sha(raw_body), 'prepared_body_sha256': sha(prepared_body),
             'injected_validated_anchor_count': len(alignment), 'distinct_folios': len({r['folio'] for r in alignment}),
             'retained_marker_count': len(matches), 'processed_nonmarker_comments': comments_removed,
             'complete_marker_sequence_matches_alignment': True, 'exact_prepared_body_reconstruction': True,
             'operations': ['At every recorded corrected character position insert percent + newline, the exact scan/folio marker, and newline.',
                            'Select the document body and then the first retained folio-1 marker through the body end.',
                            'Retain exact marker lines; for each other unescaped percent, remove the percent and the rest of its physical line including the ending.',
                            'Concatenate the retained characters without trimming or other rewriting.'],
             'qualification': 'This proves the exact source-to-body mapping. Page ranges in the change table use validated anchor bounds, and no additional visual equivalence is claimed.'}
    return raw_body, anchors, rules


def compare(label, prefix, before, after, before_label, after_label, anchors, provenance_events, references, output, body=False):
    old_lines, new_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
    old_bytes, new_bytes = common.line_byte_offsets(old_lines), common.line_byte_offsets(new_lines)
    old_chars, new_chars = char_offsets(old_lines), char_offsets(new_lines)
    rows, decisions, metadata = [], [], []
    source_links = collections.defaultdict(list)
    for operation, i, j, k, l in common.complete_line_opcodes(old_lines, new_lines):
        if operation == 'equal':
            continue
        ident = f'ENDIFF-{prefix}-{len(rows) + 1:05d}'
        old, new = ''.join(old_lines[i:j]), ''.join(new_lines[k:l])
        page, bound = anchor_bounds(anchors, new_chars[k], new_chars[l])
        types = sorted(set(common.categories(old_lines[i:j], i, common.begin_document_line(before), body)
                           + common.categories(new_lines[k:l], k, common.begin_document_line(after), body)))
        if operation == 'line-ending':
            types.append('explicit line-ending conversion')
            assert [common.line_content_key(x) for x in old_lines[i:j]] == [common.line_content_key(x) for x in new_lines[k:l]]
        attached = [e for e in provenance_events if operation != 'line-ending' and overlaps(e, new_chars[k], new_chars[l])]
        attached_refs = list(dict.fromkeys(e['reference'] for e in attached))
        sources = [f'EN_DIFF_DECISIONS.tsv:{ident}', before_label, after_label]
        sources += attached_refs
        for reference in attached_refs:
            record = references[reference]
            if record.get('id'):
                sources.append(record['id'])
                if record['id'].startswith(('SOL-', 'GLOBAL-', 'OPEN-')):
                    sources.append('OPEN_ITEMS_DECIDED.tsv:' + record['id'])
                if record['id'].startswith('R98-'):
                    sources.append('PLACES_98_DECIDED.tsv:' + record['id'])
            if record.get('source'):
                sources.append(record['source'])
            source_links[reference].append(ident)
        if body:
            sources += ['EN_REPRESENTATION_RULES.json', 'english/EN_ALIGNMENT.json', 'scripts/prepare_english_master.py']
        else:
            sources += [PORTED, 'english/EN_PORT_AUDIT.json', 'english/EN_common_corrections.json']
        sources = list(dict.fromkeys(safe(s) for s in sources if s))
        reason = ('Record the exact final corrected English obtained from the authenticated ported source by the verified common operations and source projections. This hunk introduces no additional editorial reconstruction.'
                  if not body else 'Record every literal change of the independently replayed 793-anchor insertion and source-comment mapping; preserve the exact raw and prepared body strings.')
        if operation == 'line-ending':
            reason = 'Record the exact CRLF/LF ending change. The ordered line-content keys agree after removing exactly one terminal CRLF, LF, or CR from each paired line; every original ending byte remains in the before/after cells.'
        place = (f'{label} | id={ident} | old_bytes={old_bytes[i]}:{old_bytes[j]} | new_bytes={new_bytes[k]}:{new_bytes[l]}'
                 f' | old_lines_0based={i}:{j} | new_lines_0based={k}:{l} | category={"; ".join(types)}'
                 ' | folio_basis=validated anchor bounds; no interpolation')
        rows.append({'page': page, 'place': place, 'before': old, 'after': new, 'source': '; '.join(sources)})
        metadata.append({'id': ident, 'operation': operation, 'page_label': page, 'categories': types,
                         'old_byte_range_0based_half_open': [old_bytes[i], old_bytes[j]],
                         'new_byte_range_0based_half_open': [new_bytes[k], new_bytes[l]],
                         'new_character_range_0based_half_open': [new_chars[k], new_chars[l]],
                         'before_sha256': sha(old), 'after_sha256': sha(new), 'folio_bounds': bound,
                         'source_references': attached_refs,
                         'source_link_basis': 'Validated corrected port interval or exactly transported correction/projection interval overlaps this complete final hunk; this does not assign every hunk byte to one record.'})
        decisions.append({'id': ident, 'comparison': label, 'page': page, 'categories': '; '.join(types),
                          'decision': 'retain the exact documented final English source or body representation', 'reason': reason,
                          'source_path': before_label, 'target_path': after_label, 'linked_records': '; '.join(attached_refs)})
    assert common.replay_tsv(before.encode('utf-8'), rows) == after.encode('utf-8')
    patch = output / 'patches' / f'{prefix}_to_corrected.patch'
    patch_hash = common.write_patch(patch, before, after, before_label, after_label)
    patch_check = common.verify_patch(patch, before, after, output)
    proof = {'comparison': label, 'source_path': before_label, 'target_path': after_label,
             'source_bytes': len(before.encode('utf-8')), 'target_bytes': len(after.encode('utf-8')),
             'source_sha256': sha(before), 'target_sha256': sha(after), 'rows': len(rows),
             'operation_counts': dict(collections.Counter(r['operation'] for r in metadata)),
             'category_row_counts': dict(collections.Counter(t for r in metadata for t in r['categories'])),
             'rows_with_located_record_links': sum(bool(r['source_references']) for r in metadata),
             'patch_path': 'patches/' + patch.name, 'patch_sha256': patch_hash, 'patch_verification': patch_check,
             'hunks': metadata}
    return rows, decisions, proof, source_links


def add_port_intervals(port_log, port_audit, ported_lf, target, events, references):
    assert len(port_log) == len(port_audit) == 1856
    verified = 0
    for number, (record, audit) in enumerate(zip(port_log, port_audit), 1):
        assert audit['row'] == number and audit['id'] == record['id']
        reference = f'port/PORT_EN5_LOG.jsonl#{number}'
        references[reference] = {'kind': 'port record', 'record_number_1based': number, 'id': record['id'],
                                 'source': f'english/EN_PORT_AUDIT.json#{number}',
                                 'reason': safe(audit['evidence'])}
        start = audit.get('corrected_offset')
        if isinstance(start, int):
            text = audit['corrected_reading']
            assert target[start:start + len(text)] == text, ('Port corrected interval mismatch', reference)
            base_start = audit['base_offset']
            base_reading = audit['effective_base_reading']
            assert ported_lf[base_start:base_start + len(base_reading)] == base_reading
            events.append({'reference': reference, 'start': start, 'end': start + len(text), 'later_operations': [],
                           'interval_source': f'english/EN_PORT_AUDIT.json#{number}'})
            verified += 1
    return {'port_records': len(port_log), 'audit_row_identity_matches': True,
            'exact_final_and_ported_intervals_rechecked': verified,
            'other_statuses': 'Not-applicable and explicitly covered records retain the supplied port audit decisions; no terminal interval is invented for them.'}


def write_report(output, report):
    rows = report['comparisons']
    text = ['# Complete English change logs', '',
            'The release comparison retains every byte difference between the authenticated released English source and the frozen corrected English. The second comparison retains every difference between the exact raw body beginning at the first verified Exposé I anchor and the prepared reader body. Both written TSVs and both unified patches reconstruct their target bytes exactly.', '',
            '| Comparison | Rows | Source SHA-256 | Target SHA-256 |', '|---|---:|---|---|']
    for row in rows:
        text.append(f"| `{row['comparison']}` | {row['rows']:,} | `{row['source_sha256']}` | `{row['target_sha256']}` |")
    text += ['', '## Complete differences and line endings', '',
             '`CHANGES_EN.tsv` and `CHANGES_EN_REPRESENTATION.tsv` have exactly `page`, `place`, `before`, `after`, and `source`. Before/after fields contain complete original line hunks, with all tabs, quotes, and line endings preserved. The `place` field supplies zero-based, half-open original byte ranges, so repeated strings and empty insertions replay unambiguously.', '',
             'The released file has 15,829 CRLF line endings; the corrected file uses LF. Alignment alone uses the explicit key obtained by removing exactly one terminal CRLF, LF, or CR from a physical line. Every unequal ending is still retained in a `line-ending` row; every other non-equal line span is also retained. No ending, source comment, preamble change, formula, or textual correction is silently discarded.', '',
             'To read or append these TSVs, use a CSV/TSV parser with `newline=\'\'`. Default universal-newline reading would alter the CRLF bytes inside quoted cells. No cells are truncated.', '',
             '## Source proof and attribution', '',
             f"The script verifies both attached English source files and the port log against their manifest. Starting with the ported source, it applies the explicitly recorded CRLF-to-LF input mapping, then replays all **{report['corrected_construction']['common_operation_count']} common correction operations** at their recorded counts (**{report['corrected_construction']['verified_common_occurrences']} occurrences**). Scoped internal-Hom replacements use their recorded source scope or original occurrence positions. It then applies the **{report['corrected_construction']['variants_changing_corrected_text']} corrected-text changes** from the variant catalogue. The result equals the frozen corrected English byte for byte.", '',
             f"For port provenance, all **1,856** original one-based row numbers and their source IDs are retained. The script additionally rechecks both ends of **{report['port_interval_validation']['exact_final_and_ported_intervals_rechecked']}** port-to-final intervals supplied by the port audit: the quoted source reading matches the ported source at its offset, and its terminal reading matches final English at its offset. Records with other audit dispositions keep those dispositions; no interval is fabricated.", '',
             'Every change row has its own reasoned decision in `EN_DIFF_DECISIONS.tsv` and exact source/target paths. Located port intervals and traced common/projection intervals add the relevant one-based record references, open-item IDs, French-source references, and scan decisions. Intersecting later edits are retained in an explicitly defined provenance interval envelope. A linked record supplies located evidence within the full hunk; it is not represented as accounting for every hunk byte by itself.', '',
             '`EN_COMMON_CHANGE_LINKS.tsv` has one row for each of the 398 common operations. `EN_PORT_CHANGE_LINKS.tsv` has one row for each of the 1,856 port records. `EN_PROJECTION_CHANGE_LINKS.tsv` has one row per input variant. A correction can have no non-line-ending release hunk when the released source already has its resulting reading; such an empty link list is retained without inventing a new release change. The exact source reconstruction proves the operation was applied to the ported source.', '',
             '## Folio attribution', '',
             'The 793 entries of `english/EN_ALIGNMENT.json` are the sole basis for folio labels. Their positions and folios are ordered, and their exact source hashes are recorded. Each change hunk is labelled by the nearest validated anchors that bound its final span. Equal bounding folios are labelled as bounded by validated anchors; differing folios are shown as a range. Material before the first anchor is labelled preamble/original front matter; material after the last is labelled from the last validated anchor onward. No interpolated exact folio is assigned to intervening English text.', '',
             'The representation table uses the same anchors after their exact transport to the inserted marker positions. The reconstruction JSON records both bounding anchor IDs and positions for every hunk, so the basis of each label is inspectable.', '',
             '## Body representation and scope', '',
             f"The independently replayed body mapping inserts all **793** validated marker events, retains their exact ordered folio sequence (**{report['representation']['distinct_folios']} distinct folios**), extracts from the first verified Exposé I anchor through the final body end, and processes source comments with the recorded percent/line-ending rule. It reproduces `prepared/EN_corrected_body.tex` exactly. `EN_REPRESENTATION_RULES.json` gives the full mapping and offsets. No additional visual-equivalence claim is made here.", '',
             'New reader front matter, the generated contents, apparatus wrappers, and final marker display are handled by the main reader build. This source/body log does not pretend to include those later wrapper operations.', '',
             '## Privacy and reproduction', '',
             'The shared script applies exactly the declared email and absolute-machine-path substitutions before comparison. These inputs required zero substitutions, so their sanitized bytes equal their original bytes. The detector patterns and event lists are recorded; generated outputs contain archive-relative source paths and relative build-artifact labels.', '',
             'Place `build_changes_en.py` beside `build_changes_fr.py` in `scripts/`. From the records root, with the attached English ZIP extracted under `sources/SGA5_EN` and the recorded intermediate artifacts under `english/` and `prepared/`, run:', '',
             '```sh', 'python scripts/build_changes_en.py --en sources/SGA5_EN --english english --prepared prepared --output changes_en', '```', '',
             'All four paths are configurable relative paths. The workspace command is:', '',
             '```sh', 'python work/contributions/changes_en/build_changes_en.py --en work/sources/SGA5_EN --english work/contributions/english --prepared work/build/prepared --output work/contributions/changes_en', '```', '',
             'The script reloads written TSVs, applies every row at its original byte range, and independently applies both exported patches with GNU patch. Identity, count, interval, or reconstruction failures stop the build.', '']
    (output / 'EN_CHANGELOG_REPORT.md').write_text('\n'.join(text), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--en', type=Path, default=Path('sources/SGA5_EN'))
    parser.add_argument('--english', type=Path, default=Path('english'))
    parser.add_argument('--prepared', type=Path, default=Path('prepared'))
    parser.add_argument('--output', type=Path, default=Path('changes_en'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'patches').mkdir(exist_ok=True)
    with (args.en / 'MANIFEST.tsv').open(encoding='utf-8', newline='') as f:
        manifest = {r['path_in_zip']: r for r in csv.DictReader(f, delimiter='\t')}
    verified, source_text = [], {}
    for relative in [RELEASE, PORTED, 'port/PORT_EN5_LOG.jsonl']:
        data = (args.en / relative).read_bytes()
        assert sha(data) == manifest[relative]['sha256'] and len(data) == int(manifest[relative]['bytes'])
        verified.append({'path_in_zip': relative, 'bytes': len(data), 'sha256': sha(data), 'manifest_match': True,
                         'CRLF_count': data.count(b'\r\n'), 'LF_without_CR_count': data.count(b'\n') - data.count(b'\r\n')})
        source_text[relative] = data.decode('utf-8')
    data_files = ['EN_ALIGNMENT.json', 'EN_common_corrections.json', 'EN_INTERNAL_HOM_AUDIT.json', 'EN_variants.json', 'EN_PORT_AUDIT.json']
    data, artifact_hashes = {}, []
    for name in data_files:
        raw = (args.english / name).read_bytes()
        data[name] = json.loads(raw)
        artifact_hashes.append({'path': 'english/' + name, 'bytes': len(raw), 'sha256': sha(raw)})
    target_raw = (args.english / 'EN_corrected_flat.tex').read_bytes()
    body_raw = (args.prepared / 'EN_corrected_body.tex').read_bytes()
    target, body = target_raw.decode('utf-8'), body_raw.decode('utf-8')
    privacy = []
    for path, value in [(RELEASE, source_text[RELEASE]), (PORTED, source_text[PORTED]), (CORRECTED, target), (BODY, body)]:
        clean, events = common.sanitize(value)
        privacy.append({'path': path, 'original_sha256': sha(value), 'sanitized_sha256': sha(clean), 'events': events})
        assert not events, 'Privacy substitution changed positions; explicit coordinate transport is required'
    operations, variants, alignment = data['EN_common_corrections.json'], data['EN_variants.json'], data['EN_ALIGNMENT.json']
    assert len(operations) == 398
    construction, events, references = reconstruct_corrected(source_text[PORTED], target, operations, data['EN_INTERNAL_HOM_AUDIT.json'], variants)
    port_log = [json.loads(line) for line in source_text['port/PORT_EN5_LOG.jsonl'].splitlines() if line.strip()]
    port_validation = add_port_intervals(port_log, data['EN_PORT_AUDIT.json'], source_text[PORTED].replace('\r\n', '\n').replace('\r', '\n'), target, events, references)
    anchors = validated_anchors(alignment, target)
    rows, decisions, proof, links = compare('release', 'RELEASE', source_text[RELEASE], target, RELEASE, CORRECTED,
                                            anchors, events, references, args.output)
    raw_body, body_anchors, representation = body_mapping(target, alignment, body)
    rep_rows, rep_decisions, rep_proof, _ = compare('representation:corrected-body', 'REPRESENTATION', raw_body, body,
        CORRECTED + ':first-Exposé-I-anchor-to-body-end', BODY, body_anchors, [], {}, args.output, body=True)
    common.write_tsv(args.output / 'CHANGES_EN.tsv', rows, common.FIELDS)
    common.write_tsv(args.output / 'CHANGES_EN_REPRESENTATION.tsv', rep_rows, common.FIELDS)
    common.write_tsv(args.output / 'EN_DIFF_DECISIONS.tsv', decisions + rep_decisions, list(decisions[0]))
    for name, source, result, comparison in [('CHANGES_EN.tsv', source_text[RELEASE], target, proof),
                                            ('CHANGES_EN_REPRESENTATION.tsv', raw_body, body, rep_proof)]:
        with (args.output / name).open(encoding='utf-8', newline='') as f:
            written = list(csv.DictReader(f, delimiter='\t'))
        replayed = common.replay_tsv(source.encode('utf-8'), written)
        assert replayed == result.encode('utf-8') and len(written) == comparison['rows']
        comparison['written_tsv_reconstruction_exact'] = True
        comparison['reconstructed_sha256'] = sha(replayed)
    common_links = []
    for number, record in enumerate(operations, 1):
        reference = f'english/EN_common_corrections.json#{number}'
        located = [event for event in events if event['reference'] == reference]
        common_links.append({'record': reference, 'record_number_1based': number, 'id': record['id'],
                             'recorded_applied_count': record['applied_count'], 'verified_applied_count': record['applied_count'],
                             'corrected_intervals_json': json.dumps([{'start': e['start'], 'end': e['end'], 'later_operations': e['later_operations']} for e in located]),
                             'change_hunks': '; '.join(links.get(reference, [])),
                             'link_status': 'located release difference' if links.get(reference) else 'no non-line-ending release hunk at the transported final interval',
                             'source': safe(record.get('source', '')), 'reason': safe(record.get('reason', ''))})
    common.write_tsv(args.output / 'EN_COMMON_CHANGE_LINKS.tsv', common_links, list(common_links[0]))
    port_links = []
    for number, (record, audit) in enumerate(zip(port_log, data['EN_PORT_AUDIT.json']), 1):
        reference = f'port/PORT_EN5_LOG.jsonl#{number}'
        port_links.append({'record': reference, 'record_number_1based': number, 'id': record['id'],
                           'recorded_page': record['page'], 'port_decision': record['decision'],
                           'port_audit_status': safe(audit['audit_status']),
                           'interval_rechecked': isinstance(audit.get('corrected_offset'), int),
                           'change_hunks': '; '.join(links.get(reference, [])), 'evidence_source': f'english/EN_PORT_AUDIT.json#{number}'})
    common.write_tsv(args.output / 'EN_PORT_CHANGE_LINKS.tsv', port_links, list(port_links[0]))
    projection_links = []
    for number, variant in enumerate(variants, 1):
        reference = f'english/EN_variants.json#{number}'
        projection_links.append({'record': reference, 'record_number_1based': number, 'id': variant['id'],
                                 'recorded_page': variant['page'], 'changes_corrected_source': variant.get('original', variant['after']) != variant['after'],
                                 'corrected_start_character': variant['start_corrected'], 'corrected_end_character': variant['end_corrected'],
                                 'change_hunks': '; '.join(links.get(reference, [])), 'source': safe(variant.get('source', ''))})
    common.write_tsv(args.output / 'EN_PROJECTION_CHANGE_LINKS.tsv', projection_links, list(projection_links[0]))
    report = {'source_manifest_verification': verified, 'generated_input_identities': artifact_hashes,
              'required_tsv_columns': common.FIELDS, 'changes_en_rows': len(rows), 'representation_rows': len(rep_rows),
              'corrected_construction': construction, 'port_interval_validation': port_validation,
              'source_links': {'common_operation_rows': len(common_links), 'common_operations_linked_to_release_hunks': sum(bool(r['change_hunks']) for r in common_links),
                               'port_rows': len(port_links), 'port_records_linked_to_release_hunks': sum(bool(r['change_hunks']) for r in port_links),
                               'projection_rows': len(projection_links), 'corrected_projection_rows_linked': sum(bool(r['change_hunks']) for r in projection_links)},
              'privacy': {'policy': 'Only the three explicit substitutions in the shared script; no other input rewriting before comparison.',
                          'patterns': [{'kind': kind, 'regular_expression': pattern.pattern, 'replacement': replacement} for kind, pattern, replacement in common.PRIVACY_PATTERNS],
                          'inputs': privacy},
              'alignment': {'records': len(anchors), 'distinct_folios': len({r['folio'] for r in anchors}),
                            'ordered_positions': True, 'ordered_folios': True,
                            'policy': 'Bound every hunk with neighbouring validated anchors; label ranges or last-anchor extent. Never infer an interpolated exact folio.'},
              'representation': representation, 'comparisons': [proof, rep_proof],
              'all_written_tsv_reconstructions_exact': True, 'all_unified_patches_reconstruct_exactly': True,
              'all_corrected_source_operations_replayed_exactly': True}
    common.write_json(args.output / 'EN_CHANGELOG_RECONSTRUCTION.json', report)
    common.write_json(args.output / 'EN_REPRESENTATION_RULES.json', representation)
    write_report(args.output, report)
    for path in list(args.output.glob('*.tsv')) + list(args.output.glob('*.json')) + list(args.output.glob('*.md')) + list((args.output / 'patches').glob('*.patch')):
        text = path.read_text(encoding='utf-8')
        if path.name == 'EN_CHANGELOG_RECONSTRUCTION.json':
            value = json.loads(text)
            value['privacy']['patterns'] = []
            text = json.dumps(value, ensure_ascii=False)
        for kind, pattern, _ in common.PRIVACY_PATTERNS:
            assert not pattern.search(text), 'Private value in ' + path.name + ': ' + kind
    print(json.dumps({'changes_en_rows': len(rows), 'representation_rows': len(rep_rows),
                      'operations': [p['operation_counts'] for p in [proof, rep_proof]],
                      'corrected_sha256': sha(target), 'body_sha256': sha(body),
                      'source_links': report['source_links'], 'all_reconstructions_exact': True}, indent=2))


if __name__ == '__main__':
    main()
