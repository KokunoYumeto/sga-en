#!/usr/bin/env python3
"""Compare both assembled English branches with exact final reviewed French."""
from collections import Counter
from pathlib import Path
import hashlib, json
from english_typography import MARK, render_reviewed
from source_emphasis import MATH, underline_words
from reviewed_french import load_reviewed_pages

EN = Path(__file__).resolve().parent
ROOT = EN.parents[1]
OUT = EN / 'aggregate'


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def main():
    raw = (OUT / 'SGA6_EN_raw_current.tex').read_text()
    catalog = json.loads((OUT / 'INPUT_CATALOG.json').read_text())
    variants = [json.loads(x) for x in (OUT / 'VARIANTS.jsonl').read_text().splitlines()]
    pairs = json.loads((EN / 'EN_APPROVED_LEXICAL_MATH_PAIRS.json').read_text())
    additional_pairs = EN / 'EN_AGGREGATE_LEXICAL_MATH_PAIRS.json'
    if additional_pairs.exists():
        pairs.extend(json.loads(additional_pairs.read_text()))
    for packet in catalog['packets']:
        path = ROOT / packet['directory'] / 'lexical_math_pairs.json'
        if path.exists():
            pairs.extend(dict(pair, packet=packet['directory']) for pair in json.loads(path.read_text()))
    # Carry the already approved complete lexical units through the exact new
    # word-wrapper and display-side ordinary-label transport.
    pair_transports = []
    for pair in pairs:
        for key in ['French_literal_unit', 'English_literal_unit']:
            old = pair[key]
            new, stats = underline_words(old)
            if pair['page'] == 605:
                new = new.replace(r'\textbf{3.2.}', r'\textnormal{3.2.}')
            pair[key] = new
            if old != new:
                pair_transports.append(dict(page=pair['page'], key=key, old=old, new=new,
                    source='Final inspected lexical word wrappers; or the source605 ordinary display-side label.'))
    counts, differences, references, branches, source_states = [], [], {}, {}, {}
    for layer, key in [('current', 'corrected'), ('diplomatic', 'printed')]:
        text = raw
        for variant in variants:
            a = text.index(variant['scope_start']) if variant.get('scope_start') else 0
            b = text.index(variant['scope_end'], a) if variant.get('scope_end') else len(text)
            section = text[a:b]
            assert section.count(variant['old']) == 1, (layer, variant['id'])
            text = text[:a] + section.replace(variant['old'], variant[key], 1) + text[b:]
        text, typography = render_reviewed(text, catalog, layer)
        (OUT / f'MATERIALIZED_{layer}_before_layout.tex').write_text(text)
        (OUT / f'TYPOGRAPHY_{layer}.json').write_text(json.dumps(typography, ensure_ascii=False, indent=2) + '\n')
        branches[layer] = sha(text)
        marks = list(MARK.finditer(text))
        pages = {int(m[1]): text[m.end():marks[i + 1].start() if i + 1 < len(marks) else len(text)]
                 for i, m in enumerate(marks) if m[1].isdigit()}
        french, reference = load_reviewed_pages(700, layer, start=1)
        source_states[layer] = reference
        for page in catalog['reviewed_numeric_folios']:
            fu = Counter(m.group() for m in MATH.finditer(french[page]))
            eu = Counter(m.group() for m in MATH.finditer(pages[page]))
            missing, extra = fu - eu, eu - fu
            approved = {}
            for pair in pairs:
                if pair['page'] != page or pair.get('layer', 'both') not in [layer, 'both']:
                    continue
                f, e, n = pair['French_literal_unit'], pair['English_literal_unit'], pair['expected_multiplicity']
                if missing[f] == extra[e] == n:
                    approved['French', f] = pair['status']
                    approved['English', e] = pair['status']
            for side, units in [('French', missing), ('English', extra)]:
                for unit in units.elements():
                    differences.append(dict(layer=layer, page=page, side=side, literal_unit=unit,
                        status=approved.get((side, unit), 'unreviewed literal difference')))
            counts.append(dict(layer=layer, page=page, French_math_units=sum(fu.values()),
                English_math_units=sum(eu.values()), unmatched_French_units=sum(missing.values()),
                unmatched_English_units=sum(extra.values())))
            references[layer, page] = sha(french[page])
    result = dict(
        scope=catalog['reviewed_intervals'], remaining_folios=catalog['unreviewed_numeric_folios'],
        method='Complete literal mathematical-unit multisets in both final source branches, including starred align/equation environments; every character and whitespace byte retained.',
        source_basis='Final reviewed French loader, including exact global convention patches; the preserved English raw contribution bases remain independently available.',
        English_branch_sha256s=branches, counts=counts, differences=differences,
        unexpected_difference_units=sum(x['status'] == 'unreviewed literal difference' for x in differences),
        approved_lexical_difference_side_units=sum(x['status'] != 'unreviewed literal difference' for x in differences),
        complete_lexical_pair_records=len(pairs), exact_pair_wrapper_transports=pair_transports,
        French_page_sha256s=[dict(layer=k[0], page=k[1], sha256=v) for k, v in references.items()],
        limitation='Literal content and exact wrapper transport check, before measured presentation-only line-break repairs. It does not independently certify image reading, semantic prose, macro expansion, glossary completeness or final PDF typography.')
    (OUT / 'LITERAL_MATH_VERIFICATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'FRENCH_SOURCE_STATES.json').write_text(json.dumps(source_states, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['scope', 'unexpected_difference_units', 'approved_lexical_difference_side_units', 'complete_lexical_pair_records']}))
    for difference in differences:
        if difference['status'] == 'unreviewed literal difference':
            print(json.dumps(difference, ensure_ascii=False))
    if result['unexpected_difference_units']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
