#!/usr/bin/env python3
"""Bounded Volume II audit of prose and reference differences missed by math extraction.

The supplied corrected French/English witnesses remain authoritative. Operations
restore source-attested readings in diplomatic English only; they are not fresh
emendations of the released English text.
"""
import collections
import argparse
import csv
import json
import re
from pathlib import Path

from audit_fr import group
from english_variants import balanced

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work'
OUT = ROOT / 'output' / 'records'
COMP = json.loads((WORK / 'en_components.json').read_text())
EDITION = {(c['volume'], c['expose']): c for c in json.loads((WORK / 'en_variant_data.json').read_text())}
FINAL = {(c['volume'], c['component']): c for c in json.loads((WORK / 'en_final_components.json').read_text())} if (WORK / 'en_final_components.json').exists() else {}
APP = json.loads((OUT / 'FR_APPARATUS.json').read_text())
BY_ID = {a['id']: a for a in APP}
OPERATIONS = []
REVIEWS = {}


def review(ids, status, reason, **extra):
    for ident in ids.split():
        assert ident not in REVIEWS, ident
        REVIEWS[ident] = dict(status=status, reason=reason, **extra)


def add(fr_id, prefix, corrected, printed, reason):
    fr = BY_ID[fr_id]
    choices = [c for c in COMP if c['volume'] == '7II' and c['component'].split('/')[-1].startswith(prefix)]
    assert len(choices) == 1, prefix
    c = choices[0]
    assert c['text'].count(corrected) == 1, (fr_id, c['text'].count(corrected), corrected)
    assert corrected != printed and balanced(printed), fr_id
    assert len(re.findall(r'(?<!\\)\$', printed)) % 2 == 0, fr_id
    ident = f'ED-EN-NONMATH-G{len(OPERATIONS):03d}'
    entry = dict(id=ident, mode='variant', status='variant', volume='7II', expose=fr['expose'],
                 component=c['component'], start=c['text'].index(corrected),
                 corrected=corrected, printed=printed, page=fr['page'],
                 source=f"{ident}; {fr_id}; {fr['source']}; fr/sga7ii/{{diplomatic,current}}/expose_{fr['expose']}_body.tex; folio {fr['page']}",
                 reason=reason,
                 prior_exact_printed_present=printed in EDITION[('7II', fr['expose'])]['diplomatic'])
    if ('7II', c['component']) in FINAL:
        final = FINAL[('7II', c['component'])]
        entry['component_projection_check'] = dict(
            corrected_target_count=final['corrected'].count(corrected),
            printed_target_count=final['diplomatic'].count(printed),
            printed_target_baseline_count=final['corrected'].count(printed),
            corrected_target_remaining_in_printed=final['diplomatic'].count(corrected))
        check = entry['component_projection_check']
        check['verified'] = (check['corrected_target_count'] == 1 and
                             check['printed_target_count'] == check['printed_target_baseline_count'] + 1 and
                             check['corrected_target_remaining_in_printed'] == 0)
    OPERATIONS.append(entry)
    review(fr_id, 'exact diplomatic operation', reason, operation=ident)


