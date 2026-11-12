#!/usr/bin/env python3
"""Lossless French collation and single-file reader construction.

The two authoritative text witnesses are never edited. Rendering-only additions
are reversible and kept separate from the source text and editorial decisions.
"""
import argparse
import collections
import csv
import difflib
import hashlib
import json
import re
from pathlib import Path
from french_provenance import AttributionSources

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'sources'
REC = ROOT/'output/records'
OUT = ROOT/'output/fr'
WORK = ROOT/'work'
MARK = re.compile(r'%{3,}\s*scan idx (\d+)\s*\|\s*folio ([^\s%]+)\s*%+')
TOKEN = re.compile(r'\\[a-zA-Z@]+|\\[^a-zA-Z@]|\s+|[^\W_]+|.',re.S)
EXPOSES = [('7I',x) for x in ['INTRO','I','II','VI','VII','VIII','IX']]+[('7II',x) for x in ['X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI','XXII']]


def jsonread(p):
    return json.loads(p.read_text())


def lines(p):
    return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]


def write_tsv(p, fields, rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore')
        w.writeheader();w.writerows(rows)


def comments_out(s):
    return re.sub(r'(?<!\\)%[^\n]*','',s)


def pages(s):
    ms=list(MARK.finditer(s))
    if not ms:return {'V–VII':s}
    return {m.group(2):s[m.end():ms[i+1].start() if i+1<len(ms) else len(s)] for i,m in enumerate(ms)}


def clean(s,vol,intro=False):
    """Keep all printable tokens, replacing page furniture by marginal anchors."""
    if intro:
        s=comments_out(s)
        s=re.sub(r'\\clearpage\s*\\thispagestyle\{empty\}\s*\\begin\{center\}\s*(VI|VII)\s*\\end\{center\}',
                 lambda m:'\n\\SGApage{I}{'+m.group(1)+'}\n',s)
        return '\\SGApage{I}{V}\n'+s
    s=MARK.sub(lambda m:'\\SGApage{'+('I' if vol=='7I' else 'II')+'}{'+m.group(2)+'}',s)
    return comments_out(s)


def paragraphs(s):
    """Split only at top-level paragraph boundaries, never within a TeX group.

    Page-marker tokens remain in exactly their original source positions. The
    scanner consumes complete control sequences, so escaped braces/dollars and
    line-break commands do not corrupt its state.
    """
    tokens=re.compile(r'\\begin\{([^}]+)\}|\\end\{([^}]+)\}|\\[a-zA-Z@]+|\\.|[{}$]|\n[ \t]*\n+',re.S)
    depth=0;env=[];math=False;start=0;out=[]
    for m in tokens.finditer(s):
        t=m.group()
        if m.group(1):env.append(m.group(1))
        elif m.group(2):
            if env and env[-1]==m.group(2):env.pop()
        elif t=='{':depth+=1
        elif t=='}':depth-=1
        elif t in ['$',r'\[',r'\]',r'\(',r'\)']:math=not math
        elif t.startswith('\n') and depth==0 and not env and not math:
            out.append(s[start:m.end()]);start=m.end()
    if start<len(s):out.append(s[start:])
    assert ''.join(out)==s
    return out


def token_changes(a,b):
    if a==b:return []
    at=TOKEN.findall(a);bt=TOKEN.findall(b)
    ap=[0];bp=[0]
    for t in at:ap.append(ap[-1]+len(t))
    for t in bt:bp.append(bp[-1]+len(t))
    result=[]
    for op,i,j,k,l in difflib.SequenceMatcher(None,at,bt,autojunk=False).get_opcodes():
        if op!='equal':
            result.append({'before':''.join(at[i:j]),'after':''.join(bt[k:l]),'a0':ap[i],'a1':ap[j],'b0':bp[k],'b1':bp[l],
                           'before_context':a[max(0,ap[i]-100):min(len(a),ap[j]+100)],
                           'after_context':b[max(0,bp[k]-100):min(len(b),bp[l]+100)]})
    return result


def folio(s,pos):
    ms=list(re.finditer(r'\\SGApage\{[^}]+\}\{([^}]+)\}',s[:pos+1]))
    return ms[-1].group(1) if ms else 'V–VII'


def math_at(s,pos):
    math=False;env=[]
    for m in re.finditer(r'\\begin\{([^}]+)\}|\\end\{([^}]+)\}|\\[A-Za-z@]+|\\.|\$',s[:pos],re.S):
        if m.group(1):env.append(m.group(1))
        elif m.group(2):
            if env and env[-1]==m.group(2):env.pop()
        elif m.group() in ['$',r'\[',r'\]',r'\(',r'\)']:math=not math
    return math or any(e in ['equation','equation*','align','align*','aligned','gather','gather*','array','tikzcd','matrix','cases'] for e in env)


def visible_hunk(h,old,new):
    a,b=h['before'],h['after']
    # Grouping a single zero-argument exponent token does not alter the print.
    # The paired source at I:500 adds these two braces around \natural.
    # Preserve both exact source spellings in the master/change log without
    # counting the redundant grouping as two additional critical readings.
    if not a and b in ('{','}'):
        for m in re.finditer(r'\^\{\\natural\}',new):
            if h['b0'] in (m.start()+1,m.end()-1) and h['b1']==h['b0']+1:
                return False
    if a.strip() or b.strip():return True
    if math_at(new,h['b0']):return False
    if a and b and ((a.count('\n')>=2)==(b.count('\n')>=2)):return False
    return True


def esc(s):
    table={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','$':r'\$','&':r'\&','#':r'\#','_':r'\_','%':r'\%',
           '^':r'\textasciicircum{}','~':r'\textasciitilde{}','\u200b':'','\u00a0':' '}
    return ''.join(table.get(c,c) for c in str(s))


def code(s):
    if not s:return r'\emph{(vide)}'
    if not s.strip():
        return r'\emph{('+str(s.count(' '))+' espace(s), '+str(s.count('\n'))+' retour(s) de ligne dans le témoin TeX)}'
    result=[]
    for token in re.findall(r'\s+|[^\s]{1,20}',s):
        if token.isspace():result.append(' ')
        else:result.append(esc(token)+r'\allowbreak{}')
    return r'{\ttfamily\footnotesize '+''.join(result)+'}'


class Sources(AttributionSources):
    def __init__(self):
        super().__init__(SRC, REC, token_changes)


def apply_decisions(vol,fn,text,layer):
    p=REC/'editorial_decisions.json'
    if not p.exists():return text,[]
    data=jsonread(p)
    candidates=data.get('patches',[]) if isinstance(data,dict) else []
    used=[]
    for r in candidates:
        if r.get('language','FR')!='FR' or r.get('volume') not in [vol,'SGA'+vol,vol.replace('7','')]:continue
        if r.get('file')!=fn:continue
        if layer not in r.get('layers',['current']):continue
        old,new=r['old'],r['new']
        count=text.count(old)
        if count!=r.get('expected_count',1):raise ValueError((r.get('id'),fn,count))
        text=text.replace(old,new,r.get('expected_count',1));used.append(r)
    return text,used


def apparatus_tex(entries):
    if not entries:return ''
    out=['\n\\ifnum\\SGAform=1\n\\clearpage\\section*{Apparat critique}\\small\n',
         'Les lectures ci-dessous sont données dans le TeX exact des témoins, afin de préserver les distinctions de notation. Les indices décimaux renvoient aux différences individuelles du passage marqué.\n']
    for e in entries:
        out.append('\n\\par\\medskip\\noindent\\hypertarget{app-'+e['id']+'}{}\\textbf{'+esc(e['id'])+'}'+
                   '\\quad p. '+esc(e['page'])+'; '+esc(e['kind'])+'.\\par\n')
        out.append('\\noindent Imprimé : '+code(e['before'])+'\\par\n')
        out.append('\\noindent Corrigé : '+code(e['after'])+'\\par\n')
        refs='; '.join(r'\nolinkurl{'+x.strip()+'}' for x in e['source_ref'].split(';'))
        out.append('\\noindent Source : '+esc(e['source'])+'. '+refs+'\\par\n')
    out.append('\n\\normalsize\\fi\n')
    return ''.join(out)


def make_data():
    REC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);WORK.mkdir(exist_ok=True)
    source=Sources();components=[];allentries=[];decisions=[];changes=[];markers=[];nonprinting=[]
    for vol,ex in EXPOSES:
        fn='general_introduction_body.tex' if ex=='INTRO' else f'expose_{ex}_body.tex'
        base=SRC/'fr'/('sga'+vol.lower())
        rawd=(base/'diplomatic'/fn).read_text();rawc=(base/'current'/fn).read_text()
        d,usedd=apply_decisions(vol,fn,rawd,'diplomatic');c,used=apply_decisions(vol,fn,rawc,'current')
        d=clean(d,vol,ex=='INTRO');c=clean(c,vol,ex=='INTRO')
        da,ca=paragraphs(d),paragraphs(c)
        out=[];entries=[];entry_spans={};group=0;aoffset=0;boffset=0
        offsets_a=[0];offsets_b=[0]
        for x in da:offsets_a.append(offsets_a[-1]+len(x))
        for x in ca:offsets_b.append(offsets_b[-1]+len(x))
        for op,i,j,k,l in difflib.SequenceMatcher(None,da,ca,autojunk=False).get_opcodes():
            if op=='equal':out.append(''.join(da[i:j]));continue
            old=''.join(da[i:j]);new=''.join(ca[k:l]);group+=1
            gid=f'F{vol}-{ex}-{group:03}'
            hunks=token_changes(old,new)
            entry_index=0
            for h in hunks:
                page=folio(c,offsets_b[k]+h['b0'])
                if not visible_hunk(h,old,new):
                    nonprinting.append({'volume':vol,'expose':ex,'page':page,'before':h['before'],'after':h['after'],
                                        'reason':'Nonprinting TeX whitespace/line wrapping or redundant grouping of a single exponent token; exact source projection retained without a printed-text apparatus entry.'})
                    continue
                entry_index+=1;n=entry_index
                eid=f'{gid}.{n}'
                entry_spans[eid]=((offsets_a[i]+h['a0'],offsets_a[i]+h['a1']),
                                  (offsets_b[k]+h['b0'],offsets_b[k]+h['b1']))
                entries.append(dict(h,id=eid,group_id=gid,volume=vol,expose=ex,page=page))
            out.append('\\SGAvar{'+old+'}{'+new+'}{'+(gid if entry_index else '')+'}')
        annotated=''.join(out)
        context=source.context('apparatus',vol,ex,fn,d,c,entries,
                               f'fr/sga{vol.lower()}/diplomatic/{fn}',f'fr/sga{vol.lower()}/current/{fn}')
        for entry in entries:
            src,ref,kind=source.match(context,entry['id'],entry,entry['page'],*entry_spans[entry['id']])
            entry.update(source=src,source_ref=ref,kind=kind)
            if src.startswith('ADOPT-'):
                decisions.append({'id':src,'volume':vol,'page':entry['page'],'file':fn,'printed':entry['before'],'corrected':entry['after'],
                                  'decision':'Retain the supplied corrected witness without additional normalization.',
                                  'reason':'This is a mechanically established difference between the two designated sources of record. The current witness is expressly the corrected authority for this build; the diplomatic reading remains recoverable. No new conjectural correction is introduced.',
                                  'source':ref})
            elif src.startswith('WITNESS-'):
                decisions.append({'id':src,'volume':vol,'page':entry['page'],'file':fn,'printed':entry['before'],'corrected':entry['after'],
                                  'decision':'Replace an unsupported individual historical citation by exact paired-witness attribution.',
                                  'reason':'Metadata-only attribution fallback: the earlier cited record does not support this actual changed span. Both existing readings and all entry/group identifiers remain unchanged. This is not a new textual correction or an expansion of the frozen ADOPT review cohort.',
                                  'source':ref})
        comp={'volume':vol,'expose':ex,'file':fn,'diplomatic':d,'corrected':c,'annotated':annotated,'entries':entries,
              'diplomatic_sha256':hashlib.sha256(d.encode()).hexdigest(),'corrected_sha256':hashlib.sha256(c.encode()).hexdigest(),
              'source_diplomatic_sha256':hashlib.sha256(rawd.encode()).hexdigest(),'source_current_sha256':hashlib.sha256(rawc.encode()).hexdigest(),
              'decisions':[r.get('id') for r in used+usedd]}
        components.append(comp);allentries.extend(entries)
        for form,text in [('diplomatic',d),('corrected',c),('reading',c)]:
            for m in re.finditer(r'\\SGApage\{([^}]+)\}\{([^}]+)\}',text):markers.append({'language':'FR','form':form,'volume':vol,'expose':ex,'folio':m.group(2),'source':f'fr/sga{vol.lower()}/{"diplomatic" if form=="diplomatic" else "current"}/{fn}'})
        for label,path in [('August diplomatic',SRC/'fr_baseline_aug2026'/('sga'+vol.lower())/'diplomatic'/fn),
                           ('August corrected',SRC/'fr_baseline_aug2026'/('sga'+vol.lower())/'corrected'/fn),
                           ('current',base/'current'/fn)]:
            before=clean(path.read_text(),vol,ex=='INTRO')
            def split_clean(s):
                ms=list(re.finditer(r'\\SGApage\{[^}]+\}\{([^}]+)\}',s))
                return {m.group(1):(m.start(),s[m.start():ms[q+1].start() if q+1<len(ms) else len(s)]) for q,m in enumerate(ms)}
            oldpages,newpages=split_clean(before),split_clean(c)
            pending=[]
            for page,(pageoffset,pagetext) in newpages.items():
                for h in token_changes(oldpages.get(page,(0,''))[1],pagetext):
                    ident=f'CFR-{len(changes)+len(pending)+1:05}'
                    row={'comparison':label,'page':f'{vol} {page}','place':fn+f' [corrected character {pageoffset+h["b0"]}]',
                         'before':h['before'],'after':h['after']}
                    oldoffset=oldpages.get(page,(0,''))[0]
                    pending.append({'id':ident,'page':page,'before':h['before'],'after':h['after'],'row':row,
                                    'old_span':(oldoffset+h['a0'],oldoffset+h['a1']),
                                    'new_span':(pageoffset+h['b0'],pageoffset+h['b1'])})
            context=source.context('changes',vol,ex,fn,before,c,pending,str(path.relative_to(SRC)),
                                   f'fr/sga{vol.lower()}/current/{fn}',label)
            for item in pending:
                row=item['row'];page=item['page']
                src,ref,kind=source.match(context,item['id'],row,page,item['old_span'],item['new_span'])
                if src.startswith('COLLATION-'):
                    decisions.append({'id':src,'volume':vol,'page':page,'file':fn,'printed':row['before'],'corrected':row['after'],
                                      'decision':'Adopt the final supplied corrected witness and recorded open-item decisions.',
                                      'reason':'Exact reproducible collation against the named baseline. This identifier records a source-selection decision, not a new claim to have examined the unavailable scan.',
                                      'source':str(path.relative_to(SRC))+'; '+f'fr/sga{vol.lower()}/current/{fn}'})
                elif src.startswith('WITNESS-'):
                    decisions.append({'id':src,'volume':vol,'page':page,'file':fn,'printed':row['before'],'corrected':row['after'],
                                      'decision':'Replace an unsupported historical change-log citation by paired-witness attribution.',
                                      'reason':'Metadata-only citation repair. The baseline comparison, row position, and exact before/after text are unchanged; this identifier introduces no textual decision.',
                                      'source':ref})
                changes.append(dict(row,source=src))
    attribution=source.finish(components,changes)
    (WORK/'fr_variant_data.json').write_text(json.dumps(components,ensure_ascii=False,indent=2)+'\n')
    (REC/'FR_APPARATUS.json').write_text(json.dumps(allentries,ensure_ascii=False,indent=2)+'\n')
    (REC/'FR_SOURCE_SELECTION_DECISIONS.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n')
    write_tsv(REC/'CHANGES_FR.tsv',['comparison','page','place','before','after','source'],changes)
    write_tsv(REC/'FR_PAGE_MARKERS.tsv',['language','form','volume','expose','folio','source'],markers)
    write_tsv(REC/'FR_NONPRINTING_DIFFERENCES.tsv',['volume','expose','page','before','after','reason'],nonprinting)
    print(json.dumps({'components':len(components),'apparatus_entries':len(allentries),'variant_blocks':sum(len(set(e['group_id'] for e in x['entries'])) for x in components),
                      'changes':dict(collections.Counter(x['comparison'] for x in changes)),
                      'original_adopt_cohort':sum(x['id'].startswith('ADOPT') for x in decisions),
                      'attribution_changes':{scope:attribution[scope]['metadata_changed'] for scope in ('apparatus','changes')}}))
    return components


