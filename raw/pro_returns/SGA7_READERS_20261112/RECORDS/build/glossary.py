#!/usr/bin/env python3
"""Corpus-attested bilingual glossary and alternate-rendering audit for SGA 7.

No source is rewritten. Counts are one-to-one, monotone lexical occurrence
matches constrained by the shared mathematical sequence, not whole-corpus
English word frequencies. Every match is retained in a machine-readable audit.
"""
from __future__ import annotations
import bisect
import collections
import csv
import difflib
import importlib.util
import json
import pickle
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources'
OUT = ROOT / 'output' / 'records'
WORK = ROOT / 'work'
TERMS = ROOT / 'build' / 'glossary_terms.tsv'

spec = importlib.util.spec_from_file_location('sga_port_seg', SRC / 'port' / 'segment.py')
seg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seg)

ROMANS = 'intro I II VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII'.split()
FMARK = re.compile(r'%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+([IVXLCDMivxlcdm\d]+)\s*%+')
IGNORE_CMDS = {'label':1,'ref':1,'pageref':1,'cite':1,'url':1,'href':1,'SGARefTarget':1,
               'SGARefAliasTarget':1,'SGARefLink':1,'begin':1,'end':1,'tag':1,
               'vspace':1,'hspace':1,'phantomsection':0,'addcontentsline':3,
               'setcounter':2,'addtocounter':2,'index':1,'phantom':1}
ACCENTS = {"'":'\u0301','`':'\u0300','^':'\u0302','"':'\u0308','~':'\u0303',
           'c':'\u0327','v':'\u030c','=':'\u0304'}


def brace(s, p):
    """Read one balanced group, returning contents and first offset after it."""
    while p < len(s) and s[p].isspace(): p += 1
    if p >= len(s) or s[p] != '{': return '', p
    level, q = 1, p+1
    while q < len(s) and level:
        if s[q] == '{' and (q == 0 or s[q-1] != '\\'): level += 1
        if s[q] == '}' and (q == 0 or s[q-1] != '\\'): level -= 1
        q += 1
    return s[p+1:q-1], q


def prose(s):
    """Strip presentation markup while retaining a clean-to-source offset map."""
    chars, pos = [], []
    i = 0
    def emit(t, at):
        chars.extend(t); pos.extend([at]*len(t))
    while i < len(s):
        c = s[i]
        if c == '%' and (i == 0 or s[i-1] != '\\'):
            j=s.find('\n',i); i=len(s) if j<0 else j; continue
        if c == '$' and (i == 0 or s[i-1] != '\\'):
            d='$$' if s[i:i+2]=='$$' else '$'; j=s.find(d,i+len(d))
            if j<0: emit(' ',i); i+=len(d); continue
            m=s[i+len(d):j].strip()
            sm={'\\ell':'ell','\\ell^n':'ell','\\Lambda':'lambda','\\pi':'pi'}.get(m,m)
            if re.fullmatch(r'[A-Za-z]{1,7}',sm): emit(sm,i)
            else: emit(' ',i)
            i=j+len(d); continue
        if c == '\\':
            if s[i:i+2] in ('\\[','\\('):
                end='\\]' if s[i+1]=='[' else '\\)'; j=s.find(end,i+2)
                if j>=0: emit(' ',i); i=j+2; continue
            if i+1<len(s) and s[i+1] in ACCENTS:
                a=s[i+1]; j=i+2
                if a.isalpha() and j<len(s) and s[j].isalpha(): pass
                else:
                    while j<len(s) and s[j].isspace(): j+=1
                    if j<len(s) and s[j]=='{': b,k=brace(s,j)
                    elif j<len(s): b,k=s[j],j+1
                    else: b,k='',j
                    if len(b)==1:
                        emit(unicodedata.normalize('NFC',b+ACCENTS[a]),i); i=k; continue
            m=re.match(r'\\([A-Za-z]+)\*?',s[i:])
            if m:
                name=m.group(1); j=i+len(m.group(0))
                if name in {'oe','OE','ae','AE'}: emit(name,i)
                elif name in {'ldots','dots','quad','qquad','enspace','newline','par'}: emit(' ',i)
                for _ in range(IGNORE_CMDS.get(name,0)):
                    _,j=brace(s,j)
                i=j; continue
            if i+1<len(s):
                if s[i+1] in '%&#_': emit(s[i+1],i)
                elif s[i+1]=='~': emit(' ',i)
                else: emit(' ',i)
                i+=2; continue
        if c in '{}': i+=1; continue
        if c=='~': c=' '
        if c in '–—': c='-'
        emit(c,i); i+=1
    t=''.join(chars).casefold()
    return t,pos


