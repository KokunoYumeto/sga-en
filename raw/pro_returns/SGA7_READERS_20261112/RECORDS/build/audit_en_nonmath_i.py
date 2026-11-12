"""Bounded Volume-I source prose/reference coverage audit and exact variants.

The mathematical reconstruction has a separate audit. This pass screens all
1,250 Volume-I French apparatus entries, including mapped and inherited
corrections, and verifies the final English nonformula counterparts.
"""
import json
import sys
import hashlib
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS_ONLY = '--reports-only' in sys.argv or '--audit-only' in sys.argv
INPUT_FILES = [ROOT / 'work/en_nonmath_resolutions_editorial.json',
               *sorted((ROOT / 'work').glob('en_editorial_body_patch_nonmath_i_*.json'))]
INPUT_HASHES_BEFORE = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in INPUT_FILES if p.exists()} if REPORTS_ONLY else {}
fr = json.loads((ROOT / 'output/records/FR_APPARATUS.json').read_text())
inherited = [r for r in fr if r['volume'] == '7I' and 'ADOPT-' in r['source']]
components = {c['component']: c for c in json.loads((ROOT / 'work/en_components.json').read_text()) if c['volume'] == '7I'}
final = {c['expose']: c for c in json.loads((ROOT / 'work/en_variant_data.json').read_text()) if c['volume'] == '7I'}
variants = []
coverage = {}


def add(number, prefix, corrected, printed, page, ids, reason):
    matches = [c for k, c in components.items() if k.startswith('components/' + prefix + '_')]
    assert len(matches) == 1, prefix
    c = matches[0]
    assert c['text'].count(corrected) == 1, (prefix, corrected)
    start = c['text'].index(corrected)
    related = [r for r in fr if r['id'] in ids]
    assert len(related) == len(ids), (ids, related)
    sources = sorted({r['source'] for r in related})
    source_refs = sorted({r['source_ref'] for r in related})
    row = {'id': f'ED-EN-NONMATH-I-{number:03d}', 'status': 'variant', 'volume': '7I',
           'component': c['component'], 'start': start, 'corrected': corrected,
           'printed': printed, 'source': '; '.join(sources + source_refs), 'page': str(page),
           'reason': reason, 'french_apparatus_ids': ids,
           'french_readings': [{'id': r['id'], 'printed': r['before'], 'corrected': r['after'],
                                'printed_context': r['before_context'], 'corrected_context': r['after_context']} for r in related]}
    variants.append(row)
    for item in ids:
        if any(r['id'] == item for r in fr):
            coverage[item] = ('new_exact_diplomatic_reconstruction', row['id'], reason)


add(1, '02',
    r'of one of the types (\SGARefLink{sga7.sga7i.ei.n0-1-1}{0.1.1})--(\SGARefLink{sga7.sga7i.ei.n0-1-5}{0.1.5})',
    r'of one of the types (\SGARefLink{sga7.sga7i.ei.n0-1-1}{1.1.1})--(\SGARefLink{sga7.sga7i.ei.n0-1-5}{1.1.5})',
    6, ['F7I-I-007.1', 'F7I-I-007.2'],
    'Theorem I1.2 has the printed reference range 1.1.1–1.1.5, corrected to 0.1.1–0.1.5. Both English projections previously had the corrected numbers. Restore only the visible printed numbers; stable nonprinting link keys remain unchanged.')

add(2, '04',
    r'excellent regular strictly local ring} (\SGARefLink{sga7.sga7i.ei.n0-0-2}{0.0.2})',
    r'excellent regular strictly local ring} (\SGARefLink{sga7.sga7i.ei.n0-0-2}{0.2})',
    10, ['F7I-I-013.1'],
    'The purity conjecture I3.1 refers to 0.2 in print and 0.0.2 in current. The English corrected reference is retained; the printed reference is restored only in the diplomatic branch.')

