"""Reproducible French diplomatic/corrected/reading build from the supplied ZIP trees.

The master contains exact source-controlled alternatives. Generation changes only
SGAForm (0 diplomatic, 1 apparatus, 2 reading); no independent reader editing.
"""
from fr_core import *
import argparse, collections, hashlib
import bisect, subprocess, os, unicodedata

REC=OUT/'records'; FR=OUT/'fr'; WORK=ROOT/'work_fr'
for p in [REC,FR,WORK]:p.mkdir(parents=True,exist_ok=True)
DROOT=SRC/'fr/D_diplomatic_after_scan_check'
EROOT=SRC/'fr/E_corrected_after_scan_check'
AROOT=SRC/'fr/A_orgogozo_snapshot_71766d9'

def load_layer(root,file,branch,records=None):
    text=(root/file/(file+'.tex')).read_text()
    text=explicit_pages(text,file)
    return replace_sisi(body(text),branch,records,file)

def restore_commented(text,file,diplomatic):
    if file=='01':
        pat=r'(?m)^%\\\[\\vcenter\{\n%\\xymatrix@C=2\.5cm@R=1\.5cm.*?^%\\\]'
        m=re.search(pat,text,re.S|re.M)
        if m:text=text[:m.start()]+re.sub(r'(?m)^%','',m.group())+text[m.end():]
    if file=='05bis':
        a=text.index('%Or pour toute flèche')
        b=text.index('\n\n\nOn peut supposer',a)
        printblock=re.sub(r'(?m)^%','',text[a:b])
        end=text.index("Soit $[X'/X]^p$",b)
        if diplomatic:text=text[:a]+printblock+'\n\n'+text[end:]
        else:
            # Restore the page-138 folio at the corresponding editorial replacement.
            mark=re.search(r'\\SGApageno\{\d\}\{\d+\}',printblock).group()
            text=text[:a]+mark+'\n'+text[b:end]+text[end:]
    return text

def raw_layer(root,file,branch,records=None):
    t=load_layer(root,file,branch,records)
    return t

def safe_literal(value):
    if not value or len(value)>1100:return False
    return not re.search(r'\b(?:no final|missing|misprint|instead of|printed as|plain text|no period|without a|unreadable|illegible|superscript|subscript)\b',value,re.I)

def local_edits(old,new):
    """Exact aligned deltas, avoiding unmatched contextual tails of reported excerpts."""
    toks=lambda x:re.findall(r'\\[A-Za-z]+|\\.|[A-Za-zÀ-ÿ]+|[0-9]+|[^\s]',x)
    a=toks(old);b=toks(new)
    op=list(difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes())
    out=[]
    for tag,i,j,k,l in op:
        if tag=='equal':continue
        # An excerpt often ends earlier than the scan quotation: do not infer deletion.
        if tag in ('insert','delete') and (i==0 or j==len(a) or k==0 or l==len(b)):
            continue
        if tag=='replace' and (j-i>8 or l-k>8):continue
        # Reconstruct the original spelling, including spaces, from exact token spans.
        def span(s,t,i,j):
            mm=list(re.finditer(r'\\[A-Za-z]+|\\.|[A-Za-zÀ-ÿ]+|[0-9]+|[^\s]',s))
            return s[mm[i].start():mm[j-1].end()] if j>i else ''
        aa=span(old,a,i,j);bb=span(new,b,k,l)
        if aa or bb:out.append((aa,bb))
    return out

def prepare():
    dip={};corr={};base={};org=[];placements=[];changes=[]
    for f in FILES:
        dip[f]=restore_commented(raw_layer(DROOT,f,0,org),f,True)
        corr[f]=restore_commented(raw_layer(EROOT,f,1),f,False)
        base[f]=raw_layer(EROOT,f,1)
    for r in org:r['source']=f"Fabrice Orgogozo; transmitted sisi record in fr/D_diplomatic_after_scan_check/{r['file']}/{r['file']}.tex; original A readings preserved in the original-human supplement."
    disputed={(str(x['tome']),int(x['page'])) for x in json.loads((SRC/'api_pass_20261111/PAGES_FOR_APP_CHECK.json').read_text())}
    hand=[]
    for i,r in enumerate(json.loads((SRC/'fixes/REPLAY_MANUAL_4.json').read_text())):
        if r['status']!='by hand':continue
        f=r['file'];ident='H'+str(i);status='';evidence=''
        if (str(r['tome']),int(r['page'])) in disputed:
            status='held-disputed-page';evidence='The page is in PAGES_FOR_APP_CHECK.json; no new replay is applied.'
        else:
            already=bool(find_exact(corr[f],r['new'],r['page']))
            newtext,patch=(corr[f],None) if already else replace_one(corr[f],r['old'],r['new'],r['page'])
            if patch:
                corr[f]=newtext;status='placed';evidence='Exact whitespace-insensitive match to the recorded old text.'
                changes.append({'id':ident,'file':f,'page':r['page'],'printed':patch[2],'corrected':patch[3],'source':ident,'kind':'hand replay'})
            elif already:
                status='already-present-in-corrected-reading';evidence='The recorded new text is present after resolving the source editorial alternatives.'
            else:
                status='needs-location-review';evidence='Neither full recorded old nor full recorded new excerpt matches uniquely.'
                checked={
                    'H17':(r'$\Top(X)_{/p^*(U)}','The corrected source already has the required slice denominator p^*(U), using the source asterisk token.'),
                    'H101':(r'\Hom(k^{\ast}_XK, Rf^{!}_Vk^{\ast}L)','The bottom-left vertex already has k_X^*K without the spurious comma; its other existing source correction is preserved.'),
                    'H112':(r'(R^{2}i^{!})','Formula (3.3.2) already has the functor i^! in the correct position; the existing cohomological degree 2 is preserved.')}
                adapted={
                    'H33':(r'(X, \check{\Hh}^{0}(M)),',r'(X, \Hh^{0}(M)),','The closing-parenthesis repair is already present; remove the remaining spurious check from the first H^0 in (2.4.6.1).'),
                    'H102':(r'$H^{0}(U,\GG_{m})/H^{0}(U,\GG_{m})^{n}$',r'$H^{0}(U,\GG_{m})/(H^{0}(U,\GG_{m}))^{n}$','Place the recorded denominator grouping in the proof of 1.3; the source had already removed the unmatched closing parenthesis.'),
                    'H121':('séparable,\nqui équivaut','séparable,\nce qui équivaut','The source already removed infinity; restore the remaining recorded word ce.')}
                if ident in checked:
                    anchor,reason=checked[ident]
                    assert len(find_exact(corr[f],anchor,r['page']))==1,ident
                    status='already-present-in-corrected-reading';evidence=reason
                elif ident in adapted:
                    aa,bb,reason=adapted[ident]
                    corr[f],patch=replace_one(corr[f],aa,bb,r['page']);assert patch,ident
                    status='placed-adapted-to-existing-correction';evidence=reason
                    changes.append({'id':ident,'file':f,'page':r['page'],'printed':patch[2],'corrected':patch[3],'source':ident,'kind':'hand replay'})
        hand.append({'id':ident,'expose':EXP[f],'page':r['page'],'place':r.get('where',''),'before':r['old'],'after':r['new'],'status':status,'evidence':evidence})
    writejson(WORK/'initial_layers.json',{'dip':dip,'corr':corr,'base':base,'org':org,'changes':changes})
    tsv(REC/'HAND_REPLAYS_PLACED.tsv',hand,['id','expose','page','place','before','after','status','evidence'])
    print('Hand replays:',dict(collections.Counter(x['status'] for x in hand)))
    unresolved=[x for x in hand if x['status']=='needs-location-review']
    writejson(WORK/'hand_unresolved.json',unresolved)
    # Analyze literal anchors before making uncertain transcription changes.
    mis=json.loads((SRC/'fixes/MISPRINTS_4.json').read_text())
    for i,r in enumerate(mis,1):
        f=INV[r['expose']];page=r['page'];ident=f'MP{i:04d}';sub=[]
        for model,rr in r['readings'].items():
            old=rr.get('scan','');new=rr.get('corrected','');tex=rr.get('tex','')
            oldhits=find_exact(corr[f],old,page);newhits=find_exact(corr[f],new,page);texhits=find_exact(corr[f],tex,page)
            sub.append({'model':model,'scan':old,'corrected':new,'tex':tex,'old_matches':len(oldhits),'new_matches':len(newhits),'tex_matches':len(texhits),'deltas':local_edits(old,new)})
        placements.append({'id':ident,'file':f,'expose':r['expose'],'page':page,'place':r['where'],'readings':sub})
    writejson(WORK/'misprint_anchors.json',placements)
    print('Agreed misprints with literal corrected anchor:',sum(any(x['new_matches']==1 for x in r['readings']) for r in placements),'of',len(placements))
    print('Agreed misprints with literal print anchor:',sum(any(x['old_matches']==1 for x in r['readings']) for r in placements),'of',len(placements))
    print('Orgogozo source records:',len(org))

