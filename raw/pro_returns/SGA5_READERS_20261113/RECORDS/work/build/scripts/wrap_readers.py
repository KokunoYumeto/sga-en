from __future__ import annotations
import argparse, json, re, importlib.util
from pathlib import Path
from sga5_common import *

NAMES={
 'FR':['SGA5_FR_diplomatique','SGA5_FR_corrige_apparat','SGA5_FR_texte_de_lecture'],
 'EN':['SGA5_EN_diplomatic','SGA5_EN_corrected_apparatus','SGA5_EN_reading']}

SUPPORT=r'''
% Reader infrastructure. The original mathematical macro definitions are above.
\usepackage{xcolor,marginnote,fvextra,xparse,needspace}
\setlength{\marginparwidth}{48pt}
\setlength{\marginparsep}{8pt}
\setlength{\emergencystretch}{3em}
\setcounter{tocdepth}{2}
\newif\ifSGAcontents
\SGAcontentsfalse
\newcounter{SGAfolioocc}
\newcommand{\SGAFolio}[1]{%
  \ifmmode\hbox to 0pt{\hypertarget{print-#1}{}\marginnote{\raggedright\sffamily\scriptsize #1}\hss}%
  \else\hypertarget{print-#1}{}\marginnote{\raggedright\sffamily\scriptsize #1}\fi}
\newcommand{\SGAFolioGap}{\ifmmode\hbox to0pt{\marginnote{\raggedright\sffamily\tiny 434 bis;\par 435 absent}[12pt]\hss}\else\marginnote{\raggedright\sffamily\tiny 434 bis;\par 435 absent}[12pt]\fi}
\makeatletter
\DeclareRobustCommand{\SGAmark}[1]{%
  \ifnum\SGAform=1\relax\ifSGAcontents\else
    \ifmeasuring@\hbox{\raise.7ex\hbox{\sffamily\tiny[\csname SGAnum@#1\endcsname]}}%
    \else\hypertarget{loc-#1}{}\hyperlink{app-#1}{\hbox{\raise.7ex\hbox{\color{blue!60!black}\sffamily\tiny[\csname SGAnum@#1\endcsname]}}}\fi
  \fi\fi}
\protected\long\def\SGAvar#1#2#3{\ifnum\SGAform=0\relax#1\else#2\SGAmark{#3}\fi}
\makeatother
\DefineVerbatimEnvironment{SGARead}{Verbatim}{fontsize=\footnotesize,breaklines=true,breakanywhere=true,baselinestretch=0.92}
\pdfstringdefDisableCommands{\def\SGAvar#1#2#3{#2}\def\SGAmark#1{}\def\SGAFolio#1{}}
'''

def title(lang):
    if lang=='FR':
        forms=[r'Édition diplomatique',r'Texte corrigé avec apparat',r'Texte de lecture']
        subtitle=r'Cohomologie $\ell$-adique et fonctions $L$'
        note='Séminaire de Géométrie Algébrique du Bois-Marie 1965--66'
    else:
        forms=['Diplomatic edition','Corrected text with apparatus','Reading text']
        subtitle=r'$\ell$-adic Cohomology and $L$-functions'
        note=r'S\'eminaire de G\'eom\'etrie Alg\'ebrique du Bois-Marie 1965--66'
    f=r'\ifcase\SGAform '+forms[0]+r'\or '+forms[1]+r'\or '+forms[2]+r'\fi'
    return r'\begin{titlepage}\centering\vspace*{2cm}{\Huge\bfseries SGA 5\par}\vspace{1cm}{\LARGE '+subtitle+r'\par}\vspace{.8cm}{\large '+note+r'\par}\vspace{.8cm}{\large A.~Grothendieck\par}\smallskip L.~Illusie, '+('éditeur' if lang=='FR' else 'editor')+r'\par\vspace{1.2cm}{\Large '+f+r'\par}\vfill Lecture Notes in Mathematics 589\par Springer-Verlag, 1977\par\vspace{.7cm}'+('Édition de lecture du 13 novembre 2026' if lang=='FR' else 'Reader edition, 13 November 2026')+r'\par\smallskip GPT-6 Astra (OpenAI, ChatGPT Pro mode)\par\end{titlepage}'+'\n'

