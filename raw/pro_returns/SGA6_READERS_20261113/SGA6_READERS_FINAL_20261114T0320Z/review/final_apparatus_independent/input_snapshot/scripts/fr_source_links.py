#!/usr/bin/env python3
"""Link each literal French branch edit to its adjudicated source record.

All matching operates on unchanged source strings and explicit positions. No
mathematical or textual normalization is used. The candidate report separates
uncovered edits from proved local literal correspondences.
"""
from pathlib import Path
from collections import defaultdict,Counter
import difflib,json,re

ROOT=Path(__file__).resolve().parents[1]

def jsonl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()] if path.exists() else []

def load_decisions():
    registry=json.loads((ROOT/'build/registry.json').read_text())
    byid={r['id']:r for r in registry}
    aliases={k.replace(':entries#','#'):k for k in byid}
    groups=defaultdict(list)
    for directory in sorted((ROOT/'review').iterdir()):
        if not directory.is_dir():continue
        for name in ['decisions.jsonl','own_findings.jsonl','convention_decisions.jsonl']:
            for row in jsonl(directory/name):
                sid=row.get('source_id',row.get('id'))
                sid=aliases.get(sid,sid)
                row={**row,'source_id':sid,'review_file':(directory/name).relative_to(ROOT).as_posix()}
                groups[sid].append(row)
    choices={r['source_id']:r for r in jsonl(ROOT/'review/merge_resolutions.jsonl')}
    decisions={}
    for sid,rows in groups.items():
        if sid in choices:
            choice=choices[sid]
            selected=[r for r in rows if r['review_file']==choice['primary_review_file']]
            assert len(selected)==1,sid
            d=selected[0].copy();d['reason']+=' '+choice['resolution_reason']
            d['verdict']=choice.get('verdict',d['verdict'])
        else:
            assert len(rows)==1,(sid,'unresolved duplicate')
            d=rows[0]
        assert not d.get('verdict','').startswith('pending'),sid
        decisions[sid]=d
    return registry,byid,decisions

def delta(text_a,text_b):
    return [(i,j,k,l,text_a[i:j],text_b[k:l]) for tag,i,j,k,l in difflib.SequenceMatcher(None,text_a,text_b,autojunk=False).get_opcodes() if tag!='equal']

def common_prefix(a,b):
    n=0
    for x,y in zip(a,b):
        if x!=y:break
        n+=1
    return n

def common_suffix(a,b):return common_prefix(a[::-1],b[::-1])

def candidate_pairs(registry,byid,decisions):
    from build_french import atoms
    result=defaultdict(list);seen=set();branch_pairs=defaultdict(dict)
    def add(d,a,b,label,page_override=None):
        if not isinstance(a,str) or not isinstance(b,str) or a==b:return
        page=str(d.get('page') if page_override is None else page_override)
        key=(page,d['source_id'],a,b)
        if key in seen:return
        seen.add(key)
        result[page].append(dict(source_id=d['source_id'],a=a,b=b,pair_origin=label,
            deltas=delta(a,b),reverse_deltas=delta(b,a),record=d))
    for sid,d in decisions.items():
        if not d.get('image') or not d.get('reason'):continue
        change=d.get('change')
        if isinstance(change,dict):add(d,change.get('old'),change.get('new'),'review.change')
        for other in ['correction','change']:
            add(d,d.get('printed_reading'),d.get(other),'review.printed_reading→'+other)
        raw=byid.get(sid,{}).get('data',{})
        if not d.get('verdict','').startswith('reverted') and d.get('is_misprint') is not False:
            add(d,raw.get('old'),raw.get('new'),'registry.old→new')
            add(d,raw.get('print'),raw.get('correct'),'registry.print→correct')
            fix=raw.get('fix')
            if isinstance(fix,dict):add(d,fix.get('old'),fix.get('new'),'registry.fix')
    for directory in sorted((ROOT/'review').iterdir()):
        if not directory.is_dir():continue
        for p in jsonl(directory/'patches.jsonl')+jsonl(directory/'post_review_patches.jsonl'):
            d=decisions.get(p['source_id'])
            if d:
                # The record's actual named folio, not a pre-marker front key,
                # places the authoritative literal patch on its reviewed leaf.
                add(d,p.get('old'),p.get('new'),directory.relative_to(ROOT).as_posix()+'/[post_review_]patches.jsonl',p['page'] if isinstance(p['page'],int) else None)
                if p.get('layer') in ['current','diplomatic']:
                    branch_pairs[(str(p['page']),p['source_id'],p['old'])][p['layer']]=p['new']
                # Whole-page review patches can start from two different
                # inherited spellings. Their exact TeX-atom edits still give
                # common preimages for each local notation transport.
                pa,pb=atoms(p['old']),atoms(p['new'])
                for tag,i,j,k,l in difflib.SequenceMatcher(None,pa,pb,autojunk=False).get_opcodes():
                    if tag=='equal':continue
                    before=''.join(pa[i:j]);after=''.join(pb[k:l])
                    add(d,before,after,directory.relative_to(ROOT).as_posix()+'/literal patch atom hunk',p['page'] if isinstance(p['page'],int) else None)
                    if p.get('layer') in ['current','diplomatic']:
                        branch_pairs[(str(p['page']),p['source_id'],before)][p['layer']]=after
    for (page,sid,old),branches in branch_pairs.items():
        if 'current' in branches and 'diplomatic' in branches:
            add(decisions[sid],branches['diplomatic'],branches['current'],
                'exact paired branch patches with identical original anchor',page)
    return result

