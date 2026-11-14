#!/usr/bin/env python3
"""Verify the closed terminology packet; never rewrite edition sources."""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, re

from lexical_inventory import pages, prose_view, read, MATH
from finalize_glossary import key, page_name

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text())


def put(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    inputs = load('INPUT_MANIFEST.json')['files']
    inputs += load('SUPPLEMENTAL_INPUT_MANIFEST.json')
    inputs += load('FINAL_MACRO_INPUT_MANIFEST.json')
    for row in inputs:
        data = (ROOT / row['snapshot']).read_bytes()
        assert digest(data) == row['sha256'], row['snapshot']
        assert len(data) == row['bytes'], row['snapshot']

    catalog = json.loads(read('review/english/aggregate/INPUT_CATALOG.json'))
    paths = ['review/english/GLOSSARY_SGA6_REVIEWED_001_296.tsv',
             'review/english/GLOSSARY_SGA6_CANDIDATES.tsv']
    paths += [str(Path(p['directory']) / 'terms.tsv') for p in catalog['packets']]
    paths += [str(p.relative_to(HERE / 'input_snapshots'))
              for p in sorted((HERE / 'input_snapshots/en/glossaries').glob('*.tsv'))]
    source_rows = set()
    source_counts = {}
    for relative in paths:
        rows = list(csv.DictReader((HERE / 'input_snapshots' / relative).open(), delimiter='\t'))
        source_counts[relative] = len(rows)
        source_rows.update(f'{relative}#{i}' for i in range(2, len(rows) + 2))
    dispositions = load('LEXICON_DISPOSITIONS.json')
    decided_sources = {s for row in dispositions for s in row['source_rows']}
    assert not source_rows - decided_sources, sorted(source_rows - decided_sources)
    manual = load('MANUAL_LEXICON.json')
    manual_sources = {f'review/english/terminology_final/MANUAL_LEXICON.json#{i}'
                      for i in range(1, len(manual) + 1)}
    assert manual_sources <= decided_sources

    audit = load('GLOSSARY_AUDIT.json')
    glossary = list(csv.DictReader((HERE / 'GLOSSARY_SGA6_FR_EN.tsv').open(), delimiter='\t'))
    evidence = load('GLOSSARY_ATTESTATIONS.json')
    indexes = load('PRINTED_INDEX_PAIRS.json')
    assert len(glossary) == len(evidence) == audit['glossary_rows']
    assert len({row['id'] for row in glossary}) == len(glossary)
    keys = [key(row['french_term_or_notation'], row['english_rendering'],
                row['kind'] not in ['lexical_phrase', 'reviewed_phrase_with_intervening_math'])
            for row in glossary]
    assert len(set(keys)) == len(keys)
    corpus = load('SEARCH_CORPUS.json')
    assert len(corpus) == audit['source_leaf_pairs'] == 720
    order = {p['page']: p['order'] for p in corpus}
    by_id = {row['id']: row for row in evidence}
    for row in glossary:
        ev = by_id[row['id']]
        assert int(row['count']) == ev['count'] > 0, row['id']
        assert row['french_term_or_notation'] == ev['French']
        assert row['english_rendering'] == ev['English']
        loci = row['source_loci'].split('; ')
        assert all(p in order for p in loci)
        assert loci == sorted(set(loci), key=lambda p: order[p])
        assert row['first_place'] == page_name(loci[0]), row['id']
        assert int(row['paired_index_rows']) == len(ev['index_rows'])
        assert not re.search(r'\d(?:em|pt)', row['french_term_or_notation'])
        assert not row['french_term_or_notation'].startswith('-'), row['id']
        if row['kind'] == 'exact_printed_index_label':
            assert ev['count'] == len(ev['index_rows'])
        else:
            assert ev['count'] == sum(h['English_count'] for h in ev['paired_page_attestations'])
    assigned = Counter(i for row in evidence for i in row['index_rows'])
    assert assigned == Counter(row['id'] for row in indexes)
    assert len(indexes) == audit['printed_index_rows'] == 234
    assert all(row['mathematical_units_identical'] for row in indexes)
    assert sum(row['repeated_label'] for row in indexes) == audit['source_index_ditto_rows'] == 2
    by_index = {row['id']: row for row in indexes}
    for row in indexes:
        if row['repeated_label']:
            source = by_index[row['repeated_label_source']]
            assert row['French_resolved_label'] == source['French_resolved_label']
            assert row['English_resolved_label'] == source['English_resolved_label']

    cross = list(csv.DictReader((HERE / 'CROSS_VOLUME_TERMS.tsv').open(), delimiter='\t'))
    assert len(cross) == audit['cross_volume_difference_rows']
    assert (HERE / 'CROSS_VOLUME_TERMS.tsv').read_bytes() == (HERE / 'CROSS_VOLUME_DECISIONS.tsv').read_bytes()
    assert len(load('MULTIPLE_RENDERING_DECISIONS.json')) == audit['admitted_multiple_rendering_groups']
    assert len(load('REFERENCE_MATH_LABELS_AUDIT.json')) == audit['complete_reference_math_label_input_rows']
    expansions = load('NOTATION_EXPANSION_CHOICES.json')
    assert {r['token']: r['count'] for r in expansions} == {
        r'\GL': 13, r'\red': 20, r'\longg': 2, r'\Zell': 14, r'\Qell': 5, r'\naif': 4}
    assert [(r['page'], r['count']) for r in load('LITERAL_NOTATION_CHOICES.json')] == [(545, 3), (597, 1)]

    patches = [json.loads(line) for line in (HERE / 'EN_TERMINOLOGY_PATCHES.jsonl').read_text().splitlines()]
    assert len(patches) == audit['English_terminology_patches'] == 2
    for row in patches:
        assert [m.group() for m in MATH.finditer(row['old'])] == [m.group() for m in MATH.finditer(row['new'])]
    live_comparison = []
    for language, relative in [('French', 'build/FR_current_revised.tex'),
                               ('English', 'review/english/aggregate/SGA6_EN_raw_current.tex')]:
        data = (ROOT / relative).read_bytes()
        parsed = pages(data.decode())
        assert list(parsed) == [p['page'] for p in corpus]
        changed = [p['page'] for p in corpus if prose_view(parsed[p['page']]['text']) != p[language + '_view']]
        assert not changed, (language, changed)
        live_comparison.append(dict(language=language, path=relative, sha256=digest(data),
                                    leaves_compared=len(parsed), changed=changed))
    put('FINAL_LIVE_SEARCH_VIEW_COMPARISON.json', live_comparison)
    live_english = (ROOT / 'review/english/aggregate/SGA6_EN_raw_current.tex').read_text()
    for row in patches:
        start = live_english.index(row['scope_start'])
        end = live_english.index(row['scope_end'], start)
        scope = live_english[start:end]
        assert scope.count(row['new']) == row['expected_count']
        assert row['old'] not in scope

    # The dedicated published records use portable source references only.
    private = re.compile(r'(?:[A-Z]:\\(?:Users|work|home)\\|/(?:workspace/scratch|home/agent|root/\.codex)/[^\s]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})')
    privacy_checked = []
    for name in ['GLOSSARY_SGA6_FR_EN.tsv', 'CROSS_VOLUME_TERMS.tsv',
                 'GLOSSARY_INCONSISTENCIES.md', 'EN_TERMINOLOGY_PATCHES.jsonl',
                 'GLOSSARY_AUDIT.json', 'TERMINOLOGY_DECISIONS.json']:
        assert not private.search((HERE / name).read_text()), name
        privacy_checked.append(name)
    report = dict(passed=True, input_manifest_file_records_verified=len(inputs),
                  distinct_snapshot_files=len({r['snapshot'] for r in inputs}),
                  TSV_input_rows_with_explicit_dispositions=len(source_rows),
                  TSV_input_row_counts=source_counts, manual_lexicon_rows_with_dispositions=len(manual),
                  complete_math_label_rows_separately_tested=audit['complete_reference_math_label_input_rows'],
                  glossary_rows=len(glossary), distinct_French_headword_keys=audit['distinct_French_headword_keys'],
                  printed_index_rows_assigned_once=len(indexes), repeated_index_labels_resolved=2,
                  multiple_rendering_groups=audit['admitted_multiple_rendering_groups'],
                  cross_volume_difference_rows=len(cross), English_terminology_patches_applied=2,
                  macro_invocation_counts={r['token']:r['count'] for r in expansions},
                  current_live_edition_search_views=live_comparison,
                  privacy_checked_outputs=privacy_checked, shared_edition_sources_changed=False,
                  limitations=audit['count_definition'] + ' ' + audit['completeness'])
    put('FINAL_VERIFICATION.json', report)
    print(json.dumps({k:report[k] for k in ['passed','TSV_input_rows_with_explicit_dispositions',
                                         'glossary_rows','printed_index_rows_assigned_once',
                                         'cross_volume_difference_rows']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