def balanced_delta(a,b):
    def bal(x):
        x=re.sub(r'\\[{}$]','',x)
        return x.count('{')-x.count('}'),x.count('$')%2
    return bal(a)==bal(b)

def pairs_for(old,new):
    pairs=[]
    if safe_literal(old) and safe_literal(new):
        ratio=difflib.SequenceMatcher(None,old,new,autojunk=False).ratio()
        tokens=lambda z:re.findall(r'\\[A-Za-z]+|\\.|[A-Za-zÀ-ÿ]+|[0-9]+|[^\s]',z)
        ta,tb=tokens(old),tokens(new)
        ops=difflib.SequenceMatcher(None,ta,tb,autojunk=False).get_opcodes()
        conservative=all(tag=='equal' or (tag=='replace' and j-i==l-k) for tag,i,j,k,l in ops)
        if ratio>=.55 and len(ta)==len(tb) and balanced_delta(old,new) and conservative:pairs.append((old,new,'full recorded reading'))
        for a,b in local_edits(old,new):
            if a and b and balanced_delta(a,b) and len(tokens(a))==len(tokens(b))==1 and len(a)<80 and len(b)<80:pairs.append((a,b,'aligned exact token delta'))
    # Order is deliberately longest first, to avoid replacing an unrelated short symbol.
    return sorted(set(pairs),key=lambda p:-len(p[0]))

def apply_pair(text,old,new,page):
    if old==new:return text,'unresolved',None
    nh=find_exact(text,new,page);oh=find_exact(text,old,page)
    if len(oh)==1 and len(nh)==0:
        text,patch=replace_one(text,old,new,page)
        return text,'placed',patch
    if len(nh)==1 and len(oh)==0:return text,'already-present',None
    return text,'unresolved',None

def correct_misprints():
    data=json.loads((WORK/'initial_layers.json').read_text());dip=data['dip'];corr=data['corr'];changes=data['changes'];ledger=[];unresolved=[]
    mis=json.loads((SRC/'fixes/MISPRINTS_4.json').read_text())
    from fr_manual import PAIRS
    reviewed=set(PAIRS)
    for path in sorted(set(list((OUT/'shared').glob('MP_*PATCHES.json'))+list((OUT/'shared').glob('MP*PAIRS.json')))):
        reviewed.update(r['id'] for r in json.loads(path.read_text()))
    for i,r in enumerate(mis,1):
        f=INV[r['expose']];page=r['page'];ident=f'MP{i:04d}';subs=[]
        for model,rr in [('canonical', {'scan':r['print'],'corrected':r['correct'],'tex':r['tex_did']})]:
            old=rr.get('scan','');new=rr.get('corrected','');tex=rr.get('tex','')
            def unmath(v):
                v=v.strip()
                return v[1:-1] if v.startswith('$') and v.endswith('$') and v.count('$')==2 else v
            try:atex=unmath(replace_sisi(tex,0))
            except ValueError:atex=unmath(tex)
            try:btex=unmath(replace_sisi(new,1))
            except ValueError:btex=unmath(new)
            pairs=pairs_for(atex,btex) if f in FILES[:9] and ident not in reviewed else []
            # Literal French words can also recover silent spelling corrections.
            # Scan descriptions and informal mathematical renderings are never inserted as TeX.
            if f in FILES[:9] and ident not in reviewed and re.fullmatch(r"[A-Za-zÀ-ÿ\s,;:!?'.’()\-]+",old) and re.fullmatch(r"[A-Za-zÀ-ÿ\s,;:!?'.’()\-]+",new):
                pairs+=pairs_for(old,new)
            dc=[];cc=[];done=[]
            for a,b,method in pairs:
                # Tiny mathematical tokens require context: a bare index/letter is not an address.
                if a==b or len(a)<=2 or len(b)<=2:continue
                cor2,cs,cp=apply_pair(corr[f],a,b,page)
                dip2,ds,dp=apply_pair(dip[f],b,a,page)
                if cs=='unresolved' and ds=='unresolved':continue
                if cp:
                    corr[f]=cor2;changes.append({'id':ident+'-'+model,'file':f,'expose':r['expose'],'page':page,'printed':cp[2],'corrected':cp[3],'source':ident,'kind':'agreed misprint','method':method})
                if dp:dip[f]=dip2
                cc.append(cs);dc.append(ds);done.append({'old':a,'new':b,'method':method,'corrected':cs,'diplomatic':ds})
                # A complete quotation subsumes its aligned local deltas.
                if method=='full recorded reading' and cs!='unresolved' and ds!='unresolved':break
            cseen=bool(find_exact(corr[f],btex,page))
            dseen=bool(find_exact(dip[f],atex,page)) and atex!=btex
            status='represented' if cseen and dseen and atex!=btex else 'represented' if done and 'unresolved' not in cc and 'unresolved' not in dc else 'partly-resolved' if done or cseen or dseen else 'needs-location-review'
            subs.append({'model':model,'status':status,'scan':old,'corrected':new,'tex':tex,'patches':done})
        row={'id':ident,'expose':r['expose'],'file':f,'page':page,'place':r['where'],'readings':subs}
        row['status']='represented' if all(x['status']=='represented' for x in subs) else 'needs-location-review'
        ledger.append(row)
        if row['status']!='represented':unresolved.append(row)
    data.update({'dip':dip,'corr':corr,'changes':changes})
    writejson(WORK/'corrected_layers.json',data)
    writejson(REC/'AGREED_MISPRINTS_PLACEMENT.json',ledger)
    writejson(WORK/'misprints_unresolved.json',unresolved)
    writejson(REC/'FR_APPLIED_PATCHES.json',changes)
    print('Misprint coverage:',dict(collections.Counter(x['status'] for x in ledger)))
    print('Subreading statuses:',dict(collections.Counter(x['status'] for r in ledger for x in r['readings'])))

