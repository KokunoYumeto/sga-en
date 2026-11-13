from __future__ import annotations
import argparse,json,re,subprocess,sys
from pathlib import Path
from sga5_common import *
from prepare_french import make_variants

class EnglishIndex:
    language='EN'
    def __init__(self,variants):
        self.by_page={}
        for v in variants:self.by_page.setdefault(int(v['page']),[]).append(v)
    def sources(self,page,before,after):
        hits=[]
        for v in self.by_page.get(page,[]):
            a=v['before'];b=v['after'];score=0
            if a and (a in before or (before and before in a)):score+=2
            if b and (b in after or (after and after in b)):score+=2
            if not a and not before:score+=1
            if not b and not after:score+=1
            if score>=3:hits.append(v)
        if not hits:return ''
        return '; '.join(dict.fromkeys(['EN_variants_input.json:'+v['id'] for v in hits]+[v['source'] for v in hits]))

def inject(s,events):
    out=[];last=0
    for start,end,new in sorted(events,key=lambda x:(x[0],x[1])):
        assert start>=last,(start,last)
        out.append(s[last:start]);out.append(new);last=end
    out.append(s[last:]);return ''.join(out)

def depth(s):
    n=0;i=0
    while i<len(s):
        if s[i]=='\\':
            m=re.match(r'\\(?:[A-Za-z@]+|.)',s[i:],re.S);i+=len(m[0]);continue
        n+=(s[i]=='{')-(s[i]=='}');i+=1
    return n

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--contributions',default='work/contributions');ap.add_argument('--out',default='work/build/prepared');a=ap.parse_args()
    con=Path(a.contributions);en=con/'english';out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    c=(en/'EN_corrected_flat.tex').read_text();d=(en/'EN_diplomatic_flat.tex').read_text()
    vs=json.loads((en/'EN_variants.json').read_text());align=json.loads((en/'EN_ALIGNMENT.json').read_text())
    ordered=sorted(vs,key=lambda v:v['start_corrected']);delta=0;scan_events={'corrected':[],'diplomatic':[]};fixed=[];replayed=c
    for v in reversed(ordered):
        start,end=v['start_corrected'],v['end_corrected'];assert c[start:end]==v['after'],v['id']
        replayed=replayed[:start]+v['before']+replayed[end:]
    assert replayed==d,'Input variant replay does not reconstruct diplomatic English'
    for v in ordered:
        start,end=v['start_corrected'],v['end_corrected'];ds=start+delta;de=ds+len(v['before']);assert d[ds:de]==v['before']
        if v['id'].startswith('R98-'):
            tag=r'\SGAFixedVariant{'+v['id']+'}'
            scan_events['corrected'].append((start,end,tag));scan_events['diplomatic'].append((ds,de,tag));fixed.append(v)
        delta+=len(v['before'])-len(v['after'])
    assert len(fixed)==32
    bodies={};pres={};original_body_slices={}
    for branch,text in [('corrected',c),('diplomatic',d)]:
        events=list(scan_events[branch])
        for row in align:
            p=int(row['folio']);pos=row['position_'+branch]
            marker=f'%\n%%%%%%%%%%  scan idx {p+11}  |  folio {p}  %%%%%%%%%%\n'
            events.append((pos,pos,marker))
        marked=inject(text,events);pre,body=split_document(marked)
        first=FOLIO.search(body);assert first and int(first[2])==1
        bodies[branch]=strip_comments(body[first.start():]);pres[branch]=pre
        firstpos=min(x['position_'+branch] for x in align)
        original_body_slices[branch]=text[firstpos:text.rfind(r'\end{document}')]
    assert pres['corrected']==pres['diplomatic']
    aa=list(FOLIO.finditer(bodies['diplomatic']));bb=list(FOLIO.finditer(bodies['corrected']))
    assert [m[2] for m in aa]==[m[2] for m in bb]
    variants=[];parts=[];abuf=bbuf='';startpage=1;idx=EnglishIndex(vs)
    for i,(ma,mb) in enumerate(zip(aa,bb)):
        abuf+=bodies['diplomatic'][ma.start():aa[i+1].start() if i+1<len(aa) else len(bodies['diplomatic'])]
        bbuf+=bodies['corrected'][mb.start():bb[i+1].start() if i+1<len(bb) else len(bodies['corrected'])]
        if depth(abuf)==depth(bbuf)==0:
            parts.append(make_variants(abuf,bbuf,startpage,idx,variants,'EN'));abuf=bbuf=''
            if i+1<len(bb):startpage=int(bb[i+1][2])
    assert not abuf and not bbuf
    master=''.join(parts)
    for v in fixed:
        tag=r'\SGAFixedVariant{'+v['id']+'}';assert master.count(tag)==1
        suffix=following_scripts(master,master.index(tag)+len(tag))
        master=master.replace(tag+suffix,r'\SGAvar{'+v['before']+suffix+'}{'+v['after']+suffix+'}{'+v['id']+'}')
        variants.append({'id':v['id'],'page':v['page'],'expose':'XV','before':v['before']+suffix,'after':v['after']+suffix,'glyph_before':v['before'],'glyph_after':v['after'],'source':'PLACES_98_DECIDED.tsv:'+v['id']+'; conventions/GLOBAL_ISSUES_SGA.md:98','kind':'derived-functor typography','reason':v.get('reason','Direct scan reading.')})
        bodies['diplomatic']=bodies['diplomatic'].replace(tag,v['before']);bodies['corrected']=bodies['corrected'].replace(tag,v['after'])
    master,marker_terminations=terminate_folio_comments(master)
    write_json(out/'EN_marker_terminations.json',marker_terminations)
    for branch,b in bodies.items():(out/f'EN_{branch}_body.tex').write_text(b)
    (out/'EN_preamble.tex').write_text(pres['corrected'])
    (out/'EN_annotated_body.tex').write_text(master)
    write_json(out/'EN_variants.json',variants);write_json(out/'EN_variants_input.json',vs)
    write_json(out/'EN_preparation_summary.json',{'input_variant_count':len(vs),'master_variants':len(variants),'scan_variants':32,'folio_anchor_count':len(align),'distinct_folios':len(set(x['folio'] for x in align)),'input_replay_exact':True,'input_hashes':{'diplomatic':digest(d),'corrected':digest(c)},'body_hashes':{k:digest(v) for k,v in bodies.items()},'original_body_slice_hashes':{k:digest(v) for k,v in original_body_slices.items()},'frontmatter_boundary':'first verified Exposé I anchor; earlier editorial title/credits/contents replaced by the new front matter'})
    # Source labels are resolved through two independently replayed edit paths,
    # after the safe annotation has fixed its final call boundaries. This keeps
    # all body bytes/call IDs and replaces only heuristic source/page metadata.
    audit=con/'validation_en'
    audit_cmd=[sys.executable,str(audit/'audit_english_master.py'),'--english',str(en),'--prepared',str(out),'--output',str(audit)]
    subprocess.run(audit_cmd,check=True)
    subprocess.run([sys.executable,str(audit/'apply_resolved_sources.py'),'--prepared',str(out),'--audit',str(audit)],check=True)
    subprocess.run(audit_cmd,check=True)
    independent=json.loads((audit/'INDEPENDENT_EN_MASTER_AUDIT.json').read_text())
    assert independent['passed'],'Independent English preservation/source-resolution audit failed'
    print(json.dumps({'language':'EN','input_variants':len(vs),'master_variants':len(variants),'folio_anchors':len(align),'distinct_folios':len(set(x['folio'] for x in align))}))

if __name__=='__main__':main()
