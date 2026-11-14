#!/usr/bin/env python3
"""Generate four explicitly unfinished English files from one annotated master.

Only accepted entries in EN_TRANSLATION_PATCHES.jsonl are applied. A future
EN_VARIANTS.jsonl may add scan-decided printed/corrected readings, with exact
old text and a source id. No variant is inferred from the French fix logs.
The incomplete-status notice is deliberately part of every candidate.
"""
from pathlib import Path
import csv
import difflib
import json
import re
from source_emphasis import underline_words
from apparatus_macro_state import prepare_macro_states
from english_reader_controls import READER_CONTROLS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def esc(s):
    # These are literal glyph transports in generated editorial prose only.
    # The original source/reason strings remain exact in the variant records.
    s=s.replace('1\u0332','\ue000').replace('c\u0303','\ue001')
    return ''.join({'\\':r'\textbackslash{}','{':r'\{','}':r'\}','_':r'\_',
                    '%':r'\%','$':r'\$','#':r'\#','&':r'\&','^':r'\textasciicircum{}',
                    '~':r'\textasciitilde{}','≤':r'\ensuremath{\leq}',
                    '≥':r'\ensuremath{\geq}','→':r'\ensuremath{\to}','×':r'\ensuremath{\times}',
                    'λ':r'\ensuremath{\lambda}','−':r'\ensuremath{-}',
                    '∈':r'\ensuremath{\in}','↦':r'\ensuremath{\mapsto}',
                    '≅':r'\ensuremath{\cong}','≃':r'\ensuremath{\simeq}',
                    '⊗':r'\ensuremath{\otimes}','∘':r'\ensuremath{\circ}',
                    'ε':r'\ensuremath{\varepsilon}','τ':r'\ensuremath{\tau}',
                    'α':r'\ensuremath{\alpha}','β':r'\ensuremath{\beta}',
                    '•':r'\textbullet{}','′':r'\ensuremath{\prime}',
                    '²':r'\textsuperscript{2}','¹':r'\textsuperscript{1}',
                    '±':r'\ensuremath{\pm}','·':r'\ensuremath{\cdot}',
                    'Σ':r'\ensuremath{\Sigma}','φ':r'\ensuremath{\varphi}',
                    'ψ':r'\ensuremath{\psi}','″':r'\ensuremath{\prime\prime}',
                    '∧':r'\ensuremath{\wedge}','⊂':r'\ensuremath{\subset}',
                    '⊕':r'\ensuremath{\oplus}','⊣':r'\ensuremath{\dashv}',
                    'γ':r'\ensuremath{\gamma}','η':r'\ensuremath{\eta}',
                    'ι':r'\ensuremath{\iota}','ξ':r'\ensuremath{\xi}',
                    'ρ':r'\ensuremath{\rho}','χ':r'\ensuremath{\chi}',
                    '⁰':r'\textsuperscript{0}','∏':r'\ensuremath{\prod}',
                    '∞':r'\ensuremath{\infty}','≡':r'\ensuremath{\equiv}',
                    '⊔':r'\ensuremath{\sqcup}','δ':r'\ensuremath{\delta}',
                    'Φ':r'\ensuremath{\Phi}','σ':r'\ensuremath{\sigma}',
                    'ℙ':r'\ensuremath{\mathbb P}','∩':r'\ensuremath{\cap}',
                    'ⁿ':r'\textsuperscript{n}','₁':r'\ensuremath{_1}',
                    '√':r'\ensuremath{\surd}','≠':r'\ensuremath{\ne}',
                    'ℓ':r'\ensuremath{\ell}','ₙ':r'\ensuremath{_n}',
                    '⁻':r'\textsuperscript{-}','₂':r'\ensuremath{_2}',
                    '₀':r'\ensuremath{_0}','⁴':r'\textsuperscript{4}',
                    'π':r'\ensuremath{\pi}','Ω':r'\ensuremath{\Omega}',
                    '∨':r'\ensuremath{\vee}','θ':r'\ensuremath{\theta}',
                    '⋯':r'\ensuremath{\cdots}','Γ':r'\ensuremath{\Gamma}',
                    '⋆':r'\ensuremath{\star}','∉':r'\ensuremath{\notin}',
                    'μ':r'\ensuremath{\mu}','κ':r'\ensuremath{\kappa}',
                    '∖':r'\ensuremath{\setminus}','∐':r'\ensuremath{\coprod}',
                    '←':r'\ensuremath{\leftarrow}','⇉':r'\ensuremath{\rightrightarrows}',
                    '⊃':r'\ensuremath{\supset}','↪':r'\ensuremath{\hookrightarrow}',
                    '↝':r'\ensuremath{\rightsquigarrow}','Ĝ':r'\ensuremath{\widehat{G}}',
                    '\ue000':r'\ensuremath{\underline{1}}',
                    '\ue001':r'\ensuremath{\tilde{c}}'}.get(c,c) for c in s)


