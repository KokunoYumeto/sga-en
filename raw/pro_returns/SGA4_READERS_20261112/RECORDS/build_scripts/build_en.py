r"""Generate the three complete English readers from one annotated TeX master.

Run after extract_sources.py. Inputs are always read-only. The generated
master's only form switch is \SGAform (0 diplomatic, 1 apparatus, 2 reading).
"""
import argparse, bisect, collections, difflib, json, re, sys
from pathlib import Path
from en_common import *

OUT=ROOT/'output/en'
OUT.mkdir(parents=True,exist_ok=True)
RECORDS.mkdir(parents=True,exist_ok=True)
changes=[]
variants=[]
page_ledger=[]
source_audit=[]
human_records=[]
notation_decisions=[]

def record(source,expose,page,place,before,after,kind='content'):
    changes.append(dict(page=str(page),place=expose+' '+place,before=before,after=after,source=source,kind=kind))

MARKER_REPAIRS={
 'SGA4_V_LINES_3431_3814_English.texfrag':[
  (r'\item[($\Ll2$)] For every ',r'\item[($\Ll2$)] For every\pageoriginale '),
  ('whose projection in $\\Ss$',r'whose\pageoriginale projection in $\Ss$')],
 'SGA4_VBIS_LINES_2586_2816_English.texfrag':[
  ("it gives an object on $X_0$, two\nobjects on $X_1$", "it gives an object on $X_0$, two\\pageoriginale\nobjects on $X_1$")],
 'SGA4_VI_LINES_2937_3239_English.texfrag':[
  ("$X'$ the family of $u : X''\\to f(X')$ whose source", "$X'$ the family of $u : X''\\to f(X')$\\pageoriginale whose source")],
 'SGA4_IX_LINES_1137_1339_English.texfrag':[
  (r'In \hyperref[IX.prop3.6]{3.6} (i) and (ii)',r'In\pageoriginale \hyperref[IX.prop3.6]{3.6} (i) and (ii)')],
 'SGA4_IX_LINES_1340_1459_English.texfrag':[
  ('of $X$ at $\\bar x$ (VIII 4),\nand $F$', 'of $X$ at $\\bar x$ (VIII 4),\\pageoriginale\nand $F$')],
 'SGA4_XII_LINES_234_382_English.texfrag':[
  ('which, on the initial terms,',r'which,\pageoriginale on the initial terms,')],
 'SGA4_XII_LINES_1925_2169_English.texfrag':[
  ('Noetherian Henselian local subrings $A_i$',r'Noetherian Henselian local subrings\pageoriginale $A_i$')],
 'SGA4_XIII_LINES_317_549_English.texfrag':[
  (r'\item Let $Z_{\circ}$ be the union',r'\item Let\pageoriginale $Z_{\circ}$ be the union')],
 'SGA4_XV_LINES_970_1136_English.texfrag':[
  ('covering of $X=\\PP^1_k$, unramified away', 'covering of $X=\\PP^1_k$,\\pageoriginale unramified away'),
  ('algebraic (necessarily radicial)',r'algebraic (necessarily\pageoriginale radicial)')],
}

def page_markers(s):
    edits=[]
    for f in page_data(s):
        t=f['text'];d=f['file']
        for old,new in MARKER_REPAIRS.get(f['name'],[]):
            assert t.count(old)==1,(f['name'],old)
            t=t.replace(old,new)
            record('EN-PAGE-'+f['name'].split('_LINES_')[1].split('_English')[0],EXPOSE[d],','.join(map(str,f['folios'])),'restored page marker',old,new,'page marker')
        ps=[p for _,_,p in f['fmarkers']]
        if f['name']=='SGA4_XVII_LINES_8201_8600_English.texfrag':ps=ps[:-1]
        if f['name']=='SGA4_XVII_LINES_8601_9000_English.texfrag':
            ps=[next(p for p in PAGES if p['file']=='17' and p['folio']==461)]+ps
        mm=marks(t)
        assert len(mm)==len(ps),(f['name'],len(mm),len(ps))
        es=[]
        for m,p in zip(mm,ps):
            macro='\\SGApage{%s}{%s}{%s}'%(p['tome'],p['expose'],p['folio'])
            es.append((m.start(),m.end(),macro))
            page_ledger.append(dict(tome=p['tome'],expose=p['expose'],page=p['folio'],fragment=f['name'],source='PAGES.json',status='aligned'))
        t=replace_spans(t,es)
        edits.append((f['start'],f['end'],t))
    return replace_spans(s,edits)

