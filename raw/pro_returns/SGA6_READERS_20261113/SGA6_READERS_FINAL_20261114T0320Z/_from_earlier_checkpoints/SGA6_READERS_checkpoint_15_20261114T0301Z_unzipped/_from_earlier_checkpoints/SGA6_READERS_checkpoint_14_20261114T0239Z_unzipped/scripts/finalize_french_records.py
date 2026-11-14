#!/usr/bin/env python3
"""Complete literal French change streams and final reader invariants."""
from pathlib import Path
import csv,difflib,hashlib,json,re
from intake import write_tsv
ROOT=Path(__file__).resolve().parents[1]

def sha(s):return hashlib.sha256(s.encode()).hexdigest()

def diff_rows(before,after,before_path,after_path,scope):
    a=before.splitlines(keepends=True);b=after.splitlines(keepends=True)
    ops=list(difflib.SequenceMatcher(None,a,b,autojunk=True).get_opcodes())
    rebuilt=[];rows=[]
    for tag,i,j,k,l in ops:
        if tag=='equal':
            assert a[i:j]==b[k:l];rebuilt.extend(a[i:j]);continue
        old=''.join(a[i:j]);new=''.join(b[k:l]);rebuilt.extend(b[k:l])
        prefix=''.join(b[:k]);marks=list(re.finditer(r'(?m)^%+\s*scan idx\s+\d+\s*\|\s*folio\s+([^%\n]+?)\s*%+',prefix))
        page=marks[-1][1].strip() if marks else 'edition-front-and-preamble'
        if r'\section*{Apparat des lectures}' in prefix:page='apparatus'
        rows.append({'scope':scope,'page':page,'place':f'{after_path}: lines {k+1}–{l}',
          'before':old,'after':new,'source':before_path,'after_source':after_path,
          'before_start_line':i+1,'before_end_line':j,'after_start_line':k+1,'after_end_line':l,
          'provenance':'Literal hunk; accepted source edits are individually linked in PATCH_APPLICATION_FR.json and the decision tables. Generated reader material is defined by scripts/build_french.py and scripts/fr_readable_apparatus.py.'})
    assert ''.join(rebuilt)==after,(before_path,after_path,scope)
    return rows,dict(scope=scope,before_source=before_path,after_source=after_path,before_sha256=sha(before),after_sha256=sha(after),changed_hunks=len(rows),exact_reconstruction=True)

def main():
    final=ROOT/'readers/fr/final'
    master=(final/'SGA6_FR_master_annote.tex').read_text()
    forms=[(0,'SGA6_FR_diplomatique.tex'),(1,'SGA6_FR_corrige_apparat.tex'),(2,'SGA6_FR_texte_de_lecture.tex')]
    for mode,name in forms:assert (final/name).read_text()=='\\def\\SGAform{'+str(mode)+'}\n'+master,name
    from build_french import annotate,fit_heading_boxes,anchor_heading_folios,start_exposes_on_new_pages,PAGE
    bodies=[(ROOT/f'build/FR_{name}_revised.tex').read_text().split(r'\begin{document}',1)[1].rsplit(r'\end{document}',1)[0] for name in ['diplomatic','current']]
    annotated,roundtrip_variants=annotate(*bodies,[],[],readable=True)
    blanks={'IV','VI','X','690','rear-715','rear-716'}
    expected=fit_heading_boxes(start_exposes_on_new_pages(anchor_heading_folios(PAGE.sub(lambda m:m[0]+('\n' if m[2].strip() in blanks else '\n\\SGAfolio{'+m[2].strip()+'}%'),annotated))))
    assert master.count(expected)==1,'Actual final master must contain the exact proved annotated body.'
    roundtrip=dict(method='The actual final master contains the exact generated annotated body. Selecting the stored branch fragments, including transported identical lexical tails, reconstructs both complete revised source bodies byte for byte. TikZ delimiter and heading-box transports are separately defined in build_french.py.',
      variants=len(roundtrip_variants),borrowed_tails=sum(bool(v.get('marker_tail')) for v in roundtrip_variants),
      expanded_contexts=sum(bool(v.get('apparatus_context_prefix')) for v in roundtrip_variants),
      display_markers=sum(v.get('marker_mode')=='display margin' for v in roundtrip_variants),
      source_body_sha256={k:sha(s) for k,s in zip(['diplomatic','current'],bodies)},
      exact_source_branch_reconstruction=True,actual_master_body_verified=True)
    (ROOT/'records/FR_RENDERED_BRANCH_ROUNDTRIP.json').write_text(json.dumps(roundtrip,ensure_ascii=False,indent=2)+'\n')
    rows=[];proofs=[]
    targets=[('build/FR_current_revised.tex','reviewed author-text projection'),('readers/fr/final/SGA6_FR_corrige_apparat.tex','exact final corrected-reader TeX, including generated and editorial material')]
    for before_path in ['fr/codex/ref_hold/main.tex','fr/sga6/current/main.tex']:
        before=(ROOT/before_path).read_text()
        for after_path,scope in targets:
            part,proof=diff_rows(before,(ROOT/after_path).read_text(),before_path,after_path,scope);rows.extend(part);proofs.append(proof)
    write_tsv(ROOT/'records/CHANGES_FR.tsv',rows,['scope','page','place','before','after','source','after_source','before_start_line','before_end_line','after_start_line','after_end_line','provenance'])
    markers=re.findall(r'(?m)^%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+([^%\n]+?)\s*%+',master)
    expected=['cover','cover-verso','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']+[str(n) for n in range(1,701)]+[f'rear-{n}' for n in range(715,721)]
    assert [f.strip() for _,f in markers]==expected
    assert [int(i) for i,_ in markers]==list(range(720))
    variants=json.loads((ROOT/'records/FR_VARIANTS.json').read_text())
    assert [(v['id'],v['page'],v['printed'],v['corrected']) for v in variants]==[(v['id'],v['page'],v['printed'],v['corrected']) for v in roundtrip_variants]
    assert len(variants)==len(set(v['id'] for v in variants))==970
    counts={}
    for v in variants:
        assert v['printed']!=v['corrected'] and v['source'] and all(not s.startswith('LAYER-DIFFERENCE') for s in v['source'])
        assert master.count('}{'+v['id']+'}')==1,(v['id'],'body call count')
        assert master.count(r'\hypertarget{SGAApp'+v['id']+'}')==1,(v['id'],'apparatus entry count')
        counts[v['kind']]=counts.get(v['kind'],0)+1
    result=dict(status='French source and literal change invariants passed',forms_from_identical_master=True,
      original_source_leaves=len(markers),numeric_folios=700,source_marker_order_exact=True,
      variants=len(variants),body_calls=len(variants),apparatus_entries=len(variants),source_links_complete=True,
      kinds=counts,change_streams=proofs,changes_rows=len(rows),
      author_text_projection='The exact branch reconstruction proof is records/FR_RENDERED_BRANCH_ROUNDTRIP.json; generated wrappers retain their recorded source strings.',
      compilation='Actual two-pass receipts are required separately for each of the four final PDFs.')
    (ROOT/'records/FR_FINAL_SOURCE_INVARIANTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='change_streams'},ensure_ascii=False))

if __name__=='__main__':main()
