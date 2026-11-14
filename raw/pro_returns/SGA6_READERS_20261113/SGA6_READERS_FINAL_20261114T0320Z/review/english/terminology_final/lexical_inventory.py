#!/usr/bin/env python3
"""Reproducible lexical search views and source-linked terminology inventory.

All typography conversion is confined to a search view. No source file is
rewritten. Co-attestation is evidence for a lexical index, not a declaration
that every matched word is a semantically aligned translation token.
"""
from pathlib import Path
from collections import defaultdict, Counter
import csv, difflib, hashlib, json, re, unicodedata

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SNAP=HERE/'input_snapshots'
MARK=re.compile(r'%%%%%%%%%%\s+scan idx\s+\d+\s*\|\s*folio\s+(\S+)\s+%%%%%%%%%%')
MATH=re.compile(r'\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}.*?\\end\{\1\}|(?<!\\)\\\[.*?(?<!\\)\\\]|(?<!\\)\\\(.*?(?<!\\)\\\)|(?<!\\)\$(?:[^$]|\\\$)*?(?<!\\)\$',re.S)
ACCENTS={"'":'\u0301','`':'\u0300','^':'\u0302','"':'\u0308','~':'\u0303','c':'\u0327','=':'\u0304','v':'\u030c','u':'\u0306','H':'\u030b'}

def read(relative):return (SNAP/relative).read_text()

def pages(text):
    ms=list(MARK.finditer(text))
    return {m[1]:dict(text=text[m.end():ms[i+1].start() if i+1<len(ms) else len(text)],
                     offset=m.end(),order=i) for i,m in enumerate(ms)}

def tex_accents(s):
    s=s.replace('\\oe{}','œ').replace('\\OE{}','Œ').replace('\\ae{}','æ').replace('\\AE{}','Æ')
    s=re.sub(r"\\(['`^\"~=])\s*\{?([A-Za-z])\}?",lambda m:unicodedata.normalize('NFC',m[2]+ACCENTS[m[1]]),s)
    # Letter-named accent controls require their TeX token delimiter.  In
    # particular, neither \uline nor \clearpage is an accent invocation.
    s=re.sub(r"\\([cvuH])(?:\s+\{?|\{)([A-Za-z])\}?",lambda m:unicodedata.normalize('NFC',m[2]+ACCENTS[m[1]]),s)
    return s

def simple_math(m):
    s=m.group()
    for command,value in [('lambda','λ'),('gamma','γ'),('beta','β'),('alpha','α'),('tau','τ')]:
        if re.fullmatch(r'(?:\\\(|\$)\s*\\'+command+r'\s*(?:\\\)|\$)',s):return value
    if re.fullmatch(r'\\\(\s*(?:\\mathrm\{)?Tor\}?\s*\\\)',s):return 'Tor'
    # Lexical labels inside displays remain searchable; symbolic operands do not.
    words=re.findall(r'\\(?:text|textrm|textit|textbf|mbox)\{([^{}]*)\}',s)
    return ' '+ ' '.join(words)+' ' if words else ' '

def prose_view(s):
    s=re.sub(r'(?m)^\s*\\(?:newcommand|renewcommand|providecommand|def|gdef|long\\def)\b[^\n]*',' ',s)
    s=re.sub(r'(?<!\\)%[^\n]*',' ',s)
    s=re.sub(r'\\(?:sgaStableTarget(?:Inline)?|hypertarget|SGAPrintPage|SGAOriginalLeaf|label|ref|pageref|cite)\{[^{}]*\}', ' ',s)
    s=MATH.sub(simple_math,s)
    s=re.sub(r'\\(?:begin|end)\{[^{}]*\}(?:\[[^\]]*\])?', ' ',s)
    # Physical spacing dimensions are not lexical index labels.
    s=re.sub(r'\\(?:hspace|vspace)\*?\{[^{}]*\}', ' ',s)
    s=tex_accents(s)
    s=re.sub(r'\\hyperref\[[^\]]*\]', '',s)
    s=re.sub(r'\\(?:SGAAuthorFootnote|SGAAuthorFootText)\{[^{}]*\}', ' ',s)
    s=re.sub(r'\\(?:SGAAuthorFootMark)\{[^{}]*\}', ' ',s)
    s=re.sub(r'\\[A-Za-z@]+\*?', '',s)
    s=re.sub(r'\\[{}$%&#_]',' ',s)
    s=s.replace('\\',' ').replace('{','').replace('}','').replace('~',' ')
    s=s.replace('’',"'").replace('‘',"'").replace('``','"').replace("''",'"').replace('–','-').replace('—','-').replace('--','-')
    return re.sub(r'\s+',' ',unicodedata.normalize('NFC',s)).strip()

