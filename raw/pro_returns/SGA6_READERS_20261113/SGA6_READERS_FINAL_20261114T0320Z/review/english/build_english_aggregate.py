#!/usr/bin/env python3
"""Build all reader forms from the assembled exact English annotated master."""
from pathlib import Path
import argparse, hashlib, json, re
from apparatus_macro_state import prepare_macro_states
from build_english_candidates import esc
from english_reader_controls import READER_CONTROLS
from english_typography import render_reviewed

EN = Path(__file__).resolve().parent
ROOT = EN.parents[1]
OUT = EN / 'aggregate'


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def put(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def annotate(source, variants):
    checks = []
    for variant in variants:
        a = source.index(variant['scope_start']) if variant.get('scope_start') else 0
        b = source.index(variant['scope_end'], a) if variant.get('scope_end') else len(source)
        section = source[a:b]
        assert section.count(variant['old']) == 1, (variant['id'], section.count(variant['old']))
        if variant.get('mode') == 'display':
            replacement = ('% Complete display branch ' + variant['id'] + '\n'
                + r'\SGACaptureAppState{' + variant['id'] + '}%\n'
                + r'\ifnum\SGAReaderForm=1\relax\SGAAppMark{' + variant['id'] + r'}\fi' + '\n'
                + r'\ifnum\SGAReaderForm=0\relax' + '\n' + variant['printed'] + '\n'
                + r'\else' + '\n' + variant['corrected'] + '\n' + r'\fi')
        else:
            replacement = r'\var{' + variant['printed'] + '}{' + variant['corrected'] + '}{' + variant['id'] + '}'
        source = source[:a] + section.replace(variant['old'], replacement, 1) + source[b:]
        checks.append(dict(id=variant['id'], unique_anchor=True, mode=variant.get('mode', 'text'),
                           source=variant['source']))
    return source, checks


def apply_layout(source, catalog):
    files = [EN / 'EN_RENDERING_REPAIRS.jsonl', EN / 'EN_AGGREGATE_RENDERING_REPAIRS.jsonl']
    for packet in catalog['packets']:
        candidate = ROOT / packet['directory'] / 'rendering_repairs.jsonl'
        if candidate.exists():
            files.append(candidate)
    applications = []
    for file in files:
        if not file.exists():
            continue
        for line in file.read_text().splitlines():
            repair = json.loads(line)
            a = source.index(repair['scope_start'])
            b = source.index(repair['scope_end'], a)
            part = source[a:b]
            assert part.count(repair['old']) == 1, (repair['id'], part.count(repair['old']))
            source = source[:a] + part.replace(repair['old'], repair['new'], 1) + source[b:]
            applications.append(dict(input=file.relative_to(ROOT).as_posix(), **repair))
    return source, applications


def anchor_heading_folios(source):
    """Keep the four observed displaced labels with their actual headings."""
    records=[]
    observed={'VII':(5,6),'160':(89,90),'365':(198,199),'498':(271,272)}
    for folio,(old_page,heading_page) in observed.items():
        marker=r'\SGAPrintPage{'+folio+'}'
        assert source.count(marker)==1
        a=source.index(marker)
        match=re.search(r'\\(?:sub)*section\*?\{',source[a:])
        assert match and match.start()<500
        b=a+match.end()
        old=source[a:b]
        targets=re.findall(r'\\sgaStableTarget\{[^{}]+\}',old)
        assert len(targets)==1,(folio,targets)
        prefix=old[len(marker):a+match.start()-a]
        residue=re.sub(r'%[^\n]*(?:\n|$)','',prefix)
        for target in targets:residue=residue.replace(target,'')
        assert not residue.strip(),(folio,residue)
        new=old[len(marker):]
        for target in targets:new=new.replace(target,'',1)
        new+=marker+''.join(targets)+' '
        assert source.count(old)==1
        original=source
        source=source.replace(old,new,1)
        assert source.count(new)==1 and source.replace(new,old,1)==original
        records.append(dict(id='EN-HEADING-FOLIO-'+folio,folio=folio,old=old,new=new,
            observed_reading_label_page=old_page,observed_heading_page=heading_page,
            exact_inverse_pass=True,original_source_comment_fixed=True,
            native_target_ids_retained=targets,
            reason='The nonfloating source-folio label was emitted before a heading page break. Move only the generated label and its immediately adjacent nonprinting native target into that same heading argument, keeping the source comment and every original heading token fixed.'))
    return source,records


def start_exposes_on_new_pages(source):
    original=source
    starts={1:'0',78:'I',160:'II',222:'III',274:'IV',297:'V',365:'VI',
            416:'VII',466:'VIII',498:'IX',519:'X',595:'XII',616:'XIII',667:'XIV'}
    records=[]
    for folio,expose in starts.items():
        match=next(m for m in re.finditer(r'%{10}\s+scan idx\s+\d+\s*\|\s*folio\s+(\S+)\s+%{10}',source) if m[1]==str(folio))
        old=match.group()
        inserted='% SGA6 generated exposé-start page '+expose+'\n\\clearpage\n'
        new=inserted+old
        assert source.count(old)==1
        source=source.replace(old,new,1)
        records.append(dict(expose=expose,folio=folio,old=old,new=new,
            generated_prefix=inserted,reason='Start this exposé on a fresh output page so its title, byline and opening paragraph remain together. Original source comment and every author token stay fixed.'))
    restored=source
    for record in reversed(records):
        assert restored.count(record['new'])==1
        restored=restored.replace(record['new'],record['old'],1)
    assert restored==original
    return source,dict(expose_count=14,exact_inverse_pass=True,records=records)


def appendix(variants):
    parts = ['\\ifnum\\SGAReaderForm=1\n\\clearpage\n\\section*{Apparatus}\n']
    for number, variant in enumerate(variants, 1):
        parts.extend(['\\noindent\\begin{minipage}{\\linewidth}\\raggedright\n',
                      '\\SGARestoreAppState{' + variant['id'] + '}%\n',
                      '\\paragraph{[' + str(number) + '] ' + esc(variant['id']) + '}\n'])
        parts.append('Source folio ' + esc(str(variant['page'])) + '. Scan/witness: '
                     + esc(variant['scan_image']) + '\\par\n')
        for label, key in [('Printed reading', 'printed'), ('Corrected reading', 'corrected')]:
            reading = variant[key]
            if variant.get('mode') == 'math':
                reading = '\\(' + reading + '\\)'
            parts.append(label + ': ' + reading + '\\par\n')
        related=variant.get('related_sources',[])
        if isinstance(related,str):related=[related]
        citation='; '.join(dict.fromkeys([variant['source']]+related))
        parts.append('{\\raggedright Source: ' + esc(citation) + '. ' + esc(variant['reason']) + '\\par}\n')
        parts.append('\\end{minipage}\\par\\medskip\n')
    parts.append('\\fi\n')
    return ''.join(parts)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--final',action='store_true')
    args=parser.parse_args()
    books=EN/'final' if args.final else OUT
    books.mkdir(exist_ok=True)
    raw = (OUT / 'SGA6_EN_raw_current.tex').read_text()
    catalog = json.loads((OUT / 'INPUT_CATALOG.json').read_text())
    assert sha(raw) == catalog['raw_current_sha256']
    macro_transports = []
    macro_file = EN / 'EN_AGGREGATE_MACRO_TRANSPORTS.jsonl'
    if macro_file.exists():
        for line in macro_file.read_text().splitlines():
            repair = json.loads(line)
            assert raw.count(repair['old']) == 1, repair['id']
            raw = raw.replace(repair['old'], repair['new'], 1)
            macro_transports.append(repair)
    variants = [json.loads(line) for line in (OUT / 'VARIANTS.jsonl').read_text().splitlines()]
    definitions, macro_states = prepare_macro_states(raw, variants)
    source, anchors = annotate(raw, variants)
    (OUT / 'SGA6_EN_annotated_unrendered.tex').write_text(source)
    source, typography = render_reviewed(source, catalog)
    (OUT / 'SGA6_EN_annotated_rendered.tex').write_text(source)
    source, layouts = apply_layout(source, catalog)
    source, heading_anchors=anchor_heading_folios(source)
    source, expose_starts=start_exposes_on_new_pages(source)
    diagnostic_changes=[]
    for match in re.finditer(re.escape(r'\hfuzz=20pt'),source):
        diagnostic_changes.append(dict(old=r'\hfuzz=20pt',new=r'\hfuzz=0.1pt',
            original_offset=match.start(),reason='Expose small overfull boxes that the inherited20pt tolerance hid; no typesetting or author content changes.'))
    assert len(diagnostic_changes)==3
    source=source.replace(r'\hfuzz=20pt',r'\hfuzz=0.1pt')
    (OUT / 'SGA6_EN_annotated_body.tex').write_text(source)
    modes = READER_CONTROLS + definitions
    numeric_labels = sorted(set(re.findall(r'\\SGAAuthorFoot(?:note|Mark|Text)\{(\d+)\}', source)), key=int)
    modes += ''.join('\\expandafter\\def\\csname SGAAuthorLabel@' + n + '\\endcsname{(\\textsuperscript{' + n + '})}\n' for n in numeric_labels)
    modes += ''.join('\\expandafter\\def\\csname SGAAppNumber@' + v['id'] + '\\endcsname{' + str(n) + '}\n' for n, v in enumerate(variants, 1))
    assert source.count(r'\begin{document}') == source.count(r'\end{document}') == 1
    source = source.replace(r'\begin{document}', '\\usepackage[normalem]{ulem}\n\\usepackage{marginnote}\n\\usetikzlibrary{arrows}\n' + modes + '\n\\begin{document}', 1)
    status = r'''
\begin{center}\Large\bfseries English assembly: verification in progress\end{center}
The complete recorded English reconstruction covers printed folios
1--700, together with all original front and rear leaves.
Final aggregate mathematical, terminology, macro-expansion and PDF checks are
still in progress. This candidate is not the completed reader edition.
\par The three forms use the same annotated master: diplomatic source reading,
corrected reading with apparatus, and corrected reading without that apparatus.
'''
    if args.final:
        status=r'''
\section*{Editorial preface}
This edition reconstructs the English text against the reviewed French source,
including all printed folios 1--700 and the original front and rear matter.
The Introduction, the authors' and editors' notes, and the original additions
are retained in translation. Original source folios remain marked throughout;
the comments for the certified blank leaves are preserved without printing
an empty-leaf label beside subsequent text.

The three reader forms come from this single annotated master. The diplomatic
form follows the printed readings wherever they affect the English. The
corrected form gives the adjudicated readings and their source-linked apparatus.
French spelling or agreement corrections that leave the English unchanged
are recorded in the transfer ledger and create no English variant.
\ifnum\SGAReaderForm=2
\par This reading form retains the corrected text, the Introduction and all
original authorial and editorial matter. It omits only the new variant
apparatus; source folios appear in the margin.
\fi

Some source assertions remain as printed because the examination did not
establish a unique textual emendation. In particular, the accompanying dossier
gives explicit counterexamples for the passages on source folios 431, 443
and 590--592 while retaining the authors' wording in translation. The printed
blank locators on folio 464 and the integral membership assertions on folio 465
are likewise retained, with the exact computations and their limits recorded.
These unchanged passages have no variant entries. The decision records also
identify the other retained mathematical issues and give their source evidence.
'''
        source=source.replace(r'\date{22 July 2026}',r'\date{14 November 2026}',1)
    credits = (EN / 'EN_NEW_EDITION_FRONTMATTER.tex').read_text()
    generated = ('\n% SGA6 generated edition matter begins\n' + status + '\n' + credits
                 + '\n\\clearpage\n% SGA6 generated edition matter ends\n')
    source = source.replace(r'\begin{document}', r'\begin{document}' + generated, 1)
    source = source.replace(r'\end{document}', appendix(variants) + r'\end{document}', 1)
    stem='SGA6_EN_' if args.final else 'DRAFT_SGA6_EN_'
    master = books / (stem+'annotated_master.tex')
    master.write_text(source)
    for form, mode in [('diplomatic', 0), ('corrected_apparatus', 1), ('reading', 2)]:
        (books / (stem + form + '.tex')).write_text(source.replace(
            r'\providecommand{\SGAReaderForm}{1}', r'\providecommand{\SGAReaderForm}{' + str(mode) + '}', 1))
    put(OUT / 'APPARATUS_MACRO_STATES.json', macro_states)
    put(OUT / 'MACRO_TRANSPORT.json', macro_transports)
    put(OUT / 'TYPOGRAPHY_TRANSPORT.json', typography)
    put(OUT / 'LAYOUT_TRANSPORT.json', layouts)
    put(OUT / 'HEADING_FOLIO_ANCHOR_TRANSPORT.json',heading_anchors)
    put(OUT / 'EXPOSE_START_LAYOUT_TRANSPORT.json',expose_starts)
    put(OUT / 'DIAGNOSTIC_TOLERANCE_TRANSPORT.json',diagnostic_changes)
    generation=dict(
        raw_sha256=sha(raw), annotated_master_sha256=sha(source),
        variant_groups=len(variants), sequential_unique_anchors=anchors,
        printed_marker_commands=len(catalog['original_leaf_marker_keys']),
        reviewed_intervals=catalog['reviewed_intervals'], remaining_source_folios=catalog['unreviewed_numeric_folios'],
        generated_credit_placement='Immediately after begin{document}, outside the exact original-front replacement.',
        source_certified_blank_labels_suppressed=['IV', 'VI', 'X', '690', 'rear-715', 'rear-716'],
        book_directory=books.relative_to(ROOT).as_posix(),final_names=args.final,
        verification_scope='Generation receipt only. Compilation and the completed release gates are recorded independently; this receipt does not assert or deny those results.',
        release_status='review/english/final/RELEASE_STATUS.json' if args.final else None)
    put(OUT / 'GENERATION_STATUS.json',generation)
    if args.final:put(books/'GENERATION_STATUS.json',generation)
    print(json.dumps(dict(variants=len(variants), unique_anchors=len(anchors),
                          mapped_typography_groups=typography['mapped_source_outer_groups'],
                          layout_repairs=len(layouts), generated_forms=4)))


if __name__ == '__main__':
    main()
