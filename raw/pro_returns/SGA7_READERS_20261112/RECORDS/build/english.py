#!/usr/bin/env python3
"""Build all English forms from one annotated, losslessly projected master.

The released component bodies are verified directly against both release
single-file readers. The original-English Expose VI is taken from the same
paired witnesses as the French book. Reconstruction decisions are explicit.
"""
import argparse
import bisect
import collections
import csv
import difflib
import hashlib
import json
import re
from pathlib import Path
import french
from english_stage import ROOT,SRC,WORK,OUT,MARK,load_components
from english_variants import editorial_spans,math_entries,norm,balanced
from english_manual import build_manual

REC=ROOT/'output/records';DEST=ROOT/'output/en'


def read(p):return json.loads(p.read_text())


def clean(t):return french.comments_out(t)


def tex_safe(t):
    # Macro arguments tokenize ampersands before TikZ changes their catcodes.
    # Transport them explicitly without changing the rendered alignment.
    # A deleted mathematical line may leave an empty source line; TeX must not
    # turn that nonprinting spacing into a paragraph token inside the formula.
    t=re.sub(r'\\begin\{(equation\*?|align\*?|aligned|gather\*?|multline\*?|split|displaymath|eqnarray\*?|tikzcd|tikzpicture)\}.*?\\end\{\1\}',
             lambda m:re.sub(r'\n[ \t]*\n+', '\n',m.group()),t,flags=re.S)
    t=re.sub(r'(?<!\\)\\\[.*?(?<!\\)\\\]',lambda m:re.sub(r'\n[ \t]*\n+', '\n',m.group()),t,flags=re.S)
    t=re.sub(r'(\\SGApage\{[^}]*\}\{[^}]*\}\s*)\\clearpage',r'\\clearpage\n\1',t)
    def cv(m):return re.sub(r'(?<!\\)&',r'\\&',m.group())
    return re.sub(r'\\begin\{(tikzcd|tikzpicture)\}.*?\\end\{\1\}',cv,t,flags=re.S)


def protected_spans(t):
    result=[]
    for m in re.finditer(r'\\(?:begin|end|SGARefTarget|SGARefAliasTarget|label|SGARefLink)\{[^}]*\}',t):result.append((m.start(),m.end(),'structural key'))
    for m in re.finditer(r'\\begin\{(?:tikzcd|tikzpicture)\}\[[^\]]*\]',t):result.append((m.start(),m.end(),'diagram layout'))
    for m in re.finditer(r'\\(?:text|mbox|hbox)\{[^{}]*\}',t):
        if re.search(r'[A-Za-z]{3,}',m.group()):result.append((m.start(),m.end(),'English prose in formula'))
    return result


def source_formula_status(op):
    m=re.search(r'fr/(sga7ii?)/\{diplomatic,current\}/([^;]+); folio [^;]+; formula (\d+)',op['source'])
    if not m:return None
    base=SRC/'fr'/m.group(1);fn=m.group(2);index=int(m.group(3))-1
    key=(m.group(1),fn)
    if key not in source_formula_status.cache:
        d=(base/'diplomatic'/fn).read_text();c=(base/'current'/fn).read_text();dm,cm=math_entries(d),math_entries(c)
        unequal=set()
        for tag,i,j,k,l in difflib.SequenceMatcher(None,[x['norm'] for x in dm],[x['norm'] for x in cm],autojunk=False).get_opcodes():
            if tag!='equal' and j-i!=l-k:unequal.update(range(k,l))
        source_formula_status.cache[key]=(c,cm,unequal)
    c,cm,unequal=source_formula_status.cache[key]
    if index>=len(cm):return 'stale source formula index'
    start=cm[index]['start'];line=c[c.rfind('\n',0,start)+1:start]
    if re.search(r'(?<!\\)%',line):return 'nonprinting source comment'
    if index in unequal:return 'source formula split/merge requires explicit review'
    return None
source_formula_status.cache={}