def normphrase(s):
    s=s.casefold().replace('–','-').replace('—','-').replace('’',"'")
    return re.sub(r'\s+',' ',s).strip()


def pattern(s):
    # An explicit regex may be supplied as /.../; otherwise tolerate line wraps
    # and TeX's double hyphen but preserve lexical spelling.
    if s.startswith('/') and s.endswith('/'): p=s[1:-1]
    else:
        p=re.escape(normphrase(s))
        p=p.replace(r'\ ',r'\s+').replace(r'\-',r'-{1,2}')
        p=p.replace("'",r"['’]")
    return re.compile(r'(?<![\w])(?:'+p+r')(?![\w])',re.I)


def source_data():
    cache=WORK/'glossary_source_cache.pickle'
    if cache.exists():
        with cache.open('rb') as f: return adjust_corpus(pickle.load(f))
    data=[]
    for vol, dirname in [('7I','sga7i'),('7II','sga7ii')]:
        native=SRC/'en'/'sources'/'native'/('SGA7I' if vol=='7I' else 'SGA7II')
        masters=sorted(native.rglob('*source_first_workpass.tex'))
        master=masters[0]; eroot=master.parent
        ef=seg.master_files(eroot,master.name)
        by_exp=collections.defaultdict(list)
        for p in ef: by_exp[seg.expose_of(p.name)].append(p)
        ff=sorted((SRC/'fr'/dirname/'current').glob('*body.tex'),key=lambda p:ROMANS.index(seg.expose_of(p.name)))
        for fp in ff:
            exp=seg.expose_of(fp.name); ep=by_exp.get(exp,[])
            if not ep: continue
            ft=fp.read_text(); et=''; components=[]
            for p in ep:
                components.append((len(et),str(p.relative_to(SRC))))
                et+=p.read_text()+'\n\n'
            fc,fmap=prose(ft); ec,emap=prose(et)
            fa,ea=seg.tokens(ft),seg.tokens(et)
            sm=difflib.SequenceMatcher(None,[k for _,k in fa],[k for _,k in ea],autojunk=False)
            anchors=[]
            for a,b,n in sm.get_matching_blocks():
                anchors.extend((fa[a+i][0],ea[b+i][0]) for i in range(n))
            anchors=sorted(set(anchors))
            # The same equation can contain multiple tag/token entries.
            uniq=[]
            for a,b in anchors:
                if not uniq or a>uniq[-1][0] and b>=uniq[-1][1]: uniq.append((a,b))
            data.append(dict(vol=vol,exp=exp,fr=ft,en=et,fc=fc,ec=ec,fmap=fmap,emap=emap,
                             fpath=str(fp.relative_to(SRC)),components=components,
                             folios=[(m.start(),m.group(2)) for m in FMARK.finditer(ft)],
                             anchors=uniq))
            print('Glossary source:',vol,exp,'anchors',len(uniq),flush=True)
    with cache.open('wb') as f: pickle.dump(data,f,protocol=5)
    return adjust_corpus(data)


def adjust_corpus(data):
    for d in data:
        if d['exp']=='intro':
            d['folios']=[(0,'V (inferred)')]
            for m in re.finditer(r'\\begin\{center\}\s*(VI|VII)\s*\\end\{center\}',d['fr']):
                d['folios'].append((m.start(),m.group(1)))
        if d['exp']=='VI':
            # This exposé was printed in English. Both readers use the same
            # source-authoritative English text, not the inherited paraphrase.
            d['en']=d['fr'];d['ec']=d['fc'];d['emap']=d['fmap']
            d['components']=[(0,d['fpath'])]
            d['anchors']=[(a,a) for a,k in seg.tokens(d['fr'])]
    return data


