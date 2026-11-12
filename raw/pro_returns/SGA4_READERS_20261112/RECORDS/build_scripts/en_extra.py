"""Source-backed English correction port and its per-record audit."""
from en_common import *
import collections, unicodedata
from functools import lru_cache

SYMBOLS={
 '∅':r'\varnothing','∈':r'\in','∉':r'\notin','⊂':r'\subset','⊆':r'\subseteq',
 '⊃':r'\supset','⊇':r'\supseteq','≤':r'\leq','≥':r'\geq','≠':r'\neq',
 '≃':r'\simeq','≅':r'\cong','≡':r'\equiv','×':r'\times','∏':r'\prod',
 '∐':r'\coprod','∑':r'\sum','∞':r'\infty','∩':r'\cap','∪':r'\cup',
 '→':r'\rightarrow','⟶':r'\rightarrow','←':r'\leftarrow','⟵':r'\leftarrow',
 '↦':r'\mapsto','⟼':r'\mapsto','∘':r'\circ','·':r'\cdot','∗':r'\ast',
 'α':r'\alpha','β':r'\beta','γ':r'\gamma','δ':r'\delta','ε':r'\epsilon',
 'ζ':r'\zeta','η':r'\eta','θ':r'\theta','ι':r'\iota','κ':r'\kappa',
 'λ':r'\lambda','μ':r'\mu','ν':r'\nu','ξ':r'\xi','π':r'\pi','ρ':r'\rho',
 'σ':r'\sigma','τ':r'\tau','υ':r'\upsilon','φ':r'\phi','ϕ':r'\varphi',
 'χ':r'\chi','ψ':r'\psi','ω':r'\omega','Γ':r'\Gamma','Δ':r'\Delta',
 'Θ':r'\Theta','Λ':r'\Lambda','Ξ':r'\Xi','Π':r'\Pi','Σ':r'\Sigma',
 'Υ':r'\Upsilon','Φ':r'\Phi','Ψ':r'\Psi','Ω':r'\Omega',
 'ℋ':r'\mathcal{H}','ℰ':r'\mathcal{E}','ℱ':r'\mathcal{F}',
 'ℬ':r'\mathcal{B}','ℒ':r'\mathcal{L}','ℳ':r'\mathcal{M}',
 'ℛ':r'\mathcal{R}','℘':r'\mathcal{P}',
}
for cp in range(0x1d400,0x1d800):
    c=chr(cp);n=unicodedata.name(c,'')
    if n.startswith('MATHEMATICAL SCRIPT CAPITAL '):
        letter=n.rsplit(' ',1)[-1]
        if len(letter)==1:SYMBOLS[c]=r'\mathcal{'+letter+'}'
    elif n.startswith('MATHEMATICAL BOLD SMALL '):
        letter=n.rsplit(' ',1)[-1]
        if len(letter)==1:SYMBOLS[c]=r'\mathbf{'+letter.lower()+'}'

ALIASES={r'\to':r'\rightarrow',r'\longrightarrow':r'\rightarrow',r'\longleftarrow':r'\leftarrow',
 r'\emptyset':r'\varnothing',r'\le':r'\leq',r'\leqslant':r'\leq',r'\ge':r'\geq',r'\geqslant':r'\geq',
 r'\longmapsto':r'\mapsto',r'\ast':r'\ast',r'\PP':'P'}
ALIASES[r'\varprojlim']='lim'+r'\leftarrow'
ALIASES[r'\varinjlim']='lim'+r'\rightarrow'
for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':ALIASES['\\'+c+c.lower()]=r'\mathcal{'+c+'}'
for name in ['Hom','ob','Ob','Ker','Coker','Spec','Ext','Tor','Im','card','lim']:
    ALIASES['\\'+name]=name

def compact(s):
    """Return exact token-equivalence key and a map back to every source byte.

    Only explicit macro/glyph expansions listed above and TeX whitespace are
    used; the original matched spelling is retained in each reader branch.
    """
    out=[];mapping=[];i=0
    while i<len(s):
        if s[i].isspace():i+=1;continue
        if s[i]=='%':
            j=s.find('\n',i);i=len(s) if j<0 else j+1;continue
        if s.startswith(r'\SGApage',i):
            j=i+len(r'\SGApage')
            try:
                for _ in range(3):_,_,j,_=group(s,j)
                i=j;continue
            except ValueError:pass
        if s[i]=='\\':
            m=re.match(r'\\[A-Za-z@]+|\\.',s[i:]);tok=m.group() if m else '\\';j=i+len(tok)
            val=ALIASES.get(tok,tok)
        else:
            j=i+1;val=SYMBOLS.get(s[i],s[i])
            if s[i]=='*':val=r'\ast'
        out.extend(val);mapping.extend([(i,j)]*len(val));i=j
    text=''.join(out)
    # A one-token TeX group is mapped to that token, with the complete raw
    # group retained in the offset map: x_{i} and x_i have the same tokens
    # consumed by the subscript primitive. No multi-token group is removed.
    single=re.compile(r'(?<!\\)\{([^{}\\]|\\[A-Za-z@]+|\\.)\}')
    while True:
        groups=list(single.finditer(text))
        if not groups:break
        for g in reversed(groups):
            a,b=g.span();inner=g.group(1);whole=(mapping[a][0],mapping[b-1][1])
            text=text[:a]+inner+text[b:]
            mapping=mapping[:a]+[whole]*len(inner)+mapping[b:]
    return text,mapping