def make_operations(components,candidates):
    overrides,no,decisions=build_manual(components,candidates)
    bykey={(c['volume'],c['component']):c for c in components}
    port=read(WORK/'en_port_operations.json');formula=read(WORK/'en_formula_operations.json')
    allops=[];rejected=[]
    supersessions=read(WORK/'en_proposal_supersessions.json') if (WORK/'en_proposal_supersessions.json').exists() else []
    superseded_ports=[]
    port_reviews={}
    for review_file in sorted(WORK.glob('en_port_witness_audit_*.json')):
        for r in read(review_file):
            i=r['port_operation_index'];candidate=port[i]
            assert (candidate['volume'],candidate['component'],candidate['corrected'])==(r['volume'],r['component'],r['corrected']),('stale port review',i)
            port_reviews[i]=r;decisions.append(r)
            if r['action']=='override':
                allops.append((120,{**r,'source':r['id']+'; '+r['source_diplomatic']+'; folio '+str(r['folio']),
                                    'kind':'verified final printed witness','method':'individual final-witness review'}))
    formula_reviews={}
    review_files=sorted(WORK.glob('en_formula_resolutions_*.json'))+sorted(WORK.glob('en_formula_accepted_audit_*.json'))
    for review_file in review_files:
        data=read(review_file);rows=data if isinstance(data,list) else data.get('resolutions',[])
        for r in rows:
            if 'operation_index' not in r:continue
            r=dict(r)
            if 'action' in r:r['status']='replace' if r['action']=='override' else r['action']
            if 'rejected_automatic_printed' in r:r['original_printed']=r['rejected_automatic_printed']
            i=r['operation_index']
            def same(op):
                return (op['volume']==r['volume'] and op['component']==r['component']
                        and op['corrected']==r['corrected'] and op['printed']==r.get('original_printed',op['printed'])
                        and op['source']==r['source'])
            if not (i<len(formula) and same(formula[i])):
                matches=[j for j,op in enumerate(formula) if same(op)]
                assert len(matches)==1,('stale formula review',review_file.name,i,matches)
                i=matches[0]
            existing=formula_reviews.get(i)
            if not (existing and existing['status']=='replace' and r['status']=='accept'):
                formula_reviews[i]=r
            decisions.append(r)
    for i,op in enumerate(port):
        if i in port_reviews:continue
        m=re.search(r'#(C\d+)',op['source']);key=op['volume']+':'+m.group(1) if m else ''
        superseded=next((r for r in supersessions if key==r['volume']+':'+r['port_id']),None)
        if superseded:
            assert op['component']==superseded['component'] and op['corrected']==superseded['corrected'] and op['printed']==superseded['proposed_printed']
            superseded_ports.append(superseded);continue
        if key in no or key in overrides:continue
        allops.append((80,op))
    for i,original_op in enumerate(formula):
        op=dict(original_op);review=formula_reviews.get(i)
        if review and review['status']=='reject':
            rejected.append({**op,'reason':review['reason'],'review':'individual formula structural audit','operation_index':i,
                             'disposition':review.get('covered_by','explicit source-context rejection; no additional English edit'),
                             'review_id':review.get('id','EN-FORMULA-ROOT-'+str(i))});continue
        if review and review['status']=='replace':
            op['printed']=review['printed'];op['method']='reviewed structural reconstruction'
            if review.get('id')=='ED-EN-ILLEGIBLE-XVIII-5.8.3.1':op['apparatus_note']=review['reason']
        why=source_formula_status(op)
        if why and not (review and review['status']=='replace' and why.startswith('source formula split')):
            rejected.append({**op,'reason':why});continue
        spans=protected_spans(op['corrected']);bad=[]
        for h in french.token_changes(op['corrected'],op['printed']):
            for a,b,reason in spans:
                if h['a0']<b and h['a1']>a:bad.append(reason)
        if bad:
            rejected.append({**op,'reason':'; '.join(sorted(set(bad)))});continue
        allops.append((98 if review else 90,op))
    allops.extend((100,op) for op in overrides.values())
    # Parallel editorial resolutions are optional while a draft is compiling;
    # the final audit records whether every assigned item has been resolved.
    for p in (sorted(WORK.glob('en_formula_resolutions_*.json'))+sorted(WORK.glob('en_font_resolutions_*.json'))
              +sorted(WORK.glob('en_nonmath_resolutions_*.json'))):
        data=read(p);rows=data if isinstance(data,list) else data.get('resolutions',[])
        for r in rows:
            if 'operation_index' in r:continue
            decisions.append(r)
            if r.get('status','variant')!='variant':continue
            key=(r['volume'],r['component']);t=bykey[key]['text'];target=r['corrected']
            if 'start' in r and t[r['start']:r['start']+len(target)]==target:a=r['start']
            else:
                assert t.count(target)==1,(p.name,r.get('index'),r['component'],t.count(target))
                a=t.index(target)
            priority=130 if p.name.startswith('en_nonmath_') else 125 if p.name.startswith('en_font_') else 110
            cohort=('prose, reference or bibliography reconstruction' if p.name.startswith('en_nonmath_') else
                    'font, accent, scope or equation-tag reconstruction' if p.name.startswith('en_font_') else
                    'reviewed formula or formula-context reconstruction')
            allops.append((priority,{'volume':r['volume'],'component':r['component'],'start':a,'end':a+len(target),
                               'corrected':target,'printed':r['printed'],'source':r.get('source','EN_FORMULA_RESOLUTIONS.json'),
                               'folio':str(r.get('page','?')),'kind':cohort,'method':'individual editorial resolution',
                               'apparatus_note':r['reason'] if r.get('id')=='ED-EN-XX-ANNEXE' else ''}))
    atoms=collections.defaultdict(list);conflicts=[]
    for priority,op in sorted(allops,key=lambda x:-x[0]):
        key=(op['volume'],op['component']);text=bykey[key]['text'];start=op['start']
        assert text[start:op['end']]==op['corrected'],('stale operation',op)
        pending=[];duplicates=[];blocked=[]
        for h in french.token_changes(op['corrected'],op['printed']):
            if french.comments_out(h['before']).strip()==french.comments_out(h['after']).strip():continue
            a=start+h['a0'];b=start+h['a1'];old=text[a:b];new=h['after']
            note_ranges=editorial_spans(text)
            if any(a0<=a<b0 for a0,b0,_,_ in note_ranges):continue
            identical=next((x for x in atoms[key] if x['start']==a and x['end']==b and x['printed']==new),None)
            if identical:
                duplicates.append(identical);continue
            overlaps=[x for x in atoms[key] if not (b<=x['start'] or a>=x['end'])
                      or (a==b and x['start']<=a<=x['end'])
                      or (x['start']==x['end'] and a<=x['start']<=b)]
            if overlaps:
                blocked.append({'candidate':op,'candidate_atom':h,'retained':overlaps,'decision':'Entire lower-priority operation omitted; higher-priority reconstruction retained, avoiding partial structural edits.'});continue
            pending.append({'start':a,'end':b,'corrected':old,'printed':new,'source':op['source'],
                               'folio':op['folio'],'kind':op['kind'],'method':op['method'],'priority':priority,
                               'apparatus_note':op.get('apparatus_note','')})
        # A TeX group is indivisible when two descriptions of the same edit use
        # different token boundaries. Applying only the nonoverlapping residue
        # could delete one brace while retaining its mate. Independent formula
        # changes still compose, because their token ranges do not intersect.
        if blocked:
            conflicts.extend(blocked)
            continue
        for identical in duplicates:identical['source']+='; '+op['source']
        atoms[key].extend(pending)
    (WORK/'en_atomic_operations.json').write_text(json.dumps([{**x,'volume':v,'component':f} for (v,f),xs in atoms.items() for x in xs],ensure_ascii=False,indent=1))
    (WORK/'en_rejected_operations.json').write_text(json.dumps(rejected,ensure_ascii=False,indent=1))
    (REC/'EN_REJECTED_PROPOSAL_DISPOSITIONS.json').write_text(json.dumps(rejected,ensure_ascii=False,indent=1))
    (REC/'EN_SUPERSEDED_PORT_PROPOSALS.json').write_text(json.dumps(superseded_ports,ensure_ascii=False,indent=1))
    (WORK/'en_operation_conflicts.json').write_text(json.dumps(conflicts,ensure_ascii=False,indent=1))
    (REC/'EN_RECONSTRUCTION_DECISIONS.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=1))
    return atoms,rejected,conflicts


def strip_notes(t):
    for a,b,body,kind in reversed(editorial_spans(t)):t=t[:a]+t[b:]
    return t


def original_offset_map(original,current):
    """Map retained reader tokens back to their exact released-source offsets.

    Replaced paragraphs map to their source spans; unchanged tokens map
    character for character. This also prevents removed editorial notes from
    displacing the folio alignment of later authorial paragraphs.
    """
    at=list(french.TOKEN.finditer(original));bt=list(french.TOKEN.finditer(current))
    ao=[m.start() for m in at]+[len(original)];bo=[m.start() for m in bt]+[len(current)]
    blocks=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,[m.group() for m in at],[m.group() for m in bt],autojunk=False).get_opcodes():
        blocks.append((bo[k],bo[l],ao[i],ao[j],tag))
    ends=[x[1] for x in blocks]
    def locate(pos):
        if not blocks:return 0
        pos=max(0,min(len(current),pos));i=min(len(blocks)-1,bisect.bisect_right(ends,pos))
        b0,b1,a0,a1,tag=blocks[i]
        if tag=='equal':return min(a1,a0+max(0,pos-b0))
        if b1==b0:return a1
        return a0+round((a1-a0)*max(0,pos-b0)/(b1-b0))
    return locate