def integrate_reviewed():
    from fr_manual import PAIRS,ALREADY,CORR_EXTRA,DIP_EXTRA
    data=json.loads((WORK/'corrected_layers.json').read_text());dip=data['dip'];corr=data['corr'];changes=data['changes']
    ledger=json.loads((REC/'AGREED_MISPRINTS_PLACEMENT.json').read_text());byid={r['id']:r for r in ledger};audit=[]
    for ident,pairs in CORR_EXTRA.items():
        r=byid[ident];f=r['file'];page=r['page']
        for a,b in pairs:
            if find_exact(corr[f],b,page):continue
            corr[f],patch=replace_one(corr[f],a,b,page,global_fallback=True)
            if patch:changes.append({'id':ident,'file':f,'expose':EXP[f],'page':page,'printed':a,'corrected':b,'source':ident,'kind':'agreed misprint','method':'Adaptation to the existing E corrected spelling'})
    for ident,pairs in DIP_EXTRA.items():
        r=byid[ident];f=r['file'];page=r['page']
        for a,b in pairs:
            if find_exact(dip[f],b,page):continue
            dip[f],patch=replace_one(dip[f],a,b,page,global_fallback=True)
            if patch:changes.append({'id':ident,'file':f,'expose':EXP[f],'page':page,'printed':b,'corrected':a,'source':ident,'kind':'agreed misprint','method':'Restoration of the documented printed reading'})
    def apply_explicit(ident,f,page,a,b,reason):
        states={};patches=[]
        for key,layer,old,new in [('dip',dip,b,a),('corr',corr,a,b)]:
            oh=find_exact(layer[f],old,page);nh=find_exact(layer[f],new,page)
            if not nh:
                globalnew=find_exact(layer[f],new,None)
                if len(globalnew)==1:nh=globalnew
            ok,_=searchable(old);nk,_=searchable(new)
            if ok!=nk and ok in nk:oh=[z for z in oh if not any(x<=z[0] and z[1]<=y for x,y in nh)]
            if ok!=nk and nk in ok:nh=[z for z in nh if not any(x<=z[0] and z[1]<=y for x,y in oh)]
            if key=='dip' and nh:states[key]='already-present';continue
            if len(oh)==1:
                from marker_projection import carry_markers
                x,y=oh[0];replacement=carry_markers(layer[f][x:y],new)
                result=layer[f][:x]+replacement+layer[f][y:];patch=(x,y,layer[f][x:y],replacement)
            elif not oh and nh:states[key]='already-present';continue
            else:result,patch=replace_one(layer[f],old,new,page,global_fallback=True)
            if patch:layer[f]=result;states[key]='placed';patches.append(key)
            else:states[key]='needs-location-review'
        if ident in ALREADY and find_exact(corr[f],ALREADY[ident],page):states['corr']='already-present-existing-source-spelling'
        changes.append({'id':ident,'file':f,'expose':EXP[f],'page':page,'printed':a,'corrected':b,'source':ident,'kind':'agreed misprint','method':reason,'states':states})
        audit.append({'id':ident,'file':f,'page':page,'printed':a,'corrected':b,**states})
        return states
    for ident,pairs in PAIRS.items():
        r=byid[ident];states=[]
        for a,b in pairs:states.append(apply_explicit(ident,r['file'],r['page'],a,b,'Manual exact contextual placement of canonical record'))
        if all('needs-location-review' not in x.values() for x in states):r['status']='represented-manual'
        r['manual']=states
    external_paths=list((OUT/'shared').glob('MP_*PATCHES.json'))+list((OUT/'shared').glob('MP*PAIRS.json'))
    for path in sorted(set(external_paths)):
        for r in json.loads(path.read_text()):
            f=r['file'];page=r['page'];ident=r['id'];states={}
            for key,layer in [('dip',dip),('corr',corr)]:
                if key not in r or not r[key]:states[key]='needs-location-review';continue
                a,b=r[key]['old'],r[key]['new']
                result,patch=replace_one(layer[f],a,b,page,global_fallback=True)
                if patch:layer[f]=result;states[key]='placed'
                elif find_exact(layer[f],b,page):states[key]='already-present'
                else:states[key]='needs-location-review'
            if ident in byid:
                byid[ident].setdefault('external',[]).append(states)
                byid[ident]['status']='represented-manual' if all('needs-location-review' not in st.values() for st in byid[ident]['external']) else 'needs-location-review'
            changes.append({'id':ident,'file':f,'expose':EXP[f],'page':page,'printed':r['printed'],'corrected':r['corrected'],'source':ident,'kind':'agreed misprint','method':r.get('reason','Exact reviewed source pair'),'states':states})
            audit.append({'id':ident,'file':f,'page':page,'printed':r['printed'],'corrected':r['corrected'],**states})
    data.update({'dip':dip,'corr':corr,'changes':changes})
    for row in ledger:
        if row['status']=='represented-manual':
            for reading in row['readings']:
                reading.setdefault('initial_literal_status',reading['status'])
                reading['status']='represented-manual'
                reading['final_evidence']='Exact reviewed canonical pairs and final branch checks; see manual/external states and FR_APPLIED_PATCHES.json.'
    writejson(WORK/'corrected_layers.json',data);writejson(REC/'FR_APPLIED_PATCHES.json',changes)
    writejson(REC/'AGREED_MISPRINTS_PLACEMENT.json',ledger);writejson(WORK/'manual_placement_audit.json',audit)
    print('After reviewed placement:',dict(collections.Counter(r['status'] for r in ledger)))

def integrate_one_model():
    path=REC/'one_model_edits.json'
    if not path.exists():return
    data=json.loads((WORK/'corrected_layers.json').read_text());report=[]
    for r in json.loads(path.read_text()):
        f=r['file'];page=r['page'];ident=r['id']
        if r.get('on_disputed_page') or r.get('application')=='hold-disputed-page':
            report.append({'id':ident,'page':page,'expose':EXP[f],'status':'held-disputed-page','evidence':'No text change; the recorded page remains pending scan review.'});continue
        if ident=='OM-SOL-0352':
            report.append({'id':ident,'page':page,'expose':EXP[f],'status':'needs-location-review','evidence':'The six bounded factors are integrated after all earlier reviewed corrections, including OM-SOL-0353.'});continue
        ps=[]
        for seg in r.get('segments',[]):
            if seg.get('method')=='verified-local-tex':ps.append((seg['printed'],seg['corrected'],'verified local TeX'))
            else:ps.extend(pairs_for(seg['printed'],seg['corrected']))
        # Keep full contextual pairs before lexical deltas.
        ps=sorted(set(ps),key=lambda x:-len(x[0]));states=[]
        for a,b,method in ps:
            if not a or not b or len(a)<=2 or len(b)<=2:continue
            ss={}
            for key,old,new in [('dip',b,a),('corr',a,b)]:
                if find_exact(data[key][f],new,page):ss[key]='already-present';continue
                text,patch=replace_one(data[key][f],old,new,page)
                if patch:data[key][f]=text;ss[key]='placed'
                else:ss[key]='needs-location-review'
            if all(s=='needs-location-review' for s in ss.values()):continue
            data['changes'].append({'id':ident,'file':f,'expose':EXP[f],'page':page,'printed':a,'corrected':b,'source':ident,'kind':'accepted one-model misprint','method':method,'states':ss})
            states.append(ss)
            if method in ('full recorded reading','verified local TeX') and all(s!='needs-location-review' for s in ss.values()):break
        status='represented' if states and any(all(s!='needs-location-review' for s in x.values()) for x in states) else 'needs-location-review'
        report.append({'id':ident,'page':page,'expose':EXP[f],'status':status,'evidence':json.dumps(states,ensure_ascii=False)})
    writejson(WORK/'corrected_layers.json',data);writejson(REC/'FR_APPLIED_PATCHES.json',data['changes'])
    tsv(REC/'ONE_MODEL_PLACEMENT_FR.tsv',report,['id','page','expose','status','evidence'])
    print('One-model placement:',dict(collections.Counter(x['status'] for x in report)))

