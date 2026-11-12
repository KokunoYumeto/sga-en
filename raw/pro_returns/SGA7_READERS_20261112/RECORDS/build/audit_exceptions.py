#!/usr/bin/env python3
"""Verify all nonliteral French fix records with explicit local predicates.

The supplied witnesses are read only. Archive-internal paths are used in the
report. Historical log ordinals are one-based; printed misprint IDs are kept.
"""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources'
REC = ROOT / 'output' / 'records'
MARK = re.compile(r'%{3,}\s*scan idx (\d+)\s*\|\s*folio ([^\s%]+)\s*%+')


def pages(path):
    s = path.read_text()
    ms = list(MARK.finditer(s))
    return {m.group(2): s[m.end():ms[i+1].start() if i+1 < len(ms) else len(s)]
            for i, m in enumerate(ms)} if ms else {'V–VII': s}


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def main():
    audit = list(csv.DictReader((REC / 'FR_FIX_AUDIT.tsv').open(), delimiter='\t'))
    logs = {log: [json.loads(x) for x in (SRC / log).read_text().splitlines() if x.strip()]
            for log in {r['log'] for r in audit}}
    cached = {}

    def context(row, baseline=False):
        vol = row['page'].split()[0]
        layer = 'current' if '_CURRENT' in row['log'] else 'diplomatic'
        if baseline:
            root, layer = 'fr_baseline_aug2026', 'corrected' if layer == 'current' else 'diplomatic'
        else:
            root = 'fr'
        path = f'{root}/sga{vol.lower()}/{layer}/{row["file"]}'
        if path not in cached:
            cached[path] = pages(SRC / path)
        return path, cached[path]

    def ident(log, n):
        rr = logs[log][n-1]
        vol = rr['vol']
        branch = 'C' if '_CURRENT' in log else 'D'
        return rr.get('id', f'FIX-{vol}-{branch}-{n:04}')

    def record_ref(log, n):
        r = logs[log][n-1]
        return {'id': ident(log, n), 'log': log, 'record': n, 'old': r['old'],
                'new': r.get('new', ''), 'source': r.get('source', '')}

    exceptions = []
    for row in audit:
        if not ('differs' in row['replay'] or 'transformed' in row['final_evidence']):
            continue
        n = int(row['record'])
        r = logs[row['log']][n-1]
        path, pp = context(row)
        basepath, bp = context(row, True)
        page = str(r['page'])
        final, baseline = pp[page], bp[page]
        checks = []
        successors = []
        evidence = {}

        def check(predicate, actual, expected):
            checks.append({'predicate': predicate, 'actual': actual, 'expected': expected,
                           'passed': actual == expected})
            assert actual == expected, (row['id'], predicate, actual, expected)

        if r['kind'] == 'dash_convention':
            expected = int(re.search(r'x(\d+)', r['old']).group(1))
            oldprices = re.findall(r'DM\s+\d+[,.]-(?!-)', baseline)
            newprices = re.findall(r'DM\s+\d+[,.]--(?!-)', final)
            check('baseline single-dash price count equals the synthetic log multiplicity', len(oldprices), expected)
            check('final double-dash price count equals the synthetic log multiplicity', len(newprices), expected)
            check('all price values and their comma/dot punctuation are preserved in order',
                  [p[:-2] for p in newprices], [p[:-1] for p in oldprices])
            check('no single-dash price remains on this folio', len(re.findall(r'DM\s+\d+[,.]-(?!-)', final)), 0)
            evidence = {'matched_final_prices': newprices,
                        'comma_price_count': len(re.findall(r'DM\s+\d+,--', final)),
                        'dot_price_count': len(re.findall(r'DM\s+\d+\.--', final)),
                        'dot_price_lines': [x for x in final.splitlines() if re.search(r'DM\s+\d+\.--', x)]}
            why = ('The old/new fields are a bulk-operation description, not literal TeX. '
                   'Folio 526 includes three dot-separated prices (catalogue volumes 181, 186, 198); '
                   'the price-dash operation preserves those punctuation readings.')
        elif r['source'] == 'global_fraktur_XIII_87_89':
            oldletters = re.findall(r'\\mathcal\{([FG])\}', baseline)
            newletters = re.findall(r'\\mathfrak\{([FG])\}', final)
            check('all original calligraphic F/G occurrences become fraktur in the same order', newletters, oldletters)
            check('no calligraphic F or G remains on this folio', len(re.findall(r'\\mathcal\{[FG]\}', final)), 0)
            check('at least one intended glyph was checked', bool(newletters), True)
            evidence = {'baseline_counts': {x: oldletters.count(x) for x in 'FG'},
                        'final_counts': {x: newletters.count(x) for x in 'FG'},
                        'ordered_letter_sequence': ''.join(newletters)}
            why = ('The log uses a synthetic all-on-page operation. Neither page 87 nor page 89 '
                   'contains both letters, so literal search for the comma-separated placeholder is invalid.')
        elif r['vol'] == '7I' and r['page'] == 357:
            normalized = r['new'].replace('A^{*O}', 'A^{*o}')
            check('continuation marker absent from final folio', 'CONT' in final, False)
            check('old uppercase identity-component letter absent', 'A^{*O}' in final, False)
            check('new reading survives after the recorded uppercase-to-lowercase repair', final.count(normalized), 2)
            ns = [580, 583] if '_CURRENT' not in row['log'] else [503, 506]
            successors = [record_ref(row['log'], k) for k in ns]
            evidence = {'composed_new': normalized, 'occurrences': final.count(normalized)}
            why = ('The continuation token was removed. The later scan-established identity-component '
                   'letter repair changes O to o at both matching formula contexts; no continuation token returns.')
        elif r['vol'] == '7I' and r['page'] == 526:
            normalized = r['new'].replace('DM 16,-\n', 'DM 16,--\n')
            check('terminal catalogue rule remains after the later price-dash conversion', final.count(normalized), 1)
            k = 708 if '_CURRENT' not in row['log'] else 606
            successors = [record_ref(row['log'], k)]
            evidence = {'composed_new': normalized}
            why = 'The horizontal rule survives exactly; the later bulk operation changes the preceding price dash.'
        elif r['vol'] == '7I' and r['page'] == 420:
            normalized = r['new'].replace("M'", r"\check{M}'")
            check('corrected outer parentheses survive with the later checked character group', final.count(normalized), 1)
            check('malformed original W-prime subexpression absent', r'T_{\ell}(T\'_o)(\overline{k})' in final, False)
            successors = [record_ref(row['log'], 909)]
            evidence = {'composed_new': normalized}
            why = 'Record 7I:660 later supplies the check on M-prime; it preserves the corrected parenthesis placement.'
        elif r['vol'] == '7II' and r['page'] == 410:
            normalized = '(2.2.4).\n\n\\begin{equation}\\tag{3.1.2}'
            check('full stop still immediately precedes equation 3.1.2', final.count(normalized), 1)
            check('exact later underline-boundary reading present', final.count(r'\underline{ou, ce qui est équivalent par} (2.2.4).'), 1)
            successors = [record_ref(row['log'], 663)]
            evidence = {'composed_new': normalized, 'final_sentence': r'\underline{ou, ce qui est équivalent par} (2.2.4).'}
            why = 'The later recheck moves the closing underline brace before the reference; the printed full stop is unchanged.'
        elif r['vol'] == '7II' and r['page'] == 430:
            normalized = r['new'].replace(r'\right)', r'\right.')
            check('Omega remains underlined in the final printed-parenthesis reading', final.count(normalized), 1)
            successors = [record_ref(row['log'], 518)]
            evidence = {'composed_new': normalized}
            why = ('The next recorded diplomatic-only correction restores the print\'s missing right parenthesis '
                   'using an invisible right delimiter. The underline on Omega survives.')
        elif r['vol'] == '7II' and r['page'] == 431:
            name = r'E_{\mathrm{DR}}^n(V)'
            check('old formula ending occurs on baseline folio 430', bp['430'].count(r['old']), 1)
            check('old formula ending does not occur on baseline folio 431', baseline.count(r['old']), 0)
            check('corrected formula ending occurs on final folio 431', final.count(r['new']), 1)
            check('the E_DR display has moved from folio 430 to folio 431',
                  [bp['430'].count(name), baseline.count(name), pp['430'].count(name), final.count(name)], [1, 0, 0, 1])
            evidence = {'exact_final_formula_ending': r['new'],
                        'supplemental_sources': ['conventions/GLOBAL_ISSUES_SGA.md#64', 'conventions/GLOBAL_ISSUES_SGA.md#66']}
            why = ('The formula was first moved across the 430/431 folio marker, as explicitly recorded in '
                   'GLOBAL_ISSUES 64 and 66. A replay that does not perform that marker move cannot find the '
                   'old string on 431; the final hooked arrow and comma are exact.')
        else:
            raise AssertionError(('unhandled exception', row['id']))
        exceptions.append({'id': row['id'], 'log': row['log'], 'record': n, 'page': row['page'],
                           'file': row['file'], 'historical_replay_status': row['replay'],
                           'historical_final_evidence': row['final_evidence'],
                           'verification': 'passed all explicit predicates', 'reason': why,
                           'source': path, 'baseline_source': basepath,
                           'final_page_sha256': sha(final), 'baseline_page_sha256': sha(baseline),
                           'predicates': checks, 'evidence': evidence, 'later_records': successors})

    # Close every reported supersession by concrete later record(s), recursively
    # when a second supersession altered the immediate successor's literal string.
    supersessions = []
    for row in audit:
        if 'superseded' not in row['final_evidence']:
            continue
        log = row['log']; n = int(row['record']); rr = logs[log][n-1]
        path, pp = context(row); final = pp[str(rr['page'])]

        def trace(k, seen):
            r = logs[log][k-1]
            if r.get('new') and r['new'] in final:
                return {'record': record_ref(log, k), 'final_literal_count': final.count(r['new']), 'children': []}
            assert k not in seen
            matches = [(j, s) for j, s in enumerate(logs[log][k:], k+1)
                       if s['file'] == r['file'] and s['page'] == r['page'] and r.get('new')
                       and (r['new'] in s['old'] or s['old'] in r['new'])]
            assert matches, (row['id'], k)
            return {'record': record_ref(log, k), 'final_literal_count': 0,
                    'children': [trace(j, seen | {k}) for j, _ in matches]}

        supersessions.append({'id': row['id'], 'log': log, 'record': n, 'page': row['page'],
                              'source': path, 'final_page_sha256': sha(final),
                              'verification': 'all recorded successor chains terminate in exact final literals',
                              'chain': trace(n, set())})

    exception_ids = {r['id'] for r in exceptions}
    supersession_ids = {r['id'] for r in supersessions}
    exact = 0
    transformed = 0
    for row in audit:
        if row['id'] in supersession_ids:
            continue
        if 'transformed' in row['final_evidence']:
            assert row['id'] in exception_ids
            transformed += 1
            continue
        rr = logs[row['log']][int(row['record'])-1]
        _, pp = context(row)
        final = pp[str(rr['page'])]
        assert rr.get('new') and rr['new'] in final, row['id']
        exact += 1
    assert len(exceptions) == 19
    assert len(supersessions) == 56
    assert exact + len(supersessions) + transformed == len(audit) == 3434
    summary = {'total_fix_records': len(audit), 'exact_final_literal_records': exact,
               'concrete_successor_chain_records': len(supersessions),
               'explicit_transformed_or_bulk_predicate_records': transformed,
               'distinct_historical_exception_rows': len(exceptions),
               'replay_mismatch_rows': sum('differs' in r['replay'] for r in audit),
               'all_records_concretely_verified': True, 'source_files_modified': False}
    out = {'schema_version': 1, 'summary': summary,
           'scope': ('This report proves survival, composition, or explicit supersession of all logged fixes '
                     'in the designated final witnesses. It does not claim a fresh comparison to unavailable scans. '
                     'Exact master-to-source projections are independently checked by audit_fr.py.'),
           'exceptions': exceptions, 'supersessions': supersessions}
    (REC / 'FR_FIX_EXCEPTIONS.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
