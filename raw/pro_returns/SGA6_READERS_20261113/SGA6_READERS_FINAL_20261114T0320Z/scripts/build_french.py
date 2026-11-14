#!/usr/bin/env python3
"""Build source-locked French candidates from reviewed patches and layered inputs.

Each annotation has both exact alternatives and an explicit provenance record.
The release gate is separate: a successful build does not imply scan collation.
"""
import argparse
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

def post_review_patches():
    """Explicit final typography pass, anchored in the composed reviewed text."""
    result=[]
    for directory in sorted((ROOT/'review').iterdir()):
        if directory.is_dir():result.extend(get_jsonl(directory/'post_review_patches.jsonl'))
    return result

def integrate_additional_pages(text,layer):
    """Insert declared source leaves at exact anchors or before the document ends."""
    additions=[]
    for directory in sorted((ROOT/'review').iterdir()):
        if not directory.is_dir():continue
        for row in get_jsonl(directory/'new_pages.jsonl'):
            if row.get('layer') in [layer,'both']:
                additions.append(row)
    if not additions:return text
    existing,_=split_pages(text)
    keys=[row['page'] for row in additions]
    assert len(set(keys))==len(keys),'Duplicate new-page key'
    assert all(key not in existing for key in keys),'New page already present'
    for row in additions:
        marks=list(PAGE.finditer(row['text']))
        assert len(marks)==1 and marks[0][2].strip()==str(row['page'])
        assert int(marks[0][1])+1==row['pdf_page']
    additions.sort(key=lambda row:row['pdf_page'])
    rear=[]
    for row in additions:
        anchor=row.get('insert_before')
        if anchor:
            assert text.count(anchor)==1,(row['page'],'new-page insertion anchor')
            text=text.replace(anchor,row['text']+anchor,1)
        else:
            rear.append(row)
    assert text.count('\\end{document}')==1
    return text.replace('\\end{document}','\n'+''.join(row['text'] for row in rear)+'\\end{document}',1)

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

def anchor_heading_folios(body,write_record=False):
    """Attach an initial marginal label to the following heading paragraph.

    A margin note in vertical mode can remain on the preceding output page
    when TeX moves a heading. Only zero-text prefixes are crossed; source
    comments and all author tokens remain in their original order.
    """
    spans=list(PAGE.finditer(body));edits=[]
    for n,m in enumerate(spans):
        folio=m[2].strip();end=spans[n+1].start() if n+1<len(spans) else len(body)
        command='\\SGAfolio{'+folio+'}'
        start=m.end()+1
        if not body.startswith(command,start):continue
        i=start+len(command)
        while i<end:
            ws=re.match(r'(?:\s+|%[^\n]*(?:\n|$))+',body[i:end])
            if ws:i+=len(ws[0]);continue
            layout=re.match(r'\\(?:clearpage|newpage)\b',body[i:end])
            if layout:i+=len(layout[0]);continue
            declaration=re.match(r'\\(?:providecommand|renewcommand|newcommand)\*?\s*\{?\\[A-Za-z@]+',body[i:end])
            if declaration:
                j=i+len(declaration[0])
                if body[j:j+1]=='}':j+=1
                while True:
                    while j<end and body[j].isspace():j+=1
                    if body[j:j+1]=='[':j=brace_end(body,j,'[',']')
                    else:break
                if body[j:j+1]!='{':break
                i=brace_end(body,j);continue
            break
        heading=re.match(r'\\(?:section|subsection|subsubsection)\*?\{',body[i:end])
        if not heading:continue
        insert=i+len(heading[0]);old=body[start:insert]
        new=body[start+len(command):insert]+command
        assert old.startswith(command) and new.endswith(command)
        assert command+new[:-len(command)]==old
        edits.append({'folio':folio,'start':start,'end':insert,'old':old,'new':new,
                      'heading_command':heading[0],'crossed_prefix':body[start+len(command):i]})
    revised=body
    for e in reversed(edits):revised=revised[:e['start']]+e['new']+revised[e['end']:]
    # Each move has equal byte length, so all saved offsets remain valid.
    restored=revised
    for e in reversed(edits):
        assert restored[e['start']:e['end']]==e['new']
        restored=restored[:e['start']]+e['old']+restored[e['end']:]
    assert restored==body
    assert PAGE.findall(revised)==PAGE.findall(body)
    if write_record:
        (ROOT/'records/FR_HEADING_FOLIO_ANCHORS.json').write_text(json.dumps({'method':'Move only the generated visible marginal-label command across an explicitly parsed zero-text prefix into the first heading argument. The original source marker, author tokens, macro declarations and numerical label are unchanged; exact inverse reconstruction passes. This prevents a heading page break from leaving its label on the previous output page.','applications':len(edits),'exact_inverse':True,'source_marker_sequence_identical':True,'moves':edits},ensure_ascii=False,indent=2)+'\n')
    return revised

