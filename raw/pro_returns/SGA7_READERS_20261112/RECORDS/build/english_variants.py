#!/usr/bin/env python3
"""Reconstruct English diplomatic readings from attested French variants.

Every accepted operation records its source, location, exact readings, and
the matching rule. This file never edits the supplied sources.
"""
import bisect
import collections
import difflib
import json
import re
from pathlib import Path
from english_stage import ROOT,SRC,WORK,OUT,MARK,MATH,load_components,load_port,english_root,expose

OPS='Hom|Ext|Tor|Specf|Spec|Gal|Aut|Isom|Biext|Pic|Coker|Ker|Im|Proj|Sym|Tr|Gr|Lie|End|Supp|dim|rank|char|car|length'
MTOKEN=re.compile(r'\\(?:SGARefTarget|SGARefAliasTarget|label)\{[^}]*\}|\\tag\*?\{[^}]*\}|\\SGARefLink\{[^}]*\}|\\(?:operatorname|mathrm|textup)\{(?:'+OPS+r')\}|\\(?:'+OPS+r')\b|\\[A-Za-z]+|\\.|[^\s]',re.S)
MDROP={'\\,','\\;','\\:','\\!','\\ ','\\quad','\\qquad','\\left','\\right','\\big','\\Big','\\bigl','\\bigr','\\Bigl','\\Bigr','\\biggl','\\biggr','\\displaystyle','\\textstyle','\\mathrm','\\mathbf','\\mathbb','\\mathcal','\\mathscr','\\mathfrak','\\operatorname','\\text','\\mbox','\\hbox','{','}'}
MSAME={'\\varphi':'\\phi','\\epsilon':'\\varepsilon','\\leqslant':'\\le','\\leq':'\\le','\\geqslant':'\\ge','\\geq':'\\ge','\\longrightarrow':'\\to','\\rightarrow':'\\to','\\overline':'\\bar','\\widetilde':'\\tilde','\\widehat':'\\hat','\\longleftrightarrow':'\\leftrightarrow'}


def lex(t):
    out=[]
    for m in MTOKEN.finditer(t):
        z=m.group()
        if z in MDROP or re.match(r'\\(?:SGARef|label|tag)',z):continue
        op=re.fullmatch(r'\\(?:operatorname|mathrm|textup)\{('+OPS+r')\}|\\('+OPS+r')',z)
        if op:
            name=op.group(1) or op.group(2)
            z='OP'+('char' if name=='car' else name)
        else:z=MSAME.get(z,z)
        out.append((m.start(),m.end(),z))
    return out


def norm(t):return tuple(z[2] for z in lex(t))