@lru_cache(maxsize=16384)
def key(s):
    return compact(s)[0]

def pure_math(s):
    x=re.sub(r'\\(?:[A-Za-z@]+|.)','',s)
    x=re.sub(r'\b(?:Hom|Ob|ob|Ker|Coker|Spec|Ext|Tor|Im|lim|card|top|mod)\b','',x)
    x=re.sub(r'[0-9A-Za-zΑ-ω𝒜-𝒵ℋℒℰℱℳℛ]', 'x',x)
    return not re.search(r'x{2,}',x) and not re.search('[àâäéèêëîïôöùûüç…]',s,re.I) and '^_' not in s

def balanced(s,check_dollars=True):
    dep=0
    for m in re.finditer(r'\\.|[{}]',s):
        if m.group()=='{':dep+=1
        if m.group()=='}':dep-=1
        if dep<0:return False
    return dep==0 and (not check_dollars or len(re.findall(r'(?<!\\)\$',s))%2==0)

def carry_original_pages(old,new):
    from marker_projection import carry_markers
    pattern=re.compile(r'\\SGApage\{(\d)\}\{([^}]+)\}\{(\d+)\}')
    markers={r'\SGApageno{'+m.group(1)+'}{'+m.group(3)+'}':m.group() for m in pattern.finditer(old)}
    if not markers:return new
    def temporary(t):return pattern.sub(lambda m:r'\SGApageno{'+m.group(1)+'}{'+m.group(3)+'}',t)
    out=carry_markers(temporary(old),temporary(new))
    for interim,real in markers.items():out=out.replace(interim,real)
    assert set(pattern.findall(old))<=set(pattern.findall(out)),('page marker lost in English pair',old,new)
    return out

def candidates(old,new):
    old=old.strip();new=new.strip()
    if old.startswith('$') and old.endswith('$') and old.count('$')==2:old=old[1:-1]
    if new.startswith('$') and new.endswith('$') and new.count('$')==2:new=new[1:-1]
    out=[]
    if old==new:return out
    def math_evidence(x):
        return bool(re.search(r'\\|[$_^\d=<>+\-/∈∉⊂⊆≤≥≠→←{}()]',x)) or bool(re.fullmatch(r"[A-Za-z]'?",x))
    if pure_math(old) and pure_math(new) and balanced(old) and balanced(new) and math_evidence(old) and math_evidence(new):out.append((old,new,'full mathematical reading'))
    om=re.findall(r'(?<!\\)\$(?!\$)(.*?)(?<!\\)\$',old,re.S)
    nm=re.findall(r'(?<!\\)\$(?!\$)(.*?)(?<!\\)\$',new,re.S)
    if len(om)==len(nm):
        for a,b in zip(om,nm):
            if a!=b and balanced(a) and balanced(b):out.append((a,b,'paired mathematical expression'))
    if len(om)==1 and pure_math(new) and balanced(new):out.append((om[0],new,'one mathematical expression in prose'))
    if len(nm)==1 and pure_math(old) and balanced(old):out.append((old,nm[0],'one mathematical expression in prose'))
    # Full TeX source snippets sometimes contain a French context surrounding
    # one mathematical token. Grow the exact changed span to balanced groups.
    sm=difflib.SequenceMatcher(None,old,new,autojunk=False)
    ops=[o for o in sm.get_opcodes() if o[0]!='equal']
    if len(ops)==1:
        _,a,b,c,d=ops[0]
        for pad in [0,1,2,3,5,8,12,20,30,50]:
            aa=max(0,a-pad);bb=min(len(old),b+pad);cc=max(0,c-pad);dd=min(len(new),d+pad)
            x=old[aa:bb];y=new[cc:dd]
            if len(compact(x)[0])<5 or len(compact(y)[0])<5:continue
            if pure_math(x) and pure_math(y) and balanced(x) and balanced(y) and math_evidence(x) and math_evidence(y):
                # Do not cut an alphabetic TeX command at either end.
                if aa and old[aa-1].isalpha() and old[aa].isalpha():continue
                if bb<len(old) and old[bb-1].isalpha() and old[bb].isalpha():continue
                out.append((x,y,'balanced exact changed context'))
    seen=set();result=[]
    for a,b,how in out:
        pair_key=(key(a),key(b))
        if pair_key not in seen and pair_key[0]!=pair_key[1]:result.append((a,b,how));seen.add(pair_key)
    return result