def comment_offset_map(original):
    positions=[];totals=[];removed=0
    for m in re.finditer(r'(?<!\\)%[^\n]*',original):
        positions.append(m.start()-removed);removed+=m.end()-m.start();totals.append(removed)
    def locate(pos):
        i=bisect.bisect_right(positions,pos)-1
        return pos+(totals[i] if i>=0 else 0)
    return locate


def sources_for_hunk(component,current_start,current_end):
    """Attach each contiguous difference to the operation that made it."""
    a=component['_original_offset'](current_start);b=component['_original_offset'](current_end)
    candidates=[x for x in component['variant_sources'] if 'start' in x]
    selected=[x for x in candidates if (x['start']<max(b,a+1) and x['end']>a)
              or (x['start']==x['end'] and a<=x['start']<=b)]
    method='overlapping source operation'
    if not selected and candidates:
        distance=lambda x:max(x['start']-b,a-x['end'],0)
        closest=min(distance(x) for x in candidates)
        selected=[x for x in candidates if distance(x)==closest]
        method='nearest source operation after textual projection; distance '+str(closest)
    assert selected,('unattributed English variant',component['component'],current_start,current_end)
    return selected,method,a,b


def get_source_page(vol,exp,t):
    """Exact numbered-item anchors where unique; otherwise a stated estimate."""
    return None


def source_headings(vol,exp):
    fp=SRC/'fr'/('sga7i' if vol=='7I' else 'sga7ii')/'current'/('general_introduction_body.tex' if exp=='Introduction' else 'expose_'+exp+'_body.tex')
    if not fp.exists():return {}
    t=fp.read_text();marks=list(MARK.finditer(t));mp=[m.start() for m in marks];out=collections.defaultdict(list)
    for m in re.finditer(r'^.*$',t,re.M):
        key=heading_key(m.group())
        if key and marks:
            folio=marks[max(0,bisect.bisect_right(mp,m.start())-1)].group(2)
            if folio not in out[key]:out[key].append(folio)
    return dict(out)


def expose_start(vol,exp):
    if exp=='Introduction':return 'V'
    if exp=='Catalogue':return '525'
    if exp=='XIII':return '82'  # its title is at the end of XII's source file
    p=SRC/'fr'/('sga7i' if vol=='7I' else 'sga7ii')/'current'/('expose_'+exp+'_body.tex')
    m=MARK.search(p.read_text())
    assert m,(vol,exp,'missing source start')
    return m.group(2)