def integrate_reviewed_one_model():
    path=OUT/'shared/ONE_MODEL_FR_PATCHES.json'
    if not path.exists():return
    data=json.loads((WORK/'corrected_layers.json').read_text());audit=[]
    report=list(csv.DictReader((REC/'ONE_MODEL_PLACEMENT_FR.tsv').open(),delimiter='\t'))
    byid={r['id']:r for r in report};statesby=collections.defaultdict(list)
    rows=json.loads(path.read_text())
    repairs=OUT/'shared/ONE_MODEL_FR_AUTO_REPAIRS.json'
    if repairs.exists():rows+=json.loads(repairs.read_text())
    supplement=OUT/'shared/ONE_MODEL_FR_0352_SUPPLEMENT.json'
    if supplement.exists():rows+=json.loads(supplement.read_text())
    supplement=OUT/'shared/ONE_MODEL_FR_1326_SUPPLEMENT.json'
    if supplement.exists():rows+=json.loads(supplement.read_text())
    # Replace the provisional lexical source candidates by the independently
    # reviewed full contexts. A nearby occurrence cannot supply provenance.
    data['changes']=[r for r in data['changes'] if not r['id'].startswith('OM-')]
    for r in rows:
        f=r['file'];page=r['page'];ident=r['id'];states={}
        assert byid[ident]['status']!='held-disputed-page'
        for key in ['dip','corr']:
            a,b=r[key]['old'],r[key]['new'];text=data[key][f]
            # This reviewed repair was located after the common glyph decision;
            # integration precedes that decision, so use the source cardinal
            # token here and project both branches together below.
            if ident=='OM-SOL-0113':a=a.replace(r'\pi',r'\Pi');b=b.replace(r'\pi',r'\Pi')
            result,patch=replace_one(text,a,b,page,global_fallback=True)
            if patch:data[key][f]=result;states[key]='placed'
            elif len(find_exact(text,b,page))==1:states[key]='already-present'
            else:states[key]='needs-location-review'
        printed=r.get('joint_printed',r['printed']);corrected=r.get('joint_corrected',r['corrected'])
        data['changes'].append({'id':ident,'file':f,'expose':EXP[f],'page':page,'printed':printed,'corrected':corrected,'source':ident,'kind':'accepted one-model misprint','method':r.get('placement_note',r.get('reason','Reviewed exact source pair')),'states':states,'represented_by':r.get('represented_by')})
        for related in r.get('related_ids',[]):data['changes'].append({'id':related,'file':f,'expose':EXP[f],'page':page,'printed':printed,'corrected':corrected,'source':related,'kind':'accepted one-model misprint','method':'Joint exact span: retain the separately accepted delimiter repair while applying the bounded first-factor correction.'})
        if r.get('editorial_decision'):data['changes'].append({'id':r['editorial_decision'],'file':f,'expose':EXP[f],'page':page,'printed':printed,'corrected':corrected,'source':r['editorial_decision'],'kind':'explicit editorial scope decision','method':r['reason']})
        audit.append({'id':ident,'part':r.get('part',1),'file':f,'page':page,**states})
        statesby[ident].append(states)
    for ident,states in statesby.items():
        byid[ident]['status']='represented-manual' if all('needs-location-review' not in z.values() for z in states) else 'needs-location-review'
        byid[ident]['evidence']=json.dumps(states,ensure_ascii=False)
    full_auto=OUT/'shared/ONE_MODEL_FR_AUTO_AUDIT_PAIRS.json'
    if full_auto.exists():
        repaired={r['id'] for r in json.loads(repairs.read_text())} if repairs.exists() else set()
        for r in json.loads(full_auto.read_text()):
            if r['id'] in repaired:continue
            data['changes'].append({'id':r['id'],'file':r['file'],'expose':EXP[r['file']],'page':r['page'],'printed':r['printed'],'corrected':r['corrected'],'source':r['id'],'kind':'accepted one-model misprint','method':r.get('reason','Independently verified full source context')})
    writejson(WORK/'corrected_layers.json',data);writejson(REC/'FR_APPLIED_PATCHES.json',data['changes'])
    writejson(WORK/'reviewed_one_model_placement_audit.json',audit)
    tsv(REC/'ONE_MODEL_PLACEMENT_FR.tsv',report,['id','page','expose','status','evidence'])
    print('After reviewed one-model placement:',dict(collections.Counter(x['status'] for x in report)))

def edition_decisions():
    data=json.loads((WORK/'corrected_layers.json').read_text());decisions=[]
    counts={};locations={}
    for layer in ['dip','corr']:
        text=data[layer]['01'];start=text.index(r'\etiquette[8.13]{I.sec8.13}');end=text.index(r'\section{Glossaire}',start)
        protected=[]
        for mm in re.finditer(r'\\(?:nde|ndetext)\s*\{',text):
            _,ee=group(text,text.find('{',mm.start()));protected.append((mm.start(),ee))
        hits=[];records=[]
        for mm in re.finditer(r'\\Pi(?![A-Za-z@])',text[start:end]):
            a=start+mm.start();b=start+mm.end()
            if any(x<=a<y for x,y in protected):continue
            if re.search(r'(?<!\\)%',text[text.rfind('\n',0,a)+1:a]):continue
            # This occurrence denotes the product of the I_alpha. Its token is
            # preserved; all other occurrences in this scope denote cardinals.
            if re.match(r'\\Pi_\{\\alpha\}\s*I_\{\\alpha\}',text[a:]):continue
            hits.append((a,b));records.append({'page':page_at(text,a,'01'),'before':text[max(start,a-36):min(end,b+44)]})
        for a,b in reversed(hits):text=text[:a]+r'\pi'+text[b:]
        data[layer]['01']=text;counts[layer]=len(hits);locations[layer]=records
    decisions.append({'id':'FR-ED93-PI','file':'01','page':'136–178','before':r'\Pi','after':r'\pi','decision':'Use the same printed small-pi glyph for the cardinal throughout the bounded scope I §8.13 through the end of §9. Both scan-check model records identify this glyph in pp.136–145 and 171–175; the connected notation continues through the cardinal-filtration discussion. Preserve the product operator I=Pi_alpha I_alpha at p.163, notes, and all Pi tokens outside this scope.','counts':counts,'source':'method/GLOBAL_ISSUES_SGA.md#93; api_pass_20261111/COORDINATOR_NOTES.md','occurrences':locations})
    for ident,f,pages,old,new,reason in [
        ('FR-ED93-CHAMP','05',list(range(65,81)),r'\mathsf{e}',r'\mathcal{C}','Both scan-check models describe script C for the champ; retain that notation in all forms.'),
        ('FR-ED93-IV492','04',[492],r'\hyperref[IV.sec1]{1}',r'\hyperref[IV.sec1]{IV~1}','Both model records explicitly retain the exposé prefix in the pair III 4 et IV 1; the existing hyperrefext prints III 4 and is retained.'),
        ('FR-ED93-IV494','04',[494],r'\hyperref[IV.rem1.8]{1.8}',r'\hyperref[IV.rem1.8]{IV~1.8}','Both model records explicitly retain the printed exposé prefix in this reference.'),
        ('FR-ED93-IV495','04',[495],r'\hyperref[IV.subsec5.2]{5.2}',r'\hyperref[IV.subsec5.2]{IV~5.2}','Both model records explicitly retain the printed exposé prefix in this reference.'),
    ]:
        counts={}
        for layer in ['dip','corr']:
            text=data[layer][f];hits=[]
            for page in pages:
                for a,b in find_exact(text,old,page):
                    if page_at(text,a,f)==page:hits.append((a,b))
            hits=sorted(set(hits),reverse=True)
            for a,b in hits:text=text[:a]+new+text[b:]
            data[layer][f]=text;counts[layer]=len(hits)
        decisions.append({'id':ident,'file':f,'page':','.join(map(str,pages)),'before':old,'after':new,'decision':reason,'counts':counts,'source':'method/GLOBAL_ISSUES_SGA.md#93; api_pass_20261111/COORDINATOR_NOTES.md'})
    decisions += [
        {'id':'FR-ED90','page':'II219–263;III265–297','decision':'Replace every inherited page counter with explicit PAGES.json tome/folio markers; original II/III offsets no longer propagate.'},
        {'id':'FR-ED91-I34','page':'I34','decision':'Restore the source-commented diagram 5.13.2 in all forms without rewriting it.'},
        {'id':'FR-ED91-Vbis138','page':'Vbis138','decision':'Restore the source-commented printed proof in diplomatic; retain the existing Orgogozo rewrite in corrected, with its source dossier and restored page marker.'},
        {'id':'FR-ED92','page':'see disputed-place ledger','decision':'Keep all previously agreed empty-set transcriptions; no additional phi-to-empty-set substitution without the scan.'},
        {'id':'FR-ED93-EQREF','page':'V32–33','decision':'Retain eqhyperref punctuation pending the scan; no blanket parenthesis deletion is made.'},
        {'id':'FR-ED93-PP','page':'all','decision':'The common PP macro prints plain P in all forms, following the instructed printed notation.'},
        {'id':'FR-ED93-LABELS','page':'all','decision':'The common enonce* environment prints statement labels in capitals, following the instructed printed labels.'},
        {'id':'FR-TEX-SISI-SPACES','page':'all; observed XIV151 display','decision':'On inlining an editorial alternative, represent its single leading or trailing end-line as the space token TeX originally read inside the argument. Keep internal paragraphs. Insert a swallowed delimiter after a control word adjoining a letter. This preserves TeX token boundaries and prevents a new paragraph or merged command created by source concatenation.'},
        {'id':'FR-TEX-GLYPHS','page':'all','decision':'Provide the source spelling car as a math operator in the diplomatic typo, le/ge aliases for leq/geq, and the ordinal superscript-o glyph as text superscript o. In literal apparatus quotations, print Unicode mathematical letters in the installed math font. No mathematical token is substituted by a new proposed reading.'},
        {'id':'FR-TEX-STANDALONE','page':'all','decision':'Inline the supplied packages, theorem definitions, numbering and notation macros into a standard amsbook document; remove the source git-status shell invocation. Use the explicit recorded folio markers and the SGAForm selector for all three forms.'},
        {'id':'FR-TEX-RUNNINGHEADS','page':'all','decision':'The running header identifies the exposé by its number, avoiding clipping of long titles. Complete chapter and section titles are retained in the body and contents.'},
        {'id':'FR-ED94','page':'listed in README','decision':'No source is invented for the untranscribed summary pages, front matter, or indexes.'},
    ]
    writejson(REC/'FR_EDITION_DECISIONS.json',decisions);writejson(WORK/'corrected_layers.json',data)

