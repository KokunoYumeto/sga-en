#!/usr/bin/env python3
"""Preserve the coherent English240 build in a new immutable checkpoint stage."""
from pathlib import Path
import hashlib,json,shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
STAGE=ROOT.parent/'sga6_checkpoint08_english240_stage'
DEST=STAGE/'review/english'
assert not STAGE.exists(),'Never overwrite an existing checkpoint.'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
summary=json.loads((HERE/'EN_WORK_SUMMARY.json').read_text())
assert summary['compiled_reviewed_folios']==list(range(1,241))
assert summary['variant_count']==161 and summary['translation_patch_count']==56
assert summary['mathematical_units']==7853 and summary['scoped_glossary_rows']==253
assert not summary['registered_not_yet_built_folios'] and not summary['pending_layout_repairs']
old=json.loads((ROOT.parent/'sga6_checkpoint07_english221_stage/review/english/EN_FROZEN221_HANDOFF.json').read_text())
external={x['path'] for x in old['required_external_inputs']}
external.update(f'build/page_packets/{n}/{layer}.tex' for n in range(222,241) for layer in ['current','diplomatic'])
for path in (ROOT/'review').glob('*/patches.jsonl'):
    rows=[json.loads(x) for x in path.read_text().splitlines()]
    if any(isinstance(x['page'],int) and 222<=x['page']<=240 for x in rows):
        external.add(str(path.relative_to(ROOT)))
external.update('review/expose_iii/'+name for name in ['decisions.jsonl','own_findings.jsonl','page_status.jsonl','external_ega_224.json','projection_formula_235.json'])
external_rows=[dict(path=x,sha256=sha(ROOT/x)) for x in sorted(external)]
files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
DEST.mkdir(parents=True)
for p in files:
    out=DEST/p.relative_to(HERE);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
assert all(sha(p)==sha(DEST/p.relative_to(HERE)) for p in files)
commands=['python review/english/verify_reviewed_english.py','python review/english/verify_expose_i_forms.py','python review/english/verify_expose_ii_forms.py','python review/english/verify_expose_iii_forms.py','python review/english/build_english_candidates.py','python review/english/compile_candidates.py','python review/english/make_alignment_hints.py','python review/english/refresh_work_summary.py']
record=dict(scope='English reconstruction through printed240;56 accepted translation records;161 source variants',copied_English_files=len(files),excluded_live_files=['__pycache__/**'],staged_changes=[],frozen=True,
 source_validation=dict(mathematical_units=7853,approved_difference_side_units=106,unexpected_difference_units=0,both_source_forms='ExposéI78–159, ExposéII160–221 and ExposéIII222–240 separately materialized and checked',glossary_reference_pairs=253),
 builds=summary['builds'],reproduction_check='All four exact source verification scripts passed before copying. Each built source has its recorded unchanged SHA-256; all four forms completed two successful passes. The annotated-master compilation was resumed separately after the interrupted first batch, and its result was merged with the three successful reader records.',
 visual_QA='Direct regional inspection of corrected outputs123–134 through the Corollary2.5 display, and every new apparatus entry152–161 on outputs394–396. No clipping or overlap observed. Later text on134 is inherited and outside the completed passage. All four final reading margin diagnostics match the established221 locations; no new alternate-form pixel comparison is claimed.',
 required_external_inputs=external_rows,generation_commands=commands,
 integration='Copy this complete staged review/english directory into the combined checkpoint and supply the named external inputs. The isolated TeX runtime and wrapper environment are required for recompilation. Copy the read-only stage to a separate working directory before regenerating.',
 limitations='English after240, the whole-volume semantic glossary, complete front-matter alignment and full-PDF visual inspection remain unfinished. Source observations, translation comparisons, mathematical audits and regional PDF checks retain their separate scopes. No global propagation or full-volume completion claim is made.')
(DEST/'EN_FROZEN240_HANDOFF.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(DEST/'EN_FROZEN_HANDOFF_240.md').write_text('''# English through240 frozen handoff

The frozen source and all four PDFs contain the complete reconstructed Exposés0,
I andII, and ExposéIII through the Corollary2.5 statement on printed240. There are
56 accepted translation records and161 explicit source variants. All four forms
completed two successful passes:396 pages for corrected/apparatus and master,
371 for diplomatic and reading. The only final diagnostics are the four reading
margin moves on20,21,49,110, at the established221 warning locations.

The current-source comparison covers7,853 mathematical units with53 approved
paired lexical occurrences and zero unexpected differences. Both forms of I,
II and reconstructed III pass their separate literal comparisons. The scoped
glossary has253 reference pairs; this is not a semantic-completeness claim.

Corrected outputs123–134 through the final Corollary2.5 display and all ten new
apparatus entries on394–396 were directly inspected. No clipping or overlap was
observed. Later text on134 remains inherited; alternate-form visual verification
was not repeated at this boundary. EN_PDF_VISUAL_QA.json gives the exact scope.

EN_FROZEN240_HANDOFF.json records source/PDF hashes, external input hashes,
commands and limitations. EN_FROZEN240_INCLUDE_LIST.txt lists every staged file.
EN_FROZEN240_MANIFEST.tsv hashes every payload file; EN_FROZEN240_SEAL.json hashes
that manifest. Copy this read-only stage before regeneration. Earlier stages
are unchanged. English after240 and the complete volume remain unfinished.
''')
manifest=DEST/'EN_FROZEN240_MANIFEST.tsv';seal=DEST/'EN_FROZEN240_SEAL.json';include=DEST/'EN_FROZEN240_INCLUDE_LIST.txt'
names=sorted([str(p.relative_to(STAGE)) for p in DEST.rglob('*') if p.is_file()]+[str(p.relative_to(STAGE)) for p in [manifest,seal,include]])
include.write_text('\n'.join(names)+'\n')
payload=sorted(p for p in DEST.rglob('*') if p.is_file())
manifest.write_text('sha256\tbytes\tpath\n'+''.join(f'{sha(p)}\t{p.stat().st_size}\t{p.relative_to(STAGE)}\n' for p in payload))
seal_record=dict(boundary='printed1–240',manifest='review/english/EN_FROZEN240_MANIFEST.tsv',manifest_sha256=sha(manifest),manifest_payload_files=len(payload),total_staged_files=len(payload)+2,include_list='review/english/EN_FROZEN240_INCLUDE_LIST.txt',include_list_sha256=sha(include),immutable_snapshot=True)
seal.write_text(json.dumps(seal_record,indent=2)+'\n')
for p in STAGE.rglob('*'):
    if p.is_file():p.chmod(0o444)
for p in sorted((p for p in STAGE.rglob('*') if p.is_dir()),reverse=True):p.chmod(0o555)
STAGE.chmod(0o555)
receipt=dict(stage=STAGE.name,**seal_record,seal_sha256=sha(seal),original_English_files_sha_verified=True)
(HERE/'EN_FROZEN240_SNAPSHOT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
