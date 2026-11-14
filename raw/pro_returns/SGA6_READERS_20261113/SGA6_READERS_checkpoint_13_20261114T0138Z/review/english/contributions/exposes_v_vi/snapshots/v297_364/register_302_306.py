#!/usr/bin/env python3
"""Register the manually compared English folios 302–306 in this contribution."""
from pathlib import Path
import json, sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from contribution import MATH, build_records, dump

def units(page, layer):
    return [m.group() for m in MATH.finditer((HERE / 'source_packets' / str(page) / f'{layer}.tex').read_text())]

pairs = json.loads((HERE / 'lexical_math_pairs.json').read_text())
pairs = [p for p in pairs if p['page'] != 302]
fr = units(302, 'current')[35]
assert fr.count(r'\text{(par 1.6.i))}') == 1
en = fr.replace(r'\text{(par 1.6.i))}', r'\text{(by 1.6.i))}')
pairs.append(dict(page=302, layer='both', French_literal_unit=fr, English_literal_unit=en,
                  expected_multiplicity=1, status='individually reviewed lexical translation only',
                  scope='The complete concluding display; only par is translated as by. Every formula token, parenthesis, label and whitespace character outside that lexical word is unchanged.'))
dump(HERE / 'lexical_math_pairs.json', pairs)

u304c, u304d = units(304, 'current')[2], units(304, 'diplomatic')[2]
u306c, u306d = units(306, 'current')[0], units(306, 'diplomatic')[0]
assert u304c != u304d and u306c != u306d
batches = json.loads((HERE / 'batches.json').read_text())
batches = [b for b in batches if b['first'] != 302]
batches.append(dict(
    expose='V', first=302, last=306,
    native_start='\\[\n  \\theta=\\xi(1+Xt).\n\\]\nWe show',
    native_end='is an isomorphism.\n\nTo see that it is injective,',
    source='review/expose_v/FROZEN_HANDOFF.md; reviewed French302–306 in both forms',
    reason='Complete reconstruction of the continuation of1.6, its gluing and additivity calculations,1.7,1.8,and the beginning of1.9 from the frozen French source. All four native stable targets remain at the corresponding passages; every reviewed mathematical unit is transferred literally apart from the one separately recorded lexical translation inside a display.',
    variants=[
        dict(id='EN-CONTRIB-V-304-01', page=304, old=u304c, printed=u304d, mode='display',
             source='check/findings/findings_301_305.json#17',
             related_sources=['check/findings/findings_301_305.json#18']),
        dict(id='EN-CONTRIB-V-306-01', page=306, old=u306c[2:-2], printed=u306d[2:-2], mode='math',
             source='check/findings/findings_306_310.json#2')
    ],
    notes=[
        dict(page=302, source_id='ASTRA-V-SIGMA-302;ASTRA-V-ELLIPSES-302',
             English_rendering='the complete1.6 continuation, unaccented sigma map, and final by1.6.i) explanation',
             decision='Preserve capital Phi, the exact source composition Phi∘Ghat(f_n)=H(f_n)∘Phi, every low ellipsis, the two sigma occurrences without added tilde, and every diagram label position. Restore the concluding citation omitted by the native English. Symmetric function is translated without adding elementary, which is absent from this source passage.'),
        dict(page=303, source_id='check/findings/findings_301_305.json#15',
             English_rendering='a system of maps',
             decision='The French singular/plural application/applications correction has the same English collective rendering in both forms; it creates no separate English spelling variant.'),
        dict(page=303, source_id='ASTRA-V-ELLIPSES-303;ASTRA-V-NOTATION-303',
             English_rendering='full gluing congruence and the set-valued naturality statement',
             decision='Restore the explicit initial congruence, the source chi and open-left varphi forms, the exact infinite polynomial-ring target in the last congruence, and underlined Ens. Retain F^{p+1} in the first two congruences and the printed weaker F^p in the final one. The native claim with values in groups is replaced by the source category Ens.'),
        dict(page=304, source_id='fixes/RECONCILE_CODEX_6.json#296;ASTRA-V-ELLIPSES-304',
             English_rendering='the inclusive filtration bound and full invariant-ring triangle',
             decision='Transfer the observed chi series names separately from polynomial variables X_i. Restore the literal source bound ≥n, the congruence followed by equality to zero, the hook on the left downward arrow, the fraktur symmetric-group names and the diagram punctuation. The two parenthesis defects are explicitly branched together in their complete display, each with its own source identifier.'),
        dict(page=305, source_id='check/findings/findings_301_305.json#24;fixes/RECONCILE_CODEX_6.json#308',
             English_rendering='the j-th symmetric function',
             decision='The French masculine/feminine article repair le/la has the same English article the in both forms; no English grammatical error is invented.'),
        dict(page=305, source_id='ASTRA-V-ELLIPSES-305;ASTRA-V-FONT-305',
             English_rendering='complete two-stage Phi(chi) equality and all of1.7',
             decision='Restore the H(f_chi) member omitted from the native display, retain the printed bare f-prime in the preceding prose, and keep the resp. chi_2 clause inside its original mathematical unit. Preserve the source ring notation with parenthesized generators, plain paragraph number, reinforced Z,and the ending page split before the universal element.'),
        dict(page=306, source_id='ASTRA-V-FONT-306;check/findings/findings_306_310.json#5;check/findings/findings_306_310.json#6',
             English_rendering='coarse filtration; literal Id and the separately underlined category words',
             decision='Preserve the source semicolons and absence of a final stop after the reference, the capital Id occurrence, all three separately ruled Ab/fil names, and the exact lexical underline groups of Lemma1.9. The index-list two-dot misprint is an explicit branch; all coefficients and endpoints stay fixed.'),
        dict(page=306, source_id='review/expose_v/page_status.jsonl#pages302-306',
             English_rendering='five exact folio boundaries, four native stable targets, and no author notes',
             decision='Every prose clause, formula and placement was manually compared against its reviewed French page. Source boundaries inside the naturality sentence, group-action description and universal-element phrase remain in their corresponding positions. No author-note call or text occurs in these five reviewed source pages; no continuation macro block crosses this batch.')
    ], retained_proof_audits=[]))
dump(HERE / 'batches.json', batches)
build_records()