def preamble():
    # Preserve the union of the two source preambles; only presentation is added.
    p=(SRC/'fr/sga7i/current/SGA7I_Fresh_Source_Transcription_Complete_Working.tex').read_text().split(r'\begin{document}')[0]
    p=re.sub(r'\\documentclass[^\n]+',r'\\documentclass[11pt,a4paper,leqno,oneside,openany]{book}',p)
    p=re.sub(r'\\pdfinfo\{.*?\n\}', '',p,flags=re.S)
    p=p.replace(r'\usepackage[french,english]{babel}',r'\usepackage[provide=*,french,english]{babel}'+'\n'+r'\usepackage{lmodern}')
    p=p.replace(r'\geometry{margin=2.4cm}',r'\geometry{left=21mm,right=21mm,top=22mm,bottom=23mm,marginparwidth=15mm,marginparsep=3mm}')
    p+=r'''
\usepackage{etoolbox,adjustbox,marginnote,xurl,hyperref}
\tikzcdset{ampersand replacement=\&}
\tikzset{ampersand replacement=\&}
\hypersetup{hidelinks,hypertexnames=false,pdfauthor={GPT-6 Astra; source authors credited in the edition},pdftitle={SGA 7 I et II - lecteur francais}}
\BeforeBeginEnvironment{tikzcd}{\begin{adjustbox}{max width=\linewidth}}
\AfterEndEnvironment{tikzcd}{\end{adjustbox}}
\setcounter{tocdepth}{1}
\setlength{\emergencystretch}{4em}
\newcount\SGAform
\SGAform=FORM_NUMBER
\ifnum\SGAform=0
  \long\def\SGAvar#1#2#3{#1}
\else\ifnum\SGAform=1
  \long\def\SGAvar#1#2#3{\SGAvmark{#3}#2}
\else
  \long\def\SGAvar#1#2#3{#2}
\fi\fi
\newcommand{\SGAvmark}[1]{\ifstrempty{#1}{}{\leavevmode\textsuperscript{\tiny\hyperlink{app-#1.1}{[#1]}}\ignorespaces}}
\newcommand{\SGApage}[2]{\marginnote{\normalfont\scriptsize #1\,\textbf{#2}}}
\newcommand{\SGAtoc}[1]{\phantomsection\addcontentsline{toc}{chapter}{#1}}
\newcommand{\SGAtocunderline}[1]{\ifmmode\mathunderline{#1}\else #1\fi}
\newcommand{\SGAsectiontoc}[2]{\phantomsection\addcontentsline{toc}{section}{\texorpdfstring{#1}{Section #2}}}
'''
    return p