def strip_standalone_preambles(s):
    """Retain the book branch of each standalone exposé wrapper exactly."""
    edits=[]
    for m in re.finditer(re.escape(r'\ifx\danslelivre\undefined'),s):
        chapter=re.search(r'\\else\s*\\chapter',s[m.end():m.end()+25000])
        if not chapter:continue
        c=m.end()+chapter.start();before=s[m.end():c]
        if not before.lstrip().startswith(r'\documentclass'):continue
        fi=s.find(r'\fi',c)
        assert fi>=0
        kept=re.sub(r'^\\else\s*','',s[c:fi])
        edits.append((m.start(),fi+len(r'\fi'),kept))
    assert len(edits)==20,len(edits)
    return replace_spans(s,edits)

def add_variant(printed,corrected,source,expose,page,place,kind='correction',credit='AI-produced corrections'):
    if printed==corrected:return printed
    ident='EN-V%05d'%(len(variants)+1)
    variants.append(dict(id=ident,source=source,expose=expose,page=page,place=place,printed=printed,corrected=corrected,kind=kind,credit=credit))
    return r'\SGAvar{'+printed+'}{'+corrected+'}{'+ident+'}'

def source_location(s,pos):
    matches=list(re.finditer(r'\\SGApage\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}',s[:pos]))
    if matches:
        m=matches[-1];return m.group(2),m.group(3)
    return 'I','1'

