#!/usr/bin/env python3
"""Record additional glossary phrases from inspected, exactly paired passages.

This changes glossary evidence only. All source positions refer to the frozen
corrected English and the supplied corrected French; neither body is edited.
"""
from pathlib import Path
import bisect, json
import build_glossary as g

OUT = Path(__file__).parent
E = (OUT / 'EN_corrected_flat.tex').read_text()
F = Path('work/sources/SGA5_FR/fr/sga5/current/s5.tex').read_text()
pages = g.p.getpages(F)
ea = E.index(r'\phantomsection\addcontentsline{toc}{section}{Exposé I ---')
eb = E.index(r'\section*{Terminological Index}')
ev, ep = g.view(E, ea, eb)
fv, fp = g.view(F, pages[1]['start'], pages[481]['start'])
folios = list(pages)
starts = [v['start'] for v in pages.values()]

CANDIDATES = [
    ('cohomologie étale', 'étale cohomology',
     'Exposé I, Introduction; the opening biduality sentence and the shared citation SGA A XVIII.'),
    ('cohomologie galoisienne', 'Galois cohomology',
     'Exposé I, the paragraph citing SGAA VIII 2 and using the identical objects U, G, and A_U.'),
    ('radiciel|radicielle|radiciels|radicielles', 'radicial',
     'Exposé I, Lemma 1.14(b); the same factorization X_i --u_i--> X_i prime --v_i--> Y_i and the property of u_i.'),
    ('strictement parfait|strictement parfaite|strictement parfaits|strictement parfaites', 'strictly perfect',
     'Exposé III B, 5.6(b); both passages explicitly make formula 5.6.4 concrete for the same E and then set E=A.'),
    ('amplitude parfaite finie', 'finite perfect amplitude',
     'Exposé III B, 5.6; the same full subcategory D(A)_parf and the following trace formula (5.6.1).'),
    ('essentiellement constant|essentiellement constante|essentiellement constants|essentiellement constantes', 'essentially constant',
     'Exposé V, Definition 4.1.2; the same projective system X indexed by Z and transition arrow X_s to X_r.'),
    ('catégorie quotient|catégories quotients', 'quotient category|quotient categories',
     'Exposé VI, 1.4.6; the same L, A, constructible L-sheaves, constructible A-sheaves and torsion A-sheaves.'),
    ('pro-objet|pro-objets', 'pro-object|pro-objects',
     'Exposé III, 6.2; the same (u,v), types (2,1) and (3,4), proper f and the f_! construction.'),
    ("lemme d'Artin-Rees", 'Artin-Rees lemma',
     'Exposé V, heading 4.2 and Lemma 4.2.6, with the same projective systems adapted to J.'),
    ('homéomorphisme universel|homéomorphismes universels', 'universal homeomorphism|universal homeomorphisms',
     'Exposé XV, the same relative Frobenius arrow Fr_{X/S}:X to X^{(p/S)} and the adjacent integral/surjective/radicial wording.'),
    ('clôture intégrale', 'integral closure',
     'Exposé VI, 1.4.6; the same coefficient ring A, Z_ell and extension L. The other French headword cloture normale at folio 470 remains separately recorded.'),
    ('complexe filtré|complexes filtrés', 'filtered complex|filtered complexes',
     'Exposé III B, the same underlined u and v, filtered correspondences, and cross-reference III 4.13.'),
    ('sous-catégorie triangulée épaisse|sous-catégories triangulées épaisses', 'thick triangulated subcategory|thick triangulated subcategories',
     'Exposé VIII, Proposition 3.1; the identical categories A, B, quotient A/B and functors Q and i.'),
]

rows = []
for n, (fs, es, basis) in enumerate(CANDIDATES, 1):
    fforms, eforms = fs.split('|'), es.split('|')
    fh = sorted(x for term in fforms for x in g.hits(fv, fp, term))
    eh = sorted(x for term in eforms for x in g.hits(ev, ep, term))
    assert fh and eh, (fs, es)
    fpos, epos = fh[0][0], eh[0][0]
    rows.append({
        'id': f'BODY-AUDIT-{n:03d}', 'French_term': fforms[0],
        'French_search_forms': fforms, 'English_search_forms': eforms,
        'paired_evidence': {
            'French_offset': fpos, 'English_offset': epos,
            'French_folio': folios[max(0, bisect.bisect_right(starts, fpos) - 1)],
            'French_context': F[max(0, fpos - 100):fpos + 230],
            'English_context': E[max(0, epos - 100):epos + 230],
            'alignment_basis': basis,
        },
        'disposition': 'Add the attested paired vocabulary and literal counts; preserve all source wording and formulas.',
    })

# The former zero-hit cofibred-category candidate has coordinated noun phrases
# in its exact source. Record those phrases instead of silently inferring hits
# for an absent contiguous French phrase.
coordinate = {
    'id': 'BODY-EXTRA-007',
    'French_term': 'catégorie cofibrée',
    'French_search_forms': ['catégorie cofibrée', 'catégories cofibrées',
                           'catégories fibrées et cofibrées', 'catégories fibrées ou cofibrées',
                           'catégorie fibrée et cofibrée'],
    'English_search_forms': ['cofibred category', 'cofibred categories'],
    'paired_evidence': {
        'French_exact_phrase': 'catégories fibrées et cofibrées',
        'English_exact_phrase': 'fibred and cofibred categories',
        'French_offset': F.index('catégories fibrées et cofibrées'),
        'English_offset': E.index('fibred and cofibred categories'),
        'alignment_basis': 'Exposé III introduction, both paragraphs beginning the description of no. 1; also III 1.4 and 6.2 with the same four arrow types.',
    },
    'disposition': 'Recover coordinated French phrases explicitly; count their complete observed strings and retain the exact fibred/cofibred wording.',
}
for lang, text in [('French', F), ('English', E)]:
    pos = coordinate['paired_evidence'][lang + '_offset']
    coordinate['paired_evidence'][lang + '_context'] = text[pos - 100:pos + 230]
coordinate['paired_evidence']['French_folio'] = folios[bisect.bisect_right(starts, coordinate['paired_evidence']['French_offset']) - 1]
(OUT / 'GLOSSARY_ADDITIONS.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
(OUT / 'GLOSSARY_COORDINATED_CATEGORY_EVIDENCE.json').write_text(json.dumps(coordinate, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'additional_phrase_families': len(rows), 'recovered_coordinated_family': 1, 'source_bodies_changed': False}))
