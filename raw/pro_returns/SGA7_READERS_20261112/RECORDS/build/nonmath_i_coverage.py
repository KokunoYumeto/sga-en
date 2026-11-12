"""Public coverage report for the bounded Volume-I nonformula source audit."""
import difflib
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
import french

ROOT = Path(__file__).resolve().parents[1]


def make_report(fr, variants, body_patches, coverage):
    rows = [r for r in fr if r['volume'] == '7I']
    final_components = {(c['volume'], c['component']): c for c in json.loads((ROOT / 'work/en_final_components.json').read_text())}
    final_exposes = {c['expose']: c for c in json.loads((ROOT / 'work/en_variant_data.json').read_text()) if c['volume'] == '7I'}
    frdata = [c for c in json.loads((ROOT / 'work/fr_variant_data.json').read_text()) if c['volume'] == '7I']
    groups = {}
    for c in frdata:
        if c['expose'] == 'VI':
            continue
        da, ca = french.paragraphs(c['diplomatic']), french.paragraphs(c['corrected'])
        n = 0
        for tag, i, j, k, l in difflib.SequenceMatcher(None, da, ca, autojunk=False).get_opcodes():
            if tag == 'equal':
                continue
            n += 1
            groups[f'F7I-{c["expose"]}-{n:03d}'] = (''.join(da[i:j]), ''.join(ca[k:l]))

    already = '''F7I-I-020.1
F7I-VII-078.1
F7I-VIII-008.2
F7I-VIII-036.3
F7I-VIII-047.2
F7I-IX-011.1
F7I-IX-030.1 F7I-IX-030.2
F7I-IX-073.4 F7I-IX-073.5 F7I-IX-073.6 F7I-IX-073.7
F7I-IX-077.1
F7I-IX-085.1
F7I-IX-086.1 F7I-IX-086.2 F7I-IX-086.3
F7I-IX-115.1
F7I-IX-123.1 F7I-IX-123.2
F7I-IX-139.1
F7I-IX-143.1
F7I-IX-147.1
F7I-IX-151.1 F7I-IX-151.2
F7I-IX-152.1'''.split()
    for fid in already:
        assert any(r['id'] == fid for r in rows), fid
        coverage.setdefault(fid, ('already_covered_by_final_English_reference_variant', 'final English source/port reconstruction',
            'The final English body already preserves the two reference or equation-label readings. This source item was checked independently of whether it carries an ADOPT or mapped correction identifier.'))
    for fid in ['F7I-VII-037.1', 'F7I-VII-037.2']:
        coverage[fid] = ('mathematical_or_formula_layout_not_reaudited', 'completed formula/source reconstruction',
            'The source writes P and Q outside the neighbouring TeX math delimiters in P times Q/Q times P. These are mathematical factors, not French words or alphabetic assertion references.')
    for fid in ['F7I-I-025.3']:
        coverage[fid] = ('already_covered_by_final_English_mathematical_prose', '7I:32',
            'Final corrected English has self-intersection $-2$; diplomatic English has self-intersection two, exactly preserving the printed mathematical assertion.')
    for suffix in [3,4,5,10,12]:
        coverage[f'F7I-VII-056.{suffix}'] = ('already_covered_by_explicit_prose_reconstruction', 'ED-EN-FORMULA-E014',
            'This lexical part of the construction of E0 lies in the previously reviewed full-paragraph reconstruction, together with its homomorphisms and quotient description.')
    for fid, reason in {
        'F7I-VII-010.3': 'Printed biridifié is a misspelled French word, not the distinct valid term birigidifié. The clause explicitly specifies a single rigidification relative to e_P; English rigidified expresses that same clause in both readings.',
        'F7I-VIII-007.1': 'Only a missing space between VII and 1 changes; no distinct cross-reference target is introduced.',
        'F7I-VIII-011.4': 'French et/de is a prepositional transcription repair in the phrase identifying an object S of the topos T; it does not introduce a second mathematical object or a different English assertion.',
        'F7I-VIII-028.1': 'French noun/adjective repair isomorphisme/isomorphe; the English isomorphic construction has the same mathematical content.',
        'F7I-VIII-066.1': 'French directional-preposition repair in the syntax of a functor from one category to another. The two named categories and the functor are unchanged; no additional English mathematical claim is introduced.',
        'F7I-IX-010.1': 'French adjective/noun repair isomorphe/isomorphisme; the asserted isomorphism is unchanged.',
        'F7I-IX-044.1': 'The source repairs singular/plural agreement in the assertion that the set maps underlying the two morphisms are equal. Both English branches state the same equality.',
        'F7I-IX-044.2': 'The source repairs singular/plural agreement in the assertion that the set maps underlying the two morphisms are equal. Both English branches state the same equality.',
        'F7I-IX-044.3': 'French adjectival agreement in that same equality of underlying set maps; no distinct English proposition.',
        'F7I-IX-136.3': 'French où/ou accent repair inside the equivalent descriptions of a canonical isomorphism. The native English recasts the same equivalence as an equivalent compatible family; no separate reference, negation, or mathematical hypothesis is lost.',
    }.items():
        coverage.setdefault(fid, ('no_substantive_English_difference', None, reason))
    for fid in ['F7I-IX-061.1', 'F7I-IX-146.1']:
        coverage[fid] = ('already_covered_by_final_English_meaning_variant', 'exact source port',
            'The final paired bodies already preserve étale/connected for F prime(n), or generic/special fibre in the Néron universal property, respectively.')

    def n(s):
        return re.sub(r'\s+', ' ', s).strip()

    checks = []
    exceptions = []
    for r in variants + body_patches:
        c = final_components[(r['volume'], r['component'])]
        check = {'id': r['id'], 'component': r['component'],
                 'corrected_reading_present': n(r['corrected']) in n(c['corrected']),
                 'printed_reading_present': n(r['printed']) in n(c['diplomatic']),
                 'comparison': 'exact TeX after collapsing whitespace only',
                 'french_apparatus_ids': r['french_apparatus_ids']}
        checks.append(check)
        if not check['corrected_reading_present'] or not check['printed_reading_present']:
            exceptions.append(check)

    # Explicit verification of the previously covered numeric/semantic candidates.
    verified_existing = []
    def comp(prefix):
        return next(c for (v,k), c in final_components.items() if v == '7I' and k.startswith('components/' + prefix + '_'))
    def present(prefix, corrected, printed, fid, absence=False):
        c = comp(prefix)
        okc = n(corrected) in n(c['corrected'])
        okd = (n(printed) not in n(c['diplomatic'])) if absence else (n(printed) in n(c['diplomatic']))
        r = {'french_apparatus_id': fid, 'component': c['component'], 'corrected': corrected, 'printed': printed,
             'corrected_present': okc, 'printed_present': okd, 'printed_condition': 'absent' if absence else 'present'}
        verified_existing.append(r)
        if not (okc and okd):
            exceptions.append(r)
    present('06', 'self-intersection $-2$', 'self-intersection two', 'F7I-I-025.3')
    present('136', 'unipotent (SGA 3, XVII, 1.1),', 'unipotent (SGA 3, VII, 1.1,', 'F7I-IX-030.2')
    present('173', r'\tag{\SGARefTarget{sga7.sga7i.eix.n12-3-8}{12.3.8}}',
            r'\notag\SGARefAliasTarget{sga7.sga7i.eix.n12-3-8}', 'F7I-IX-151.1')
    present('146', "with $F'(n)$ \\'{e}tale", "with $F'(n)$ connected", 'F7I-IX-061.1')
    present('172', 'in terms of its generic fibre', 'in terms of its special fibre', 'F7I-IX-146.1')

    # Keep exact applied atoms as evidence. The explicitly reviewed IX 347 atom
    # is bound by its French apparatus ID and English clause/offset: later
    # historical-attribution corrections must not break that reading identity.
    # Other already-reviewed candidates retain their historical-ID links.
    existing_evidence = {}
    for fid in already:
        row = next(r for r in rows if r['id'] == fid)
        refs = set(re.findall(r'7I:\d+', row['source']))
        matched = []
        stable_context = 'unipotent (SGA 3, XVII, 1.1),'
        if fid == 'F7I-IX-030.2':
            assert (row['expose'], row['page'], row['before'], row['after']) == ('IX', '347', 'VII', 'XVII')
            bound = comp('136')
            assert bound['text'].count(stable_context) == 1
            bound_start = bound['text'].index(stable_context) + len('unipotent (SGA 3, ')
        for (v,k), c in final_components.items():
            if v != '7I':
                continue
            for op in c['variant_sources']:
                found = set(re.findall(r'7I:\d+', op.get('source', '')))
                stable_match = (fid == 'F7I-IX-030.2' and k == bound['component']
                                and op.get('start') == bound_start
                                and op.get('end') == bound_start + len('XVII')
                                and (op.get('corrected'), op.get('printed'), str(op.get('folio'))) == ('XVII', 'VII', '347')
                                and 'ED-EN-PORT-WITNESS-7I-C1035' in op.get('source', ''))
                if stable_match or (fid != 'F7I-IX-030.2' and refs & found):
                    evidence = {'component': k, 'start': op.get('start'), 'end': op.get('end'),
                                'corrected': op.get('corrected'), 'printed': op.get('printed'),
                                'source': op.get('source')}
                    if stable_match:
                        evidence.update(french_apparatus_id=fid,
                                        french_source=row['source'], french_source_ref=row['source_ref'],
                                        exact_native_context=stable_context,
                                        match_basis='Exact reviewed English component, native-clause offset, atom readings and folio, bound to the unchanged French apparatus ID; historical citation IDs are not used as reading identity.')
                    matched.append(evidence)
        existing_evidence[fid] = matched
        if not matched and fid not in ['F7I-IX-151.1', 'F7I-IX-151.2']:
            exceptions.append({'french_apparatus_id': fid, 'problem': 'No final applied source atom found for previously covered reference.'})

    screened = []
    pending_references = []
    math_count = 0
    for row in rows:
        if row['expose'] == 'VI':
            status, owner, reason = ('covered_by_original_English_source_identity', 'ED-VI-AUTHOR',
                'Both English VI branches are the exact source-original English projections used by the French reader; no translation transfer is involved.')
            math_flags = None
        else:
            d,c = groups[row['group_id']]
            assert d[row['a0']:row['a1']] == row['before'] and c[row['b0']:row['b1']] == row['after'], row['id']
            math_flags = {'printed_in_math': french.math_at(d,row['a0']), 'corrected_in_math': french.math_at(c,row['b0'])}
            math_count += int(any(math_flags.values()))
            if row['id'] in coverage:
                status, owner, reason = coverage[row['id']]
            elif row['page'].isdigit() and int(row['page']) >= 525:
                status, owner, reason = ('already_covered_in_preserved_publisher_catalogue', 'English Catalogue component',
                    'The supplied publisher catalogue is included in both English forms with its source-recorded spelling variants; it is original multilingual matter, not newly translated prose.')
            elif any(math_flags.values()):
                status, owner, reason = ('mathematical_or_formula_layout_not_reaudited', None,
                    'The source token is inside a mathematical expression or display. It belongs to the completed formula/source reconstruction audits and is not re-reviewed in this bounded nonformula pass.')
            else:
                plain = re.sub(r'\\[A-Za-z]+|\\.', '', row['before']+row['after'])
                if re.search(r'[A-Za-zÀ-ÿ]{2,}', plain):
                    status, owner, reason = ('French_orthography_or_grammar_outside_substantive_scope', None,
                        'Context reviewed: French spelling, agreement, lexical joining, or grammatical syntax, without a changed mathematical hypothesis, negation, numbered reference, or substantive translated assertion. Exact French readings remain in the French apparatus.')
                else:
                    status, owner, reason = ('punctuation_spacing_or_TeX_layout_outside_substantive_scope', None,
                        'The changed span concerns punctuation, spacing, or TeX layout; the requested bounded pass excludes such changes.')
                if re.search(r'\d|\b[IVX]{2,}\b', row['before']+row['after']):
                    pending_references.append(row['id'])
        screened.append({'french_apparatus_id': row['id'], 'source': row['source'], 'source_ref': row['source_ref'],
                         'expose': row['expose'], 'page': row['page'], 'printed': row['before'], 'corrected': row['after'],
                         'status': status, 'covered_by': owner, 'reason': reason, 'source_math_context': math_flags,
                         'final_English_evidence': existing_evidence.get(row['id'], [])})
    assert not pending_references, pending_references
    vi = next(c for c in frdata if c['expose'] == 'VI')
    assert vi['corrected'] == final_exposes['VI']['corrected'] and vi['diplomatic'] == final_exposes['VI']['diplomatic']
    inherited = [r for r in screened if 'ADOPT-' in r['source']]
    report = {
        'scope': 'All 1,250 Volume-I French apparatus atoms, including mapped corrections and ADOPT source selections. Numeric/cross-reference and meaning-changing prose are reviewed; original-English VI and previously audited mathematics are separately identified.',
        'all_volume_i_apparatus_entries_screened': len(screened),
        'source_selection_entries_screened': len(inherited),
        'non_VI_apparatus_entries_screened': len(screened)-390,
        'source_math_context_entries': math_count,
        'source_nonmath_context_entries': len(screened)-390-math_count,
        'status_counts': dict(Counter(r['status'] for r in screened)),
        'source_selection_status_counts': dict(Counter(r['status'] for r in inherited)),
        'exact_diplomatic_operation_decisions': len(variants),
        'paired_corrected_body_repair_decisions': len(body_patches),
        'reader_operation_pair_checks': len(checks),
        'reader_individual_reading_checks': len(checks)*2,
        'remaining_missing_reference_decisions': pending_references,
        'exceptions': exceptions,
        'all_requested_reference_and_meaning_candidates_decided': not pending_references and not exceptions,
        'introduction_five_entries': [r for r in screened if r['expose'] == 'INTRO'],
        'coverage': screened, 'operations': variants, 'paired_body_repairs': body_patches,
        'final_projection_checks': checks, 'previously_covered_explicit_projection_checks': verified_existing,
        'final_component_snapshot_sha256': hashlib.sha256((ROOT / 'work/en_final_components.json').read_bytes()).hexdigest(),
        'reports_only_supported': True,
        'reproduction': 'python build/audit_en_nonmath_i.py generates decisions before the English build; python build/audit_en_nonmath_i.py --reports-only refreshes this report after the English build without writing reader inputs.'
    }
    return report