def link(variants,diplomatic_pages,corrected_pages):
    registry,byid,decisions=load_decisions()
    candidates=candidate_pairs(registry,byid,decisions)
    results=[]
    for v in variants:
        page=v['page'];old=v['printed'];new=v['corrected']
        dp=diplomatic_pages[page];cp=corrected_pages[page]
        ai=v['diplomatic_page_offset'];bi=v['corrected_page_offset']
        assert dp[ai:ai+len(old)]==old and cp[bi:bi+len(new)]==new,v['id']
        pieces=[]
        for i,j,k,l,a,b in delta(old,new):
            matches=[]
            for candidate in candidates[str(page)]:
                for reverse in [False,True]:
                    aa,bb=(candidate['b'],candidate['a']) if reverse else (candidate['a'],candidate['b'])
                    d=candidate['record']
                    explicit=('misprint' in str(d.get('kind','')) or d.get('type')=='misprint' or d.get('record_type')=='misprint' or d.get('is_misprint') is True)
                    # A single literal replacement that reconstructs the
                    # complete variant proves all of its character edits,
                    # independently of the diff algorithm's segmentation.
                    if aa and old.count(aa)==1 and old.replace(aa,bb,1)==new:
                        xa=old.index(aa)
                        matches.append(dict(source_id=candidate['source_id'],pair_origin=candidate['pair_origin'],
                            orientation='reverse' if reverse else 'forward',
                            proof='one exact source-pair replacement reconstructs this whole branch variant',
                            source_pair_printed=aa,source_pair_corrected=bb,
                            printed_anchor_offset=xa,corrected_anchor_offset=xa,
                            literal_context_characters=len(old)-len(aa),
                            explicit_misprint_disposition=explicit,
                            score=(1000 if explicit else 0)+750))
                    edits=candidate['reverse_deltas'] if reverse else candidate['deltas']
                    for ci,cj,ck,cl,ca,cb in edits:
                        if (a,b)!=(ca,cb):continue
                        left=min(common_suffix(dp[:ai+i],aa[:ci]),common_suffix(cp[:bi+k],bb[:ck]))
                        right=min(common_prefix(dp[ai+j:],aa[cj:]),common_prefix(cp[bi+l:],bb[cl:]))
                        # The correspondence records every literal context
                        # byte. Very short context is left for manual linkage.
                        evidence_size=len(a)+len(b)+left+right
                        if evidence_size<6 or (left+right<3 and max(len(a),len(b))<5):continue
                        matches.append(dict(source_id=candidate['source_id'],pair_origin=candidate['pair_origin'],
                            orientation='reverse' if reverse else 'forward',source_pair_printed=aa,source_pair_corrected=bb,
                            source_pair_printed_edit=[ci,cj],source_pair_corrected_edit=[ck,cl],
                            common_left_literal=dp[ai+i-left:ai+i],common_right_literal=dp[ai+j:ai+j+right],
                            literal_context_characters=left+right,explicit_misprint_disposition=explicit,
                            score=(1000 if explicit else 0)+min(500,left+right)))
            # Different aliases of a single scanned correction are all kept,
            # with the strongest literal correspondence per authoritative id.
            best={}
            for match in matches:
                sid=match['source_id']
                if sid not in best or match['score']>best[sid]['score']:best[sid]=match
            matches=sorted(best.values(),key=lambda m:(-m['score'],m['source_id']))
            pieces.append(dict(printed_offsets=[i,j],corrected_offsets=[k,l],printed=a,corrected=b,matches=matches))
        results.append(dict(variant_id=v['id'],page=page,printed=old,corrected=new,edits=pieces,
                            uncovered_edits=sum(not p['matches'] for p in pieces)))
    return results,decisions

def main():
    from build_french import atoms
    from intake import split_pages
    variants=[]
    dp,_=split_pages((ROOT/'build/FR_diplomatic_revised.tex').read_text().split(r'\begin{document}',1)[1].rsplit(r'\end{document}',1)[0])
    cp,_=split_pages((ROOT/'build/FR_current_revised.tex').read_text().split(r'\begin{document}',1)[1].rsplit(r'\end{document}',1)[0])
    for page in dp:
        a=atoms(dp[page]);b=atoms(cp[page])
        apos=[0];bpos=[0]
        for s in a:apos.append(apos[-1]+len(s))
        for s in b:bpos.append(bpos[-1]+len(s))
        for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
            if tag=='equal':continue
            variants.append(dict(id=f'FRV{len(variants)+1:04d}',page=page,printed=''.join(a[i:j]),corrected=''.join(b[k:l]),diplomatic_page_offset=apos[i],corrected_page_offset=bpos[k]))
    result,_=link(variants,dp,cp)
    summary=dict(variants=len(result),fully_covered=sum(not r['uncovered_edits'] for r in result),
                 uncovered_variants=sum(bool(r['uncovered_edits']) for r in result),
                 literal_edits=sum(len(r['edits']) for r in result),uncovered_edits=sum(r['uncovered_edits'] for r in result))
    (ROOT/'records/FR_SOURCE_LINK_CANDIDATES.json').write_text(json.dumps(dict(summary=summary,variants=result),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary))
    for r in result:
        if r['uncovered_edits']:
            print(json.dumps(dict(id=r['variant_id'],page=r['page'],uncovered=[{k:p[k] for k in ['printed','corrected']} for p in r['edits'] if not p['matches']]),ensure_ascii=False))

if __name__=='__main__':main()
