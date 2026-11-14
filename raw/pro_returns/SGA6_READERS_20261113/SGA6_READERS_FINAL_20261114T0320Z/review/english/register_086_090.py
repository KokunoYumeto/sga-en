#!/usr/bin/env python3
"""Record the manually translated 86–90 passage and its exact source transfers."""
from pathlib import Path
import hashlib
import json
import re
from reviewed_french import load_reviewed_pages

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
chunk = (HERE / 'EN_EXPOSE_I_P086_090.tex').read_text()
native = (HERE / 'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
start = native.index(r'We shall say that \(\mathcal C_0\) is \emph{locally stable under kernels of epimorphisms}')
end_anchor = r'\emph{Proof.} The procedure is as follows: first one shows that \(r\) and \(s\) may be chosen locally so as to make \(\Ho^{n+1}(u)\) injective; one verifies '
end = native.index(end_anchor, start) + len(end_anchor)
path = HERE / 'EN_TRANSLATION_PATCHES.jsonl'
patches = [json.loads(x) for x in path.read_text().splitlines()]
record = dict(id='EN-EXPOSE-I-086-090', page='86–90',
    place='Exposé I 1.2 terminology, 1.3 examples and start of extension lemma1.4.1',
    layer='both', old=native[start:end], new=chunk,
    status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
    source='build/page_packets/86–90/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
    reason='Fresh faithful translation preserves all quantifiers, formula placement, underlined category/site/sheaf symbols, four local lifting diagrams, source baseline dots, original starred note89 and observed statement underlining. Explicit variants preserve the printed labels and omitted category/site rules. The source diagram90 retains every X subscript and its unlabelled bottom arrows.')
indices = [i for i, x in enumerate(patches) if x['id'] == record['id']]
if indices:
    patches[indices[0]] = record
else:
    patches.append(record)
path.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in patches))

variants = [json.loads(x) for x in (HERE / 'EN_VARIANTS.jsonl').read_text().splitlines()]
variants = [v for v in variants if not 69 <= int(v['id'].rsplit('-', 1)[1]) <= 78]

def variant(number, page, corrected, printed, source, reason, region):
    assert chunk.count(corrected) == 1, (number, chunk.count(corrected))
    variants.append(dict(id=f'EN-VAR-{number:03}', page=page, old=corrected,
        printed=printed, corrected=corrected, mode='text', source=source, reason=reason,
        scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
        scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',
        scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',
        scan_region=region))

diagram = r'''\[
\begin{tikzcd}
& H_U \arrow[d] \arrow[dl]\\
E_U \arrow[r,"u_U"] & F_U
\end{tikzcd}
\]'''
variant(69, 86, diagram, diagram.replace(r'\arrow[dl]', r'''\arrow[dl,"u"']''').replace(r'\arrow[r,"u_U"]', r'\arrow[r,"U"]'),
    'check/findings/findings_086_090.json#6; review/expose_i/decisions.jsonl',
    'The printed diagonal has label u and the horizontal label is U. The diagonal is the chosen lift H_U→E_U; the horizontal is the pullback u_U:E_U→F_U of u. Current removes the diagonal label and writes u_U horizontally.',
    'second lifting diagram at the bottom of86')
variants[-1]['mode']='display'
variant(70, 88, r'(SGA 4 V 3.11), \(k\)', r'(SGA 4 V 3.11) \(k\)',
    'check/findings/findings_086_090.json#15',
    'The comma separates the topos datum from the following field datum in example c). Its absence is retained diplomatically.', 'example c), opening data')
variant(71, 89, r'\textbf{Lemma 1.3.1.}', r'\textbf{Lemma 1.3.1,}',
    'fixes/MISPRINTS_6.json#123; check/findings/findings_086_090.json#17',
    'The scan has a descending comma after the lemma number. Current uses the full stop separating its label from its statement.', 'Lemma1.3.1 label')
variant(72, 89, r'\uline{-Module. Equivalent conditions}', r'\uline{-Module, Equivalent conditions}',
    'fixes/MISPRINTS_6.json#124; check/findings/findings_086_090.json#18',
    'Both scans print a comma before the new sentence introducing the equivalent conditions. Current supplies a sentence stop.', 'Lemma1.3.1 opening')

site_reason = 'The printed plain S denotes the site governing the fibered categories. The statement later declares the object S to belong to the category underlined-S, identifying that base site. Current restores its individual underline; diplomatic preserves the printed glyph.'
category_reason = 'The printed plain C occurs in the declaration or subsequent mention of the same flat abelian category over the site. Current restores its category underline; diplomatic preserves the plain glyph.'
cases = [
 (73, r'\(\underline{S}\) \uline{be a site,}', r'\underline{S}', 'S', 'ASTRA-I-S-089-PROP', site_reason, 'first site declaration'),
 (74, r'\(\underline{C}\) \uline{a flat abelian}', r'\underline{C}', 'C', 'fixes/MISPRINTS_6.json#125; check/findings/findings_086_090.json#23', category_reason, 'category declaration'),
 (75, r'\(\underline{S}\)\uline{-category (1.1),}', r'\underline{S}', 'S', 'ASTRA-I-S-089-PROP', site_reason, 'base of the flat abelian category'),
 (76, r'\uline{a strictly full additive sub-}\(\underline{S}\)', r'\underline{S}', 'S', 'ASTRA-I-S-089-PROP', site_reason, 'base of the additive subcategory'),
 (77, r'\(\underline{C}\)\uline{; assume that}', r'\underline{C}', 'C', 'fixes/MISPRINTS_6.json#126; check/findings/findings_086_090.json#24', category_reason, 'ambient category of the strictly full subcategory'),
 (78, r'\(\underline{C}\) \uline{(1.2). Let}', r'\underline{C}', 'C', 'fixes/MISPRINTS_6.json#127; check/findings/findings_086_090.json#25', category_reason, 'ambient category for local quasi-lifting'),
]
for number, current, needle, printed, source, reason, region in cases:
    variant(number, 89, current, current.replace(needle, printed), source, reason, 'Proposition1.4.1, ' + region)
