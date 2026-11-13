#!/usr/bin/env python3
"""Independent EN master audit; no imports from the preparation/build code.

Read-only inputs; all audit outputs are written next to this script. Offsets are
Unicode character offsets, zero-based, end-exclusive. Generated folio comments
have no origin in the flat source; every retained source character does.
"""
from __future__ import annotations

import bisect
import argparse
import collections
import difflib
import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
EN = WORK / 'contributions' / 'english'
BUILD = WORK / 'build' / 'prepared'
CONTROL = re.compile(r'\\(?:[A-Za-z@]+|.)', re.S)
CALL = re.compile(r'\\SGAvar(?![A-Za-z@])')
FOLIO = re.compile(r'%{5,}[ \t]*scan idx[ \t]+(\d+)[ \t]*\|[ \t]*folio[ \t]+(\d+)[ \t]*%+[ \t]*\n?')


def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def write_json(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def skip_space_and_comments(s, i):
    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s[i] == '%':
            j = s.find('\n', i)
            i = len(s) if j < 0 else j + 1
        else:
            return i
    return i


def group(s, i):
    assert s[i] == '{', (i, s[max(0, i - 20):i + 60])
    begin = i + 1
    level = 1
    i += 1
    while i < len(s):
        ch = s[i]
        if ch == '\\':
            m = CONTROL.match(s, i)
            assert m
            i = m.end()
            continue
        if ch == '%':
            j = s.find('\n', i)
            i = len(s) if j < 0 else j + 1
            continue
        if ch == '{':
            level += 1
        elif ch == '}':
            level -= 1
            if level == 0:
                return s[begin:i], i + 1
        i += 1
    raise AssertionError(('unclosed group', begin))


def calls_and_branches(s):
    calls = []
    last = 0
    pieces = {'corrected': [], 'diplomatic': []}
    lengths = {'corrected': 0, 'diplomatic': 0}
    for m in CALL.finditer(s):
        assert m.start() >= last, ('nested variant', m.start())
        i = m.end()
        args = []
        for _ in range(3):
            i = skip_space_and_comments(s, i)
            a, i = group(s, i)
            args.append(a)
        rec = {'id': args[2], 'master_start': m.start(), 'master_end': i,
               'before': args[0], 'after': args[1]}
        for branch, arg in [('diplomatic', args[0]), ('corrected', args[1])]:
            common = s[last:m.start()]
            pieces[branch].extend([common, arg])
            lengths[branch] += len(common)
            rec[branch + '_span'] = [lengths[branch], lengths[branch] + len(arg)]
            lengths[branch] += len(arg)
        calls.append(rec)
        last = i
    for branch in pieces:
        pieces[branch].append(s[last:])
    return calls, {b: ''.join(x) for b, x in pieces.items()}


def strip_comments_with_origins(s, origins):
    """Discard TeX comments and endlines; preserve generated folio data lines.

    The escape rule is implemented as a token scanner independently of the
    builder's line-index procedure. Control symbols including \\% are retained.
    """
    pieces = []
    kept = []
    removed_source = []
    removed_generated = 0
    ordinary_comments = 0
    original_comment_lines = 0
    generated_separator_comments = 0
    cursor = 0
    for line in s.splitlines(keepends=True):
        end = cursor + len(line)
        if FOLIO.fullmatch(line):
            pieces.append(line)
            kept.extend(origins[cursor:end])
            cursor = end
            continue
        i = cursor
        cutoff = end
        while i < end:
            if s[i] == '\\':
                m = CONTROL.match(s, i)
                assert m
                i = m.end()
            elif s[i] == '%':
                cutoff = i
                ordinary_comments += 1
                break
            else:
                i += 1
        pieces.append(s[cursor:cutoff])
        kept.extend(origins[cursor:cutoff])
        if cutoff < end:
            if any(x is not None for x in origins[cutoff:end]):
                original_comment_lines += 1
            else:
                generated_separator_comments += 1
        for origin in origins[cutoff:end]:
            if origin is None:
                removed_generated += 1
            else:
                removed_source.append(origin)
        cursor = end
    return ''.join(pieces), kept, {
        'ordinary_comments_removed': ordinary_comments,
        'original_source_comment_lines_removed': original_comment_lines,
        'generated_separator_comment_lines_removed': generated_separator_comments,
        'source_comment_characters_removed': len(removed_source),
        'generated_comment_separator_characters_removed': removed_generated,
        'removed_source_comment_characters_sha256': None,
        '_removed_source_positions': removed_source,
    }


def expected_body(flat, branch, alignment):
    first = min(r['position_' + branch] for r in alignment)
    end = flat.rfind(r'\end{document}')
    begin_doc = flat.index(r'\begin{document}')
    author_start = first
    assert begin_doc < first < end
    ordered = sorted(alignment, key=lambda r: r['position_' + branch])
    pieces = []
    origins = []
    last = first
    for r in ordered:
        pos = r['position_' + branch]
        assert first <= pos <= end and pos >= last
        pieces.append(flat[last:pos])
        origins.extend(range(last, pos))
        p = int(r['folio'])
        marker = f'%\n%%%%%%%%%%  scan idx {p + 11}  |  folio {p}  %%%%%%%%%%\n'
        pieces.append(marker)
        origins.extend([None] * len(marker))
        last = pos
    pieces.append(flat[last:end])
    origins.extend(range(last, end))
    marked = ''.join(pieces)
    first_marker = FOLIO.search(marked)
    assert first_marker and first_marker.group(2) == '1'
    removed_initial_generated = first_marker.start()
    assert all(x is None for x in origins[:removed_initial_generated])
    marked = marked[removed_initial_generated:]
    origins = origins[removed_initial_generated:]
    text, kept, meta = strip_comments_with_origins(marked, origins)
    removed = meta.pop('_removed_source_positions')
    meta['removed_source_comment_characters_sha256'] = sha(''.join(flat[i] for i in removed))
    source_positions = [i for i in kept if i is not None]
    body_positions = [i for i, x in enumerate(kept) if x is not None]
    assert source_positions == sorted(source_positions)
    assert len(source_positions) == len(set(source_positions))
    retained = ''.join(text[i] for i in body_positions)
    assert retained == ''.join(flat[i] for i in source_positions)
    assert len(source_positions) + len(removed) == end - first
    meta.update({
        'first_author_body_offset': author_start,
        'end_author_body_offset': end,
        'author_body_characters_before_comments': end - first,
        'author_body_sha256_before_comments': sha(flat[first:end]),
        'preamble_sha256': sha(flat[:begin_doc]),
        'removed_editorial_front_characters': first - begin_doc - len(r'\begin{document}'),
        'removed_editorial_front_sha256': sha(flat[begin_doc + len(r'\begin{document}'):first]),
        'retained_author_source_characters': len(source_positions),
        'retained_author_source_sha256': sha(retained),
        'inserted_marker_characters': sum(x is None for x in kept),
        'body_character_count': len(text),
        'body_sha256': sha(text),
        'initial_generated_separator_removed': removed_initial_generated,
        'all_author_body_characters_accounted_for': True,
    })
    return text, source_positions, body_positions, meta


def source_interval_to_body(start, end, source_positions, body_positions):
    left = bisect.bisect_left(source_positions, start)
    right = bisect.bisect_left(source_positions, end)
    if left == right:
        return None
    return [body_positions[left], body_positions[right - 1] + 1]


def source_edit_span_to_body(start, end, source_positions, body_positions, body_length):
    if start != end:
        result = source_interval_to_body(start, end, source_positions, body_positions)
        assert result is not None, ('source variant wholly inside removed comments', start, end)
        return result
    point = bisect.bisect_left(source_positions, start)
    out = body_positions[point] if point < len(body_positions) else body_length
    return [out, out]


def closed_intersects(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


def edit_components(original_rows, calls, projected):
    """Compare two exact edit paths, joining touching edit rectangles.

    The before and after text of each resulting rectangle is checked directly.
    Component edges permit repeated equal tokens to move the apparent insertion
    or deletion position without attributing the moved token to another source.
    """
    nodes = []
    for r in original_rows:
        nodes.append({'kind': 'input', 'id': r['input_id'],
                      'corrected': r['body_corrected_span'],
                      'diplomatic': r['body_diplomatic_span']})
    for c in calls:
        nodes.append({'kind': 'master', 'id': c['id'],
                      'corrected': c['corrected_span'],
                      'diplomatic': c['diplomatic_span']})
    parent = list(range(len(nodes)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    def union(i, j):
        a, b = find(i), find(j)
        if a != b:
            parent[b] = a
    for branch in ['corrected', 'diplomatic']:
        ordered = sorted(range(len(nodes)), key=lambda i: nodes[i][branch][0])
        active = []
        for i in ordered:
            start = nodes[i][branch][0]
            active = [j for j in active if nodes[j][branch][1] >= start]
            for j in active:
                if nodes[i]['kind'] != nodes[j]['kind'] and closed_intersects(nodes[i][branch], nodes[j][branch]):
                    union(i, j)
            active.append(i)
    groups = collections.defaultdict(list)
    for i, node in enumerate(nodes):
        groups[find(i)].append(node)
    result = []
    for group_nodes in groups.values():
        record = {'input_ids': [x['id'] for x in group_nodes if x['kind'] == 'input'],
                  'master_ids': [x['id'] for x in group_nodes if x['kind'] == 'master']}
        for branch in ['corrected', 'diplomatic']:
            span = [min(x[branch][0] for x in group_nodes), max(x[branch][1] for x in group_nodes)]
            record[branch + '_span'] = span
            record[branch + '_text'] = projected[branch][span[0]:span[1]]
        result.append(record)
    result.sort(key=lambda x: (x['corrected_span'][0], x['diplomatic_span'][0]))
    # A run of identical adjacent characters can place an insertion/deletion
    # several characters apart in two valid edit paths. Merge consecutive
    # rectangles exactly when their supposed common gap fails the byte test.
    merged = []
    for r in result:
        if merged:
            previous = merged[-1]
            pc = previous['corrected_span'][1]
            pd = previous['diplomatic_span'][1]
            c0, d0 = r['corrected_span'][0], r['diplomatic_span'][0]
            if (c0 < pc or d0 < pd or
                projected['corrected'][pc:c0] != projected['diplomatic'][pd:d0]):
                previous['input_ids'].extend(r['input_ids'])
                previous['master_ids'].extend(r['master_ids'])
                for branch in ['corrected', 'diplomatic']:
                    previous[branch + '_span'][1] = max(previous[branch + '_span'][1], r[branch + '_span'][1])
                    a, b = previous[branch + '_span']
                    previous[branch + '_text'] = projected[branch][a:b]
                continue
        merged.append(r)
    result = merged
    # Equal gaps between components are an explicit proof that both complete
    # edit paths describe exactly these local old/new pairs, without omitted
    # changes between components.
    last_c = last_d = 0
    for n, r in enumerate(result, 1):
        c0, c1 = r['corrected_span']
        d0, d1 = r['diplomatic_span']
        assert c0 >= last_c and d0 >= last_d, ('overlapping component hulls', r)
        assert projected['corrected'][last_c:c0] == projected['diplomatic'][last_d:d0], ('unequal component gap', r)
        r['component_id'] = f'EN-EDIT-COMPONENT-{n:04d}'
        r['preceding_common_gap_exact'] = True
        for kind, rows, ids, id_key, prefix in [
            ('input', original_rows, r['input_ids'], 'input_id', 'body_'),
            ('master', calls, r['master_ids'], 'id', ''),
        ]:
            members = sorted((x for x in rows if x[id_key] in ids),
                             key=lambda x: (x[prefix + 'corrected_span'][0], x[prefix + 'diplomatic_span'][0]))
            cursor_c, cursor_d = c0, d0
            reconstructed_d = []
            for member in members:
                a, b = member[prefix + 'corrected_span']
                u, v = member[prefix + 'diplomatic_span']
                assert a >= cursor_c and u >= cursor_d, ('member order', kind, member[id_key])
                assert projected['corrected'][cursor_c:a] == projected['diplomatic'][cursor_d:u], ('member gap', kind, member[id_key])
                reconstructed_d.extend([projected['corrected'][cursor_c:a], projected['diplomatic'][u:v]])
                cursor_c, cursor_d = b, v
            reconstructed_d.append(projected['corrected'][cursor_c:c1])
            assert ''.join(reconstructed_d) == projected['diplomatic'][d0:d1], ('component replay', kind, r['component_id'])
            r[kind + '_edit_path_replay_exact'] = True
        last_c, last_d = c1, d1
    assert projected['corrected'][last_c:] == projected['diplomatic'][last_d:]
    return result


def intersects(a, b):
    return a and b and max(a[0], b[0]) < min(a[1], b[1])


def without_comments(s):
    return strip_comments_with_origins(s, list(range(len(s))))[0]


def token_at(s, i):
    i = skip_space_and_comments(s, i)
    if i >= len(s):
        return '', i
    if s[i] == '\\':
        m = CONTROL.match(s, i)
        assert m
        return m.group(), m.end()
    return s[i], i + 1


def check_macro_boundaries(master, calls, preamble):
    # All arities below refer to required TeX arguments; optional arguments are
    # separately consumed by the small signature scanner where applicable.
    one = ('underline overline hat widehat tilde widetilde bar vec dot ddot breve '
           'check acute grave ol wt wh not sqrt mathrm mathbf mathbb mathcal '
           'mathfrak mathscr mathsf mathtt mathnormal mathit text textrm textsf '
           'texttt textbf textit emph operatorname operatornamewithlimits '
           'phantom hphantom vphantom smash llap rlap mathrel mathbin mathop '
           'mathord mathopen mathclose mathpunct mathinner pmod pod mod').split()
    two = ('frac dfrac tfrac binom dbinom tbinom overset underset stackrel '
           'underset overset href hyperlink hypertarget').split()
    arity = {'\\' + name: 1 for name in one}
    arity.update({'\\' + name: 2 for name in two})
    arity.update({'\\mathchoice': 4, '\\genfrac': 6, '\\raisebox': 2})
    for m in re.finditer(r'\\(?:newcommand|renewcommand|providecommand)\*?\s*'
                         r'\{(\\[A-Za-z@]+)\}(?:\s*\[(\d+)\])?', preamble):
        arity[m[1]] = int(m[2] or 0)
    for m in re.finditer(r'\\DeclareMathOperator\*?\s*\{(\\[A-Za-z@]+)\}', preamble):
        arity[m[1]] = 0
    zero_standard = ('in simeq longrightarrow to times qquad quad circ otimes '
                     'bullet eta ell vee cdot scriptstyle mod clearpage newpage bigskip').split()
    # \mod has one argument, so do not overwrite its arity.
    for name in zero_standard:
        arity.setdefault('\\' + name, 0)
    for name in [r'\,', r'\;', r'\:', r'\!', r'\[', r'\]', r'\(', r'\)', r'\\', '\\ ']:
        arity[name] = 0
    prior_macros = []
    hazards = []
    tail_passthrough = []
    subsequent_scripts = []
    preceding_script_arguments = []
    seen_prior = collections.Counter()
    for call in calls:
        start, end = call['master_start'], call['master_end']
        prefix = without_comments(master[max(0, start - 300):start])
        previous = re.search(r'(\\(?:[A-Za-z@]+|.))\s*$', prefix, re.S)
        nxt, _ = token_at(master, end)
        if nxt in ['_', '^', "'"]:
            subsequent_scripts.append({'id': call['id'], 'next_token': nxt,
                                       'context': master[start:end + 70]})
        if prefix.rstrip().endswith(('_', '^')):
            preceding_script_arguments.append({'id': call['id'], 'context': prefix[-100:] + master[start:end]})
        if previous:
            name = previous[1]
            seen_prior[name] += 1
            row = {'id': call['id'], 'macro': name, 'required_arguments': arity.get(name),
                   'context': prefix[-110:] + master[start:end]}
            prior_macros.append(row)
            if name == r'\mod':
                row = dict(row)
                row['definition'] = (r'\DeclareRobustCommand{\mod}[1]{\allowbreak\if@display\mkern18mu'
                                     r'\else\mkern12mu\fi{\operator@font mod}\,\,#1}')
                row['definition_source'] = 'amsmath.sty, installed build dependency, lines 910–911'
                row['token_expansion'] = ('The single argument token is \\SGAvar. It is reinserted once as the '
                                          'last token of the \\mod replacement, immediately followed by its '
                                          'three original groups; no delimiter, closing group, or additional '
                                          'token separates \\SGAvar from those groups.')
                tail_passthrough.append(row)
            elif arity.get(name, 0) > 0:
                hazards.append(row)
            elif name not in arity:
                hazards.append(dict(row, reason='unknown immediate predecessor arity'))
    # Scan required arguments of known commands in the common stream. Variant
    # calls and their complete arguments are one opaque editing unit here.
    call_by_start = {c['master_start']: c for c in calls}
    unbraced_argument_calls = []
    i = 0
    while i < len(master):
        if i in call_by_start:
            i = call_by_start[i]['master_end']
            continue
        if master[i] == '%':
            j = master.find('\n', i)
            i = len(master) if j < 0 else j + 1
            continue
        if master[i] != '\\':
            i += 1
            continue
        m = CONTROL.match(master, i)
        assert m
        name = m.group()
        j = m.end()
        n = arity.get(name, 0)
        # This audit targets direct mandatory-argument consumption. For sqrt
        # and common text commands an initial optional [] group is skipped.
        for argno in range(1, n + 1):
            j = skip_space_and_comments(master, j)
            if j >= len(master):
                break
            if master[j] == '[' and name in [r'\sqrt', r'\raisebox']:
                k = master.find(']', j + 1)
                if k >= 0:
                    j = skip_space_and_comments(master, k + 1)
            if j in call_by_start:
                c = call_by_start[j]
                unbraced_argument_calls.append({'id': c['id'], 'macro': name, 'argument_number': argno,
                                                'transparent_tail_substitution': name == r'\mod'})
                # TeX consumes one token, not the following SGAvar groups.
                j += len(r'\SGAvar')
            elif master[j] == '{':
                _, j = group(master, j)
            else:
                _, j = token_at(master, j)
        i = m.end()
    unsafe_args = [x for x in unbraced_argument_calls if not x['transparent_tail_substitution']]
    return {
        'variant_calls_checked': len(calls),
        'immediate_control_sequence_predecessors': dict(seen_prior),
        'immediate_predecessor_rows': prior_macros,
        'immediate_predecessor_hazards': hazards,
        'unbraced_required_argument_calls': unbraced_argument_calls,
        'unsafe_unbraced_required_argument_calls': unsafe_args,
        'transparent_tail_argument_cases': tail_passthrough,
        'unabsorbed_following_scripts': subsequent_scripts,
        'unbraced_preceding_script_arguments': preceding_script_arguments,
        'no_operator_argument_interference': not (hazards or unsafe_args or subsequent_scripts or preceding_script_arguments),
    }


def main():
    global HERE, EN, BUILD
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--english', type=Path, default=EN)
    ap.add_argument('--prepared', type=Path, default=BUILD)
    ap.add_argument('--output', type=Path, default=HERE)
    args = ap.parse_args()
    EN, BUILD, HERE = args.english, args.prepared, args.output
    HERE.mkdir(parents=True, exist_ok=True)
    filenames = {
        'flat_corrected': EN / 'EN_corrected_flat.tex',
        'flat_diplomatic': EN / 'EN_diplomatic_flat.tex',
        'master': BUILD / 'EN_annotated_body.tex',
        'prepared_corrected': BUILD / 'EN_corrected_body.tex',
        'prepared_diplomatic': BUILD / 'EN_diplomatic_body.tex',
        'input_variants': EN / 'EN_variants.json',
        'copied_input_variants': BUILD / 'EN_variants_input.json',
        'master_variants': BUILD / 'EN_variants.json',
        'alignment': EN / 'EN_ALIGNMENT.json',
        'preamble': BUILD / 'EN_preamble.tex',
    }
    if (BUILD / 'EN_wrapper_editorial_extractions.json').exists():
        filenames['wrapper_editorial_extractions'] = BUILD / 'EN_wrapper_editorial_extractions.json'
    contents = {k: p.read_text() for k, p in filenames.items()}
    initial_hashes = {k: sha(s) for k, s in contents.items()}
    variants = json.loads(contents['input_variants'])
    metadata = json.loads(contents['master_variants'])
    alignment = json.loads(contents['alignment'])
    assert variants == json.loads(contents['copied_input_variants'])
    calls, projected = calls_and_branches(contents['master'])
    by_id = {c['id']: c for c in calls}
    meta_by_id = {c['id']: c for c in metadata}
    assert len(by_id) == len(calls) == len(meta_by_id) == len(metadata)
    assert by_id.keys() == meta_by_id.keys()
    for call in calls:
        assert call['before'] == meta_by_id[call['id']]['before'], call['id']
        assert call['after'] == meta_by_id[call['id']]['after'], call['id']
    assert r'\SGAFixedVariant' not in contents['master']
    wrapper_relocation = None
    if 'wrapper_editorial_extractions' in contents:
        extraction_rows = json.loads(contents['wrapper_editorial_extractions'])
        assert len(extraction_rows) == 1
        e = extraction_rows[0]
        assert e['id'] == 'EN-INHERITED-0046-P43'
        start, end = e['start_before'], e['end_before']
        assert contents['master'][start:end] == e['before'] and e['after'] == ''
        relocated = contents['master'][:start] + contents['master'][end:]
        assert sha(contents['master']) == e['body_before_sha256']
        assert sha(relocated) == e['body_after_sha256']
        assert relocated[:start] + e['before'] + relocated[start:] == contents['master']
        relocated_calls, _ = calls_and_branches(relocated)
        assert [x['id'] for x in relocated_calls] == [x['id'] for x in calls]
        assert [m.group() for m in FOLIO.finditer(relocated)] == [m.group() for m in FOLIO.finditer(contents['master'])]
        wrapper_relocation = {
            'id': e['id'], 'exact_reverse_replay': True,
            'removed_inherited_editorial_footnote_characters': end - start,
            'frozen_prepared_master_unchanged': True,
            'variant_calls_unchanged': len(relocated_calls),
            'folio_markers_unchanged': len(list(FOLIO.finditer(relocated))),
            'full_payload_preservation_checked_separately_in': 'READER_UNRESOLVED_NOTES_AUDIT.json',
            'source': e['source'],
        }
    body_meta = {}
    coordinates = {}
    marker_rows = {}
    for branch in ['corrected', 'diplomatic']:
        expected, positions, body_positions, meta = expected_body(contents['flat_' + branch], branch, alignment)
        prepared = contents['prepared_' + branch]
        assert projected[branch] == prepared, ('master branch != prepared', branch)
        assert expected == prepared, ('frozen source projection != prepared', branch)
        markers = list(FOLIO.finditer(prepared))
        expected_folios = [int(x['folio']) for x in sorted(alignment, key=lambda x: x['position_' + branch])]
        assert [int(m[2]) for m in markers] == expected_folios
        assert all(int(m[1]) == int(m[2]) + 11 for m in markers)
        assert len(markers) == len(alignment)
        marker_rows[branch] = [{'index': i + 1, 'folio': int(m[2]), 'scan_index': int(m[1]),
                               'body_span': list(m.span()),
                               'flat_anchor_position': sorted(alignment, key=lambda x: x['position_' + branch])[i]['position_' + branch]}
                              for i, m in enumerate(markers)]
        meta.update({'master_branch_equals_prepared_body_exactly': True,
                     'frozen_source_projection_equals_prepared_body_exactly': True,
                     'whitespace_equivalence_fallback_used': False,
                     'marker_count': len(markers), 'distinct_folios': len(set(expected_folios)),
                     'marker_sequence_exact': True})
        body_meta[branch] = meta
        coordinates[branch] = positions, body_positions
    # Verify the original variation list reconstructs the complete flat D text.
    ordered = sorted(variants, key=lambda r: r['start_corrected'])
    flat_c = contents['flat_corrected']
    flat_d = contents['flat_diplomatic']
    rebuilt = flat_c
    for v in reversed(ordered):
        a, b = v['start_corrected'], v['end_corrected']
        assert rebuilt[a:b] == v['after'], v['id']
        rebuilt = rebuilt[:a] + v['before'] + rebuilt[b:]
    assert rebuilt == flat_d
    delta = 0
    original_rows = []
    master_to_original = {c['id']: [] for c in calls}
    for v in ordered:
        cs, ce = v['start_corrected'], v['end_corrected']
        ds, de = cs + delta, cs + delta + len(v['before'])
        assert flat_c[cs:ce] == v['after'] and flat_d[ds:de] == v['before']
        delta += len(v['before']) - len(v['after'])
        changed = {'corrected': [], 'diplomatic': []}
        for tag, a0, a1, b0, b1 in difflib.SequenceMatcher(None, v['before'], v['after'], autojunk=False).get_opcodes():
            if tag == 'equal':
                continue
            for branch, start, end in [('diplomatic', ds + a0, ds + a1), ('corrected', cs + b0, cs + b1)]:
                span = source_interval_to_body(start, end, *coordinates[branch])
                if span:
                    changed[branch].append(span)
        matched = []
        for call in calls:
            if any(intersects(span, call[branch + '_span']) for branch in changed for span in changed[branch]):
                matched.append(call['id'])
                master_to_original[call['id']].append(v['id'])
        original_rows.append({'input_id': v['id'], 'page': v['page'], 'source': v['source'],
                              'flat_corrected_span': [cs, ce], 'flat_diplomatic_span': [ds, de],
                              'body_corrected_span': source_edit_span_to_body(cs, ce, *coordinates['corrected'], len(projected['corrected'])),
                              'body_diplomatic_span': source_edit_span_to_body(ds, de, *coordinates['diplomatic'], len(projected['diplomatic'])),
                              'changed_body_spans': changed, 'master_ids': matched})
    components = edit_components(original_rows, calls, projected)
    component_by_input = {i: r for r in components for i in r['input_ids']}
    component_by_master = {i: r for r in components for i in r['master_ids']}
    direct_master_to_original = master_to_original
    master_to_original = {c['id']: component_by_master[c['id']]['input_ids'] for c in calls}
    for r in original_rows:
        r['direct_changed_character_master_ids'] = r.pop('master_ids')
        r['component_id'] = component_by_input[r['input_id']]['component_id']
        r['master_ids'] = component_by_input[r['input_id']]['master_ids']
    unmatched_inputs = [r for r in original_rows if not r['master_ids']]
    unmatched_masters = [k for k, v in master_to_original.items() if not v]
    input_by_id = {v['id']: v for v in variants}
    source_rows = []
    for c in calls:
        mid = c['id']
        declared = re.findall(r'EN_variants_input\.json:([A-Za-z0-9-]+)', meta_by_id[mid]['source'])
        ids = master_to_original[mid]
        source_rows.append({'master_id': mid, 'master_page': meta_by_id[mid]['page'],
                            'master_corrected_span': c['corrected_span'],
                            'master_diplomatic_span': c['diplomatic_span'],
                            'original_input_ids_by_exact_edit_component': ids,
                            'direct_changed_character_input_ids': direct_master_to_original[mid],
                            'component_id': component_by_master[mid]['component_id'],
                            'input_component_pages': sorted(set(int(input_by_id[i]['page']) for i in ids)),
                            'declared_input_ids': declared,
                            'declared_source': meta_by_id[mid]['source'],
                            'position_resolved_source_ids': [input_by_id[i]['source'] for i in ids],
                            'declared_ids_missing_from_input': [i for i in declared if i not in input_by_id],
                            'declared_ids_outside_exact_position_map': [i for i in declared if i not in ids],
                            'declared_ids_have_no_exact_match': bool(declared) and not bool(set(declared) & set(ids)),
                            'is_generic_build_source': meta_by_id[mid]['source'].startswith('BUILD-SOURCE-'),
                            'resolved': bool(ids)})
    resolved_sources = []
    for row in source_rows:
        mid = row['master_id']
        ids = row['original_input_ids_by_exact_edit_component']
        pages = sorted(set(int(input_by_id[i]['page']) for i in ids))
        source_parts = ['EN_variants_input.json:' + i for i in ids]
        for i in ids:
            source_parts.extend(x.strip() for x in input_by_id[i]['source'].split(';') if x.strip())
        if mid.startswith('R98-'):
            source_parts.insert(0, 'PLACES_98_DECIDED.tsv:' + mid)
        resolved_sources.append({'id': mid, 'input_ids': ids,
                                 'page': pages[0], 'pages': pages,
                                 'exposes': list(dict.fromkeys(input_by_id[i].get('expose') for i in ids)),
                                 'source': '; '.join(dict.fromkeys(source_parts)),
                                 'component_id': row['component_id'],
                                 'mapping_basis': 'Exact old/new edit component with separately replayed input and master paths.'})
    scan_rows = []
    for c in calls:
        if c['id'].startswith('R98-'):
            v = input_by_id[c['id']]
            assert c['before'].startswith(v['before']) and c['after'].startswith(v['after'])
            suffix_d = c['before'][len(v['before']):]
            suffix_c = c['after'][len(v['after']):]
            assert suffix_c == suffix_d
            scan_rows.append({'id': c['id'], 'page': v['page'],
                              'original_before': v['before'], 'original_after': v['after'],
                              'absorbed_identical_script_suffix': suffix_c,
                              'exact_glyph_preservation': True,
                              'source': meta_by_id[c['id']]['source']})
    assert len(scan_rows) == 32
    boundaries = check_macro_boundaries(contents['master'], calls, contents['preamble'])
    folio_calls = [{'id': f'FOLIO-{m[2]}-{n}', 'master_start': m.start(), 'master_end': m.end()}
                   for n, m in enumerate(FOLIO.finditer(contents['master']), 1)]
    folio_boundaries = check_macro_boundaries(contents['master'], folio_calls, contents['preamble'])
    source_summary = {
        'original_input_variants': len(variants), 'master_variants': len(calls),
        'input_full_text_replay_exact': True,
        'input_catalog_copy_exact': True,
        'master_metadata_matches_exact_call_arguments': True,
        'original_variants_with_master_matches': sum(bool(r['master_ids']) for r in original_rows),
        'master_variants_with_original_matches': sum(bool(v) for v in master_to_original.values()),
        'original_to_master_degree_counts': dict(collections.Counter(len(r['master_ids']) for r in original_rows)),
        'master_to_original_degree_counts': dict(collections.Counter(len(v) for v in master_to_original.values())),
        'unmatched_original_variants': unmatched_inputs,
        'unmatched_master_variants': unmatched_masters,
        'master_rows_with_generic_build_source': sum(r['is_generic_build_source'] for r in source_rows),
        'generic_build_source_rows_resolved_by_position': sum(r['is_generic_build_source'] and r['resolved'] for r in source_rows),
        'master_rows_with_explicit_input_id': sum(bool(r['declared_input_ids']) for r in source_rows),
        'master_rows_with_unknown_declared_input_id': sum(bool(r['declared_ids_missing_from_input']) for r in source_rows),
        'master_rows_with_broad_declared_input_ids': sum(bool(r['declared_ids_outside_exact_position_map']) for r in source_rows),
        'master_rows_with_declared_ids_but_no_exact_match': sum(r['declared_ids_have_no_exact_match'] for r in source_rows),
        'master_page_labels_outside_input_component_folios': sum(int(r['master_page']) not in r['input_component_pages'] for r in source_rows),
        'individual_scan_variants_preserved': len(scan_rows),
        'exact_edit_components': len(components),
        'every_gap_between_edit_components_exact': True,
        'provenance_mapping_method': 'Exact connected edit rectangles from both complete before/after paths; each component retains its full before and after text, with every intervening common substring verified byte-exact.',
    }
    final_hashes = {k: sha(p.read_text()) for k, p in filenames.items()}
    assert initial_hashes == final_hashes, 'Input files changed during audit'
    success = (not unmatched_inputs and not unmatched_masters and boundaries['no_operator_argument_interference']
               and folio_boundaries['no_operator_argument_interference']
               and not source_summary['master_rows_with_unknown_declared_input_id']
               and not source_summary['master_rows_with_broad_declared_input_ids']
               and not source_summary['master_rows_with_generic_build_source']
               and not source_summary['master_page_labels_outside_input_component_folios'])
    report = {
        'audit': 'Independent English annotated-master preservation audit',
        'passed': success,
        'body_and_original_variation_preservation_passed': not unmatched_inputs and not unmatched_masters,
        'implementation_independent_of_builder': True,
        'input_files_unchanged_during_audit': True,
        'offset_convention': 'Unicode character offsets, zero-based, end-exclusive',
        'input_hashes': initial_hashes,
        'body_projection': body_meta,
        'source_variation_preservation': source_summary,
        'operator_and_script_boundary_summary': {k: v for k, v in boundaries.items() if k not in ['immediate_predecessor_rows']},
        'folio_marker_boundary_summary': {k: v for k, v in folio_boundaries.items() if k not in ['immediate_predecessor_rows']},
        'full_body_coverage_verified': True,
        'separate_reader_wrapper_editorial_relocation': wrapper_relocation,
        'all_793_markers_matched_in_both_branches': all(x['marker_count'] == 793 and x['marker_sequence_exact'] for x in body_meta.values()),
        'whitespace_only_changes_requiring_equivalence_argument': 0,
        'scope': 'Both frozen English bodies from the first verified Exposé I anchor through the final index, before end{document}; old editorial front removed explicitly. Their inherited p43 editorial footnote is retained in this prepared-source comparison, then relocated exactly at the separate reader-wrapper stage described in this report. Apparatus rendering and PDF visual layout are validated separately by the build owner.',
        'evidence_files': ['EN_MASTER_TO_INPUT_VARIANTS.json', 'EN_INPUT_TO_MASTER_VARIANTS.json',
                           'EN_MASTER_FOLIO_MARKERS.json', 'EN_MASTER_SCRIPT_AND_ARGUMENT_AUDIT.json',
                           'EN_MASTER_R98_PRESERVATION.json', 'EN_MASTER_EDIT_COMPONENTS.json',
                           'EN_MASTER_RESOLVED_SOURCES.json', 'EN_MASTER_FOLIO_BOUNDARY_AUDIT.json'],
    }
    write_json('INDEPENDENT_EN_MASTER_AUDIT.json', report)
    write_json('EN_MASTER_TO_INPUT_VARIANTS.json', source_rows)
    write_json('EN_INPUT_TO_MASTER_VARIANTS.json', original_rows)
    write_json('EN_MASTER_FOLIO_MARKERS.json', marker_rows)
    write_json('EN_MASTER_SCRIPT_AND_ARGUMENT_AUDIT.json', boundaries)
    write_json('EN_MASTER_R98_PRESERVATION.json', scan_rows)
    write_json('EN_MASTER_EDIT_COMPONENTS.json', components)
    write_json('EN_MASTER_RESOLVED_SOURCES.json', resolved_sources)
    write_json('EN_MASTER_FOLIO_BOUNDARY_AUDIT.json', folio_boundaries)
    print(json.dumps({'passed': success, 'branches_exact': 2, 'markers_each': len(alignment),
                      'sources': source_summary,
                      'boundary_hazards': {k: boundaries[k] for k in ['immediate_predecessor_hazards', 'unsafe_unbraced_required_argument_calls', 'unabsorbed_following_scripts', 'unbraced_preceding_script_arguments']}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