def preamble():
    cfg=EROOT/'fichiers-configuration-latex'
    packages=(cfg/'paquets.tex').read_text()
    sty=(cfg/'smfthm.sty').read_text().split('\\endinput')[0]
    sty=re.sub(r'\\ProvidesPackage\{smfthm\}\[[^]]*\]','',sty)
    packages=packages.replace(r'\usepackage{../fichiers-configuration-latex/smfthm}', '\\makeatletter\n'+sty+'\n\\makeatother')
    packages=packages.replace(r'\setmainfont[Ligatures=TeX]{Linux Libertine O}',r'\IfFontExistsTF{Linux Libertine O}{\setmainfont[Ligatures=TeX]{Linux Libertine O}}{\setmainfont{Latin Modern Roman}}')
    packages=packages.replace(r'\setmathfont{XITS Math}',r'\IfFontExistsTF{XITS Math}{\setmathfont{XITS Math}}{\setmathfont{Latin Modern Math}}')
    num=(cfg/'numerotation.tex').read_text()
    mac=(cfg/'macros.tex').read_text()
    a=mac.index('\\catcode`\\%=12');b=mac.index('% macros pour LaTeX',a)
    mac=mac[:a]+r'\def\showgitstatus{SGA 4, lecteurs 2026-11-12}'+'\n'+mac[b:]
    # Shared notation macros take the documented printed form in every reader.
    num+=r'\def\sisi#1#2{#1}'+'\n'
    return r'''% Self-contained SGA 4 French reader, generated from SGA4_FR_master_annote.tex.
% SGAForm: 0 diplomatic; 1 corrected with apparatus; 2 reading.
\providecommand\SGAForm{1}
\documentclass[12pt]{amsbook}
\usepackage[a4paper,left=3cm,right=3cm,marginparwidth=1.1cm,marginparsep=.55cm,vmargin=2.8cm]{geometry}
'''+packages+'\n'+num+'\n'+mac+r'''
\providecommand{\nderef}[1]{la N.D.E.~(\ref{#1}) page~\pageref{#1}}
\providecommand{\car}{\operatorname{car}}
\providecommand{\le}{\leq}
\providecommand{\ge}{\geq}
\newcommand{\SGAordinalo}{\textsuperscript{o}}
\begingroup\catcode`ᵒ=\active\gdefᵒ{\SGAordinalo}\endgroup
\catcode`ᵒ=\active
\def\sisi#1#2{#1}
\renewcommand{\PP}{P}
\makeatletter
\AtBeginDocument{\renewenvironment{enonce*}[2][plain]{\let\smfenonce\relax\theoremstyle{#1}\newtheorem*{smfenonce}{#2}\begin{smfenonce}}{\end{smfenonce}}}
\let\SGAoriginalheadings\ps@headings
\def\SGAexposehead{SGA 4}
\newif\ifSGAmaintext
\def\ps@headings{\SGAoriginalheadings
  \def\@evenhead{\normalfont\scriptsize\rlap{\thepage}\hfil\ifSGAmaintext\SGAexposehead\else\leftmark{}{}\fi\hfil}
  \def\@oddhead{\normalfont\scriptsize\hfil\ifSGAmaintext\SGAexposehead\else\rightmark{}{}\fi\hfil\llap{\thepage}}}
\pagestyle{headings}
\makeatother
\long\def\nde#1{\ifnum\SGAForm=2\relax\else\stepcounter{cnote}\begingroup\renewcommand\thefootnote{\arabic{cnote}}\footnote[\value{cnote}]{N.D.E. (F. Orgogozo) : #1}\endgroup\fi}
\def\ndemark{\ifnum\SGAForm=2\relax\else\stepcounter{cnote}\begingroup\renewcommand\thefootnote{\arabic{cnote}}\footnotemark[\value{cnote}]\endgroup\fi}
\long\def\ndetext#1{\ifnum\SGAForm=2\relax\else\begingroup\renewcommand\thefootnote{\arabic{cnote}}\footnotetext[\value{cnote}]{N.D.E. (F. Orgogozo) : #1}\endgroup\fi}
\newcommand\SGApageno[2]{\setcounter{pageoriginal}{#2}\marginpar{\footnotesize\textbf{#1:#2}}\xspace}
\newcommand\SGAvmark[2]{\ifnum\SGAForm=1\relax\ifmmode{}^{\scriptscriptstyle\text{\hyperlink{sgav.#1}{v#2}}}\else\textsuperscript{\scriptsize\hyperlink{sgav.#1}{v#2}}\fi\allowbreak\fi}
\newcommand\SGAdmark[1]{\ifnum\SGAForm=1\relax\ifmmode{}^{\scriptscriptstyle\text{\hyperlink{#1}{#1?}}}\else\textsuperscript{\scriptsize\hyperlink{#1}{#1?}}\fi\allowbreak\fi}
\emergencystretch=2em
\begin{document}
\frontmatter
\begin{titlepage}\centering
{\LARGE SGA 4\par}\vspace{1cm}
{\Large Théorie des topos et cohomologie étale des schémas\par}\vspace{1cm}
{\large M. Artin, A. Grothendieck, J.-L. Verdier\par}\vspace{1cm}
Tomes 1, 2 et 3\par\bigskip
\ifcase\SGAForm Forme diplomatique\or Texte corrigé avec apparat\or Texte de lecture\fi\par
\vfill GPT-6 Astra (OpenAI, ChatGPT Pro mode)\par 12 novembre 2026
\end{titlepage}
'''

def quote_tex(s):
    out=[]
    for c in sanitize(s):
        if c=='\u2009':out.append(r'\hspace{0.16667em}')
        elif c=='~':out.append(r'\textasciitilde{}')
        elif unicodedata.category(c)=='Sm' or ord(c)>=0x1d400 or 0x0370<=ord(c)<=0x03ff or 0x2100<=ord(c)<=0x214f:
            out.append(r'\ensuremath{'+c+'}')
        else:out.append(escaped(c))
        if c in '{}[]()_=+,-;/':out.append(r'\allowbreak ')
    return ''.join(out).replace('\n',' ').replace(r'\textbackslash{}',r'\textbackslash{}\allowbreak ')

