#!/usr/bin/env python3
"""Verify the complete glossary, its additions, and inherited-note relocation.

No reader or source body is changed. Audit outputs are written in this
contribution directory; all provenance paths in reports are archive-relative.
"""
from __future__ import annotations
import ast, bisect, collections, csv, hashlib, json, re
from pathlib import Path
import build_glossary as g
from editorial_note_relocation import DECISION, EVIDENCE, NOTE_PREFIX, locate_note, mask_editorial_note, relocate_en_note

OUT = Path(__file__).parent
DEC = OUT.parent / 'decisions'
WORK = OUT.parents[1]
PREP = WORK / 'build' / 'prepared'
ROOT = WORK.parent
EN_SOURCE = OUT / 'EN_corrected_flat.tex'
FR_SOURCE = WORK / 'sources/SGA5_FR/fr/sga5/current/s5.tex'


def digest(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def assignment_literal(path, name):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError((path.name, name))


def group(s, start):
    while s[start].isspace():
        start += 1
    assert s[start] == '{'
    depth, i = 1, start + 1
    while depth:
        assert i < len(s)
        if s[i] == '\\':
            m = re.match(r'\\(?:[A-Za-z@]+|.)', s[i:], re.S)
            assert m
            i += m.end()
            continue
        depth += (s[i] == '{') - (s[i] == '}')
        i += 1
    return s[start + 1:i - 1], i


def indexes(s):
    result = []
    for m in re.finditer(r'^\\sgaindexentry(?=\{)', s, re.M):
        term, end = group(s, m.end())
        refs, end = group(s, end)
        result.append({'term': term, 'references': refs, 'start': m.start(), 'end': end})
    return result


def main():
    en, fr = EN_SOURCE.read_text(), FR_SOURCE.read_text()
    initial_hashes = {'EN_corrected_flat': digest(en),
                      'EN_diplomatic_flat': digest((OUT / 'EN_diplomatic_flat.tex').read_text()),
                      'EN_common_corrections': digest((OUT / 'EN_common_corrections.json').read_text())}
    rows = list(csv.DictReader((OUT / 'GLOSSARY_SGA5_FR_EN.tsv').open(), delimiter='\t'))
    by_id = {r['source id']: r for r in rows}
    assert len(by_id) == len(rows)
    families = json.loads((OUT / 'GLOSSARY_FAMILIES.json').read_text())
    occurrences = json.loads((OUT / 'GLOSSARY_OCCURRENCES.json').read_text())
    occurrence_by_id = {r['id']: r for r in occurrences}
    summary = json.loads((OUT / 'GLOSSARY_SUMMARY.json').read_text())
    pairs = json.loads((DEC / 'index_glossary_pairs.json').read_text())
    f_index, e_index = indexes(fr), indexes(en)
    assert len(pairs) == len(f_index) == len(e_index) == 108
    index_audit = []
    for n, (record, f, e) in enumerate(zip(pairs, f_index, e_index), 1):
        rid = f'INDEX-{n:03d}'
        row = by_id[rid]
        assert record['id'] == rid
        assert row['French term or notation'] == record['French_term_or_notation'] == f['term']
        assert row['English rendering'] == record['English_rendering'] == e['term']
        assert row['references'] == record['English_references'] == e['references']
        assert record['French_references'] == f['references']
        compare = lambda s: s.replace('déf', 'def').replace(r'n\textsuperscript{o}', 'no.').replace('~', ' ')
        assert compare(f['references']) == compare(e['references'])
        index_audit.append({'id': rid, 'kind': record['kind'], 'French_offset': f['start'],
                            'English_offset': e['start'], 'exact_labels_and_references_present': True,
                            'paired_reference_comparison_passed': True})

    ea = en.index(r'\phantomsection\addcontentsline{toc}{section}{Exposé I ---')
    eb = en.index(r'\section*{Terminological Index}')
    pages = g.p.getpages(fr)
    fa, fb = pages[1]['start'], pages[481]['start']
    ev, ep = g.view(mask_editorial_note(en), ea, eb)
    old_ev, old_ep = g.view(en, ea, eb)
    fv, fp = g.view(fr, fa, fb)
    curated = assignment_literal(DEC / 'curate_terminology.py', 'inventory')
    inventory = [{'id': f'BODY-TERM-{n:03d}', 'French_term': f.split('|')[0],
                  'French_search_forms': f.split('|'), 'English_search_forms': e.split('|')}
                 for n, (f, e) in enumerate(curated, 1)]
    for n, (term, fs, es) in enumerate(assignment_literal(OUT / 'build_glossary.py', 'additions'), 1):
        inventory.append({'id': f'BODY-EXTRA-{n:03d}', 'French_term': term,
                          'French_search_forms': fs, 'English_search_forms': es})
    additions = json.loads((OUT / 'GLOSSARY_ADDITIONS.json').read_text())
    inventory.extend(additions)
    coordinate = json.loads((OUT / 'GLOSSARY_COORDINATED_CATEGORY_EVIDENCE.json').read_text())
    inventory = [coordinate if r['id'] == coordinate['id'] else r for r in inventory]
    for r in inventory:
        if r['French_term'] == 'produit fibré':
            r['English_search_forms'] += ['fibred product', 'fibred products', 'fibre products']
        if r['French_term'] == 'borné à gauche':
            r['English_search_forms'] += ['left-bounded', 'bounded on the left']
        if r['French_term'] == 'fonction centrale':
            r['English_search_forms'] += ['class function', 'class functions']
        if r['French_term'] == 'catégorie fibrée':
            r['French_search_forms'] += ['catégories fibrées et cofibrées', 'catégories fibrées ou cofibrées', 'catégorie fibrée et cofibrée']
            r['English_search_forms'] += ['fibred and cofibred category', 'fibred and cofibred categories', 'fibred or cofibred categories']
    family_by_id = {r['id']: r for r in families}
    excluded = []
    form_audit = []
    note_count_effects = []
    expected_body_ids = []
    for candidate in inventory:
        f_hits = sorted(set(x for form in candidate['French_search_forms'] for x in g.hits(fv, fp, form)))
        forms = []
        counts = []
        for form in dict.fromkeys(candidate['English_search_forms']):
            hits = g.hits(ev, ep, form)
            old_hits = g.hits(old_ev, old_ep, form)
            if old_hits != hits:
                note_count_effects.append({'family_id': candidate['id'], 'form': form,
                                          'before_editorial_exclusion': len(old_hits), 'after_editorial_exclusion': len(hits),
                                          'excluded_offsets': sorted(set(x[0] for x in old_hits) - set(x[0] for x in hits))})
            counts.append({'form': form, 'count': len(hits)})
            if hits:
                forms.append((form, hits))
        if not f_hits or not forms:
            assert candidate['id'] not in family_by_id
            excluded.append({'id': candidate['id'], 'French_term': candidate['French_term'],
                             'French_forms': [{'form': f, 'count': len(g.hits(fv, fp, f))} for f in candidate['French_search_forms']],
                             'English_forms': counts,
                             'reason': 'All specified literal phrase forms have zero body occurrences in both corpora.'})
            assert not f_hits and not forms
            continue
        family = family_by_id[candidate['id']]
        assert family['French_count'] == len(f_hits)
        assert len(family['English_forms']) == len(forms)
        for n, ((form, hits), existing) in enumerate(zip(forms, family['English_forms']), 1):
            rid = candidate['id'] + '-' + str(n).zfill(2)
            expected_body_ids.append(rid)
            row, oc = by_id[rid], occurrence_by_id[rid]
            assert row['French term or notation'] == candidate['French_term']
            assert row['English rendering'] == existing['form'] == oc['English_rendering'] == form
            assert int(row['count']) == existing['count'] == oc['count'] == len(hits)
            assert int(row['French count']) == len(f_hits)
            assert oc['positions_corrected'] == [x[0] for x in hits]
            assert existing['first_offset'] == hits[0][0]
            assert existing['first_place'] == row['first place']
            form_audit.append({'id': rid, 'count': len(hits), 'first_offset': hits[0][0],
                               'all_occurrence_offsets_verified': True, 'French_count': len(f_hits)})
    assert len(excluded) == 10
    assert set(expected_body_ids) == {r['source id'] for r in rows if r['kind'] == 'body term'}
    assert len(expected_body_ids) == len(occurrences) == 212
    for pair in pairs:
        row = by_id[pair['id']]
        assert int(row['count']) == en[ea:].count(pair['English_rendering'])
        assert int(row['French count']) == fr[fa:].count(pair['French_term_or_notation'])
    prose = (OUT / 'GLOSSARY_INCONSISTENCIES.md').read_text()
    multi = [f for f in families if len(f['English_forms']) > 1]
    for family in multi:
        assert '| ' + family['French_term'].replace('|', r'\|') + ' |' in prose
        for form in family['English_forms']:
            assert form['form'] + ' (' + str(form['count']) + ')' in prose
    assert len(multi) == 65
    for r in additions + [coordinate]:
        evidence = r['paired_evidence']
        for language, source in [('French', fr), ('English', en)]:
            context = evidence[language + '_context']
            pos = evidence[language + '_offset']
            assert context in source and pos >= 0
    common = json.loads((OUT / 'EN_common_corrections.json').read_text())
    repairs = [r for r in common if r['id'].startswith('GLOSSARY-')]
    assert len(common) == 398 and len(repairs) == 5 and sum(r['applied_count'] for r in repairs) == 13
    for r in repairs:
        assert r['id'] in prose
        assert not g.hits(ev, ep, r['old']), (r['id'], 'old spelling still occurs')
    dispositions = json.loads((DEC / 'SOL_glossary_variants.json').read_text())
    assert len(dispositions) == 8 and all(r['source_id'] in prose for r in dispositions)

    # Verify the exact wrapper-level extraction against its archived source.
    prepared = (PREP / 'EN_annotated_body.tex').read_text()
    extracted_body, appendix, extraction = relocate_en_note(prepared)
    stored_ledger = json.loads((PREP / 'EN_wrapper_editorial_extractions.json').read_text())
    assert stored_ledger == [extraction]
    evidence_text = (WORK / 'sources/SGA5_EN' / EVIDENCE).read_text()
    assert extraction['before'] in evidence_text
    assert extraction['payload'] in appendix
    note_inventory = json.loads((DEC / 'unresolved_notes_inventory.json').read_text())
    shared_ids = note_inventory['included_ids']
    decisions = {r['item']: r for r in json.loads((DEC / 'decisions.json').read_text())}
    assert len(shared_ids) == 30 and DECISION in decisions
    assert all('needs the scan' in decisions[i]['decision'] for i in shared_ids + [DECISION])
    note_audit = []
    reader_bodies = []
    for language, names in [
        ('EN', ['SGA5_EN_diplomatic', 'SGA5_EN_corrected_apparatus', 'SGA5_EN_reading', 'SGA5_EN_master_annotated']),
        ('FR', ['SGA5_FR_diplomatique', 'SGA5_FR_corrige_apparat', 'SGA5_FR_texte_de_lecture', 'SGA5_FR_master_annotated']),
    ]:
        fragment = (DEC / f'unresolved_notes_{language}.tex').read_text()
        extracted_ids = re.findall(r'\\textbf\{((?:SOL-EN-\d+|REVIEW-5-01|GLOBAL-[A-Za-z0-9-]+)) \(', fragment)
        assert extracted_ids == shared_ids
        for name in names:
            text = (ROOT / 'deliverables' / language / (name + '.tex')).read_text()
            assert text.count(fragment) == 1
            body = text.split('% SGA5_BODY_START\n', 1)[1].split('\n% SGA5_BODY_END', 1)[0]
            body_end = text.index('% SGA5_BODY_END')
            gate = text.index(r'\ifnum\SGAform=1\relax\clearpage', body_end)
            note_start = text.index(fragment)
            final_gate_end = text.rfind(r'\fi')
            assert gate < note_start < final_gate_end
            if language == 'EN':
                assert NOTE_PREFIX not in body and r'\emph{Editorial note.}' not in body
                assert text.count(extraction['payload']) == 1
                assert text.count(appendix) == 1
                assert gate < text.index(appendix) < final_gate_end
                assert len(re.findall(r'\}\{((?:EN)-\d{4}|R98-\d{2})\}', body)) == 879
                assert len(re.findall(r'\\SGAFolio\{\d+\}', body)) == 793
                reader_bodies.append(body)
            else:
                assert DECISION not in text
            note_audit.append({'reader': name, 'shared_notes_exact': 30,
                               'inherited_English_note': language == 'EN',
                               'total_unresolved_notes': 31 if language == 'EN' else 30,
                               'notes_within_corrected_only_gate': True,
                               'shared_fragment_exact': True})
    assert all(s == reader_bodies[0] for s in reader_bodies)
    assert note_count_effects == [{'family_id': 'BODY-TERM-021', 'form': 'pullback',
                                  'before_editorial_exclusion': 1, 'after_editorial_exclusion': 0,
                                  'excluded_offsets': note_count_effects[0]['excluded_offsets']}]
    final_hashes = {'EN_corrected_flat': digest(EN_SOURCE.read_text()),
                    'EN_diplomatic_flat': digest((OUT / 'EN_diplomatic_flat.tex').read_text()),
                    'EN_common_corrections': digest((OUT / 'EN_common_corrections.json').read_text())}
    assert initial_hashes == final_hashes
    assert summary == {'rows': 320, 'body_term_families': 131, 'body_rendering_rows': 212,
                       'index_pairs': 108, 'multiple_form_families': 65,
                       'lexical_repair_operations': 5, 'lexical_replacements': 13}
    report = {
        'passed': True, 'final_counts': summary,
        'baseline_glossary_rows_audited': 303, 'baseline_body_families_audited': 117,
        'original_index_pairs_verified': 108, 'index_terminology_entries': 56, 'index_notation_entries': 52,
        'all_final_body_forms_recounted': 212, 'all_final_occurrence_offsets_verified': True,
        'all_multiple_form_families_listed_in_inconsistencies': 65,
        'new_exactly_paired_phrase_families': 13, 'recovered_coordinated_category_family': 1,
        'new_coordinated_renderings_in_existing_fibred_family': 3,
        'excluded_curated_candidates': excluded,
        'editorial_note_effect_on_glossary': note_count_effects,
        'plain_spelling_repair_operations': 5, 'plain_spelling_replacements': 13,
        'source_based_SOL_terminology_dispositions_documented': 8,
        'frozen_common_corrections_count': 398, 'frozen_sources_unchanged': True,
        'source_hashes': final_hashes,
        'reader_note_totals': {'FR': 30, 'EN': 31},
        'note_relocation_exact_and_reversible': True,
        'authorial_body_formulas_changed_in_this_audit': 0,
        'coverage_scope': 'All 108 supplied index pairs; all literal alternatives in the declared curated/extra/additional body phrase inventories. Counts measure those explicit phrase forms, with nested phrases separately counted; no claim of exhaustive enumeration of every possible mathematical term.'
    }
    dump('GLOSSARY_COVERAGE_AUDIT.json', report)
    dump('GLOSSARY_INDEX_COVERAGE_AUDIT.json', index_audit)
    dump('GLOSSARY_BODY_COVERAGE_AUDIT.json', form_audit)
    dump('READER_UNRESOLVED_NOTES_AUDIT.json', {'passed': True, 'decision': decisions[DECISION],
                                             'reader_checks': note_audit, 'extraction': extraction,
                                             'archived_original_footnote_exact': True,
                                             'source_bodies_and_398_operations_unchanged': True})
    lines = [
        '# Final glossary and unresolved-note coverage audit', '',
        '**Passed.** The final glossary has **320 rows**: **212 English body forms in 131 French term families**, plus all **108 paired index entries** (56 terminology and 52 notation). All 65 families with multiple observed English forms are listed in the inconsistencies report.', '',
        '## Coverage and additions', '',
        'The original 303-row inventory was checked completely. Every index label and reference was re-extracted from both source files and matched to its glossary row. Every final body-form count and occurrence offset was recounted in the declared search scope. Each first occurrence agrees with the recorded glossary position and anchor range.', '',
        'Thirteen additional phrase families have exact paired source contexts and shared section, object or formula identifiers in `GLOSSARY_ADDITIONS.json`. The formerly excluded cofibred-category family is recovered from the exact coordinated French phrases, with their actual English wording. Three coordinated forms are also added to the existing fibred-category family. These additions change the glossary only.', '',
        '| Excluded original candidate | French literal hits | English literal hits |',
        '|---|---:|---:|',
    ]
    for r in excluded:
        lines.append('| ' + r['French_term'] + ' | 0 | 0 |')
    lines += [
        '', 'All listed search forms, including their tested inflections, are retained in the JSON audit. These zero counts concern the stated literal phrases. The complete index pairs remain independently covered.', '',
        '## Corrections already applied', '',
        'All five earlier spelling operations and their 13 replacements remain documented and present. Their old literal spellings have zero occurrences in the final body counting scope. All eight source-based terminology/notation dispositions remain in the inconsistencies report. This final audit makes no new authorial wording, formula or notation change.', '',
        '## Editorial-note relocation and count scope', '',
        'The supplied ported English retained one English-only editorial footnote in Exposé I, 4.6, folio 43. The archive separately identifies its full text as SGA5-READER-PROSE-002. Its exact footnote is removed at the reader-wrapper stage and its entire payload is preserved in the corrected-only unresolved appendix under **EN-INHERITED-0046-P43**, with MISPRINTS_5:0054 and MISPRINTS_5:0055 as additional provenance. The extraction ledger reverses exactly, and all 879 variant calls and 793 folio markers remain in the same order.', '',
        'The sole counted body phrase affected by the relocation is **pullback**: one occurrence in that editorial footnote becomes zero in the authorial-body count. Its former glossary row is excluded, and no frozen source position is shifted in the search view. This explains the final total of 320 rows after the additions.', '',
        'The French readers carry the shared **30** unresolved notes. The English corrected apparatus carries those same 30 plus the separately preserved inherited note, for **31**. All source fragments occur exactly once and lie within the corrected-only apparatus gate; the inherited note is absent from every English reader body. The diplomatic and plain-reading forms suppress the apparatus by their form switch.', '',
        'The frozen corrected and diplomatic English files and all **398** common correction operations retain their hashes. The final output checks are recorded in `GLOSSARY_COVERAGE_AUDIT.json` and `READER_UNRESOLVED_NOTES_AUDIT.json`.', '',
    ]
    (OUT / 'GLOSSARY_COVERAGE_AUDIT.md').write_text('\n'.join(lines))
    print(json.dumps({'passed': True, 'rows': len(rows), 'families': len(families),
                      'body_forms': len(form_audit), 'index_pairs': len(index_audit),
                      'unresolved_notes': {'FR': 30, 'EN': 31}, 'frozen_sources_changed': False}))


if __name__ == '__main__':
    main()