def preface(lang):
    if lang=='FR':
        return r'''
\section*{Mode d'emploi de cette édition}
\ifcase\SGAform
Ce lecteur reproduit la couche diplomatique vérifiée fournie avec les sources : les erreurs de l'imprimé y sont conservées. Les 32 lectures de $R\Gamma$ des pages 457--474 ont été revues sur les images jointes; le $R$ doublement souligné est reproduit à chacun de ces endroits. Les numéros marginaux repèrent les changements de page de l'imprimé.
\or
Ce lecteur donne la couche corrigée. Chaque variante avec la lecture diplomatique porte un appel chiffré renvoyant à l'apparat en fin de volume. Une entrée donne les deux lectures exactes en code TeX et leur source; les conventions de macros sont développées explicitement quand elles changent un glyphe imprimé. Les appels sont des liens vers l'apparat, dont les numéros renvoient au lieu du texte. Les questions conservées faute d'image sont réunies dans des notes séparées et ne sont pas comptées comme variantes.
\or
Ce texte de lecture donne intégralement la couche corrigée. Les appels éditoriaux, l'apparat des variantes et les notes de décisions ont été laissés hors de ce lecteur. Les notes originales, toutes les démonstrations, les références et les deux index sont conservés. Seuls les numéros de page de l'imprimé figurent en marge. Les corrections et leurs sources sont consignées dans les fichiers de contrôle joints.
\fi
Les pages originales sont 1--484. L'imprimé répète la page 434 à la place de la page 435; les repères passent donc de 434 à 436. Cette répétition est signalée en marge à cet endroit. La table qui suit est produite à partir des titres présents dans le texte. Le texte manquant du frontispice, de l'Introduction de L.~Illusie (iii--viii), de la Liste des SGA et de la Table des matières originale est décrit dans le README.
\clearpage
'''
    return r'''
\section*{How to use this edition}
\ifcase\SGAform
This reader follows the supplied checked diplomatic layer and retains printed misprints where they affect the English. The 32 readings of $R\Gamma$ on printed pages 457--474 were inspected in the attached scans; double-underlined upright $R$ is reproduced at every one of these places. Marginal folios identify the verified alignments with the French print. The alignment register records the textual anchors.
\or
This reader gives the corrected layer. Every difference from the diplomatic reading carries a numbered link to the apparatus at the end. Each entry gives the exact two readings in TeX notation and their sources; scoped macros are expanded explicitly wherever they change a printed glyph. The apparatus number links back to the text. Unresolved readings retained for want of a scan are presented in a separate notes section and are not counted as variants.
\or
This reading text contains the complete corrected layer. Editorial variant calls, the apparatus and decision notes have been omitted from this reader. Original footnotes, all proofs, references and both indexes are retained. Printed folios appear only in the margin. The accompanying records retain all corrections and their sources.
\fi
The original text occupies printed pages 1--484. The print repeats page 434 in the place of page 435; the folio sequence consequently passes from 434 to 436. A marginal notice records this repetition. English folios are attached to source-supported section or formula anchors, as detailed in the alignment register. The contents below are generated from the headings in the text. The original title page, L.~Illusie's Introduction (iii--viii), Liste des SGA and original Table des mati\`eres have no transcription in the supplied sources; the README records these omissions.
\clearpage
'''

TOC_HOOK=r'''
\let\SGAoriginalsection\section
\let\SGAoriginalsubsection\subsection
\newcommand{\SGAcontentsentry}[2]{\begingroup\def\footnote##1{}\addcontentsline{toc}{#1}{#2}\endgroup}
\newcommand{\SGAtopheading}[1]{\SGAoriginalsection*{#1}\SGAcontentsentry{section}{#1}}
\newcommand{\SGAprintedtopheading}[1]{\SGAoriginalsection*{#1}}
\newcommand{\SGAlevelheading}[1]{\SGAoriginalsubsection*{#1}\SGAcontentsentry{subsection}{#1}}
\RenewDocumentCommand{\section}{s o m}{%
\IfBooleanTF{#1}{\SGAoriginalsection*{#3}\SGAcontentsentry{subsection}{#3}}{\IfNoValueTF{#2}{\SGAoriginalsection{#3}}{\SGAoriginalsection[#2]{#3}}}}
\RenewDocumentCommand{\subsection}{s o m}{%
\IfBooleanTF{#1}{\SGAoriginalsubsection*{#3}\SGAcontentsentry{subsubsection}{#3}}{\IfNoValueTF{#2}{\SGAoriginalsubsection{#3}}{\SGAoriginalsubsection[#2]{#3}}}}
'''

