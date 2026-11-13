from __future__ import annotations
import argparse, difflib, json, re, subprocess, sys
from pathlib import Path
from sga5_common import *

def expand_document(s, layer):
    pre,body=split_document(s)
    body=strip_comments(body)
    r=r'\mathbb{R}' if layer=='diplomatic' else r'\mathrm{R}'
    core=r'\mathbb{R}\mathrm{Hom}' if layer=='diplomatic' else r'\mathrm{RHom}'
    u=r'\underline{'+core+'}'
    log=[];out=[];page=0
    for line in body.splitlines(keepends=True):
        fm=FOLIO.fullmatch(line.rstrip('\n'))
        if fm:page=int(fm[2]);out.append(line);continue
        if re.search(r'\\renewcommand\{\\R\}',line):
            m=re.search(r'\\renewcommand\{\\R\}\{(\\(?:mathrm|mathbb)\{R\})\}',line)
            if not m:raise ValueError('Unknown scoped R definition')
            r=m[1];log.append({'page':page,'macro':r'\R','expansion':r,'layer':layer,'operation':'scoped definition expanded at every following use'})
            line=line.replace(m[0],'')
        if re.search(r'\\renewcommand\{\\uRHom\}',line):
            if r'\mathrm{R}\underline{\mathrm{Hom}}' in line:u=r'\mathrm{R}\underline{\mathrm{Hom}}'
            elif r'\underline{\RHom}' in line:u=r'\underline{'+core+'}'
            else:raise ValueError('Unknown uRHom definition')
            log.append({'page':page,'macro':r'\uRHom','expansion':u,'layer':layer,'operation':'scoped definition expanded at every following use'})
            line=re.sub(r'\\renewcommand\{\\uRHom\}.*?(?=\n|$)','',line)
        if re.match(r'\s*\\(?:providecommand|newcommand|renewcommand|DeclareMathOperator|newenvironment|renewenvironment)',line):
            out.append(line);continue
        # Preserve TeX's one-token argument when expanding a zero-argument
        # macro that was passed without braces to an accent/font command.
        line=re.sub(r'(\\(?:underline|overline|hat|widehat|tilde|widetilde|bar|vec|dot|ddot|check|ol|wt|wh|mathrm|mathbf|mathbb|mathcal)\s*)(\\(?:RHomCore|RHom|uRHom|RGamma|RGc|RG|Rpi|Rj|rG|R))(?![A-Za-z@])',lambda m:m[1]+'{'+m[2]+'}',line)
        reps={r'\uRHom':u,r'\RHomCore':core,r'\RHom':core,r'\RGamma':r+r'\Gamma',r'\RGc':r+r'\Gamma_c',r'\RG':r+r'\Gamma',r'\Rpi':r+r'\pi',r'\Rj':r+'j',r'\rG':r+r'\Gamma^G',r'\R':r}
        for macro,value in reps.items():
            pat=re.escape(macro)+r'(?![A-Za-z@])'
            n=len(re.findall(pat,line))
            if n:
                log.append({'page':page,'macro':macro,'expansion':value,'layer':layer,'occurrences':n,'operation':'literal expansion by the source definition'})
                line=re.sub(pat,lambda m:value,line)
        # A TeX font macro consumes one token or a braced argument identically.
        line=re.sub(r'\\(mathrm|mathbb|mathcal|mathbf|mathfrak|mathscr)\s+([A-Za-z0-9])',r'\\\1{\2}',line)
        out.append(line)
    return pre,''.join(out),log

def source_for(index,page,before,after,variant_id):
    if getattr(index,'language','FR')=='EN':
        return index.sources(page,before,after) or f'BUILD-SOURCE-{variant_id}; EN_variants_input.json; en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex'
    if ('\\mathbb{R}' in before and '\\mathrm{R}' in after) or ('\\mathbb{R}\\mathrm{Hom}' in before and '\\mathrm{RHom}' in after):
        return 'conventions/GLOBAL_ISSUES_SGA.md:98; fr/sga5/diplomatic/s5.tex:macro R/RHomCore; fr/sga5/current/s5.tex:macro R/RHomCore'
    if page==433 and "F'" in before and "f'" in after:return 'OPEN-H75'
    if page==472 and before=='F' and after==r'F_\nu':return 'SOL-EN-084; OPEN_ITEMS_DECIDED.tsv'
    src=index.sources(page,before,after)
    return src or f'BUILD-SOURCE-{variant_id}; fr/sga5/diplomatic/s5.tex; fr/sga5/current/s5.tex'

