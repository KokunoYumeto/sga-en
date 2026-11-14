#!/usr/bin/env python3
"""Close IX after personal comparison of all six primary/native page images."""
import re
from review_helpers import Review, base_text

r = Review()
batch = '516_520'
obs = {
1: ('Coproduct sign in the first algebra display', 'The complete primary and native 516 pages show two upright stems on a lower bar. Retain the attached coproduct glyph. The algebra is the character-graded sum of the tensor powers; multiplication sends a tensor in degree k and one in degree l to their tensor product in degree k+l, using the canonical line-bundle evaluation maps for opposite powers.', 'Opening algebra display', 516),
2: ('The explicit second tensor factor is present', 'Both complete 516 images explicitly print the factor with index (2), between those with indices (1) and (n). Retain its restored occurrence. Each multi-index summand remains the ordered tensor product of all the displayed line powers, with the canonical associativity identification.', 'Opening algebra display, second factor', 516),
3: ('First factor without extra enclosing parentheses', 'Both complete 516 images put the tensor exponent after the superscript (1), with no additional parentheses surrounding the F expression. Retain the attached grouping braces, which do not print extra punctuation and denote the identical tensor-power functor.', 'Opening algebra display, first factor', 516),
4: ('Final factor without extra enclosing parentheses', 'Both complete 516 images put the tensor exponent after the superscript (n), with no additional enclosing parentheses. Retain the attached grouping braces and the identical tensor-power functor.', 'Opening algebra display, final factor', 516),
5: ('516 starts with the complete first algebra display', 'The complete 515 and 516 primary/native pairs place the colon after algèbre at the end of 515 and the full A_0 display at the top of 516. Retain the marker before the opening display. Findings 1–4 of this batch have nominal page 515 but actual page 516.', 'Boundary 515/516', 516),
6: ('Coproduct sign in the second algebra display', 'Both complete 516 images show the same two stems on a lower bar in the second algebra. Retain its attached coproduct glyph. The character grading and multiplication are the ones explicitly described for the first display, after the associated-bundle construction.', 'Second algebra display', 516),
7: ('Second display has only the (1) and (n) factors, without extra parentheses', 'Both complete 516 images print the first and last factors separated by tensor dots, without the extra enclosing parentheses of the earlier transcription. Retain the attached expression. The omitted middle factors are exactly those represented by the printed dots, with the same ordered tensor-product associativity maps.', 'Second algebra display, factors', 516),
8: ('Struck flag-scheme D in running prose', 'Both complete 516 images show the doubled D stem and a separately ruled E argument. Retain mathbb D and restore the E rule. The associated quotient P/B maps to the complete-flag scheme by sending a frame modulo its flag stabilizer to the induced flag; the inverse is its sheaf of adapted frames modulo B.', 'The scheme X in the first paragraph', 516),
9: ('Struck flag-scheme D in the diagram', 'Both complete 516 images show the same struck D in the right-hand vertex. Retain it, with the separately observed E rule. The map P/B to the flag scheme is the frame-to-flag isomorphism recorded for the prose occurrence.', 'Right-hand diagram vertex', 516),
10: ('One full stop at the lower right of the diagram', 'Both complete 516 images show the stop beside the final row of the diagram. Retain the attached full stop. All four quotient/structural arrows have the directions shown in the print.', 'End of diagram', 516),
11: ('Fourteen raised filled K dots on 516–518', 'All complete primary/native 516–518 pairs were personally compared: six raised dots on 516, four on 517 and four on 518. Restore exactly these filled raised dots, leaving every lower coherent-group dot unchanged. The comparison sends a locally free class [E] to its coherent class [E]; the module operation sends ([E],[F]) to [E tensor F]. Both maps and their domains remain identical.', 'All raised K occurrences on 516–518', 516),
12: ('Occurrence-specific sheaf rules on 516–517, with the separate X519–520 audit', 'The complete 516 primary/native pair shows E5, F6, L1, A2 and O1 with single rules; 517 has only its final E and O ruled, while each E in the gamma-polynomial class formulas is plain. Restore exactly these occurrences. The cross-exposé part on 519–520 is closed by the personally inspected X records ASTRA-X-0002 and ASTRA-X-0005: 519 has O5/F8, and 520 O7/F5/G8 with the middle G in 1.1.5 visibly plain. The blanket suggestion to underline all G letters is amended by that exact exception. Identity on each sheaf and the class map E to [E] give the explicit notation comparisons.', 'Sheaf notation on 516–520', 516),
13: ('The quotient formula before Lemma 4.2 is inline', 'Both complete 517 images put the K_bullet(Y) formula at the left margin and continue On achève on the same line. Retain the attached inline formula and its one full stop.', 'Before Lemma 4.2', 517),
14: ('Plain Gl with a lower-case l', 'Both complete 517 images print a plain capital G followed by lower-case l. Retain the attached Gl spelling. Its functor on an S-algebra R is Aut_R(R^n), and the notation comparison with the earlier struck Gl sends each invertible matrix to itself.', 'Corollary 4.3', 517),
}
for k, (printed, why, region, page) in obs.items():
    r.finding(batch, k, printed, why, region, witness=page+11,
              actual_page=page,
              verdict='amended' if k == 12 else 'not applied and now applied' if k == 11 else 'confirmed')
    r.decisions[-1]['is_misprint'] = False

def current(page, layer):
    text = base_text(page, layer)
    for p in r.patches:
        if p['page'] == page and p['layer'] in ['both', layer]:
            assert text.count(p['old']) == p['expected_count'], (page, layer, p['source_id'])
            text = text.replace(p['old'], p['new'])
    return text