EXPOSE_TITLES_FR={'I':'Complexes dualisants','I appendice':'Appendice à Exposé I','III':'Formule de Lefschetz','III B':'Calculs de termes locaux','V':r'Systèmes projectifs $J$-adiques','VI':r'Coefficients $\ell$-adiques','VII':'Classes de Chern et classes de cycles','VIII':'Classes de cycles et théorème de Riemann--Roch','X':'Formule d’Euler--Poincaré','XII':'Formule de Lefschetz et invariants locaux','XV':'Morphismes de Frobenius et rationalité des fonctions L','Index terminologique':'Index terminologique','Index des notations':'Index des notations'}

def markerize(body,lang):
    seen=set()
    def sub(m):
        p=int(m[2]);text=f'\\SGAFolio{{{p}}}'
        if p==436 and p not in seen:text+=r'\SGAFolioGap'
        seen.add(p)
        return m[0].rstrip('\r\n')+'\n'+text+'%\n'
    body=re.sub(FOLIO.pattern+r'(?:\r?\n)?',sub,body)
    if lang=='FR':
        for m in list(re.finditer(r'\\(section|subsection)\*\{',body))[::-1]:
            j=m.end()-1;e=brace_end(body,j);label=body[j+1:e-1]
            repl=None
            if m[1]=='section' and (re.match(r'(?:EXPOSÉ|Exposé)\s+',label) or label in ['APPENDICE','Index terminologique','Index des notations']):repl=r'\SGAtopheading'
            elif m[1]=='subsection' and re.match(r'(?:§\s*)?\d+\.\s',label):repl=r'\SGAlevelheading'
            if repl:body=body[:m.start()]+repl+body[j:]
        # I and III use centered title blocks rather than section commands.
        for exp in ['I','III']:
            pat=r'\\begin\{center\}(\s*\{\\Large \\textbf\{Exposé '+exp+r'\}\})'
            body,n=re.subn(pat,lambda m:r'\phantomsection\addcontentsline{toc}{section}{Exposé '+exp+'}\n'+m[0],body)
            assert n==1,(exp,n)
    else:
        for m in list(re.finditer(r'\\(section|subsection)\*\{',body))[::-1]:
            j=m.end()-1;e=brace_end(body,j);label=body[j+1:e-1];repl=None
            if m[1]=='section' and re.match(r'(?:EXPOSÉ|Exposé)\s+',label):repl=r'\SGAprintedtopheading'
            elif m[1]=='section' and label in ['APPENDIX','Terminological Index','Index of Notation']:repl=r'\SGAtopheading'
            elif m[1]=='subsection' and re.match(r'(?:§\s*)?\d+\.\s',label):repl=r'\SGAlevelheading'
            if repl:body=body[:m.start()]+repl+body[j:]
    return body