def restore_archived_human_notes(s):
    path=ROOT/'output/shared/EN_HUMAN_ARCHIVE_NOTE_RESTORATIONS.json'
    if not path.exists():return s
    rows=json.loads(path.read_text())
    if isinstance(rows,dict):rows=rows['records']
    assert len(rows)==5
    (RECORDS/'EN_ARCHIVED_HUMAN_NOTES.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    for row in rows:
        old=row['old_wrapper'];new=row['new_wrapper']
        assert s.count(old)==1,('archived human note anchor',row.get('id'),s.count(old))
        position=s.index(old);exp,page=source_location(s,position)
        s=s.replace(old,new,1)
        record('DEC-EN-HUMAN-NOTE-VISIBILITY; '+row['id']+'; '+row['original_human_note_id'],exp,page,'restore the existing translated human note at its source location',old,new,'human note visibility; argument unchanged')
    inline=r'''\stepcounter{cnote}\textsuperscript{\arabic{cnote}}%
\textup{ [N.D.E.: This exercise does not seem to exist.]}'''
    assert s.count(inline)==1,('inline human note',s.count(inline))
    guarded=r'\SGAeditor{'+inline+'}'
    s=s.replace(inline,guarded,1)
    record('DEC-EN-HUMAN-NOTE-VISIBILITY; A-NDE-04-010','IV',465,'inline human note inside the printed footnote; text retained verbatim',inline,guarded,'human note reading-form guard')
    return s

def restore_commented_print(s):
    # Orgogozo's commented-out diagram is already present verbatim in English.
    idx=s.index('(5.13.2)');a=s.rfind('%\\[',0,idx);b=s.index('%\\]',idx)+len('%\\]')
    old=s[a:b];new=re.sub(r'^%', '',old,flags=re.M)
    record('FR-ED91-I34','I',34,'diagram (5.13.2)',old,new,'restored printed text')
    s=s[:a]+new+s[b:]
    # Exact translation of the paragraph preserved as comments in the French.
    a=s.index('We may suppose that $p>n+1$. Write')
    b=s.index('\nUsing \\hyperref[Vbis.prop3.3.1]',a)
    corrected=s[a:b]
    printed=r'''Now, for every arrow $\iota:i\to j$ of
$\Delta^+_{n+1[p]}$, we have a commutative diagram with exact rows:
\[
\xymatrix@R=.1cm@C=2cm@M=.15cm{
  K'_{\iota} \ar[r]\ar[ddddddd]_{a_{\iota}} & \prod\qquad X'_2 \ar[rr] &  &X'_i \ar[ddddddd]^{f_i}\\
                  & r\in
\ob(\displaystyle{\mathop{\Delta^{+}}_{{n+1}[p]}}) \ar[dddddd]\ar[r]&X'_j
\ar[r]&\\
 & & &\\
 & & &\\
 & & &\\
 & & &\\
 & & &\\
K_{\iota} \ar[r] & \prod\qquad X_2 \ar[rr]& &X_i\\
           & \ob(\displaystyle{\mathop{\Delta^{+}}_{{n+1}[p]}})
\ar[r]&X_j\ar[r]&
}
\]
whose\SGApage{2}{Vbis}{138} left-hand square is Cartesian (either
$i=n+1=j$ and $\iota=\id$, or $i<n+1$ and $f_i$ is an
isomorphism). Using \hyperref[Vbis.prop3.3.1]{3.3.1}, we then see that
$\alpha_\iota$ is a morphism of universal
$G$-$1$-cohomological descent. The proof is completed by observing
that $f_p$ is identified with the canonical morphism
$\displaystyle\mathop{\cap}_{\iota} K'_\iota
\xrightarrow{X\alpha_\iota}\displaystyle\mathop{\cap}_{\iota}K_\iota$.
'''
    corrected=r'\SGApage{2}{Vbis}{138}'+corrected
    source='FR-ED91-Vbis138'
    variant=add_variant(printed,corrected,source,'Vbis',138,'Lemma 3.3.3.3; printed argument and Orgogozo edition rewrite','human editorial rewrite','Fabrice Orgogozo edition; Changement Yves')
    s=s[:a]+variant+s[b:]
    page_ledger.append(dict(tome='2',expose='Vbis',page=138,fragment='SGA4_VBIS_LINES_2586_2816_English.texfrag',source='GLOBAL_ISSUES_SGA.md item 91; PAGES.json',status='restored from commented printed proof'))
    record(source,'Vbis',138,'Lemma 3.3.3.3; paired original and editorial rewrite',corrected.replace(r'\SGApage{2}{Vbis}{138}',''),corrected,'page marker')
    return s

def typography_equivalent(a,b):
    """Explicit typography-only mappings; each retains the printed branch."""
    def plain(x):
        x=re.sub(r'\\(?:textit|textsc|textrm|textup|emph)\{([^{}]*)\}',r'\1',x)
        x=re.sub(r'\\(?:hyperref|eqhyperref)\[[^]]*\]\{([^{}]*)\}',r'\1',x)
        x=re.sub(r'\\(?:,|;|:|!|quad|qquad)|[\s~]','',x)
        return x
    return plain(a)==plain(b)

def sisi_variants(s):
    start=s.index(r'\mainmatter')
    edits=[];number=0
    for m in active_matches(r'\\sisi\b',s[start:]):
        pos=start+m.start()
        if any(a<=pos<b for a,b,_ in edits):continue
        # Definitions are governed separately; do not rewrite parameter text.
        ls=s.rfind('\n',0,pos)+1
        prefix=s[ls:pos]
        if re.search(r'\\(?:def|newcommand|renewcommand|providecommand|DeclareMathOperator)',prefix):continue
        try:
            a,_,ae,_=group(s,pos+len(r'\sisi'))
            b,_,be,_=group(s,ae)
        except ValueError:
            continue
        number+=1;exp,page=source_location(s,pos)
        sid='EN-ORG-%04d'%number
        human_records.append(dict(id=sid,expose=exp,page=page,printed=a,corrected=b,source='released English; Orgogozo edition paired record',credit='Fabrice Orgogozo edition'))
        if typography_equivalent(a,b) or (exp=='IV' and a.strip() in ['IV~','IV'] and not b.strip()):
            repl=a
            if a!=b:record(sid,exp,page,'Orgogozo typography; printed form retained',s[pos:be],repl,'notation / typography')
        else:
            # Some source pairs are character fragments whose braces are sound
            # but whose math delimiters balance only in their larger context.
            repl=add_variant(a,b,sid,exp,page,'Orgogozo paired readings','human editorial correction','Fabrice Orgogozo edition')
        edits.append((pos,be,repl))
    return replace_spans(s,edits)

PREAMBLE=r'''
% Single-source form selector: 0 diplomatic, 1 corrected apparatus, 2 reading.
\providecommand{\SGAform}{1}
\newif\ifSGAdiplomatic
\newif\ifSGAapparatus
\newif\ifSGAreading
\ifnum\SGAform=0\relax\SGAdiplomatictrue\fi
\ifnum\SGAform=1\relax\SGAapparatustrue\fi
\ifnum\SGAform=2\relax\SGAreadingtrue\fi
\long\def\SGAfirst#1#2{#1}
\long\def\SGAsecond#1#2{#2}
\long\def\SGAquietvar#1#2#3{\ifSGAdiplomatic\expandafter\SGAfirst\else\expandafter\SGAsecond\fi{#1}{#2}}
\long\def\SGAvar#1#2#3{\ifSGAdiplomatic\expandafter\SGAfirst\else\expandafter\SGAsecond\fi{#1}{#2\SGAvariantmark{#3}}}
\def\SGAvariantmark#1{\ifSGAapparatus\SGAmark{#1}\fi}
\DeclareRobustCommand{\SGAmark}[1]{\ifmmode\hbox{\raisebox{.5ex}{\hyperlink{app:#1}{\tiny\textdagger}}}\else\textsuperscript{\hyperlink{app:#1}{\tiny\textdagger}}\fi}
\def\SGApagelabel#1#2#3{\raggedright\scriptsize\bfseries #1:#3\ifSGAapparatus\ifcsname SGAdispute#2:#3\endcsname\par\normalfont\tiny\csname SGAdispute#2:#3\endcsname\fi\fi}
\DeclareRobustCommand{\SGApage}[3]{\setcounter{pageoriginal}{#3}\ifmmode\hbox{\marginnote{\SGApagelabel{#1}{#2}{#3}}}\else\marginnote{\SGApagelabel{#1}{#2}{#3}}\fi\xspace}
\long\def\SGAeditor#1{\ifSGAreading\else#1\fi}
\renewcommand{\sisi}[2]{#1}
\def\nde#1{\ifSGAreading\else\stepcounter{cnote}\def\thefootnote{\arabic{cnote}}\protect\footnote[\value{cnote}]{N.D.E. (Fabrice Orgogozo edition): #1}\fi}
\def\ndemark{\ifSGAreading\else\stepcounter{cnote}\def\thefootnote{\arabic{cnote}}\protect\footnotemark[\value{cnote}]\fi}
\def\ndetext#1{\ifSGAreading\else\def\thefootnote{\arabic{cnote}}\protect\footnotetext[\value{cnote}]{N.D.E. (Fabrice Orgogozo edition): #1}\fi}
\providecommand{\theoname}{Theorem}
\providecommand{\propname}{Proposition}
\providecommand{\conjname}{Conjecture}
\providecommand{\coroname}{Corollary}
\providecommand{\lemmname}{Lemma}
\providecommand{\definame}{Definition}
\providecommand{\remaname}{Remark}
\providecommand{\exemname}{Example}
\providecommand{\skippointrait}{\par\smallskip\noindent}
\providecommand{\optexpose}[1]{#1\space}
\providecommand{\labelstyle}{\scriptstyle}
\providecommand{\simarrow}{\rightsquigarrow}
\providecommand{\sheafell}{\underline{\ell}}
\providecommand{\sheafZZ}{\underline{\ZZ}}
\providecommand{\nderef}[1]{the N.D.E.~(\ref{#1}) on page~\pageref{#1}}
\usepackage{fvextra}
\usepackage{marginnote}
\setlength{\marginparwidth}{1.3cm}
\DefineVerbatimEnvironment{SGAReadingCode}{Verbatim}{fontsize=\footnotesize,breaklines=true,breakanywhere=true,commandchars=\\\{\},codes={\catcode`\$=12\catcode`\_=12}}
'''

def frontend(s):
    s=strip_standalone_preambles(s)
    # The release's custom class was deliberately omitted from the upload.
    s=s.replace(r'\documentclass[12pt]{../fichiers-configuration-latex/amsbook}',r'\documentclass[12pt]{amsbook}')
    style=(ENROOT/'fichiers-configuration-latex/smfthm.sty').read_text().split(r'\endinput')[0]
    style=re.sub(r'\\ProvidesPackage\{smfthm\}\[[\s\S]*?\]','',style)
    s=s.replace(r'\usepackage{../fichiers-configuration-latex/smfthm}',r'\makeatletter'+'\n'+style+'\n'+r'\makeatother')
    s=s.replace(r'\setmainlanguage{french}',r'\setmainlanguage{english}')
    s=s.replace(r'\setotherlanguage{english}',r'\setotherlanguage{french}')
    s=s.replace(r'\renewcommand{\sisi}[2]{#2}',r'% The master form selector governs this exposé.')
    s=s.replace(r'\setboolean{original}{false}',r'\setboolean{original}{true}')
    # Keep print notation in macros; the body pairs carry independent variants.
    i=s.index(r'\begin{document}')
    dispute_groups=collections.defaultdict(list)
    for d in json.loads((ROOT/'output/shared/disputes_index.json').read_text()):dispute_groups[(d['expose'],str(d['page']))].append(d['id'])
    dispute_defs=[]
    for (exp,page),ids in dispute_groups.items():
        text=', '.join(r'\hyperlink{'+x+'}{'+x+'}' for x in ids)
        dispute_defs.append(r'\expandafter\def\csname SGAdispute'+exp+':'+page+r'\endcsname{'+text+'}')
    s=s[:i]+PREAMBLE+'\n'+'\n'.join(dispute_defs)+'\n'+s[i:]
    return s

def protected_note_ranges(s):
    out=[]
    for m in active_matches(r'\\(?:nde|ndetext)\b',s):
        try:_,_,b,_=group(s,m.end());out.append((m.start(),b))
        except ValueError:pass
    return out

def replace_pi(s):
    protected=protected_note_ranges(s);edits=[]
    for m in active_matches(r'\\Pi(?![A-Za-z@])',s):
        if any(a<=m.start()<b for a,b in protected):continue
        if re.match(r'_\{\\alpha\}\s*I_\{\\alpha\}',s[m.end():]):continue
        edits.append((m.start(),m.end(),r'\pi'))
    return replace_spans(s,edits),len(edits)

def printed_notation(s):
    from en_extra import page_window
    a=s.index(r'\etiquette[8.13]{I.sec8.13}')
    b=s.index(r'\section{Glossary}',a)
    original_scope=s[a:b]
    selected_counts={name:replace_pi(select_inline_variants(original_scope,corrected))[1] for name,corrected in [('diplomatic',False),('corrected',True)]}
    part,n=replace_pi(original_scope);s=s[:a]+part+s[b:]
    record('FR-ED93-PI','I','136–178','cardinal notation in §§8.13–9',r'\Pi: '+str(n)+' source occurrences',r'\pi; product operator retained','printed notation')
    notation_decisions.append(dict(id='FR-ED93-PI',count_source=n,counts_by_selected_form=selected_counts,scope='I §§8.13–9, original pp.136–178',before=r'\Pi',after=r'\pi'))
    for v in variants:
        if v['expose']=='I' and str(v['page']).isdigit() and 136<=int(v['page'])<=178:
            for field in ['printed','corrected']:v[field]=replace_pi(v[field])[0]
    a,_=page_window(s,'V',65);_,b=page_window(s,'V',80)
    part=s[a:b];notes=protected_note_ranges(part)
    selected_counts={}
    for name,corrected in [('diplomatic',False),('corrected',True)]:
        chosen=select_inline_variants(part,corrected);protected=protected_note_ranges(chosen)
        selected_counts[name]=sum(not any(x<=m.start()<y for x,y in protected) for m in active_matches(r'\\mathsf\{e\}',chosen))
    edits=[(m.start(),m.end(),r'\mathcal{C}') for m in active_matches(r'\\mathsf\{e\}',part) if not any(x<=m.start()<y for x,y in notes)]
    s=s[:a]+replace_spans(part,edits)+s[b:]
    record('FR-ED93-CHAMP','V','65–80','printed champ symbol',r'\mathsf{e}: '+str(len(edits))+' occurrences',r'\mathcal{C}','printed notation')
    notation_decisions.append(dict(id='FR-ED93-CHAMP',count_source=len(edits),counts_by_selected_form=selected_counts,scope='V original pp.65–80',before=r'\mathsf{e}',after=r'\mathcal{C}'))
    for v in variants:
        if v['expose']=='V' and str(v['page']).isdigit() and 65<=int(v['page'])<=80:
            for field in ['printed','corrected']:v[field]=v[field].replace(r'\mathsf{e}',r'\mathcal{C}')
    for pg,label,value in [(492,'IV.sec1','1'),(494,'IV.rem1.8','1.8'),(495,'IV.subsec5.2','5.2')]:
        a,b=page_window(s,'IV',pg);part=s[a:b]
        old=r'\hyperref['+label+']{'+value+'}';new=r'\hyperref['+label+']{IV~'+value+'}'
        count=0;edits=[]
        for m in re.finditer(re.escape(old),part):
            if re.search(r'IV[~\s]*$',part[max(0,m.start()-8):m.start()]):continue
            edits.append((m.start(),m.end(),new));count+=1
        s=s[:a]+replace_spans(part,edits)+s[b:]
        record('FR-ED93-IV'+str(pg),'IV',pg,'printed exposé prefix',old,new,'printed notation')
        notation_decisions.append(dict(id='FR-ED93-IV'+str(pg),count_source=count,before=old,after=new))
    return s

def printed_statement_labels(s):
    pattern=re.compile(r'(\\begin\{enonce\*\}(?:\[[^]]*\])?\{)([A-Za-zÀ-ÿŒœ \n’\-]+)')
    def change(t):return pattern.sub(lambda m:m.group(1)+m.group(2).upper(),t)
    counts={name:sum(m.group(2)!=m.group(2).upper() for m in pattern.finditer(select_inline_variants(s,corrected))) for name,corrected in [('diplomatic',False),('corrected',True)]}
    after=change(s)
    for v in variants:
        for side in ['printed','corrected']:v[side]=change(v[side])
    record('FR-ED93-LABELS','all','all','literal statement labels','Mixed-case literal statement labels','Capital literal statement labels; mathematical tokens and commands unchanged','printed notation')
    notation_decisions.append(dict(id='FR-ED93-LABELS',counts_by_selected_form=counts,before='mixed-case literal heading letters',after='capital literal heading letters'))
    counts={name:len(list(active_matches(r'\\PP\b',select_inline_variants(after,corrected)))) for name,corrected in [('diplomatic',False),('corrected',True)]}
    notation_decisions.append(dict(id='DEC-NOTATION-P',counts_by_selected_form=counts,before=r'\newcommand{\PP}{\mathbf{P}}',after=r'\newcommand{\PP}{P}',scope='single preamble macro; counts include source commands in the preamble and body before appendices'))
    return after

def encoded_macrons(s):
    def encode(x):
        x=re.sub(r'(\{[^{}]+\}|[A-Za-z])\u0304',lambda m:r'\bar{'+m.group(1)+'}',x)
        return x
    for v in variants:
        for side in ['printed','corrected']:
            before=v[side];after=encode(before)
            if before!=after:
                s=s.replace(before,after)
                v[side]=after
                record('DEC-EN-MACRON',v['expose'],v['page'],v['id']+' '+side,before,after,'faithful TeX glyph encoding')
    return s

def apparatus_text():
    out=[r'\ifSGAapparatus',r'\chapter*{Critical apparatus}',r'\addcontentsline{toc}{chapter}{Critical apparatus}',
         'The following entries identify the printed and corrected readings. '+
         'Entries credited to the Fabrice Orgogozo edition preserve the human editorial record. '+
         'AI-produced corrections retain their source identifiers. Literal TeX is used to preserve every symbol exactly.',r'\begingroup\small\raggedright\sloppy']
    for v in variants:
        if v['kind'].startswith('human'):continue
        out.append('\\par\\medskip\\noindent\\hypertarget{app:%s}{}\\textbf{%s}. Exposé %s, printed page %s.\\par'%(v['id'],v['id'],tex_escape(str(v['expose'])),tex_escape(str(v['page']))))
        out.append('Source: '+literal_reading(v['source'])+'. '+literal_reading(v['credit'])+'. '+literal_reading(v['place'])+'.\\par')
        out.append('\\noindent Printed reading: '+literal_reading(v['printed'])+'\\par')
        out.append('\\noindent Corrected reading: '+literal_reading(v['corrected'])+'\\par')
    out.extend([r'\endgroup',r'\fi'])
    return '\n'.join(out)+'\n'

def literal_reading(s):
    from shared_records import tex
    return tex(s).replace('\n',' ').replace(r'\textbackslash{}',r'\allowbreak\textbackslash{}').replace(r'\_',r'\_\allowbreak{}').replace(r'\{',r'\{\allowbreak{}').replace(r'\}',r'\allowbreak{}\}')

def human_dossier():
    out=[r'\ifSGAreading\else',r'\chapter*{Orgogozo edition: human editorial records}',r'\addcontentsline{toc}{chapter}{Orgogozo edition: human editorial records}',
         'This documentary dossier preserves every original paired record in the released English, including typography-only alternatives. It is present in the diplomatic and corrected forms. The body follows the separately recorded decisions on printed notation. These records are credited to the Fabrice Orgogozo edition; the AI apparatus follows separately.',r'\begingroup\small\raggedright\sloppy']
    linked={}
    for v in variants:
        if v['kind'].startswith('human'):
            for source in v['source'].split('; '):linked[source]=v
    rows=list(human_records)
    for v in variants:
        if v['kind']=='human editorial rewrite':rows.append(dict(id=v['source'],expose=v['expose'],page=v['page'],printed=v['printed'],corrected=v['corrected'],credit=v['credit']))
    for h in rows:
        v=linked.get(h['id']);anchor=(r'\hypertarget{app:'+v['id']+'}{}') if v else ''
        out.append(r'\par\medskip\noindent'+anchor+r'\textbf{'+h['id']+'}. Exposé '+str(h['expose'])+', printed page '+str(h['page'])+'. '+literal_reading(h['credit'])+r'.\par')
        out.append(r'\noindent Original first reading: '+literal_reading(h['printed'])+r'\par')
        out.append(r'\noindent Original second reading: '+literal_reading(h['corrected'])+r'\par')
        if v and (v['printed']!=h['printed'] or v['corrected']!=h['corrected']):
            out.append(r'\noindent Body variant after the separately recorded notation and correction decisions. Sources: '+literal_reading(v['source'])+r'.\par')
            out.append(r'\noindent Diplomatic body: '+literal_reading(v['printed'])+r'\par')
            out.append(r'\noindent Corrected body: '+literal_reading(v['corrected'])+r'\par')
    out.extend([r'\endgroup',r'\fi'])
    return '\n'.join(out)+'\n'

def diplomatic_editorial_references():
    """Keep the original human note citations resolvable in diplomatic form."""
    required={'sga4.exp.XVIII.bib.'+x for x in ['0','0bis','0ter','2bis','3bis','3ter','4bis','5bis']}
    records=[];entries=[]
    for h in human_records:
        if h['printed'].strip():continue
        matches=list(re.finditer(r'\\bibitem\{([^}]+)\}',h['corrected']))
        for i,m in enumerate(matches):
            key=m.group(1)
            if key not in required:continue
            end=matches[i+1].start() if i+1<len(matches) else len(h['corrected'])
            entry=h['corrected'][m.start():end].rstrip()
            records.append(dict(key=key,human_source=h['id'],entry=entry,form='diplomatic',decision='DEC-EN-HUMAN-CITED-REFERENCES'))
            entries.append(entry)
    assert {r['key'] for r in records}==required and len(records)==8
    (RECORDS/'EN_EDITORIAL_REFERENCE_RECORDS.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    return '\n'.join([r'\ifSGAdiplomatic',r'\begingroup',
      r'\renewcommand{\bibname}{References cited in Orgogozo\textquotesingle s editorial notes}',
      r'\begin{thebibliography}{99}',
      r'\item[] These eight references were supplied by the Fabrice Orgogozo edition and are cited in its retained editorial notes. Their original released-English entries are reproduced here so that those citations remain available in the diplomatic form. The printed bibliography in the body retains its own recorded entries.',
      *entries,r'\end{thebibliography}',r'\endgroup',r'\fi'])+'\n'


