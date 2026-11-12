"""Explicit, source-checked repairs to the non-local English formula transfers.

This reads the immutable released-component snapshot and the saved source-pair
review.  It does not edit any source or shared build script.
"""
import json
import hashlib
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
frozen = ROOT / 'output/records/EN_FORMULA_NONLOCAL_REVIEW.json'
if not frozen.exists():
    frozen = ROOT / 'EN_FORMULA_NONLOCAL_REVIEW.json'
review = {r['operation_index']: r for r in json.loads(frozen.read_text())}
operations = review
components_file = ROOT / 'work/en_components.json'
components = {(c['volume'], c['component']): c['text'] for c in json.loads(
    components_file.read_text())} if components_file.exists() else {}
decisions = []


def decision(index, action, reason, printed=None, covered_by=None):
    op = operations[index]
    assert index in review, (index, 'outside non-local audit scope')
    assert not op['method'].startswith('local'), index
    if components:
        component = components[op['volume'], op['component']]
        assert component[op['start']:op['end']] == op['corrected'], index
    else:
        assert op['native_span_verified'], index
        assert hashlib.sha256(op['corrected'].encode()).hexdigest() == op['native_span_sha256'], index
    row = {k: op[k] for k in ('volume', 'component', 'start', 'end', 'corrected', 'source', 'folio')}
    row.update(operation_index=index, id=f'ED-EN-FORMULA-AUDIT-{index:03d}',
               action=action, printed=op['printed'] if printed is None else printed,
               rejected_automatic_printed=op['printed'], reason=reason,
               source_printed=review[index]['source_printed'],
               source_current=review[index]['source_current'])
    if covered_by:
        row['covered_by'] = covered_by
    if action == 'override':
        assert balanced(row['printed']), (index, 'unbalanced braces')
    decisions.append(row)


def balanced(text):
    depth = 0
    for token in re.findall(r'\\[{}]|[{}]', text):
        if token == '{':
            depth += 1
        elif token == '}':
            depth -= 1
        if depth < 0:
            return False
    return depth == 0


def replace(index, old, new, reason, count=1):
    value = operations[index]['printed']
    assert value.count(old) == count, (index, old, value.count(old))
    decision(index, 'override', reason, value.replace(old, new))


replace(25, r'A^{I_i)}', r'A^{I_i})',
        'The diplomatic formula is T_l(A^{I_i}), not T_l(A^{I_i)}). The parenthesis closes the argument after the exponent group; normalization had moved it into that group.')

for index, old, new, reason in [
    (108, r'\longrightarrowP', r'\longrightarrow P', 'The printed morphism reverses the endpoints to A→P. The inserted target must remain a separate TeX token from the arrow command.'),
    (149, r'\subsetV', r'\subset V', 'The printed inclusion is V⊂V-perpendicular. Its target must remain separate from the subset command.'),
    (160, r'\overlineK', r'\overline K', 'The printed denominator is the algebraic closure of K, with an overline applied to K, not a newly invented control word.'),
    (179, r'\longmapstou', r'\longmapsto u', 'The printed formula includes g↦u(g). The mapsto command and the function u require a token boundary.'),
    (223, r'\longrightarrowC', r'\longrightarrow C', 'The diplomatic exact sequence really terminates in C. Restore the C as the arrow target without creating a control word.'),
    (243, r'\longrightarrowK', r'\longrightarrow K', 'The printed relation is an arrow to K*, not equality; preserve the TeX boundary before K.'),
    (253, r'\leqn', r'\leq n', 'The diplomatic inequality uses ≤n−1; n is the argument after the relation, not part of a control word.'),
    (259, r'\longrightarrowf', r'\longrightarrow f', 'The source diplomatic exact sequence has the quotient term first and uses f throughout. Preserve that order while separating the middle arrow from f_*.'),
    (270, r'\ldotsf', r'\ldots f', 'The diplomatic list has no separating commas but retains an ellipsis followed by f_n; it does not introduce a control word ldotsf.'),
    (320, r'\bars', r'\bar s', 'The diplomatic Galois-group denominator is bar s; preserve the accent command and its argument separately.'),
    (335, r'\leqr', r'\leq r', 'The diplomatic bound is r(d), with r following the ≤ relation as a separate token.'),
    (365, r'\widetildeX', r'\widetilde X', 'The diplomatic X_s carries a tilde. Reconstruct the accent applied to X rather than concatenating a control word.'),
    (366, r'\widetildeX', r'\widetilde X', 'The first X in the diplomatic equality carries a tilde; retain the native script grouping and a separate accent argument.'),
]:
    replace(index, old, new, reason)

