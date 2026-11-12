"""Exact-text helpers for the English SGA 4 reader build.

No source content is fetched; all inputs are the attached archives.
"""
from pathlib import Path
import bisect, csv, difflib, json, re

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'sources'
RECORDS = ROOT / 'output/records'
ENROOT = SOURCES / 'en/A_sga-en_4a4cbac_sources_native_SGA4/SGA4_English_current_buildable_source_20260906/source'
FRROOT = SOURCES / 'fr/A_orgogozo_snapshot_71766d9'
RELEASE = SOURCES / 'en/C_release_20261112/04_SGA4_EN_COMPLETE_READER.tex'
DIRS = ['01','02','03','04','05','05bis']+[f'{i:02d}' for i in range(6,20)]
PAGES = json.loads((SOURCES/'api_pass_20261111/PAGES.json').read_text())
EXPOSE = {p['file']:p['expose'] for p in PAGES}
TOME = {p['file']:p['tome'] for p in PAGES}
MARK = re.compile(r'\\pageoriginale(?![A-Za-z])')
FRAG = re.compile(r'LINES_(\d+)_(\d+)')

def code(line):
    m=re.search(r'(?<!\\)%',line)
    return line if m is None else line[:m.start()]

def uncomment(s):
    return '\n'.join(code(l) for l in s.split('\n'))

def active_matches(pattern,s):
    for m in re.finditer(pattern,s):
        if '%' not in code(s[s.rfind('\n',0,m.start())+1:m.start()]):
            ls=s.rfind('\n',0,m.start())+1
            if len(code(s[ls:m.start()]))==m.start()-ls:
                yield m

def marks(s):
    return list(active_matches(MARK,s))

def group(s,pos):
    """Read one TeX argument (braced or a single token), preserving bytes."""
    while pos<len(s):
        if s[pos].isspace():pos+=1;continue
        if s[pos]=='%':
            end=s.find('\n',pos)
            pos=len(s) if end<0 else end+1
            continue
        break
    if pos>=len(s):raise ValueError('Missing TeX argument')
    start=pos
    if s[pos]!='{':
        m=re.match(r'\\(?:[A-Za-z@]+|.)|.',s[pos:],re.S)
        end=pos+len(m.group());return s[pos:end],start,end,False
    dep=1;pos+=1;content=pos
    while pos<len(s):
        c=s[pos]
        if c=='\\':
            if pos+1<len(s) and not s[pos+1].isalpha():pos+=2;continue
        if c=='%':
            pos=s.find('\n',pos)
            if pos<0:break
            continue
        if c=='{':dep+=1
        elif c=='}':
            dep-=1
            if dep==0:return s[content:pos],start,pos+1,True
        pos+=1
    raise ValueError('Unbalanced TeX argument near '+s[start:start+80])

def norm(s):
    return re.sub(r'\s+','',uncomment(s))

def tex_escape(s):
    chars={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','$':r'\$','&':r'\&','#':r'\#','%':r'\%','_':r'\_','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(chars.get(c,c) for c in s)

def sanitize(s):
    s=re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}','[email omitted]',s)
    s=re.sub(r'[A-Z]:[\\/](?:Users|users)[\\/][^\n\r]*','[local path omitted]',s)
    s=re.sub(r'/(?:home|Users|workspace|root)/[^\s{}]*','[local path omitted]',s)
    return s

def write_tsv(path,rows,fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore');w.writeheader()
        for row in rows:w.writerow({k:sanitize(str(row.get(k,''))).replace('\r','') for k in fields})

def fragment_blocks(s):
    pattern=re.compile(r'% BEGIN INCLUDED ([^\n]*?/([^/\n]+)/drafts/([^/\n]+\.texfrag))\n')
    out=[]
    for m in pattern.finditer(s):
        end=s.index('% END INCLUDED '+m.group(1),m.end())
        # release assembler adds a \relax\space before the end sentinel.
        ce=end
        if s[max(m.end(),end-12):end].endswith(r'\relax\space'):
            ce=end-len(r'\relax\space')
        a,b=map(int,FRAG.search(m.group(3)).groups())
        out.append({'path':m.group(1),'file':m.group(2),'name':m.group(3),'a':a,'b':b,'start':m.end(),'end':ce,'text':s[m.end():ce]})
    return out

def french_marker_map(d):
    text=(FRROOT/d/(d+'.tex')).read_text()
    sm=marks(text)
    pp=sorted([p for p in PAGES if p['file']==d],key=lambda p:p['marker_line'])
    # One index row is a marker within a commented section. It stays a record,
    # and is restored separately rather than offsetting subsequent live pages.
    pr=(SOURCES/'fr/B_corpus_diplomatic_before_scan_check'/d/(d+'.tex')).read_text().splitlines()
    active=[p for p in pp if MARK.search(code(pr[p['marker_line']-1]))]
    assert len(sm)==len(active),(d,len(sm),len(active))
    return text,[(m.start(),text.count('\n',0,m.start())+1,p) for m,p in zip(sm,active)]

def page_data(s):
    """Exact fragment/page alignment; mismatches remain explicit."""
    out=[]
    fm={d:french_marker_map(d) for d in DIRS}
    for f in fragment_blocks(s):
        _,mm=fm[f['file']]
        f['fmarkers']=[(o,ln,p) for o,ln,p in mm if f['a']<=ln<=f['b']]
        f['emarkers']=marks(f['text'])
        f['aligned']=len(f['fmarkers'])==len(f['emarkers'])
        f['folios']=[p['folio'] for _,_,p in f['fmarkers']]
        out.append(f)
    return out

def replace_spans(s,edits):
    edits=sorted(edits,key=lambda e:(e[0],e[1]))
    prev=-1
    for a,b,t in edits:
        assert a>=prev,(a,prev)
        assert b>=a
        prev=b
    for a,b,t in reversed(edits):s=s[:a]+t+s[b:]
    return s