add(3, '08',
    "S. Abhyankar, ``Local uniformization on algebraic surfaces over\nground fields of characteristic $p\\neq0$,'' \\emph{Ann. of Math.},\nvol. 63, no. 3, 1956, pp. 491--526.",
    "S. Abhyankar, ``Local uniformization of algebraic surfaces over\nground field of characteristic $p=0$,'' \\emph{Amer. J. of Math.},\nvol. 63, 1956.",
    31, [f'F7I-II-008.{i}' for i in range(1, 8)],
    'The final diplomatic bibliography has of, singular ground field, p=0, Amer. J. of Math., and no issue number or page range. Only p=0 had previously reached diplomatic English. Restore the complete attested bibliographical reading in one span; the corrected citation and native English citation formatting are retained.')

add(4, '94',
    'Taking the standard truncation of the derived tensor product, whose\nhomology objects are the $\\Tor_i(P,Q)$, one obtains from (\\SGARefLink{sga7.sga7i.eviii.n1-1-1}{1.1.1}) the\nfollowing infinite exact sequence:',
    'From (\\SGARefLink{sga7.sga7i.eviii.n1-1-1}{1.1.1}) one deduces the following infinite exact sequence,\ntaking into account that the homology objects of\n$P\\mathbin{\\overset{\\mathbb L}{\\otimes}}Q$ are the $\\Tor_i(P,Q)$,\nwhich vanish for $i\\geqslant1$:',
    220, [f'F7I-VIII-001.{i}' for i in range(1, 10)],
    'The printed justification before (1.1.3) claims vanishing of Tor_i for i≥1; the corrected source instead uses standard truncation. Both English projections previously retained the corrected explanation. Restore the complete printed assertion, including its false vanishing claim, only in the diplomatic branch. This is the source-recorded correction 7I:420, not a new mathematical emendation.')

add(5, '113',
    r'under (\SGARefLink{sga7.sga7i.eviii.n4-14-2}{4.14.2}) is the class of an ample biextension',
    r'under (\SGARefLink{sga7.sga7i.eviii.n4-14-2}{4.14.1}) is the class of an ample biextension',
    278, ['F7I-VIII-043.1'],
    'The last sentence of VIII4.14 refers to 4.14.1 in print and 4.14.2 in current. Both English branches previously had the corrected number. Restore the printed visible reference while retaining its stable link key.')

add(6, '138',
    r'is canonically isomorphic to $\mathbb Z_\ell(1)$,',
    r'is canonically isomorphic to $\mathbb Z_\ell(1)$ $(I\qquad)$,',
    351, ['F7I-IX-034.1'],
    'The printed IX3.5(v) statement includes the incomplete parenthetical locator (I followed by a blank). Current deletes it, and the English release has already made that deletion. Restore the blank locator in diplomatic English without supplying any missing number.')

add(7, '139',
    "cf.\nExpos\\'e I [reference omitted in the source]",
    r'cf. I\hspace{2.5em}',
    357, ['F7I-IX-040.3', 'F7I-IX-040.4'],
    'After IX4.2.1 the print has cf. I followed by a blank, whereas current explicitly calls the exposé and explains the omitted internal reference in brackets. The English release already follows current. Restore the exact blank-locator form in the diplomatic body; do not manufacture a target.')

add(8, '162',
    r'define a pairing (\SGARefLink{sga7.sga7i.eix.n9-5-5}{9.5.5})',
    r'define a pairing (\SGARefLink{sga7.sga7i.eix.n9-5-5}{9.5.6})',
    437, ['F7I-IX-117.2'],
    'The defining-pairing sentence in IX9.6 cites 9.5.6 in print and 9.5.5 in current. Both English branches previously had 9.5.5. Restore the printed visible locator only.')

add(9, '170',
    r'It follows immediately from Proposition \SGARefLink{sga7.sga7i.eix.n9-4-7}{9.4.7}',
    r'It follows immediately from \SGARefLink{sga7.sga7i.eix.n9-4-7}{9.4.6}',
    460, ['F7I-IX-137.3'],
    'The printed sentence following the IX11.6.13 proof diagram cites 9.4.6 without calling it a proposition. Current cites the actual Proposition 9.4.7; the released English explanatory footnote already records the discrepancy, but the diplomatic body had not restored it. Restore the printed locator and omit the release-added proposition label in that branch.')