def write_tsv(path,fields,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
        w.writeheader();w.writerows(rows)


def main():
    source=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
    applied=[]
    for line in (HERE/'EN_TRANSLATION_PATCHES.jsonl').read_text().splitlines():
        p=json.loads(line)
        if not p['status'].startswith('accepted'):
            continue
        count=source.count(p['old'])
        if count!=1:
            raise ValueError(p['id']+': exact anchor count '+str(count))
        source=source.replace(p['old'],p['new'],1)
        applied.append(p)
    reviewed=[p for p in applied if re.fullmatch(r'\d+[–-]\d+',str(p.get('page','')))]
    last_reviewed=reviewed[-1]
    expected_markers=[]
    for p in reviewed:
        first,last=map(int,re.split('[–-]',str(p['page'])))
        expected_markers.extend(range(first,last+1))
    assert expected_markers==list(range(1,expected_markers[-1]+1)), 'Noncontiguous accepted English passage records'
    actual_markers=[int(n) for n in re.findall(r'\\SGAPrintPage\{(\d+)\}',source)]
    assert actual_markers==expected_markers, dict(
        missing_print_markers=sorted(set(expected_markers)-set(actual_markers)),
        unexpected_print_markers=sorted(set(actual_markers)-set(expected_markers)),
        expected_count=len(expected_markers),actual_count=len(actual_markers))
    end=source.index(last_reviewed['new'])+len(last_reviewed['new'])
    source=source[:end]+'% SGA_END_REVIEWED_EN_BODY\n'+source[end:]
    variants=[]
    variant_file=HERE/'EN_VARIANTS.jsonl'
    if variant_file.exists():
        variants=[json.loads(l) for l in variant_file.read_text().splitlines() if l.strip()]
    if len({v['id'] for v in variants}) != len(variants):
        raise ValueError('Duplicate variant id')
    macro_state_definitions,macro_state_record=prepare_macro_states(source,variants)
    (HERE/'EN_APPARATUS_MACRO_STATES.json').write_text(json.dumps(macro_state_record,ensure_ascii=False,indent=2)+'\n')
    for v in variants:
        for required in ['id','old','printed','corrected','source','reason','scan_image','scan_region']:
            if required not in v or (required not in ['printed','corrected'] and not v[required]):
                raise ValueError('Variant lacks evidence field '+required)
        a=source.index(v['scope_start']) if v.get('scope_start') else 0
        b=source.index(v['scope_end'],a) if v.get('scope_end') else len(source)
        scoped=source[a:b]
        count=scoped.count(v['old'])
        if count!=1:
            raise ValueError(v['id']+': exact anchor count '+str(count))
        if v.get('mode')=='display':
            # TikZ-cd reads its column separators directly from the input.
            # Keep both complete displays outside a macro argument, while
            # selecting them with the same master reader-form switch.
            replacement=('% SGA display variant '+v['id']+'\n'
                +r'\SGACaptureAppState{'+v['id']+'}%\n'
                +r'\ifnum\SGAReaderForm=1\relax\SGAAppMark{'+v['id']+r'}\fi'+'\n'
                +r'\ifnum\SGAReaderForm=0\relax'+'\n'+v['printed']+'\n'
                +r'\else'+'\n'+v['corrected']+'\n'
                +r'\fi')
        else:
            replacement=r'\var{'+v['printed']+'}{'+v['corrected']+'}{'+v['id']+'}'
        scoped=scoped.replace(v['old'],replacement,1)
        source=source[:a]+scoped+source[b:]
    a=source.index('%%%%%%%%%%  scan idx 14  |  folio 1')
    b=source.index('% SGA_END_REVIEWED_EN_BODY',a)
    rendered,font_stats=underline_words(source[a:b])
    source=source[:a]+rendered+source[b:]
    rendering_applications=[]
    rendering_file=HERE/'EN_RENDERING_REPAIRS.jsonl'
    if rendering_file.exists():
        for line in rendering_file.read_text().splitlines():
            repair=json.loads(line)
            a=source.index(repair['scope_start'])
            b=source.index(repair['scope_end'],a)
            section=source[a:b]
            assert section.count(repair['old'])==1,(repair['id'],section.count(repair['old']))
            updated=section.replace(repair['old'],repair['new'],1)
            source=source[:a]+updated+source[b:]
            rendering_applications.append(repair)
    (HERE/'EN_RENDERING_REPAIR_APPLICATIONS.json').write_text(json.dumps({
        'scope':'generated presentation only; raw reviewed chunks retain the exact French mathematical units',
        'repairs':rendering_applications},ensure_ascii=False,indent=2)+'\n')
    (HERE/'EN_FONT_RENDERING_RECORD.json').write_text(json.dumps({
        'scope':'fresh English reconstruction, printed1–'+str(last_reviewed['page']).split('–')[-1],
        'basis':'The early reviewer directly confirmed the retained French emphasis groups through77; the coordinator directly confirmed the Exposé I word-group spans in review/expose_i. English retains the corresponding groups. Direct uline commands already present in the reconstructed chunks are preserved separately from the emph groups counted below.',
        'method':'Underline words only; preserve mathematical units literally except the separately recorded emph-to-uline wrappers of inspected lexical words inside text commands. Keep explicit author notes and print markers independent.',
        'counts':font_stats,'volume_wide_font_verification':False},ensure_ascii=False,indent=2)+'\n')
    modes=READER_CONTROLS
    modes+=macro_state_definitions
    numeric_labels=sorted(set(re.findall(r'\\SGAAuthorFoot(?:note|Mark|Text)\{(\d+)\}',source)),key=int)
    modes+=''.join('\\expandafter\\def\\csname SGAAuthorLabel@'+n+'\\endcsname{(\\textsuperscript{'+n+'})}\n' for n in numeric_labels)
    modes+=''.join('\\expandafter\\def\\csname SGAAppNumber@'+v['id']+'\\endcsname{'+str(n)+'}\n' for n,v in enumerate(variants,1))
    source=source.replace(r'\begin{document}',r'\usepackage[normalem]{ulem}'+'\n'+r'\usepackage{marginnote}'+'\n'+modes+'\n'+r'\begin{document}',1)
    credit=(HERE/'EN_NEW_EDITION_FRONTMATTER.tex').read_text()
    status=r'''
\begin{center}\Large\bfseries In-progress collation: unverified candidate\end{center}
This candidate retains the supplied English corpus with the specifically
recorded accepted changes. The complete second scan collation, French-to-English
correction transfer, printed-page alignment and English diplomatic variants
remain unfinished. The form switch is implemented, but these files do not yet
meet the requested completion criteria.
\ifnum\SGAReaderForm=2
\par This reading form keeps the Introduction and the authors' and editors'
text. The completed reading form will omit only the new variant apparatus;
this candidate's verification notice remains visible.
\fi
'''
    # Generated edition matter precedes the exact original-source front span.
    # The full front contribution replaces native matter up to e00.expose;
    # its replacement must never consume these generated credits.
    new_credit=('\n% SGA6 generated edition matter begins\n'+status+'\n'+credit
                +'\n\\clearpage\n% SGA6 generated edition matter ends\n')
    assert source.count(r'\begin{document}')==1
    source=source.replace(r'\begin{document}',r'\begin{document}'+new_credit,1)
    if variants:
        appendix=['\\ifnum\\SGAReaderForm=1\n\\clearpage\n\\section*{Apparatus}\n']
        for n,v in enumerate(variants,1):
            appendix.append('\\noindent\\begin{minipage}{\\linewidth}\\raggedright\n')
            appendix.append('\\SGARestoreAppState{'+v['id']+'}%\n')
            appendix.append('\\paragraph{['+str(n)+'] '+esc(v['id'])+'}\n')
            for label,key in [('Printed reading','printed'),('Corrected reading','corrected')]:
                reading=v[key]
                if v.get('mode')=='math':
                    appendix.append(label+': \\('+reading+'\\)\\par\n')
                else:
                    appendix.append(label+': '+reading+'\\par\n')
            appendix.append('{\\raggedright Source: '+esc(v['source'])+'. '+esc(v['reason'])+'\\par}\n')
            appendix.append('\\end{minipage}\\par\\medskip\n')
        appendix.append('\\fi\n')
        source=source.replace(r'\end{document}',''.join(appendix)+r'\end{document}')
    base=HERE/'DRAFT_SGA6_EN_annotated_master.tex'
    base.write_text(source)
    for form,mode in [('diplomatic',0),('corrected_apparatus',1),('reading',2)]:
        (HERE/('DRAFT_SGA6_EN_'+form+'.tex')).write_text(source.replace(r'\providecommand{\SGAReaderForm}{1}',r'\providecommand{\SGAReaderForm}{'+str(mode)+'}',1))
    rows=[]
    old=(ROOT/'en/release_v2026-11-12/07_SGA6_EN_CURRENT_LAYERED_READER.tex').read_text().splitlines(True)
    new=source.splitlines(True)
    for tag,i,j,a,b in difflib.SequenceMatcher(None,old,new,autojunk=False).get_opcodes():
        if tag=='equal':
            continue
        rows.append({'id':f'EN-CANDIDATE-DIFF-{len(rows)+1:04d}','place':f'released English lines {i+1}-{j}; candidate master lines {a+1}-{b}',
                     'before':''.join(old[i:j]),'after':''.join(new[a:b]),
                     'source':'EN_TRANSLATION_PATCHES.jsonl; EN_NEW_EDITION_FRONTMATTER.tex; source flattening; candidate form controls',
                     'status':'candidate build, not final reader'})
    write_tsv(HERE/'CHANGES_EN_CANDIDATE.tsv',['id','place','before','after','source','status'],rows)
    (HERE/'EN_CANDIDATE_STATUS.json').write_text(json.dumps({'accepted_patch_ids':[p['id'] for p in applied],
        'variant_count':len(variants),'source_differences':len(rows),'printed_markers':source.count('\\SGAPrintPage{'),
        'complete':False,'status':'unfinished; reader completion gates are not met'},indent=2)+'\n')
    print('Applied',len(applied),'reviewed English changes; variants',len(variants),'; candidate files generated.')


if __name__=='__main__':
    main()
