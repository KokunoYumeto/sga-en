"""Verify the five stale already-decision targets by exact successor/scope predicates.

This audit writes records only. It does not alter source text or reader inputs.
"""
import csv
import hashlib
import json
import re
from pathlib import Path
from english_stage import load_port, french_pages
from french import math_at

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'output/records'


def sha(t):
    return hashlib.sha256(t.encode()).hexdigest()


def underline_ranges(t):
    out = []
    for m in re.finditer(r'\\underline\s*\{', t):
        start = m.end()
        depth = 1
        p = start
        while depth:
            assert p < len(t)
            if t[p] == '\\':
                p += 2
                continue
            if t[p] == '{':
                depth += 1
            elif t[p] == '}':
                depth -= 1
            p += 1
        out.append((start, p - 1))
    return out


def build_supplement():
    finals = {(c['volume'], c['component']): c for c in json.loads((ROOT / 'work/en_final_components.json').read_text())}
    ports = {v: load_port(v)[0] for v in ['7I', '7II']}
    source_logs = {}
    for v in ['7I', '7II']:
        for suffix in ['', '_CURRENT']:
            name = 'fixes/FIXLOG_' + v + suffix + '.jsonl'
            source_logs[name] = [json.loads(s) for s in (ROOT / 'sources' / name).read_text().splitlines() if s.strip()]
    french_audit = {(r['log'], int(r['record'])): r for r in csv.DictReader((REC / 'FR_FIX_AUDIT.tsv').open(), delimiter='\t')}
    results = []

    def setup(v, pid):
        p = ports[v][pid]
        fix = source_logs['fixes/FIXLOG_' + v + '_CURRENT.jsonl'][int(pid[1:])]
        c = finals[v, p['tr_file']]
        assert p['decision'] == 'already'
        assert c['text'].count(p['tr_old']) == c['corrected'].count(p['tr_old']) == 0
        affected = []
        for log in ['fixes/FIXLOG_' + v + '.jsonl', 'fixes/FIXLOG_' + v + '_CURRENT.jsonl']:
            for i, f in enumerate(source_logs[log]):
                if all(f[k] == fix[k] for k in ['file', 'page', 'old', 'new']):
                    fr = french_audit[log, i+1]
                    affected.append({'source_log': log, 'source_record': i+1, 'source_fix_id': fr['id'], 'page': fr['page']})
        source = {b: french_pages(v,b)[fix['file'], str(fix['page'])] for b in ['current', 'diplomatic']}
        r = {'id': 'EN-ALREADY-' + v + '-' + pid, 'volume': v, 'port_id': pid,
             'component': p['tr_file'], 'folio': str(fix['page']),
             'port_decision_source': p['source'], 'historical_target': p['tr_old'],
             'historical_target_native_count': 0, 'historical_target_final_corrected_count': 0,
             'source_fix': fix, 'affected_source_records': affected, 'checks': [],
             'source_disposition': '', 'body_change_required': False,
             'final_component_sha256': {b: sha(c[b]) for b in ['text','corrected','diplomatic']},
             'final_source_page_sha256': {b: sha(source[b]) for b in source}}
        return r,p,c,source

    def exact(r,c,target,branches=('text','corrected','diplomatic'),label='exact corresponding English passage'):
        counts = {b: c[b].count(target) for b in branches}
        assert all(n == 1 for n in counts.values()), (r['id'], label, counts, target)
        r['checks'].append({'predicate': 'exact occurrence count equals one', 'description': label,
                            'target': target, 'observed_counts': counts, 'passed': True})

    def source_exact(r,s,target,branches=('current','diplomatic')):
        counts = {b: s[b].count(target) for b in branches}
        assert all(n == 1 for n in counts.values()), (r['id'],counts,target)
        r['checks'].append({'predicate': 'exact source-page occurrence count equals one',
                            'target': target, 'observed_counts': counts, 'passed': True})

    def successors(r,p,ids,extension=''):
        target = p['tr_old'] + extension
        if extension:
            r['historical_target_extension_from_successor_context'] = extension
        steps = []
        for pid in ids:
            later = ports[r['volume']][pid]
            assert later.get('outcome') == 'applied'
            assert target.count(later['tr_old']) == 1
            target = target.replace(later['tr_old'], later['tr_new'], 1)
            steps.append({'port_id': pid, 'source': later['source'], 'old': later['tr_old'], 'new': later['tr_new']})
        r['exact_successor_chain'] = steps
        return target

    r,p,c,s = setup('7I','C217')
    target = successors(r,p,['C577'])
    exact(r,c,target,label='complete old already-target after recorded C577 underline-boundary repair')
    inner = '\\underline{Its essential image consists of the\nrigidified line bundles $\\mathbb L$ on $P$ for which}'
    exact(r,c,inner,label='second underline contains the line-bundle symbol')
    position = c['corrected'].index(inner) + inner.index('\\mathbb L')
    enclosed = [(a,b) for a,b in underline_ranges(c['corrected']) if a <= position < b]
    assert len(enclosed) == 1 and math_at(c['corrected'], position)
    r['checks'].append({'predicate': 'line-bundle symbol is inside exactly one underline argument and in math mode', 'symbol': r'\mathbb L', 'passed': True})
    source_exact(r,s,r'$\underline{L}$ \underline{sur}')
    r['English_evidence_kind'] = 'already-correct underline scope verified after C577'
    r['evidence'] = 'C577 exactly transforms the obsolete full-statement target into the released two-underline statement. The unique second underline contains $\\mathbb L$ in native, corrected and diplomatic English; brace-scope and math-mode predicates pass. Both final French source pages contain $\\underline{L}$ \\underline{sur}. EN_ALREADY_EXCEPTIONS.json#EN-ALREADY-7I-C217.'
    r['source_disposition'] = 'Common transcription repair retained in both French layers and both English projections. C577 changes the underline boundary around fully faithful, while preserving the line-bundle symbol inside the next underline.'
    results.append(r)

    r,p,c,s = setup('7I','C851')
    target = successors(r,p,['C1035'])
    exact(r,c,target,('text','corrected'),'closing parenthesis retained after the recorded VII-to-XVII reference correction')
    printed = '$K_t$ is unipotent (SGA 3, VII, 1.1, then $K_s$ is unipotent as well.'
    exact(r,c,printed,('diplomatic',),'printed wrong exposé reference and missing closing parenthesis retained together')
    source_exact(r,s,'(SGA 3 XVII 1.1), il en est',('current',))
    source_exact(r,s,'(SGA 3 VII 1.1, il en est',('diplomatic',))
    r['English_evidence_kind'] = 'already-correct closing parenthesis verified after C1035'
    r['evidence'] = 'C1035 changes VII to XVII in the exact C851 target. The unique native/final corrected sentence has (SGA 3, XVII, 1.1), including the required closing parenthesis. Diplomatic English independently has (SGA 3, VII, 1.1, matching both printed defects. EN_ALREADY_EXCEPTIONS.json#EN-ALREADY-7I-C851.'
    r['source_disposition'] = 'C851 supplies the missing closing parenthesis; later C1035 supplies the corrected exposé numeral. Final French current has XVII and the close, whereas diplomatic has VII without it. The existing final-witness reconstruction preserves the printed combination.'
    r['french_apparatus_ids'] = ['F7I-IX-030.2','F7I-IX-030.3']
    results.append(r)

    r,p,c,s = setup('7I','C909')
    target = p['tr_old'].replace('^I',r'^{\pi_o}')
    assert target != p['tr_old']
    exact(r,c,target,('text','corrected'),'balanced outer parentheses with final-source invariant pi_o')
    assert target.count('(') == target.count(')') == 2
    printed = target.replace(r'\bigl(','',1).replace(r'^{\pi_o}',r'^{I}')
    exact(r,c,printed,('diplomatic',),'printed missing outer opening parenthesis and invariant I')
    assert printed.count('(') == 1 and printed.count(')') == 2
    r['checks'].append({'predicate': 'literal visible-parenthesis counts', 'corrected': {'open':2,'close':2}, 'diplomatic': {'open':1,'close':2}, 'passed':True})
    source_exact(r,s,r['source_fix']['new'],('current',))
    source_exact(r,s,r['source_fix']['old'].replace(r'^{\pi_o}','^I'),('diplomatic',))
    r['English_evidence_kind'] = 'already-correct outer parentheses verified in final formula'
    r['evidence'] = 'The historical C909 target differs only by its obsolete invariant exponent I. Replacing that exponent with the final-source pi_o yields one exact native/corrected match. The corrected expression has two opening and two closing parentheses; the printed branch has one opening and two closing parentheses and exponent I, as the final French witnesses require. EN_ALREADY_EXCEPTIONS.json#EN-ALREADY-7I-C909.'
    r['source_disposition'] = 'The C909 outer-parenthesis repair is present. The recorded already-target still used I, while released native English and current French already use pi_o. This independent source reading is not falsely described as an applied later port edit. Existing formula reconstruction 3067 restores the printed missing parenthesis and exponent I together.'
    r['french_apparatus_ids'] = ['F7I-IX-098.1','F7I-IX-098.2']
    results.append(r)

    r,p,c,s = setup('7II','C233')
    target = successors(r,p,['C860'])
    exact(r,c,target,label='terminal diagram period after recorded arrow-label-position repair C860')
    source_exact(r,s,'\\mathrm{U} \\arrow[l, "\\nu"] & .\n\\end{tikzcd}')
    r['English_evidence_kind'] = 'already-correct terminal punctuation verified after C860'
    r['evidence'] = 'C860 exactly changes the historical arrow-label placement from U\\arrow[l,"\\nu"\']. to U\\arrow[l,"\\nu"]. while retaining the period. The transformed target occurs once in native, corrected and diplomatic English. Both final French source diagrams also retain their terminal period. EN_ALREADY_EXCEPTIONS.json#EN-ALREADY-7II-C233.'
    r['source_disposition'] = 'The punctuation correction is common to both source layers. The historical already-target becomes nonliteral only because C860 removes the label-position prime; the terminal punctuation is retained in every English form.'
    results.append(r)

    r,p,c,s = setup('7II','C265')
    target = successors(r,p,['C878','C879'],extension=', with')
    exact(r,c,target,label='theorem statement after exact recorded changes from underlined G to plain G')
    for branch in ['text','corrected','diplomatic']:
        position = c[branch].index(target) + target.index('$E$') + 1
        enclosed = [(a,b) for a,b in underline_ranges(c[branch]) if a <= position < b]
        assert not enclosed and math_at(c[branch],position)
    r['checks'].append({'predicate': 'E in the unique Theorem 5.5.2 target is in math mode and outside every underline argument', 'branches':['text','corrected','diplomatic'], 'passed':True})
    source_exact(r,s,r'\underline{un} $E$-\underline{faisceau constructible sur}')
    r['English_evidence_kind'] = 'already-correct math-symbol scope verified after C878 and C879'
    r['evidence'] = 'C878 and C879 exactly transform the stale target by removing the two unrelated underlines on G. The resulting Theorem 5.5.2 passage occurs once in native, corrected and diplomatic English. Its $E$-sheaf symbol is in math mode and outside every underline scope in all three; both final French pages have the same E-scope property. EN_ALREADY_EXCEPTIONS.json#EN-ALREADY-7II-C265.'
    r['source_disposition'] = 'The common transcription correction moves E into math mode and outside the statement underline. Later applied C878/C879 change G and log|G|, not E. Exact successor replay and independent scope predicates verify the required effect.'
    results.append(r)

    assert len(results) == 5
    assert sum(len(r['affected_source_records']) for r in results) == 8
    return {'unique_already_decisions':5, 'source_audit_records':8,
            'all_predicates_verified':True, 'body_changes_required':0,
            'blank_reasons':0, 'records':results,
            'reproduction':'python build/audit_en_already_exceptions.py',
            'scope':'Only the five stale already-decision targets flagged by EN_FIX_AUDIT.tsv. Exact successor replay, final paired source readings, and TeX scope/count predicates are distinguished from literal historical-target matches.'}


if __name__ == '__main__':
    result = build_supplement()
    (REC / 'EN_ALREADY_EXCEPTIONS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['unique_already_decisions','source_audit_records','all_predicates_verified','body_changes_required','blank_reasons']},indent=2))
