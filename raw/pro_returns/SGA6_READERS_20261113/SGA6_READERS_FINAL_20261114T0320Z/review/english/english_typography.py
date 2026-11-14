#!/usr/bin/env python3
"""Exact English transport of the completed source convention occurrence map."""
from bisect import bisect_right
from collections import defaultdict, Counter
from pathlib import Path
import hashlib, json, re
from source_emphasis import MATH, braced, underline_words

EN = Path(__file__).resolve().parent
ROOT = EN.parents[1]
MARK = re.compile(r'%{10}\s+scan idx\s+\d+\s*\|\s*folio\s+(\S+)\s+%{10}')
NESTED = {
    (616, r"\emph{$m$-r\'egulier}"): r'\emph{$m$-regular}',
    (619, r'\emph{\((b)\)-faisceau}'): r'\emph{\((b)\)-sheaf}',
    (621, r'\emph{\((b)\)-polynômes}'): r'\emph{\((b)\)-polynomials}',
    (658, r"\emph{$k$-cycle positif sp\'ecial de dimension $r$}"): r'\emph{special positive $k$-cycle of dimension $r$}',
    (658, r'\emph{int\`egre}'): r'\emph{integral}',
    (658, r"\emph{degr\'e}"): r'\emph{degree}',
}
DIRECT = {
    168: r'\uline{This definition conflicts with}',
    169: r'\uline{and replaces that definition}',
}


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def outer_groups(text):
    marks = list(MARK.finditer(text))
    offsets = [m.start() for m in marks]
    pos = 0
    groups = []
    while True:
        start = text.find(r'\emph{', pos)
        if start < 0:
            break
        body, end = braced(text, start + 5)
        k = bisect_right(offsets, start) - 1
        page = marks[k][1] if k >= 0 else None
        groups.append(dict(start=start, end=end, page=page, old=text[start:end]))
        pos = end
    return groups


def protect_group(group, source_group):
    original = group
    records = []
    page = source_group['page']
    for occurrence in source_group['plain_nested']:
        old = NESTED[page, occurrence['old']]
        assert group.count(old) == 1, (page, old, group.count(old))
        inner, end = braced(old, 5)
        assert end == len(old)
        new = r'\SGAPlainWords{' + inner + '}'
        group = group.replace(old, new, 1)
        records.append(dict(kind='plain_nested', French=occurrence['old'], English_before=old, English_after=new))
    for kind, items in [('plain_resp', source_group['plain_resp']),
                        ('plain_references', source_group['plain_references'])]:
        counts = Counter(item['text'] for item in items)
        for token, count in counts.items():
            math = [(m.start(), m.end()) for m in MATH.finditer(group)]
            candidates = [m for m in re.finditer(r'(?<![A-Za-z0-9])' + re.escape(token) + r'(?![A-Za-z0-9])', group)
                          if not any(a <= m.start() < b for a, b in math)]
            assert len(candidates) == count, (page, kind, token, len(candidates), count)
            for match in reversed(candidates):
                new = r'\SGAPlainWords{' + match.group() + '}'
                group = group[:match.start()] + new + group[match.end():]
            records.extend(dict(kind=kind, French=token, English_before=token,
                                English_after=r'\SGAPlainWords{' + token + '}') for _ in candidates)
    assert [m.group() for m in MATH.finditer(original)] == [m.group() for m in MATH.finditer(group)]
    return group, records


def note_records(text):
    marks = list(MARK.finditer(text))
    offsets = [m.start() for m in marks]
    result = []
    for match in re.finditer(r'\\SGAAuthorFoot(note|Mark|Text)\{', text):
        label, end = braced(text, match.end() - 1)
        if match[1] != 'Mark':
            _, end = braced(text, end)
        k = bisect_right(offsets, match.start()) - 1
        result.append(dict(page=marks[k][1] if k >= 0 else None, command=match[1],
                           label=label, literal=text[match.start():end]))
    return result