def render_transport(s):
    """Catcode-only spelling needed when a TikZ matrix is in a macro argument."""
    s=re.sub(r'\\begin\{(equation\*?|align\*?|aligned|gather\*?|multline\*?|split|displaymath|eqnarray\*?|tikzcd)\}.*?\\end\{\1\}',
             lambda m:re.sub(r'\n[ \t]*\n+', '\n',m.group()),s,flags=re.S)
    s=re.sub(r'(?<!\\)\\\[.*?(?<!\\)\\\]',lambda m:re.sub(r'\n[ \t]*\n+', '\n',m.group()),s,flags=re.S)
    def replace(m):
        return re.sub(r'\\(?:[A-Za-z@]+|.)|&',lambda t:r'\&' if t.group()=='&' else t.group(),m.group(),flags=re.S)
    return re.sub(r'\\begin\{(tikzcd|tikzpicture)\}.*?\\end\{\1\}',replace,s,flags=re.S)


def add_section_contents(s,component):
    pattern=re.compile(r'^(?:(?:(?:\\S(?:\{\})?|§)\s*)?(\d+)\.?(?:\s|\\quad|\\qquad)+\\underline\{|\\underline\{(?:(?:\\S|§)\s*)?(\d+)\.?(?:\s|\\quad|\\qquad)+)')
    candidates={}
    for layer in ['diplomatic','corrected']:
        for line in component[layer].splitlines():
            line=line.strip();m=pattern.match(line)
            balance=0
            for q in re.finditer(r'\\.|[{}]',line):
                if q.group()=='{':balance+=1
                elif q.group()=='}':balance-=1
            if m and len(line)<900 and balance==0:candidates[line]=(m.group(1) or m.group(2),line)
            wrapped=re.match(r'^\\section\*\{(\d+)\.\s.*\}$',line)
            if wrapped and balance==0:candidates[line]=(wrapped.group(1),line[len(r'\section*{'):-1])
    def strip_text_underlining(t):
        out=[];i=0;math=False
        while i<len(t):
            if t.startswith(r'\underline{',i) and not math:
                k=i+len(r'\underline{');j=k;d=1
                while j<len(t) and d:
                    if t[j]=='\\':
                        q=re.match(r'\\(?:[A-Za-z@]+|.)',t[j:],re.S);j+=len(q.group());continue
                    if t[j]=='{':d+=1
                    elif t[j]=='}':d-=1
                    j+=1
                out.append(strip_text_underlining(t[k:j-1]));i=j;continue
            if t[i]=='\\':
                q=re.match(r'\\(?:[A-Za-z@]+|.)',t[i:],re.S);v=q.group()
                out.append((r'\protect' if v==r'\underline' else '')+v);i+=len(v);continue
            if t[i]=='$':math=not math
            out.append(t[i]);i+=1
        return ''.join(out)
    for line,(n,heading) in sorted(candidates.items(),key=lambda x:-len(x[0])):
        if line not in s:continue
        # Grouping braces are harmless in contents; suppress text underlining
        # locally while preserving the full heading, including trailing math.
        title=strip_text_underlining(heading)
        added='\\SGAsectiontoc{'+title+'}{'+n+'}\n'
        s=s.replace(line,added+line)
    return s


