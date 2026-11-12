#!/usr/bin/env python3
"""Prepare lossless English components and source-grounded alignment candidates.

The mathematical alignment adapts port/segment.py from supplied ZIP 2. All
reported file names are archive-internal. No personal source paths are copied.
"""
import bisect
import collections
import difflib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources'
WORK = ROOT / 'work'
OUT = ROOT / 'output' / 'records'
MARK = re.compile(r'%%%%%%%%%%\s+scan idx (\d+)\s+\|\s+folio (\S+)\s+%%%%%%%%%%')
INPUT = re.compile(r'^\s*\\input\{([^}]+)\}', re.M)
MATH = re.compile(r'(?<!\\)\$\$(.+?)(?<!\\)\$\$|(?<!\\)\$([^$]{1,1200}?)(?<!\\)\$|(?<!\\)\\\[(.+?)\\\]|(?<!\\)\\\((.+?)\\\)|\\begin\{(equation|align|eqnarray|gather|multline|displaymath)(\*?)\}(.+?)\\end\{\5\6\}', re.S)
TOKEN = re.compile(r'\\[A-Za-z]+|\\.|[A-Za-zÀ-ÿ]+|\d+|[^\s]', re.S)
DROP = {'\\,','\\;','\\:','\\!','\\ ','\\quad','\\qquad','\\left','\\right','\\bigl','\\bigr','\\Bigl','\\Bigr','\\biggl','\\biggr','\\displaystyle','\\textstyle','\\mathrm','\\mathbf','\\mathbb','\\mathcal','\\mathscr','\\mathfrak','\\operatorname','\\text','\\mbox','\\hbox','{','}'}
SAME = {'\\varphi':'\\phi','\\epsilon':'\\varepsilon','\\leqslant':'\\le','\\leq':'\\le','\\geqslant':'\\ge','\\geq':'\\ge','\\longrightarrow':'\\to','\\rightarrow':'\\to'}


def lex(t):
    return [(m.start(), m.end(), SAME.get(m.group(), m.group())) for m in TOKEN.finditer(t) if m.group() not in DROP]


def norm(t):
    return tuple(x[2] for x in lex(t))


def math_tokens(t):
    result = []
    for m in MATH.finditer(t):
        body = next(g for g in (m.group(1),m.group(2),m.group(3),m.group(4),m.group(7)) if g is not None)
        n = norm(re.sub(r'\\(?:SGARefTarget|SGARefLink|label)\{[^}]*\}', '', body))
        if len(n) > 1:
            result.append((m.start(), n))
    return result


def expose(name):
    if 'general_introduction' in name:
        return 'Introduction'
    if 'terminal_publisher' in name:
        return 'Catalogue'
    m = re.search(r'expose_([IVX]+)(?:_|\.)',name)
    return m.group(1) if m else 'Front'


def french_pages(vol,layer):
    result = {}
    for p in (SRC/'fr'/('sga7i' if vol=='7I' else 'sga7ii')/layer).glob('*_body.tex'):
        t=p.read_text(); matches=list(MARK.finditer(t))
        for i,m in enumerate(matches):
            result[(p.name,m.group(2))]=t[m.end():matches[i+1].start() if i+1<len(matches) else len(t)]
    return result


def english_root(vol):
    p=SRC/'en/sources/native'/('SGA7I' if vol=='7I' else 'SGA7II')
    return p/'SGA7I_English_current_buildable_source_20260823' if vol=='7I' else p


def load_components(vol):
    d=english_root(vol)
    master=d/('SGA7_I_English_source_first_workpass.tex' if vol=='7I' else 'SGA7_II_English_source_first_workpass.tex')
    result=[]
    for name in INPUT.findall(master.read_text()):
        p=d/(name if name.endswith('.tex') else name+'.tex')
        result.append({'volume':vol,'file':str(p.relative_to(SRC)),'component':str(p.relative_to(d)),
                       'expose':expose(p.name),'text':p.read_text()})
    if vol=='7I':
        p=d/'components/187_expose_IX_terminal_publisher_matter.tex'
        result.append({'volume':vol,'file':str(p.relative_to(SRC)),'component':str(p.relative_to(d)),
                       'expose':'Catalogue','text':p.read_text()})
    return result