def operations():
    add('F7II-X-023.1', '005_',
        '$T$ \\underline{be a closed subscheme of} $S_1$ \\underline{with ideal} $q$;\n\\underline{let} $n$',
        '$T$ \\underline{be a closed subscheme of} $S_1$ \\underline{with ideal} $q$;\n\\underline{let} $D$ \\underline{be a divisor}; \\underline{let} $n$',
        'Lemma 2.14 first introduces a redundant unspecified divisor D in print, before introducing the regular divisor D later. Restore that first clause only in diplomatic English.')
    add('F7II-X-024.1', '005_', 'By the theorem on formal functions,', 'By the theorem on holomorphic functions,',
        'The supplied print names holomorphic functions; the corrected witness and native English correctly name the theorem on formal functions. This is a distinct theorem name, not French spelling.')
    add('F7II-XIII-023.1', '033_', r'Let $\Lambda$ be as in 2.1.1,', r'Let $\Lambda$ be as in 2.2.1,',
        'The coefficient-ring reference in 2.2.3 is printed as 2.2.1 and corrected to 2.1.1; the inherited English source note independently records both readings.')
    add('F7II-XIV-010.1', '044_', 'Under this hypothesis, the triangle of 1.2.6 gives', 'Under this hypothesis, the triangle of 1.2.1 gives',
        'The triangle citation in 1.3.6 is 1.2.1 in print and 1.2.6 in the corrected witness, also expressly documented by the native English editorial note.')
    add('F7II-XVII-005.4', '091_', 'with the $d$-th Veronese embedding', 'with the $d$-th Segre embedding',
        'Restore the printed Segre name in 2.4. The native English note explicitly identifies the monomial map as Veronese and records the printed name.')
    add('F7II-XVIII-019.4', '113_',
        'The four singular fibers lie over $\\mu^3=-1$ and $\\mu=\\infty$,\nrespectively,',
        'The four singular fibers lie over $\\mu=$ a cube root of unity and $\\mu=\\infty$,\nrespectively,',
        'Restore the entire printed finite-parameter clause, including the words cube root of unity. A formula-only reversal leaves the incomplete phrase mu= without its prose complement; this operation supersedes that partial reversal and covers ADOPT entries .2-.4 in group019.')
    for fr_id, phrase in [
        ('F7II-XIX-009.3', 'Weyl group of the root system in (b).'),
        ('F7II-XIX-010.4', 'root system whose\nWeyl group is the monodromy group.'),
        ('F7II-XIX-010.5', 'are conjugate under the Weyl group;'),
        ('F7II-XIX-010.6', 'the unique invariant form under\nthe Weyl group.'),
        ('F7II-XIX-011.2', 'or $E$, whose Weyl group is the monodromy group.'),
        ('F7II-XIX-018.2', r'$\pi_1$ in $\operatorname{GL}(\operatorname{Ev}(V))$ is the Weyl group of')]:
        add(fr_id, '138_' if fr_id == 'F7II-XIX-018.2' else '136_', phrase, phrase.replace('Weyl', 'Weil'),
            'This occurrence is printed Weil and corrected Weyl. The native English editorial note records the repeated misnaming; restore only the source-attested occurrence, leaving the corrected name in reading English.')
    add('F7II-XXII-062.1', '179_', 'formula (4.5.33) gives', 'formula (4.5.24) gives',
        'The opening of Section 6 cites 4.5.24 in print and 4.5.33 in the corrected witness. The inherited English source note independently confirms the distinction.')

    # The same blind spot affects mapped historical fixes as well as ADOPT
    # entries. These exact contextual references are therefore checked too.
    for fr_id, prefix, corrected, printed in [
        ('F7II-X-043.3', '009_', r'\textit{Amer. J. Math.} 90, no. 2', r'\textit{Amer. J. Math.} 15, no. 2'),
        ('F7II-XII-006.1', '019_', '1.8. We saw in 1.3 that,', '1.8. We saw in 1.6 that,'),
        ('F7II-XII-012.1', '021_', 'By 2.3(iii), the Picard scheme', 'By 2.3(ii), the Picard scheme'),
        ('F7II-XII-012.2', '021_', 'having the structure described in\n2.3(ii).', 'having the structure described in\n2.3(iii).'),
        ('F7II-XII-020.3', '023_', 'By duality, or from\n(3.6.3),', 'By duality, or from\n(3.5.3),'),
        ('F7II-XIII-015.1', '031_', r"when $f$ is \'{e}tale, is the inverse of (2.1.7.2).", r"when $f$ is \'{e}tale, is the inverse of (2.1.7.1)."),
        ('F7II-XIII-020.1', '032_', r"The d\'{e}vissage just used reduces us", r"The d\'{e}vissage used in 2.1.11 reduces us"),
        ('F7II-XIII-027.1', '033_', 'The compatibility (2.2.5.2) says that the trace morphism (2.2.5.1),', 'The compatibility (2.3.5.2) says that the trace morphism (2.3.5.1),'),
        ('F7II-XIII-031.1', '036_', 'its essential ingredients are the variation morphisms (2.4.5.1),', 'its essential ingredients are the variation morphisms (2.4.4.1),'),
        ('F7II-XIV-043.1', '059_', 'It is clear that (4.1.2) is a quasi-isomorphism', 'It is clear that (4.1.1) is a quasi-isomorphism'),
        ('F7II-XIV-055.4', '062_', 'both sides of 4.18.5 vanish.', 'both sides of 4.18.4 vanish.'),
        ('F7II-XV-005.2', '066_', r'Let $Y_0$ be defined by $Q$ as in 1.2.3.', r'Let $Y_0$ be defined by $Q$ as in 4.3.'),
        ('F7II-XV-008.1', '066_', 'It is therefore enough to verify (1.2.11.1) after extending scalars', 'It is therefore enough to verify (4.11.1) after extending scalars'),
        ('F7II-XVII-027.6', '100_', 'On the one hand, 3.7.1 and 4.1.2 show', 'On the one hand, 3.8.1 and 4.1.2 show'),
        ('F7II-XVIII-047.1', '117_', 'But by (5.2.4.3) and the projection formula,', 'But by (5.2.5) and the projection formula,'),
        ('F7II-XVIII-050.4', '117_', 'hypotheses of Lemma 5.2.6.', 'hypotheses of Lemma 5.2.5.'),
        ('F7II-XVIII-054.2', '120_', r'$\rho:\widetilde X\to\mathbb P^1$ satisfies condition (A).', r'$\rho:\widetilde X\to\mathbb P^1$ satisfies condition (5.3.2).'),
        ('F7II-XVIII-058.5', '120_', 'Hence the kernel\nof (5.6.5) identifies,', 'Hence the kernel\nof (5.6.8) identifies,'),
        ('F7II-XVIII-106.1', '132_', r'\tag{6.5.1.2}', r'\tag{6.5.2.2}'),
        ('F7II-XVIII-111.2', '133_', 'Math. \\textbf{90} (4) (1968),', 'Math. \\textbf{15} (4) (1968),'),
        ('F7II-XIX-018.3', '138_', 'assertion 5.2(ii) is well known', 'assertion 4.2(ii) is well known'),
        ('F7II-XIX-018.4', '138_', 'and for small values of $n$, 5.2(iii) was known,', 'and for small values of $n$, 4.2(iii) was known,'),
        ('F7II-XIX-018.5', '138_', 'He deduces 5.2(iii) from', 'He deduces 4.2(iii) from'),
        ('F7II-XX-006.1', '139_', 'in which $S,X,f,Y,g$ are as in (1.0.1)--(1.0.4),', 'in which $S,X,f,Y,g$ are as in (1.0.2)--(1.0.4),'),
        ('F7II-XX-034.3', '145_', 'This follows from (4.4.12), by 1.7.', 'This follows from (4.3.12), by 1.7.'),
        ('F7II-XXI-014.1', '150_', 'Proposition~1.1.5 now shows', 'Proposition~1.5 now shows'),
        ('F7II-XXI-042.1', '161_', 'as in the proof of\nTheorem~5.2.2.', 'as in the proof of\nTheorem~5.5.2.'),
        ('F7II-XXI-043.1', '161_', 'it is enough to prove the desired assertion for $U$.', 'it is enough to prove 5.2.2 for $U$.'),
        ('F7II-XXI-048.1', '162_', 'Lemma~5.6.2(i), together with the induction hypothesis', 'Lemma~6.2(i), together with the induction hypothesis'),
        ('F7II-XXII-019.1', '167_', '(3.1.2), (3.2.1)--(3.2.2), and (3.3.1) of (3.1.1).', '(6.1.2), (3.1.1.2), and (3.1.3) of (3.1.1).'),
        ('F7II-XXII-030.1', '168_', 'Lemmas~3.8 and 3.5 and deduce (3.4.1) for', 'Lemmas~3.8 and 3.5 and deduce (3.1.3) for'),
        ('F7II-XXII-030.8', '168_', 'Lemmas~3.8 and 3.5 gives (3.4.1) for every quasi-projective', 'Lemmas~3.8 and 3.5 gives (3.1.3) for every quasi-projective'),
        ('F7II-XXII-059.2', '178_', 'the proof by applying Lemma~4.6.6 once', 'the proof by applying Lemma~4.4.6 once')]:
        add(fr_id, prefix, corrected, printed,
            'The complete supplied French source pair changes this contextual numeric reference. The native English expresses the corrected reference; restore the printed locator at this exact occurrence, leaving other occurrences unchanged.')

    add('F7II-XIII-013.1', '030_', r'with generic point $\eta_{\mathrm{nr}}$.', r'with geometric point $\eta_{\mathrm{nr}}$.',
        'The source print says geometric point, whereas the corrected source says generic point. Supersede the earlier port output geometric generic point, which retained an unattested extra qualifier.')
    add('F7II-XIV-039.1', '058_', 'The normal bundle of this fiber is the constant', 'The normal bundle of this bundle is the constant',
        'The printed French repeats fibre with an erroneous accent, yielding the distinct technical noun fibré (bundle). The exact English counterpart is this fiber; retain the printed bundle wording in the diplomatic branch.')
    add('F7II-XV-023.1', '075_', r'The sheaf $R^n\Phi(\Lambda)$ is zero outside', r'The sheaf $R^n\Phi(\Lambda)$ is alone outside',
        'The native English editorial note explicitly renders the printed seul as alone and the corrected nul as zero. Restore that attested English rendering of the erroneous support assertion.')
    add('F7II-XIX-003.1', '135_', 'pure of odd\ndimension', 'pure of even\ndimension',
        'The printed hypothesis says even dimension 2n; the corrected source says odd dimension 2n+1. The numerical 2n+1 reversal was already present, but its adjective was not: restore even independently of the formula operation.')
    add('F7II-XX-040.9', '146_', 'but of which no nonzero multiple is', 'but of which no multiple is',
        'The print omits nonzero in the final quadric example. The corrected qualification excludes the zero multiple and changes the literal assertion; it must also be omitted in diplomatic English.')
    add('F7II-XXI-038.1', '159_',
        'It is enough to verify Lemma~5.3.2 when $V$ corresponds to\nan indecomposable $k[T]$-module',
        'It is enough to verify Lemma~3.2 when $V$ corresponds to\nan irreducible $k[T]$-module',
        'The same sentence prints the shortened reference 3.2 and the mathematically different term irreducible. Restore both together; this also covers F7II-XXI-038.2. The native source note independently records both errors.')
    add('F7II-XVIII-103.7', '131_',
        '$n=\\dim X$ is even or $\\operatorname{char}(k)\\ne2$, and that $X$\nsatisfies condition (LV).',
        '$n=\\dim X$ is even, or $\\operatorname{char}(k)\\ne2$ and that $X$\nsatisfies condition (LV).',
        'The source punctuation attaches the (LV) hypothesis only to the second alternative; the corrected parentheses make it common to both. The native English note expressly identifies this change of logical scope. Restore the printed comma placement without changing either mathematical predicate; this also covers F7II-XVIII-103.10.')
    add('F7II-XX-011.1', '140_', 'that $S$ is connected,', r'that $S$ is \underline{annexe},',
        'ED-EN-XX-ANNEXE: the French printed adjective annexe is corrected to connexe, rendered connected in native English. Retain the corrupt source adjective untranslated and underlined in diplomatic English, because selecting a determinate English predicate would add meaning; corrected English remains connected. No sic or conjectured English predicate is added.')
    entry = OPERATIONS[-1]
    old_id = entry['id']
    entry['id'] = 'ED-EN-XX-ANNEXE'
    entry['source'] = entry['source'].replace(old_id, entry['id'])
    REVIEWS['F7II-XX-011.1']['operation'] = entry['id']