def catalogue_folios():
    p=SRC/'fr/sga7i/current/expose_IX_body.tex';t=p.read_text();marks=list(MARK.finditer(t));out={}
    for i,m in enumerate(marks):
        if not m.group(2).isdigit() or int(m.group(2))<525:continue
        body=t[m.end():marks[i+1].start() if i+1<len(marks) else len(t)]
        for n in re.findall(r'Vol\.\s*([\d ]+)\s*:',body):out[int(n.replace(' ',''))]=m.group(2)
    return out


def heading_key(t):
    t=re.sub(r'\\SGARef(?:Target|Link)\{[^}]*\}\{([^}]+)\}',r'\1',t)
    t=re.sub(r'\\(?:noindent|medskip|smallskip|par)\s*','',t)
    t=re.sub(r'\\(?:underline|textbf|textit|section\*|subsection\*|subsubsection\*)\{','',t)
    t=t.lstrip().replace('}','')
    names={'Théorème':'Theorem','Lemme':'Lemma','Définition':'Definition','Corollaire':'Corollary','Remarque':'Remark','Exemple':'Example','Proposition':'Proposition'}
    m=re.match(r'(Theorem|Lemma|Definition|Corollary|Remark|Example|Proposition|Théorème|Lemme|Définition|Corollaire|Remarque|Exemple)\s+(\d+(?:[.,]\d+)*)',t)
    if m:return names.get(m.group(1),m.group(1))+':'+m.group(2).replace(',','.')
    m=re.match(r'(\d+(?:\.\d+)*)(?:\.\s+|\s*[-–.]\s+)(?=[A-Za-zÀ-ÿ\\])',t)
    return 'Number:'+m.group(1) if m else None