def editorial_spans(t):
    """Find explicitly identified inherited editorial notes, not author notes."""
    spans=[]
    for m in re.finditer(r'\\footnote\{',t):
        d=1;i=m.end()
        while d and i<len(t):
            if t[i]=='\\':i+=2;continue
            if t[i]=='{':d+=1
            elif t[i]=='}':d-=1
            i+=1
        body=t[m.end():i-1];flat=' '.join(body.split())
        if (re.search(r'\b(?:the print|The print|printed source|[Tt]he source|[Ww]orking transcription|[Ff]rozen transcription|[Ee]ditorial|[Ee]nglish restores|source-visible)',flat)
            or flat.startswith(('Both printed citations','This paragraph prints','The last printed implication','The ink beside the vertical arrow'))):
            spans.append((m.start(),i,body,'inherited editorial footnote'))
    # These paragraphs name their editorial role explicitly. Their complete
    # text is retained separately in the records and apparatus-only notes.
    for m in re.finditer(r'(?:\A|(?<=\n\n))([^\n]*(?:\n(?!\s*\n)[^\n]*)*)',t):
        body=m.group();flat=' '.join(body.split())
        if any(a<=m.start()<b for a,b,_,_ in spans):continue
        if (flat.startswith(('The source prints ','The printed target ','The working transcription ',r'\noindent\emph{Editorial note.}'))
            or flat.startswith('In (2.1.8.8) the English restores')):
            spans.append((m.start(),m.end(),body,'inherited editorial paragraph'))
    extra=[
      r'(?:\\medskip\s*)?\\noindent\\emph\{Source note\.\}.*?(?=\n\s*\n|\Z)',
      r'\\noindent\\emph\{Editorial note\.\}.*?(?=\n\s*\n|\Z)',
      r'The printed upper identification.*?supplied here\.',
      r'The working transcription misreads.*?all give\s*\$[^$]*\$\.',
      r'\(the printed diagram inadvertently.*?\$\\bar X\$\)\.',
      r'Here and below we retain the scheme.*?inadvertently writes.*?\$\.',
      r'The printed bottom-right term.*?as written here\.',
      r'The print\s+mistakenly refers here.*?\(2\.1\.8\.1\)\.',
      r'The printed\s+reference to \(2\.1\.7\.1\).*?involved\.',
      r'The print refers here to 2\.2\.1.*?fixed in 2\.1\.1\.',
      r'The print\s+has \$Rf_\\Phi\$.*?which is used here\.',
      r'The print has \$\\\{x\\\}\$ also.*?following diagram confirms\.',
      r"The print's references.*?the relevant support\.",
      r'The printed \$R\\Phi\(F\)\$.*?general formulation\.',
      r'The printed reference \(2\.4\.4\.1\).*?\(2\.4\.5\.1\)\.',
      r'The print writes target \$C\$.*?readings used here\.',
      r'The print omits the final closing parenthesis in the target of \(4\.4\.6\)\.',
      r'The print repeats an extraneous.*?preceding sentence\.',
      r'The print gives the twist \$n\$.*?adjacent terms require \$m\$\.',
      r'The print has \$2n-1\$ and twist.*?\(4\.4\.12\)\.',
      r'The print has twist \$n\$ here.*?twist \$m\$\.',
      r'The print has the evident typographical forms.*?\\emph\{suffisamment\}\.',
      r"The print calls this ``Appendix I,''.*?Appendix as \\S 5\.",
      r'; the further citation is left\s+blank in the print',
      r'; the further\s+citation is blank in the print',
      r'; the\s+further citation is blank in the print',
      r'In \(2\.1\.8\.8\) the English restores.*?as in \(2\.1\.8\.8\)\.',
    ]
    for pattern in extra:
        for m in re.finditer(pattern,t,re.S):
            if any(a<=m.start() and m.end()<=b for a,b,_,_ in spans):continue
            spans.append((m.start(),m.end(),m.group(),'inherited editorial statement'))
    # Disjoint maximal intervals prevent a note nested in a larger note from
    # being removed twice; its text is preserved once in the separate register.
    out=[]
    for row in sorted(spans,key=lambda z:(z[0],-z[1])):
        if out and row[0]<out[-1][1]:
            if row[1]<=out[-1][1]:continue
            a,b,_,kind=out.pop();out.append((a,row[1],t[a:row[1]],kind))
        else:out.append(row)
    return out


def balanced(t):
    depth=0
    for m in re.finditer(r'\\.|[{}]',t):
        x=m.group()
        if x=='{':depth+=1
        elif x=='}':depth-=1
        if depth<0:return False
    return depth==0