def start_exposes_on_new_pages(body,write_record=False):
    """Add an edition-only page break before each original exposé opening.

    This keeps an exposé's title, byline and opening together. Removing the
    fourteen recorded insertions reconstructs the input literally.
    """
    starts={'1','78','160','222','274','297','365','416','466','498','519','595','616','667'}
    prefix='\\clearpage\n% Edition layout: a fresh output page for the following exposé.\n'
    matches=[m for m in PAGE.finditer(body) if m[2].strip() in starts]
    assert len(matches)==len(starts)==14
    edits=[{'folio':m[2].strip(),'offset':m.start(),'inserted':prefix} for m in matches]
    revised=body
    for e in reversed(edits):revised=revised[:e['offset']]+prefix+revised[e['offset']:]
    restored=revised
    for i,e in reversed(list(enumerate(edits))):
        offset=e['offset']+i*len(prefix)
        assert restored[offset:offset+len(prefix)]==prefix
        restored=restored[:offset]+restored[offset+len(prefix):]
    assert restored==body and PAGE.findall(revised)==PAGE.findall(body)
    if write_record:
        (ROOT/'records/FR_EXPOSE_OPENING_LAYOUT.json').write_text(json.dumps({
          'method':'Insert a generated clearpage before each of the fourteen original exposé-opening source markers. No author token or source marker is changed. Exposé XI has no body and receives no insertion. Removing the recorded insertions reconstructs the prior body exactly.',
          'applications':len(edits),'exact_inverse':True,'source_marker_sequence_identical':True,'insertions':edits},ensure_ascii=False,indent=2)+'\n')
    return revised

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

def annotate(dipl,corr,registry,patches,readable=False):
    # An exact atom diff is computed page by page to prevent cross-page matches.
    da,do=split_pages(dipl);ca,co=split_pages(corr)
    assert list(da)==list(ca),'The two layers have differing marker sequences.'
    pieces=[];variants=[];left_roundtrip=[];right_roundtrip=[];render_left=[];render_right=[]
    for page in da:
        a=atoms(da[page]);b=atoms(ca[page])
        ops=list(difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes())
        consumed_tail=0
        apos=[0];bpos=[0]
        for token in a:apos.append(apos[-1]+len(token))
        for token in b:bpos.append(bpos[-1]+len(token))
        for op_index,(tag,i,j,k,l) in enumerate(ops):
            before=''.join(a[i:j]);after=''.join(b[k:l])
            left_roundtrip.append(before);right_roundtrip.append(after)
            if tag=='equal':
                pieces.append(before[consumed_tail:]);render_left.append(before[consumed_tail:]);render_right.append(before[consumed_tail:]);consumed_tail=0;continue
            id=f'FRV{len(variants)+1:04d}'
            src=provenance(page,before,after,registry)
            for p in patches:
                if str(p['page'])==str(page) and p['old'] in before and p['new'] in after:
                    src.append(p['source_id'])
            if not src:src=[f'LAYER-DIFFERENCE:{page}:{id}']
            v={'id':id,'page':page,'printed':before,'corrected':after,'source':list(dict.fromkeys(src)),
              'status':'requires individual scan-decision linkage','sha256_printed':hashlib.sha256(before.encode()).hexdigest(),'sha256_corrected':hashlib.sha256(after.encode()).hexdigest(),
              'diplomatic_page_offset':apos[i],'corrected_page_offset':bpos[k]}
            prefix='';tail='';command='SGAvar'
            if readable:
                from fr_readable_apparatus import context_and_tail,DISPLAY
                previous=''.join(a[ops[op_index-1][1]:i]) if op_index and ops[op_index-1][0]=='equal' else ''
                following=''.join(a[j:ops[op_index+1][2]]) if op_index+1<len(ops) and ops[op_index+1][0]=='equal' else ''
                prefix,tail=context_and_tail(before,after,previous,following)
                consumed_tail=len(tail)
                if DISPLAY.match(after):command='SGAvarDisplay'
                v.update(apparatus_context_prefix=prefix,marker_tail=tail,marker_mode='display margin' if command=='SGAvarDisplay' else 'inline superscript after complete lexical tail')
            variants.append(v)
            render_left.append(before+tail);render_right.append(after+tail)
            pieces.append('\\'+command+'{'+macro_safe(before+tail)+'}{'+macro_safe(after+tail)+'}{'+id+'}')
    # The reversible model itself, independent from TeX expansion, is checked.
    assert sum(v['printed']!=v['corrected'] for v in variants)==len(variants)
    assert ''.join(left_roundtrip)==dipl
    assert ''.join(right_roundtrip)==corr
    assert ''.join(render_left)==dipl
    assert ''.join(render_right)==corr
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