replace(113, r'Z_P_\eta', r'Z_{P_\eta}',
        'The diplomatic expression is Z indexed by P_eta. The complete nested subscript must be grouped, avoiding an artificial double subscript on Z.')

replace(213, r'\bigl(M,T_\ell(\mathbb \underlineG_{m\underline S}\bigr)',
        r'\bigl(M,T_\ell(\underline{\mathbb G}_{m\underline S})',
        'The source diplomatic diagram underlines the blackboard G and lacks the outer Hom closing parenthesis. Preserve the inner Tate-module closing parenthesis, underline the complete blackboard symbol, and omit only the outer parenthesis. The automatic transfer both merged the underline control word and consumed the wrong closing parenthesis.')

replace(296, 'card(A)=2', r'\operatorname{card}(A)=2',
        'The source misprint changes char to card but retains upright operator typography (source mathrm). Keep the native English operatorname style for that same printed operator.')

replace(345, r'\Omega^*_\bar X^*', r'\Omega^*_{\bar X^*}',
        'The diplomatic expression has all of bar X* as the subscript of Omega*. Group the complete indexed expression instead of allowing the accent and second star to escape the subscript.')

replace(384, r'\stackrel{\operatorname{pr}_2}\relbar\joinrel\relbar\joinrel\relbar',
        r'\stackrel{\operatorname{pr}_2}{\relbar\joinrel\relbar\joinrel\relbar}',
        'The source diplomatic morphism is a three-segment rule labelled pr_2, without an arrowhead. The entire rule is the second argument of stackrel and must be grouped.')

replace(445, r'R^{i-1}_f_*', r'R^{i-1}_{f_*}',
        'The diplomatic diagram places f_* as a single subscript of R^{i−1}. Group the nested subscript; the ungrouped automatic form creates a double-subscript error.')
replace(446, r'T_/S', r'T_{/S}',
        'The diplomatic source places the complete /S below T. Its missing Prim superscript and printed R^{dot−1} are retained, but the slash and S must occupy one TeX subscript group.')
replace(467, r'D_\overline\eta', r'D_{\overline\eta}',
        'The first D in the diplomatic fundamental-group argument is indexed by overline eta. Group the accent and its argument together; the second D_eta remains as printed.')
replace(493, r'\eta^2n', r'\eta^{2n}',
        'The source diplomatic exponent is the complete product 2n. The automatic transfer had exponentiated only 2 and placed n on the baseline.')
replace(494, r'\mathbb (Q', r'(\mathbb Q',
        'In the diplomatic direct-image formula each added opening parenthesis precedes blackboard Q. Preserve the printed missing first outer closing parenthesis and the printed −d_2 twist, while preventing mathbb from styling a parenthesis instead of Q.', count=2)

op = operations[526]
printed = op['corrected'].replace(r'\mathbb Q_\ell(m)', r'\mathbb Q_\ell(n)').replace(r'\right)=1', r'\right.=1')
decision(526, 'override',
         'Direct inspection of source formula 357 resolves the split/merge warning: the source retains the Prim argument closing parenthesis and omits the outer dim closing parenthesis. Preserve the inner parenthesis, change the coefficient twist m→n, and use a null right delimiter solely to balance TeX left/right without printing an invented character. The 2m exponent remains 2m.', printed)

decision(530, 'override',
         'Direct inspection of source (1.2.4) resolves the generic split/merge warning: the diplomatic summation really has lower index i alone and upper index r, while current has i=1. The complete native English displayed formula is the unique corresponding formula; the original proposed printed reading is retained.')

replace(567, '(x).\n=', '(x)\\right.\n=',
        'The source diplomatic exponential lacks the /p and the visible right parenthesis, and the later trace denominator is H_p. Retain its null right delimiter: the automatic transfer turned that delimiter into a visible period and left an unmatched left delimiter. The period terminating the entire formula remains.')

for index in (578, 584, 592):
    replace(index, r'\right...', r'\right..',
            'The source diplomatic ending is a null right delimiter followed by one printed full stop. The automatic transfer duplicated the visible full stop; retain exactly the source punctuation while keeping TeX delimiter balance.')

replace(580, r'\operatorname{\operatorname{car}}', r'\operatorname{car}',
        'The source diplomatic first exponent contains the upright operator car(A)−1, not a nested operatorname. Retain its separate printed extra parenthesis after alpha_B; remove only the transfer-created duplicate operator wrapper.')
