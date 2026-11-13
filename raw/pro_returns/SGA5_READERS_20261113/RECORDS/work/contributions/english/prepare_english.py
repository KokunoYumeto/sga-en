"""Reproducible English content preparation. Input paths are archive-relative.
All comparison signatures retain source-offset maps; no signature is rendered.
"""
from pathlib import Path
import re, json, difflib, bisect, csv, collections, hashlib
BS=chr(92)
MATH = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$|(?<!\\)\$([^$]{1,600}?)(?<!\\)\$|(?<!\\)\\\[(.+?)\\\]|"
                  r"(?<!\\)\\\((.+?)\\\)|\\begin\{(equation|align|eqnarray|gather|multline|displaymath)(\*?)\}(.+?)"
                  r"\\end\{\5\6\}", re.S)
TAG = re.compile(re.escape(BS) + r"tag\*?\{([^{}]*)\}")
DROP = re.compile(re.escape(BS) + r"(?:[,;:! ]|quad|qquad|left|right|[bB]igg?[lr]?|displaystyle|textstyle|limits|"
                  r"nolimits|mathrm|mathbf|mathbb|mathcal|mathscr|mathfrak|boldsymbol|bm|bf|rm|it|operatorname\*?|"
                  r"text(?:rm|it|bf|up)?|mbox|hbox|mathop|label\{[^}]*\}|tag\*?|underline|overline|emph)(?![A-Za-z])")
SAME = [(BS + "varphi", BS + "phi"), (BS + "epsilon", BS + "varepsilon"), (BS + "leqslant", BS + "le"),
        (BS + "leq", BS + "le"), (BS + "geqslant", BS + "ge"), (BS + "geq", BS + "ge"),
        (BS + "longrightarrow", BS + "to"), (BS + "rightarrow", BS + "to"), (BS + "xrightarrow", BS + "to"),
        (BS + "uRHom", "RHom"), (BS + "RHom", "RHom"), (BS + "uHom", BS + "Hom"), (BS + "R", "R"),
        (BS + "lten", BS + "otimes"), (BS + "check", ""), (BS + "bullet", "*")]


def norm(s):
    s = DROP.sub("", s)
    for a, b in SAME:
        s = s.replace(a, b)
    return re.sub(r"[\s{}]", "", s)


def tokens(t):
    out = []
    for m in MATH.finditer(t):
        body = next(g for g in (m.group(1), m.group(2), m.group(3), m.group(4), m.group(7)) if g is not None)
        for tm in TAG.finditer(body):
            out.append((m.start(), "#" + tm.group(1).strip()))
        k = norm(TAG.sub("", body))
        if len(k) >= 3:
            out.append((m.start(), k))
    return out


FRMARK=re.compile(r'%%%%%%%%%%  scan idx (\d+)  \|  folio (\d+)  %%%%%%%%%%')
ENREL='en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex'
ENBEFORE='en/release_source/sources/native/SGA5/SGA5_English_sync_workpass.tex'
FRD='fr/sga5/diplomatic/s5.tex'; FRC='fr/sga5/current/s5.tex'

def uncomment(s):
    return re.sub(r'(?<!\\)%[^\n]*',lambda m:' '*len(m[0]),s)

def getpages(s):
    ms=list(FRMARK.finditer(s));return {int(m[2]):{'start':m.end(),'end':ms[i+1].start() if i+1<len(ms) else len(s),'text':s[m.end():ms[i+1].start() if i+1<len(ms) else len(s)]} for i,m in enumerate(ms)}

def expose(folio):
    es=[(1,'I'),(73,'III'),(138,'III B'),(204,'V'),(251,'VI'),(282,'VII'),(351,'VIII'),(372,'X'),(407,'XII'),(442,'XV'),(481,'Index')]
    return next(v for p,v in reversed(es) if folio>=p)

def mathchunks(s):
    return [{'start':m.start(),'end':m.end(),'text':m[0],'key':norm(m[0])} for m in MATH.finditer(uncomment(s))]

def align_math(fr,en):
    fc,ec=mathchunks(fr),mathchunks(en)
    # The signature is a search index only. Every match retains both exact source strings and offsets.
    sm=difflib.SequenceMatcher(None,[c['key'] for c in fc],[c['key'] for c in ec],autojunk=False)
    direct={}; anchors=[]
    for a,b,n in sm.get_matching_blocks():
        for j in range(n):
            direct[a+j]=b+j
            if n>=2 or len(fc[a+j]['key'])>=12:anchors.append((fc[a+j]['start'],ec[b+j]['start']))
    return fc,ec,direct,anchors