def transfer(old,new,target):
    """Transfer only altered tokens; retain English commands and surrounding text.

    Alignment is local to the attested English passage. An operation is rejected
    if changed tokens cannot be identified or if the resulting braces are unsafe.
    """
    a,b,c=lex(old),lex(new),lex(target)
    av,bv,cv=[x[2] for x in a],[x[2] for x in b],[x[2] for x in c]
    sm=difflib.SequenceMatcher(None,bv,cv,autojunk=False)
    links={i+k:j+k for i,j,n in sm.get_matching_blocks() for k in range(n)}
    operations=[]
    for tag,bi,bj,ai,aj in difflib.SequenceMatcher(None,bv,av,autojunk=False).get_opcodes():
        if tag=='equal':continue
        if bi<bj:
            if any(k not in links for k in range(bi,bj)):return None
            ci,cj=links[bi],links[bj-1]+1
            if cj-ci!=bj-bi:return None
            s,e=c[ci][0],c[cj-1][1]
        else:
            if bi in links:
                ci=links[bi];s=e=c[ci][0]
            elif bi-1 in links:
                ci=links[bi-1]+1;s=e=c[ci-1][1]
            else:return None
        replacement=old[a[ai][0]:a[aj-1][1]] if ai<aj else ''
        # A missing printed delimiter must not leave a TeX sizing command
        # without its argument. A null delimiter has no printed glyph.
        if not replacement and target[s:e] in ['(',')','[',']','|']:
            prefix=re.search(r'\\(left|right|bigl|bigr|Bigl|Bigr|biggl|biggr)\s*$',target[:s])
            if prefix:
                if prefix.group(1) in ['left','right']:replacement='.'
                else:s=prefix.start()
        operations.append((s,e,replacement))
    res=target
    for s,e,r in reversed(operations):res=res[:s]+r+res[e:]
    res=re.sub(r'\\(?:operatorname|mathrm|mathcal|mathbb)\{\}', '', res)
    if not operations or res==target:return None
    if balanced(target)!=balanced(res):return None
    return res


def math_entries(t,exclude_editorial=False):
    result=[]
    spans=editorial_spans(t) if exclude_editorial else []
    for m in MATH.finditer(t):
        if any(a<=m.start()<b for a,b,_,_ in spans):continue
        g=next(i for i in [1,2,3,4,7] if m.group(i) is not None)
        result.append({'start':m.start(),'end':m.end(),'body_start':m.start(g),'body_end':m.end(g),
                       'body':m.group(g),'text':m.group(),'norm':norm(m.group(g))})
    return result


def op_entry(volume,component,start,end,before,after,source,page,kind,method):
    return {'volume':volume,'component':component,'start':start,'end':end,
            'corrected':before,'printed':after,'source':source,'folio':str(page),
            'kind':kind,'method':method}


def exact_port_variants(components,candidates):
    bykey={(c['volume'],c['component']):c for c in components}
    ops=[];pending=[];excluded=[]
    for x in candidates:
        vol=x['volume'];f=x['fr_fix'];p=x['port'];cid=x['id']
        if f['file']=='expose_VI_body.tex':continue
        if not x['fr_page_differs']:
            excluded.append({**x,'reason':'French diplomatic and corrected pages are identical'});continue
        if p.get('decision')=='not_applicable':
            excluded.append({**x,'reason':p.get('note','French language or punctuation has no distinct English rendering')});continue
        key=(vol,p.get('tr_file',''))
        if key not in bykey:
            pending.append({**x,'reason':'No exact English component in saved port decision'});continue
        c=bykey[key];et=c['text']
        if p.get('decision')=='apply':
            new=p.get('tr_new','');old=p.get('tr_old','')
            if new and et.count(new)==1:
                q=et.index(new);ops.append(op_entry(vol,c['component'],q,q+len(new),new,old,f"{p['source']}; fixes/FIXLOG_{vol}_CURRENT.jsonl#{cid}; "+str(f.get('id','')),f['page'],f['kind'],'exact port reverse, French-layer distinction'))
                continue
        elif p.get('decision')=='already':
            target=p.get('tr_old','');before=transfer(f['old'],f['new'],target) if target else None
            if before and et.count(target)==1:
                q=et.index(target);ops.append(op_entry(vol,c['component'],q,q+len(target),target,before,f"{p['source']}#{cid}; fixes/FIXLOG_{vol}_CURRENT.jsonl#{cid}; "+str(f.get('id','')),f['page'],f['kind'],'token transfer within attested port passage'))
                continue
        pending.append({**x,'reason':'English passage requires a contextual reconstruction'})
    return ops,pending,excluded