FINAL_PREFACE=r'''
\section*{Présentation de cette édition}
Cette édition est établie à partir des deux couches françaises fournies et
de la seconde collation des 720 feuillets du volume numérisé, avec consultation
du second exemplaire pour les lectures précisées dans le dossier. Les décisions
sur les corrections antérieures et sur les conventions sont consignées dans les
tables accompagnant les lecteurs.

\ifnum\SGAform=0
La présente forme diplomatique conserve les lectures imprimées, y compris les
coquilles adjugées. Les numéros en marge situent les pages de l'original.
\else\ifnum\SGAform=1
La présente forme corrigée signale chaque différence avec la lecture
diplomatique par un appel entre crochets. L'apparat donne les deux lectures et
leurs sources; les motifs complets sont conservés dans le dossier de décisions.
\else
La présente forme de lecture donne le texte corrigé sans les appels ni notre
apparat. Elle conserve l'Introduction, les notes des auteurs et des éditeurs,
les tables et les autres matières imprimées transcrites. Les numéros en marge
sont ceux des pages de l'original.
\fi\fi
Les conventions de notation sont explicites dans le dossier. Les identifications
qui justifient une autre représentation typographique y sont précisées.
L'exposé XI porte dans la table originale la mention « Non rédigé ».

Le dossier donne des contre-exemples aux assertions imprimées examinées aux
pages 431, 443 et 590--592. Le texte des auteurs est conservé à ces endroits,
aucune émendation textuelle unique n'ayant été établie. Les blancs de références
de la page 464 et les appartenances à des groupes intégraux de la page 465 sont
également conservés; les limites constatées et les calculs exacts figurent dans
les décisions correspondantes. Ces passages inchangés ne créent pas d'entrée
dans l'apparat des variantes.

Une partie de l'avis original de l'éditeur est masquée par une étiquette dans
l'exemplaire numérisé. Elle est restituée d'après l'avis correspondant de
\textit{Lecture Notes in Mathematics}~228, Springer, 1971, dont les 17 points
visibles comparés concordent. Cette restitution provient de ce modèle
contemporain; les traits cachés de l'exemplaire de SGA~6 n'ont pas été récupérés.
Les cachets, codes-barres, annotations manuscrites et étiquettes propres à cet
exemplaire ne font pas partie de la transcription de l'œuvre imprimée.

Ce travail est AI-transcribed; les couches et corrections de Codex (août 2026),
le contrôle de chaque page numérotée par Claude Opus 5.5 à effort max
(10--13 novembre 2026), ainsi que les corrections de cette édition sont
AI-produced corrections. Cette édition est produite par GPT-6 Astra
(OpenAI, ChatGPT Pro mode). L'anglais correspondant est AI-translated.

Les droits sur l'œuvre originale appartiennent à son auteur, à ses représentants
ou à ses ayants droit. Dans la mesure où nous détenons des droits sur la
transcription, la traduction, les corrections et la composition produites par
l'IA, nous les consacrons au domaine public sous CC0 1.0. Cette édition est publiée
à des fins éducatives et non lucratives, et nous ne revendiquons aucun droit que
nous ne détenons pas. Si vous détenez des droits sur cette œuvre et vous opposez
à sa publication ici, veuillez ouvrir une issue GitHub et nous la retirerons.
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

def make(final=False):
    out=ROOT/('readers/fr/final' if final else 'readers/fr');out.mkdir(parents=True,exist_ok=True)
    registry=json.loads((ROOT/'build/registry.json').read_text())
    patches=all_patches();final_patches=post_review_patches();logs=[];layers={}
    original_patches=[p for p in patches if p['page']=='front' or str(p['page']).isdigit()]
    named_page_patches=[p for p in patches if p not in original_patches]
    for layer in ['diplomatic','current']:
        s=(ROOT/f'fr/sga6/{layer}/main.tex').read_text()
        s,log=apply_patches(s,layer,original_patches);logs.extend(log)
        sys.path.insert(0,str(ROOT/'review/front'))
        from front_markers import integrate_front
        s=integrate_front(s)
        s=integrate_additional_pages(s,layer)
        s,log=apply_patches(s,layer,named_page_patches);logs.extend(log)
        s,log=apply_patches(s,layer,final_patches);logs.extend(log)
        layers[layer]=clean_private_metadata(s)
        (ROOT/f'build/FR_{layer}_revised.tex').write_text(layers[layer])
    (ROOT/'records/PATCH_APPLICATION_FR.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
    blocked=[x for x in logs if x['status']=='blocked']
    # Annotate body only. Preamble equality is a separate checked invariant.
    dp,db=layers['diplomatic'].split('\\begin{document}',1)
    cp,cb=layers['current'].split('\\begin{document}',1)
    if dp!=cp:raise ValueError('Source preambles differ; an explicit notation decision is required.')
    db=db.rsplit('\\end{document}',1)[0];cb=cb.rsplit('\\end{document}',1)[0]
    body,variants=annotate(db,cb,registry,patches+final_patches,readable=final)
    extra_macros=''
    if final:
        from fr_readable_apparatus import sourced_variants,prepare_macro_states,readable_apparatus,READABLE_MACROS
        variants=sourced_variants(variants)
        extra_macros=READABLE_MACROS+prepare_macro_states(dp+'\\begin{document}'+cb,variants)
        extra_macros+=''.join(r'\expandafter\def\csname SGANumber@'+v['id']+r'\endcsname{'+str(i)+'}\n' for i,v in enumerate(variants,1))
        final_apparatus=readable_apparatus(variants)
    else:final_apparatus=apparatus(variants)
    # Preserve original textual markers and add the margin representation.
    # The documented blank source leaves have no visible text position.
    # Keep their exact source markers, without stacking empty margin labels.
    blank_leaves={'IV','VI','X','690','rear-715','rear-716'}
    body=PAGE.sub(lambda m:m[0]+('\n' if m[2].strip() in blank_leaves else
      '\n\\SGAfolio{'+m[2].strip()+'}%'),body)
    if final:
        body=anchor_heading_folios(body,write_record=True)
        body=start_exposes_on_new_pages(body,write_record=True)
    body=fit_heading_boxes(body)
    dp=dp.replace('\\usepackage[hidelinks]{hyperref}','\\usepackage[hidelinks,hyperfootnotes=false]{hyperref}')
    credits=(ROOT/'review/front/credits_fr.tex').read_text()
    master=dp+MACROS+extra_macros+'\n\\begin{document}\n'+credits+(FINAL_PREFACE if final else PREFACE)+body+final_apparatus+'\n\\end{document}\n'
    suffix='' if final else '_DRAFT'
    (out/('SGA6_FR_master_annote'+suffix+'.tex')).write_text(master)
    for mode,name in [(0,'SGA6_FR_diplomatique'+suffix+'.tex'),(1,'SGA6_FR_corrige_apparat'+suffix+'.tex'),(2,'SGA6_FR_texte_de_lecture'+suffix+'.tex')]:
        (out/name).write_text('\\def\\SGAform{'+str(mode)+'}\n'+master)
    (ROOT/'records/FR_VARIANTS.json').write_text(json.dumps(variants,ensure_ascii=False,indent=2)+'\n')
    write_tsv(ROOT/'records/FR_VARIANTS.tsv',variants,['id','page','printed','corrected','source','status','sha256_printed','sha256_corrected'])
    summary={'status':'final French sources; compilation and release checks recorded separately' if final else 'working source assembly','variant_entries':len(variants),'patches_applied':sum(x['status']=='applied' for x in logs),'patches_blocked':len(blocked),'forms_generated':3,'preamble_equal':True,
             'branch_source_roundtrip_exact':True,'readable_apparatus':final,'sourced_entries':len(variants) if final else None}
    (ROOT/'records/FR_BUILD_GENERATION.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--final',action='store_true');args=parser.parse_args();make(final=args.final)