def build_data():
    DEST.mkdir(parents=True,exist_ok=True);REC.mkdir(parents=True,exist_ok=True)
    originals=read(WORK/'en_components.json');candidates=read(WORK/'en_candidates.json')
    atoms,rejected,conflicts=make_operations(originals,candidates)
    decisions=read(REC/'editorial_decisions.json');patches=[r for r in decisions['patches'] if r['language']=='EN']
    explicit=decisions.get('english_variants',[])
    for p in sorted(WORK.glob('en_editorial_body_patch_*.json')):
        r=read(p);patches.append({**r,'language':'EN','file':Path(r['component']).name})
        explicit.append({**r,'file':Path(r['component']).name})
    alignment=read(WORK/'en_alignment.json');byalign=collections.defaultdict(list)
    for x in alignment:byalign[(x['volume'],x['component'])].append(x)
    changes=[];notes=[];parts=[];anchors=[];patch_audit=[];common_repairs=[]
    for c in originals:
        if c['expose']=='VI':continue
        v=c['volume'];fn=c['component'];key=(v,fn);d=cur=c['text'];used=atoms.get(key,[])
        for op in sorted(used,key=lambda x:x['start'],reverse=True):d=d[:op['start']]+op['printed']+d[op['end']:]
        if c['expose']=='Introduction':
            oldref='(I. 4.5)';newref='(I. 4.6)';assert cur.count(oldref)==1
            a=c['text'].index(oldref);cur=cur.replace(oldref,newref,1)
            used.append({'start':a,'end':a+len(oldref),'corrected':newref,'printed':oldref,
                         'source':'ED-EN-INTRO-I4.6; F7I-INTRO-003.2; fr/sga7i/{diplomatic,current}/general_introduction_body.tex',
                         'folio':'V','kind':'verified English correction','method':'exact source reference counterpart'})
            furniture=r'\\clearpage\s*\\thispagestyle\{empty\}\s*\\begin\{center\}\s*(VI|VII)\s*\\end\{center\}'
            for which,text in [('corrected',cur),('diplomatic',d)]:
                text,n=re.subn(furniture,lambda m:'\\SGApage{I}{'+m.group(1)+'}',text)
                assert n==2,('introduction page furniture',which,n)
                if which=='corrected':cur=text
                else:d=text
            patch_audit.append({'id':'ED-EN-INTRO-I4.6','component':fn,'volume':v,'status':'source reference correction in corrected and reading forms; printed4.5 retained diplomatic'})
        if c['expose']=='Catalogue':
            # These two common-layer transcription fixes were omitted by the
            # old port because the catalogue was not input by the release.
            price=re.compile(r'(^Vol\.\s*([\d ]+)\s*:[^\n]*?DM\s+\d+[,\.])-(?!-)',re.M)
            def repair_price(m):
                number=int(m.group(2).replace(' ',''));page='525' if number<=177 else '526'
                assert 111<=number<=245
                return m.group(1)+'--'
            prices=list(price.finditer(cur));assert len(prices)==135,len(prices)
            assert sum(int(m.group(2).replace(' ',''))<=177 for m in prices)==67
            for m in prices:
                pg='525' if int(m.group(2).replace(' ',''))<=177 else '526';fix='C604' if pg=='525' else 'C605'
                common_repairs.append({'id':'ED-EN-CATALOGUE-'+fix,'volume':v,'component':fn,'page':pg,
                                       'before':m.group(),'after':repair_price(m),'source':'fixes/FIXLOG_7I_CURRENT.jsonl#'+fix+'; common diplomatic/current price-dash repair'})
            cur=price.sub(repair_price,cur);d=price.sub(repair_price,d)
            patch_audit.extend([{'id':'ED-EN-CATALOGUE-C604','component':fn,'volume':v,'status':'67 source-recorded price-dash repairs applied to all forms'},
                                {'id':'ED-EN-CATALOGUE-C605','component':fn,'volume':v,'status':'68 source-recorded price-dash repairs applied to all forms'}])
        for r in patches:
            if r['volume']!=v or r['file']!=Path(fn).name:continue
            for layer,text in [('current',cur),('diplomatic',d)]:
                if layer=='current':
                    assert text.count(r['old'])==1,(r['id'],layer,text.count(r['old']))
                    cur=text.replace(r['old'],r['new'],1)
                elif text.count(r['old'])==1:d=text.replace(r['old'],r['new'],1)
                else:
                    # An authorial paragraph restored by a decision supersedes
                    # reconstructions in the released substitute paragraph.
                    original=c['text'];assert original.count(r['old'])==1
                    a=original.index(r['old']);b=a+len(r['old'])
                    da=a+sum(len(o['printed'])-len(o['corrected']) for o in used if o.get('end',10**12)<=a)
                    db=b+sum(len(o['printed'])-len(o['corrected']) for o in used if o.get('end',10**12)<=b)
                    d=d[:da]+r['new']+d[db:]
            patch_audit.append({'id':r['id'],'component':fn,'volume':v,'status':'applied to all English forms'})
        for r in explicit:
            if r['volume']!=v or r['file']!=Path(fn).name:continue
            if r['corrected'] in d:
                assert d.count(r['corrected'])==1,(r['id'],'diplomatic ambiguity')
                d=d.replace(r['corrected'],r['printed'],1)
            elif r['printed'] not in d:
                raise ValueError(('explicit variant conflicts',r['id']))
            original=c['text'];target=r['corrected']
            if original.count(target)==1:a=original.index(target);b=a+len(target)
            else:
                patch=next(z for z in patches if r['id'].startswith(z['id']) and z['file']==r['file'])
                a=original.index(patch['old']);b=a+len(patch['old'])
            provenance=r['id']+'; '+r.get('source','OPEN_ITEMS_DECIDED.tsv')
            if r.get('french_apparatus_ids'):provenance+='; '+', '.join(r['french_apparatus_ids'])
            used.append({'source':provenance,'folio':str(r['page']),'kind':'explicit editorial body or reading decision',
                         'start':a,'end':b,'corrected':r['corrected'],'printed':r['printed']})
        if v=='7I' and fn=='components/136_expose_IX_sections_4_1_through_4_4.tex':
            pass
        # The port's already decision at C857 overlooked the printed prime.
        if v=='7I' and 'this subgroup $I\'$ corresponds to' in cur:
            old="this subgroup $I'$ corresponds to";new='this subgroup $I$ corresponds to'
            assert cur.count(old)==1
            cur=cur.replace(old,new,1)
            a=c['text'].index(old)
            used.append({'source':'EN-REPAIR-C857; fixes/MISPRINTS_7I.json; fixes/FIXLOG_7I_CURRENT.jsonl#C857','folio':'355','kind':'verified English correction',
                         'start':a,'end':a+len(old),'corrected':new,'printed':old})
        component_notes=[]
        for a,b,body,kind in editorial_spans(c['text']):
            aa=byalign.get(key,[]);pos=[z['offset'] for z in aa];i=max(0,bisect.bisect_right(pos,a)-1)
            pg=aa[i]['folio'] if aa else '?'
            note={'id':f'EN-NOTE-{len(notes)+1:03}','volume':v,'expose':c['expose'],'page':pg,'file':c['file'],'text':body,'kind':kind,
                  'original_start':a,'original_end':b}
            notes.append(note);component_notes.append(note)
        cur=strip_notes(cur);d=strip_notes(d)
        old=clean(c['text']);cur=clean(cur);d=clean(d)
        edit_ranges=[(n['original_start'],n['original_end'],'ED-EN-NOTES; '+n['id'],'~'+n['page']) for n in component_notes]
        for r in patches:
            if r['volume']==v and r['file']==Path(fn).name:
                a=c['text'].index(r['old']);edit_ranges.append((a,a+len(r['old']),r['id'],str(r['page'])))
        if c['expose']=='Introduction':
            a=c['text'].index('(I. 4.5)');edit_ranges.append((a,a+len('(I. 4.5)'),'ED-EN-INTRO-I4.6','V'))
            for m in re.finditer(furniture,c['text']):edit_ranges.append((m.start(),m.end(),'ED-EN-PAGE-FURNITURE',m.group(1)))
        if v=='7I' and "this subgroup $I'$ corresponds to" in c['text']:
            target="this subgroup $I'$ corresponds to";a=c['text'].index(target)
            edit_ranges.append((a,a+len(target),'EN-REPAIR-C857','355'))
        old_to_original=comment_offset_map(c['text'])
        for h in french.token_changes(old,cur) if c['expose']!='Catalogue' else []:
            oa=old_to_original(h['a0']);ob=old_to_original(h['a1'])
            hits=[r for r in edit_ranges if (oa<r[1] and ob>r[0]) or (oa==ob and r[0]<=oa<=r[1])]
            assert hits,('unattributed released-English change',v,fn,h,oa,ob)
            source='; '.join(dict.fromkeys(r[2] for r in hits));pg=';'.join(dict.fromkeys(r[3] for r in hits))
            changes.append({'page':v+':'+pg,'place':c['file']+f' [character {h["a0"]}]','before':h['before'],'after':h['after'],'source':source})
        if c['expose']=='Catalogue':
            changes.append({'page':'7I:525–528','place':c['file'],'before':'','after':cur,'source':'ED-EN-CATALOGUE: restore supplied publisher catalogue component excluded from released reader'})
        assert balanced(d)==balanced(cur),(v,fn,'reconstruction changed TeX group balance')
        parts.append({**c,'corrected':cur,'diplomatic':d,'variant_sources':used,'_original_offset':original_offset_map(c['text'],cur)})
    (WORK/'en_final_components.json').write_text(json.dumps([{k:v for k,v in c.items() if not k.startswith('_')} for c in parts],ensure_ascii=False,indent=1))
    # Collate by exposé, then insert source folios identically in both witnesses.
    expos=[];byexp=collections.OrderedDict()
    for c in parts:byexp.setdefault((c['volume'],c['expose']),[]).append(c)
    frdata=read(WORK/'fr_variant_data.json');vi=next(x for x in frdata if x['expose']=='VI')
    allentries=[]
    for (v,ex),cs in byexp.items():
        if v=='7I' and ex=='VII':
            vi_en={**vi,'entries':[{**e,'language':'EN'} for e in vi['entries']]}
            expos.append(vi_en);allentries+=vi_en['entries']
            for m in re.finditer(r'\\SGApage\{I\}\{([^}]+)\}',vi['corrected']):
                anchors.append({'volume':'7I','expose':'VI','folio':m.group(1),'quality':'exact source English Exposé VI folio',
                                'component':'fr/sga7i/current/expose_VI_body.tex','corrected_character':m.start()})
            old='\n\n'.join(clean(c['text']) for c in originals if c['expose']=='VI')
            marker_pattern=r'\\SGApage\{[^}]*\}\{([^}]*)\}'
            new=re.sub(marker_pattern,'',vi['corrected'])
            page_positions=[];removed=0
            for m in re.finditer(marker_pattern,vi['corrected']):
                page_positions.append((m.start()-removed,m.group(1)));removed+=m.end()-m.start()
            page_starts=[p for p,n in page_positions]
            ol,nl=old.splitlines(keepends=True),new.splitlines(keepends=True)
            line_starts=[0]
            for line in nl:line_starts.append(line_starts[-1]+len(line))
            for tag,a,b,c,d in difflib.SequenceMatcher(None,ol,nl,autojunk=False).get_opcodes():
                if tag!='equal':
                    first=page_positions[max(0,bisect.bisect_right(page_starts,line_starts[c])-1)][1]
                    last=page_positions[max(0,bisect.bisect_right(page_starts,max(line_starts[c],line_starts[d]-1))-1)][1]
                    pg=('adjacent to '+first) if c==d else first if first==last else first+'–'+last
                    changes.append({'page':'7I:'+pg,'place':'Exposé VI, original English source','before':''.join(ol[a:b]),'after':''.join(nl[c:d]),'source':'ED-VI-AUTHOR; fr/sga7i/current/expose_VI_body.tex'})
        ctext='';dtext='';meta=[];headings=source_headings(v,ex);lastpg=None
        for comp in cs:
            base=len(ctext);ctext+=comp['corrected']+'\n\n';dtext+=comp['diplomatic']+'\n\n'
            meta.append((base,len(ctext),comp))
        ca=french.paragraphs(ctext);da=french.paragraphs(dtext)
        co=[0];do=[0]
        for s in ca:co.append(co[-1]+len(s))
        for s in da:do.append(do[-1]+len(s))
        annotated=[];entries=[];group=0;catfolios=catalogue_folios() if ex=='Catalogue' else {}
        segments=[]
        for tag,i,j,k,l in difflib.SequenceMatcher(None,da,ca,autojunk=False).get_opcodes():
            if tag=='equal':segments.extend((tag,i+n,i+n+1,k+n,k+n+1) for n in range(j-i))
            else:segments.append((tag,i,j,k,l))
        for tag,i,j,k,l in segments:
            old=''.join(da[i:j]);new=''.join(ca[k:l]);cpos=co[k]
            selected=next((comp for a,b,comp in meta if a<=cpos<b),meta[-1][2])
            aa=byalign.get((v,selected['component']),[]);within=selected['_original_offset'](max(0,cpos-next(a for a,b,c in meta if c is selected)))
            ai=max(0,bisect.bisect_right([z['offset'] for z in aa],within)-1);pg=aa[ai]['folio'] if aa else '?';quality='estimated formula alignment'
            for line in (new or old).splitlines()[:4]:
                hk=heading_key(line)
                if hk in headings and len(headings[hk])==1:pg=headings[hk][0];quality='exact unique numbered-item anchor';break
            if cpos==0:pg=expose_start(v,ex);quality='source exposé start'
            embedded_marker=False
            if ex=='Introduction':
                roman=re.search(r'\\SGApage\{I\}\{(VI|VII)\}',new or old)
                pg=roman.group(1) if roman else lastpg or 'V';quality='source introduction folio';embedded_marker=bool(roman)
            if ex=='Catalogue':
                vm=re.search(r'Vol\.\s*([\d ]+)\s*:',new or old)
                if vm:
                    pg=catfolios[int(vm.group(1).replace(' ',''))];quality='exact source catalogue entry'
                elif 'ISBN' in (new or old):pg='528';quality='exact source terminal ISBN matter'
                else:pg=lastpg or '525';quality='source catalogue boundary'
            marker=''
            if pg!=lastpg:
                foliotex=pg if quality.startswith(('exact','source')) else r'\(\approx\)'+pg
                marker='' if embedded_marker else '\\SGApage{'+('I' if v=='7I' else 'II')+'}{'+foliotex+'}\n'
                anchors.append({'volume':v,'expose':ex,'folio':pg,'quality':quality,'component':selected['component'],'corrected_character':cpos})
                lastpg=pg
            if tag=='equal':annotated.append(marker+new);continue
            hunks=[h for h in french.token_changes(old,new) if re.sub(r'\s+','',h['before'])!=re.sub(r'\s+','',h['after'])]
            if not hunks:
                annotated.append(marker+new);continue
            group+=1;gid=f'E{v}-{ex}-{group:03}'
            for n,h in enumerate(hunks,1):
                hpos=cpos+h['b0'];hend=cpos+h['b1']
                hbase,_,hcomp=next(((a,b,comp) for a,b,comp in meta if a<=hpos<b),meta[-1])
                sources,source_match,oa,ob=sources_for_hunk(hcomp,hpos-hbase,hend-hbase)
                src='; '.join(dict.fromkeys(x['source'] for x in sources))
                epg=next((x['folio'] for x in sources if x.get('folio') not in ['?','']),pg)
                entries.append({**h,'id':gid+'.'+str(n),'group_id':gid,'volume':v,'expose':ex,'page':epg,
                                'source':src,'source_ref':hcomp['file'],'kind':'; '.join(dict.fromkeys(x['kind'] for x in sources)),'language':'EN',
                                'source_match':source_match,'original_start':oa,'original_end':ob,
                                'note':' '.join(dict.fromkeys(x.get('apparatus_note','') for x in sources if x.get('apparatus_note')))})
            annotated.append(marker+'\\SGAvar{'+old+'}{'+new+'}{'+gid+'}')
        expos.append({'volume':v,'expose':ex,'corrected':ctext,'diplomatic':dtext,'annotated':''.join(annotated),'entries':entries})
        allentries+=entries
    (WORK/'en_variant_data.json').write_text(json.dumps(expos,ensure_ascii=False,indent=1))
    (REC/'EN_APPARATUS.json').write_text(json.dumps(allentries,ensure_ascii=False,indent=1))
    (REC/'EN_INHERITED_EDITORIAL_NOTES.json').write_text(json.dumps(notes,ensure_ascii=False,indent=1))
    french.write_tsv(REC/'EN_COMMON_SOURCE_REPAIRS.tsv',['id','volume','component','page','before','after','source'],common_repairs)
    french.write_tsv(REC/'CHANGES_EN.tsv',['page','place','before','after','source'],changes)
    french.write_tsv(REC/'EN_ALIGNMENT.tsv',['volume','expose','folio','quality','component','corrected_character'],anchors)
    (REC/'EN_BUILD_STATUS.json').write_text(json.dumps({'original_components':len(originals),'source_VI_reused':True,'catalogue_restored':True,
                                                      'apparatus_entries':len(allentries),'variant_blocks':sum(len(set(e['group_id'] for e in x['entries'])) for x in expos),
                                                      'inherited_editorial_notes':len(notes),'release_body_changes':len(changes),'anchors':len(anchors),
                                                      'rejected_operations':len(rejected),'rejected_operations_pending':sum('disposition' not in r for r in rejected),
                                                      'operation_conflicts':len(conflicts),'editorial_patches':patch_audit},ensure_ascii=False,indent=2))
    print('English data:',len(expos),'exposés/parts,',len(allentries),'apparatus entries,',len(notes),'inherited notes,',len(changes),'release differences.')
    return expos,notes