def formula_variants(components):
    raw=json.loads((WORK/'fr_differences_raw.json').read_text())
    byexp=collections.defaultdict(list)
    for c in components:
        if c['expose'] not in ['VI','Catalogue','Introduction','Front']:
            byexp[(c['volume'],c['expose'])].append(c)
    mapped={}; stats=[]; structures={}
    for (vol,exp),cs in byexp.items():
        fp=SRC/'fr'/('sga7i' if vol=='7I' else 'sga7ii')/'current'/('expose_'+exp+'_body.tex')
        ft=fp.read_text();fm=math_entries(ft)
        em=[]
        for c in cs:
            for z in math_entries(c['text'],True):em.append({**z,'component':c['component']})
        a,b=[z['norm'] for z in fm],[z['norm'] for z in em]
        links=[]
        for i,j,n in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks():
            for k in range(n):
                mapped[(vol,exp,fm[i+k]['body_start'])]=em[j+k]
                links.append((fm[i+k]['body_start'],j+k))
        structures[(vol,exp)]=(fm,em,links)
        stats.append({'volume':vol,'expose':exp,'French_formulas':len(fm),'English_formulas':len(em),
                      'matched':sum(n for i,j,n in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks())})
    ops=[];unmapped=[];fuzzy=[]
    for idx,r in enumerate(raw):
        vol,fn,page=r['volume'],r['file'],r['page'];exp=expose(fn)
        if exp in ['VI','Catalogue','Introduction','Front']:continue
        old,new=r['old'],r['new']
        om,nm=math_entries(old),math_entries(new)
        if not om or len(om)!=len(nm):
            if norm(old)!=norm(new):unmapped.append({'raw_index':idx,'volume':vol,'expose':exp,'page':page,'reason':'unequal or absent formula counts'})
            continue
        fp=SRC/'fr'/('sga7i' if vol=='7I' else 'sga7ii')/'current'/fn
        ft=fp.read_text();marks=list(MARK.finditer(ft))
        choices=[(m.end(),marks[i+1].start() if i+1<len(marks) else len(ft)) for i,m in enumerate(marks) if m.group(2)==str(page)]
        if not choices:continue
        ps,pe=choices[0];at=ft.find(new,ps,pe)
        if at<0:continue
        for on,nn in zip(om,nm):
            if on['norm']==nn['norm']:continue
            e=mapped.get((vol,exp,at+nn['body_start']));method='ordered normalized formula match'
            if not e:
                fm,em,links=structures.get((vol,exp),([],[],[]))
                fpos=at+nn['body_start'];j=bisect.bisect_left([p for p,k in links],fpos)
                lo=links[j-1][1]+1 if j>0 else 0;hi=links[j][1] if j<len(links) else len(em)
                nearby=em[max(0,lo-1):min(len(em),hi+1)]
                nv=nn['norm']
                exact=[]
                for cand in nearby:
                    cv=cand['norm']
                    for k in range(len(cv)-len(nv)+1):
                        if tuple(cv[k:k+len(nv)])==tuple(nv):
                            if len(nv)>=4 or len(cv)==len(nv):exact.append(cand)
                if len(exact)==1:
                    e=exact[0];method='unique exact formula substring between ordered anchors'
                elif len(nv)>=8:
                    ranked=sorted([(difflib.SequenceMatcher(None,nv,cand['norm'],autojunk=False).ratio(),q,cand) for q,cand in enumerate(nearby)],reverse=True)
                    if ranked and ranked[0][0]>=.86 and (len(ranked)==1 or ranked[0][0]-ranked[1][0]>=.08):
                        e=ranked[0][2];method='reviewed local formula alignment; similarity '+str(round(ranked[0][0],4))
                if not e:
                    unmapped.append({'raw_index':idx,'volume':vol,'expose':exp,'page':page,'old':on['body'],'new':nn['body'],'reason':'no aligned exact normalized English formula'});continue
            printed=transfer(on['body'],nn['body'],e['body'])
            if printed:
                op=op_entry(vol,e['component'],e['body_start'],e['body_end'],e['body'],printed,
                           f"fr/{'sga7i' if vol=='7I' else 'sga7ii'}/{{diplomatic,current}}/{fn}; folio {page}; difference {idx+1}",page,'mathematical reading',method)
                ops.append(op)
                if method!='ordered normalized formula match':fuzzy.append(op)
            else:unmapped.append({'raw_index':idx,'volume':vol,'expose':exp,'page':page,'old':on['body'],'new':nn['body'],'reason':'token transfer unsafe'})
    (WORK/'en_formula_extended_matches.json').write_text(json.dumps(fuzzy,ensure_ascii=False,indent=1))
    return ops,stats,unmapped


