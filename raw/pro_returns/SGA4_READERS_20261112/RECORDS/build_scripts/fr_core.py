"""Structural helpers for the French reader build; no mathematical rewriting."""
from pathlib import Path
import re, json, csv, bisect, difflib

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'sources'
OUT=ROOT/'output'
FILES=['01','02','03','04','05','05bis','06','07','08','09','10','11','12','13','14','15','16','17','18','19']
EXPOSES=['I','II','III','IV','V','Vbis','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX']
EXP=dict(zip(FILES,EXPOSES)); INV={v:k for k,v in EXP.items()}
PAGES=json.loads((SRC/'api_pass_20261111/PAGES.json').read_text())
PAGEBY={f:[x for x in PAGES if x['file']==f] for f in FILES}

def strip_comments(text):
    out=[];i=0
    while i<len(text):
        if text[i]=='\\' and i+1<len(text):out.append(text[i:i+2]);i+=2;continue
        if text[i]=='%':
            j=text.find('\n',i);n=len(text) if j<0 else j+1
            if n<len(text) and re.match(r'[A-Za-z]',text[n]) and re.search(r'\\[A-Za-z]+$',''.join(out[-80:])):out.append(' ')
            i=n;continue
        out.append(text[i]);i+=1
    return ''.join(out)

def strip_comments_map(text):
    out=[];positions=[];i=0
    while i<len(text):
        if text[i]=='\\' and i+1<len(text):out.extend(text[i:i+2]);positions.extend([i,i+1]);i+=2;continue
        if text[i]=='%':
            j=text.find('\n',i);n=len(text) if j<0 else j+1
            if n<len(text) and re.match(r'[A-Za-z]',text[n]) and re.search(r'\\[A-Za-z]+$',''.join(out[-80:])):out.append(' ');positions.append(i)
            i=n;continue
        out.append(text[i]);positions.append(i);i+=1
    positions.append(len(text))
    return ''.join(out),positions

def group(text,pos):
    while pos<len(text):
        if text[pos].isspace():pos+=1;continue
        if text[pos]=='%':
            n=text.find('\n',pos);pos=len(text) if n<0 else n+1;continue
        break
    if pos>=len(text) or text[pos]!='{':raise ValueError(('expected group',text[pos:pos+60]))
    start=pos+1;depth=1;pos+=1
    while pos<len(text):
        if text[pos]=='\\':pos+=2;continue
        if text[pos]=='%':
            n=text.find('\n',pos);pos=len(text) if n<0 else n+1;continue
        if text[pos]=='{':depth+=1
        if text[pos]=='}':
            depth-=1
            if depth==0:return text[start:pos],pos+1
        pos+=1
    raise ValueError('unclosed TeX group')

def replace_sisi(text,which,records=None,file=''):
    out=[];pos=0;n=0
    pattern=re.compile(r'\\sisi\s*\{|\\(?:nde|ndetext)\s*\{|(?<!\\)%[^\n]*')
    for m in pattern.finditer(text):
        if m.start()<pos:continue
        if m.group().startswith('%'):continue
        if m.group().startswith(('\\nde{','\\nde ','\\ndetext')):
            _,end=group(text,text.find('{',m.start()));out.append(text[pos:end]);pos=end;continue
        a,end1=group(text,text.find('{',m.start()))
        try:b,end2=group(text,end1)
        except ValueError:
            at=end1
            while at<len(text) and text[at].isspace():at+=1
            if at>=len(text):raise
            token=re.match(r'\\[A-Za-z]+|\\.|.',text[at:])
            if not token:raise
            b=token.group();end2=at+len(b)
        prefix=text[pos:m.start()]
        selected=replace_sisi(a if which==0 else b,which)
        # A single end-line inside an argument is a space token in TeX. When
        # inlining that argument, do not merge it with the caller's end-line
        # into a new paragraph token (which would break displayed mathematics).
        selected=re.sub(r'^[ \t]*\n(?![ \t]*\n)[ \t]*',' ',selected)
        selected=re.sub(r'[ \t]*(?<!\n)\n[ \t]*$',' ',selected)
        if selected and re.search(r'\\[A-Za-z]+$',prefix) and re.match(r'[A-Za-z]',selected):prefix+=' '
        if re.search(r'\\[A-Za-z]+$',selected) and end2<len(text) and re.match(r'[A-Za-z]',text[end2]):selected+=' '
        out.append(prefix);out.append(selected)
        n+=1
        if records is not None:
            page=page_at(text,m.start(),file)
            records.append({'id':f'ORG-{file}-{n:04d}','file':file,'expose':EXP.get(file,file),'page':page,'printed':a,'corrected':b,'source':'Fabrice Orgogozo, LaTeX edition 71766d9; sisi record'})
        pos=end2
    out.append(text[pos:]);return ''.join(out)