def apparatus(lang,variants,notes,additional_notes=''):
    heading='Apparat des variantes' if lang=='FR' else 'Apparatus of variants'
    out=[r'\ifnum\SGAform=1\relax\clearpage\let\section\SGAoriginalsection\let\subsection\SGAoriginalsubsection',r'\section*{'+heading+r'}\addcontentsline{toc}{section}{'+heading+r'}\raggedright',('Les lectures sont des fragments exacts du code TeX; les formes choisies dans le texte sont déterminées par le même maître annoté.' if lang=='FR' else 'Readings are exact TeX source fragments. The same annotated master selects the readings printed in the text.'),'\n']
    last=None
    for n,v in enumerate(variants,1):
        if v['expose']!=last:
            out.append(r'\subsection*{'+tex_escape(v['expose'])+'}');last=v['expose']
        code_lines=sum(sum(max(1,(len(line)+94)//95) for line in str(v[key]).splitlines()) or 1 for key in ['before','after'])
        source_lines=max(1,(len(v['source'])+109)//110)
        reserve=min(40,8+code_lines+source_lines)
        out.append(r'\Needspace{'+str(reserve)+r'\baselineskip}')
        kind=v['kind']
        if lang=='FR':kind={'derived-functor typography':'typographie des foncteurs dérivés','typography / notation':'typographie / notation','punctuation':'ponctuation','formula / reference':'formule / référence','word / reference':'mot / référence'}.get(kind,kind)
        out.append(r'\par\medskip\noindent\hypertarget{app-'+v['id']+r'}{\textbf{\hyperlink{loc-'+v['id']+'}{['+str(n)+'] '+tex_escape(v['id'])+r'}}}\quad '+('p.~' if lang=='FR' else 'folio~')+str(v['page'])+r'\quad\textit{'+tex_escape(kind)+r'}\par')
        for label,key in [('Imprimé' if lang=='FR' else 'Printed','before'),('Corrigé' if lang=='FR' else 'Corrected','after')]:
            out.append(r'\noindent\textbf{'+label+':}')
            val=v[key].strip('\n')
            out.append('\\begin{SGARead}\n'+(val if val else '[empty]')+'\n\\end{SGARead}')
        out.append(r'\noindent{\footnotesize\textbf{Source:} '+tex_escape(v['source'])+r'}\par')
    if notes and Path(notes).exists():
        out.append(r'\clearpage\section*{'+('Lectures réservées et décisions' if lang=='FR' else 'Retained readings and decisions')+'}')
        out.append(Path(notes).read_text())
    if additional_notes:out.append(additional_notes)
    out.append(r'\fi')
    return '\n'.join(out)+'\n'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('lang',choices=['FR','EN']);ap.add_argument('--prepared',default='work/build/prepared');ap.add_argument('--contributions',default='work/contributions');ap.add_argument('--out',default='deliverables');args=ap.parse_args()
    lang=args.lang;prep=Path(args.prepared);con=Path(args.contributions);out=Path(args.out)/lang;out.mkdir(parents=True,exist_ok=True)
    pre=(prep/f'{lang}_preamble.tex').read_text().replace(r'\nofiles','')
    body=(prep/f'{lang}_annotated_body.tex').read_text()
    additional_notes=''
    if lang=='EN':
        relocation_path=con/'english/editorial_note_relocation.py'
        spec=importlib.util.spec_from_file_location('sga5_english_editorial_relocation',relocation_path)
        relocation=importlib.util.module_from_spec(spec);spec.loader.exec_module(relocation)
        body,additional_notes,extraction=relocation.relocate_en_note(body)
        write_json(prep/'EN_wrapper_editorial_extractions.json',[extraction])
        (prep/'EN_inherited_editorial_note.tex').write_text(additional_notes)
    variants=json.loads((prep/f'{lang}_variants.json').read_text())
    # The order in the apparatus is the order of calls in the master.
    ids=re.findall(r'\}\{((?:FR|EN)-\d{4}|R98-\d{2})\}',body)
    positions={v:body.find('}{'+v+'}') for v in [x['id'] for x in variants]}
    variants.sort(key=lambda v:positions[v['id']])
    assert all(positions[v['id']]>=0 for v in variants)
    numbers='\n'.join(r'\expandafter\def\csname SGAnum@'+v['id']+r'\endcsname{'+str(n)+'}' for n,v in enumerate(variants,1))+'\n'
    credits=(con/f'decisions/frontmatter_{lang}.tex').read_text()
    credits=re.sub(r'\\texttt\{([^{}]*[/][^{}]*)\}',lambda m:r'\nolinkurl{'+m[1].replace(r'\_','_')+'}',credits)
    support=SUPPORT
    if lang=='EN':support=support.replace(r'\hypertarget{print-#1}{}',r'\stepcounter{SGAfolioocc}\hypertarget{print-#1-\arabic{SGAfolioocc}}{}')
    full=pre+support+numbers+r'\begin{document}'+'\n'+r'\pagenumbering{roman}'+'\n'+title(lang)+credits+preface(lang)+r'\SGAcontentstrue\tableofcontents\SGAcontentsfalse\clearpage\pagenumbering{arabic}'+'\n'+TOC_HOOK+'\n% SGA5_BODY_START\n'+markerize(body,lang)+'\n% SGA5_BODY_END\n'+apparatus(lang,variants,con/f'decisions/unresolved_notes_{lang}.tex',additional_notes)+r'\end{document}'+'\n'
    full=redact(full)
    for form,name in enumerate(NAMES[lang]):
        s='% Generated from the single annotated master; 0=diplomatic, 1=corrected apparatus, 2=reading.\n'+r'\def\SGAform{'+str(form)+'}\n'+full
        (out/(name+'.tex')).write_text(s)
    master_name='SGA5_'+lang+'_master_annotated.tex'
    (out/master_name).write_text('% Annotated master. Change only SGAform: 0=diplomatic, 1=corrected apparatus, 2=reading.\n'+r'\providecommand{\SGAform}{1}'+'\n'+full)
    write_json(prep/f'{lang}_variants_ordered.json',variants)
    print(json.dumps({'language':lang,'reader_files':3,'master_files':1,'apparatus_entries':len(variants),'source_folio_calls':len(re.findall(r'\\SGAFolio\{\d+\}',markerize(body,lang)))}))

if __name__=='__main__':main()