def editorial_reference_appendix():
    text=raw_layer(AROOT,'18',1)
    a=text.index(r'\begin{thebibliography}')
    b=text.index(r'\end{thebibliography}',a)
    text=text[a:b];matches=list(re.finditer(r'\\bibitem\{([^}]+)\}',text))
    wanted={'0','0bis','0ter','2bis','3bis','3ter','4bis','5bis'};records=[]
    parts=[r'''\begingroup
\renewcommand{\bibname}{Références éditoriales de Fabrice Orgogozo}
\begin{thebibliography}{99}\small
\item[] Ces références sont les ajouts bibliographiques de Fabrice Orgogozo
dans sa source originale 71766d9. Elles permettent de résoudre les appels de
ses notes N.D.E. sans modifier la bibliographie imprimée. Les numéros
reprennent leur place dans sa bibliographie éditoriale complète.
''']
    for n,m in enumerate(matches,1):
        key=m.group(1)
        if key not in wanted:continue
        end=matches[n].start() if n<len(matches) else len(text)
        content=text[m.end():end].strip()
        globalkey='SGA4-18:'+key
        entry=r'\setcounter{enumiv}{'+str(n-1)+'}\n'+r'\bibitem{'+globalkey+'} '+content+'\n'
        parts.append(entry)
        records.append({'id':'FR-ORG-BIB-'+key,'source':'fr/A_orgogozo_snapshot_71766d9/18/18.tex','original_key':key,'global_key':globalkey,'original_editorial_number':n,'text':content,'placement':'diplomatic-only attributed editorial-reference appendix','decision':'FR-ORG-REFERENCES'})
    assert {r['original_key'] for r in records}==wanted
    parts.append(r'\end{thebibliography}\endgroup'+'\n')
    writejson(REC/'ORGOGOZO_EDITORIAL_REFERENCES_FR.json',records)
    return ''.join(parts)

def uppercase_statement_labels(text):
    # Only literal heading letters change case. Commands (notably footnotemark)
    # and mathematical tokens keep their original tokens and execution order.
    pattern=re.compile(r'(\\begin\{enonce\*\}(?:\[[^]]*\])?\{)([A-Za-zÀ-ÿŒœ \n’\-]+)')
    return pattern.sub(lambda m:m.group(1)+m.group(2).upper(),text)

_SOURCE_RECORDS=None
_SOURCE_DECISIONS=[]

def source_spans(a,b,f):
    global _SOURCE_RECORDS
    if _SOURCE_RECORDS is None:
        _SOURCE_RECORDS=json.loads((REC/'FR_APPLIED_PATCHES.json').read_text())
        data=json.loads((WORK/'corrected_layers.json').read_text())
        for r in data['org']:
            rr=dict(r);rr['printed']=replace_sisi(rr['printed'],0);rr['corrected']=replace_sisi(rr['corrected'],1)
            _SOURCE_RECORDS.append(rr)
        for n,line in enumerate((SRC/'fixes/FIXLOG_4.jsonl').read_text().splitlines(),1):
            r=json.loads(line);_SOURCE_RECORDS.append({'id':f'AF{n:04d}','file':r['file'].split('/')[0],'page':r['page'],'printed':r['old'],'corrected':r['new']})
    spans=[];indices={'a':ExactIndex(a),'b':ExactIndex(b)}
    for r in _SOURCE_RECORDS:
        if r['file']!=f:continue
        old,new=r.get('printed',''),r.get('corrected','')
        # The convention projects the same attested cardinal token on both sides.
        if f=='01' and 136<=int(r['page'])<=178:
            def cardinal_glyph(z):return re.sub(r'\\Pi(?![A-Za-z@])(?!(?:_\{\\alpha\}\s*I_\{\\alpha\}))',lambda m:r'\pi',z)
            old=cardinal_glyph(old);new=cardinal_glyph(new)
        ka,_=searchable(old);kb,_=searchable(new)
        spacing_only=ka==kb and visible_projection(old)!=visible_projection(new)
        if ka==kb and not spacing_only:continue
        ops=[z for z in difflib.SequenceMatcher(None,ka,kb,autojunk=False).get_opcodes() if z[0]!='equal']
        for side,text,needle in [('a',a,old),('b',b,new)]:
            hits=indices[side].find(needle,r['page'])
            if not hits:
                globalhits=indices[side].find(needle,None)
                if len(globalhits)==1:hits=globalhits
            if len(hits)!=1:continue
            start,end=hits[0];key,positions=searchable(text[start:end])
            if spacing_only:
                spans.append((side,start,end,r['id']));continue
            for tag,i,j,k,l in ops:
                lo,hi=(i,j) if side=='a' else (k,l)
                if lo>len(positions) or hi>len(positions):continue
                left=start+(positions[lo] if lo<len(positions) else end-start)
                right=start+(positions[hi-1]+1 if hi>lo else (positions[lo] if lo<len(positions) else end-start))
                spans.append((side,left,right,r['id']))
    return spans

def source_for(f,rawa,rawb,rawold_a,rawold_b,oldtext,newtext,spans,ident,page):
    ids=re.findall(r'SGA4-CORR-\d{4}',newtext[rawa:rawb])
    for side,start,end,source in spans:
        lo,hi=(rawold_a,rawold_b) if side=='a' else (rawa,rawb)
        if (start<hi and end>lo) or (start==end and lo<=start<hi):ids.append(source)
    if uppercase_statement_labels(oldtext[rawold_a:rawold_b])==newtext[rawa:rawb] and oldtext[rawold_a:rawold_b]!=newtext[rawa:rawb]:ids.append('FR-ED93-LABELS')
    if not ids:
        decision='FR-STATE-'+ident
        _SOURCE_DECISIONS.append({'id':decision,'expose':EXP[f],'page':page,'decision':'Retain the exact corrected source-of-record reading over the diplomatic source-of-record reading at this source-diff span.','source':f'fr/D_diplomatic_after_scan_check/{f}/{f}.tex; fr/E_corrected_after_scan_check/{f}/{f}.tex','variant':ident})
        ids=[decision]
    return '; '.join(dict.fromkeys(ids))

def diffs(a,b,f,prefix):
    spans=source_spans(a,b,f)
    mappeda,amap=strip_comments_map(a)
    mappedb,bmap=strip_comments_map(b)
    aa=mappeda.splitlines(keepends=True);bb=mappedb.splitlines(keepends=True)
    apos=[0];bpos=[0]
    for line in aa:apos.append(apos[-1]+len(line))
    for line in bb:bpos.append(bpos[-1]+len(line))
    cleanb=''.join(bb);cleana=''.join(aa);out=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,aa,bb,autojunk=True).get_opcodes():
        if tag=='equal':continue
        old=''.join(aa[i:j]);new=''.join(bb[k:l])
        if not old.strip() and not new.strip():continue
        if prefix=='FRV' and visible_projection(old)==visible_projection(new):continue
        n=len(out)+1;ident=f'{prefix}-{f}-{n:04d}'
        page=page_at(cleanb,bpos[k],f)
        rawa=bmap[bpos[k]];rawb=bmap[bpos[l]]
        rawold_a=amap[apos[i]];rawold_b=amap[apos[j]]
        source=source_for(f,rawa,rawb,rawold_a,rawold_b,a,b,spans,ident,page)
        reported={int(z['page']) for z in _SOURCE_RECORDS if z['file']==f and z['id'] in source.split('; ') and (z['id'].startswith('MP') or z['id'].startswith('OM-'))}
        if len(reported)==1:page=next(iter(reported))
        out.append({'id':ident,'file':f,'expose':EXP[f],'page':page,'place':f'Exposé {EXP[f]}, folio {page}, source line {k+1}','printed':old,'corrected':new,'source':source,'offset':bpos[k],'kind':'correction'})
    return out,cleana,cleanb