def transplant(actual,source,target):
    """Apply only the differing tokens, keeping the English common notation."""
    ka,ma=compact(actual);ks,_=compact(source);kt,mt=compact(target)
    if ka!=ks:return None
    edits=[]
    for tag,a,b,c,d in difflib.SequenceMatcher(None,ks,kt,autojunk=False).get_opcodes():
        if tag=='equal':continue
        # An expanded named glyph must be replaced as a complete source token.
        if (a and a<len(ma) and ma[a-1]==ma[a]) or (b and b<len(ma) and ma[b-1]==ma[b]) or (c and c<len(mt) and mt[c-1]==mt[c]) or (d and d<len(mt) and mt[d-1]==mt[d]):
            return target if r'\SGApage' not in actual else None
        start=ma[a][0] if a<len(ma) else len(actual)
        end=ma[b-1][1] if b>a else start
        replacement=target[mt[c][0]:mt[d-1][1]] if d>c else ''
        # Control-word boundaries remain token boundaries after text splicing.
        if not replacement and end<len(actual) and actual[end].isalpha() and re.search(r'\\[A-Za-z]+$',actual[:start]):replacement=' '
        if replacement and replacement[0].isalpha() and re.search(r'\\[A-Za-z]+$',actual[:start]):replacement=' '+replacement
        if re.search(r'\\[A-Za-z]+$',replacement) and end<len(actual) and actual[end].isalpha():replacement+=' '
        edits.append((start,end,replacement))
    result=replace_spans(actual,edits)
    if key(result)!=kt or not balanced(result,False):return None
    if len(re.findall(r'(?<!\\)\$',actual))%2 != len(re.findall(r'(?<!\\)\$',result))%2:return None
    if bool(re.search(r'(?<!\\)\$',actual)) != bool(re.search(r'(?<!\\)\$',result)):return None
    return result

def variant_ranges(s):
    result=[]
    for m in active_matches(r'\\SGA(?:quiet)?var\b',s):
        try:
            _,_,j,_=group(s,m.end());_,_,j,_=group(s,j);ident,_,j,_=group(s,j)
        except ValueError:continue
        result.append((m.start(),j,ident))
    return result

def selected_with_owners(text,corrected):
    """Select body branches and retain the variant owning each output byte."""
    out=[];owners=[];cursor=0
    for m in active_matches(r'\\SGA(?:quiet)?var\b',text):
        if m.start()<cursor:continue
        try:
            d,_,j,_=group(text,m.end());c,_,j,_=group(text,j);ident,_,end,_=group(text,j)
        except ValueError:continue
        out.append(text[cursor:m.start()]);owners.extend(['']*(m.start()-cursor))
        chosen,child=selected_with_owners(c if corrected else d,corrected)
        if chosen and chosen[0].isalpha() and re.search(r'\\[A-Za-z@]+$',text[:m.start()]):
            chosen=' '+chosen;child.insert(0,'')
        if end<len(text) and text[end].isalpha():
            if re.search(r'\\[A-Za-z]+$',chosen) or (not chosen and re.search(r'\\[A-Za-z]+$',text[:m.start()])):
                chosen+=' ';child.append('')
        out.append(chosen);owners.extend([x or ident for x in child]);cursor=end
    out.append(text[cursor:]);owners.extend(['']*(len(text)-cursor))
    return ''.join(out),owners

def context_human_links(text,old,new,variants):
    """Bind only the changed bytes of a reviewed two-branch English context.

    The complete context must occur once in each selected branch. Its exact
    changed token spans must belong to human records; neighboring selectors
    outside those spans receive no attribution.
    """
    d,downers=selected_with_owners(text,False)
    c,cowners=selected_with_owners(text,True)
    dm=find_matches(old,d);cm=find_matches(new,c)
    if len(dm)!=1 or len(cm)!=1:return []
    da,db=dm[0];ca,cb=cm[0]
    dk,dp=compact(d[da:db]);ck,cp=compact(c[ca:cb])
    affected=set()
    uncovered=False
    def take(fragment,owners,offset,mapping,a,b):
        nonlocal uncovered
        if b<=a:return
        lo,hi=mapping[a][0],mapping[b-1][1]
        for pos in range(lo,hi):
            owner=owners[offset+pos]
            if owner:affected.add(owner)
            elif fragment[pos] not in '{} \n\t\r':uncovered=True
    for tag,a,b,x,y in difflib.SequenceMatcher(None,dk,ck,autojunk=False).get_opcodes():
        if tag=='equal':continue
        take(d[da:db],downers,da,dp,a,b)
        take(c[ca:cb],cowners,ca,cp,x,y)
    # Every changed character has to be inside a known human selector. An
    # unrelated visible change cannot be credited to the nearby human record.
    if uncovered or not affected:return []
    byid={v['id']:v for v in variants}
    if any(k not in byid or not byid[k]['kind'].startswith('human') for k in affected):return []
    return [byid[k] for k in sorted(affected)]