def apparatus(entries):
    if not entries:return ''
    out=['\n\\ifnum\\SGAform=1\n\\clearpage\\section*{Critical apparatus}\\begingroup\\small\\raggedright\\sloppy\n',
         'Readings are given in the exact TeX notation of the two English witnesses. Decimal suffixes identify the individual differences in each marked passage.\n']
    for e in entries:
        out.append('\n\\par\\medskip\\noindent\\hypertarget{app-'+e['id']+'}{}\\textbf{'+french.esc(e['id'])+'}\\quad printed folio '+french.esc(e['page'])+'.\\par\n')
        out.append('\\noindent Printed reading: '+french.code(e['before']).replace('(vide)','(empty)')+'\\par\n')
        out.append('\\noindent Corrected reading: '+french.code(e['after']).replace('(vide)','(empty)')+'\\par\n')
        out.append('\\noindent Source: '+french.code(e['source'])+'\\par\n')
        if e.get('note'):out.append('\\noindent Editorial explanation: '+french.esc(e['note'])+'\\par\n')
    out.append('\n\\par\\endgroup\\normalsize\\fi\n');return ''.join(out)


def build_readers(expos,notes):
    pre=french.preamble().replace('SGA 7 I et II - lecteur francais','SGA 7 I and II - English reader')
    pre+=r'''
\providecommand{\Pic}{\operatorname{Pic}}
\providecommand{\uExt}{\underline{\operatorname{Ext}}}
\providecommand{\uTor}{\underline{\operatorname{Tor}}}
\makeatletter
\DeclareRobustCommand{\SGARefTarget}[1]{\mbox{\phantomsection\label{#1}}}
\DeclareRobustCommand{\SGARefAliasTarget}[1]{\mbox{\phantomsection\label{#1}}}
\DeclareRobustCommand{\SGARefLink}[2]{\@ifundefined{r@#1}{#2}{\hyperref[#1]{#2}}}
\let\SGAoriginaltextcircled\textcircled
\DeclareRobustCommand{\textcircled}[1]{\ifmmode\text{\SGAoriginaltextcircled{#1}}\else\SGAoriginaltextcircled{#1}\fi}
\renewcommand{\SGAtoc}[1]{\phantomsection\addcontentsline{toc}{chapter}{#1}\markboth{#1}{#1}}
\makeatother
\tikzcdset{ampersand replacement=\&}
\tikzset{ampersand replacement=\&}
'''
    intro=r'''
\begin{document}\selectlanguage{english}\frontmatter
\begin{titlepage}\centering
{\Large S\'eminaire de g\'eom\'etrie alg\'ebrique du Bois Marie\par}\vspace{20mm}
{\Huge\bfseries SGA 7\par}\vspace{8mm}
{\LARGE Monodromy Groups in Algebraic Geometry\par}\vspace{8mm}
{\Large Volumes I and II\par}\vspace{16mm}
{\Large\ifcase\SGAform Diplomatic text\or Corrected text with apparatus\or Plain reading text\fi\par}\vfill
{\large Edition of 12 November 2026\par}
{\large GPT-6 Astra (OpenAI, ChatGPT Pro mode)\par}
\end{titlepage}
\section*{About this form}
\ifcase\SGAform
The diplomatic form follows the printed readings established by the paired source witnesses. Transcription repairs common to the two witnesses are retained. Expos\'e VI reproduces the original English directly.
\or
The corrected form follows the released English, the shared original English of Expos\'e VI, and the explicit editorial decisions. Every passage different from the diplomatic form is marked. The apparatus records each difference and its source. Inherited editorial notes and questions retained for review are presented separately.
\or
This is the corrected text without variant marks, critical apparatus, inherited editorial explanations, or unresolved-reading notes. The authorial text, authorial notes, bibliographies, and supplied publisher catalogue are retained. Printed folios appear in the margins only.
\fi
The margin labels refer to the original print, independently of this book's page numbers. An approximation sign marks an estimated English alignment between mathematical anchors; exact numbered-item matches are unqualified. The original English of Expos\'e VI retains every source folio marker. Expos\'es III--V do not exist as separate written texts.
'''
    body=[];last=None
    for c in expos:
        v,ex=c['volume'],c['expose']
        if v!=last:body.append('\\part{SGA 7 '+('I' if v=='7I' else 'II')+'}\n');last=v
        title='General introduction' if ex in ['Introduction','INTRO'] else 'Publisher catalogue' if ex=='Catalogue' else 'Exposé '+ex
        body.append('\\clearpage\\SGAtoc{'+title+'}\n\\selectlanguage{english}\n')
        body.append(tex_safe(c['annotated']))
        body.append('\\markboth{'+title+'}{'+title+'}\n'+apparatus(c['entries']))
    body.append('\n\\ifnum\\SGAform=1\\clearpage\\chapter*{Inherited editorial notes}\\small\\raggedright\\sloppy\n')
    body.append('These notes are inherited from the released English. They are preserved here as provenance records, separate from the variant apparatus and the authorial text.\n')
    for n in notes:
        body.append('\\par\\medskip\\noindent\\textbf{'+n['id']+'} '+french.esc(n['volume']+' '+n['expose']+'; approximate folio '+n['page'])+'\\par\n'+french.code(n['text'])+'\\par\n')
    unresolved=(WORK/'unresolved_en.tex').read_text() if (WORK/'unresolved_en.tex').exists() else ''
    body.append('\n\\normalsize\n'+unresolved+'\n\\fi\n')
    front=(WORK/'frontmatter_en.tex').read_text()
    master=pre+intro+front+'\n\\tableofcontents\n\\mainmatter\n'+''.join(body)+'\n\\end{document}\n'
    master=master.replace('FORM_NUMBER','1')
    (DEST/'SGA7_EN_annotated_master.tex').write_text(master)
    for name,mode in [('SGA7_EN_diplomatic',0),('SGA7_EN_corrected_apparatus',1),('SGA7_EN_reading',2)]:
        t=master.replace('\\SGAform=1\n','\\SGAform='+str(mode)+'\n',1)
        (DEST/(name+'.tex')).write_text(t)
    print('English annotated master and three single-file forms written.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--data-only',action='store_true');args=parser.parse_args()
    inputs=[WORK/name for name in ['en_components.json','en_candidates.json','en_port_operations.json','en_formula_operations.json','en_proposal_supersessions.json','fr_variant_data.json','frontmatter_en.tex','unresolved_en.tex']]
    inputs += [REC/'editorial_decisions.json']
    for pattern in ['en_formula_resolutions_*.json','en_formula_accepted_audit_*.json','en_port_witness_audit_*.json',
                    'en_font_resolutions_*.json','en_nonmath_resolutions_*.json','en_editorial_body_patch_*.json']:
        inputs.extend(sorted(WORK.glob(pattern)))
    inputs += [ROOT/'build'/name for name in ['english.py','english_stage.py','english_variants.py','english_manual.py','french.py']]
    fingerprints={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    data,notes=build_data()
    if not args.data_only:build_readers(data,notes)
    changed=[name for name,digest in fingerprints.items() if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest]
    assert not changed,('editorial input changed during build; rerun to obtain one coherent snapshot',changed)
    (REC/'EN_BUILD_INPUTS.json').write_text(json.dumps({'inputs':fingerprints,'coherent_snapshot_verified':True},ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()