def paired_formula_variants(components):
    """Collate complete source formulas, so line-diff boundaries lose no math."""
    byexp=collections.defaultdict(list)
    for c in components:
        if c['expose'] not in ['VI','Catalogue','Introduction','Front']:
            byexp[(c['volume'],c['expose'])].append(c)
    operations=[];unmapped=[];stats=[]
    for (vol,exp),cs in byexp.items():
        fn='expose_'+exp+'_body.tex';base=SRC/'fr'/('sga7i' if vol=='7I' else 'sga7ii')
        dt=(base/'diplomatic'/fn).read_text();ct=(base/'current'/fn).read_text()
        dm,cm=math_entries(dt),math_entries(ct);em=[]
        for c in cs:
            for e in math_entries(c['text'],True):em.append({**e,'component':c['component']})
        links={};anchors=[]
        for i,j,n in difflib.SequenceMatcher(None,[z['norm'] for z in cm],[z['norm'] for z in em],autojunk=False).get_matching_blocks():
            for k in range(n):links[i+k]=j+k;anchors.append((i+k,j+k))
        pairs=[]
        for tag,i,j,k,l in difflib.SequenceMatcher(None,[z['norm'] for z in dm],[z['norm'] for z in cm],autojunk=False).get_opcodes():
            if tag=='equal':continue
            if j-i==l-k:
                pairs.extend((i+n,k+n) for n in range(j-i))
            else:
                # Unequal formula counts require a uniquely close, ordered mate.
                previous=i-1
                for ci in range(k,l):
                    candidates=sorted([(difflib.SequenceMatcher(None,dm[di]['norm'],cm[ci]['norm'],autojunk=False).ratio(),di) for di in range(max(i,previous+1),j)],reverse=True)
                    if candidates and candidates[0][0]>.60 and (len(candidates)==1 or candidates[0][0]-candidates[1][0]>.10):
                        di=candidates[0][1];pairs.append((di,ci));previous=di
                    else:unmapped.append({'volume':vol,'expose':exp,'current_formula':ci,'new':cm[ci]['body'],
                                          'old_candidates':[z['body'] for z in dm[i:j]],
                                          'reason':'source formula counts differ; no unique mate'})
        marks=list(MARK.finditer(ct));mp=[m.start() for m in marks]
        hit=0
        for di,ci in pairs:
            old,new=dm[di],cm[ci]
            if old['norm']==new['norm']:continue
            page=marks[max(0,bisect.bisect_right(mp,new['start'])-1)].group(2) if marks else '?'
            target=em[links[ci]] if ci in links else None;method='ordered complete-formula alignment'
            if target is None:
                q=bisect.bisect_left([a for a,b in anchors],ci)
                lo=anchors[q-1][1]+1 if q else 0;hi=anchors[q][1] if q<len(anchors) else len(em)
                nearby=em[max(0,lo-1):min(len(em),hi+1)]
                exact=[];nv=new['norm']
                for e in nearby:
                    ev=e['norm']
                    if len(nv)>=4:
                        for j in range(len(ev)-len(nv)+1):
                            if ev[j:j+len(nv)]==nv:exact.append(e)
                    elif ev==nv:exact.append(e)
                if len(exact)==1:target=exact[0];method='unique complete-formula substring between ordered anchors'
                elif len(nv)>=8:
                    ranked=sorted([(difflib.SequenceMatcher(None,nv,e['norm'],autojunk=False).ratio(),j,e) for j,e in enumerate(nearby)],reverse=True)
                    if ranked and ranked[0][0]>=.86 and (len(ranked)==1 or ranked[0][0]-ranked[1][0]>=.08):
                        target=ranked[0][2];method='local complete-formula alignment; similarity '+str(round(ranked[0][0],4))
            if target is None:
                ranked=sorted([(difflib.SequenceMatcher(None,new['norm'],e['norm'],autojunk=False).ratio(),j,e) for j,e in enumerate(nearby)],reverse=True)
                choices=[{'component':e['component'],'body':e['body'],'start':e['body_start'],'end':e['body_end'],'similarity':score} for score,j,e in ranked[:5]]
                unmapped.append({'volume':vol,'expose':exp,'page':page,'old':old['body'],'new':new['body'],'target_candidates':choices,
                                 'reason':'no unique English formula alignment'});continue
            printed=transfer(old['body'],new['body'],target['body'])
            if printed is None:
                unmapped.append({'volume':vol,'expose':exp,'page':page,'old':old['body'],'new':new['body'],'english':target['body'],
                                 'component':target['component'],'start':target['body_start'],'end':target['body_end'],
                                 'reason':'token transfer cannot preserve balanced TeX'});continue
            operations.append(op_entry(vol,target['component'],target['body_start'],target['body_end'],target['body'],printed,
                                       f"fr/{'sga7i' if vol=='7I' else 'sga7ii'}/{{diplomatic,current}}/{fn}; folio {page}; formula {ci+1}",page,'mathematical reading',method));hit+=1
        stats.append({'volume':vol,'expose':exp,'French_diplomatic_formulas':len(dm),'French_current_formulas':len(cm),
                      'English_formulas_without_editorial_notes':len(em),'source_formula_pairs_differing':len(pairs),'mapped_variants':hit})
    return operations,stats,unmapped


