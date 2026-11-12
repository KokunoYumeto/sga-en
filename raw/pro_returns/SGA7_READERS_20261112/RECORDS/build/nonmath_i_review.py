"""Exact Volume-I reference/prose transfer decisions, reviewed against both witnesses."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extend(add, components, fr, coverage, write_inputs=True):
    number = 10
    body_patches = []

    def c(prefix):
        found = [v for k, v in components.items() if k.startswith('components/' + prefix + '_')]
        assert len(found) == 1, prefix
        return found[0]

    def op(prefix, corrected, printed, page, ids, reason):
        nonlocal number
        number += 1
        add(number, prefix, corrected, printed, page, ids, reason)

    def ref(prefix, anchor, visible, printed, page, ids, reason):
        text = c(prefix)['text']
        assert text.count(anchor) == 1, (prefix, anchor)
        a = text.index(anchor)
        pat = re.compile(r'\\SGARef(?:Link|Target)\{[^{}]+\}\{' + re.escape(visible) + r'\}')
        m = pat.search(text, a)
        assert m and m.start() - a < 500, (prefix, anchor, visible)
        corrected = text[a:m.end()]
        new = corrected[:m.start()-a] + m.group().rsplit('{' + visible + '}', 1)[0] + '{' + printed + '}'
        op(prefix, corrected, new, page, ids, reason + ' Only the visible locator changes; the stable internal link key is retained.')

    def patch(suffix, prefix, old, new, printed, page, ids, reason):
        comp = c(prefix)
        assert comp['text'].count(old) == 1, (prefix, old)
        related = [r for r in fr if r['id'] in ids]
        assert len(related) == len(ids)
        row = {'id': 'ED-EN-NONMATH-I-' + suffix, 'language': 'English', 'volume': '7I',
               'component': comp['component'], 'page': str(page), 'old': old, 'new': new,
               'corrected': new, 'printed': printed, 'expected_count': 1,
               'start': comp['text'].index(old),
               'source': '; '.join(sorted({r['source'] for r in related} | {r['source_ref'] for r in related})),
               'french_apparatus_ids': ids, 'reason': reason}
        body_patches.append(row)
        for item in ids:
            coverage[item] = ('corrected_body_repaired_with_paired_diplomatic_reading', row['id'], reason)
        if write_inputs:
            (ROOT / 'work' / ('en_editorial_body_patch_nonmath_i_' + suffix.lower() + '.json')).write_text(json.dumps(row, ensure_ascii=False, indent=2) + '\n')

    ref('06', r'For $\xi=\bar x$, the exact sequence (', '5.2.1', '5.2.2', 18,
        ['F7I-I-027.1'], 'The printed splitting sentence cites 5.2.2; current cites the exact sequence 5.2.1. Both released English branches had the corrected reference.')
    op('71', r'In this case the conclusions of \SGARefLink{sga7.sga7i.evii.n1-3-5}{1.3.5} and \SGARefLink{sga7.sga7i.evii.n1-3-6}{1.3.6}',
        r'In this case the conclusions of \SGARefLink{sga7.sga7i.evii.n1-3-5}{3.5} and \SGARefLink{sga7.sga7i.evii.n1-3-6}{3.6}', 154,
        ['F7I-VII-018.1', 'F7I-VII-018.2'], 'The printed conclusions of 3.5 and 3.6 are corrected to 1.3.5 and 1.3.6. This is the final example in VII1.3.8, not the several unchanged references in VII1.3.7.')
    op('82', 'Then the hypothesis of Proposition 2.9.3 is\nsatisfied',
        'Then the preliminary conditions of 2.9.2 are\nsatisfied', 174,
        ['F7I-VII-040.1', 'F7I-VII-040.2', 'F7I-VII-040.3'], 'Restore the complete printed phrase preliminary conditions of 2.9.2, rather than retaining the corrected proposition description with an obsolete number.')
    ref('82', 'To prove sufficiency, apply Proposition ', '2.9.3', '2.9.2', 175,
        ['F7I-VII-041.1'], 'The first proof reference to proposition part (b) is 2.9.2 in print and 2.9.3 in current.')
    ref('82', 'The\nconclusion follows from Proposition ', '2.9.3', '2.9.2', 175,
        ['F7I-VII-041.2'], 'The later conclusion reference to proposition part (b) is independently 2.9.2 in print and 2.9.3 in current.')
    ref('84', 'The isomorphism (', '3.1.8', '3.1.7.1', 182,
        ['F7I-VII-048.1'], 'The functoriality sentence cites 3.1.7.1 in print and 3.1.8 in current.')
    ref('86', 'belongs to a short exact sequence as in\n', '3.3.2.1', '3.2.3', 187,
        ['F7I-VII-055.1', 'F7I-VII-055.2'], 'The short-exact-sequence hypothesis cites 3.2.3 in print and 3.3.2.1 in current.')
    ref('86', 'left exactness stated in ', '3.3.2.1', '3.2.3', 187,
        ['F7I-VII-055.3', 'F7I-VII-055.4'], 'The concluding left-exactness reference repeats the printed 3.2.3, corrected to 3.3.2.1.')
    ref('94', 'The last term of (', '1.3.5', '1.3.4', 223,
        ['F7I-VIII-004.1'], 'The projective-system explanation cites 1.3.4 in print and 1.3.5 in current.')
    ref('98', 'symmetry properties of the pairings (', '2.2.5', '2.2.4', 238,
        ['F7I-VIII-018.3'], 'The first pairing in the symmetry sentence is numbered 2.2.4 in print and 2.2.5 in current; the second reference 2.2.6 is unchanged.')
    ref('100', r'\underline{Proof of ', '2.3.11', '2.5.11', 243,
        ['F7I-VIII-021.1'], 'The proof heading itself has the printed 2.5.11, corrected to 2.3.11.')
    ref('112', 'therefore the left annihilator of (', '4.11.1', '1.11.1', 274,
        ['F7I-VIII-040.1'], 'This is the conclusion identifying the left annihilator as an inverse image, where print has 1.11.1. The other nearby references to 4.11.1 are unchanged.')
    ref('115', 'clear from the form (', '5.7.2', '2.7.2', 285,
        ['F7I-VIII-050.1'], 'The represented-functor sentence cites 2.7.2 in print and 5.7.2 in current.')
    ref('117', 'Since the description in ', '6.2', '3.2', 289,
        ['F7I-VIII-056.5'], 'The base-change compatibility sentence cites the description in 3.2 in print and 6.2 in current.')
    ref('132', 'unipotent rank zero\n(cf. ', '2.1.5', '1.5.5', 329,
        ['F7I-IX-014.1', 'F7I-IX-014.2'], 'The p-divisibility discussion cites 1.5.5 in print and 2.1.5 in current.')
    ref('133', r'$\operatorname{Hom}_S(\widetilde S,A)=A(\widetilde K)$, which proves' + '\n(', '2.2.5.1', '6.2.5.1', 333,
        ['F7I-IX-016.1'], 'The final equality reference in this argument is 6.2.5.1 in print; the equation label and preceding references are already 2.2.5.1 in both witnesses.')
    ref('134', 'invariants under the inertia group $I$ (', '2.2.5', '1.6.5', 337,
        ['F7I-IX-020.2', 'F7I-IX-020.3'], 'The invariants sentence cites 1.6.5 in print and 2.2.5 in current. The separately transferred parenthesis repair from the same source item does not cover this reference.')
    op('138', 'Indeed, to prove that (vi) implies (iv),', 'Indeed, to prove that (v) implies (vi),', 353,
        ['F7I-IX-036.1', 'F7I-IX-036.2'], 'Restore the printed direction and the two printed Roman-numbered conditions as one operation; changing only one numeral would fabricate a third implication.')
    ref('139', 'Then, by the Galois criterion for semistable\nreduction (', '3.5', '4.5', 356,
        ['F7I-IX-039.1'], 'This is the later Galois-criterion reference after passage to K prime, printed 4.5 and corrected 3.5; the earlier reference remains unchanged.')
    ref('148', "``essentially good reduction over $S$'' in the sense of ", '5.12', '6.5', 398,
        ['F7I-IX-074.2', 'F7I-IX-074.3'], 'The definition of essentially good reduction is cited as 6.5 in print and 5.12 in current.')
    ref('155', 'toric parts of $T_{\\ell}(A_K)$ (', '6.3', '6.5', 414,
        ['F7I-IX-088.1'], 'The second definition reference for the essentially fixed and toric parts is 6.5 in print and 6.3 in current.')
    ref('155', r'$T_\ell(A_K)/T_\ell(A_K)^{ef}$, (', '6.3.2', '6.5.2', 415,
        ['F7I-IX-089.1'], 'The third-quotient sentence cites 6.5.2 in print and 6.3.2 in current.')
    ref('160', 'to $S$ if and only if the pairings (', '9.4.7.2', '9.4.6.2', 432,
        ['F7I-IX-111.1'], 'The final proof sentence prints 9.4.6.2. The English release already explained the misprint in an editorial footnote but had not restored it in diplomatic body text.')
    ref('161', 'follows immediately from ', '9.4.7', '9.4.6', 434,
        ['F7I-IX-113.1'], 'The proof of the first assertion of 9.5.6 prints 9.4.6, corrected to 9.4.7. An explanatory editorial footnote is separate from the required body variant.')
    ref('161', 'One then sees that the homomorphism\n(', '9.5.5', '9.5.6', 436,
        ['F7I-IX-116.1'], 'The homomorphism interpreting the inertia action is called 9.5.6 in print and 9.5.5 in current; the English editorial footnote alone did not reconstruct the printed body.')
    ref('163', 'is of course precisely the monodromy pairing (', '9.1.2', '9.2.1', 441,
        ['F7I-IX-121.3', 'F7I-IX-121.4'], 'The identification following 10.2.7 prints 9.2.1, corrected to the pairing 9.1.2. Earlier uses of 9.1.2 in this component are unchanged.')
    ref('168', 'without any restriction on $\\ell$. As in ', '11.3', '11.4', 454,
        ['F7I-IX-132.1'], 'The sentence inside 11.4 refers to 11.4 in print and to the preceding construction 11.3 in current.')
    ref('170', 'which is the generic fibre of (', '11.6.5', '11.7.5', 460,
        ['F7I-IX-137.1'], 'The generic-fibre locator is 11.7.5 in print and 11.6.5 in current.')
    ref('170', 'The construction made in ', '11.6', '11.7', 461,
        ['F7I-IX-138.1'], 'At the opening of Remarks 11.7, the print says the construction made in 11.7; current corrects the locator to 11.6.')
    for visible, printed, fid in [('12.3.3', '12.2.3', 'F7I-IX-149.1'), ('12.3.4', '12.2.4', 'F7I-IX-149.2')]:
        target = '\\SGARefTarget{sga7.sga7i.eix.n' + visible.replace('.', '-') + '}{' + visible + '}'
        op('173', target, target.rsplit('{'+visible+'}',1)[0] + '{'+printed+'}', 471, [fid],
           'Restore the printed equation label ' + printed + ' itself. The corrected label ' + visible + ' is retained in the corrected body and as the stable nonprinting anchor key; the separate explanatory footnote is not a substitute for this label variant.')
    ref('178', 'a), b), and c) of ', '13.2.1', '13.2.2', 489,
        ['F7I-IX-172.1'], 'Corollary 13.2.2 refers to its own number in print and to the conditions of Lemma 13.2.1 in current.')
    ref('184', 'In\n', '7.2.2', '7.22', 517,
        ['F7I-IX-199.1'], 'The construction of G is cited as 7.22 in print and 7.2.2 in current.')
    op('184', r'Consequently (\SGARefLink{sga7.sga7i.eix.n14-3-5-3}{14.3.5.3}) and (\SGARefLink{sga7.sga7i.eix.n14-3-5-5}{14.3.5.5})',
        r'Consequently (\SGARefLink{sga7.sga7i.eix.n14-3-5-3}{14.3.8}) and (\SGARefLink{sga7.sga7i.eix.n14-3-5-5}{14.3.10})', 518,
        ['F7I-IX-200.3', 'F7I-IX-200.4'], 'Restore both printed references 14.3.8 and 14.3.10 in the sentence constructing the extension; current has 14.3.5.3 and 14.3.5.5.')
    ref('185', "Then $S'$ is a complete trait, and the uniqueness result of ", '14.3.4', '4.3', 520,
        ['F7I-IX-202.1', 'F7I-IX-202.2'], 'The uniqueness argument cites 4.3 in print and 14.3.4 in current.')

    op('05', 'and let $Z$ be the\nnon-smooth locus of $f$.', 'and let $Z$ be the\nnon- locus of $f$.', 16,
        ['F7I-I-022.1'], 'The diplomatic French has the incomplete phrase lieu de non de f; current supplies -lissité. Retain the equally incomplete non- locus in diplomatic English, without silently supplying smooth or inventing an editorial bracket in the authorial body.')
    op('69', 'Let $E$ be a bitorsor under\n$(G_P,G_P)$.', 'Let $E$ be a torsor under\n$G_P$.', 148,
        ['F7I-VII-010.4', 'F7I-VII-010.5', 'F7I-VII-010.6'], 'The formula transfer had restored G_P but left the corrected word bitorsor. Restore the complete printed torsor-under-G_P phrase, preserving the paired correction to bitorsor under (G_P,G_P).')
    op('86', 'cocartesian functors is canonically in bijection with\n', 'cocartesian functors is canonically in bijection with the set of isomorphisms\n', 192,
        ['F7I-VII-060.4'], 'The print incorrectly calls the following Hom set a set of isomorphisms; current says homomorphisms. Native English expresses the corrected Hom-set statement without repeating the noun. Restore the printed isomorphisms claim before the unchanged display in diplomatic English.')
    op('94', 'a\nsimpler interpretation of the next member:', 'a\nsimpler interpretation of the last member:', 223,
        ['F7I-VIII-005.2', 'F7I-VIII-005.3'], 'The displayed D(T_n(P)) definition explains the next member in current, whereas print says the last member. These are distinct terms of the preceding multi-line isomorphism.')
    op('97', 'a functorial injective homomorphism, in the', 'a functorial injective isomorphism, in the', 235,
        ['F7I-VIII-016.1'], 'Print calls the injection an isomorphism; current corrects it to homomorphism. Restore the stronger printed assertion only in diplomatic English.')
    op('114', 'be their groups of connected\ncomponents.', 'be their groups of neutral\ncomponents.', 283,
        ['F7I-VIII-048.2'], 'The component groups Phi and Psi are described as groups of neutral components in print, corrected to connected components. The English release used the corrected description in both branches.')
    op('122', 'defined on the category of extensions by $\\overline G$.', 'defined on the category of biextensions by $\\overline G$.', 300,
        ['F7I-VIII-066.4'], 'The restriction functor in the proof of 7.1(a) is defined on biextensions in print and extensions in current. This substantive category change was absent from diplomatic English.')

    # Names and original-language bibliographical quotations have an exact English
    # counterpart, unlike ordinary French spelling or agreement in translated prose.
    op('02', "when Hironaka's resolution", "when Hironoka's resolution", 2,
        ['F7I-I-001.1'], 'The personal name is printed Hironoka and corrected Hironaka in the source. Preserve that concrete name difference in diplomatic English; the other Hironaka occurrence is unchanged.')
    op('07', "``The irreducibility of the space of", "``The irreductibility of the space of", 24,
        ['F7I-I-034.1'], 'This bibliographical title is already English in the French source. Restore its exact printed misspelling irreductibility, retaining irreducibility in corrected English.')
    op('92', 'Complexe cotangent relatif}, Lecture Notes in Mathematics 79,',
        'Complexe cotangent relatif}, Lectures Notes in Math. 79,', 217,
        ['F7I-VII-078.2', 'F7I-VII-078.3'], 'The series title is original English bibliographical matter: print has Lectures Notes in Math., current has Lecture Notes in Mathematics. Preserve both exact title readings.')
    op('186', "schemes} (notes by I. Coates and O. Jussila), in \\emph{Dix expos\\'{e}s\n  sur la cohomologie des sch\\'{e}mas}, North-Holland Publishing Co.",
        "schémes} (notesby I. Coates and O. Jussila), in \\emph{Dix expos\\'{e}s\n  sur la cohomologie des sch\\'{e}mas}, Noth-Holland Publishing Co.", 521,
        ['F7I-IX-203.1', 'F7I-IX-203.2', 'F7I-IX-203.3'], 'Preserve the three attested printed variants in the original-English title and publisher information of reference [7]: schémes, notesby, and Noth. The human credit names I. Coates and O. Jussila remain exactly present in both readings.')
    op('186', 'Endlichkeitssatz f\\"{u}r eigentliche\n  Abbildungen',
        'Endlichkeitssatzf\\"{u}r eigentliche\n  Abbildnngen', 521,
        ['F7I-IX-204.1', 'F7I-IX-204.2'], 'This German article title is quoted unchanged in language in both readers. Restore the source spelling and word-join defects in the printed branch only.')
    op('186', "d'un faisceau et cohomologie des", "d'un faisceau et et cohomologie des", 522,
        ['F7I-IX-205.1'], 'This French title is quoted, not translated, in the English bibliography. Its printed repeated et therefore has an exact diplomatic counterpart.')
    op('186', '(1962), Hermann, Paris.', '(1962), Herman, Paris.', 523,
        ['F7I-IX-206.1'], 'Restore the printed publisher name Herman, corrected to Hermann, in the original bibliographical citation.')

    op('159', 'It remains to prove (c).', 'It remains to prove (d).', 425,
        ['F7I-IX-103.1'], 'This single-letter change is a reference to the assertion being proved, not a formula variable. The final proof paragraph prints (d), corrected to (c); restore (d) in the diplomatic body.')

    # Source-reference clauses suppressed or misread by the released translation.
    old = 'The asserted properties of the fibres follow from (a)--(c).'
    new = 'Conditions (ii) and (iii) are precisely conditions (b) and (c).'
    printed = 'Conditions (i) and (ii) are precisely conditions (a) and (b).'
    patch('II26', '08', old, new, printed, 26, [f'F7I-II-001.{i}' for i in range(1,5)],
          'Restore the source statement identifying the two pairs of conditions. The release generalized it to (a)--(c), losing both the corrected identification and the printed erroneous indices. The corrected and diplomatic branches now explicitly preserve their respective four labels.')
    old = 'If $n\\geq3$, the $P_i$ are abelian schemes over a scheme $S$, and\n$G=\\underline G_{m,S}$, every $n$-extension of\n$(P_1,\\ldots,P_n)$ by $G$ is \\underline{trivial}.'
    new = 'If $n\\geq3$, the $P_i$ are abelian schemes over a scheme $S$, and\n$G=\\underline G_{m,S}$ is the multiplicative group over $S$\n(compare \\SGARefLink{sga7.sga7i.evii.n2-9-3}{2.9.3}), every $n$-extension of\n$(P_1,\\ldots,P_n)$ by $G$ is \\underline{trivial}.'
    printed = 'If $n\\geq3$, the $P_i$ are abelian schemes over a scheme $S$, and\n$G$ is the multiplicative group over $\\underline G_m$\n(compare \\SGARefLink{sga7.sga7i.evii.n2-9-3}{2.9.2}), every $n$-extension of\n$(P_1,\\ldots,P_n)$ by $G$ is \\underline{trivial}.'
    patch('VII177', '83', old, new, printed, 177, [f'F7I-VII-044.{i}' for i in range(1,4)],
          'The released translation omits the comparison reference. Restore its corrected 2.9.3 and printed 2.9.2 readings together with the explicit group description. This complete clause retains the wrong printed base already reconstructed by G023 and supersedes that narrower operation without losing it.')
    old = 'diagram (\\SGARefTarget{sga7.sga7i.eviii.n2-1-11-2}{2.1.11.2}) symmetric to (\\SGARefLink{sga7.sga7i.eviii.n2-1-11-1}{2.1.11.1}) is commutative; it has the\nsame vertices except that the upper vertex'
    new = 'diagram (\\SGARefTarget{sga7.sga7i.eviii.n2-1-11-2}{2.1.11.2}) symmetric to (\\SGARefLink{sga7.sga7i.eviii.n2-1-11-1}{2.1.11.1}) is commutative; it has the\nsame vertices as (\\SGARefLink{sga7.sga7i.eviii.n2-1-11-1}{2.1.11.1}), except that the upper vertex'
    printed = new.replace('}{2.1.11.2}', '}{2.11.2}').replace('}{2.1.11.1}', '}{2.11.1}')
    patch('VIII232', '96', old, new, printed, 232, [f'F7I-VIII-013.{i}' for i in range(1,4)],
          'Restore the third explicit source locator, which native English compressed into same vertices, and preserve all three corrected/printed reference displays together. The existing equation target key is kept stable.')
    old = 'the special fibers: namely, that the inclusion\n'
    new = 'the special fibers: namely, that the inclusion already obtained (\\SGARefLink{sga7.sga7i.eix.n2-4-7}{2.4.7})\n'
    printed = new.replace('}{2.4.7}', '}{1.10}')
    patch('IX340', '134', old, new, printed, 340, ['F7I-IX-023.2', 'F7I-IX-023.3'],
          'Restore the prose reference already obtained (2.4.7), omitted in the native paraphrase. Print instead cites (1.10). The following displayed inclusion is numbered 2.4.7 in both source witnesses and remains unchanged.')
    old = r'already considered in \SGARefLink{sga7.sga7i.eix.n4-1}{4.1}.'
    new = r'already considered in \SGARefLink{sga7.sga7i.eix.n14-1}{14.1}.'
    printed = r'already considered in \SGARefLink{sga7.sga7i.eix.n14-1}{4.1}.'
    patch('IX512', '183', old, new, printed, 512, ['F7I-IX-194.4'],
          'The released English retained the printed 4.1 despite the corrected French reference 14.1 to the earlier definition of E_K. Correct the English displayed reference and link target to 14.1; retain the printed visible 4.1 only in the diplomatic branch.')
    return body_patches
