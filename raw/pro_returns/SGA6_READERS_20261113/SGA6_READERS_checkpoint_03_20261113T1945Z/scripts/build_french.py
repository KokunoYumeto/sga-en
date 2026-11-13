#!/usr/bin/env python3
"""Build source-locked French candidates from reviewed patches and layered inputs.

Each annotation has both exact alternatives and an explicit provenance record.
The release gate is separate: a successful build does not imply scan collation.
"""
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path
from intake import split_pages, write_tsv

ROOT=Path(__file__).resolve().parents[1]
PAGE=re.compile(r'(?m)^%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+([^%\n]+?)\s*%+[^\n]*$')

def get_jsonl(path):
    if not path.exists(): return []
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

def all_patches():
    result=[]
    primary=['front','early','late','middle']
    extra=sorted(p.name for p in (ROOT/'review').iterdir() if p.is_dir() and p.name not in primary)
    for d in primary+extra:
        result.extend(get_jsonl(ROOT/'review'/d/'patches.jsonl'))
    return result

def apply_patches(text, layer, patches):
    log=[]
    for p in patches:
        if p.get('layer') not in [layer,'both']: continue
        pages,offsets=split_pages(text)
        key=p['page']
        if isinstance(key,str) and key.isdigit(): key=int(key)
        if key not in pages:
            log.append({'source':p['source_id'],'page':key,'layer':layer,'status':'blocked','reason':'page has no source marker','old':p['old'],'new':p['new']})
            continue
        start=offsets[key]
        chunk=pages[key]
        expected=p.get('expected_count',1)
        n=chunk.count(p['old'])
        if n==expected:
            new=chunk.replace(p['old'],p['new'],expected)
            text=text[:start]+new+text[start+len(chunk):]
            log.append({'source':p['source_id'],'page':key,'layer':layer,'status':'applied','occurrences':expected,'old':p['old'],'new':p['new'],'reason':p['reason']})
        elif n==0 and p['new'] in chunk:
            log.append({'source':p['source_id'],'page':key,'layer':layer,'status':'already present','old':p['old'],'new':p['new'],'reason':p['reason']})
        else:
            log.append({'source':p['source_id'],'page':key,'layer':layer,'status':'blocked','reason':f'anchor occurs {n} times; expected {expected}','old':p['old'],'new':p['new']})
    return text,log

def brace_end(s,i,left='{',right='}'):
    assert s[i]==left
    n=1;j=i+1
    while j<len(s):
        if s[j]=='\\': j+=2;continue
        if s[j]=='%':
            k=s.find('\n',j);j=len(s) if k<0 else k+1;continue
        if s[j]==left:n+=1
        elif s[j]==right:
            n-=1
            if n==0:return j+1
        j+=1
    return len(s)

MATH_ENVS={'align','align*','alignat','alignat*','equation','equation*','gather','gather*','multline','multline*','displaymath','tikzcd','tikzpicture','array','matrix','pmatrix','bmatrix','cases'}
def atoms(s):
    """TeX-aware atoms keep math expressions and macro arguments intact."""
    out=[];i=0
    while i<len(s):
        j=i+1
        if s[i]=='%':
            k=s.find('\n',i);j=len(s) if k<0 else k+1
        elif s[i]=='{':j=brace_end(s,i)
        elif s[i]=='$':
            delimiter='$$' if s.startswith('$$',i) else '$'
            j=i+len(delimiter)
            while j<len(s):
                if s[j]=='\\':j+=2;continue
                if s.startswith(delimiter,j):j+=len(delimiter);break
                j+=1
        elif s.startswith('\\[',i) or s.startswith('\\(',i):
            close='\\]' if s[i+1]=='[' else '\\)'
            k=s.find(close,i+2);j=len(s) if k<0 else k+2
        elif s[i]=='\\':
            m=re.match(r'\\(?:[A-Za-z@]+\*?|.)',s[i:])
            j=i+len(m[0]) if m else i+1
            accent_commands={"\\'",'\\`','\\^','\\"','\\~','\\=','\\.','\\u','\\v','\\H','\\c','\\k','\\b','\\d','\\r','\\t'}
            if m and m[0] in accent_commands and j<len(s) and s[j]!='{':
                # A TeX accent consumes its next token even without braces.
                # Annotation must never be inserted between that accent and
                # its argument: doing so changes TeX's argument scanner.
                if s[j]=='\\':
                    a=re.match(r'\\(?:[A-Za-z@]+|.)',s[j:])
                    j+=len(a[0]) if a else 1
                else:j+=1
            if s.startswith('\\begin{',i):
                k=brace_end(s,i+6);env=s[i+7:k-1]
                if env in MATH_ENVS:
                    end='\\end{'+env+'}'
                    k2=s.find(end,k)
                    if k2>=0:j=k2+len(end)
                else:j=k
            # Immediate optional/mandatory arguments are part of the macro atom.
            while j<len(s) and s[j] in '[{':
                j=brace_end(s,j,'[',']') if s[j]=='[' else brace_end(s,j)
        elif s[i].isspace():
            while j<len(s) and s[j].isspace():j+=1
        elif s[i].isalnum():
            while j<len(s) and (s[j].isalnum() or s[j] in "’'-"):
                j+=1
        out.append(s[i:j]);i=j
    assert ''.join(out)==s
    return out