def select_inline_variants(text,corrected):
    edits=[]
    for m in active_matches(r'\\SGA(?:quiet)?var\b',text):
        if any(a<=m.start()<b for a,b,_ in edits):continue
        try:
            d,_,j,_=group(text,m.end());c,_,j,_=group(text,j);_,_,end,_=group(text,j)
        except ValueError:continue
        chosen=select_inline_variants(c if corrected else d,corrected)
        if chosen and chosen[0].isalpha() and re.search(r'\\[A-Za-z@]+$',text[:m.start()]):chosen=' '+chosen
        if end<len(text) and text[end].isalpha():
            if re.search(r'\\[A-Za-z]+$',chosen) or (not chosen and re.search(r'\\[A-Za-z]+$',text[:m.start()])):chosen+=' '
        edits.append((m.start(),end,chosen))
    return replace_spans(text,edits)

def safe_diagram_markers(s):
    """Select a whole Xy-pic diagram before its alignment scanner starts.

    Cell separators and arrow syntax must be literal input to Xy-pic. The
    enclosing selector carries the same recorded branches and appends each
    existing apparatus marker once, without creating an additional variant.
    """
    edits=[]
    for m in re.finditer(r'\\xymatrix\b',s):
        a=s.find('{',m.end())
        if a<0:continue
        try:t,_,end,_=group(s,a)
        except ValueError:continue
        if r'\SGAvar' not in t:continue
        ids=list(dict.fromkeys(re.findall(r'\{(EN-V\d+)\}',t)))
        raw=s[m.start():end]
        printed=select_inline_variants(raw,False)
        corrected=select_inline_variants(raw,True)
        replacement=r'\SGAquietvar{'+printed+'}{'+corrected+'}{diagram}'
        replacement+=''.join(r'\SGAvariantmark{'+v+'}' for v in ids)
        if edits and m.start()<edits[-1][1]:continue
        edits.append((m.start(),end,replacement))
    return replace_spans(s,edits)

