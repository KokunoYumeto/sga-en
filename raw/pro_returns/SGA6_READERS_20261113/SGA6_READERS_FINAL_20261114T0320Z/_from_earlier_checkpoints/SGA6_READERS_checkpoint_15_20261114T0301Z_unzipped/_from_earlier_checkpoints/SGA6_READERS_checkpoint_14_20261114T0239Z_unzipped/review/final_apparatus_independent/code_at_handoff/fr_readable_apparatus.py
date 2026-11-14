#!/usr/bin/env python3
"""Readable French alternatives with exact adjudicated source correspondences."""
from pathlib import Path
import hashlib,json,re,collections
from fr_source_links import load_decisions
ROOT=Path(__file__).resolve().parents[1]

def sourced_variants(variants):
    cached=json.loads((ROOT/'records/FR_SOURCE_LINK_CANDIDATES.json').read_text())['variants']
    assert len(cached)==len(variants)
    manual={r['variant_id']:r for r in (json.loads(s) for s in (ROOT/'review/final_apparatus_links/manual_links.jsonl').read_text().splitlines() if s.strip())}
    _,_,decisions=load_decisions()
    report=[]
    for v,c in zip(variants,cached):
        assert (v['id'],v['page'],v['printed'],v['corrected'])==(c['variant_id'],c['page'],c['printed'],c['corrected']),v['id']
        component_proofs=[]
        if v['id'] in manual:
            m=manual[v['id']]
            assert all(v[k]==m[k] for k in ['page','printed','corrected','sha256_printed','sha256_corrected'])
            ids=m['source_ids'];method=m['method'];mapping_reason=m['reason']
        else:
            assert not c['uncovered_edits'],v['id']
            ids=[]
            for e in c['edits']:
                chosen=e['matches'][0]
                ids.append(chosen['source_id'])
                component_proofs.append({**{k:e[k] for k in ['printed_offsets','corrected_offsets','printed','corrected']},'selected_correspondence':chosen})
            ids=list(dict.fromkeys(ids));method='Exact whole-pair replacement or explicitly located literal component correspondence to an adjudicated source.'
            mapping_reason='All character edits have a recorded literal source pair. The selected short-context correspondences were inspected against their complete source pairs; unused candidate aliases are excluded.'
        provenance=[]
        for sid in ids:
            d=decisions[sid]
            assert d.get('image') and d.get('reason'),(v['id'],sid)
            assert not d['verdict'].startswith(('pending','reverted','rejected')),(v['id'],sid)
            assert str(d.get('page')) in [str(v['page']),'front'],(v['id'],sid,d.get('page'),v['page'])
            provenance.append({k:d.get(k,'') for k in ['source_id','page','kind','record_type','type','verdict','printed_reading','change','correction','image','region','reason','review_file','is_misprint','correction_status','source_error_kind','classification_basis','classification_reason','classification_source']})
        v.update(source=ids,status='adjudicated source correspondence complete',source_decisions=provenance,
                 kind=classify(provenance),link_method=method)
        report.append(dict(variant_id=v['id'],page=v['page'],source_ids=ids,kind=v['kind'],
             sha256_printed=v['sha256_printed'],sha256_corrected=v['sha256_corrected'],method=method,
             mapping_reason=mapping_reason,component_proofs=component_proofs,source_decisions=provenance))
    summary=dict(variants=len(variants),sourced_variants=len(report),manual_contextual_links=len(manual),
                 unresolved=0,source_decisions=len({s for r in report for s in r['source_ids']}),
                 by_kind=dict(collections.Counter(r['kind'] for r in report)))
    (ROOT/'records/FR_APPARATUS_SOURCE_LINKS.json').write_text(json.dumps(dict(summary=summary,variants=report),ensure_ascii=False,indent=2)+'\n')
    return variants