def classify_prose():
    # These grammatical or compositional edits have no distinct English
    # reading. Each explanation is local to the displayed source context.
    for ids, reason in [
        ('F7II-X-008.1 F7II-XI-015.1 F7II-XIII-007.1', 'French number/agreement only; the assertion and the English verb/adjective do not change.'),
        ('F7II-X-034.2 F7II-XI-025.1', 'French capital A receives its grave accent; the English preposition is unchanged.'),
        ('F7II-X-037.5 F7II-X-037.6 F7II-X-037.9 F7II-X-037.12 F7II-X-037.13', 'Lemma 2.28 already specifies the same scheme T_1, point t_1, morphism f and equations in print. The correction makes implicit French nouns explicit and reorders them; native English already states these objects. This is the same contextual no-counterpart decision as formula-gap G077.'),
        ('F7II-XVIII-099.5 F7II-XVIII-099.6', 'French indicative verbs are replaced by the subjunctive required after equivaut à ce que. Both readings assert that the scheme has one point and is the spectrum of a field.'),
        ('F7II-XVIII-103.8 F7II-XVIII-103.9 F7II-XVIII-103.11', 'French subjunctive and masculine agreement only. The separate punctuation change affecting the scope of (LV) is reconstructed by G052.'),
        ('F7II-XVIII-107.1', 'The French preposition par is corrected to pour in for each i. Native English for each i expresses the intended quantifier in both witnesses; the independent inertia-group errors remain separately reconstructed.'),
        ('F7II-XVIII-109.11 F7II-XVIII-109.13 F7II-XVIII-109.15', 'The inferential connective donc is moved and en vertu de (6.6.1) becomes par 6.6.1. Both versions invoke the same proposition for the same implication; native English therefore/by phrasing is retained.'),
        ('F7II-XX-002.2 F7II-XX-002.3', 'The French expression à caractéristiques is repaired to de caractéristique. Both specify characteristic different from ell; native English expresses the same hypothesis.'),
        ('F7II-XX-010.1', 'Adding toute makes the generic primitive-class quantification explicit. Native English takes primitive classes to primitive classes already quantifies over every such class; no separate English assertion results.'),
        ('F7II-XX-020.5', 'Les opérations and l’action both denote the same subgroup action. The full nearby mathematical correction is handled separately by ED-7II-1018-EN; no lexical substitution of the released English action is required.'),
        ('F7II-XX-024.1', 'French on a déjà remarqué becomes on l’a déjà remarqué by supplying its object pronoun. English as already remarked conveys both readings.'),
        ('F7II-XX-025.5 F7II-XX-025.6 F7II-XX-025.7 F7II-XX-025.8 F7II-XX-025.9', 'French feminine agreement and the phrase dans tous les cas replace unidiomatic en tous cas. The English statement in all cases is unchanged.'),
        ('F7II-XX-025.10 F7II-XX-025.14', 'The French abbreviation car for characteristic is moved from prose into the mathematical operator car(k). Native English already uses the mathematical characteristic operator; the separate equality/inequality source variant is handled in the formula audit.'),
        ('F7II-XXI-001.10 F7II-XXI-001.11', 'French vectoriel is expanded to espace vectoriel and car. to caractéristique. Native English vector space in characteristic p already gives the complete meaning.'),
        ('F7II-XXI-023.1', 'Finite-rank vector spaces over Q_ell are rephrased as finite-dimensional vector spaces over Q_ell. The released English finite-dimensional terminology expresses both; the separate missing Galois numerator is not classified here.'),
        ('F7II-XXI-026.1 F7II-XXI-026.2', 'The same ambient projective space P^N is moved within the smooth-complete-intersection hypothesis. No scheme, ambient space, or dimension changes.'),
        ('F7II-XXII-029.3', 'Part of the Latin i.e. is removed while the adjacent mapped edit supplies French c’est-à-dire. Both mean that is; the English logical equivalence is unchanged.'),
        ('F7II-XXII-029.4 F7II-XXII-029.5', 'Hypersurface projective is regrouped and rewrapped across underline commands. Both witnesses specify a projective hypersurface; native English already does so.')]:
        review(ids, 'same English reading', reason)

    # One exact reconstruction can cover several atomic French apparatus rows.
    for target, ids in [
        ('F7II-XVIII-019.4', 'F7II-XVIII-019.2 F7II-XVIII-019.3'),
        ('F7II-XIII-027.1', 'F7II-XIII-027.2'),
        ('F7II-XVIII-054.2', 'F7II-XVIII-054.1'),
        ('F7II-XVIII-103.7', 'F7II-XVIII-103.10'),
        ('F7II-XXI-038.1', 'F7II-XXI-038.2'),
        ('F7II-XXII-019.1', 'F7II-XXII-019.2 F7II-XXII-019.3 F7II-XXII-019.4 F7II-XXII-019.5'),
        ('F7II-XXII-030.1', 'F7II-XXII-030.2'),
        ('F7II-XXII-030.8', 'F7II-XXII-030.9')]:
        review(ids, 'covered by exact operation', 'Covered by the complete contextual operation for ' + target + '.', operation=REVIEWS[target]['operation'])

    review('F7II-XXI-001.14 F7II-XXI-001.15 F7II-XXI-001.16', 'existing English variant',
           'The existing Appendix I / Appendix (§5) reconstruction also preserves the print’s omission of here. Both exact phrases occur in the respective current English projections.',
           printed='proved in Appendix I.', corrected='proved here in the Appendix\n(\\S 5).')
    review('F7II-XXI-036.3', 'existing English variant',
           'The complete eigenvalue-lemma reconstruction G223 already removes the added r=dim_E V^I convention from diplomatic English.',
           printed='space of coinvariants under $I$, regarded as $G/I$-modules.  Let',
           corrected='space of coinvariants under $I$, regarded as $G/I$-modules.  Put\n$r=\\dim_E V^I$')

    for fr_id, printed, corrected in [
        ('F7II-XII-003.4', 'Lemma 1.2.1 then defines a transitive', 'Lemma 1.3.1 then defines a transitive'),
        ('F7II-XIII-014.1', 'when $f$ is proper, is the inverse of (2.1.8.1).', 'when $f$ is proper, is the inverse of (2.1.7.1).'),
        ('F7II-XIII-032.1', r'\subsubsection*{2.4.6.}', r'\subsubsection*{2.4.7.}'),
        ('F7II-XIV-006.1', 'As in 1.1.1, one checks', 'As in 1.2.1, one checks'),
        ('F7II-XIV-032.1', 'the action described in 1.15', 'the action described in 1.1.5'),
        ('F7II-XIV-037.2', 'By 3.1.13 this gives', 'By 3.1.12 this gives'),
        ('F7II-XV-004.1', r'\item[(1)] \underline{If $k$', r'\item \underline{If $k$'),
        ('F7II-XV-014.1', r'\subsubsection*{Lemma 2.7.8.}', r'\subsubsection*{Lemma 2.1.8.}'),
        ('F7II-XVII-003.2', r'Ch.~X).', r'Ch.~IX).'),
        ('F7II-XVII-047.1', r'\subsubsection*{6.3 (exceptional case).}', r'\subsubsection*{6.4 (exceptional case).}'),
        ('F7II-XVIII-103.1', 'by 6.1.6,', 'by 6.1.10,'),
        ('F7II-XVIII-103.6', 'surjectivity in (6.1.2).', 'surjectivity in (6.1.1).'),
        ('F7II-XIX-011.1', 'If the equivalent conditions of 3.3 hold,', 'If the equivalent conditions of 3.4 hold,'),
        ('F7II-XX-040.3', 'In particular (4.2),', 'In particular, when $m=2$,'),
        ('F7II-XXI-020.3', 'By the trace formula (XX~3.2.1),', 'By the trace formula (XXII~3.2.1),'),
        ('F7II-XXI-035.1', 'Lemma~5.2.1 and Theorem~5.2 show', 'Lemma~5.2.1 and Theorem~5.2.2 show'),
        ('F7II-XXII-056.1', 'Assertions (5.0.4) and (5.0.2)', 'Assertions (5.0.5) and (5.0.2)')]:
        review(fr_id, 'existing English variant', 'Both contextual locator readings are already present in the appropriate English projections.', printed=printed, corrected=corrected)