add(10, '171',
    'divisible by $n$.',
    r'divisible by $n$ (cf. I\hspace{3em}).',
    464, ['F7I-IX-142.1'],
    'The final sentence in the proof of IX11.9 has an incomplete cf. I locator in print, which current removes. A released English editorial footnote mentions it, but the diplomatic body had omitted the authorial locator. Restore the printed blank reference without supplying a number.')

from nonmath_i_review import extend
body_patches = extend(add, components, fr, coverage, write_inputs=not REPORTS_ONLY)

# Classify the bounded inherited-only population. Formula entries are explicitly
# reserved to the completed mathematical audit, rather than claimed as rechecked.
neutral = {
    'F7I-INTRO-002.1': 'French semicolon/comma at a translated clause boundary; no change in the English meaning.',
    'F7I-INTRO-003.1': 'French verb agreement soients/soient; English vanish is unchanged.',
    'F7I-INTRO-004.1': 'French spelling succinte/succincte; English succinctly is unchanged.',
    'F7I-INTRO-005.1': 'French missing word-space after punctuation; English spacing already normal.',
    'F7I-II-008.5': 'Bibliographical spacing before the volume number; the complete substantive citation is reconstructed by ED-EN-NONMATH-I-003.',
    'F7I-VIII-007.2': 'A missing word-space, without an English lexical or semantic counterpart.',
    'F7I-VIII-040.2': 'Sentence punctuation only; excluded from this bounded meaning/reference review.',
    'F7I-VIII-064.1': 'Paragraph spacing before item c), without an English wording change.',
    'F7I-VIII-064.3': 'Repeated French conditional si; the existing English if construction carries the same condition.',
    'F7I-VIII-064.4': 'French finite verb insertion in the same condition; English is already requires the verb in both forms.',
    'F7I-VIII-077.1': 'French spelling paraître; the English forthcoming reading is unchanged.',
}
for key, reason in neutral.items():
    coverage.setdefault(key, ('no_substantive_English_difference', None, reason))
coverage['F7I-INTRO-003.2'] = ('already_repaired_in_final_English', 'ADOPT-F7I-INTRO-003.2',
    'The English build has now applied I.4.5→I.4.6 to corrected introduction and preserved I.4.5 in its diplomatic branch.')
coverage['F7I-VII-056.2'] = ('already_covered_by_explicit_prose_reconstruction', 'ED-EN-FORMULA-E014',
    'The complete E014 construction removes the inserted bar-d0 definition in the diplomatic branch and preserves it in corrected English.')
coverage['F7I-VIII-064.2'] = ('already_covered_by_explicit_prose_reconstruction', 'ED-EN-FORMULA-E038',
    'The E038 reconstruction removes the explicit closed-immersion definition only from diplomatic English.')
assert '(I. 4.6)' in final['Introduction']['corrected']
assert '(I. 4.5)' in final['Introduction']['diplomatic']

from nonmath_i_coverage import make_report
summary = make_report(fr, variants, body_patches, coverage)
if REPORTS_ONLY:
    after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in INPUT_FILES if p.exists()}
    assert INPUT_HASHES_BEFORE == after, 'Reports-only mode changed a reader input.'
    summary['reports_only_input_identity_verified'] = {'files': len(after), 'unchanged': True, 'sha256': after}
if not REPORTS_ONLY:
    (ROOT / 'work/en_nonmath_resolutions_editorial.json').write_text(json.dumps(variants, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'output/records/EN_NONMATH_I_AUDIT.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: summary[k] for k in ('all_volume_i_apparatus_entries_screened', 'source_selection_entries_screened', 'status_counts', 'exact_diplomatic_operation_decisions', 'paired_corrected_body_repair_decisions', 'reader_individual_reading_checks', 'remaining_missing_reference_decisions', 'exceptions')}, indent=2))