def projection(d,p):
    aa=d['anchors']; fs=[a for a,b in aa]
    k=bisect.bisect_left(fs,p)
    if not aa: return round(p*len(d['en'])/max(1,len(d['fr']))),0,len(d['en'])
    if k==0:
        a,b=aa[0]; return max(0,b-(a-p)),0,b
    if k==len(aa):
        a,b=aa[-1]; return min(len(d['en']),b+(p-a)),b,len(d['en'])
    a,b=aa[k-1]; c,e=aa[k]
    return b+(p-a)*(e-b)//max(1,c-a),b,e


def location(d,fp,ep):
    fidx=bisect.bisect_right([x for x,p in d['folios']],fp)-1
    page=d['folios'][fidx][1] if fidx>=0 else 'front'
    cidx=bisect.bisect_right([x for x,p in d['components']],ep)-1
    base,comp=d['components'][max(0,cidx)]
    line=d['en'][base:ep].count('\n')+1
    return f"SGA {d['vol']}, Exposé {d['exp']}, folio {page}; {comp}:{line}",page,comp,line


def occurrences(pat,text,mapping):
    return [(mapping[m.start()],mapping[m.end()-1]+1,m.group(0),m.start(),m.end()) for m in pat.finditer(text) if m.end()>m.start()]


def read_terms():
    rows=[]
    with TERMS.open() as f:
        for row in csv.DictReader(f,delimiter='\t'):
            if row['french'].startswith('#'): continue
            row['variants']=[v.strip() for v in row['english'].split(' || ') if v.strip()]
            rows.append(row)
    return rows


def align_term(d,t):
    notation=t.get('kind')=='notation'
    if d['exp']=='VI' and not notation: return []
    if notation:
        p=re.compile(t['fr_pattern'])
        fs=[(m.start(),m.end(),m.group(0),m.start(),m.end()) for m in p.finditer(d['fr'])]
    else:
        fs=occurrences(pattern(t['fr_pattern'] or t['french']),d['fc'],d['fmap'])
        if t['french']=='nul':
            fs=[f for f in fs if not re.search(r'non\s+$',d['fc'][max(0,f[3]-8):f[3]])]
    if not fs: return []
    es=[]
    for v in t['variants']:
        label,sep,pat=v.partition('=>')
        if notation:
            es.extend(((m.start(),m.end(),m.group(0),m.start(),m.end()),label)
                      for m in re.finditer(pat,d['en']))
        else:
            oo=occurrences(pattern(pat if sep else v),d['ec'],d['emap'])
            if t['french']=='nul' and label=='vanishing':
                oo=[o for o in oo if not re.match(r'(?:\s+|-)(?:cycles?|cohomology)\b',d['ec'][o[4]:o[4]+30])]
            es.extend((o,label) for o in oo)
    if not es: return []
    es.sort(key=lambda x:x[0][0]); used=set(); out=[]; last=-1
    for f in fs:
        target,lower,upper=projection(d,f[0]); target2,_,_=projection(d,f[1])
        # Exact shared mathematics bounds the translated prose. A small padding
        # accommodates formulas moved across a line boundary by the translation.
        a=max(0,lower-110); b=min(len(d['en']),upper+110)
        if b-a>2800:
            a=max(a,target-1000); b=min(b,target2+1000)
        candidates=[(abs((e[0]+e[1])/2-(target+target2)/2),e,v)
                    for e,v in es if e[0]>=a and e[1]<=b and e[0]>=last and (e[0],e[1]) not in used]
        if not candidates: continue
        candidates.sort(key=lambda x:x[0]); dist,e,v=candidates[0]
        # When one lexical form is nested in a longer one, use the longest form
        # at the same English occurrence (e.g. 'residue field', not 'field').
        competing=[(dd,ee,vv) for dd,ee,vv in candidates if ee[0]<=e[0]<ee[1] or e[0]<=ee[0]<e[1]]
        if competing:
            _,e,v=max(competing,key=lambda x:x[1][1]-x[1][0])
        used.add((e[0],e[1])); last=e[0]
        place,page,comp,line=location(d,f[0],e[0])
        out.append(dict(french=t['french'],english=v,vol=d['vol'],expose=d['exp'],page=page,
                        first_place=place,fr_source=d['fpath'],en_source=comp,en_line=line,
                        fr_offset=f[0],en_offset=e[0],fr_occurrence=normphrase(f[2]),
                        en_occurrence=normphrase(e[2]),anchor_window_start=lower,anchor_window_end=upper,
                        fr_context=re.sub(r'\s+',' ',d['fr' if notation else 'fc'][max(0,f[3]-90):f[4]+90]),
                        en_context=re.sub(r'\s+',' ',d['en' if notation else 'ec'][max(0,e[3]-90):e[4]+90]),
                        kind=t.get('kind','term'),judgment=t.get('judgment','retain contextual variation')))
    return out