def term_view(s):
    # Plain glossary λ and a source \(\lambda\) are aliases only in this view.
    return prose_view(s).strip()

def match_term(text,term,notation=False):
    if not term:return []
    if notation:return list(re.finditer(re.escape(term)+r'(?![A-Za-z@])',text))
    left=r'(?<![^\W\d_])' if term[0].isalpha() else ''
    right=r'(?![^\W\d_])' if term[-1].isalpha() else ''
    # Preserve the source convention Module/Modules as its own surface form.
    flags=0 if re.search(r'\bModules?\b',term) else re.I
    return list(re.finditer(left+re.escape(term)+right,text,flags))

def fields(row):
    f=next((row[k] for k in ['french_term_or_notation','French term or notation','french','French','French_term'] if k in row),'')
    e=next((row[k] for k in ['english_rendering','English rendering','english','English','English_rendering'] if k in row),'')
    return f,e

def load_lexicon():
    cat=json.loads(read('review/english/aggregate/INPUT_CATALOG.json'))
    inputs=[('review/english/GLOSSARY_SGA6_REVIEWED_001_296.tsv','reviewed_prefix')]
    inputs += [(str(Path(p['directory'])/'terms.tsv'),'reviewed_contribution') for p in cat['packets']]
    inputs += [(str(p.relative_to(SNAP)), 'reference_glossary') for p in sorted((SNAP/'en/glossaries').glob('*.tsv'))]
    inputs += [('review/english/GLOSSARY_SGA6_CANDIDATES.tsv','earlier_unpaired_candidate')]
    lex={}
    for relative,kind in inputs:
        for line,row in enumerate(csv.DictReader((SNAP/relative).open(),delimiter='\t'),2):
            f,e=fields(row)
            if not f or not e:continue
            mixed_math=bool(MATH.search(f) and MATH.search(e) and not (MATH.fullmatch(f) and MATH.fullmatch(e)))
            notation=(f.startswith('\\') and e.startswith('\\')) or mixed_math
            fn,en=(f,e) if notation else (term_view(f),term_view(e))
            if not fn or not en:continue
            key=(fn,en)
            record=lex.setdefault(key,dict(French=fn,English=en,notation=notation,aliases_French=[],aliases_English=[],provenance=[]))
            if f not in record['aliases_French']:record['aliases_French'].append(f)
            if e not in record['aliases_English']:record['aliases_English'].append(e)
            record['provenance'].append(dict(path=relative,line=line,kind=kind,row=row))
    extra=HERE/'MANUAL_LEXICON.json'
    if extra.exists():
        for i,row in enumerate(json.loads(extra.read_text()),1):
            f,e=row['French'],row['English'];fn,en=term_view(f),term_view(e)
            record=lex.setdefault((fn,en),dict(French=fn,English=en,notation=False,aliases_French=[],aliases_English=[],provenance=[]))
            if f not in record['aliases_French']:record['aliases_French'].append(f)
            if e not in record['aliases_English']:record['aliases_English'].append(e)
            record['provenance'].append(dict(path='review/english/terminology_final/MANUAL_LEXICON.json',line=i,kind='reviewed_final_terminology',row=row))
    return list(lex.values())

def strip_nonbody(s):
    s=re.sub(r'(?m)^\s*\\(?:newcommand|renewcommand|providecommand|def|gdef|long\\def)\b[^\n]*',' ',s)
    return re.sub(r'(?<!\\)%[^\n]*',' ',s)