def estimate(x,anchors):
    i=bisect.bisect_left([p[0] for p in anchors],x)
    if i==0:return max(0,anchors[0][1]-(anchors[0][0]-x))
    if i>=len(anchors):return anchors[-1][1]+x-anchors[-1][0]
    (a,b),(c,d)=anchors[i-1:i+1]
    return b+(d-b)*(x-a)//max(1,c-a)

def lex(s):
    return [(m[0],m.start(),m.end()) for m in re.finditer(r'\\[A-Za-z]+|\\.|[A-Za-z]+|\d+|[^\s]',s)]

def normlex(s):
    # A reversible source-location map accompanies every comparison token.
    ts=lex(s);out=[]
    aliases={r'\Z':'ZZ',r'\ZZ':'ZZ',r'\bZ':'ZZ',r'\Q':'QQ',r'\QQ':'QQ',r'\bQ':'QQ',r'\F':'FF',r'\FF':'FF',r'\bF':'FF',r'\N':'NN',r'\NN':'NN',r'\bN':'NN',r'\ol':r'\overline',r'\bar':r'\overline',r'\H':'H',r'\Hh':'H',r'\uHom':r'\Hom',r'\uRHom':r'\RHom',r'\RGamma':'RGamma',r'\R':'R',r'\to':r'\longrightarrow',r'\rightarrow':r'\longrightarrow',r'\leq':r'\le',r'\leqslant':r'\le',r'\geq':r'\ge',r'\geqslant':r'\ge',r'\lten':'LTENSOR'}
    skip={r'\,',r'\;',r'\:',r'\!',r'\ ',r'\quad',r'\qquad',r'\left',r'\right',r'\bigl',r'\bigr',r'\Bigl',r'\Bigr',r'\big',r'\Big',r'\displaystyle',r'\textstyle'}
    i=0
    while i<len(ts):
        val,a,b=ts[i]
        if val in skip:i+=1;continue
        if val in ('{','}'):i+=1;continue
        if val in (r'\mathrm',r'\operatorname',r'\mathbb',r'\mathbf',r'\mathcal',r'\mathfrak',r'\mathscr',r'\underline'):
            # Retain the glyph content for search, leaving typeface changes to exact-spelling records.
            i+=1;continue
        v=aliases.get(val,val)
        if val in ('Z','Q','F','N') and i>0 and any(q[0]==r'\mathbb' for q in ts[max(0,i-2):i]):v=val*2
        out.append((v,a,b));i+=1
    return out

def project_chunk(c,d,e):
    """Project a French printed-reading edit through exact matched search tokens.
    Returned edits are raw English character edits; unmatched cases require review.
    """
    ct,dt,et=normlex(c),normlex(d),normlex(e)
    cv,dv,ev=[[q[0] for q in v] for v in [ct,dt,et]]
    cd=difflib.SequenceMatcher(None,cv,dv,autojunk=False)
    ce=difflib.SequenceMatcher(None,cv,ev,autojunk=False)
    mp={a+j:b+j for a,b,n in ce.get_matching_blocks() for j in range(n)}
    edits=[];unresolved=[]
    for op,a,b,k,l in cd.get_opcodes():
        if op=='equal':continue
        if a<b:
            eis=[mp.get(i) for i in range(a,b)]
            if None in eis or eis!=list(range(eis[0],eis[0]+b-a)):
                unresolved.append({'reason':'changed French tokens do not map contiguously','before':d[dt[k][1]:dt[l-1][2]] if k<l else '', 'after':c[ct[a][1]:ct[b-1][2]]});continue
            x,y=et[eis[0]][1],et[eis[-1]][2]
        else:
            if a>0 and a<len(ct) and a-1 in mp and a in mp and mp[a]==mp[a-1]+1:
                x=y=et[mp[a]][1]
            else:
                unresolved.append({'reason':'insertion boundary not matched','tokens':dv[k:l]});continue
        old=d[dt[k][1]:dt[l-1][2]] if k<l else ''
        # Include braces belonging wholly to the changed old fragment; insertions use balanced TeX below.
        if k<l:
            da,db=dt[k][1],dt[l-1][2]
            while old.count('{')>old.count('}') and db<len(d) and d[db]=='}':old+='}';db+=1
            while old.count('}')>old.count('{') and da>0 and d[da-1]=='{':old='{'+old;da-=1
        before=e[x:y]
        if old==before:continue
        if old.count('{')-old.count('}') != before.count('{')-before.count('}'):
            unresolved.append({'reason':'raw TeX brace boundary needs review','before':old,'after':before});continue
        edits.append({'start':x,'end':y,'before':old,'after':before,'raw_fr_print':old})
    return edits,unresolved,ce.ratio()