def standalone_toc_entries(s):
    """The standard amsbook class already records each starred chapter."""
    edits=[]
    for m in active_matches(r'\\chapter\*',s):
        title,_,end,_=group(s,m.end())
        k=end
        while k<len(s) and s[k].isspace():k+=1
        if not s.startswith(r'\addcontentsline',k):continue
        pos=k+len(r'\addcontentsline');args=[]
        for _ in range(3):arg,_,pos,_=group(s,pos);args.append(arg)
        if args!=['toc','chapter',title]:continue
        edits.append((end,pos,'\n'))
        record('DEC-EN-AMSBOOK-TOC','all','all',title,s[m.start():pos],s[m.start():end],'standard-class table of contents')
    return replace_spans(s,edits)

def bounded_diagram_annotation(s):
    """Keep XVII275 diagram(2) and its condition inside the physical page."""
    from en_extra import page_window
    a,b=page_window(s,'XVII',275);local=s[a:b];edits=[]
    for m in active_matches(r'\\vcenter\b',local):
        content,_,end,_=group(local,m.end())
        tail=local[end:end+180]
        if not tail.startswith('(s') or r'\in S, f_1 \in \Fl \Aa)\tag{2}' not in tail:continue
        old=local[m.start():end]
        # A restricted horizontal math box prevents the linked annotation
        # from starting a full-width paragraph inside the vertical center.
        new=r'\vcenter{\hbox{$'+content+'$}}'
        assert r'\SGAquietvar' in content
        edits.append((m.start(),end,new))
        record('DEC-EN-XVII275-DIAGRAM-LAYOUT','XVII',275,'diagram(2); preserve diagram and adjoining condition',old,new,'typesetting box; mathematical tokens unchanged')
    assert len(edits)==1,('XVII275 layout anchor',len(edits))
    return s[:a]+replace_spans(local,edits)+s[b:]

