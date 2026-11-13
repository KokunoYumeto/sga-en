"""Single-source edition preprocessing and an inlined Miller-style TeX preamble.

Public interface:
    prepared = prepare_body(body, lang, part=None, citation_map=None,
                            source_metadata=None, first_number=1)
    prepared['body'], prepared['apparatus'], prepared['entries']
    preamble(lang, mode=1, master=False)   # includes documentclass, no begin{document}

Every prepared variant remains \\var[stable occurrence]{printed}{corrected}{source}.
The stable optional identifier prevents diagram measurement from duplicating entries.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'work/common'
DEFAULT_CITATIONS={
 '1':{'ar62':'1','gi64':'5','se94':'14','se59':'15','se55':'GAGA'},
 '2':{'de73':'1','gr95':'2','la83':'3','we48':'4'},
 '3':{},'4':{},'5':{},
 '6':{'ca69-2':'1','de73':'2','dl76':'3','ka77':'4','se68':'5','sp76':'6','we74':'7','we52':'8','we74-2':'9'},
 '7':{'de71-1':'1','de71-2':'2','de74':'3','de80':'4'},'8':{},'erratum':{},'opening':{}}
ROMAN={'I':'1','II':'2','III':'3','IV':'4','V':'5','VI':'6','VII':'7','VIII':'8'}
LABEL_OVERRIDES={'I:5-2-4':'2.3.1','I:5-2-5':'2.3.2','I:5-2-6':'2.3.3','I:5-2-7':'2.3.4','III:4-1bis':'4.1bis'}

def group(s,pos,left='{',right='}'):
    while pos<len(s) and s[pos].isspace():pos+=1
    if pos>=len(s) or s[pos]!=left:raise ValueError(('expected group',left,s[pos:pos+90]))
    start=pos+1;depth=1;brace=0;pos+=1
    while pos<len(s):
        if s[pos]=='\\' and pos+1<len(s) and s[pos+1] in '{}[]%$\\':pos+=2;continue
        if s[pos]=='%' and (pos==0 or s[pos-1]!='\\'):
            e=s.find('\n',pos);pos=len(s) if e<0 else e+1;continue
        if left=='[':
            if s[pos]=='{':brace+=1
            elif s[pos]=='}':brace-=1
        if not brace:
            if s[pos]==left:depth+=1
            elif s[pos]==right:
                depth-=1
                if not depth:return s[start:pos],pos+1
        pos+=1
    raise ValueError('unclosed TeX group')

def commands(s,name,nargs=1,optional=False):
    rows=[]
    for m in re.finditer(r'\\'+re.escape(name)+r'(?![A-Za-z])',s):
        # Ignore complete comment lines and inline comments.
        line=s.rfind('\n',0,m.start())+1
        if re.search(r'(?<!\\)%',s[line:m.start()]):continue
        p=m.end()
        while p<len(s) and s[p].isspace():p+=1
        opt=None
        if optional and p<len(s) and s[p]=='[':opt,p=group(s,p,'[',']')
        args=[]
        try:
            for _ in range(nargs):a,p=group(s,p);args.append(a)
        except ValueError:continue
        rows.append(dict(start=m.start(),end=p,args=args,optional=opt))
    return rows

def current_page(s,pos):
    rows=list(re.finditer(r'\\(?:PrintPage|MathPage)\{([^}]+)\}',s[:pos]))
    return rows[-1][1] if rows else ''

def current_part(s,pos,part=None):
    if part is not None:return str(part)
    rows=list(re.finditer(r'\\label\{(I|II|III|IV|V|VI|VII|VIII)\}',s[:pos]))
    return ROMAN[rows[-1][1]] if rows else 'opening'

def escape_text(s,breakable=False):
    out=[]
    table={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','$':r'\$','&':r'\&','#':r'\#','%':r'\%','_':r'\_','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}
    for c in str(s):
        if c in '\r\n\t':out.append(' ');continue
        out.append(table.get(c,c))
        if breakable and c in '{}_^-=/,+()[]\\':out.append(r'\allowbreak{}')
    return ''.join(out)

def convert_citations(body,lang,part=None,citation_map=None):
    logs=[];unresolved=[]
    # Restore inherited keys which Codex replaced by a printed hyperlink literal.
    replacements=[]
    for row in commands(body,'hyperlink',2):
        target,literal=row['args']
        if not target.startswith('cite.'):continue
        key=target[5:]
        new=r'\PrintCite{'+literal+r'}{\cite{'+key+'}}'
        replacements.append((row['start'],row['end'],new))
        logs.append(dict(kind='key_restoration',key=key,literal=literal,part=current_part(body,row['start'],part),page=current_page(body,row['start'])))
    for a,b,new in reversed(replacements):body=body[:a]+new+body[b:]
    protected=[(r['start'],r['end']) for r in commands(body,'PrintCite',2)]
    maps={p:dict(m) for p,m in DEFAULT_CITATIONS.items()}
    if citation_map:
        for p,m in citation_map.items():maps.setdefault(str(p),{}).update(m)
    replacements=[]
    for row in commands(body,'cite',1,optional=True):
        if any(a<=row['start']<b for a,b in protected):continue
        p=current_part(body,row['start'],part);keys=[k.strip() for k in row['args'][0].split(',')]
        values=[]
        for key in keys:
            if key in maps.get(p,{}):value=maps[p][key]
            elif re.fullmatch(r'sga\d+',key):value='SGA~'+key[3:]
            elif key=='ega':value='EGA'
            else:value=None
            values.append(value)
        if any(v is None for v in values):
            unresolved.append(dict(part=p,page=current_page(body,row['start']),keys=keys,postnote=row['optional'],source=body[row['start']:row['end']]))
            continue
        post=row['optional'] or ''
        if all(re.fullmatch(r'\[?\d+\]?',str(v)) for v in values):
            literal='['+', '.join(str(v).strip('[]') for v in values)+((', '+post) if post else '')+']'
        else:
            literal='; '.join(str(v) for v in values)+((' '+post) if post else '')
        old=body[row['start']:row['end']]
        new=r'\PrintCite{'+literal+'}{'+old+'}'
        replacements.append((row['start'],row['end'],new))
        logs.append(dict(kind='local_display',part=p,page=current_page(body,row['start']),keys=keys,postnote=post,literal=literal))
    for a,b,new in reversed(replacements):body=body[:a]+new+body[b:]
    return body,logs,unresolved

def math_context(s,pos):
    # Branches of well-formed variants contain balanced dollar/display pairs.
    p=re.sub(r'(?<!\\)%[^\n]*','',s[:pos]);state=False
    stack=[]
    token=r'(?<!\\)\$|\\\[|\\\]|\\\(|\\\)|\\(?:begin|end)\{(?:align\*?|equation\*?|gather\*?|multline\*?|eqnarray\*?)\}'
    for m in re.finditer(token,p):
        t=m[0]
        if t=='$':state=not state
        elif t in [r'\[',r'\('] or t.startswith(r'\begin'):stack.append(t)
        elif stack:stack.pop()
    return state or bool(stack)

def relocate_markers(body):
    changes=[];replacements=[]
    for row in commands(body,'PrintPage',1):
        end=row['end'];p=end
        while True:
            old=p
            while p<len(body) and body[p].isspace():p+=1
            if p<len(body) and body[p]=='%':
                q=body.find('\n',p);p=len(body) if q<0 else q+1
            if p==old:break
        m=re.match(r'\\(chapter|section|subsection|subsubsection|paragraph|subparagraph)(\*)?',body[p:])
        kind=None;q=p
        if m:
            kind=m[1];q=p+m.end()
            while q<len(body) and body[q].isspace():q+=1
            if q<len(body) and body[q]=='[':_,q=group(body,q,'[',']')
            try:_,q=group(body,q)
            except ValueError:continue
            label=re.match(r'\s*\\label\s*\{',body[q:])
            if label:_,q=group(body,q+label.end()-1)
        elif re.match(r'\\item(?![A-Za-z])',body[p:]):
            kind='item';q=p+len(r'\item')
            while q<len(body) and body[q].isspace():q+=1
            if q<len(body) and body[q]=='[':_,q=group(body,q,'[',']')
        if kind:
            marker=body[row['start']:end]
            # Keep the boundary recorded before the heading in a comment; place its
            # visible marginal marker after the heading/label, avoiding clearpage.
            replacement=body[end:q]+marker
            replacements.append((row['start'],q,replacement))
            changes.append(dict(page=row['args'][0],kind=kind,action='visible marker moved immediately after heading/label or item label'))
    for a,b,new in reversed(replacements):body=body[:a]+new+body[b:]
    return body,changes

def restore_heading_numbers(body,lang):
    """Restore visible source-local numbers as well as the corresponding refs.

    These are inherited Miller heading counters, not printed-text variants.
    French Arcata already scopes these four local numbers in its component.
    """
    targets={'III:4-1bis':('subsection','4.1bis')}
    if lang=='en':
        targets.update({k:('subsubsection',v) for k,v in LABEL_OVERRIDES.items() if k.startswith('I:5-2-')})
    replacements=[];logs=[]
    for label,(counter,number) in targets.items():
        hit=re.search(r'\\label\{'+re.escape(label)+r'\}',body)
        if not hit:continue
        start=None;end=None;kind=None
        # A theorem label follows its begin token and optional theorem note.
        begins=list(re.finditer(r'\\begin\{([^}]+)\}',body[:hit.start()]))
        if begins:
            begin=begins[-1];p=begin.end()
            while p<len(body) and body[p].isspace():p+=1
            if p<len(body) and body[p]=='[':_,p=group(body,p,'[',']')
            if not body[p:hit.start()].strip():
                env=begin[1];depth=0
                for close in re.finditer(r'\\(begin|end)\{'+re.escape(env)+r'\}',body[begin.start():]):
                    depth+=1 if close[1]=='begin' else -1
                    if depth==0:
                        start=begin.start();end=begin.start()+close.end();kind=env;break
        if start is None:
            for heading in commands(body,'subsubsection',1):
                if heading['end']<=hit.start() and not body[heading['end']:hit.start()].strip():
                    start=heading['start'];end=hit.end();kind='subsubsection';break
        if start is None:
            raise ValueError('Cannot locate visible heading for '+label)
        prefix='\\begingroup\n\\renewcommand*{\\the'+counter+'}{'+number+'}\n'
        replacements.append((start,end,prefix+body[start:end]+'\n\\endgroup'))
        logs.append(dict(label=label,number=number,counter=counter,kind=kind,page=current_page(body,start)))
    for a,b,new in sorted(replacements,reverse=True):body=body[:a]+new+body[b:]
    return body,logs

def prepare_bookmark_strings(body):
    replacements=[];logs=[]
    for row in commands(body,'addcontentsline',3):
        title=row['args'][2]
        if r'$4\frac12$' not in title or r'\texorpdfstring' in title:continue
        args=row['args'][:]
        args[2]=title.replace(r'$4\frac12$',r'\texorpdfstring{$4\frac12$}{4½}')
        replacements.append((row['start'],row['end'],r'\addcontentsline'+''.join('{'+a+'}' for a in args)))
        logs.append(dict(kind='bookmark_math_alternative',page=current_page(body,row['start']),printed=r'$4\frac12$',pdf_string='4½'))
    for a,b,new in reversed(replacements):body=body[:a]+new+body[b:]
    return body,logs

def load_metadata():
    out={}
    for folder in ['arcata','rapport_cycle','sommes','finitude_verdier']:
        for name in ['decisions.jsonl','own_findings.jsonl','variants.jsonl']:
            p=ROOT/'work'/folder/name
            if not p.exists():continue
            for line in p.read_text().splitlines():
                if not line.strip():continue
                row=json.loads(line);key=row.get('id') or row.get('source_id') or row.get('source')
                if key:out.setdefault(key,{}).update(row)
    return out

def literal_reading(fragment):
    if not fragment.strip():return r'\emph{\textnormal{[omission]}}'
    return r'{\footnotesize\ttfamily\raggedright '+escape_text(fragment,True)+r'\par}'

def incomplete_math_arguments(fragment):
    # A variant can legitimately end after a numerator and take its denominator
    # from the surrounding text. It is not a standalone apparatus formula.
    arities={name:2 for name in ['frac','dfrac','tfrac','binom','dbinom','tbinom','overset','underset','stackrel']}
    arities.update({name:1 for name in ['sqrt','operatorname','mathrm','mathsf','mathcal','mathbb','mathscr','mathfrak','underline','overline']})
    for match in re.finditer(r'\\('+'|'.join(arities)+r')(?![A-Za-z])',fragment):
        p=match.end()
        while p<len(fragment) and fragment[p].isspace():p+=1
        if match[1]=='sqrt' and p<len(fragment) and fragment[p]=='[':
            try:_,p=group(fragment,p,'[',']')
            except ValueError:return True
        for _ in range(arities[match[1]]):
            while p<len(fragment) and fragment[p].isspace():p+=1
            if p>=len(fragment) or fragment[p]=='}':return True
            if fragment[p]=='{':
                try:_,p=group(fragment,p)
                except ValueError:return True
            elif fragment[p]=='\\':
                token=re.match(r'\\(?:[A-Za-z]+|.)',fragment[p:])
                if not token:return True
                p+=token.end()
            else:p+=1
    return False

def formatted_reading(fragment,is_math=False):
    # A partial diagram command or a dangling delimiter cannot be interpreted as
    # standalone mathematics. Those readings remain exact, breakable TeX text.
    unsafe=(r'\\(?:ar|item|begin|end|label|tag|setcounter|addtocounter|def|if\w*|else|fi)\b|(?<!\\)&')
    if re.search(unsafe,fragment):return literal_reading(fragment),'literal'
    if len(re.findall(r'\\left(?![A-Za-z])',fragment))!=len(re.findall(r'\\right(?![A-Za-z])',fragment)):return literal_reading(fragment),'literal'
    if len(re.findall(r'(?<!\\)\$',fragment))%2:return literal_reading(fragment),'literal'
    if incomplete_math_arguments(fragment):return literal_reading(fragment),'literal'
    if not fragment.strip():return literal_reading(fragment),'literal'
    if is_math and '$' not in fragment and not re.search(r'[^\x00-\x7f]',fragment):
        return r'\('+fragment+r'\)','math'
    if is_math and '$' not in fragment:return literal_reading(fragment),'literal'
    # Bare math-only commands in prose fragments usually belong to an enclosing
    # math expression which the lightweight scanner could not safely infer.
    if not is_math and '$' not in fragment and re.search(r'\\(?:frac|hom|e[A-Z]|s[A-Z]|c[A-Z]|sum|h\b|mathsf|mathrm|varinjlim|delta|partial|beta|alpha|rho|pi|Pi|Psi|varepsilon|circ|left|right)',fragment):
        return literal_reading(fragment),'literal'
    return fragment,'text'

def apparatus(entries,lang='fr',conditional=True):
    fr=lang=='fr';title='Apparat des corrections' if fr else 'Apparatus of corrections'
    explanation=('Chaque numéro correspond à un lieu précis du texte corrigé. Les fragments qui ne peuvent pas être composés isolément (délimiteur ouvert, commande mathématique incomplète, fragment de diagramme) sont reproduits exactement en notation TeX. Les réparations de transcription communes aux trois formes ne figurent pas ici. Les justifications complètes sont consignées dans \\texttt{MISPRINTS\\_45.tsv}.' if fr else 'Each number identifies one particular occurrence in the corrected text. Fragments that cannot stand alone (an open delimiter, an incomplete mathematical command, or part of a diagram) are reproduced exactly in TeX notation. Transcription repairs shared by all three forms do not appear here. Full reasons are recorded in \\texttt{MISPRINTS\\_45.tsv}.')
    lines=[r'\ifnum\EditionMode=1\relax' if conditional else '',r'\clearpage',r'\chapter*{'+title+'}',r'\markboth{'+title+'}{'+title+'}',r'\addcontentsline{toc}{chapter}{'+title+'}',explanation,r'\begingroup\small',r'\begin{description}']
    for e in entries:
        p=e['page'];source=e['source'];idx=e['occurrence'];num=e['number']
        lines.append(r'\item[\hypertarget{apparatus:'+idx+'}{'+str(num)+r'}] '+(('Page' if fr else 'Page')+' '+(r'\hyperlink{printpage:'+lang+':'+p+'}{'+escape_text(p)+'}' if p else '?'))+r'\quad\texttt{'+escape_text(source)+'}')
        for key,label in [('printed','Imprimé' if fr else 'Printed'),('corrected','Corrigé' if fr else 'Corrected')]:
            value,form=formatted_reading(e[key],e['math_context']);e[key+'_apparatus_form']=form
            lines.append(r'\par\noindent\textbf{'+label+':} '+value)
        if re.search(r'conjectur',e.get('reason',''),re.I):
            lines.append(r'\par\noindent\emph{'+('Restitution conjecturale' if fr else 'Conjectural restoration')+'}.')
        lines.append(r'\smallskip')
    lines.extend([r'\end{description}',r'\endgroup',r'\fi' if conditional else ''])
    return '\n'.join(lines)+'\n'

def prepare_body(body,lang='fr',part=None,citation_map=None,source_metadata=None,first_number=1):
    if lang not in ['fr','en']:raise ValueError('language must be fr or en')
    metadata=load_metadata() if source_metadata is None else source_metadata
    body,citations,unresolved=convert_citations(body,lang,part,citation_map)
    entries=[];replacements=[];diagnostics=[]
    rows=commands(body,'var',3,optional=True)
    for a,b in zip(rows,rows[1:]):
        if b['start']<a['end']:raise ValueError('nested variants are not supported')
    for row in rows:
        printed,corrected,source=row['args']
        if printed==corrected:
            diagnostics.append(dict(kind='identical_variant_removed',source=source,page=current_page(body,row['start'])))
            replacements.append((row['start'],row['end'],corrected));continue
        n=first_number+len(entries);occurrence=lang.upper()+'-'+str(n).zfill(4)
        e=dict(occurrence=occurrence,number=n,source=source,printed=printed,corrected=corrected,page=current_page(body,row['start']),part=current_part(body,row['start'],part),math_context=math_context(body,row['start']),reason=metadata.get(source,{}).get('reason',''),source_line=body[:row['start']].count('\n')+1)
        entries.append(e)
        new=r'\var['+occurrence+']{'+printed+'}{'+corrected+'}{'+source+'}'
        replacements.append((row['start'],row['end'],new))
    for a,b,new in reversed(replacements):body=body[:a]+new+body[b:]
    body,headings=restore_heading_numbers(body,lang)
    body,relocations=relocate_markers(body)
    body,bookmarks=prepare_bookmark_strings(body)
    diagnostics.extend(bookmarks)
    return dict(body=body,entries=entries,apparatus=apparatus(entries,lang),citations=citations,unresolved_citations=unresolved,marker_relocations=relocations,heading_overrides=headings,diagnostics=diagnostics,next_number=first_number+len(entries))

MACROS=r'''
% EditionMode: 0 = diplomatic; 1 = corrected with apparatus; 2 = reading.
\providecommand\EditionMode{@MODE@}
\providecommand\EditionLanguage{@LANG@}
\usepackage{xcolor}
\usepackage{marginnote}
\setlength{\marginparwidth}{0.55in}
\setlength{\marginparsep}{0.12in}
\definecolor{EditionAppColor}{rgb}{0.18,0.25,0.42}
\makeatletter
% The apparatus is indexed by source occurrence before TeX runs: no counters
% can be incremented twice by math/diagram measuring passes.
\DeclareRobustCommand{\EditionVariantMark}[2]{%
  \ifx\relax#1\relax\else
    \ifmmode
      \hbox{\raisebox{0.7ex}{\normalfont\scriptsize\color{EditionAppColor}%
        \hyperlink{apparatus:#1}{\EditionShortOccurrence{#1}}}}%
    \else
      \textsuperscript{\normalfont\scriptsize\color{EditionAppColor}%
        \hyperlink{apparatus:#1}{\EditionShortOccurrence{#1}}}%
    \fi
  \fi}
\def\EditionShortOccurrence#1{\expandafter\EditionShortOccurrenceAux#1\@nil}
\def\EditionShortOccurrenceAux#1-#2\@nil{\number#2\relax}
% IMPORTANT: Neither branch is put in a group, box, or math wrapper. A branch
% may be only \left. or \left|, matched by a later \right outside this macro.
\DeclareRobustCommand{\var}[4][]{%
  \ifnum\EditionMode=0\relax
    \expandafter\@firstoftwo
  \else
    \expandafter\@secondoftwo
  \fi
  {#2}{\ifnum\EditionMode=1\relax\EditionVariantMark{#1}{#4}\fi#3}}
\providecommand\CurrentPrintPage{}
\DeclareRobustCommand{\PrintPage}[1]{%
  \gdef\CurrentPrintPage{#1}%
  \hypertarget{printpage:\EditionLanguage:#1}{}%
  \marginnote{\normalfont\sffamily\scriptsize\color{black!65}%
    \ifnum\EditionMode=2\relax#1\else[p.~#1]\fi}}
\DeclareRobustCommand{\MathPage}[1]{\PrintPage{#1}}
% Metadata-only cite execution. No global bibliography is introduced.
\newcommand{\EditionRememberCite}[2][]{%
  \if@filesw\immediate\write\@auxout{\string\citation{#2}}\fi}
\DeclareRobustCommand{\PrintCite}[2]{%
  \begingroup\let\cite\EditionRememberCite
    \setbox\z@=\hbox{#2}%
  \endgroup#1}
% Preserve existing label names while restoring their original local numbers.
\let\EditionOriginalLabel\label
\renewcommand{\label}[1]{%
  \@ifundefined{EditionLabelNumber@#1}{\EditionOriginalLabel{#1}}{%
    \begingroup
      \protected@edef\@currentlabel{\csname EditionLabelNumber@#1\endcsname}%
      \EditionOriginalLabel{#1}%
    \endgroup}}
@LABELS@
\expandafter\def\csname EditionLabelNumber@I:1-6-6\endcsname{%
  \ifnum\EditionMode=0\relax6.5\else6.6\fi}
% PDF bookmarks contain the selected reading and no editorial markers.
% prepare_body assigns an explicit optional occurrence identifier to every
% variant. Parsing that known form directly remains fully expandable inside
% hyperref's PDF-string conversion (unlike an \@ifnextchar look-ahead).
\def\EditionPDFVar[#1]#2#3#4{\ifnum\EditionMode=0\relax\expandafter\@firstoftwo\else\expandafter\@secondoftwo\fi{#2}{#3}}
\pdfstringdefDisableCommands{%
  \let\var\EditionPDFVar
  \def\PrintPage#1{}\def\MathPage#1{}%
  \def\PrintCite#1#2{#1}%
  \def\EditionVariantMark#1#2{}}
\makeatother
\hypersetup{hidelinks,bookmarksopen=true,bookmarksnumbered=true}
'''

UNICODE={
 0x202f:r'\,',0x00a0:'~',0x2032:r'\ensuremath{\prime}',0x2033:r'\ensuremath{\prime\prime}',
 0x2212:r'\ensuremath{-}',0x00d7:r'\ensuremath{\times}',0x00b1:r'\ensuremath{\pm}',
 0x2192:r'\ensuremath{\to}',0x2190:r'\ensuremath{\leftarrow}',0x2194:r'\ensuremath{\leftrightarrow}',0x21d2:r'\ensuremath{\Rightarrow}',0x21d4:r'\ensuremath{\Leftrightarrow}',
 0x21dd:r'\ensuremath{\leadsto}',0x2208:r'\ensuremath{\in}',0x2209:r'\ensuremath{\notin}',0x2205:r'\ensuremath{\varnothing}',0x221e:r'\ensuremath{\infty}',
 0x2260:r'\ensuremath{\ne}',0x2264:r'\ensuremath{\leqslant}',0x2265:r'\ensuremath{\geqslant}',0x2243:r'\ensuremath{\simeq}',0x2245:r'\ensuremath{\cong}',0x223c:r'\ensuremath{\sim}',
 0x2282:r'\ensuremath{\subset}',0x2286:r'\ensuremath{\subseteq}',0x2283:r'\ensuremath{\supset}',0x22a5:r'\ensuremath{\perp}',0x2218:r'\ensuremath{\circ}',0x2229:r'\ensuremath{\cap}',0x222a:r'\ensuremath{\cup}',
 0x2113:r'\ensuremath{\ell}',0x2124:r'\ensuremath{\mathbb Z}',0x211a:r'\ensuremath{\mathbb Q}',0x2102:r'\ensuremath{\mathbb C}',0x211d:r'\ensuremath{\mathbb R}',
 0x2297:r'\ensuremath{\otimes}',0x2295:r'\ensuremath{\oplus}',0x2200:r'\ensuremath{\forall}',0x2203:r'\ensuremath{\exists}',0x2202:r'\ensuremath{\partial}',
 0x1d62:r'\ensuremath{{}^i}',0x2070:r'\ensuremath{{}^0}',0x00b9:r'\ensuremath{{}^1}',0x00b2:r'\ensuremath{{}^2}',0x00b3:r'\ensuremath{{}^3}',
 0x207a:r'\ensuremath{{}^+}',0x207b:r'\ensuremath{{}^-}',0x2080:r'\ensuremath{{}_0}',0x2081:r'\ensuremath{{}_1}',0x2082:r'\ensuremath{{}_2}',
}
for c,n in {'α':'alpha','β':'beta','γ':'gamma','δ':'delta','ε':'varepsilon','ζ':'zeta','η':'eta','θ':'theta','ι':'iota','κ':'kappa','λ':'lambda','μ':'mu','ν':'nu','ξ':'xi','π':'pi','ρ':'rho','σ':'sigma','τ':'tau','υ':'upsilon','φ':'varphi','χ':'chi','ψ':'psi','ω':'omega','Γ':'Gamma','Δ':'Delta','Θ':'Theta','Λ':'Lambda','Ξ':'Xi','Π':'Pi','Σ':'Sigma','Υ':'Upsilon','Φ':'Phi','Ψ':'Psi','Ω':'Omega'}.items():UNICODE[ord(c)]='\\ensuremath{\\'+n+'}'

def preamble(lang='fr',mode=1,master=False,label_overrides=None):
    if lang not in ['fr','en'] or mode not in [0,1,2]:raise ValueError('bad language or mode')
    style=(ROOT/'source/fr/codex_dip/sga-style.sty').read_text()
    # Some runtime installations include calligra.sty but omit its font files.
    # Retain the source font when its metric is available; otherwise the initial
    # mathscr H/E/T still distinguishes sheaf Hom/Ext/Tor from ordinary operators.
    style=style.replace(r'\usepackage{calligra}',r'''\IfFileExists{callig15.tfm}{\usepackage{calligra}}{%
  \providecommand\calligra{\itshape}}''')
    # Printed counters and explicit equation tags legitimately restart in each
    # exposé. Automatic PDF destinations must use hyperref's global link counter
    # instead of those reused printed numbers. Named printpage/apparatus targets
    # are explicit hypertargets and are not affected by this option.
    style=style.replace(r'\usepackage[backref=page,pdfpagelabels]{hyperref}',r'\usepackage[backref=page,pdfpagelabels,hypertexnames=false]{hyperref}')
    # Retain normal package use on a complete TeX Live installation; the
    # documented fallback composes the same double-bracket sign from brackets.
    style=style.replace('  mathrsfs,','  mathrsfs')
    style=re.sub(r'^\s*stmaryrd\s*%[^\n]*\n','',style,flags=re.M)
    guard=r'''
\IfFileExists{stmaryrd.sty}{\usepackage{stmaryrd}}{%
  \providecommand\llbracket{[\! [}%
  \providecommand\rrbracket{]\! ]}}
'''
    pos=style.find('% operators')
    style=style[:pos]+guard+style[pos:]
    if lang=='en':
        for a,b in [('Corollaire','Corollary'),('Définition','Definition'),('Théorème','Theorem'),('Lemme','Lemma'),('Proposition-définition','Proposition-definition')]:style=style.replace('{'+a+'}','{'+b+'}')
    labels=dict(LABEL_OVERRIDES)
    if label_overrides:labels.update(label_overrides)
    labeltex='\n'.join(r'\expandafter\def\csname EditionLabelNumber@'+k+r'\endcsname{'+v+'}' for k,v in labels.items())
    macros=MACROS.replace('@MODE@',str(mode)).replace('@LANG@',lang).replace('@LABELS@',labeltex)
    unicode='\n'.join(r'\DeclareUnicodeCharacter{'+format(k,'04X')+'}{'+v+'}' for k,v in sorted(UNICODE.items()))
    language=(r'\renewcommand{\chaptername}{Exposé}\renewcommand{\appendixname}{Annexe}\renewcommand{\bibname}{Bibliographie}\renewcommand{\proofname}{Démonstration}\renewcommand{\contentsname}{Table des matières}' if lang=='fr' else r'\renewcommand{\chaptername}{Exposé}\renewcommand{\bibname}{Bibliography}\renewcommand{\proofname}{Proof}\renewcommand{\contentsname}{Contents}')
    return r'\documentclass[oneside]{book}'+'\n% Inlined baseline: Daniel Miller style, as preserved in the diplomatic tree.\n'+style+'\n'+unicode+'\n'+macros+'\n'+language+'\n'

if __name__=='__main__':
    COMMON.mkdir(parents=True,exist_ok=True)
    for lang in ['fr','en']:(COMMON/f'edition_preamble_{lang}.tex').write_text(preamble(lang))
    (COMMON/'edition_tex_interface.json').write_text(json.dumps(dict(module='scripts/edition_tex.py',preamble='preamble(lang, mode=1, master=False) -> str; no begin/end document',prepare='prepare_body(body, lang, part=None, citation_map=None, source_metadata=None, first_number=1) -> dict',outputs=['body','apparatus','entries','citations','unresolved_citations','marker_relocations','heading_overrides','diagnostics','next_number'],variant='\\var[LANG-0001]{printed}{corrected}{source}',modes={'0':'diplomatic','1':'corrected with apparatus','2':'reading'},no_global_bibliography=True),ensure_ascii=False,indent=2))
    print('Wrote both inlined preambles and the interface description.')