def load_port(vol):
    decisions={}
    for p in sorted((SRC/'port/decisions').glob('decisions_en'+vol+'_*')):
        for r in json.loads(p.read_text()):
            decisions[r['id']]={**r,'source':'port/decisions/'+p.name}
    logs=[json.loads(x) for x in (SRC/'port'/('PORT_EN'+vol+'_LOG.jsonl')).read_text().splitlines() if x.strip()]
    for r in logs:
        if r.get('outcome')=='applied':
            decisions[r['id']]={**decisions.get(r['id'],{}),**r,'source':'port/PORT_EN'+vol+'_LOG.jsonl#'+r['id']}
    return decisions,logs


def align(vol,components):
    result=[]
    frdir=SRC/'fr'/('sga7i' if vol=='7I' else 'sga7ii')/'current'
    byexp=collections.defaultdict(list)
    for c in components:
        byexp[c['expose']].append(c)
    for exp,group in byexp.items():
        fp=frdir/('general_introduction_body.tex' if exp=='Introduction' else 'expose_'+exp+'_body.tex')
        if exp=='Catalogue':
            fp=frdir/'expose_IX_body.tex'
        if not fp.exists():continue
        ft=fp.read_text()
        fm=list(MARK.finditer(ft))
        if not fm:continue
        if exp=='Catalogue':
            fm=[m for m in fm if m.group(2).isdigit() and int(m.group(2))>=525]
        et=''; starts=[]
        for c in group:
            starts.append(len(et)); et+=c['text']+'\n\n'
        ftok,etok=math_tokens(ft),math_tokens(et)
        sm=difflib.SequenceMatcher(None,[x[1] for x in ftok],[x[1] for x in etok],autojunk=False)
        anchors=[(ftok[a+k][0],etok[b+k][0]) for a,b,n in sm.get_matching_blocks() for k in range(n)]
        epos=[e for f,e in anchors]
        frpos=[m.start() for m in fm]
        for c,start in zip(group,starts):
            paragraphs=[0]+[m.end() for m in re.finditer(r'\n\s*\n',c['text'])]
            for i,off in enumerate(paragraphs):
                x=start+off
                j=bisect.bisect_left(epos,x)
                if not anchors: f=frpos[0]; quality='expose-start'
                elif j==0: f=anchors[0][0]; quality='following-math-anchor'
                elif j>=len(anchors):f=anchors[-1][0]; quality='preceding-math-anchor'
                else:
                    f0,e0=anchors[j-1];f1,e1=anchors[j]
                    f=f0+(f1-f0)*(x-e0)//max(1,e1-e0);quality='interpolated-math-anchors'
                k=max(0,bisect.bisect_right(frpos,f)-1)
                folio=fm[k].group(2)
                end=paragraphs[i+1] if i+1<len(paragraphs) else len(c['text'])
                result.append({'volume':vol,'expose':exp,'component':c['component'],'offset':off,'end':end,
                               'folio':folio,'quality':quality,'text':c['text'][off:end]})
    return result


def main():
    WORK.mkdir(exist_ok=True); OUT.mkdir(parents=True,exist_ok=True)
    candidates=[];allalign=[];allcomponents=[]
    for vol in ['7I','7II']:
        components=load_components(vol);allcomponents+=components
        allalign+=align(vol,components)
        current=[json.loads(x) for x in (SRC/'fixes'/('FIXLOG_'+vol+'_CURRENT.jsonl')).read_text().splitlines()]
        dip=[json.loads(x) for x in (SRC/'fixes'/('FIXLOG_'+vol+'.jsonl')).read_text().splitlines()]
        ds={(x['file'],x['page'],x['old'],x['new']) for x in dip}
        port,logs=load_port(vol)
        dp,cp=french_pages(vol,'diplomatic'),french_pages(vol,'current')
        for i,f in enumerate(current):
            if (f['file'],f['page'],f['old'],f['new']) in ds:continue
            p=port.get('C'+str(i),{})
            dt=dp.get((f['file'],str(f['page'])),'');ct=cp.get((f['file'],str(f['page'])),'')
            candidates.append({'volume':vol,'id':'C'+str(i),'fr_fix':f,'port':p,
                               'fr_old_in_diplomatic':f['old'] in dt,'fr_new_in_current':f['new'] in ct,
                               'fr_page_differs':dt!=ct})
    (WORK/'en_components.json').write_text(json.dumps(allcomponents,ensure_ascii=False,indent=1))
    (WORK/'en_alignment.json').write_text(json.dumps(allalign,ensure_ascii=False,indent=1))
    (WORK/'en_candidates.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=1))
    print(json.dumps({'components':len(allcomponents),'alignment_paragraphs':len(allalign),'candidate_fixes':len(candidates)},indent=2))


if __name__=='__main__':main()