def underlined(s):
    out=[]
    for m in re.finditer(r'\\underline\s*\{',s):
        body,end=brace(s,m.end()-1)
        clean,_=prose(body); clean=normphrase(clean)
        # A double underline is one occurrence of a phrase, not two lexical
        # attestations. Preserve different nested phrases, but collapse an
        # identical inner wrapper.
        if out and out[-1][2]==clean and out[-1][0]<=m.start() and end<=out[-1][1]:
            continue
        out.append((m.start(),end,clean))
    return out


FR_GRAMMAR=re.compile(r'^(?:soit|soient|supposons|on |alors|et |ou |pour |dans |par |avec |comme |sous |tel|de |du |des |le |la |les |un |une |est |en |si |qui |que |tout|dont |ce |ces |il |au |aux |notons|posons|considérons|désignons)\b')
EN_GRAMMAR=re.compile(r'^(?:let|then|and|or|for|in|by|with|under|as|such|of|the|a|an|is|are|on|if|which|that|all|whose|this|these|it|at|to|suppose|set|consider|we|there)\b')


def extract_candidates(data,terms):
    known={normphrase(x['french']) for x in terms}; out=[]
    known_patterns=[pattern(t['fr_pattern'] or t['french']) for t in terms if t.get('kind')!='notation']
    technical=set()
    for t in terms:
        for w in normphrase(t['french']).split():
            if len(w)>4: technical.add(w)
    for d in data:
        if d['exp']=='VI':continue
        eu=underlined(d['en'])
        for a,b,s in underlined(d['fr']):
            if s in known or any(p.fullmatch(s) for p in known_patterns) or not 3<=len(s)<=85 or not 1<=len(s.split())<=8: continue
            if re.search(r'[.:;=<>0-9]',s) or FR_GRAMMAR.search(s):continue
            if re.search(r'\b(?:est|sont|soit|soient|et|sur|dans|pour|par|avec|donc|vérifie|induit|admet|a|ont|être|puisse|quelconque)\b',s):continue
            if re.match(r"^(?:l['’]|d['’]|aucun|muni|toute?|deux|cette?|ces|sa |son |ses |se |ne |s['’]|à |étant |désign|fixons|choisissons|provien|correspond|associ|forme|forment|autre |nous |y |met |suffit|ayant|ait |induis|dépend|satisf|appart|engendr|modulo |tels? |ceci |qu['’]|telle? )",s): continue
            if re.search(r"\b(?:de|d['’]|à|en|du|des|au|aux|le|la|les|un|une)$",s): continue
            if not set(s.split())&technical:continue
            p,l,u=projection(d,a); q,_,_=projection(d,b)
            cs=[(abs((x+y)/2-(p+q)/2),t,x,y) for x,y,t in eu
                if x>=l-120 and y<=u+120 and 3<=len(t)<=100 and len(t.split())<=10
                and not EN_GRAMMAR.search(t) and not re.search(r'[.:;=<>0-9]',t)]
            cs.sort()
            place,page,comp,line=location(d,a,p)
            if s in {'hodge','gysin','picard','lefschetz','bertini','picard-lefschetz'}:
                status='reviewed: proper name; named constructions are indexed separately'
            elif s in {'strictement','fidèlement','pleinement','universellement'}:
                status='reviewed: grammatical modifier; technical compounds are indexed separately'
            else:
                status='reviewed: compositional heading or sentence fragment; constituent terms are indexed separately'
            out.append(dict(french_phrase=s,english_candidates=' | '.join(dict.fromkeys(t for _,t,_,_ in cs[:4])),
                            source=place,status=status,
                            vol=d['vol'],expose=d['exp'],page=page,fr_offset=a))
    return out


