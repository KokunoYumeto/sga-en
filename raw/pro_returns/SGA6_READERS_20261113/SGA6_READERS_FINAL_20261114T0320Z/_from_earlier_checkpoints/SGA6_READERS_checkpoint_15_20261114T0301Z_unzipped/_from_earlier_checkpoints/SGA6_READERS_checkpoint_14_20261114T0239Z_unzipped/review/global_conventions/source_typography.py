"""Explicit final source typography transport; mathematical units stay literal.

This is a scoped formatter for groups already read in the source. It does not
choose new statement spans. The caller supplies the separately observed plain
nested groups and resp. occurrences. Decimal references are enumerated in the
returned record; they are preserved outside the lexical rules.
"""
import re

MATH = re.compile(
    r'\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}.*?'
    r'\\end\{(?:equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}'
    r'|(?<!\\)\\\[.*?(?<!\\)\\\]'
    r'|(?<!\\)\\\(.*?(?<!\\)\\\)'
    r'|(?<!\\)\$(?:[^$]|\\\$)*?(?<!\\)\$',re.S)
ARG_COUNTS = {'SGAPrintPage':1,'sgaStableTarget':1,'SGAAuthorFootnote':2,
              'SGAAuthorFootMark':1,'SGAAuthorFootText':2,'footnote':1,
              'footnotetext':1,'var':3}
CONTROL = r'\\(?:'+ '|'.join(ARG_COUNTS)+r')\{'
REFERENCE = r'(?<![A-Za-z0-9])\d+(?:\.\d+)+(?![A-Za-z0-9])'
TOKEN = re.compile(MATH.pattern+'|'+CONTROL+r'|\\emph\{'
                   r'|(?<!\\)%[^\n]*(?:\n|$)'+'|'+REFERENCE+r'|\bresp\.',re.S)
MARK = re.compile(r'%{10}\s+scan idx\s+\d+\s*\|\s*folio\s+(\d+)\s+%{10}')

def braced(text,start):
    assert text[start]=='{'
    depth=1;i=start+1
    while depth:
        if i>=len(text):raise ValueError('Unclosed control argument')
        if text[i]=='\\':i+=2;continue
        if text[i]=='%':
            k=text.find('\n',i);i=len(text) if k<0 else k+1;continue
        if text[i]=='{':depth+=1
        elif text[i]=='}':depth-=1
        i+=1
    return text[start+1:i-1],i

def note_spans(text):
    out=[]
    rx=re.compile(r'\\(?:SGAAuthorFootnote|SGAAuthorFootMark|SGAAuthorFootText)\{')
    for m in rx.finditer(text):
        name=m.group()[1:-1];j=m.end()-1
        for _ in range(ARG_COUNTS[name]):_,j=braced(text,j)
        out.append((m.start(),j,text[m.start():j]))
    return out

def notes(text):return [s for a,b,s in note_spans(text)]

def note_labels(text):
    answer=[]
    for a,b,s in note_spans(text):
        k=s.find('{');label,_=braced(s,k)
        answer.append((s[1:k],label))
    return answer