def main():
    fr=pages(read('build/FR_current_revised.tex'))
    english=read('review/english/aggregate/SGA6_EN_raw_current.tex')
    patch_file=HERE/'EN_TERMINOLOGY_PATCHES.jsonl'
    applications=[]
    if patch_file.exists():
        for line in patch_file.read_text().splitlines():
            row=json.loads(line);a=english.index(row['scope_start']);b=english.index(row['scope_end'],a)
            part=english[a:b];assert part.count(row['old'])==row['expected_count'],row['id']
            replacement=part.replace(row['old'],row['new'],row['expected_count'])
            assert [m.group() for m in MATH.finditer(part)]==[m.group() for m in MATH.finditer(replacement)]
            english=english[:a]+replacement+english[b:]
            applications.append(dict(id=row['id'],page=row['page'],expected_count=row['expected_count'],mathematical_units_identical=True))
    (HERE/'VIRTUAL_PATCH_APPLICATION.json').write_text(json.dumps(dict(input_sha256=hashlib.sha256(read('review/english/aggregate/SGA6_EN_raw_current.tex').encode()).hexdigest(),patched_sha256=hashlib.sha256(english.encode()).hexdigest(),applications=applications,shared_source_changed=False),indent=2)+'\n')
    en=pages(english)
    assert list(fr)==list(en) and len(fr)==720
    corpus=[]
    for page in fr:
        f,e=fr[page]['text'],en[page]['text']
        fm=list(MATH.finditer(f));em=list(MATH.finditer(e))
        sm=difflib.SequenceMatcher(None,[m.group() for m in fm],[m.group() for m in em],autojunk=False)
        matches=[]
        for block in sm.get_matching_blocks():
            for j in range(block.size):matches.append((fm[block.a+j],em[block.b+j]))
        segments=[];fp=ep=0
        for a,b in matches:
            fs,es=f[fp:a.start()],e[ep:b.start()]
            fv,ev=prose_view(fs),prose_view(es)
            if fv or ev:segments.append(dict(French_start=fp,French_end=a.start(),English_start=ep,English_end=b.start(),French_view=fv,English_view=ev))
            fp,ep=a.end(),b.end()
        fv,ev=prose_view(f[fp:]),prose_view(e[ep:])
        if fv or ev:segments.append(dict(French_start=fp,French_end=len(f),English_start=ep,English_end=len(e),French_view=fv,English_view=ev))
        corpus.append(dict(page=page,order=fr[page]['order'],French_view=prose_view(f),English_view=prose_view(e),French_offset=fr[page]['offset'],English_offset=en[page]['offset'],French_notation_view=strip_nonbody(f),English_notation_view=strip_nonbody(e),segments=segments))
    (HERE/'SEARCH_CORPUS.json').write_text(json.dumps(corpus,ensure_ascii=False,indent=2)+'\n')
    lex=load_lexicon();attested=[];unattested=[]
    for row in lex:
        f,e,n=row['French'],row['English'],row['notation']
        hits=[];interval_hits=[]
        for p in corpus:
            fv,ev=(p['French_notation_view'],p['English_notation_view']) if n else (p['French_view'],p['English_view'])
            fs,es=match_term(fv,f,n),match_term(ev,e,n)
            if fs and es:
                hits.append(dict(page=p['page'],French_count=len(fs),English_count=len(es),French_context=fv[max(0,fs[0].start()-120):fs[0].end()+180],English_context=ev[max(0,es[0].start()-120):es[0].end()+180]))
                if not n:
                    for j,seg in enumerate(p['segments']):
                        a,b=match_term(seg['French_view'],f),match_term(seg['English_view'],e)
                        if a and b:interval_hits.append(dict(page=p['page'],segment=j,pair_count=min(len(a),len(b)),French=seg['French_view'],English=seg['English_view']))
        row.update(paired_page_attestations=hits,paired_page_English_count=sum(x['English_count'] for x in hits),paired_page_French_count=sum(x['French_count'] for x in hits),formula_bounded_interval_attestations=interval_hits,formula_bounded_pair_count=sum(x['pair_count'] for x in interval_hits))
        (attested if hits else unattested).append(row)
    (HERE/'LEXICON_ATTESTATIONS.json').write_text(json.dumps(attested,ensure_ascii=False,indent=2)+'\n')
    (HERE/'LEXICON_UNATTESTED.json').write_text(json.dumps(unattested,ensure_ascii=False,indent=2)+'\n')
    grouped=defaultdict(list)
    for r in attested:grouped[r['French'].casefold()].append(r)
    rows=[]
    for k,group in sorted(grouped.items()):
        alternatives={r['English'].casefold() for r in group}
        if len(alternatives)>1:
            rows.append(dict(French=' / '.join(dict.fromkeys(r['French'] for r in group)),English=' ; '.join(dict.fromkeys(r['English'] for r in group)),counts=' ; '.join(str(r['paired_page_English_count']) for r in group),first_pages=' ; '.join(r['paired_page_attestations'][0]['page'] for r in group),interval_counts=' ; '.join(str(r['formula_bounded_pair_count']) for r in group)))
    with (HERE/'REVIEW_QUEUE.tsv').open('w') as out:
        w=csv.DictWriter(out,fieldnames=['French','English','counts','first_pages','interval_counts'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    stats=dict(lexicon_pairs=len(lex),attested_pairs=len(attested),unattested_pairs=len(unattested),multiple_rendering_groups=len(rows),pages=len(corpus),formula_bounded_prose_intervals=sum(len(x['segments']) for x in corpus))
    (HERE/'LEXICAL_INVENTORY_COUNTS.json').write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps(stats))

if __name__=='__main__':main()
