#!/usr/bin/env python3
"""Copy the complete coherent English221 boundary to a new read-only stage."""
from pathlib import Path
import hashlib,json,shutil,os
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
STAGE=ROOT.parent/'sga6_checkpoint07_english221_stage'
DEST=STAGE/'review/english'
assert not STAGE.exists(),'Never overwrite an existing checkpoint.'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
summary=json.loads((HERE/'EN_WORK_SUMMARY.json').read_text())
assert summary['compiled_reviewed_folios']==list(range(1,222)) and summary['variant_count']==151
assert not summary['registered_not_yet_built_folios'] and not summary['pending_layout_repairs']
old=json.loads((ROOT.parent/'sga6_checkpoint06_english179_stage/review/english/EN_FROZEN179_HANDOFF.json').read_text())
external={x['path'] for x in old['required_external_inputs']}
external.update(f'build/page_packets/{n}/{layer}.tex' for n in range(180,222) for layer in ['current','diplomatic'])
external_rows=[dict(path=x,sha256=sha(ROOT/x)) for x in sorted(external)]
files=[f for f in HERE.rglob('*') if f.is_file() and '__pycache__' not in f.parts]
DEST.mkdir(parents=True)
for f in files:
 out=DEST/f.relative_to(HERE);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,out)
assert all(sha(f)==sha(DEST/f.relative_to(HERE)) for f in files)
commands=['python review/english/verify_reviewed_english.py','python review/english/verify_expose_i_forms.py','python review/english/verify_expose_ii_forms.py','python review/english/build_english_candidates.py','python review/english/compile_candidates.py','python review/english/make_alignment_hints.py','python review/english/refresh_work_summary.py']
record=dict(scope='English reconstruction and all four built forms through printed221;52 accepted translation records;151 source variants',copied_English_files=len(files),excluded_live_files=['__pycache__/**'],staged_changes=[],frozen=True,source_validation=dict(mathematical_units=7127,approved_difference_side_units=102,unexpected_difference_units=0,both_source_forms='ExposéI78–159 and ExposéII160–221 separately materialized and checked',glossary_reference_pairs=242),builds=summary['builds'],reproduction_check='All three exact source verification scripts passed immediately before copying. Regeneration reproduced every standalone TeX source byte for byte. All four PDFs are the exact two-pass final221 builds with matching recorded hashes.',visual_QA='Regional checks only, detailed in EN_PDF_VISUAL_QA.json. Final corrected112–123 and apparatus392–394 directly viewed; diplomatic/reading111,118,121 directly viewed; final111 and moved-margin110 compared to earlier inspected images. Reading20/21/49 match inspected frozen179. Master regional pages match the inspected corrected pages pixel for pixel.',pagination_repair='EN-LAYOUT-202-01 keeps the numerical1 display call with its original complete note; numerical2 also remains complete on the same page. Body/formula/note bytes are unchanged by the wrapper.',required_external_inputs=external_rows,generation_commands=commands,integration='Copy only this staged review/english directory into the combined checkpoint, and supply the named source inputs from the coordinator stage. The installed TeX runtime/wrapper environment is required for recompilation. The staged files are read-only; regenerate in a separate working copy.',limitations='The inherited English after221, whole-volume glossary, complete front-matter alignment and whole-PDF visual inspection remain unfinished. Exact-source checks, translation scope, mathematical audits and scan observations are separately attributed. No whole-volume correction-propagation claim is made.')
(DEST/'EN_FROZEN221_HANDOFF.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(DEST/'EN_FROZEN_HANDOFF_221.md').write_text('''# English through221 frozen handoff

The frozen source and all four PDFs include the complete reconstructed Exposés0,
I andII, printed1–221. There are52 accepted passage records and151 explicit source
variants. All four forms completed two successful passes:394 pages for corrected
apparatus and annotated master;371 for diplomatic and reading.

The literal current-source comparison covers7,127 mathematical units with51
approved paired occurrences and zero unexpected differences. Both ExposéI andII
branches pass their independent comparisons. The scoped glossary has242 reference
pairs; these are literal occurrence records, not a completed semantic glossary.

The final202 pagination repair keeps the original numerical1 display call with
its complete symmetric-power note. Direct regional visual checks and exact pixel
comparisons are recorded in EN_PDF_VISUAL_QA.json and the EN_221_* comparison
files. The only final diagnostics are reading margin movement on20,21,49,110;
those page clearances are verified. No full-volume visual completion is claimed.

EN_FROZEN221_HANDOFF.json contains exact source/PDF hashes, external input hashes,
commands, scope and limitations. EN_FROZEN221_INCLUDE_LIST.txt gives every staged
file. EN_FROZEN221_MANIFEST.tsv hashes every file except the manifest itself and
its seal; EN_FROZEN221_SEAL.json hashes that manifest. This stage has no writable
files and must be copied before regeneration. Earlier checkpoints are unchanged.

English after221 remains inherited and unreviewed. Source author-claim packets
remain separate from the faithfully retained historical statements. No global
propagation or full-volume translation completion is asserted.
''')
manifest=DEST/'EN_FROZEN221_MANIFEST.tsv';seal=DEST/'EN_FROZEN221_SEAL.json';include=DEST/'EN_FROZEN221_INCLUDE_LIST.txt'
all_names=sorted([str(f.relative_to(STAGE)) for f in DEST.rglob('*') if f.is_file()]+[str(x.relative_to(STAGE)) for x in [manifest,seal,include]])
include.write_text('\n'.join(all_names)+'\n')
payload=sorted(f for f in DEST.rglob('*') if f.is_file())
manifest.write_text('sha256\tbytes\tpath\n'+''.join(f'{sha(f)}\t{f.stat().st_size}\t{f.relative_to(STAGE)}\n' for f in payload))
seal_record=dict(boundary='printed1–221',manifest='review/english/EN_FROZEN221_MANIFEST.tsv',manifest_sha256=sha(manifest),manifest_payload_files=len(payload),total_staged_files=len(payload)+2,include_list='review/english/EN_FROZEN221_INCLUDE_LIST.txt',include_list_sha256=sha(include),immutable_snapshot=True)
seal.write_text(json.dumps(seal_record,indent=2)+'\n')
for f in STAGE.rglob('*'):
 if f.is_file():f.chmod(0o444)
for d in sorted((x for x in STAGE.rglob('*') if x.is_dir()),reverse=True):d.chmod(0o555)
STAGE.chmod(0o555)
receipt=dict(stage=STAGE.name,**seal_record,seal_sha256=sha(seal),original_English_files_sha_verified=True)
(HERE/'EN_FROZEN221_SNAPSHOT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