def clean_private_metadata(s):
    result=[]
    for line in s.splitlines(True):
        if line.lstrip().startswith('%') and (re.search(r'(?:[A-Z]:\\|/(?:home|root|Users|workspace)/|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,})',line)):
            result.append('% Source metadata omitted: private path or email.\n')
        else:result.append(line)
    return ''.join(result)

def tex_escape(s):
    return ''.join({'\\':r'\textbackslash{}','{':r'\{','}':r'\}','_':r'\_','#':r'\#','%':r'\%','&':r'\&','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}.get(c,c) for c in str(s))

def fit_heading_boxes(body):
    """Transport each existing heading underline box into a max-width box.

    The underline box contents are retained byte for byte. Only a box exceeding
    the available line width is scaled, preventing inherited clipped headings.
    """
    def fit_inner(text):
        out=[];i=0
        while True:
            j=text.find('\\underline{',i)
            if j<0:out.append(text[i:]);break
            end=brace_end(text,j+len('\\underline'))
            unit=text[j:end]
            if unit.startswith('\\underline{\\underline{') or len(unit)>100:
                out.extend([text[i:j],'\\SGAheadingline{',unit,'}'])
            else:out.extend([text[i:j],unit])
            i=end
        return ''.join(out)
    out=[];i=0
    pattern=re.compile(r'\\(?:section|subsection|subsubsection)\*?\{')
    while True:
        m=pattern.search(body,i)
        if not m:out.append(body[i:]);break
        start=m.end()-1;end=brace_end(body,start)
        out.extend([body[i:start+1],fit_inner(body[start+1:end-1]),'}'])
        i=end
    return ''.join(out)

def provenance(page,old,new,records):
    hits=[]
    for r in records:
        if str(r.get('page'))!=str(page):continue
        d=r.get('data',{})
        a=d.get('old','');b=d.get('new','')
        if a and b and ((a in old and b in new) or (b in old and a in new)):
            hits.append(r['id'])
        if r['type']=='misprint':
            a=d.get('print','');b=d.get('correct','')
            if a and b and a in old and b in new:hits.append(r['id'])
    return list(dict.fromkeys(hits))

def macro_safe(fragment):
    """Give TikZ-CD its explicit separator when a diagram is a macro argument.

    The source '&' token is mapped to '\\&', and TikZ-CD is told that exact
    replacement. Cell contents, row separators, arrows, and labels are retained.
    This is a reversible token transport for TeX's argument catcodes.
    """
    pattern=re.compile(r'\\begin\{tikzcd\}(?:\[[^\]]*\])?.*?\\end\{tikzcd\}',re.S)
    def convert(m):
        raw=m[0]
        if 'ampersand replacement' in raw:return raw
        head='\\begin{tikzcd}'
        rest=raw[len(head):]
        if rest.startswith('['):
            end=brace_end(rest,0,'[',']')
            options=rest[1:end-1]
            tail=rest[end:]
            prefix=head+'[ampersand replacement=\\&,'+options+']'
        else:
            tail=rest;prefix=head+'[ampersand replacement=\\&]'
        rewritten=re.sub(r'(?<!\\)&',lambda _:r'\&',tail)
        # The exact count of transported column separator tokens is invariant.
        assert len(re.findall(r'(?<!\\)&',tail))==len(re.findall(r'\\&',rewritten))-len(re.findall(r'\\&',tail))
        return prefix+rewritten
    return pattern.sub(convert,fragment)

def annotate(dipl,corr,registry,patches):
    # An exact atom diff is computed page by page to prevent cross-page matches.
    da,do=split_pages(dipl);ca,co=split_pages(corr)
    assert list(da)==list(ca),'The two layers have differing marker sequences.'
    pieces=[];variants=[];left_roundtrip=[];right_roundtrip=[]
    for page in da:
        a=atoms(da[page]);b=atoms(ca[page])
        for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
            before=''.join(a[i:j]);after=''.join(b[k:l])
            left_roundtrip.append(before);right_roundtrip.append(after)
            if tag=='equal':pieces.append(before);continue
            id=f'FRV{len(variants)+1:04d}'
            src=provenance(page,before,after,registry)
            for p in patches:
                if str(p['page'])==str(page) and p['old'] in before and p['new'] in after:
                    src.append(p['source_id'])
            if not src:src=[f'LAYER-DIFFERENCE:{page}:{id}']
            variants.append({'id':id,'page':page,'printed':before,'corrected':after,'source':list(dict.fromkeys(src)),
              'status':'requires individual scan-decision linkage','sha256_printed':hashlib.sha256(before.encode()).hexdigest(),'sha256_corrected':hashlib.sha256(after.encode()).hexdigest()})
            pieces.append('\\SGAvar{'+macro_safe(before)+'}{'+macro_safe(after)+'}{'+id+'}')
    # The reversible model itself, independent from TeX expansion, is checked.
    assert sum(v['printed']!=v['corrected'] for v in variants)==len(variants)
    assert ''.join(left_roundtrip)==dipl
    assert ''.join(right_roundtrip)==corr
    return ''.join(pieces),variants

MACROS=r'''
\usepackage{marginnote}
\usepackage{fvextra}
\usepackage{adjustbox}
\usepackage{xurl}
\providecommand{\SGAform}{1}
\newcommand{\SGAheadingline}[1]{\adjustbox{max width=\linewidth}{#1}}
\newcommand{\SGAmark}[1]{\ifmmode\text{\textsuperscript{[#1]}}\else\textsuperscript{[#1]}\fi}
\long\def\SGAvar#1#2#3{\ifnum\SGAform=0 #1\else #2\fi\ifnum\SGAform=1\SGAmark{#3}\fi}
\newcommand{\SGAfolio}[1]{\ifmmode\hbox{\marginnote{\scriptsize #1}}\else\marginnote{\scriptsize #1}\fi}
\newcommand{\SGAAuthorLabel}[1]{\ifcsname SGAAuthorLabel@#1\endcsname\csname SGAAuthorLabel@#1\endcsname\else(#1)\fi}
\makeatletter
\newcommand{\SGAAuthorFootnote}[2]{\begingroup\renewcommand{\thefootnote}{#1}\def\@makefnmark{\hbox{\normalfont\SGAAuthorLabel{#1}}}\def\@makefntext##1{\parindent1em\noindent\hb@xt@1.8em{\@makefnmark\hss}##1}\footnote{#2}\endgroup}
\newcommand{\SGAAuthorFootMark}[1]{\begingroup\renewcommand{\thefootnote}{#1}\def\@makefnmark{\hbox{\normalfont\SGAAuthorLabel{#1}}}\footnotemark[\value{footnote}]\endgroup}
\newcommand{\SGAAuthorFootText}[2]{\begingroup\renewcommand{\thefootnote}{#1}\def\@makefnmark{\hbox{\normalfont\SGAAuthorLabel{#1}}}\def\@makefntext##1{\parindent1em\noindent\hb@xt@1.8em{\@makefnmark\hss}##1}\footnotetext[\value{footnote}]{#2}\endgroup}
\makeatother
'''
MACROS+=''.join(r'\expandafter\def\csname SGAAuthorLabel@'+str(n)+r'\endcsname{(\textsuperscript{'+str(n)+'})}\n' for n in range(1,10))
MACROS+=r'\expandafter\def\csname SGAAuthorLabel@raisedstar\endcsname{(\textsuperscript{*})}'+'\n'
MACROS+=r'\expandafter\def\csname SGAAuthorLabel@unmarked\endcsname{}'+'\n'

PREFACE=r'''
\section*{État de ce fichier de travail}
Ce fichier est un candidat de travail incomplet. La seconde collation de toutes
les pages et l'adjudication de toutes les variantes sont en cours. La présence
d'une variante dans ce fichier atteste une différence entre les sources fournies;
elle ne constitue pas, à elle seule, une validation de cette différence par le scan.
Ce fichier ne doit pas être présenté comme l'édition achevée demandée.

Ce travail est AI-transcribed; les corrections de Codex (août 2026), le contrôle
par Claude Opus 5.5 à effort max (10--13 novembre 2026), ainsi que les corrections
de ce travail sont AI-produced corrections. Ce travail est produit par GPT-6 Astra
(OpenAI, ChatGPT Pro mode). L'anglais correspondant est AI-translated.

Les droits sur l'œuvre originale appartiennent à son auteur, à ses représentants
ou à ses ayants droit. Dans la mesure où nous détenons des droits sur la
transcription, la traduction, les corrections et la composition produites par
l'IA, nous les consacrons au domaine public sous CC0 1.0. Cette édition est publiée
à des fins éducatives et non lucratives, et nous ne revendiquons aucun droit que
nous ne détenons pas. Si vous détenez des droits sur cette œuvre et vous opposez
à sa publication ici, veuillez ouvrir une issue GitHub et nous la retirerons.

\ifnum\SGAform=2
La forme de lecture garde l'Introduction et les notes des auteurs et éditeurs;
seul notre apparat est omis. Les nombres en marge renvoient aux pages imprimées.
\fi
\clearpage
'''

def apparatus(variants):
    out=['\n\\ifnum\\SGAform=1\n\\clearpage\n\\section*{Apparat de travail : lectures exactes}\n',
      'Chaque entrée conserve les deux lectures en code LaTeX exact et leur provenance. Les entrées sans adjudication de scan restent à examiner.\n']
    for v in variants:
        out.append('\\subsection*{'+v['id']+' --- page '+tex_escape(v['page'])+'}\n')
        out.append('Source : '+''.join('\\nolinkurl{'+s+'}\\par\n' for s in v['source']))
        for label,key in [('Lecture diplomatique','printed'),('Lecture corrigée','corrected')]:
            out.append('\\textbf{'+label+'}\\par\n\\begin{Verbatim}[fontsize=\\footnotesize,breaklines=true,breakanywhere=true]\n')
            out.append(v[key]+'\n\\end{Verbatim}\n')
    out.append('\\fi\n')
    return ''.join(out)

def make():
    out=ROOT/'readers/fr';out.mkdir(parents=True,exist_ok=True)
    registry=json.loads((ROOT/'build/registry.json').read_text())
    patches=all_patches();logs=[];layers={}
    for layer in ['diplomatic','current']:
        s=(ROOT/f'fr/sga6/{layer}/main.tex').read_text()
        s,log=apply_patches(s,layer,patches);logs.extend(log)
        sys.path.insert(0,str(ROOT/'review/front'))
        from front_markers import integrate_front
        s=integrate_front(s)
        layers[layer]=clean_private_metadata(s)
        (ROOT/f'build/FR_{layer}_revised.tex').write_text(layers[layer])
    (ROOT/'records/PATCH_APPLICATION_FR.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
    blocked=[x for x in logs if x['status']=='blocked']
    # Annotate body only. Preamble equality is a separate checked invariant.
    dp,db=layers['diplomatic'].split('\\begin{document}',1)
    cp,cb=layers['current'].split('\\begin{document}',1)
    if dp!=cp:raise ValueError('Source preambles differ; an explicit notation decision is required.')
    db=db.rsplit('\\end{document}',1)[0];cb=cb.rsplit('\\end{document}',1)[0]
    body,variants=annotate(db,cb,registry,patches)
    # Preserve original textual markers and add the margin representation.
    body=PAGE.sub(lambda m:m[0]+'\n\\SGAfolio{'+m[2].strip()+'}%',body)
    body=fit_heading_boxes(body)
    dp=dp.replace('\\usepackage[hidelinks]{hyperref}','\\usepackage[hidelinks,hyperfootnotes=false]{hyperref}')
    credits=(ROOT/'review/front/credits_fr.tex').read_text()
    master=dp+MACROS+'\n\\begin{document}\n'+credits+PREFACE+body+apparatus(variants)+'\n\\end{document}\n'
    (out/'SGA6_FR_master_annote_DRAFT.tex').write_text(master)
    for mode,name in [(0,'SGA6_FR_diplomatique_DRAFT.tex'),(1,'SGA6_FR_corrige_apparat_DRAFT.tex'),(2,'SGA6_FR_texte_de_lecture_DRAFT.tex')]:
        (out/name).write_text('\\def\\SGAform{'+str(mode)+'}\n'+master)
    (ROOT/'records/FR_VARIANTS.json').write_text(json.dumps(variants,ensure_ascii=False,indent=2)+'\n')
    write_tsv(ROOT/'records/FR_VARIANTS.tsv',variants,['id','page','printed','corrected','source','status','sha256_printed','sha256_corrected'])
    summary={'status':'draft, incomplete scan collation','variant_entries':len(variants),'patches_applied':sum(x['status']=='applied' for x in logs),'patches_blocked':len(blocked),'forms_generated':3,'preamble_equal':True}
    (ROOT/'records/FR_BUILD_GENERATION.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':make()