def make_variants(a,b,page,index,variants,prefix='FR'):
    aa=atoms(a);bb=atoms(b);out=[]
    seq=difflib.SequenceMatcher(None,aa,bb,autojunk=False)
    for op,i,j,k,l in seq.get_opcodes():
        seen=list(FOLIO.finditer(''.join(bb[:k])))
        localpage=int(seen[-1][2]) if seen else page
        old=''.join(aa[i:j]);new=''.join(bb[k:l])
        if op=='equal':out.append(new);continue
        # Pure line wrapping / indentation differences have the same TeX space
        # token, except blank lines, which retain their paragraph boundary.
        if old.isspace() and new.isspace() and ('\n\n' in old)==('\n\n' in new):
            out.append(new);continue
        if old.startswith('{') and new.startswith('{') and brace_end(old,0)==len(old) and brace_end(new,0)==len(new):
            out.append('{'+make_variants(old[1:-1],new[1:-1],localpage,index,variants,prefix)+'}');continue
        # Recurse inside an identical one-argument wrapper to avoid making an
        # entire paragraph a single apparatus item for a changed letter.
        om=re.fullmatch(r'(\\(?:emph|textbf|textit|text|underline|mathrm|mathbf|mathbb|mathcal))\{(.*)\}',old,re.S)
        nm=re.fullmatch(r'(\\(?:emph|textbf|textit|text|underline|mathrm|mathbf|mathbb|mathcal))\{(.*)\}',new,re.S)
        if om and nm and om[1]==nm[1] and len(old)+len(new)>180:
            out.append(om[1]+'{'+make_variants(om[2],nm[2],localpage,index,variants,prefix)+'}');continue
        # Empty/space-only selections are real punctuation/spacing differences
        # unless both sides differ solely in one ordinary space token.
        vid=f'{prefix}-{len([v for v in variants if v["id"].startswith(prefix+"-")])+1:04d}'
        source=source_for(index,localpage,old,new,vid)
        reason=('Exact printed and corrected readings retained from the authenticated source layers at this folio; source identifiers resolve to the supplied correction register or fix log.' if 'BUILD-SOURCE' not in source else 'The supplied final diplomatic and corrected layers give these exact distinct readings at this place. This build retains their documented layer decision; no new mathematical reconstruction is introduced.')
        v={'id':vid,'page':localpage,'expose':expose_for(localpage),'before':old,'after':new,'source':source,'kind':classify(old,new,source),'reason':reason}
        variants.append(v)
        out.append('\\SGAvar{'+old+'}{'+new+'}{'+vid+'}')
    return ''.join(out)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--sources',default='work/sources');ap.add_argument('--contributions',default='work/contributions');ap.add_argument('--out',default='work/build/prepared');args=ap.parse_args()
    src=Path(args.sources)/'SGA5_FR';con=Path(args.contributions);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    scans=json.loads((con/'scans/PLACES_98_PATCHES.json').read_text())
    texts={x:(src/f'fr/sga5/{x}/s5.tex').read_text() for x in ['diplomatic','current']}
    patched={};marked={};source_edits=[];fixed=[]
    for layer,s in texts.items():
        actual=s;temp=s
        for d in reversed(scans['decisions']):
            ref=d['fr_'+layer];start,end=ref['start'],ref['end'];assert s[start:end]==ref['source_tex']
            repl=d['diplomatic_reading' if layer=='diplomatic' else 'corrected_reading']
            actual=actual[:start]+repl+actual[end:]
            temp=temp[:start]+r'\SGAFixedVariant{'+d['id']+'}'+temp[end:]
            source_edits.append({'id':d['id'],'page':d['folio'],'layer':layer,'before':ref['source_tex'],'after':repl,'source':'PLACES_98_DECIDED.tsv:'+d['id'],'place':ref['context']})
        if layer=='current':
            needle="par $F'/G_{x'}$ l'endomorphisme";repl="par $f'/G_{x'}$ l'endomorphisme"
            assert actual.count(needle)==temp.count(needle)==1
            actual=actual.replace(needle,repl);temp=temp.replace(needle,repl)
            source_edits.append({'id':'OPEN-H75','page':433,'layer':layer,'before':needle,'after':repl,'source':'OPEN_ITEMS_DECIDED.tsv:OPEN-H75','place':'XII 6.4 b; quotient endomorphism explicitly induced by f\u2032'})
            needle=r'avec $F$ annulé par $\ell^{\nu+1}$';repl=r'avec $F_\nu$ annulé par $\ell^{\nu+1}$'
            assert actual.count(needle)==temp.count(needle)==1
            actual=actual.replace(needle,repl);temp=temp.replace(needle,repl)
            source_edits.append({'id':'SOL-EN-084','page':472,'layer':layer,'before':needle,'after':repl,'source':'OPEN_ITEMS_DECIDED.tsv:SOL-EN-084','place':'XV, application of (3)_nu to the component F_nu; scan confirms the printed F'})
            needle=r'\Fr_{Y/S}';repl=r'\underline{\operatorname{\mathbb{F}r}}_{Y/S}'
            def retain_441(text):
                ms=list(FOLIO.finditer(text));m=next(m for m in ms if int(m[2])==441);n=ms[ms.index(m)+1]
                chunk=text[m.end():n.start()];assert chunk.count(needle)==1
                return text[:m.end()]+chunk.replace(needle,repl)+text[n.start():]
            actual=retain_441(actual);temp=retain_441(temp)
            source_edits.append({'id':'GLOBAL-98b','page':441,'layer':layer,'before':needle,'after':repl,'source':'OPEN_ITEMS_DECIDED.tsv:GLOBAL-98b; MISPRINTS_5:0572','place':'XII Exemple 7.3; retain supplied printed glyph in both branches pending the unavailable scan'})
        patched[layer]=actual;marked[layer]=temp
    prepared={};macro_log=[];preamble=None
    for layer,s in marked.items():
        pre,body,log=expand_document(s,layer)
        if layer=='current':preamble=pre
        prepared[layer]=body;macro_log+=log
    apages=split_folios(prepared['diplomatic']);bpages=split_folios(prepared['current'])
    assert list(apages)==list(bpages)==[p for p in range(1,485) if p!=435]
    idx=RecordIndex(src);variants=[];parts=[]
    def depth(s):
        n=0;i=0
        while i<len(s):
            if s[i]=='\\':
                m=re.match(r'\\(?:[A-Za-z@]+|.)',s[i:],re.S);i+=len(m[0]);continue
            n+=(s[i]=='{')-(s[i]=='}');i+=1
        return n
    abuf='';bbuf='';startpage=1
    for page in apages:
        marker=f'%%%%%%%%%%  scan idx {page+11}  |  folio {page}  %%%%%%%%%%'
        abuf+=marker+apages[page];bbuf+=marker+bpages[page]
        if depth(abuf)==depth(bbuf)==0:
            parts.append(make_variants(abuf,bbuf,startpage,idx,variants));abuf=bbuf='';startpage=page+1
    assert not abuf and not bbuf, 'Unclosed source groups at end of book'
    master=''.join(parts)
    nonprinting=[]
    for v in list(variants):
        if not v['before'].strip() and not v['after'].strip():
            call=r'\SGAvar{'+v['before']+'}{'+v['after']+'}{'+v['id']+'}'
            # The sole case is the endline immediately before \] at folio 52.
            assert v['page']==52 and master.find(call+r'\]')>=0
            master=master.replace(call,v['after'])
            variants.remove(v);nonprinting.append({**v,'reason':'TeX discards this endline in display math immediately before \\]; both branches have exactly the same printed tokens.'})
    for d in scans['decisions']:
        vid=d['id'];before=d['diplomatic_reading'];after=d['corrected_reading'];tag=r'\SGAFixedVariant{'+vid+'}'
        assert master.count(tag)==1,(vid,master.count(tag))
        suffix=following_scripts(master,master.index(tag)+len(tag))
        master=master.replace(tag+suffix,r'\SGAvar{'+before+suffix+'}{'+after+suffix+'}{'+vid+'}')
        variants.append({'id':vid,'page':d['folio'],'expose':'XV','before':before+suffix,'after':after+suffix,'glyph_before':before,'glyph_after':after,'source':'PLACES_98_DECIDED.tsv:'+vid+'; conventions/GLOBAL_ISSUES_SGA.md:98','kind':'derived-functor typography','reason':d['reason']})
        for layer in prepared:prepared[layer]=prepared[layer].replace(tag,before if layer=='diplomatic' else after)
    master,marker_terminations=terminate_folio_comments(master)
    write_json(out/'FR_marker_terminations.json',marker_terminations)
    (out/'FR_preamble.tex').write_text(preamble)
    (out/'FR_annotated_body.tex').write_text(master)
    (out/'FR_diplomatic_body.tex').write_text(prepared['diplomatic'])
    (out/'FR_corrected_body.tex').write_text(prepared['current'])
    for layer,s in patched.items():(out/f'FR_{layer}_source.tex').write_text(s)
    write_json(out/'FR_variants.json',variants)
    write_json(out/'FR_source_edits.json',source_edits)
    write_json(out/'FR_macro_expansion_log.json',macro_log)
    write_json(out/'FR_nonprinting_equivalences.json',nonprinting)
    write_json(out/'FR_preparation_summary.json',{'variants':len(variants),'scan_variants':32,'source_folios':list(apages),'body_hashes':{k:digest(v) for k,v in prepared.items()},'source_hashes':{k:digest(v) for k,v in texts.items()}})
    # Resolve every apparatus citation from exact original-source intervals
    # after the layer representation has been written. This changes metadata
    # only; the resolver asserts every ID, branch, page and ordering invariant.
    subprocess.run([sys.executable,str(con/'validation_fr/resolve_fr_sources.py'),
                    '--sources',str(src),'--prepared',str(out),
                    '--contributions',str(con),'--out',str(con/'validation_fr'),'--apply'],check=True)
    print(json.dumps({'language':'FR','variants':len(variants),'scan_variants':32,'source_folios':len(apages),'macro_expansion_events':len(macro_log)}))

if __name__=='__main__':main()