def in_math(t, pos):
    """Formula context, including multline and TikZ environments."""
    math = False
    env = []
    for m in re.finditer(r'\\begin\{([^}]+)\}|\\end\{([^}]+)\}|\\[A-Za-z@]+|\\.|\$', t[:pos], re.S):
        if m[1]:
            env.append(m[1])
        elif m[2]:
            if env and env[-1] == m[2]:
                env.pop()
        elif m[0] in ['$', r'\[', r'\]', r'\(', r'\)']:
            math = not math
    return math or any(e in {'equation', 'equation*', 'align', 'align*', 'aligned', 'gather', 'gather*',
                            'array', 'tikzcd', 'tikzpicture', 'matrix', 'cases', 'multline', 'multline*',
                            'displaymath', 'eqnarray', 'eqnarray*', 'split'} for e in env)


def audit():
    classify_prose()
    groups = {}
    for c in json.loads((WORK / 'fr_variant_data.json').read_text()):
        t = c['annotated']; pos = 0
        while (pos := t.find(r'\SGAvar', pos)) >= 0:
            pos += len(r'\SGAvar')
            a, pos = group(t, pos); b, pos = group(t, pos); ident, pos = group(t, pos)
            if ident:
                groups[ident] = (a, b)
    rows = []
    prose_candidates = []
    mapped_numeric = []
    for a in APP:
        if a['volume'] != '7II':
            continue
        old, new = groups[a['group_id']]
        outside = []
        for t, begin, end in [(old, a['a0'], a['a1']), (new, a['b0'], a['b1'])]:
            assert t[begin:end] in [a['before'], a['after']], a['id']
            for m in re.finditer(r'\\[A-Za-z]+|[^\W_]+', t[begin:end]):
                if not m[0].startswith('\\') and not in_math(t, begin + m.start()):
                    outside.append(m[0])
        primary = a['source'].startswith('ADOPT-')
        diagram = a['group_id'] == 'F7II-XIX-014'
        numeric = not diagram and any(re.search(r'\d', w) or w in ['ii', 'iii', 'X', 'IX', 'XX', 'XXII'] for w in outside)
        if primary and outside and not diagram:
            prose_candidates.append(a['id'])
        if not primary and numeric:
            mapped_numeric.append(a['id'])
        if not (primary or numeric or a['id'] in REVIEWS):
            continue
        if a['id'] in REVIEWS:
            decision = REVIEWS[a['id']]
        elif diagram:
            decision = dict(status='diagram implementation', reason='The same marked paths and point labels are redrawn from TikZ matrix syntax to coordinates. This introduces no numeric prose reference or prose assertion; the separate formula-gap diagram review remains the mathematical check.')
        elif outside:
            raise AssertionError(('unreviewed prose/numeric hunk', a['id'], outside, a['before'], a['after']))
        else:
            decision = dict(status='formula, TeX, or nonsemantic punctuation scope', reason='No changed alphabetic or numeric prose token occurs outside formula environments. Mathematical symbols, typeface, delimiters and tags belong to the separate formula/font audits. Nonsemantic French punctuation and wrapping retain native English styling; the substantive Corollary 6.4 punctuation is explicitly reviewed separately.')
        row = dict(fr_id=a['id'], expose=a['expose'], folio=a['page'], primary_adopt=primary,
                   printed_french=a['before'], corrected_french=a['after'],
                   source=a['source'], source_ref=a['source_ref'], changed_prose_tokens=outside, **decision)
        if row['status'] == 'existing English variant':
            edition = EDITION[('7II', a['expose'])]
            assert ' '.join(row['printed'].split()) in ' '.join(edition['diplomatic'].split()), (a['id'], 'printed coverage', row['printed'])
            assert ' '.join(row['corrected'].split()) in ' '.join(edition['corrected'].split()), (a['id'], 'corrected coverage', row['corrected'])
            row['current_projection_check'] = True
        rows.append(row)
    primary_rows = [r for r in rows if r['primary_adopt']]
    assert len(primary_rows) == sum(a['volume'] == '7II' and a['source'].startswith('ADOPT-') for a in APP)
    assert len({o['id'] for o in OPERATIONS}) == len(OPERATIONS)
    for key, grouped in __import__('itertools').groupby(sorted(OPERATIONS, key=lambda o: (o['component'], o['start'])), lambda o: o['component']):
        prev = None
        for o in grouped:
            if prev:
                assert prev['start'] + len(prev['corrected']) <= o['start'], (key, prev['id'], o['id'])
            prev = o
    data = dict(scope='All Volume II ADOPT apparatus rows, plus every mapped nonformula numeric-reference hunk and the specifically identified meaning-changing lexical cases. Volume I is audited separately.',
                primary_adopt_entries=len(primary_rows), primary_changed_prose_entries=len(prose_candidates),
                mapped_numeric_reference_entries=len(mapped_numeric),
                primary_status_counts=dict(collections.Counter(r['status'] for r in primary_rows)),
                total_review_rows=len(rows), exact_operations=len(OPERATIONS),
                exact_printed_operation_spans_present=sum(o['prior_exact_printed_present'] for o in OPERATIONS),
                exact_component_projection_checks_passed=sum(o.get('component_projection_check', {}).get('verified', False) for o in OPERATIONS),
                current_body_repairs=0, unreviewed_prose_entries=0, rows=rows, operations=OPERATIONS,
                limits='This audit classifies the final supplied source-pair differences, not fresh physical-page readings. It does not re-evaluate formula-only or font-only mathematics, or force French grammatical defects into artificial English errors. It is not a claim that every French stylistic change has a separately different English sentence.')
    (OUT / 'EN_NONMATH_AUDIT.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    fields = ['fr_id', 'expose', 'folio', 'primary_adopt', 'printed_french', 'corrected_french', 'status', 'operation', 'reason', 'source', 'source_ref']
    with (OUT / 'EN_NONMATH_AUDIT.tsv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n', extrasaction='ignore')
        writer.writeheader(); writer.writerows(rows)
    def cell(t):
        return str(t).replace('|', '\\|').replace('\n', ' ')
    lines = ['# English Volume II prose and reference audit', '',
             '## Scope and counting unit', '', data['scope'], '',
             f"The primary review contains **{len(primary_rows)} atomic French apparatus entries**, including **{len(prose_candidates)} entries with changed prose words or numeric tokens outside mathematical environments**. The mapped-reference extension checks **{len(mapped_numeric)} further numeric-reference entries**. Multiple atomic entries may belong to one contextual reconstruction; entries and operations are therefore different counting units.", '',
             '| Primary ADOPT disposition | Entries |', '| --- | ---: |']
    lines.extend(f'| {cell(k)} | {v} |' for k, v in sorted(data['primary_status_counts'].items()))
    lines += ['', '## Exact reconstructions and checks', '',
              f"There are **{len(OPERATIONS)} exact native-English-span operations**, with no changes to the corrected English body. Every target is a unique substring of its native released component; reconstructed spans have balanced TeX groups and math delimiters; the operations have no internal overlap. At this audit snapshot, **{data['exact_printed_operation_spans_present']} of {len(OPERATIONS)}** complete printed target spans occur in the English diplomatic projection. Rerunning this audit after the English build refreshes that integration check.", '',
              f"The stricter component check also passes for **{data['exact_component_projection_checks_passed']} of {len(OPERATIONS)}** operations: the corrected target occurs exactly once in its assigned component, the diplomatic reading adds exactly one occurrence of the printed target relative to that component’s corrected baseline, and the corrected target no longer occurs in that diplomatic component. This distinguishes a correctly placed reconstruction from an unrelated matching phrase elsewhere in the exposé.", '',
              'These operations restore numerical references, bibliography volume numbers, repeated Weil/Weyl misnamings, formal/holomorphic functions, Segre/Veronese, even/odd dimension, alone/zero, irreducible/indecomposable, and the missing nonzero qualification. They also repair incomplete earlier reverse transfers: the cube-root-of-unity prose following mu= and the unattested geometric generic point. The Corollary 6.4 punctuation receives separate treatment because it changes the scope of condition (LV).', '',
              'The corrupt adjective annexe in XX 1.5.3 is retained underlined and untranslated only in diplomatic English under decision ED-EN-XX-ANNEXE. Corrected English remains connected. A determinate replacement such as annexed would add an interpretation absent from the source.', '',
              '## Source operations', '', '| Decision | Location | Source entry | Printed English | Corrected English |', '| --- | --- | --- | --- | --- |']
    for o in OPERATIONS:
        source_id = re.search(r'F7II-[A-Z]+-\d+\.\d+', o['source'])[0]
        lines.append('| ' + ' | '.join(cell(x) for x in [o['id'], o['expose'] + ' ' + o['page'], source_id, o['printed'], o['corrected']]) + ' |')
    lines += ['', '## Explicit unchanged-English decisions', '',
              'The complete machine-readable ledger gives a local reason for each exclusion. The following are the entries for which the same English sentence expresses both French readings; they are not unresolved translations.', '',
              '| French entry | Location | Reason |', '| --- | --- | --- |']
    for row in rows:
        if row['status'] == 'same English reading':
            lines.append('| ' + ' | '.join(cell(x) for x in [row['fr_id'], row['expose'] + ' ' + row['folio'], row['reason']]) + ' |')
    lines += ['', '## Limits', '', data['limits'], '',
              'The classification uses complete annotated French variant blocks, so the position of each changed token is checked in its true TeX context. The formula-context scanner includes multline and TikZ environments. Every primary prose candidate and every mapped numeric-reference candidate has an explicit reviewed disposition; no candidate is silently accepted by a vocabulary-frequency heuristic.', '']
    (OUT / 'EN_NONMATH_AUDIT.md').write_text('\n'.join(lines))
    return data


def run(write_operations=True):
    operations()
    result = audit()
    if write_operations:
        (WORK / 'en_nonmath_resolutions_glossary.json').write_text(json.dumps(OPERATIONS, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['primary_adopt_entries', 'primary_changed_prose_entries', 'mapped_numeric_reference_entries', 'primary_status_counts', 'total_review_rows', 'exact_operations', 'exact_printed_operation_spans_present', 'unreviewed_prose_entries']}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reports-only', action='store_true', help='Refresh audit records without rewriting the reconstruction-input ledger.')
    run(write_operations=not parser.parse_args().reports_only)