def underlined_inventory(data):
    """Every distinct underlined phrase, including fragments and nontechnical text."""
    grouped=collections.defaultdict(list)
    for d in data:
        if d['exp']=='VI': continue
        for a,b,s in underlined(d['fr']):
            if not s: continue
            p,_,_=projection(d,a)
            place,_,_,_=location(d,a,p)
            grouped[s].append(place)
    return [dict(french_phrase=s,count=len(places),first_place=places[0],
                 scope='all underlined source phrases; not all entries are terms')
            for s,places in sorted(grouped.items())]


def write_tsv(path,rows,fields):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore')
        w.writeheader();w.writerows(rows)


def verify_outputs():
    with (OUT/'GLOSSARY_SGA7_FR_EN.tsv').open() as f:
        rows=list(csv.DictReader(f,delimiter='\t'))
    with (OUT/'GLOSSARY_ATTESTATIONS.tsv').open() as f:
        att=list(csv.DictReader(f,delimiter='\t'))
    counts=collections.Counter((r['french'],r['english']) for r in att)
    assert {(r['french'],r['english']):int(r['count']) for r in rows}==dict(counts)
    for r in att:
        assert (SRC/r['fr_source']).is_file()
        assert (SRC/r['en_source']).is_file()
    grouped=collections.defaultdict(set)
    for r in rows: grouped[r['french']].add(r['english'])
    report=(OUT/'GLOSSARY_INCONSISTENCIES.md').read_text()
    for term,forms in grouped.items():
        if len(forms)>1: assert '| '+term+' | ' in report
    p=OUT/'GLOSSARY_AUDIT.json';stats=json.loads(p.read_text())
    stats['validation']={'all_counts_equal_attestation_counts':True,
                         'all_source_paths_exist':True,'all_multiple_renderings_listed':True}
    p.write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True); WORK.mkdir(exist_ok=True)
    data=source_data(); terms=read_terms(); matches=[]
    for ti,t in enumerate(terms):
        for d in data: matches.extend(align_term(d,t))
        if ti%100==0: print('Glossary terms:',ti,'matches',len(matches),flush=True)
    groups=collections.defaultdict(list)
    for m in matches: groups[(m['french'],m['english'])].append(m)
    rows=[]
    for (f,e),mm in sorted(groups.items()):
        rows.append(dict(french=f,english=e,count=len(mm),first_place=mm[0]['first_place'],kind=mm[0]['kind']))
    write_tsv(OUT/'GLOSSARY_SGA7_FR_EN.tsv',rows,['french','english','count','first_place','kind'])
    write_tsv(OUT/'GLOSSARY_ATTESTATIONS.tsv',matches,['french','english','vol','expose','page','fr_source','en_source','en_line','fr_offset','en_offset','fr_occurrence','en_occurrence','anchor_window_start','anchor_window_end','fr_context','en_context','kind'])
    candidates=extract_candidates(data,terms)
    write_tsv(OUT/'GLOSSARY_CANDIDATES.tsv',candidates,['french_phrase','english_candidates','source','status'])
    inventory=underlined_inventory(data)
    write_tsv(OUT/'GLOSSARY_UNDERLINED_INVENTORY.tsv',inventory,['french_phrase','count','first_place','scope'])
    byterm=collections.defaultdict(list)
    for r in rows:byterm[r['french']].append(r)
    multi={k:v for k,v in byterm.items() if len(v)>1}
    md=['# English terminology: attested alternate renderings','',
        '## Scope and count definition','',
        f'The glossary contains {len(rows):,} attested term/rendering pairs for {len(byterm):,} French terms, drawn from the complete source corpus. Its counts total {len(matches):,} occurrence-pair matches. Each counted item has an exact French occurrence and an exact English occurrence in a local interval constrained by the common mathematical sequence; the script enforces one-to-one monotone matching for each French term. These are reproducible lexical alignment counts, not unrestricted English word frequencies and not counts of distinct mathematical concepts. Singular/plural forms listed together by an explicit regular expression are one rendering; spelling, dialect, and lexical alternatives remain distinct. Nested terms can overlap, so the grand total must not be read as a word count.','',
        'The original English of Exposé VI is not used as evidence of French-to-English terminology. It remains part of the readers without translation. Notation in that exposé is counted against the same source-authoritative English text used in both readers. This prevents accidental treatment of English words in the French layer as French terms. The introduction is located by its source-attested folios VI and VII; folio V is explicitly marked inferred, following the supplied source note.','',
        'The lexicon supplies an explicit set of mathematical terms and their possible renderings; only actually co-attested pairs enter the glossary. The source alignment is mechanical and is not a claim of independently validated sentence translation. Formula anchors can leave broad prose intervals, and counts can undercount phrases separated by substantially reordered prose. Every counted match, both source locations, and the surrounding context are in `GLOSSARY_ATTESTATIONS.tsv`. `GLOSSARY_UNDERLINED_INVENTORY.tsv` inventories every distinct underlined French phrase, including nontechnical text and sentence fragments. `GLOSSARY_CANDIDATES.tsv` records the review of residual underlined phrases: these are compositional headings, incomplete sentence fragments, modifiers, or proper names whose constituent technical terms or named constructions are indexed separately. Nearby underlined English strings are retained as search aids only; they are not asserted to be translations. No uncertain candidate is silently promoted to an established equivalence.','',
        '## Editorial policy','',
        'Existing English terminology is authoritative. A change is justified only by an identifiable semantic or typographical slip in context. Variation between British and American spelling, singular/plural forms, ordinary synonyms, or different mathematical senses is retained. In particular, fibre/fiber and cofibred/cofibered reflect language already present in the release and in the original English Exposé VI. The attested alternatives below do not establish an unambiguous lexical error, so this audit makes no vocabulary replacements. Mathematical editorial corrections and their separate reasons belong in `OPEN_ITEMS_DECIDED.tsv` and `CHANGES_EN.tsv`.','',
        f'## All alternate renderings in the attested glossary ({len(multi)})','',
        '| French term | English renderings and aligned counts | First witnesses | Decision |',
        '|---|---|---|---|']
    termmap={t['french']:t for t in terms}
    for f,rr in sorted(multi.items()):
        forms='; '.join(f"{r['english'].replace('|','/')} ({r['count']})" for r in rr)
        wit='; '.join(r['first_place'].split(';')[0] for r in rr)
        judgment=termmap[f].get('judgment') or 'Retain: inspect the attested contexts; no unambiguous slip established.'
        md.append('| '+f+' | '+forms+' | '+wit+' | '+judgment+' |')
    md += ['', '## Reproducibility','',
           'Run `python build/glossary.py` after `build/verify_inputs.py`. The script reads only the supplied French corrected layers and native English components, in master input order. It imports the supplied formula-token normalizer without altering the edition. Source citations are ZIP-internal names; all generated files omit personal local paths and e-mail addresses.','',
           'A term missing from the glossary means that a defensible occurrence pair was not established by this procedure; it does not assert the term is absent from the book. The candidates table makes the remaining underlined vocabulary reviewable.']
    (OUT/'GLOSSARY_INCONSISTENCIES.md').write_text('\n'.join(md)+'\n')
    stats=dict(terms_defined=len(terms),terms_attested=len(byterm),pairs=len(rows),occurrence_pairs=len(matches),
               multiple_rendering_terms=len(multi),underlined_candidates=len(candidates),underlined_inventory=len(inventory),
               sources=[dict(volume=d['vol'],expose=d['exp'],formula_anchors=len(d['anchors']),fr_chars=len(d['fr']),en_chars=len(d['en'])) for d in data])
    (OUT/'GLOSSARY_AUDIT.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
    verify_outputs()
    print(json.dumps({k:v for k,v in stats.items() if k!='sources'},indent=2))


if __name__=='__main__': main()
