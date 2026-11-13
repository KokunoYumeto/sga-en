"""Reproducible SGA 5 edition helpers. All reported paths are archive-relative."""
from __future__ import annotations
import bisect, csv, difflib, hashlib, json, re
from pathlib import Path

FOLIO = re.compile(r'%{5,}[ \t]*scan idx[ \t]+(\d+)[ \t]*\|[ \t]*folio[ \t]+(\d+)[ \t]*%+[ \t]*')
EXPOSES = [(1,'I'),(55,'I appendice'),(73,'III'),(138,'III B'),(204,'V'),(251,'VI'),(282,'VII'),(351,'VIII'),(372,'X'),(407,'XII'),(442,'XV'),(481,'Index terminologique'),(483,'Index des notations')]

def expose_for(page):
    return next((v for p,v in reversed(EXPOSES) if page>=p),'Front matter')

def write_json(path, data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def write_tsv(path, rows, fields):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore',lineterminator='\n')
        w.writeheader();w.writerows(rows)

def digest(s):
    return hashlib.sha256(s.encode() if isinstance(s,str) else s).hexdigest()

def split_document(s):
    pre,body=s.split(r'\begin{document}',1)
    body,tail=body.rsplit(r'\end{document}',1)
    return pre,body

def split_folios(s):
    ms=list(FOLIO.finditer(s));out={}
    for i,m in enumerate(ms):
        out[int(m[2])]=s[m.end():ms[i+1].start() if i+1<len(ms) else len(s)]
    return out

def strip_comments(s):
    # TeX discards an unescaped percent and the rest of its input line,
    # including that endline. Retain folio comments as data until insertion.
    out=[]
    for line in s.splitlines(keepends=True):
        if FOLIO.fullmatch(line.rstrip('\n')):
            out.append(line);continue
        i=0
        while i<len(line):
            if line[i]=='\\':i+=2;continue
            if line[i]=='%':line=line[:i];break
            i+=1
        out.append(line)
    return ''.join(out)

def terminate_folio_comments(s):
    """Keep each retained folio comment on a complete physical input line.

    Variant boundaries can move an original endline into an argument.  A fresh
    endline after a retained percent comment protects the following command
    from that comment.  Every inserted character is recorded explicitly.
    """
    edits=[]
    for m in FOLIO.finditer(s):
        if m.end()<len(s) and s[m.end()] not in '\r\n':
            edits.append({'folio':int(m[2]),'position':m.end(),'before':'','after':'\n',
                          'following_context':s[m.end():m.end()+120],
                          'reason':'Terminate the retained percent-comment line before the annotated command; the endline after the percent comment contributes no TeX token.'})
    for e in reversed(edits):s=s[:e['position']]+'\n'+s[e['position']:]
    return s,edits

def tex_escape(s):
    return ''.join({'\\':r'\textbackslash{}','{':r'\{','}':r'\}','$':r'\$','&':r'\&','#':r'\#','_':r'\_','%':r'\%','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in str(s))

def redact(s):
    # Original records can contain machine-specific paths and addresses.
    s=re.sub(r'[A-Za-z]:\\(?:Users|Documents|Temp|Windows|workspace|home)\\[^\s"\n<>]+','[local source path omitted]',s)
    s=re.sub(r'(?<![A-Za-z0-9])/(?:home|Users|workspace|root|tmp|mnt|var|opt)/[^\s"\n<>]+','[local source path omitted]',s)
    s=re.sub(r'[A-Za-z0-9.!#$%&\'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+','[email omitted]',s)
    return s

def load_jsonl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]

def brace_end(s,i,opening='{',closing='}'):
    assert s[i]==opening,(s[i:i+20],opening)
    depth=1;j=i+1
    while j<len(s):
        if s[j]=='\\':
            m=re.match(r'\\(?:[A-Za-z@]+|.)',s[j:],re.S)
            j+=len(m[0]) if m else 1;continue
        if s[j]==opening:depth+=1
        elif s[j]==closing:
            depth-=1
            if depth==0:return j+1
        j+=1
    raise ValueError('Unbalanced group: '+repr(s[i:i+120]))

def following_scripts(s,i):
    """Return a complete immediate superscript/subscript suffix.

    Editorial calls follow this suffix so the original scripts remain attached
    to the original mathematical nucleus, not to the callout box.
    """
    start=i
    while i<len(s):
        j=i
        while j<len(s) and s[j] in ' \t\n':j+=1
        if j>=len(s) or s[j] not in "^_'":break
        if s[j]=="'":i=j+1;continue
        j+=1
        while j<len(s) and s[j].isspace():j+=1
        if j<len(s) and s[j]=='{':i=brace_end(s,j)
        elif j<len(s) and s[j]=='\\':
            m=re.match(r'\\(?:[A-Za-z@]+|.)',s[j:],re.S);i=j+len(m[0])
        else:i=j+1
    return s[start:i]

def atoms(s):
    """Tokenize with balanced groups and complete macro argument sequences.

    This tokenizer preserves every input character; it is an annotation boundary
    parser, not a mathematical rewriting system.
    """
    out=[];i=0
    while i<len(s):
        start=i;c=s[i]
        if c=='\\':
            m=re.match(r'\\(?:[A-Za-z@]+\*?|.)',s[i:],re.S);i+=len(m[0]) if m else 1
            cmd=s[start:i]
            consumed_args=0
            two_arg_commands={r'\frac',r'\dfrac',r'\tfrac',r'\binom',r'\dbinom',r'\tbinom',r'\overset',r'\underset',r'\stackrel'}
            if cmd in two_arg_commands:
                for _ in range(2):
                    while i<len(s) and s[i].isspace():i+=1
                    if i>=len(s):break
                    if s[i]=='{':i=brace_end(s,i)
                    elif s[i]=='\\':
                        q=re.match(r'\\(?:[A-Za-z@]+|.)',s[i:],re.S);i+=len(q[0])
                    else:i+=1
                consumed_args=2
            simple_arg_commands={r'\underline',r'\overline',r'\hat',r'\widehat',r'\tilde',r'\widetilde',r'\bar',r'\vec',r'\dot',r'\ddot',r'\breve',r'\check',r'\acute',r'\grave',r'\ol',r'\wt',r'\wh',r'\not',r'\sqrt',r'\mathrm',r'\mathbf',r'\mathbb',r'\mathcal',r'\mathfrak',r'\mathscr'}
            if cmd in simple_arg_commands:
                j=i
                while j<len(s) and s[j].isspace():j+=1
                if j<len(s) and s[j]!='{':
                    if s[j]=='\\':
                        q=re.match(r'\\(?:[A-Za-z@]+|.)',s[j:],re.S);i=j+len(q[0])
                    else:i=j+1
                    consumed_args=1
            one_arg_commands=simple_arg_commands|{r'\begin',r'\end',r'\tag',r'\tag*',r'\label',r'\ref',r'\eqref',r'\text',r'\textbf',r'\textit',r'\textrm',r'\textsf',r'\texttt',r'\emph',r'\footnote',r'\section',r'\section*',r'\subsection',r'\subsection*',r'\subsubsection',r'\subsubsection*',r'\operatorname',r'\operatorname*',r'\SGAFixedVariant'}
            zero_arg_commands={r'\small',r'\footnotesize',r'\scriptsize',r'\tiny',r'\large',r'\Large',r'\LARGE',r'\huge',r'\Huge',r'\centering',r'\noindent',r'\par',r'\medskip',r'\bigskip',r'\quad',r'\qquad',r'\displaystyle',r'\textstyle',r'\scriptstyle',r'\scriptscriptstyle'}
            arg_limit=2 if cmd in two_arg_commands else 1 if cmd in one_arg_commands else 0 if cmd in zero_arg_commands else None
            if cmd in (r'\left',r'\right',r'\big',r'\Big',r'\bigg',r'\Bigg',r'\bigl',r'\bigr',r'\Bigl',r'\Bigr'):
                while i<len(s) and s[i].isspace():i+=1
                if i<len(s):
                    if s[i]=='\\':
                        q=re.match(r'\\(?:[A-Za-z@]+|.)',s[i:],re.S);i+=len(q[0])
                    else:i+=1
            while True:
                j=i
                while j<len(s) and s[j].isspace():j+=1
                if j<len(s) and s[j]=='{':
                    if arg_limit is not None and consumed_args>=arg_limit:break
                    i=brace_end(s,j);consumed_args+=1;continue
                if j<len(s) and s[j]=='[' and cmd not in (r'\[',r'\]',r'\\'):
                    try:i=brace_end(s,j,'[',']');continue
                    except ValueError:pass
                break
        elif c=='{':i=brace_end(s,i)
        elif c.isspace():
            i+=1
            while i<len(s) and s[i].isspace():i+=1
        elif c.isalpha() or c.isdigit():
            i+=1
            while i<len(s) and (s[i].isalpha() or s[i].isdigit()):i+=1
        else:i+=1
        # Unbraced scripts consume exactly one token. Keep them with their base.
        while i<len(s) and s[i] in "^_'":
            if s[i]=="'":
                i+=1;continue
            i+=1
            if i>=len(s):break
            if s[i]=='{':i=brace_end(s,i)
            elif s[i]=='\\':
                q=re.match(r'\\(?:[A-Za-z@]+|.)',s[i:],re.S);i+=len(q[0])
            else:i+=1
        out.append(s[start:i])
    assert ''.join(out)==s
    return out

def comparable(s):
    # Exact TeX macro-argument equivalences: a single character argument and
    # that character enclosed in braces are consumed identically by these
    # one-argument font macros. Whitespace is left untouched here.
    s=re.sub(r'\\(mathrm|mathbb|mathcal|mathbf|mathfrak|mathscr)\s+([A-Za-z0-9])',r'\\\1{\2}',s)
    s=re.sub(r'\\operatorname\{(Hom|Ext|Tor|Spec|Ker|Coker|Tr|Supp|Gal|Ob|ob)\}',lambda m:'\\'+m[1],s)
    return s

def classify(before,after,sources):
    if 'R98-' in sources:return 'derived-functor typography'
    if ('\\mathbb{R}' in before or '\\underline{\\underline{\\mathrm{R}}}' in before) and '\\mathrm{R}' in after:return 'derived-functor typography'
    if any(k in before+after for k in ('\\underline','\\emph','\\mathcal','\\mathrm','\\mathbf')):return 'typography / notation'
    b=re.sub(r'[^A-Za-zÀ-ÿ0-9\\]','',before);a=re.sub(r'[^A-Za-zÀ-ÿ0-9\\]','',after)
    if a==b:return 'punctuation'
    if '\\' in before+after or '$' in before+after or any(c in before+after for c in '_^'):return 'formula / reference'
    return 'word / reference'

class RecordIndex:
    def __init__(self,fr):
        self.by_page={};self.rows=[]
        specs=[('FIXLOG_5','fixes/FIXLOG_5.jsonl'),('FIXLOG_5_CURRENT','fixes/FIXLOG_5_CURRENT.jsonl'),('HANDFIX_5','fixes/HANDFIX_5.jsonl'),('MISPRINTS_5','fixes/MISPRINTS_5.json')]
        for label,fn in specs:
            data=load_jsonl(fr/fn) if fn.endswith('jsonl') else json.loads((fr/fn).read_text())
            for n,r in enumerate(data,1):
                rec={'id':f'{label}:{n:04d}','path':fn,'row':n,'data':r};self.rows.append(rec)
                page=r.get('page')
                if isinstance(page,(int,str)) and str(page).isdigit():self.by_page.setdefault(int(page),[]).append(rec)
    def sources(self,page,before,after):
        hits=[];b=comparable(re.sub(r'\s+',' ',before)).strip();a=comparable(re.sub(r'\s+',' ',after)).strip()
        for r in self.by_page.get(page,[]):
            d=r['data'];old=comparable(re.sub(r'\s+',' ',str(d.get('old',d.get('print','')))));new=comparable(re.sub(r'\s+',' ',str(d.get('new',d.get('correct','')))))
            score=0
            if b and len(b)>1 and b in old:score+=3
            if a and len(a)>1 and a in new:score+=3
            if len(old)>5 and old in b:score+=2
            if len(new)>5 and new in a:score+=2
            if score>=5:hits.append((score,r['id']))
        hits.sort(reverse=True)
        return '; '.join(v for sc,v in hits[:5])

def public_record(r):
    return json.loads(redact(json.dumps(r,ensure_ascii=False)))