sid = 'ASTRA-IX-RAISED-K-516-518'
r.own_finding(sid, 516, obs[11][0], r'K^\circ', 'Restore the fourteen observed raised bullets.',
              obs[11][1], obs[11][2], kind='symbol', witness=527)
r.own[-1].update(is_misprint=False, source_pages=[516, 517, 518], observed_occurrences={516:6, 517:4, 518:4})
for page, count in [(516,6),(517,4),(518,4)]:
    r.patch(page, 'both', r'K^\circ', r'K^{\bullet}', sid, obs[11][1], count=count)

def rule_occurrences(text, letter, ordinals, count):
    matches = list(re.finditer(r'(?<![A-Za-z\\])' + letter + r'(?![A-Za-z])', text))
    assert len(matches) == count, (letter, len(matches), count)
    for i, m in reversed(list(enumerate(matches, 1))):
        if i in ordinals:
            text = text[:m.start()] + r'\underline{' + letter + '}' + text[m.end():]
    return text

for page in [516, 517]:
    sid = f'ASTRA-IX-GLYPHS-{page}'
    why = obs[12][1]
    r.own_finding(sid, page, 'The individually observed single rules', 'Plain sheaf letters and mathcal O',
                  'Restore each observed rule, keeping class letters plain.', why,
                  'Sheaf and class notation', kind='font', witness=page+11)
    r.own[-1].update(is_misprint=False, observed_rule_counts={516:{'E':5,'F':6,'L':1,'A':2,'O':1},517:{'E':1,'O':1}}[page])
    for layer in ['diplomatic', 'current']:
        old = current(page, layer)
        assert old.count(r'\mathcal O') == 1
        new = old.replace(r'\mathcal O', r'\underline{O}')
        if page == 516:
            for letter, count in [('E',5),('F',6),('A',2)]:
                new = rule_occurrences(new, letter, set(range(1,count+1)), count)
            new = rule_occurrences(new, 'L', {1}, 2)  # The later L starts the prose word L'homomorphisme.
        else:
            new = rule_occurrences(new, 'E', {4}, 4)
        r.patch(page, layer, old, new, sid, why)

def rules(text, phrases):
    pattern = '(?<![A-Za-zÀ-ÿ])(' + '|'.join(re.escape(x).replace(r'\ ', r'\s+') for x in sorted(phrases, key=len, reverse=True)) + ')(?![A-Za-zÀ-ÿ])'
    return re.sub(pattern, lambda m: r'\uline{' + m[0] + '}', text)

blocks = {
517: [('Lemme 4.2.', 'En effet,', ['Soient','un schéma noethérien',"un sous-groupe parabolique d'un",'-groupe réductif','un torseur sous le radical unipotent','de','alors on a un isomorphisme']),
      ('Corollaire 4.3.', 'Résulte immédiatement', ['Soient','un schéma noethérien',"Alors l'homomorphisme canonique",'est un isomorphisme'])],
518: [('Corollaire 4.4.', 'Si $S$ est régulier', ['Sous les hypothèses de','supposons','régulier','Alors on a un isomorphisme'])]
}
for page, ranges in blocks.items():
    sid = f'ASTRA-IX-WORD-RULES-{page}'
    why = 'Both complete primary/native pages show the recorded separate rules on the statement prose. Restore those exact word groups while leaving formulas under their independent glyph decisions. The existing bold named-statement labels follow the accepted NOTE_6 convention; paragraph numbers and the internal reference 4.1 receive no added rule.'
    r.own_finding(sid, page, 'Individually ruled statement prose', 'Plain statement prose',
                  'Restore the observed word groups.', why, 'Statements 4.2–4.4', witness=page+11)
    r.own[-1]['is_misprint'] = False
    for layer in ['diplomatic', 'current']:
        old = current(page, layer)
        new = old
        for label, end, phrases in ranges:
            a = new.index(r'\textbf{' + label + '}') + len(r'\textbf{' + label + '}')
            b = new.index(end, a)
            new = new[:a] + rules(new[a:b], phrases) + new[b:]
        assert new != old
        r.patch(page, layer, old, new, sid, why)

sid = 'ASTRA-IX-LOCAL-NOTATION-516-518'
why = 'The complete primary/native 516–518 pairs agree on both coproduct glyphs, the separate algebra factors, the struck flag D, the plain Gl on 517, the headless tilde comparison before Lemma 4.2, and the headed tilde arrows in 4.2 and 4.4. Retain each attached form. In the final regular-scheme comparison, the map from locally free/perfect classes to coherent classes is [E] to [E]; the inverse assigns a coherent sheaf the alternating class of its finite locally free local resolution in the perfect-complex group. The stated source reference 4.1 and the words finie car B est noethérien remain the author text. The Exposé X macro block after the 518 text is infrastructure and represents no additional printed matter.'
r.own_finding(sid, 516, 'Local symbols, arrows and literal author wording', 'Attached matching forms',
              'Retain these locally observed forms.', why, 'Local notation and author text', kind='font',
              verdict='confirmed', witness=527)
r.own[-1].update(is_misprint=False, source_pages=[516,517,518])

for page, begins, ends in [(516,'A_0 = coproduct of the indexed line powers','K_bullet(Y) = K_bullet(S) tensor (K^bullet(X)/I).'),
                           (517,'Or d’après VI 4.8','puisqu’alors E = O_S^n.'),
                           (518,'Corollaire 4.4.','d’où le résultat d’après 4.1.')]:
    r.page(page, begins, ends, witness=page+11,
           notes='Complete primary and native pages personally compared. HOLD61, nominally filed under 518, belongs to actual 554 and is already closed in review/expose_x/decisions.jsonl. The final 518 macro definitions are unprinted build infrastructure.')
r.commit()