def transport(text,plain_nested_pages,plain_resp_pages):
    marks=list(MARK.finditer(text))
    def page_at(pos):
        prior=[m for m in marks if m.start()<=pos]
        return int(prior[-1].group(1)) if prior else None
    changes=[]
    def content(body,absolute):
        stats={'word_spans':0,'plain_nested':[],'plain_resp':[],
               'plain_references':[],'punctuation_only_spans':[]}
        def words(s):
            if not s.strip():return s
            # Separate edge punctuation from the ruled lexical words. Apostrophe
            # and TeX accent/control tokens are deliberately not in this set.
            edge=' \t\r\n.,;:!?()[]«»~'
            a=0;b=len(s)
            while a<b and s[a] in edge:a+=1
            while b>a and s[b-1] in edge:
                k=b-2;escape_count=0
                while k>=a and s[k]=='\\':escape_count+=1;k-=1
                if escape_count%2:break
                b-=1
            if a==b or not re.search(r'[A-Za-zÀ-ÿ]',s[a:b]):
                stats['punctuation_only_spans'].append(s)
                return s
            # Do not split a TeX control-space from its backslash.
            k=b-1;slashes=0
            while k>=a and s[k]=='\\':slashes+=1;k-=1
            if slashes%2 and b<len(s) and s[b]==' ':b+=1
            stats['word_spans']+=1
            return s[:a]+r'\uline{'+s[a:b]+'}'+s[b:]
        out=[];pos=0
        while True:
            m=TOKEN.search(body,pos)
            if not m:
                out.append(words(body[pos:]));break
            out.append(words(body[pos:m.start()]))
            token=m.group();p=page_at(absolute+m.start())
            command=re.fullmatch(r'\\([A-Za-z]+)\{',token)
            if command:
                name=command.group(1);j=m.end()-1
                if name=='emph':
                    assert p in plain_nested_pages,('Unmapped nested emphasis',p)
                    inner,j=braced(body,j)
                    assert r'\emph{' not in inner
                    out.append(inner)
                    stats['plain_nested'].append(dict(page=p,old=body[m.start():j],plain=inner))
                else:
                    args=[]
                    for _ in range(ARG_COUNTS[name]):
                        arg,j=braced(body,j);args.append(arg)
                    # French branch inputs contain no var. This exclusion keeps
                    # apparatus selectors and author-note arguments out of rules.
                    out.append(body[m.start():j])
                pos=j
            elif re.fullmatch(REFERENCE,token):
                out.append(token);pos=m.end()
                stats['plain_references'].append(dict(page=p,text=token))
            elif token=='resp.':
                if p in plain_resp_pages:
                    out.append(token)
                    stats['plain_resp'].append(dict(page=p,text=token))
                else:
                    out.append(words(token))
                pos=m.end()
            else:
                out.append(token);pos=m.end()
        return ''.join(out),stats
    pos=0
    while True:
        a=text.find(r'\emph{',pos)
        if a<0:break
        body,z=braced(text,a+5)
        replacement,stats=content(body,a+6)
        changes.append(dict(start=a,end=z,page=page_at(a),old=text[a:z],new=replacement,**stats))
        pos=z
    final=text
    for c in reversed(changes):final=final[:c['start']]+c['new']+final[c['end']:]
    oldmath=[m.group() for m in MATH.finditer(text)]
    newmath=[m.group() for m in MATH.finditer(final)]
    expected=[];lexical=[]
    for m in MATH.finditer(text):
        unit=m.group();local=[]
        for c in changes:
            if m.start()<=c['start'] and c['end']<=m.end():
                assert re.search(r'\\text\{\s*$',text[m.start():c['start']])
                assert re.fullmatch(r"[A-Za-zÀ-ÿ ,.;:'-]+",text[c['start']+6:c['end']-1]), (c['page'], c['old'])
                local.append(c);lexical.append(dict(page=c['page'],old=c['old'],new=c['new']))
        for c in reversed(local):
            a=c['start']-m.start();b=c['end']-m.start()
            unit=unit[:a]+c['new']+unit[b:]
        expected.append(unit)
    assert expected==newmath,'Literal mathematical unit changed'
    assert note_labels(text)==note_labels(final),'Author note label changed'
    expected_notes=[];note_transports=[]
    for a,b,s in note_spans(text):
        local=[c for c in changes if a<=c['start'] and c['end']<=b]
        result=s
        for c in reversed(local):
            result=result[:c['start']-a]+c['new']+result[c['end']-a:]
        expected_notes.append(result)
        if result!=s:note_transports.append(dict(page=page_at(a),old=s,new=result,
            reason='Only independently inspected lexical emphasis wrappers in the original note body change; its command, label and words remain unchanged.'))
    assert expected_notes==notes(final),'Unmapped author note body change'
    assert [m.group() for m in MARK.finditer(text)]==[m.group() for m in MARK.finditer(final)]
    return final,changes,dict(math_units=len(oldmath),raw_math_equal=oldmath==newmath,
        explicit_lexical_math_transports=lexical,all_other_math_bytes_equal=True,
        author_note_commands=len(notes(text)),author_note_commands_identical=notes(text)==notes(final),
        author_note_labels_identical=True,author_note_body_typography_transports=note_transports,
        marker_commands_identical=True)