def find_matches(needle,text):
    n,_=compact(needle);t,m=compact(text)
    if len(n)<2:return []
    pos=[];i=0
    while True:
        i=t.find(n,i)
        if i<0:break
        a=m[i][0];b=m[i+len(n)-1][1]
        if balanced(text[a:b],False):pos.append((a,b))
        i+=len(n)
    return list(dict.fromkeys(pos))

def language_matches(needle,text):
    pat=r'(?<![A-Za-z])'+re.escape(needle).replace(r'\ ',r'\s+')+r'(?![A-Za-z])'
    return [m.span() for m in re.finditer(pat,text)]

def page_window(s,expose,page,width=0):
    markers=list(re.finditer(r'\\SGApage\{[^}]+\}\{'+re.escape(expose)+r'\}\{(\d+)\}',s))
    ix=[i for i,m in enumerate(markers) if abs(int(m.group(1))-int(page))<=width]
    if not ix:return None
    a=markers[ix[0]].end();b=markers[ix[-1]+1].start() if ix[-1]+1<len(markers) else len(s)
    # Stop at next exposé, rather than including the remainder of the book.
    other=re.search(r'% BEGIN INCLUDED [^\n]+/\d+(?:bis)?/\d+(?:bis)?_English\.tex',s[a:b])
    if other:b=a+other.start()
    back=s.find(r'\backmatter',a,b)
    if back>=0:b=back
    return a,b

