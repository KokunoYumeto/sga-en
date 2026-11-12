"""Review the eleven historical port reversals absent from the final witness.

Run during the build with the immutable original component snapshot present.
The output freezes the actual final French page evidence for independent review.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ops = json.loads((ROOT / 'work/en_port_operations.json').read_text())
candidates = json.loads((ROOT / 'work/en_candidates.json').read_text())
components = {(c['volume'], c['component']): c['text'] for c in json.loads(
    (ROOT / 'work/en_components.json').read_text())}
rows = []


def page(volume, layer, file, folio):
    ref = f'fr/sga{volume.lower()}/{layer}/{file}'
    source = (ROOT / 'sources' / ref).read_text()
    marks = list(re.finditer(r'(?m)^%{4,}.*?folio\s+(\S+)\s+%+', source))
    i = next(i for i, m in enumerate(marks) if m.group(1) == str(folio))
    return ref, source[marks[i].end():marks[i + 1].start() if i + 1 < len(marks) else len(source)]


def add(index, printed, reason, source_d, source_c, covered_by=None):
    op = ops[index]
    port_id = re.search(r'#(C\d+);', op['source'])[1]
    candidate = next(c for c in candidates if c['volume'] == op['volume'] and c['id'] == port_id)
    assert not candidate['fr_old_in_diplomatic']
    f = candidate['fr_fix']
    dr, d = page(op['volume'], 'diplomatic', f['file'], f['page'])
    cr, c = page(op['volume'], 'current', f['file'], f['page'])
    assert source_d in d, (port_id, source_d, 'not in final diplomatic page')
    assert source_c in c, (port_id, source_c, 'not in final current page')
    native = components[op['volume'], op['component']]
    assert native[op['start']:op['end']] == op['corrected'], port_id
    row = dict(op)
    row.update(id=f'ED-EN-PORT-WITNESS-{op["volume"]}-{port_id}', port_id=port_id,
               port_operation_index=index, action='reject' if covered_by else 'override',
               historical_printed_proposal=op['printed'], printed=printed,
               reason=reason, source_diplomatic=dr, source_current=cr,
               final_diplomatic_evidence=source_d, final_current_evidence=source_c,
               final_diplomatic_page_sha256=hashlib.sha256(d.encode()).hexdigest(),
               final_current_page_sha256=hashlib.sha256(c.encode()).hexdigest())
    if covered_by:
        row['covered_by'] = covered_by
    rows.append(row)


add(0, ops[0]['corrected'].replace("A'_K", "A'_k"),
    'The final diplomatic equation (6.3.2) has lowercase k in both A-prime subscripts, while the corrected witness has uppercase K. The K-prime reading in the historical port was an earlier transcription state and must not be restored.',
    r"T_p(A_K)^{et} = (T_p(A'_k)^{ef})^{\perp}, \; T_p(A_K)^{ef} = (T_p(A'_k)^{et})^{\perp}",
    r"T_p(A_K)^{et} = (T_p(A'_K)^{ef})^{\perp}, \; T_p(A_K)^{ef} = (T_p(A'_K)^{et})^{\perp}")

add(27, ops[27]['printed'].replace(r'2\alpha', r'2\lambda'),
    'The final diplomatic rank formula (2.5.5) has V in both numerators and ends in 2lambda. The corrected formula inserts perpendicular signs but still ends in 2lambda. The historical 2alpha proposal is not the printed witness.',
    r'\mathrm{rang}\ V/V \cap V^{\perp} \;=\; \mathrm{rang}\ V/W = 2\lambda',
    r'\mathrm{rang}\ V^{\perp}/V \cap V^{\perp} \;=\; \mathrm{rang}\ V^{\perp}/W = 2\lambda')

add(97, ops[97]['corrected'].replace("$p''=", '$p"='),
    'Both final source layers put S=P×P×P in math mode and set all three projection operators upright. The only source difference in this clause is the diplomatic p followed by a double-quote character versus the corrected double-prime. Reversing the historical dollar boundaries or operator font would reintroduce repaired transcription damage.',
    r'''$S=P\times P\times P$, $p=\mathrm{pr}_1$,$p'=\mathrm{pr}_2$,$p"=\mathrm{pr}_3$''',
    r'''$S=P\times P\times P$, $p=\mathrm{pr}_1$,$p'=\mathrm{pr}_2$,$p''=\mathrm{pr}_3$''')

add(102, ops[102]['printed'].replace('VII, 1.1)', 'VII, 1.1'),
    'The final diplomatic source has the incorrect VII reference and lacks the reference closing parenthesis; current has XVII and the closing parenthesis. The historical port captured only the numeral change. Restore both recorded printed defects in the complete native clause.',
    r"si $K_t$ est unipotent (SGA 3 VII 1.1, il en est de même de $K_s$.",
    r"si $K_t$ est unipotent (SGA 3 XVII 1.1), il en est de même de $K_s$.")

add(132, ops[132]['corrected'].replace(r'R\Psi_\eta(K_\eta)', r'R\Psi_\eta(K_s)'),
    'The final diplomatic triangle (2.1.2.4) explicitly has RΨ_eta(K_s), confirmed also by its diagram description; current changes only K_s to K_eta. Removing the nearby-cycle functor would resurrect an earlier transcription omission.',
    r'R\Psi_\eta(K_s) \arrow[ul]', r'R\Psi_\eta(K_\eta) \arrow[ul]')

add(135, ops[135]['corrected'].replace('(2.1.7.1)', '(2.1.8.1)'),
    'The final diplomatic sentence following (2.1.7.3) refers to (2.1.8.1), while current refers to (2.1.7.1). The historical 1.3.8.1 reading is absent from the source witness and is not restored.',
    r"qui, pour $f$ propre, est l'inverse de (2.1.8.1).",
    r"qui, pour $f$ propre, est l'inverse de (2.1.7.1).")

add(197, ops[197]['printed'].replace('j+n-i+1', 'j+2n-2i+2'),
    'The final diplomatic definition (5.2.2.2) both omits the outer kernel closing parenthesis and has coefficient twist j+2n−2i+2. Reconstruct both defects in the complete displayed formula. A null right delimiter balances TeX without printing the absent parenthesis.',
    r'\mathrm{Prim}^i(S,\mathbb{Q}_\ell(j)) = \mathrm{Ker}\ (L^{n-i+1} \ :\ H^i(S,\mathbb{Q}_\ell(j)) \longrightarrow H^{2n-i+2}(S,\mathbb{Q}_\ell(j+2n-2i+2)).',
    r'\mathrm{Prim}^i(S,\mathbb{Q}_\ell(j)) = \mathrm{Ker}\ (L^{n-i+1} \ :\ H^i(S,\mathbb{Q}_\ell(j)) \longrightarrow H^{2n-i+2}(S,\mathbb{Q}_\ell(j+n-i+1))).')

add(204, ops[204]['corrected'].replace('X_1^{W_1}', 'X_1^{W}'),
    'Uppercase W is already used throughout both final source layers. The only printed defect in this product is the first exponent W instead of W_1. Reversing the historical lower-to-uppercase transcription repair would silently change four printed symbols.',
    '\\prod_W\n\\Theta\\!\\left(A_W^{\\tau^j}X_0X_1^{W}\\cdots\nX_{n+2}^{W_{n+2}}\\right)',
    '\\prod_W\n\\Theta\\!\\left(A_W^{\\tau^j}X_0X_1^{W_1}\\cdots\nX_{n+2}^{W_{n+2}}\\right)')

add(210, ops[210]['corrected'].replace(r'\pi_U', r'\pi'),
    'The final diplomatic cartesian square labels the left vertical arrow pi, while current labels it pi_U. The TikZ label-side apostrophe is absent from both final layers. Preserve their common placement and restore only the actual source-label difference.',
    r'\mathrm{V} \arrow[r, hook, "\mu"] \arrow[d, "\pi"]',
    r'\mathrm{V} \arrow[r, hook, "\mu"] \arrow[d, "\pi_U"]')

add(216, ops[216]['corrected'].replace(r'(x)/p\right)', r'(x)\right.'),
    'The source diplomatic additive-character formula lacks /p and the visible right parenthesis; its second trace also has H_p rather than F_p. The complete source-checked formula-operation 567 override restores all three in one span and supersedes this partial historical port reversal.',
    r'\exp\!\left(2\pi i\,\operatorname{tr}_{\mathbb F_{q^\nu}/\mathbb F_p}(x)\right.',
    r'\exp\!\left(2\pi i\,\operatorname{tr}_{\mathbb F_{q^\nu}/\mathbb F_p}(x)/p\right)',
    covered_by='ED-EN-FORMULA-AUDIT-567')

add(217, ops[217]['printed'].replace('(1-q^it)', '(1-q^if)'),
    'The final diplomatic pair (5.0.8)–(5.0.9) has the reversed quotient, lacks the reciprocal exponent on the product, and prints f instead of t in its first factor. The full two-display native span must restore all three differences, not the intermediate historical state with t already repaired.',
    '=\\frac{Z(t,V/\\mathbb F_q)}\n{Z(qt,V/\\mathbb F_q)(1-t)}\n\\end{equation}\n\net\n\n\\begin{equation}\\tag{5.0.9}\nZ(t,V/\\mathbb F_q)\n=\\prod_{i\\geq0}\\left[(1-q^if)\nZ(q^it,V_{\\mathrm{aff}}/\\mathbb F_q)\\right].',
    '=\\frac{Z(qt,V/\\mathbb F_q)}\n{Z(t,V/\\mathbb F_q)(1-t)}\n\\end{equation}\n\net\n\n\\begin{equation}\\tag{5.0.9}\nZ(t,V/\\mathbb F_q)\n=\\prod_{i\\geq0}\\left[(1-q^it)\nZ(q^it,V_{\\mathrm{aff}}/\\mathbb F_q)\\right]^{-1}.')

assert len(rows) == 11
for name in ['work/en_port_witness_audit_editorial.json', 'output/records/EN_PORT_FINAL_WITNESS_AUDIT.json']:
    (ROOT / name).write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
print('Source-checked final port witnesses: 11; overrides: 10; superseded: 1.')
