#!/usr/bin/env python3
"""Refresh live scope and build metadata without changing frozen handoffs."""
from pathlib import Path
import csv
import hashlib
import json
import re
import fitz

HERE=Path(__file__).resolve().parent
verification_path=max(HERE.glob('EN_REVIEWED_VERIFICATION_001_*.json'),key=lambda p:int(p.stem.rsplit('_',1)[1]))
verification=json.loads(verification_path.read_text())
end=verification['reviewed_pages']
assert verification['unexpected_difference_units']==0
patches=[json.loads(x) for x in (HERE/'EN_TRANSLATION_PATCHES.jsonl').read_text().splitlines()]
patches=[p for p in patches if p['status'].startswith('accepted')]
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
pairs=json.loads((HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json').read_text())
candidate=json.loads((HERE/'EN_CANDIDATE_STATUS.json').read_text())
builds=json.loads((HERE/'EN_CANDIDATE_BUILD_STATUS.json').read_text())
forms=['corrected_apparatus','diplomatic','reading','annotated_master']
assert set(builds)==set(forms),'A complete four-form build record is required.'
summary={}
for form in forms:
 result=builds[form]
 pdf=HERE/('DRAFT_SGA6_EN_'+form+'.pdf')
 assert all(r['exit_code']==0 for r in result['runs']) and len(result['runs'])==2
 assert result['source_unchanged_during_compile']
 assert hashlib.sha256(pdf.read_bytes()).hexdigest()==result['pdf_sha256']
 with fitz.open(pdf) as doc:pages=len(doc)
 summary[form]=dict(page_count=pages,passes=len(result['runs']),all_exit_zero=True,
  source_sha256=result['source_sha256'],pdf_sha256=result['pdf_sha256'],
  diagnostics=result['runs'][-1]['diagnostics'])
compiled=builds['corrected_apparatus']['compiled_printed_markers']
assert all(b['compiled_printed_markers']==compiled for b in builds.values())
compiled_variant_ids=builds['corrected_apparatus']['compiled_variant_ids']
assert all(b['compiled_variant_ids']==compiled_variant_ids for b in builds.values())
generated=[int(x) for x in re.findall(r'\\SGAPrintPage\{(\d+)\}',(HERE/'DRAFT_SGA6_EN_annotated_master.tex').read_text())]
registered=set()
for p in patches:
 m=re.fullmatch(r'(\d+)[–-](\d+)',str(p.get('page','')))
 if m:registered.update(range(int(m.group(1)),int(m.group(2))+1))
chunk_pages=set()
for p in HERE.glob('EN_*_P*.tex'):
 m=re.fullmatch(r'EN_.*_P(\d{3})_(\d{3})\.tex',p.name)
 if m:chunk_pages.update(range(int(m.group(1)),int(m.group(2))+1))
with (HERE/f'GLOSSARY_SGA6_REVIEWED_001_{end:03}.tsv').open() as stream:glossary=list(csv.DictReader(stream,delimiter='\t'))
regions=[(1,77,'0'),(78,159,'I'),(160,221,'II'),(222,273,'III'),(274,296,'IV'),(297,364,'V'),(365,415,'VI'),(416,465,'VII'),(466,497,'VIII'),(498,518,'IX'),(519,594,'X'),(595,615,'XII'),(616,666,'XIII'),(667,700,'XIV')]
scopes=[f'Exposé{name} {start}–{min(stop,end)}'+(' complete' if stop<=end else '') for start,stop,name in regions if start<=end]
result=dict(reviewed_printed_folios=list(range(1,end+1)),
 reviewed_scope='; '.join(scopes)+'; specific Introduction/contents corrections separately recorded',
 translation_patch_count=len(patches),variant_count=len(variants),mathematical_units=verification['mathematical_units'],
 approved_nonidentical_unit_pairs=verification['literal_difference_units']//2,
 approved_exact_pair_records=sum(p.get('layer','both') in ('both','current') and p['page']<=end for p in pairs),
 approved_diplomatic_only_pair_records=sum(p.get('layer')=='diplomatic' and p['page']<=end for p in pairs),
 unexpected_math_units=verification['unexpected_difference_units'],early_current_patch_rows_classified=61,
 scoped_glossary_rows=len(glossary),full_volume_translation_complete=False,full_volume_glossary_complete=False,
 full_volume_visual_QA_complete=False,builds=summary,
 prepared_unregistered_folios=sorted(chunk_pages-registered),pending_layout_repairs=json.loads((HERE/'EN_PDF_VISUAL_QA.json').read_text()).get('pending_render_verification',[]),
 compiled_reviewed_folios=compiled,exact_Exposé_I_both_forms_check=f'EN_EXPOSE_I_FORM_VERIFICATION_078_{min(end,159):03}.json',
 exact_Exposé_II_both_forms_check=f'EN_EXPOSE_II_FORM_VERIFICATION_160_{min(end,221):03}.json' if end>=160 else None,
 exact_Exposé_III_both_forms_check=f'EN_EXPOSE_III_FORM_VERIFICATION_222_{min(end,273):03}.json' if end>=222 else None,
 exact_Exposé_IV_both_forms_check=f'EN_EXPOSE_IV_FORM_VERIFICATION_274_{min(end,296):03}.json' if end>=274 else None,
 registered_not_yet_built_folios=sorted(registered-set(compiled)),
 compiled_translation_patch_count=len(candidate['accepted_patch_ids']) if compiled==generated else None,
 compiled_variant_count=len(compiled_variant_ids),generated_reviewed_folios=generated,
 generation_status=f'All four TeX sources generated through{max(generated)}; all four corresponding PDFs compiled through{max(compiled)} in two successful passes.',
 regional_layout_probe='EN_LAYOUT_090_PROBE_RESULT.json',
 full_frozen_stage_build_pending=False,
 frozen_stage_note='Checkpoint03 through110 was separately compiled by the coordinator; its historical source manifest remains unchanged.',
 limitation='Freshly compared body scope, source-form math checks, compilation and regional PDF inspection are recorded separately; the remainder of the supplied English body remains unreviewed.')
(HERE/'EN_WORK_SUMMARY.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(compared=end,generated=max(generated),compiled=max(compiled),variants=len(variants),glossary_rows=len(glossary),page_counts={k:v['page_count'] for k,v in summary.items()})))