def initial_projection(fr_d,fr_c,en):
    fc,ec,direct,anchors=align_math(fr_c,en)
    fpages=getpages(fr_c);dpages=getpages(fr_d)
    fkeys=[x['start'] for x in fc]
    variants=[];review=[];summary=collections.Counter()
    for p,cp in fpages.items():
        dp=dpages[p]; cs=uncomment(cp['text']);ds=uncomment(dp['text'])
        cms=mathchunks(cs);dms=mathchunks(ds)
        # The two French layers have matching math chunks in document order; sequence alignment catches insertions.
        sm=difflib.SequenceMatcher(None,[m['key'] for m in cms],[m['key'] for m in dms],autojunk=False)
        pairs=[]
        for op,a,b,k,l in sm.get_opcodes():
            if op=='equal':
                pairs.extend((a+j,k+j) for j in range(b-a))
            elif b-a==l-k:pairs.extend((a+j,k+j) for j in range(b-a))
            else:
                for ci in range(a,b):
                    cand=sorted([(difflib.SequenceMatcher(None,cms[ci]['key'],dms[di]['key'],autojunk=False).ratio(),di) for di in range(k,l)],reverse=True)
                    if cand and cand[0][0]>.55:pairs.append((ci,cand[0][1]))
                    else:review.append({'page':p,'reason':'unpaired French math chunk','corrected':cms[ci]['text']})
        for ci,di in pairs:
            cm,dm=cms[ci],dms[di]
            if cm['text']==dm['text']:continue
            if norm(cm['text'])==norm(dm['text']):
                # Spacing/typeface may still affect the reading; retained for separate audit.
                summary['same_search_signature']+=1
            cglobal=cp['start']+cm['start'];fi=bisect.bisect_left(fkeys,cglobal)
            eidx=direct.get(fi) if fi<len(fc) and fc[fi]['start']==cglobal else None
            confidence='exact math anchor'
            if eidx is None:
                pos=estimate(cglobal,anchors)
                cand=[(difflib.SequenceMatcher(None,cm['key'],m['key'],autojunk=False).ratio()-abs(m['start']-pos)/300000,j) for j,m in enumerate(ec) if abs(m['start']-pos)<4000]
                cand.sort(reverse=True)
                if not cand or cand[0][0]<.72:
                    review.append({'page':p,'reason':'English math chunk not aligned','diplomatic':dm['text'],'corrected':cm['text'],'estimated_position':pos});continue
                eidx=cand[0][1];confidence='local formula correspondence'
            em=ec[eidx]
            edits,unresolved,ratio=project_chunk(cm['text'],dm['text'],em['text'])
            for ed in edits:
                ed.update({'page':p,'expose':expose(p),'start':em['start']+ed['start'],'end':em['start']+ed['end'],'fr_diplomatic':dm['text'],'fr_corrected':cm['text'],'en_context':em['text'],'alignment':confidence,'ratio':ratio,'source':'fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex','kind':'print_correction'})
                variants.append(ed)
            if unresolved:review.append({'page':p,'reason':'projection partly unresolved','diplomatic':dm['text'],'corrected':cm['text'],'english':em['text'],'unresolved':unresolved})
            summary['changed_math_chunks']+=1
    return variants,review,{'fr_math_chunks':len(fc),'en_math_chunks':len(ec),'matching_chunks':len(direct),'anchors':len(anchors),'projection':dict(summary)},anchors

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--source-root',default='work/sources');ap.add_argument('--output',default='work/contributions/english');ap.add_argument('--complete',action='store_true',help='Build both English branches, alignment, glossary and per-row port audit from the final decision catalogues.');args=ap.parse_args()
    if args.complete:
        # The contribution modules use the archive-relative workspace layout
        # documented in EN_PREPARATION_README.md. No source or output is omitted.
        if args.source_root!='work/sources' or args.output!='work/contributions/english':
            raise ValueError('Complete preparation uses the documented archive-relative work layout.')
        import finalize_english,alignment_english,build_glossary,audit_english_port
        import subprocess,sys
        finalize_english.main()
        alignment_english.make()
        subprocess.run([sys.executable,str(Path(__file__).with_name('collect_glossary_additions.py'))],check=True)
        build_glossary.main()
        audit_english_port.main()
        return
    src=Path(args.source_root);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    frd=(src/'SGA5_FR'/FRD).read_text();frc=(src/'SGA5_FR'/FRC).read_text();en=(src/'SGA5_EN'/ENREL).read_text()
    variants,review,stats,anchors=initial_projection(frd,frc,en)
    (out/'projection_candidates.json').write_text(json.dumps(variants,ensure_ascii=False,indent=2))
    (out/'projection_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
    (out/'alignment_anchors.json').write_text(json.dumps(anchors))
    (out/'preparation_stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
    print(json.dumps({'variants':len(variants),'review':len(review),**stats}))
if __name__=='__main__':main()
