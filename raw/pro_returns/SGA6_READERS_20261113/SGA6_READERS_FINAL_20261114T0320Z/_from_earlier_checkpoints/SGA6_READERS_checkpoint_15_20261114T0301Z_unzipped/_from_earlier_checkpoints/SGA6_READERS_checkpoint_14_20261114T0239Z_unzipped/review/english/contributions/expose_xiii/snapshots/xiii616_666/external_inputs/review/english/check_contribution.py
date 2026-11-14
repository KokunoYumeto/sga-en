#!/usr/bin/env python3
"""Check a disjoint English contribution without changing assembly records.

The check compares complete literal TeX mathematical units as multisets. It
does not certify prose fidelity, source-image coverage or rendered typography.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH,split

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('directory',type=Path)
    args=ap.parse_args();directory=args.directory
    chunks=[]
    for path in directory.glob('EN_*_P*.tex'):
        m=re.fullmatch(r'EN_.*_P(\d{3})_(\d{3})\.tex',path.name)
        if m:chunks.append((int(m[1]),int(m[2]),path))
    chunks.sort();assert chunks,'No contribution chunks'
    first=chunks[0][0];previous=first-1
    for start,end,path in chunks:
        assert start==previous+1,(path.name,'overlap or gap')
        previous=end
    last=previous
    source=''.join(path.read_text() for _,_,path in chunks)
    markers=[int(n) for n in re.findall(r'\\SGAPrintPage\{(\d+)\}',source)]
    assert markers==list(range(first,last+1)), 'Each local source page requires one ordered visible marker'
    variant_path=directory/'variants.jsonl'
    variants=[json.loads(x) for x in variant_path.read_text().splitlines() if x.strip()] if variant_path.exists() else []
    assert len({x['id'] for x in variants})==len(variants),'Duplicate local variant id'
    pairs_path=directory/'lexical_math_pairs.json'
    pairs=json.loads(pairs_path.read_text()) if pairs_path.exists() else []
    counts=[];differences=[];states={};branch_hashes={}
    for layer,reading in [('current','corrected'),('diplomatic','printed')]:
        text=source
        for v in variants:
            assert first<=v['page']<=last
            for key in ['id','old','printed','corrected','source','reason','scan_image','scan_region','scope_start']:
                assert key in v,(v['id'],key)
            a=text.index(v['scope_start'])
            b=text.index(v['scope_end'],a) if v.get('scope_end') else len(text)
            part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
            text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
        branch_hashes[layer]=sha(text.encode())
        en=split(text);fr,reference=load_reviewed_pages(last,layer,start=first)
        assert set(en)==set(range(first,last+1))
        states[layer]={key:[r for r in reference[key] if first<=r['page']<=last]
                       for key in ['bases','applied_patches','already_present_exact_patches','baseline_differences']}
        for page in range(first,last+1):
            fu=Counter(m.group() for m in MATH.finditer(fr[page]))
            eu=Counter(m.group() for m in MATH.finditer(en[page]))
            missing=fu-eu;extra=eu-fu;approved={}
            for pair in pairs:
                if pair['page']!=page or pair.get('layer','both') not in [layer,'both']:continue
                f=pair['French_literal_unit'];e=pair['English_literal_unit'];n=pair['expected_multiplicity']
                assert missing[f]==extra[e]==n,(page,layer,'pair not present with its exact recorded multiplicity')
                approved[('French',f)]=pair['status'];approved[('English',e)]=pair['status']
            for side,units in [('French',missing),('English',extra)]:
                for unit in units.elements():
                    differences.append(dict(layer=layer,page=page,side=side,literal_unit=unit,
                        status=approved.get((side,unit),'unreviewed literal difference')))
            counts.append(dict(layer=layer,page=page,French_math_units=sum(fu.values()),English_math_units=sum(eu.values()),
                unmatched_French_units=sum(missing.values()),unmatched_English_units=sum(extra.values())))
    result=dict(scope=f'printed{first}–{last}',status='literal source-form comparison only',
        method='Complete equation/align/display/inline TeX units as multisets, with all characters, commands and whitespace retained.',
        source_chunk_sha256s={p.name:sha(p.read_bytes()) for _,_,p in chunks},
        materialized_branch_sha256s=branch_hashes,source_states=states,counts=counts,differences=differences,
        unexpected_difference_units=sum(d['status']=='unreviewed literal difference' for d in differences),
        approved_lexical_difference_side_units=len(differences),
        limitation='A passing result does not verify prose, source-image coverage, macro expansion, PDF typography or global glossary consistency.')
    (directory/'literal_math_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['scope','unexpected_difference_units','approved_lexical_difference_side_units']}))
    for row in differences:
        if row['status']=='unreviewed literal difference':print(json.dumps(row,ensure_ascii=False))
    if result['unexpected_difference_units']:raise SystemExit(2)

if __name__=='__main__':main()