variants.sort(key=lambda v: int(v['id'].rsplit('-', 1)[1]))
(HERE / 'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in variants))

pair_path = HERE / 'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs = json.loads(pair_path.read_text())
pair = dict(page=90, French_literal_unit='\\[\n  \\text{et}\\quad s:M\\longrightarrow F_X^n\n\\]',
    English_literal_unit='\\[\n  \\text{and}\\quad s:M\\longrightarrow F_X^n\n\\]',
    expected_multiplicity=1,
    status='confirmed exact lexical translation inside displayed formula; every mathematical token retained',
    scope='Only this complete literal pair and exact occurrence multiplicity are approved; no page-wide exception.')
pairs = [x for x in pairs if x['page'] != 90] + [pair]
pair_path.write_text(json.dumps(pairs, ensure_ascii=False, indent=2) + '\n')

current, reference = load_reviewed_pages(90)
diplomatic, dip_reference = load_reviewed_pages(90, 'diplomatic')
ledger = []
source_patches = [json.loads(x) for x in (ROOT / 'review/expose_i/patches.jsonl').read_text().splitlines()]
for p in source_patches:
    if 86 <= p['page'] <= 90 and p['layer'] in ('current', 'both'):
        ref = [r for r in reference['applied_patches'] if r['page'] == p['page'] and r['source_id'] == p['source_id'] and r['layer'] == p['layer']]
        ledger.append(dict(page=p['page'], source_id=p['source_id'], layer=p['layer'],
            decision='transferred in manually reconstructed English; current-only differences also represented by explicit variants',
            patch_record_sha256s=[r['patch_record_sha256'] for r in ref],
            source_reason=p['reason'], expected_source_count=p.get('expected_count', 1)))
for page in range(86, 91):
    a=chunk.index(f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}')
    b=chunk.index(f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}') if page < 90 else len(chunk)
    body=chunk[a:b]
    counts={}
    for command in (r'\underline{C}', r'\underline{S}', r'\underline{O}', r'\underline{\Hom}'):
        counts[command]=dict(French=current[page].count(command),English=body.count(command))
        assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
    ledger.append(dict(page=page, source_id='exact reviewed page glyph inventory', decision='literal symbol-command multiplicity agrees',
        current_source=reference['bases'][page-1], diplomatic_source=dip_reference['bases'][page-1], counts=counts))
for v in variants:
    if 69 <= int(v['id'].rsplit('-', 1)[1]) <= 78:
        ledger.append(dict(page=v['page'], source_id=v['source'], decision='explicit English printed/corrected variant',
            English_variant=v['id'], printed=v['printed'], corrected=v['corrected']))
ledger.extend([
    dict(page=89, source_id='ASTRA-I-NOTE-089', decision='original baseline parenthesized star and full note restored', English_anchor=r'\SGAAuthorFootnote{*}{Here'),
    dict(page=89, source_id='check/findings/findings_086_090.json#19; check/findings/findings_086_090.json#20', decision='independent Hom underline and baseline argument point retained in both forms', English_anchor=r'\(\underline{\Hom}(P,.)\)'),
    dict(page=89, source_id='ASTRA-I-Z-089', decision='printed single-diagonal plain Z retained in both forms', English_anchor=r'\(n\in Z\)'),
    dict(page=90, source_id='ASTRA-I-TERMS-090', decision='continuous observed underline across the degree n phrase preserved', English_anchor=r'\uline{in degree \(n\) only}'),
    dict(page=90, source_id='ASTRA-I-DOTS-090', decision='all four continuation ellipses on baseline; differential subscripts E_X and unlabelled bottom arrows preserved', English_anchor=r'\begin{tikzcd}[column sep=tiny]'),
])
(HERE / 'EN_EXPOSE_I_TRANSFER_086_090.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
note_path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv'
notes=note_path.read_text().splitlines()
notes=[x for x in notes if not x.startswith('89\t')]
notes.append('89\texample d), after SGA4IV2.10\tbaseline parenthesized star\t1\tASTRA-I-NOTE-089\tcoordinator direct scan comparison, main PDF103 and witness100\tSGAAuthorFootnote{*}\tRestore the original author note concerning the sheaf of rings and its identity element.')
note_path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'], variants=list(range(69,79)), transfer_rows=len(ledger)),ensure_ascii=False))