def classify(provenance):
    kinds={str(d.get(key,'')) for d in provenance for key in ['kind','source_error_kind']}
    if any('mathematical_source' in k or 'substantive_mathematical' in k for k in kinds):return 'mathematical source correction'
    if any(d.get('is_misprint') is True or d.get('record_type')=='misprint' or d.get('type')=='misprint' or 'misprint' in str(d.get('kind','')) for d in provenance):return 'source misprint correction'
    if kinds & {'font','underline','font_convention','notation','convention','confirmed_notation'}:return 'explicit notation convention'
    return 'adjudicated source correction'

DECLARATION=re.compile(r'^\\(?:newcommand|providecommand|renewcommand|DeclareMathOperator)\*?\s*\{?\\([A-Za-z@]+)',re.M)
COMMAND=re.compile(r'\\([A-Za-z@]+)')

def prepare_macro_states(source,variants):
    from build_french import brace_end
    declarations={}
    for match in DECLARATION.finditer(source):
        # Consume a braced or unbraced command name, optional arity/default,
        # and the complete balanced definition, including the longO newline.
        begin=match.start();i=match.end()
        if source[i:i+1]=='}':i+=1
        while True:
            while i<len(source) and source[i].isspace():i+=1
            if source[i:i+1]=='[':i=brace_end(source,i,'[',']')
            else:break
        assert source[i:i+1]=='{',('unparsed source macro',match[1],source[begin:i+50])
        end=brace_end(source,i)
        declarations.setdefault(match[1],[]).append(source[begin:end])
    managed=set(declarations)
    dependencies={name:set().union(*(set(COMMAND.findall(s)) for s in spans)) & managed for name,spans in declarations.items()}
    definitions=[];records=[]
    for v in variants:
        name=v['id'];selected=set(COMMAND.findall(v['printed']+'\n'+v['corrected'])) & managed
        direct=sorted(selected)
        while True:
            expanded=selected | set().union(*(dependencies[t] for t in selected)) if selected else set()
            if expanded==selected:break
            selected=expanded
        tokens=sorted(selected)
        definitions.append(r'\expandafter\def\csname SGACapture@'+name+r'\endcsname{%'+'\n')
        for t in tokens:definitions.append(r'\global\expandafter\let\csname SGAState@'+name+'@'+t+'\\endcsname\\'+t+'%\n')
        definitions.append('}\n'+r'\expandafter\def\csname SGARestore@'+name+r'\endcsname{%'+'\n')
        for t in tokens:definitions.append('\\expandafter\\let\\expandafter\\'+t+r'\csname SGAState@'+name+'@'+t+r'\endcsname'+'%\n')
        definitions.append('}\n')
        records.append(dict(variant_id=name,direct_source_managed_commands=direct,captured_commands=tokens,relevant_declarations={t:declarations[t] for t in tokens}))
    report=dict(method='Global TeX let at the exact source occurrence and local restoration in its apparatus entry. Balanced multiline declarations are inventoried; TeX determines their active meaning.',
        source_sha256=hashlib.sha256(source.encode()).hexdigest(),source_managed_command_count=len(managed),variant_count=len(variants),variants=records)
    (ROOT/'records/FR_APPARATUS_MACRO_STATES.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return ''.join(definitions)

LEXICAL=re.compile(r"(?:[\w’'.,-]|\\['`^\"~=.uvHckbdrt](?:\{[^{}\s]\}|[^\s{}]))+",re.UNICODE)

def context_and_tail(before,after,left,right):
    from build_french import atoms
    if any(x and not LEXICAL.fullmatch(x) for x in [before,after]):return '', ''
    prefix=[];suffix=[]
    for atom in reversed(atoms(left)):
        if not LEXICAL.fullmatch(atom):break
        prefix.insert(0,atom)
    for atom in atoms(right):
        if not LEXICAL.fullmatch(atom):break
        suffix.append(atom)
    return ''.join(prefix),''.join(suffix)

DISPLAY=re.compile(r'^\s*(?:\\\[|\$\$|\\begin\{(?:align\*?|alignat\*?|equation\*?|gather\*?|multline\*?|displaymath|tikzcd|tikzpicture)\})')

READABLE_MACROS=r'''
\renewcommand{\SGAmark}[1]{\ifmmode\text{\textsuperscript{\hyperlink{SGAApp#1}{[\csname SGANumber@#1\endcsname]}}}\else\textsuperscript{\hyperlink{SGAApp#1}{[\csname SGANumber@#1\endcsname]}}\fi}
\long\def\SGAfirstoftwo#1#2{#1}
\long\def\SGAsecondoftwo#1#2{#2}
\long\def\SGAchoose#1#2{\ifnum\SGAform=0\relax\let\SGAselected\SGAfirstoftwo\else\let\SGAselected\SGAsecondoftwo\fi\SGAselected{#1}{#2}}
\long\def\SGAvar#1#2#3{\csname SGACapture@#3\endcsname\SGAchoose{#1}{#2}\ifnum\SGAform=1\relax\SGAmark{#3}\fi}
\long\def\SGAvarDisplay#1#2#3{\csname SGACapture@#3\endcsname\ifnum\SGAform=1\relax\marginnote{\scriptsize\hyperlink{SGAApp#3}{[\csname SGANumber@#3\endcsname]}}\fi\SGAchoose{#1}{#2}}
'''

def readable_apparatus(variants):
    from build_french import macro_safe,tex_escape
    out=[r'\ifnum\SGAform=1'+'\n'+r'\clearpage\section*{Apparat des lectures}'+'\n',
        "Les nombres entre crochets dans le texte renvoient aux entrées ci-dessous. Chaque entrée donne la lecture imprimée, la lecture corrigée et les identifiants des décisions. Les justifications et les régions des scans figurent dans les tables du dossier. Les conventions de notation explicitement décidées sont également signalées. Un contexte verbal identique est ajouté autour des variantes d’une partie de mot; les alternatives minimales exactes sont conservées dans le maître et dans FR\\_VARIANTS.tsv.\n\n"]
    labels={'mathematical source correction':'Correction mathématique du texte imprimé','source misprint correction':'Correction d’une coquille du texte imprimé','explicit notation convention':'Convention de notation explicitement décidée','adjudicated source correction':'Correction du texte imprimé adjugée'}
    for i,v in enumerate(variants,1):
        out.append(r'\par\addvspace{1.1em}\noindent\begin{minipage}{\linewidth}\small\raggedright'+'\n')
        out.append(r'\hypertarget{SGAApp'+v['id']+r'}{}\textbf{['+str(i)+'] '+v['id']+' — page '+tex_escape(v['page'])+r'}\par'+'\n')
        out.append(r'\csname SGARestore@'+v['id']+r'\endcsname'+'\n')
        # The original author labels and note text are displayed within each
        # alternative, without creating a second book footnote in the apparatus.
        out.append(r'\long\def\SGAAuthorFootnote#1#2{\SGAAuthorLabel{#1}\ #2}\long\def\SGAAuthorFootText#1#2{\SGAAuthorLabel{#1}\ #2}\def\SGAAuthorFootMark#1{\SGAAuthorLabel{#1}}'+'\n')
        for label,key in [('Imprimé','printed'),('Corrigé','corrected')]:
            value=v.get('apparatus_context_prefix','')+v[key]+v.get('marker_tail','')
            out.append(r'\textbf{'+label+r'.}\par\nobreak'+'\n')
            out.append(macro_safe(value) if value else r'\textit{[absence de texte]}')
            out.append('\n\\par\n')
        out.append(r'{\footnotesize '+labels[v['kind']]+r'.\par Sources : '+'; '.join(r'\nolinkurl{'+s+'}' for s in v['source'])+r'.\par}'+'\n')
        out.append(r'\end{minipage}\par'+'\n')
    out.append('\\fi\n')
    return ''.join(out)