def build():
    original=RELEASE.read_text()
    s=page_markers(original)
    s=frontend(s)
    s=restore_archived_human_notes(s)
    s=restore_commented_print(s)
    s=sisi_variants(s)
    # Later deterministic passes register source-backed mathematical variants.
    extra=ROOT/'build_scripts/en_extra.py'
    if extra.exists():
        import en_extra
        s=en_extra.apply(s,add_variant,record,source_audit,variants)
    s=printed_notation(s)
    s=printed_statement_labels(s)
    s=encoded_macrons(s)
    s=safe_diagram_markers(s)
    s=bounded_diagram_annotation(s)
    fm=ROOT/'output/shared/frontmatter_EN.tex'
    if fm.exists():
        a=s.index(r'\frontmatter');b=s.index(r'\tableofcontents',a)
        # Source notice can contain its own hidden ToC; use the actual last ToC
        # before mainmatter.
        b=s.rfind(r'\tableofcontents',a,s.index(r'\mainmatter',a))
        title=r'''\frontmatter
\begin{titlepage}
\centering\vspace*{2cm}
{\Huge SGA 4\par}\bigskip
{\LARGE Theory of Topoi and Étale Cohomology of Schemes\par}
\bigskip{\Large Tomes 1--3\par}\bigskip
{\large M. Artin, A. Grothendieck, J.-L. Verdier\par}
\vfill
\ifSGAdiplomatic{\Large Diplomatic English reader\par}\fi
\ifSGAapparatus{\Large Corrected English reader with apparatus\par}\fi
\ifSGAreading{\Large English reading text\par}\fi
\bigskip
AI-transcribed, AI-translated, with AI-produced corrections\par
Build by GPT-6 Astra (OpenAI, ChatGPT Pro mode)\par
12 November 2026
\end{titlepage}
'''
        s=s[:a]+title+fm.read_text()+'\n'+s[b:]
    else:
        s=s.replace('Corrections and typesetting are also AI-produced.',
          'This is an AI-transcribed and AI-translated edition, with AI-produced corrections. '+
          'The LaTeX edition is by Fabrice Orgogozo, snapshot 71766d9. '+
          'This build is by GPT-6 Astra (OpenAI, ChatGPT Pro mode).')
    preface=r'''\chapter*{About the three forms}
All three English forms are generated from this annotated master. The diplomatic
form follows the recorded printed readings. The corrected form marks its
variants with small linked daggers; each link opens the complete source-labelled
entry in the apparatus or human editorial dossier. The reading form carries the same corrected
body and omits the critical apparatus, the possible-misprints appendix, and
Orgogozo's editorial notes. The original page numbers appear in the margin,
preceded by the tome number. The tables of contents are generated from the
transcribed text; untranscribed summary pages, original front matter, and indexes
have not been reconstructed.
'''
    s=s.replace(r'\tableofcontents',preface+'\n'+r'\tableofcontents',1)
    appendix=human_dossier()
    supplement=ROOT/'output/shared/HUMAN_ORIGINAL_SUPPLEMENT_EN.tex'
    if supplement.exists():appendix+='\n\\begingroup\\small\\raggedright\\sloppy\n'+supplement.read_text()+'\n\\endgroup\n'
    original_notes=ROOT/'output/shared/HUMAN_ORIGINAL_NOTES_EN.tex'
    if original_notes.exists():appendix+='\n\\begingroup\\small\\raggedright\\sloppy\n'+original_notes.read_text()+'\n\\endgroup\n'
    appendix+=diplomatic_editorial_references()+apparatus_text()
    for fname in ['disputes_EN.tex','possible_misprints_EN.tex']:
        p=ROOT/'output/shared'/fname
        if p.exists():appendix+='\n\\ifSGAapparatus\n'+p.read_text()+'\n\\fi\n'
    idx=s.rfind(r'\end{document}')
    s=s[:idx]+appendix+s[idx:]
    s=standalone_toc_entries(s)
    s=sanitize(s)
    master=OUT/'SGA4_EN_annotated_master.tex'
    master.write_text(s)
    for mode,name in [(0,'SGA4_EN_diplomatic'),(1,'SGA4_EN_corrected_apparatus'),(2,'SGA4_EN_reading')]:
        (OUT/(name+'.tex')).write_text('%% Generated from SGA4_EN_annotated_master.tex.\n\\def\\SGAform{%d}\n'%mode+s)
    (RECORDS/'EN_VARIANTS.json').write_text(json.dumps(variants,ensure_ascii=False,indent=2)+'\n')
    (RECORDS/'EN_HUMAN_RECORDS.json').write_text(json.dumps(human_records,ensure_ascii=False,indent=2)+'\n')
    (RECORDS/'EN_NOTATION_DECISIONS.json').write_text(json.dumps(notation_decisions,ensure_ascii=False,indent=2)+'\n')
    write_tsv(RECORDS/'EN_BUILD_EVENTS.tsv',changes,['page','place','before','after','source','kind'])
    write_tsv(RECORDS/'EN_PAGE_MARKERS.tsv',page_ledger,['tome','expose','page','fragment','source','status'])
    (RECORDS/'EN_SOURCE_AUDIT.json').write_text(json.dumps(source_audit,ensure_ascii=False,indent=2)+'\n')
    import en_changes
    comparisons=en_changes.build(s,variants,list(changes))
    print(json.dumps({'variants':len(variants),'changes':len(changes),'page_markers':len(page_ledger),'bytes':len(s.encode()),'kinds':dict(collections.Counter(v['kind'] for v in variants))}))
    print(json.dumps({'complete_change_comparisons':comparisons}))

if __name__=='__main__':build()