replace(590, r'\longrightarrowO', r'\longrightarrow\mathcal O',
        'The source diplomatic final term is calligraphic O rather than zero. Restore its calligraphic font as well as the token boundary after the arrow.')
replace(591, '\nO', '\n\\mathcal O',
        'Both rightmost cells in the source diplomatic diagram are calligraphic O rather than zero. The automatic transfer changed the glyph but lost the calligraphic modifier; retain that font in both cells.', count=2)

for index, covered_by, reason in [
    (115, 'ED-EN-FORMULA-G037', 'The explicitly reconstructed whole VIII 282 clause already restores extensions of P by G_k together with its other source change. Reject this competing isolated split/merge transfer.'),
    (162, 'ED-EN-FORMULA-G053', 'The expanded explicit IX 395 paragraph reconstruction includes the first simplicity K→K-prime and the later incorrect extension base. Reject this isolated split/merge operation to preserve the reviewed whole passage.'),
    (448, 'ED-EN-FORMULA-G145', 'The full reviewed XVIII 303 proof reconstruction restores both H^o and the arrow with nu* above and the isomorphism symbol below. Its complete TeX grouping supersedes the automatic ungrouped overset/underset and merged longrightarrowH control word.'),
    (449, 'ED-EN-FORMULA-G145', 'The reviewed whole XVIII 303 proof reconstructs the printed P^1 alpha juxtaposition at the correct point. Do not apply a competing isolated split/merge transfer.'),
    (450, 'ED-EN-FORMULA-G145', 'The reviewed whole XVIII 303 proof reconstructs the printed implication sign and alpha*f*(alpha) in its complete conclusion. Do not apply the competing isolated transfer.'),
    (479, 'ED-EN-FORMULA-E192', 'The reviewed XVIII 324 inertia clause replaces the complete native English phrase, including the delta_i and S_i readings. This one-token operation overlaps that reconstruction and would lose its full syntactic context.'),
    (507, 'ED-7II-1018-EN', 'A decided correction restores the complete quotient equality in corrected English as well as the defective printed equality in diplomatic English. The exact body repair and variant in EN_EDITORIAL_BODY_PATCH_1018.json supersede an operation that populated only the diplomatic branch.'),
    (527, 'ED-EN-FORMULA-E218', 'The English sentence already names H^i immediately before the separate i<n−1 math span. The source difference only repartitions the formula spans; inserting H^i again here would duplicate text. The reviewed no-counterpart decision preserves the complete English statement.'),
    (551, 'ED-EN-FORMULA-G223', 'The reviewed XXI 389 lemma restores the whole printed passage, including alpha_1…alpha_n and the index-range convention. Reject this overlapping isolated formula transfer.'),
]:
    decision(index, 'reject', reason, covered_by=covered_by)

decisions.sort(key=lambda r: r['operation_index'])
assert len({r['operation_index'] for r in decisions}) == len(decisions)
out = ROOT / 'output/records/EN_FORMULA_NONLOCAL_AUDIT.json'
if not out.parent.exists():
    out = ROOT / 'EN_FORMULA_NONLOCAL_AUDIT.json'
out.write_text(json.dumps(decisions, ensure_ascii=False, indent=2) + '\n')

summary = {
    'scope': 'All accepted formula operations whose method does not start with local',
    'operations_in_scope': len(review),
    'operations_total': 596,
    'local_operations_reserved_to_root': 141,
    'actions': dict(Counter(d['action'] for d in decisions)),
    'retained_after_comparison_with_source_pair': len(review) - len(decisions),
    'reviewed_operation_indices': sorted(review),
    'retained_operation_indices': sorted(set(review) - {d['operation_index'] for d in decisions}),
    'retention_basis': 'Compared each complete proposed formula with its paired supplied diplomatic/current French source and the native English span; retained source misprints even where they are mathematically defective. Repaired only transfer-created command, group, font, delimiter, punctuation, or alignment damage, and resolved overlapping explicit reconstructions.',
    'native_span_assertions': 'All explicit decisions match the exact original English component slice.',
    'brace_assertions': 'All override printed formulas have balanced unescaped TeX braces.',
    'source_files_modified': False,
    'decision_file': 'EN_FORMULA_NONLOCAL_AUDIT.json',
    'frozen_review_input': 'EN_FORMULA_NONLOCAL_REVIEW.json',
}
(out.parent / 'EN_FORMULA_NONLOCAL_AUDIT_SUMMARY.json').write_text(
    json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: summary[k] for k in ('operations_in_scope', 'actions', 'retained_after_comparison_with_source_pair')}, indent=2))