def build_readers(components):
    parts=[];currentvol=None
    titles={'INTRO':'Introduction générale'}
    for c in components:
        texts=re.findall(r'\\underline\{\\underline\{([^{}]+)\}\}',c['corrected'][:2500])
        if texts:titles[c['expose']]=' '.join(' '.join(t.split()) for t in texts)
    titles['XXII']=titles.get('XXII','')+' '+r'\texorpdfstring{$\zeta$}{zeta}'
    xii=next(c for c in components if c['expose']=='XII')
    boundary=xii['annotated'].index(r'\SGApage{II}{82}')
    xiiititle=xii['annotated'][boundary:]
    titles['XIII']='Le formalisme des cycles évanescents'
    for c in components:
        vol,ex=c['volume'],c['expose']
        if vol!=currentvol:
            currentvol=vol
            parts.append('\\part{SGA 7 '+('I' if vol=='7I' else 'II')+'}\n')
        title=titles.get(ex,'Exposé '+ex)
        toc=title if ex=='INTRO' else 'Exposé '+ex+' — '+title if ex in titles else title
        # These title strings come from the transcribed headings. Preserve math.
        parts.append('\\clearpage\\SGAtoc{'+toc+'}\n')
        parts.append('\\selectlanguage{'+('english' if ex=='VI' else 'french')+'}\n')
        if ex=='XIII':parts.append(xiiititle)
        parts.append(add_section_contents(c['annotated'][:boundary] if ex=='XII' else c['annotated'],c))
        parts.append('\\selectlanguage{french}\n'+apparatus_tex(c['entries']))
    front=(WORK/'frontmatter_fr.tex').read_text() if (WORK/'frontmatter_fr.tex').exists() else ''
    body=render_transport(''.join(parts))
    if (WORK/'unresolved_fr.tex').exists():
        body+='\n\\ifnum\\SGAform=1\n\\clearpage\n'+(WORK/'unresolved_fr.tex').read_text()+'\n\\fi\n'
    intro=r'''
\begin{document}
\selectlanguage{french}
\frontmatter
\begin{titlepage}\centering
{\Large Séminaire de géométrie algébrique du Bois Marie\par}\vspace{20mm}
{\Huge\bfseries SGA 7\par}\vspace{8mm}
{\LARGE Groupes de monodromie en géométrie algébrique\par}\vspace{8mm}
{\Large Volumes I et II\par}\vspace{16mm}
{\Large FORM_LABEL\par}\vfill
{\large Édition du 12 novembre 2026\par}
{\large GPT-6 Astra (OpenAI, ChatGPT Pro mode)\par}
\end{titlepage}
\section*{Présentation de cette forme}
FORM_PREFACE
Les numéros marginaux renvoient exclusivement aux folios de l'imprimé : I~1--528 et II~1--438. L'introduction générale porte les repères I~V--VII (V est inféré dans les sources). La pagination du présent volume est indépendante.
'''
    tail='\n\\end{document}\n'
    forms=[('SGA7_FR_diplomatique',0,'Texte diplomatique',"Le texte suit le témoin diplomatique fourni ; les coquilles de l'imprimé sont conservées. Les réparations de transcription déjà établies restent présentes. Les repères de chaque page de l'imprimé sont indiqués en marge."),
           ('SGA7_FR_corrige_apparat',1,'Texte corrigé avec apparat',"Le texte suit le témoin corrigé fourni et les décisions documentées de cette édition. Chaque passage différent du témoin diplomatique est marqué ; chaque différence individuelle est donnée dans l'apparat de l'exposé avec les deux lectures et sa source. Les notes indécidables sans scan sont séparées des variantes effectives."),
           ('SGA7_FR_texte_de_lecture',2,'Texte de lecture',"Le texte est exactement le texte corrigé. Cette forme omet les marques de variantes, l'apparat et les notes éditoriales de lecture indécidable. Elle conserve intégralement le texte, les notes des auteurs, les bibliographies, le catalogue de l'éditeur et les seuls repères des folios imprimés en marge.")]
    master=preamble()+intro.replace('FORM_LABEL',r'\ifcase\SGAform Texte diplomatique\or Texte corrigé avec apparat\or Texte de lecture\fi').replace('FORM_PREFACE',r'\ifcase\SGAform '+forms[0][3]+r'\or '+forms[1][3]+r'\or '+forms[2][3]+r'\fi')+front+'\n\\tableofcontents\n\\mainmatter\n'+body+tail
    master=master.replace('FORM_NUMBER','1')
    (OUT/'SGA7_FR_master_annote.tex').write_text(master)
    for name,mode,label,preface in forms:
        text=master.replace('\\SGAform=1\n','\\SGAform='+str(mode)+'\n',1)
        (OUT/(name+'.tex')).write_text(text)
    print('French master and three standalone forms written.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--data-only',action='store_true');args=parser.parse_args()
    data=make_data()
    if not args.data_only:build_readers(data)


if __name__=='__main__':main()
