#!/usr/bin/env python3
"""Recompute apparatus counts from the final edition registers and TeX guards.

No totals are cached or hand-entered. Run after rebuilding both masters.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / 'output' / 'records'
INPUTS = {}


def read(relative):
    path = ROOT / relative
    data = path.read_bytes()
    INPUTS[relative] = hashlib.sha256(data).hexdigest()
    return data.decode('utf-8')


def load(name):
    return json.loads(read('output/records/' + name))


def expose_name(volume, expose, page=''):
    expose = {'Introduction': 'INTRO', 'Front': 'Front matter'}.get(expose, expose)
    # The single-page Expose XIII survives in the Expose XII source file.
    if volume == '7II' and expose == 'XII' and str(page).strip() == '82':
        return 'XIII'
    if volume == '7I' and expose == 'IX' and str(page).strip() in {'525', '526', '527'}:
        return 'Catalogue'
    return expose


ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
         'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX',
         'XX', 'XXI', 'XXII']


def sort_place(place):
    volume, expose = place
    rank = -2 if expose == 'Front matter' else -1 if expose == 'INTRO' else (
        ROMAN.index(expose) if expose in ROMAN else 99)
    return (0 if volume == '7I' else 1, rank, expose)


def label(place):
    volume, expose = place
    return volume + ' / ' + ('Introduction' if expose == 'INTRO' else expose)


def md(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join('---' for _ in headers) + ' |'] +
                     ['| ' + ' | '.join(md(x) for x in row) + ' |' for row in rows])


def verify_forms(language, entries, notes, unresolved):
    directory = language.lower()
    if language == 'FR':
        master = 'SGA7_FR_master_annote.tex'
        forms = {'diplomatic': ('SGA7_FR_diplomatique.tex', 0),
                 'corrected_apparatus': ('SGA7_FR_corrige_apparat.tex', 1),
                 'reading': ('SGA7_FR_texte_de_lecture.tex', 2)}
    else:
        master = 'SGA7_EN_annotated_master.tex'
        forms = {'diplomatic': ('SGA7_EN_diplomatic.tex', 0),
                 'corrected_apparatus': ('SGA7_EN_corrected_apparatus.tex', 1),
                 'reading': ('SGA7_EN_reading.tex', 2)}
    path = f'output/{directory}/{master}'
    text = read(path)
    ids = re.findall(r'\\hypertarget\{app-([^}]+)\}', text)
    expected = [x['id'] for x in entries]
    assert collections.Counter(ids) == collections.Counter(expected), (
        language, 'apparatus/master target mismatch')
    guarded = '\n'.join(re.findall(r'\\ifnum\\SGAform=1(.*?)\\fi', text, re.S))
    guarded_ids = re.findall(r'\\hypertarget\{app-([^}]+)\}', guarded)
    assert collections.Counter(guarded_ids) == collections.Counter(expected), (
        language, 'apparatus target outside corrected-only guard')
    for note in notes:
        assert '\\textbf{' + note['id'] + '}' in guarded, (language, note['id'])
    for note in unresolved:
        assert '\\subsection*{' + note['id'] + ' ' in guarded, (language, note['id'])
    selectors = {}
    for form, (filename, mode) in forms.items():
        source = read(f'output/{directory}/{filename}')
        found = re.search(r'^\\SGAform=(\d+)\s*$', source, re.M)
        assert found and int(found.group(1)) == mode, (language, form, 'selector')
        expected_form = text.replace('\\SGAform=1\n', '\\SGAform=' + str(mode) + '\n', 1)
        assert source == expected_form, (language, form, 'master projection')
        selectors[form] = {'selector': mode, 'master_projection_exact': True,
                           'visible_variant_entries': len(entries) if mode == 1 else 0,
                           'visible_inherited_notes': len(notes) if mode == 1 else 0,
                           'visible_unresolved_notes': len(unresolved) if mode == 1 else 0}
    return {'master_targets_match_register': True,
            'every_target_in_corrected_only_guard': True,
            'every_editorial_note_in_corrected_only_guard': True,
            'forms': selectors}


def run():
    registers = {lang: load(lang + '_APPARATUS.json') for lang in ('FR', 'EN')}
    inherited = load('EN_INHERITED_EDITORIAL_NOTES.json')
    decisions = load('editorial_decisions.json')
    unresolved = decisions['unresolved_notes']
    marks = list(csv.DictReader(io.StringIO(read('output/records/FR_PAGE_MARKERS.tsv')), delimiter='\t'))
    page_map = {}
    for row in marks:
        key = (row['volume'], row['folio'])
        page_map[key] = expose_name(row['volume'], row['expose'], row['folio'])
    page_map[('7II', '82')] = 'XIII'
    places = {(row['volume'], expose_name(row['volume'], row['expose'], row['folio']))
              for row in marks}
    places.add(('7II', 'XIII'))
    normalized = {}
    reallocations = []
    for lang, entries in registers.items():
        assert len({e['id'] for e in entries}) == len(entries), (lang, 'duplicate ids')
        assert all(e['before'] != e['after'] for e in entries), (lang, 'identical readings')
        normalized[lang] = []
        for e in entries:
            ex = expose_name(e['volume'], e['expose'], e['page'])
            places.add((e['volume'], ex))
            if ex != e['expose'] and e['expose'] != 'Introduction':
                reallocations.append({'language': lang, 'id': e['id'], 'stored_expose': e['expose'],
                                      'report_expose': ex, 'folio': e['page']})
            normalized[lang].append({**e, 'report_expose': ex})
    inherited_by = collections.Counter((e['volume'], expose_name(e['volume'], e['expose'], e['page']))
                                       for e in inherited)
    unresolved_by = collections.Counter()
    unresolved_locations = []
    for n in unresolved:
        match = re.match(r'(7I{1,2}):([0-9]+|[IVX]+)', n['page'])
        assert match, n['id']
        volume, page = match.groups()
        ex = page_map.get((volume, page))
        assert ex, (n['id'], volume, page)
        unresolved_by[(volume, ex)] += 1
        unresolved_locations.append({'id': n['id'], 'volume': volume, 'expose': ex,
                                     'page': n['page'], 'status': n['status']})
    places.update(inherited_by)
    places.update(unresolved_by)
    places = sorted(places, key=sort_place)
    checks = {lang: verify_forms(lang, registers[lang], inherited if lang == 'EN' else [], unresolved)
              for lang in ('FR', 'EN')}
    per_place = []
    per_kind = []
    for lang in ('FR', 'EN'):
        for place in places:
            entries = [e for e in normalized[lang] if (e['volume'], e['report_expose']) == place]
            groups = {e['group_id'] for e in entries}
            n_inherited = inherited_by[place] if lang == 'EN' else 0
            per_place.append({'language': lang, 'volume': place[0], 'expose': place[1],
                              'diplomatic_entries': 0, 'corrected_entries': len(entries),
                              'reading_entries': 0, 'variant_blocks': len(groups),
                              'inherited_notes': n_inherited, 'unresolved_notes': unresolved_by[place]})
            for kind, count in sorted(collections.Counter(e['kind'] for e in entries).items()):
                per_kind.append({'language': lang, 'volume': place[0], 'expose': place[1],
                                 'kind': kind, 'diplomatic_entries': 0, 'corrected_entries': count,
                                 'reading_entries': 0})
    totals = {}
    for lang in ('FR', 'EN'):
        entries = registers[lang]
        totals[lang] = {'variant_entries': len(entries),
                        'variant_blocks': len({e['group_id'] for e in entries}),
                        'inherited_notes': len(inherited) if lang == 'EN' else 0,
                        'unresolved_notes': len(unresolved),
                        'by_kind': dict(sorted(collections.Counter(e['kind'] for e in entries).items()))}
    audit = {'schema_version': 1,
             'count_unit': 'One uniquely identified individual before/after apparatus entry, not one source-log record or one variant block.',
             'totals': totals, 'by_expose': per_place, 'by_expose_and_kind': per_kind,
             'unresolved_note_locations': unresolved_locations,
             'storage_reallocations': reallocations,
             'validation': checks, 'input_sha256': INPUTS}
    # Refuse a mixed snapshot if another build rewrote an input while counting.
    assert all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h for p, h in INPUTS.items()), \
        'Inputs changed while counting; rerun after both language builds finish.'
    (RECORDS / 'APPARATUS_COUNTS.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
    with (RECORDS / 'APPARATUS_COUNTS.tsv').open('w', newline='') as f:
        writer = csv.DictWriter(f, list(per_kind[0]), delimiter='\t')
        writer.writeheader(); writer.writerows(per_kind)
    out = ['# Apparatus counts',
           '## Counting rule',
           'An **entry** is one unique identifier in `FR_APPARATUS.json` or `EN_APPARATUS.json`, '
           'with its individual printed and corrected readings. A **variant block** is one '
           'distinct `group_id` in that register; one marked passage can contain several entries. '
           'Counts of source-log records, alignment operations, or source issues are different quantities and are not substituted for entry counts.',
           'The classification below reproduces the recorded `kind` field. Some kinds describe the '
           'origin of a correction (for example `misprint_pass`) rather than its linguistic or '
           'mathematical content; this report does not silently reclassify them.',
           '## Totals by language and reader form']
    rows = []
    for lang in ('FR', 'EN'):
        for form, description in [('diplomatic', 'Diplomatic'), ('corrected_apparatus', 'Corrected with apparatus'), ('reading', 'Plain reading')]:
            z = checks[lang]['forms'][form]
            rows.append([lang, description, z['visible_variant_entries'],
                         totals[lang]['variant_blocks'] if form == 'corrected_apparatus' else 0,
                         z['visible_inherited_notes'], z['visible_unresolved_notes']])
    out.append(table(['Language', 'Reader form', 'Variant entries', 'Marked blocks', 'Inherited editorial notes', 'Retained/unresolved notes'], rows))
    out += ['Zero means no visible critical-apparatus entry or editorial note in that form. '
            'The single-file TeX necessarily retains the inactive alternatives. The report checks '
            'that every numbered apparatus target and editorial note lies in a corrected-form-only '
            'conditional, that each reader selects the stated form, and that each file is exactly '
            'the corresponding master with that selector changed. This is a source-level visibility '
            'audit; PDF compilation and page-level inspection are recorded separately.',
            '## Counts by exposé',
            'The two zero columns are included explicitly. The final two note columns are separate '
            'from the variant entries and are visible only in the corrected-apparatus form.']
    for lang in ('FR', 'EN'):
        out.append('### ' + lang)
        out.append(table(['Volume / exposé', 'Diplomatic', 'Corrected', 'Reading', 'Blocks', 'Inherited notes', 'Unresolved notes'],
                         [[label((a['volume'], a['expose'])), a['diplomatic_entries'], a['corrected_entries'],
                           a['reading_entries'], a['variant_blocks'], a['inherited_notes'], a['unresolved_notes']]
                          for a in per_place if a['language'] == lang]))
    out += ['Exposé XIII is assigned to XIII, including its single source folio 82, even though '
            'that text is stored in the Exposé XII source file. Publisher-catalogue variants on '
            'folios 525–527 of volume I are assigned to Catalogue in both languages, including '
            'those stored under IX in the French source register. Exposés III–V have no separately '
            'written text in these sources and therefore are not invented as empty source components. '
            'A zero for a supplied component means it has no registered variant, not that its text is missing.',
            '## Recorded kinds by exposé and form',
            'Only nonzero corrected-form kind combinations are listed; the diplomatic and reading '
            'counts remain explicitly zero. The complete machine-readable table is `APPARATUS_COUNTS.tsv`.']
    for lang in ('FR', 'EN'):
        out.append('### ' + lang)
        out.append(table(['Volume / exposé', 'Recorded kind', 'Diplomatic', 'Corrected', 'Reading'],
                         [[label((a['volume'], a['expose'])), a['kind'], 0, a['corrected_entries'], 0]
                          for a in per_kind if a['language'] == lang]))
    out += ['## Separate editorial notes',
            'Inherited English editorial notes preserve the release’s existing editorial explanations. '
            'They are not authorial footnotes and are not additional before/after variants. The retained '
            'or unresolved notes are the explicitly selected questions in `editorial_decisions.json`; '
            'each is counted once in each language, even when its stated scope includes several folios. '
            'Its first explicit folio determines the exposé subtotal.',
            table(['Identifier', 'Volume / exposé', 'Source folio / scope', 'Recorded status'],
                  [[n['id'], label((n['volume'], n['expose'])), n['page'], n['status']] for n in unresolved_locations]),
            'Authorial notes, references, bibliography entries, and the publisher catalogue are not '
            'critical-apparatus entries and are outside these counts.',
            '## Reproduction and validation',
            'Run `python build/edition_report.py` after rebuilding both language editions. The script '
            'reads the final registers, masters, reader selectors, page-marker table, and editorial-note '
            'registers. It verifies unique entry identifiers, nonidentical readings, one master target '
            'per entry, corrected-only guards, exact master-to-reader projections, and a stable input '
            'snapshot. `APPARATUS_COUNTS.json` records every subtotal, these validation results, and '
            'SHA-256 hashes of the exact inputs used. The report must be rerun if a source register or '
            'reader is rebuilt.']
    (RECORDS / 'APPARATUS_COUNTS.md').write_text('\n\n'.join(out) + '\n')
    print(json.dumps({'totals': totals, 'validation_passed': True}, ensure_ascii=False))


if __name__ == '__main__':
    run()