def render_reviewed(source, catalog, layer='current'):
    original = source
    folder = ROOT / 'review/global_conventions'
    source_groups = [x for x in json.loads((folder / 'typography_groups.json').read_text()) if x['layer'] == layer]
    patches = [json.loads(x) for x in (folder / 'post_review_patches.jsonl').read_text().splitlines()]
    reviewed = set(catalog['reviewed_numeric_folios'])
    labels = []
    numeric_heading_file = ROOT / 'review/global_numeric_headings/english_correspondence.jsonl'
    numeric_headings = []
    for line in numeric_heading_file.read_text().splitlines():
        patch = json.loads(line)
        a = source.index(patch['scope_start'])
        b = source.index(patch['scope_end'], a)
        part = source[a:b]
        old, new = patch['exact_old_anchor'], patch['exact_new_anchor']
        assert part.count(old) == patch['expected_count'], (patch['source_id'], part.count(old))
        assert new.replace(r'\normalfont ', '', 1) == old
        source = source[:a] + part.replace(old, new, 1) + source[b:]
        numeric_headings.append(dict(source_id=patch['source_id'], page=patch['page'],
            English_before=old, English_after=new, literal_label=patch['printed_label'],
            inverse_declaration_removal_pass=True))
    assert len(numeric_headings) == 49
    for patch in patches:
        if patch['kind'] != 'plain_paragraph_number' or patch['page'] not in reviewed:
            continue
        marks = list(MARK.finditer(source))
        k = next(i for i, m in enumerate(marks) if m[1] == str(patch['page']))
        a = marks[k].start()
        b = marks[k + 1].start() if k + 1 < len(marks) else len(source)
        part = source[a:b]
        expected = patch.get('expected_count', 1)
        assert part.count(patch['old']) == expected, (patch['patch_id'], part.count(patch['old']))
        source = source[:a] + part.replace(patch['old'], patch['new']) + source[b:]
        labels.append(dict(source_patch_id=patch['patch_id'], page=patch['page'],
                           English_before=patch['old'], English_after=patch['new'],
                           occurrence_count=expected,
                           display_side_exception=patch['page'] == 605))
    after_labels = source
    by_page = defaultdict(list)
    for group in outer_groups(source):
        if group['page'] and group['page'].isdigit() and int(group['page']) in reviewed:
            by_page[int(group['page'])].append(group)
    source_by_page = defaultdict(list)
    for group in source_groups:
        source_by_page[group['page']].append(group)
    mapped = []
    replacements = []
    exclusions = []
    for page, groups in source_by_page.items():
        assert page in reviewed
        if page == 419:
            assert not by_page[page]
            for group in groups:
                anchor = DIRECT[group['group_index']]
                assert source.count(anchor) == 1
                mapped.append(dict(source_group_index=group['group_index'], page=page,
                    French_before=group['old'], French_after=group['new'],
                    English_before=anchor, English_after=anchor,
                    status='The exact translated group already has its direct source-confirmed rule; retained once.'))
            continue
        assert len(groups) == len(by_page[page]), (page, len(groups), len(by_page[page]))
        for fr, en in zip(groups, by_page[page]):
            protected, local = protect_group(en['old'], fr)
            rendered, stats = underline_words(protected)
            mapped.append(dict(source_group_index=fr['group_index'], page=page,
                French_before=fr['old'], French_after=fr['new'],
                English_before=en['old'], English_protected=protected, English_after=rendered,
                English_before_sha256=sha(en['old']), English_after_sha256=sha(rendered),
                occurrence_count=1, mapped_exclusions=local,
                status='Corresponding complete translated outer group, in its reviewed source-page order; exact words, math, notes and markers preserved.'))
            replacements.append((en['start'], en['end'], protected))
            exclusions.extend(dict(source_group_index=fr['group_index'], page=page, **r) for r in local)
    for a, b, protected in reversed(sorted(replacements)):
        source = source[:a] + protected + source[b:]
    protected_source = source
    ranges = [
        ('1–700', '%%%%%%%%%%  scan idx 14  |  folio 1', '%%%%%%%%%%  scan idx 714  |  folio rear-715'),
    ]
    range_records = []
    for label, start, end in reversed(ranges):
        a = source.index(start)
        b = source.index(end, a)
        part = source[a:b]
        new, stats = underline_words(part)
        source = source[:a] + new + source[b:]
        range_records.append(dict(interval=label, before_sha256=sha(part), after_sha256=sha(new), counts=stats))
    reference_count = 21 if layer == 'current' else 20
    assert len(exclusions) == 14 + reference_count
    assert Counter(x['kind'] for x in exclusions) == {'plain_nested': 6, 'plain_resp': 8, 'plain_references': reference_count}
    assert len(mapped) == 387
    assert len(labels) == 77
    # Every mapped result must remain exactly present, independently of the
    # all-body mathematical invariants enforced by underline_words.
    for record in mapped:
        if record['status'].startswith('The exact translated'):
            assert source.count(record['English_after']) == 1
    notes_before, notes_after = note_records(original), note_records(source)
    assert [(r['command'], r['label']) for r in notes_before] == [(r['command'], r['label']) for r in notes_after]
    note_changes = []
    for old, new in zip(notes_before, notes_after):
        if old['literal'] != new['literal']:
            assert old['page'] == '21'
            note_changes.append(dict(page=21, before=old['literal'], after=new['literal']))
    # The two source X567 resp. groups retain their independently observed rule.
    m = next(m for m in MARK.finditer(source) if m[1] == '567')
    n = next(m for m in MARK.finditer(source) if m[1] == '568')
    assert source[m.start():n.start()].count(r'\uline{resp}.') == 2
    pos = 0
    direct_rule_groups = 0
    while True:
        a = source.find(r'\uline{', pos)
        if a < 0:
            break
        body, pos = braced(source, a + 6)
        assert r'\uline{' not in body, ('Nested underline introduced or inherited', source[a:pos])
        direct_rule_groups += 1
    record = dict(
        source_layer=layer,
        basis='Completed local French source reviews and review/global_conventions/EN_TYPOGRAPHY_HANDOFF.md; exact translated groups are mapped below, without a new image-reading claim.',
        source_input_hashes={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [folder/'typography_groups.json', folder/'plain_exclusions.json', folder/'post_review_patches.jsonl', folder/'EN_TYPOGRAPHY_HANDOFF.md']},
        annotated_input_sha256=sha(original), after_plain_labels_sha256=sha(after_labels),
        protected_input_sha256=sha(protected_source), rendered_output_sha256=sha(source),
        mapped_source_outer_groups=len(mapped), plain_exclusion_counts=dict(Counter(x['kind'] for x in exclusions)),
        ordinary_paragraph_label_transports=len(labels), paragraph_label_records=labels,
        numeric_only_structural_heading_transports=len(numeric_headings),
        numeric_heading_records=numeric_headings,
        numeric_heading_source_sha256=hashlib.sha256(numeric_heading_file.read_bytes()).hexdigest(),
        source_group_records=mapped, plain_exclusion_records=exclusions,
        range_records=list(reversed(range_records)), author_note_commands=len(notes_before),
        author_note_labels_identical=True, author_note_wrapper_changes=note_changes,
        source567_ruled_resp_occurrences=2, nested_uline_groups=0,
        retained_or_generated_uline_groups=direct_rule_groups,
        source_specific_wrapper_transport_complete=True,
        output_QA_scope='This formatter validates source-specific wrapper transport. Actual compilation, macro dispositions and bounded rendered-page inspection are recorded separately in the final release audits.',
        limitation='Exact source-specific wrapper transports validated across the complete translated body; this formatter itself makes no all-output-page visual-inspection claim.')
    return source, record