def safe_variant_anchors(text):
    safe=[0];depth=0;math=None;envs=[];items=[]
    textual={'enonce*','enonce','enumerate','itemize','description','quote','quotation','center','flushleft','flushright','thebibliography'}
    lists={'enumerate','itemize','description','thebibliography'}
    def safe_environment():return all(e in textual and (e not in lists or items[n]) for n,e in enumerate(envs))
    tokens=re.compile(r'\\(?:begin|end)\{[^}]+\}|\\[A-Za-z@]+|\\.|\$\$|[{}$]|\n[ \t]*\n+')
    for m in tokens.finditer(text):
        token=m.group()
        if token.startswith(r'\begin{'):envs.append(token[7:-1]);items.append(False)
        elif token.startswith(r'\end{'):
            name=token[5:-1]
            if envs and envs[-1]==name:envs.pop();items.pop()
            if not depth and not math and safe_environment():safe.append(m.end())
        elif token in (r'\item',r'\bibitem'):
            for n in range(len(envs)-1,-1,-1):
                if envs[n] in lists:
                    if items[n] and not depth and not math and safe_environment():safe.append(m.start())
                    items[n]=True;break
        elif token=='{':depth+=1
        elif token=='}':depth=max(0,depth-1)
        elif token in ('$', '$$'):math=None if math==token else (token if not math else math)
        elif token in (r'\[',r'\('):math=token
        elif token in (r'\]',r'\)'):
            math=None
            if not depth and safe_environment():safe.append(m.end())
        elif token.startswith('\n') and not depth and not math and safe_environment():safe.append(m.start())
    return sorted(set(safe+[len(text)]))

def annotate(text,rows):
    # Mark the textual unit containing the change, outside all math/alignment
    # grammars and macro arguments. Exact excerpts remain in the linked entry.
    safe=safe_variant_anchors(text)
    inserts=collections.defaultdict(list)
    for r in rows:
        target=min(len(text),r['offset']+len(r['corrected']))
        at=safe[min(len(safe)-1,bisect.bisect_left(safe,target))]
        r['marker_offset']=at;r['marker_page']=page_at(text,at,r['file'])
        r['marker_method']='First complete paragraph, displayed formula, or environment boundary after the exact changed span; outside macro arguments and alignment grammars.'
        inserts[at].append(r['id'])
    for at,ids in sorted(inserts.items(),reverse=True):
        text=text[:at]+''.join(r'\SGAvmark{'+i+'}{'+str(int(i.split('-')[-1]))+'}' for i in ids)+text[at:]
    return text

_DISPUTE_ANCHORS=[]

def annotate_disputes(text,file):
    rows=[r for r in json.loads((OUT/'shared/disputes_index.json').read_text()) if r['file']==file]
    inserts=collections.defaultdict(list);safe=safe_variant_anchors(text);index=ExactIndex(text)
    for r in rows:
        marker=re.search(r'\\SGApageno\{'+str(r['tome'])+r'\}\{'+str(r['page'])+r'\}',text)
        if marker:
            candidates=[]
            for records in r.get('readings',{}).values():
                if not isinstance(records,list):continue
                for rr in records:
                    needles=[rr.get('tex','')]
                    if isinstance(rr.get('fix'),dict):needles.append(rr['fix'].get('old',''))
                    for needle in needles:
                        if len(needle.strip())<8:continue
                        try:needle=replace_sisi(needle,1)
                        except ValueError:continue
                        hits=index.find(needle,r['page'])
                        if len(hits)==1:candidates.append((len(needle),hits[0][1],needle))
            if candidates:
                length,target,anchor=max(candidates);method='unique exact recorded TeX or old-reading anchor'
            else:target=marker.end();anchor=marker.group();method='recorded folio marker; full disputed location given in the appendix'
            at=safe[min(len(safe)-1,bisect.bisect_left(safe,target))]
            inserts[at].append(r['id'])
            _DISPUTE_ANCHORS.append({'id':r['id'],'file':file,'page':r['page'],'anchor':anchor,'method':method,'marker_page':page_at(text,at,file),'offset':at})
    for at,ids in sorted(inserts.items(),reverse=True):text=text[:at]+''.join(r'\SGAdmark{'+i+'}' for i in ids)+text[at:]
    return text