def body(text):
    a=re.search(r'\\else\s*\n\\chapter',text)
    if not a:raise ValueError('no book branch')
    start=a.start()+len('\\else')
    b=text.index('\\fi',start)
    text=text[start:b]+text[b+3:]
    tail=text.rfind('\\ifx\\danslelivre\\undefined')
    if tail>=0:text=text[:tail]
    return text

def explicit_pages(text,file):
    pages=PAGEBY[file];n=0
    def sub(m):
        nonlocal n
        if n>=len(pages):raise ValueError((file,'too many page markers'))
        p=pages[n];n+=1
        return '\\SGApageno{%s}{%s}'%(p['tome'],p['folio'])
    result=re.sub(r'\\pageoriginale\b',sub,text)
    assert n==len(pages),(file,n,len(pages))
    return result

def page_at(text,pos,file=None):
    markers=list(re.finditer(r'\\SGApageno\{(\d)\}\{(\d+)\}',text[:pos]))
    if markers:return int(markers[-1].group(2))
    return PAGEBY[file][0]['folio'] if file else None

def page_span(text,page):
    ms=list(re.finditer(r'\\SGApageno\{\d\}\{(\d+)\}',text))
    for i,m in enumerate(ms):
        if int(m.group(1))==int(page):
            # A marker is placed after the first word/heading of its printed page.
            return (max(0,m.start()-160),ms[i+1].start()+160 if i+1<len(ms) else len(text))
    return (0,len(text))

def searchable(text):
    """Return a whitespace/comment-free search key and the exact source offsets."""
    mask=[True]*len(text)
    for m in re.finditer(r'(?<!\\)%[^\n]*|\\SGApageno\{\d\}\{\d+\}|\\pageoriginale\b',text):
        mask[m.start():m.end()]=[False]*(m.end()-m.start())
    chars=[];positions=[]
    for i,c in enumerate(text):
        if mask[i] and not c.isspace():chars.append(c);positions.append(i)
    return ''.join(chars),positions

def find_exact(text,needle,page=None):
    if not needle or len(needle.strip())<2:return []
    lo,hi=page_span(text,page) if page is not None else (0,len(text))
    hay,offsets=searchable(text[lo:hi]);key,_=searchable(needle)
    if not key:return []
    protected=[]
    for mm in re.finditer(r'\\(?:nde|ndetext)\s*\{',text[lo:hi]):
        aa=lo+mm.start()
        if re.search(r'(?<!\\)%',text[text.rfind('\n',0,aa)+1:aa]):continue
        _,ee=group(text,text.find('{',aa));protected.append((aa,ee))
    out=[];start=0
    while True:
        at=hay.find(key,start)
        if at<0:break
        hit=(lo+offsets[at],lo+offsets[at+len(key)-1]+1)
        before=text[hit[0]-1:hit[0]] if hit[0] else ''
        after=text[hit[1]:hit[1]+1]
        leftbad=bool(re.match(r'[A-Za-zÀ-ÿ0-9]',key[0])) and bool(re.match(r'[A-Za-zÀ-ÿ0-9\\]',before))
        rightbad=bool(re.match(r'[A-Za-zÀ-ÿ0-9]',key[-1])) and bool(re.match(r"[A-Za-zÀ-ÿ0-9'_]",after))
        if not leftbad and not rightbad and not any(a<=hit[0]<b or a<hit[1]<=b for a,b in protected):out.append(hit)
        start=at+max(1,len(key))
    return out