def apply(s,add,record,audit,variants):
    # These three scopes are explicitly reviewed against the canonical MPs.
    # The original human pairs remain untouched in the separate human ledger.
    def human(source):
        found=[v for v in variants if source in v['source'].split('; ')]
        assert len(found)==1,(source,len(found))
        return found[0]
    def macro(v):return r'\SGAvar{'+v['printed']+'}{'+v['corrected']+'}{'+v['id']+'}'
    v=human('EN-ORG-0809');old=macro(v)
    compound=r"\fprod{Z'}{Z"+old+r'}{Z_1}'
    assert s.count(compound)==1,('MP0777',s.count(compound))
    v.update(printed=r"\fprod{Z'}{Z_1}{Z_1}",corrected=r"\fprod{Z'}{Z_1}{Z}")
    s=s.replace(compound,macro(v),1);v['source']+='; MP0777; DEC-EN-MP0777-HUMAN-PROJECTION'
    record('MP0777; DEC-EN-MP0777-HUMAN-PROJECTION','XVII',368,'full fiber-product scope; original human pair retained',compound,macro(v),'canonical human-scope projection')
    v=human('EN-ORG-0964');old=macro(v);before=v['corrected'];v['corrected']='('
    assert s.count(old)==1
    s=s.replace(old,macro(v),1);v['source']+='; MP0801; DEC-EN-MP0801-HUMAN-PROJECTION'
    record('MP0801; DEC-EN-MP0801-HUMAN-PROJECTION','XVII',437,'opening bibliography delimiter; original human pair retained',before,'(','canonical human-scope projection')
    v=human('EN-ORG-1120');pair=macro(v)
    old=r'R^{+}f_{!}'+pair+r'\circ';new=r'R^{+}f'+pair+r'_{!}\circ'
    assert s.count(old)==1,('MP0820',s.count(old))
    s=s.replace(old,new,1);v['source']+='; MP0820; DEC-EN-MP0820-HUMAN-PROJECTION'
    record('MP0820; DEC-EN-MP0820-HUMAN-PROJECTION','XVII',476,'place the recorded prime on f before its subscript',old,new,'canonical TeX scope')
    # Author's plain P, a single explicit macro mapping in every form.
    old=r'\newcommand{\PP}{\mathbf{P}}';new=r'\newcommand{\PP}{P}'
    if old in s:
        s=s.replace(old,new)
        record('DEC-NOTATION-P','all','all','macro PP; applies to every occurrence',old,new,'notation')
    # C293 and MP0355 refer to the same passage. C293 fixes script/case in
    # French transcription; MP0355 records V as the printed misprint for U.
    target=r'$p$ from $\Tt/V$ to $\Ss/U$.'
    assert s.count(target)==1,s.count(target)
    repl=r'$p$ from $\Tt/V$ to '+add(r'$\Ss/V$',r'$\Ss/U$','MP0355; C293; DEC-C293','V',78,'Proposition 8.2.6; target slice','agreed misprint')+'.'
    s=s.replace(target,repl)
    audit.append(dict(id='MP0355',expose='V',page=78,status='paired',method='C293/MP0355 reconciliation',printed=r'\Ss/V',corrected=r'\Ss/U'))
    target='is always right\nadjoint'
    assert s.count(target)==1
    s=s.replace(target,'is always '+add('right\nadjoint','left\nadjoint','OM-OPUS-0005; OM-SOL-0021','I',32,'5.10, adjunction stated after (5.10.1)','accepted one-model misprint'))
    record('OM-OPUS-0005; OM-SOL-0021','I',32,'5.10, adjunction stated after (5.10.1)',target,'is always left\nadjoint','accepted one-model misprint')
    # The 157 historical port edits remain part of the released baseline.
    port=[json.loads(x) for x in (SOURCES/'en/F_port_20261112/PORT_EN4_LOG.jsonl').read_text().splitlines() if x.strip()]
    baseline=RELEASE.read_text();blocks={f['name']:f['text'] for f in fragment_blocks(baseline)}
    rows=[]
    for x in port:
        phrase=x.get('tr_new') if x.get('decision')=='apply' else x.get('tr_old')
        frag=blocks.get(Path(x.get('tr_file') or '').name,'')
        found=bool(phrase and key(phrase) in key(frag))
        link_reduced=False
        if phrase and not found:
            def visible_refs(t):return re.sub(r'\\(?:hyperref|eqhyperref)\[[^]]*\]\{([^{}]*)\}',r'\1',t)
            link_reduced=compact(visible_refs(phrase))[0] in compact(visible_refs(frag))[0]
        rows.append(dict(id=x['id'],expose=x.get('expose',''),page=x.get('page',''),decision=x.get('decision',''),released_check='exact-token-equivalent text present' if found else ('rendered reading present; release link changed' if link_reduced else ('not a textual edit' if not phrase else 'needs contextual audit')),reading=phrase or '',source='en/F_port_20261112/PORT_EN4_LOG.jsonl',note=x.get('note') or ''))
    write_tsv(RECORDS/'EN_PORT_AUDIT.tsv',rows,['id','expose','page','decision','released_check','reading','source','note'])
    # Port all newly placed French mathematical patches, with conservative
    # unique matching inside the recorded printed page and its boundary.
    patches=json.loads((RECORDS/'FR_APPLIED_PATCHES.json').read_text()) if (RECORDS/'FR_APPLIED_PATCHES.json').exists() else []
    # The French ledger contains an audit history as well as the final exact
    # canonical pairs. Earlier intermediate adaptations are not additional
    # misprints and must not create a second English alteration.
    superseded={'Adaptation to the existing E corrected spelling','Restoration of the documented printed reading'}
    patches=[p for p in patches if p.get('method') not in superseded]
    for p in patches:p['id']=p.get('source',p['id']).split(';')[0]
    exact_french_ids={p['id'] for p in patches if p['id'].startswith('MP')}
    for filename in ['MP_T3_PATCHES.json','MP702_810_PAIRS.json','MP_T3_MIDDLE_PATCHES.json','MP_T1_T2_PATCHES.json']:
        path=ROOT/'output/shared'/filename
        if path.exists():
            for p in json.loads(path.read_text()):
                if p['id'] in exact_french_ids:continue
                p=dict(p);p['source']=p['id'];p['kind']='agreed misprint';patches.append(p)
    misprints=json.loads((SOURCES/'fixes/MISPRINTS_4.json').read_text())
    for i,p in enumerate(misprints,1):
        ident='MP%04d'%i
        if ident in exact_french_ids:continue
        old=p['tex_did'];new=p['correct']
        if old!=new and '%' not in old:
            patches.append(dict(id=ident,source=ident,file=next(k for k,v in EXPOSE.items() if v==p['expose']),page=p['page'],printed=old,corrected=new,kind='agreed misprint',place=p['where']))
        old=p['print']
        if old!=new and pure_math(old) and pure_math(new) and balanced(old) and balanced(new):
            patches.append(dict(id=ident,source=ident,file=next(k for k,v in EXPOSE.items() if v==p['expose']),page=p['page'],printed=old,corrected=new,kind='agreed misprint',place=p['where']))
    one=RECORDS/'one_model_edits.json'
    if one.exists():
        for p in json.loads(one.read_text()):
            if p['on_disputed_page']:continue
            for seg in p.get('segments',[]):
                if not candidates(seg['printed'],seg['corrected']):continue
                patches.append(dict(id=p['id'],source=p['id'],file=p['file'],page=p['page'],printed=seg['printed'],corrected=seg['corrected'],kind='accepted one-model misprint',place=p['place']))
    language=RECORDS/'EN_MISPRINT_LANGUAGE_ASSESSMENT.json'
    language_rows=json.loads(language.read_text()) if language.exists() else []
    for p in language_rows:
        if 'english_delta' in p:
            delta=p['english_delta']
            patches.append(dict(id=p['id'],source=p['id'],file=next(k for k,v in EXPOSE.items() if v==p['expose']),page=p['page'],printed=delta['printed'],corrected=delta['corrected'],kind='agreed misprint',place=p['place'],english_language=True))
    from en_manual_pairs import records as manual_records
    manual=manual_records()
    for fn in ['EN_REVIEW_EXTRA45.json','EN_T3_EXACT_PAIRS.json','EN_T2_LATE_EXACT_PAIRS.json','EN_T3_AUTO_REPAIR_PAIRS.json','EN_T1_T2_EXACT_PAIRS.json','EN_ONE_MODEL_NO_IMPACT_PARTIAL.json','EN_ONE_MODEL_EXACT_PAIRS.json']:
        fp=ROOT/'output/shared'/fn
        if not fp.exists():continue
        reviewed=json.loads(fp.read_text())
        reviewed_ids={row['id'] for row in reviewed}
        manual=[p for p in manual if p['id'] not in reviewed_ids]
        for row in reviewed:
            language_rows.append(row)
            if row['assessment'].lower().startswith('no'):continue
            for delta in row.get('english_deltas',[row.get('english_delta',{})]):
                if not delta or not delta.get('location_verified'):continue
                anchors=[delta.get('current_anchor'),delta.get('baseline_anchor'),row.get('baseline_anchor')]
                anchors+=delta.get('alternative_current_anchors',[])+row.get('alternative_current_anchors',[])
                anchors=list(dict.fromkeys(a for a in anchors if a))
                manual.append(dict(id=row['id'],source=row['id'],file=next(k for k,v in EXPOSE.items() if v==row['expose']),page=row['page'],printed=delta.get('pre_notation_printed',delta['printed']),corrected=delta.get('pre_notation_corrected',delta['corrected']),kind='accepted one-model misprint' if row['id'].startswith('OM-') else 'agreed misprint',place=row.get('place','reviewed source location'),manual=True,current_anchor=delta.get('current_anchor'),current_anchors=anchors,current_state=delta.get('current_state'),existing_human_source=delta.get('existing_human_source',row.get('existing_human_source')),human_printed_override=delta.get('human_printed_override',row.get('human_printed_override')),editorial_decision=delta.get('editorial_decision'),reviewed_reason=delta.get('reason',row.get('reason','')),compose_with_source=delta.get('compose_with_source',row.get('compose_with_source'))))
    # Canonical MP0664 prints 2.1. The released human first leaf is a \ref
    # to3.1 and therefore needs this specifically reviewed body projection.
    # Its original pair remains unchanged in EN_HUMAN_RECORDS and the dossier.
    for p in manual:
        if p['id']=='MP0664':
            p.update(existing_human_source='EN-ORG-0404',human_printed_override=r'\hyperref[XIV.subsec2.1]{2.1}')
        if p['id']=='OM-SOL-0136':p['compose_with_source']='MP0113'
    manual.sort(key=lambda p:p['id']=='MP0915')
    manual_ids={p['id'] for p in manual}
    patches=manual+patches
    latest_assessment={p['id']:p for p in language_rows}
    noimpact_ids={p['id'] for p in latest_assessment.values() if p['assessment'].lower().startswith('no')}
    accepted_by_id=collections.defaultdict(list)
    for p in patches:accepted_by_id[p['id']].append(p)
    touched={'MP0355'}
    for p in patches:
        if p['id']=='MP0355' or p['id'] in noimpact_ids:continue
        exp=EXPOSE.get(p['file'],p.get('expose',''));page=p['page'];source=p['id']
        if source in manual_ids and not p.get('manual'):continue
        old=p['printed'];new=p['corrected']
        # These record strings run a TeX control word into the next printed
        # letter. Spaces/braces encode the recorded symbols without altering
        # their mathematical reading.
        for malformed,encoded in [(r'\prodF',r'\prod F'),(r'\widehatB',r'\widehat{B}'),(r'\astj',r'\ast j')]:
            old=old.replace(malformed,encoded);new=new.replace(malformed,encoded)
        if old==new:continue
        result={'id':source,'expose':exp,'page':page,'status':'unresolved','printed':old,'corrected':new,'method':''}
        if p.get('existing_human_source'):
            linked=[v for v in variants if p['existing_human_source'] in v['source'].split('; ') and v['kind'].startswith('human')]
            if len(linked)!=1:raise ValueError(('reviewed human source missing',source,p['existing_human_source']))
            v=linked[0]
            if p.get('human_printed_override') is not None:
                before=v['printed'];after=p['human_printed_override']
                oldmacro=r'\SGAvar{'+before+'}{'+v['corrected']+'}{'+v['id']+'}'
                newmacro=r'\SGAvar{'+after+'}{'+v['corrected']+'}{'+v['id']+'}'
                if s.count(oldmacro)!=1:raise ValueError(('human override location',source,v['id']))
                s=s.replace(oldmacro,newmacro,1);v['printed']=after
                record(source+'; DEC-EN-MP0664-HUMAN-PROJECTION',exp,page,'canonical printed body reading; original human dossier retained',before,after,'canonical diplomatic projection')
                if 'DEC-EN-MP0664-HUMAN-PROJECTION' not in v['source']:v['source']+='; DEC-EN-MP0664-HUMAN-PROJECTION'
            if source not in v['source'].split('; '):v['source']+='; '+source
            result.update(status='represented by existing variant',method='explicit reviewed human source '+p['existing_human_source']+'; '+v['id'])
            audit.append(result);touched.add(source);continue
        pair_candidates=[(old,new,'inspected English context')] if p.get('manual') else ([(old,new,'reviewed English lexical delta')] if p.get('english_language') else candidates(old,new))
        for a,b,how in pair_candidates:
            # Link existing human pairs instead of making duplicate variants.
            av,bv=key(a),key(b)
            matches=[v for v in variants if v['expose']==exp and abs(int(v['page'])-int(page))<=1
                     and (p.get('manual') or v['kind'].startswith('human') or source in v['source'].split('; '))
                     and av in key(v['printed']) and bv in key(v['corrected'])]
            if len(matches)==1:
                v=matches[0]
                if source not in v['source'].split('; '):v['source']+='; '+source
                result.update(status='represented by existing variant',method=v['id']+'; '+how);break
            placed=False
            for width in [0,1]:
                window=page_window(s,exp,page,width)
                if window is None:continue
                ws,we=window;text=s[ws:we]
                vr=variant_ranges(text)
                order=[('printed',a,b),('corrected',b,a)]
                if av in bv and len(av)<len(bv):order.reverse()
                for which,needle,other in order:
                    found=language_matches(needle,text) if p.get('english_language') else find_matches(needle,text)
                    mm=[(x,y) for x,y in found if not any(vs<y and x<ve for vs,ve,_ in vr)]
                    if len(mm)!=1:continue
                    x,y=mm[0];actual=text[x:y]
                    prefix=text[max(0,x-250):x]
                    if re.search(r'\\(?:hyperref|eqhyperref|etiquette|hyperrefext)\[[^]]*$',prefix):continue
                    if re.search(r'\\(?:label|etiquette|hypertarget|MakeLinkTarget)\b[^{}]*(?:\{[^{}]*)?$',prefix):continue
                    # A bare symbol match inside a notation-forming macro is
                    # not the same displayed object as the canonical bare one.
                    # Exact contexts including the macro are matched as a whole.
                    if re.search(r'\\(?:widehat|hat|widetilde|tilde|bar|overline|underline|mathcal|mathscr|mathfrak|mathbf|mathsf|mathrm|sheaf|Ysheaf)\s*$',prefix):continue
                    # Inline math delimiters need the same mode in both branches.
                    other=other.strip('$') if '$' not in actual else other
                    # Inspected English contexts carry their own complete
                    # spaces and line breaks. Character splicing a word across
                    # the released line wrap can otherwise print “shea f”.
                    other=carry_original_pages(actual,other) if p.get('manual') or p.get('english_language') else transplant(actual,needle,other)
                    if other is None or not balanced(other,False):continue
                    printed=other if which=='corrected' else actual
                    corrected=actual if which=='corrected' else other
                    # A macro must receive its braced argument before the form
                    # selector is evaluated; include that command in the pair.
                    if actual.startswith('{'):
                        cm=re.search(r'\\[A-Za-z@]+(?:\[[^]]*\])?$',text[:x])
                        if cm:
                            command=cm.group()
                            printed=command+' '+printed;corrected=command+' '+corrected
                            x=cm.start()
                    kind=p.get('kind','agreed misprint')
                    if kind=='hand replay':
                        repl=corrected
                    else:repl=add(printed,corrected,source,exp,page,p.get('place','recorded mathematical correction'),kind)
                    s=s[:ws+x]+repl+s[ws+y:]
                    if which=='printed':record(source,exp,page,'French mathematical correction port',actual,corrected,kind)
                    result.update(status='confirmed common scan reading' if kind=='hand replay' else 'paired',method=how+'; unique page window '+str(width),printed=printed,corrected=corrected)
                    placed=True;break
                if placed:break
            if placed:break
        if result['status']=='unresolved' and p.get('manual'):
            for width in [0,1]:
                window=page_window(s,exp,page,width)
                if window is None:continue
                ws,we=window
                linked=context_human_links(s[ws:we],old,new,variants)
                if not linked:continue
                for v in linked:
                    if source not in v['source'].split('; '):v['source']+='; '+source
                result.update(status='represented by existing variant',method='full reviewed English context; changed-byte human mapping: '+', '.join(v['id'] for v in linked))
                break
        if result['status']=='unresolved' and p.get('manual'):
            # A released human pair may already carry the corrected formula in
            # both branches. Restore the canonical printed formula in its
            # diplomatic leaf while preserving the original human dossier.
            repairs=[]
            for v in variants:
                joint_915=source=='MP0915' and 'OM-SOL-1326' in v['source'].split('; ')
                reviewed_joint=p.get('compose_with_source') in v['source'].split('; ')
                if (not v['kind'].startswith('human') and not joint_915 and not reviewed_joint) or v['expose']!=exp or abs(int(v['page'])-int(page))>1:continue
                proposed={};changed=False
                for side,desired,alternative in [('printed',old,new),('corrected',new,old)]:
                    leaf=v[side]
                    if find_matches(desired,leaf):proposed[side]=leaf;continue
                    choices=[alternative]
                    choices+=p.get('current_anchors',[]) or ([p['current_anchor']] if p.get('current_anchor') else [])
                    out=leaf
                    for needle in choices:
                        mm=find_matches(needle,leaf)
                        if len(mm)!=1:continue
                        x,y=mm[0];newpart=transplant(leaf[x:y],needle,desired)
                        if newpart is None:continue
                        out=leaf[:x]+newpart+leaf[y:];changed=True;break
                    proposed[side]=out
                if changed:repairs.append((v,proposed))
            if len(repairs)==1:
                v,newleaves=repairs[0]
                oldmacro=r'\SGAvar{'+v['printed']+'}{'+v['corrected']+'}{'+v['id']+'}'
                newmacro=r'\SGAvar{'+newleaves['printed']+'}{'+newleaves['corrected']+'}{'+v['id']+'}'
                if s.count(oldmacro)==1:
                    s=s.replace(oldmacro,newmacro,1)
                    for side in ['printed','corrected']:
                        if v[side]!=newleaves[side]:record(source,exp,page,'canonical projection into existing '+v['id']+' '+side,v[side],newleaves[side],p.get('kind','agreed misprint'))
                    v.update(newleaves)
                    if source not in v['source'].split('; '):v['source']+='; '+source
                    result.update(status='represented by existing variant',method='reviewed canonical projection into '+v['id'])
        if result['status']=='unresolved' and p.get('manual') and (p.get('current_anchors') or p.get('current_anchor')):
            for width in [0,1]:
                window=page_window(s,exp,page,width)
                if window is None:continue
                ws,we=window;text=s[ws:we];vr=variant_ranges(text)
                anchors=p.get('current_anchors',[]) or [p['current_anchor']]
                found=list(set((x,y) for anchor in anchors for x,y in find_matches(anchor,text) if not any(vs<y and x<ve for vs,ve,_ in vr)))
                if len(found)!=1:continue
                x,y=found[0]
                if not balanced(old,False) or not balanced(new,False):continue
                kind=p.get('kind','agreed misprint')
                projected_old=carry_original_pages(text[x:y],old);projected_new=carry_original_pages(text[x:y],new)
                repl=add(projected_old,projected_new,source,exp,page,p.get('place','reviewed source-intermediate English anchor'),kind)
                s=s[:ws+x]+repl+s[ws+y:]
                record(source,exp,page,p.get('place','source-intermediate English repair'),text[x:y],new,kind)
                result.update(status='paired',method='reviewed source-intermediate English anchor',printed=old,corrected=new)
                break
        if result['status']=='unresolved' and not pair_candidates:
            result['status']='requires English-language assessment'
        if p.get('editorial_decision') and result['status']!='unresolved':
            scoped=[v for v in variants if source in v['source'].split('; ') and key(new) in key(v['corrected'])]
            assert len(scoped)==1,('editorial decision scope',source,len(scoped))
            v=scoped[0];decision=p['editorial_decision']
            if decision not in v['source'].split('; '):v['source']+='; '+decision
            result['editorial_decision']=decision
            record(source+'; '+decision,exp,page,p.get('place','reviewed scope'),old,new,p.get('kind','accepted one-model misprint'))
        audit.append(result);touched.add(source)
    for p in latest_assessment.values():
        if p['assessment'].lower().startswith('no'):
            audit.append(dict(id=p['id'],expose=p['expose'],page=p['page'],status='no English impact',printed=p.get('printed_french',p.get('printed','')),corrected=p.get('corrected_french',p.get('corrected','')),method=p['reason']))
            touched.add(p['id'])
    # Every canonical agreed misprint receives an audit row. Unlocated entries
    # are retained as such; coverage is never inferred from a row count.
    for i,p in enumerate(misprints,1):
        ident='MP%04d'%i
        if ident in touched:continue
        audit.append(dict(id=ident,expose=p['expose'],page=p['page'],status='awaiting exact French placement / English assessment',printed=p['print'],corrected=p['correct'],method='canonical record'))
    return s