def assemble():
    data=json.loads((WORK/'corrected_layers.json').read_text());dip=data['dip'];corr=data['corr'];variants=[];changes=[]
    documentary=[
        {'id':'FR-ORG-REFERENCES','page':'XVIII587; diplomatic backmatter','decision':'Preserve the eight bibliography entries added by Fabrice Orgogozo at A71766d9 in a separately attributed diplomatic-only appendix. Keep their exact entry texts and original editorial ordinals; namespace their citation keys to the existing SGA4-18 keys so the retained human NDE calls resolve. The printed bibliography stays at its original body location.'},
        {'id':'FR-ORG-ORIGINAL-SUPPLEMENT','page':'documentary backmatter','decision':'Label the 1258-record dossier as the transmission in source D. Add the 44 original A71766d9 records whose commands or raw arguments changed in transmission, with explicit A-to-D crosswalks, and the complete original Vbis138 commented proof/editorial rewrite. Preserve these human records in diplomatic and corrected forms, with no change to body readings.'},
        {'id':'FR-ORG-ORIGINAL-NOTES','page':'documentary backmatter','decision':'Preserve all 129 exact original A71766d9 editorial-note arguments (127 direct NDE calls and two acorriger arguments) in an attributed documentary supplement in both diplomatic and corrected forms, including the eight notes in corrected-only text and original arguments changed in transmission. The body readings stay unchanged.'},
        {'id':'FR-TEX-LITERAL-QUOTES','page':'apparatus and human dossiers','decision':'Quote TeX source literally with escaped syntax characters and visible ASCII tilde via textasciitilde. Add a break opportunity after literal ASCII equals signs in the shared dispute/possible-misprint quotations so the long OM-SOL-0929 Hom chain fits the physical page. Break opportunities change only quotation line wrapping. Complete raw arguments and their checksums are retained in the associated machine-readable human records.'},
        {'id':'FR-TEX-STARRED-TOC','page':'generated contents metadata','decision':'The system amsbook class writes starred chapter titles to the contents. Remove an explicit addcontentsline only when it immediately follows chapter* and repeats exactly the same plain title. Preserve the chapter heading and all body/note arguments.'},
    ]
    decisionpath=REC/'FR_EDITION_DECISIONS.json'
    current=json.loads(decisionpath.read_text())
    merged={r['id']:r for r in current}
    merged.update({r['id']:r for r in documentary})
    writejson(decisionpath,list(merged.values()))
    intro=(OUT/'shared/frontmatter_FR.tex').read_text()
    parts=[preamble(),intro,r'''\chapter*{Préface des lecteurs}
Les numéros marginaux donnent le tome et le folio de l'édition imprimée.
Les trois formes sont générées par le même maître annoté, en changeant seulement SGAForm.
\ifnum\SGAForm=2
Le texte de lecture omet l'apparat des variantes, les dossiers non tranchés,
les corrections consignées comme notes et les notes N.D.E. de l'édition Orgogozo.
Le texte mathématique corrigé reste celui de la forme avec apparat.
\else
Les notes N.D.E. et les dossiers « Orgogozo » sont le travail de l'éditeur humain.
Les variantes de cette construction portent un identifiant de source.
Les désaccords sans scan restent signalés sans décision textuelle.
\fi
\tableofcontents
\mainmatter
\SGAmaintexttrue
\def\danslelivre{1}
\def\thechapter{\Roman{chapter}}
\def\chaptername{Exposé}
''']
    for f in FILES:
        print('Assembling',EXP[f],flush=True)
        vv,dd,cc=diffs(dip[f],corr[f],f,'FRV');variants.extend(vv)
        expected=[(str(p['tome']),str(p['folio'])) for p in PAGEBY[f]]
        for which,bodytext in [('dip',dd),('corr',cc)]:
            found=re.findall(r'\\SGApageno\{(\d)\}\{(\d+)\}',bodytext)
            assert found==expected,(f,which,'printed-page marker mismatch',len(found),len(expected))
        # Page markers and source-state proof are invariant under the form switch.
        annotated=annotate_disputes(annotate(cc,vv),f)
        dd=uppercase_statement_labels(dd);annotated=uppercase_statement_labels(annotated)
        parts.append('\n'+r'\cleardoublepage\gdef\SGAexposehead{Exposé '+EXP[f]+'}\n')
        if f=='05bis':parts.append(r'\renewcommand*{\thechapter}{Vbis}'+'\n')
        if f=='06':parts.append(r'\setcounter{chapter}{5}\def\thechapter{\Roman{chapter}}'+'\n')
        parts.extend(['\n% BEGIN EXPOSE '+EXP[f]+'\n',r'\ifnum\SGAForm=0'+'\n',dd,'\n'+r'\else'+'\n',annotated,'\n'+r'\fi'+'\n'])
        for label,root in [('E',EROOT),('A71766d9',AROOT)]:
            old=raw_layer(root,f,1)
            delta,_,_=diffs(old,uppercase_statement_labels(corr[f]),f,'CHANGE-'+label)
            for r in delta:changes.append({'page':f"{PAGEBY[f][0]['tome']}:{r['page']}",'place':r['place'],'before':r['printed'],'after':r['corrected'],'source':r['source'],'comparison':label,'id':r['id']})
    for label in ['E','A71766d9']:
        for ident,before,after in [
            ('FR-ED93-PP',r'\newcommand{\PP}{\mathbf{P}}',r'\renewcommand{\PP}{P}'),
            ('FR-TEX-STANDALONE','External package/configuration inputs, source git-status shell invocation, and chapter-local builds.','One inline amsbook master; source notation macro definitions select the printed branch; three generated files differ only at SGAForm.'),
            ('FR-ED90',r'\pageoriginale increments the inherited counter.',r'\SGApageno{tome}{folio} prints each explicit PAGES.json folio; II and III do not inherit the wrong offset.'),
            ('FR-TEX-GLYPHS','Font-dependent ordinal superscript-o character, undefined car/le/ge aliases.','The documented glyph/operator compatibility definitions in the standalone preamble.'),
        ]:changes.append({'page':'all','place':'Common standalone preamble','before':before,'after':after,'source':ident,'comparison':label,'id':'CONFIG-'+label+'-'+ident})
    parts.append('\n'+r'\backmatter\SGAmaintextfalse'+'\n'+r'\raggedright\sloppy\emergencystretch=4em'+'\n'+r'\ifnum\SGAForm=1'+'\n'+r'\chapter*{Apparat des variantes}'+'\n')
    for r in variants:
        parts.append(r'\par\medskip\noindent\hypertarget{sgav.'+r['id']+r'}{}\textbf{v'+str(int(r['id'].split('-')[-1]))+' / '+escaped(r['id'])+' -- '+escaped(r['expose'])+', p. '+str(r['page'])+r'}\par\smallskip'+'\n')
        parts.append(r'\noindent\textit{Imprimé / couche diplomatique :} {\small\ttfamily '+quote_tex(r['printed'])+r'}\par'+'\n')
        parts.append(r'\noindent\textit{Texte corrigé :} {\small\ttfamily '+quote_tex(r['corrected'])+r'}\par'+'\n')
        parts.append(r'\noindent\textit{Source :} '+escaped(r['source'])+r'\par'+'\n')
    parts.append((OUT/'shared/disputes_FR.tex').read_text())
    possible=OUT/'shared/possible_misprints_FR.tex'
    if possible.exists():parts.append(possible.read_text())
    parts.append('\n'+r'\fi'+'\n'+r'\ifnum\SGAForm=0'+'\n'+editorial_reference_appendix()+r'\fi'+'\n')
    parts.append(r'\ifnum\SGAForm=2\else'+'\n'+r'\chapter*{Dossiers de Fabrice Orgogozo}'+'\n'+r'\section*{Transmission du dossier humain dans la source D}'+'\n')
    parts.append("Les paires ci-dessous reproduisent leur transmission dans la source diplomatique D. Le supplément consacré à la source originale distingue les lectures de Fabrice Orgogozo à 71766d9 des changements intervenus dans cette transmission."+r'\par'+'\n')
    for r in data['org']:
        parts.append(r'\par\medskip\noindent\textbf{'+escaped(r['id'])+' -- '+escaped(r['expose'])+', p. '+str(r['page'])+r'}\par '+'\n')
        parts.append(r'{\small\textit{Lecture imprimée consignée dans D :} '+quote_tex(r['printed'])+r'\par\textit{Lecture éditoriale transmise dans D :} '+quote_tex(r['corrected'])+r'\par}\noindent Source : transmission du dossier humain de F. Orgogozo dans fr/D\_diplomatic\_after\_scan\_check.\par'+'\n')
    parts.append('\n'+r'\fi'+'\n')
    parts.append((OUT/'shared/HUMAN_ORIGINAL_SUPPLEMENT_FR.tex').read_text())
    parts.append((OUT/'shared/HUMAN_ORIGINAL_NOTES_FR.tex').read_text())
    parts.append('\n'+r'\end{document}'+'\n')
    master=sanitize(''.join(parts))
    tocpattern=re.compile(r'(\\chapter\*\{([^{}]+)\})(\s*)\\addcontentsline\{toc\}\{chapter\}\{\2\}')
    master,toc_deduplicated=tocpattern.subn(lambda m:m.group(1)+m.group(3),master)
    (FR/'SGA4_FR_master_annote.tex').write_text(master)
    for mode,name in [(0,'SGA4_FR_diplomatique'),(1,'SGA4_FR_corrige_apparat'),(2,'SGA4_FR_texte_de_lecture')]:
        (FR/(name+'.tex')).write_text(master.replace(r'\providecommand\SGAForm{1}',r'\providecommand\SGAForm{'+str(mode)+'}',1))
    writejson(REC/'FR_VARIANTS.json',variants)
    writejson(REC/'FR_SOURCE_DECISIONS.json',_SOURCE_DECISIONS)
    writejson(REC/'DISPUTE_MARKERS_FR.json',_DISPUTE_ANCHORS)
    tsv(REC/'CHANGES_FR.tsv',changes,['page','place','before','after','source','comparison','id'])
    sourceids={s.strip() for r in variants for s in r['source'].split(';')}
    placements=list(csv.DictReader((REC/'ONE_MODEL_PLACEMENT_FR.tsv').open(),delimiter='\t'))
    judgements=list(csv.DictReader((REC/'ONE_MODEL_MISPRINTS_JUDGED.tsv').open(),delimiter='\t'))
    writejson(REC/'FR_SOURCE_FREEZE.json',{
        'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(FR.glob('*.tex'))},
        'canonical_misprint_ids':sum(bool(re.fullmatch(r'MP\d{4}',s)) for s in sourceids),
        'accepted_undisputed_one_model_ids':sum(bool(re.fullmatch(r'OM-(?:OPUS|SOL)-\d{4}',s)) for s in sourceids),
        'held_one_model_ids':sum(r['status']=='held-disputed-page' for r in placements),
        'possible_one_model_ids':sum(r['verdict'].startswith('possible') for r in judgements),
        'variant_entries':len(variants),
        'original_human_supplement':'shared/HUMAN_ORIGINAL_SUPPLEMENT_FR.tex',
        'original_human_notes':'shared/HUMAN_ORIGINAL_NOTES_FR.tex',
        'original_editorial_references':8,
        'duplicate_starred_contents_entries_removed':toc_deduplicated,
    })
    print('Readers generated; exact source-diff apparatus entries:',len(variants))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--assemble-only',action='store_true');args=ap.parse_args()
    if not args.assemble_only:
        prepare()
        correct_misprints()
        integrate_reviewed()
        integrate_one_model()
        integrate_reviewed_one_model()
        edition_decisions()
    assemble()
    from fr_changes_audit import build as audit_changes
    audit_changes()