def main():
    import argparse,hashlib
    parser=argparse.ArgumentParser(description='Generate proposals, or verify and reuse the audited proposal snapshot.')
    parser.add_argument('--refresh-proposals',action='store_true',help='Replace the proposal snapshot; all dependent editorial resolution ledgers must then be reviewed again.')
    args=parser.parse_args();frozen=WORK/'en_proposals_frozen.json'
    if frozen.exists() and not args.refresh_proposals:
        evidence=json.loads(frozen.read_text())
        for item in evidence['inputs']:
            p=(SRC if item['scope']=='archive' else WORK)/item['path']
            assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],('audited English proposal input changed',item['scope'],item['path'])
        for item in evidence['proposals']:
            assert hashlib.sha256((WORK/item['path']).read_bytes()).hexdigest()==item['sha256'],('audited English proposal ledger changed',item['path'])
        print('Verified and reused audited English proposal snapshot:',evidence['counts'])
        return
    components=json.loads((WORK/'en_components.json').read_text())
    candidates=json.loads((WORK/'en_candidates.json').read_text())
    ops,pending,excluded=exact_port_variants(components,candidates)
    fops,stats,unmapped=paired_formula_variants(components)
    (WORK/'en_port_operations.json').write_text(json.dumps(ops,ensure_ascii=False,indent=1))
    (WORK/'en_formula_operations.json').write_text(json.dumps(fops,ensure_ascii=False,indent=1))
    (WORK/'en_pending.json').write_text(json.dumps(pending,ensure_ascii=False,indent=1))
    (WORK/'en_excluded.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=1))
    for i,x in enumerate(unmapped):x['index']=i
    (WORK/'en_formula_unmapped.json').write_text(json.dumps(unmapped,ensure_ascii=False,indent=1))
    (WORK/'en_formula_alignment_stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=1))
    print(json.dumps({'port_operations':len(ops),'formula_operations':len(fops),'pending_port':len(pending),'excluded_port':len(excluded),'unmapped_formula_or_prose_hunks':len(unmapped)},indent=2))


if __name__=='__main__':main()
