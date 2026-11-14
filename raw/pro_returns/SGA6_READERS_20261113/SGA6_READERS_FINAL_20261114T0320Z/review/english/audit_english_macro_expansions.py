#!/usr/bin/env python3
"""Locate active source-managed formula macro differences in the full books.

This is a conservative declaration/usage comparison, not a TeX interpreter.
Every unequal expansion is retained for explicit adjudication or a TeX probe.
"""
from pathlib import Path
from collections import defaultdict,Counter
from bisect import bisect_right
import hashlib,json,re
from source_emphasis import MATH,braced
from english_typography import MARK

EN=Path(__file__).resolve().parent
ROOT=EN.parents[1]
OUT=EN/'aggregate'
DECL=re.compile(r'\\(newcommand|renewcommand|providecommand|DeclareMathOperator)\*?\s*')
CMD=re.compile(r'\\([A-Za-z@]+)')


def sha(text):return hashlib.sha256(text.encode()).hexdigest()


def declarations(source):
    result=[]
    for m in DECL.finditer(source):
        i=m.end()
        if source[i]=='{':
            name,i=braced(source,i)
        else:
            n=re.match(r'\\[A-Za-z@]+',source[i:])
            if not n:continue
            name=n.group();i+=len(name)
        if not re.fullmatch(r'\\[A-Za-z@]+',name):continue
        while source[i].isspace():i+=1
        args=[]
        while source[i]=='[':
            j=source.index(']',i)
            args.append(source[i+1:j]);i=j+1
            while source[i].isspace():i+=1
        if source[i]!='{':continue
        body,end=braced(source,i)
        if m[1]=='DeclareMathOperator':body=r'\operatorname{'+body+'}'
        result.append(dict(start=m.start(),end=end,kind=m[1],name=name[1:],args=args,body=body,literal=source[m.start():end]))
    return result


def expansion(name,state,seen=()):
    if name not in state:return '\\'+name
    if name in seen:return '<recursive:'+name+'>'
    d=state[name]
    body=CMD.sub(lambda m:expansion(m[1],state,seen+(name,)),d['body'])
    return ('<args:'+','.join(d['args'])+'>'+body) if d['args'] else body


def inventory(source,managed):
    marks=list(MARK.finditer(source));offsets=[m.start() for m in marks]
    decls=declarations(source);state={};d=0
    result=defaultdict(Counter);examples={}
    for unit in MATH.finditer(source):
        k=bisect_right(offsets,unit.start())-1
        if k<0 or not marks[k][1].isdigit():continue
        page=int(marks[k][1])
        while d<len(decls) and decls[d]['start']<unit.start():
            row=decls[d]
            if row['kind']!='providecommand' or row['name'] not in state:state[row['name']]=row
            d+=1
        for token in CMD.finditer(unit.group()):
            name=token[1]
            if name not in managed:continue
            value=expansion(name,state)
            result[page,name][value]+=1
            examples.setdefault((page,name,value),dict(literal_unit=unit.group(),declaration=state.get(name),expansion=value))
    return result,examples,decls


def main():
    en=(OUT/'MATERIALIZED_current_before_layout.tex').read_text()
    # This exact local support definition is applied before annotation/printing.
    for line in (EN/'EN_AGGREGATE_MACRO_TRANSPORTS.jsonl').read_text().splitlines():
        patch=json.loads(line)
        assert en.count(patch['old'])==1
        en=en.replace(patch['old'],patch['new'],1)
    fr=(ROOT/'build/FR_current_revised.tex').read_text()
    managed={r['name'] for s in [fr,en] for r in declarations(s)}
    fi,fe,fd=inventory(fr,managed);ei,ee,ed=inventory(en,managed)
    differences=[];equal=[]
    for key in sorted(set(fi)|set(ei)):
        if fi[key]==ei[key]:
            equal.append(dict(page=key[0],command=key[1],occurrences=sum(fi[key].values()),expansions=dict(fi[key])))
            continue
        differences.append(dict(page=key[0],command=key[1],French=dict(fi[key]),English=dict(ei[key]),
            French_examples=[fe[key+(value,)] for value in fi[key]],
            English_examples=[ee[key+(value,)] for value in ei[key]]))
    report=dict(method='Ordered new/renew/provide/DeclareMathOperator declarations with transitive source-managed expansion trees at formula uses; exact command and argument payloads retained.',
        limitation='Conservative static audit, not a TeX interpreter; inherited package definitions, grouping and any unlisted declaration syntax require explicit adjudication for unequal cases.',
        French_input_sha256=sha(fr),English_input_sha256=sha(en),source_managed_commands=len(managed),
        equal_page_command_groups=len(equal),unequal_page_command_groups=len(differences),
        equal=equal,differences=differences)
    (OUT/'MACRO_EXPANSION_STATIC_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('equal',len(equal),'unequal',len(differences))
    for row in differences:
        print(row['page'],row['command'],'FR',row['French'],'EN',row['English'])


if __name__=='__main__':main()
