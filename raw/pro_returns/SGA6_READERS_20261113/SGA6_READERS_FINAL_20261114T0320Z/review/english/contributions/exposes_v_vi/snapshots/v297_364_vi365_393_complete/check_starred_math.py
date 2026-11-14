#!/usr/bin/env python3
"""Supplement the shared checker with exact ordered starred-display comparison.

The shared equation/align regex intentionally remains unchanged. This report
certifies literal units only, not prose fidelity, scan viewing or PDF rendering.
"""
from pathlib import Path
import collections, hashlib, json, re, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'review/english'))
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split
STAR=re.compile(r'\\begin\{(?P<env>equation\*|align\*)\}.*?\\end\{(?P=env)\}',re.S)
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def main():
    paths=sorted(HERE.glob('EN_*_P*.tex'),key=lambda p:int(re.search(r'_P(\d+)_',p.name).group(1)))
    text=''.join(p.read_text() for p in paths)
    variants=[json.loads(s) for s in (HERE/'variants.jsonl').read_text().splitlines() if s.strip()]
    pages=split(text);first=min(pages);last=max(pages)
    counts=[];differences=[];branch_hashes={}
    for layer,key in [('current','corrected'),('diplomatic','printed')]:
        branch=text
        for v in variants:
            a=branch.index(v['scope_start']);b=branch.index(v['scope_end'],a) if v.get('scope_end') else len(branch)
            part=branch[a:b];assert part.count(v['old'])==1,v['id']
            branch=branch[:a]+part.replace(v['old'],v[key],1)+branch[b:]
        branch_hashes[layer]=sha(branch)
        en=split(branch);fr,_=load_reviewed_pages(last,layer,start=first)
        for page in range(first,last+1):
            fs=[m.group() for m in STAR.finditer(fr[page])];es=[m.group() for m in STAR.finditer(en[page])]
            row=dict(layer=layer,page=page,French_starred_units=len(fs),English_starred_units=len(es),French_unit_sha256s=[sha(s) for s in fs],English_unit_sha256s=[sha(s) for s in es],exact_ordered_equality=fs==es)
            counts.append(row)
            if fs!=es:differences.append(dict(layer=layer,page=page,French_units=fs,English_units=es))
    report=dict(scope=f'printed{first}–{last}',status='supplemental literal comparison of complete equation-star and align-star environments',pattern=STAR.pattern,source_chunk_sha256s={p.name:sha(p.read_text()) for p in paths},materialized_branch_sha256s=branch_hashes,counts=counts,differences=differences,unexpected_differences=len(differences),limitation='Exact unit order and characters only; does not certify prose,source images,macro expansion,or rendered typography.')
    (HERE/'starred_math_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(scope=report['scope'],starred_units=sum(r['French_starred_units'] for r in counts),unexpected_differences=len(differences))))
    assert not differences,differences
if __name__=='__main__':main()