class ExactIndex:
    """Index one immutable TeX text for repeated exact provenance searches.

    The key removes only comments, whitespace and explicit page markers, just
    like find_exact. Shape commands, braces and every mathematical token remain.
    """
    def __init__(self,text):
        import bisect
        self.text=text;self.key,self.offsets=searchable(text);self.bisect=bisect.bisect_left
        self.pages={};self.protected=[]
        marks=list(re.finditer(r'\\SGApageno\{\d\}\{(\d+)\}',text))
        for n,m in enumerate(marks):self.pages[int(m.group(1))]=(max(0,m.start()-160),marks[n+1].start()+160 if n+1<len(marks) else len(text))
        for m in re.finditer(r'\\(?:nde|ndetext)\s*\{',text):
            if re.search(r'(?<!\\)%',text[text.rfind('\n',0,m.start())+1:m.start()]):continue
            _,end=group(text,text.find('{',m.start()));self.protected.append((m.start(),end))
    def find(self,needle,page=None):
        if not needle or len(needle.strip())<2:return []
        key,_=searchable(needle)
        if not key:return []
        lo,hi=self.pages.get(int(page),(0,len(self.text))) if page is not None else (0,len(self.text))
        start=self.bisect(self.offsets,lo);limit=self.bisect(self.offsets,hi);out=[]
        while True:
            at=self.key.find(key,start,limit)
            if at<0:break
            a=self.offsets[at];b=self.offsets[at+len(key)-1]+1
            before=self.text[a-1:a] if a else '';after=self.text[b:b+1]
            leftbad=bool(re.match(r'[A-Za-zÀ-ÿ0-9]',key[0])) and bool(re.match(r'[A-Za-zÀ-ÿ0-9\\]',before))
            rightbad=bool(re.match(r'[A-Za-zÀ-ÿ0-9]',key[-1])) and bool(re.match(r"[A-Za-zÀ-ÿ0-9'_]",after))
            if not leftbad and not rightbad and not any(x<=a<y or x<b<=y for x,y in self.protected):out.append((a,b))
            start=at+max(1,len(key))
        return out

def replace_one(text,old,new,page,global_fallback=False):
    hits=find_exact(text,old,page)
    if not hits and global_fallback:hits=find_exact(text,old,None)
    if len(hits)!=1:return text,None
    a,b=hits[0]
    # Preserve all page markers embedded inside a matching phrase.
    if re.search(r'\\SGApageno',text[a:b]) and not re.search(r'\\SGApageno',new):
        from marker_projection import carry_markers
        new=carry_markers(text[a:b],new)
    return text[:a]+new+text[b:],(a,b,text[a:b],new)

def escaped(text):
    table={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','$':r'\$','&':r'\&','#':r'\#','%':r'\%','_':r'\_','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}
    return ''.join(table.get(c,c) for c in str(text)).replace('\n',' ')

def sanitize(text):
    text=re.sub(r'\b[A-Za-z]:[\\/](?:Users|home|Documents|Temp)[\\/](?:[^\s\n<>"\']+)', '[local source path omitted]',text)
    text=re.sub(r'(?<!\w)/(?:Users|home|workspace|root)/[^\s\n<>"\']+', '[local source path omitted]',text)
    text=re.sub(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}', '[email omitted]',text)
    return text

def tsv(path,rows,cols):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=cols,delimiter='\t',extrasaction='ignore');w.writeheader()
        for r in rows:w.writerow({k:sanitize(str(r.get(k,''))) for k in cols})

def writejson(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    def clean(x):
        if isinstance(x,str):return sanitize(x)
        if isinstance(x,list):return [clean(v) for v in x]
        if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
        return x
    path.write_text(json.dumps(clean(obj),ensure_ascii=False,indent=2)+'\n')

def visible_projection(text):
    """Expand only macros whose visible replacement is explicit in the source.

    This projection does not identify mathematical expressions. Hyperlink targets,
    anchors and label metadata disappear; their displayed arguments remain byte
    for byte. Unknown commands remain present and prevent an equality claim.
    """
    out=[];pos=0
    pattern=re.compile(r'\\(etiquette|label|hyperrefext|eqhyperrefext|neweqhyperrefext|hyperref|eqhyperref|pagehyperref|phantomsection|quoi)\b')
    for m in pattern.finditer(text):
        if m.start()<pos:continue
        name=m.group(1);end=m.end();args=[]
        if name in ('phantomsection','quoi'):value=''
        else:
            try:
                while end<len(text) and text[end].isspace():end+=1
                while end<len(text) and text[end]=='[':
                    close=text.index(']',end+1);args.append(text[end+1:close]);end=close+1
                val,end=group(text,end)
            except (ValueError,IndexError):continue
            if name in ('etiquette','label'):value=''
            elif name in ('hyperrefext','eqhyperrefext','neweqhyperrefext'):value=(args[0]+' ' if args else '')+visible_projection(val)
            elif name=='eqhyperref':value='('+visible_projection(val)+')'
            elif name=='pagehyperref':value='(page '+visible_projection(val)+')'
            else:value=visible_projection(val)
        out.append(text[pos:m.start()]);out.append(value);pos=end
    out.append(text[pos:]);text=''.join(out)
    return re.sub(r'\s+',' ',strip_comments(text)).strip()
