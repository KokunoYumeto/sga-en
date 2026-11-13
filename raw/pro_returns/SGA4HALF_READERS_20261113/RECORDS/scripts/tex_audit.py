"""Small, balanced TeX-source readers used by the edition's audit scripts."""
import re

def group(s,pos):
    while pos<len(s) and s[pos].isspace():pos+=1
    if pos>=len(s) or s[pos]!='{':raise ValueError(('expected group',s[pos:pos+80]))
    start=pos+1;depth=1;pos+=1
    while pos<len(s):
        if s[pos]=='\\':
            # Escaped braces are characters; a control word does not shield its group.
            if pos+1<len(s) and s[pos+1] in '{}%\\':pos+=2;continue
        if s[pos]=='{':depth+=1
        elif s[pos]=='}':
            depth-=1
            if not depth:return s[start:pos],pos+1
        pos+=1
    raise ValueError('unclosed TeX group')

def variants(s):
    rows=[]
    for m in re.finditer(r'\\var(?:\[[^\]]*\])?\s*\{',s):
        # Nested variant nodes are forbidden in this edition.
        a,end=group(s,m.end()-1);b,end=group(s,end);ident,end=group(s,end)
        pages=re.findall(r'\\(?:PrintPage|MathPage)\{([^}]+)\}',s[:m.start()])
        rows.append(dict(start=m.start(),end=end,printed=a,corrected=b,source=ident,
                         page=pages[-1] if pages else '',line=s[:m.start()].count('\n')+1))
    for a,b in zip(rows,rows[1:]):
        if b['start']<a['end']:raise ValueError('nested variants')
    return rows

def resolve(s,which='corrected'):
    for v in reversed(variants(s)):s=s[:v['start']]+v[which]+s[v['end']:]
    return s

def marker_rows(s):
    rows=[]
    for m in re.finditer(r'\\(?:PrintPage|MathPage)\{([^}]+)\}',s):
        rows.append(dict(page=m[1],offset=m.start(),line=s[:m.start()].count('\n')+1,
                         start=s[m.end():m.end()+240].strip()))
    return rows

def strip_comments(s):
    return re.sub(r'(?<!\\)%[^\n]*','',s)

def math_fragments(s):
    s=resolve(s);s=strip_comments(s)
    s=re.sub(r'\\(?:PrintPage|MathPage)\{[^}]*\}','',s)
    patt=r'(?<!\\)\$|\\\[|\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}'
    rows=[];pos=0
    while (m:=re.search(patt,s[pos:])):
        a=pos+m.start();b=pos+m.end()
        if m[0]=='$':
            level=0;e=b
            while e<len(s):
                if s[e]=='\\' and e+1<len(s) and s[e+1] in '{}$%\\':e+=2;continue
                if s[e]=='{':level+=1
                elif s[e]=='}':level-=1
                elif s[e]=='$' and level==0:break
                e+=1
            end=e+1
        else:
            delimiter=r'\]' if m[0]==r'\[' else r'\end{'+m[1]+'}'
            e=s.find(delimiter,b)
            if e<0:raise ValueError('unclosed math display')
            end=e+len(delimiter)
        rows.append((a,s[b:e]));pos=end
    return rows

def canonical_math(s):
    s=re.sub(r'\\(?:label|tag)\{[^}]*\}','',s)
    for command in ['text','textrm','textnormal','mbox']:
        pos=0
        while (m:=re.search(r'\\'+command+r'\s*\{',s[pos:])):
            start=pos+m.start();_,end=group(s,pos+m.end()-1)
            s=s[:start]+'TXT'+s[end:];pos=start+3
    s=re.sub(r'\\(?:left|right|big|Big|bigg|Bigg|,|;|!|quad|qquad)(?![A-Za-z])','',s)
    s=re.sub(r'\s+','',s)
    # Braces around one token are syntactic grouping, not a notation difference.
    old=None
    while old!=s:
        old=s;s=re.sub(r'\{([A-Za-z0-9]|\\[A-Za-z]+)\}',r'\1',s)
    return s
