#!/usr/bin/env python3
"""Seal the compiled English1–296 boundary, excluding live contributions."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
STAGE=ROOT.parent/'sga6_checkpoint10_english296_stage';DEST=STAGE/'review/english'
assert not STAGE.exists(),'Never overwrite an existing checkpoint.'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
builds=json.loads((HERE/'EN_CANDIDATE_BUILD_STATUS.json').read_text())
forms={'corrected_apparatus','diplomatic','reading','annotated_master'}
assert set(builds)==forms
for form,b in builds.items():
 assert b['compiled_printed_markers']==list(range(1,297))
 assert len(b['compiled_variant_ids'])==201
 assert len(b['runs'])==2 and all(r['exit_code']==0 for r in b['runs'])
 assert b['source_unchanged_during_compile']
 assert sha(HERE/f'DRAFT_SGA6_EN_{form}.tex')==b['source_sha256']
 assert sha(HERE/f'DRAFT_SGA6_EN_{form}.pdf')==b['pdf_sha256']
files=[p for p in HERE.rglob('*') if p.is_file() and not ({'__pycache__','contributions'}&set(p.relative_to(HERE).parts))]
DEST.mkdir(parents=True)
for p in files:
 out=DEST/p.relative_to(HERE);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
assert all(sha(p)==sha(DEST/p.relative_to(HERE)) for p in files)

previous=json.loads((ROOT.parent/'sga6_checkpoint09_english260_stage/review/english/EN_FROZEN260_HANDOFF.json').read_text())
external={x['path'] for x in previous['required_external_inputs']}
external.update(f'build/page_packets/{n}/{layer}.tex' for n in range(261,297) for layer in ['current','diplomatic'])
for directory in ['expose_iv','expose_iv_amendments']:
 for p in (ROOT/'review'/directory).iterdir():
  if p.is_file() and p.suffix in {'.json','.jsonl','.tsv','.md'}:external.add(str(p.relative_to(ROOT)))
# Include every actual patch stream with rows in this prefix. Streams with only
# later folios do not contribute to these sources and are not dependencies.
for p in (ROOT/'review').glob('*/patches.jsonl'):
 rows=[json.loads(s) for s in p.read_text().splitlines() if s.strip()]
 if any(isinstance(x.get('page'),int) and 1<=x['page']<=296 for x in rows):external.add(str(p.relative_to(ROOT)))
external_rows=[dict(path=x,sha256=sha(ROOT/x)) for x in sorted(external)]

# Expose external inputs only for a reproducibility check. All verification
# links are removed before sealing the snapshot.
links=[]
for name in ['en','fr','build']:
 p=STAGE/name;p.symlink_to(ROOT/name,target_is_directory=True);links.append(p)
for p in (ROOT/'review').iterdir():
 if p.is_dir() and p.name!='english':
  out=STAGE/'review'/p.name;out.symlink_to(p,target_is_directory=True);links.append(out)
commands_run=[]
for name in ['build_english_candidates.py','refresh_work_summary.py']:
 result=subprocess.run([sys.executable,str(DEST/name)],cwd=STAGE,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 commands_run.append(dict(command=f'python review/english/{name}',exit_code=result.returncode,output=result.stdout.strip()))
 assert result.returncode==0,commands_run[-1]
for form,b in builds.items():assert sha(DEST/f'DRAFT_SGA6_EN_{form}.tex')==b['source_sha256'],form
for x in external_rows:assert sha(ROOT/x['path'])==x['sha256'],x['path']
for p in links:p.unlink()
for p in DEST.rglob('__pycache__'):shutil.rmtree(p)
summary=json.loads((DEST/'EN_WORK_SUMMARY.json').read_text())
assert summary['translation_patch_count']==68 and summary['variant_count']==201
assert summary['mathematical_units']==9621 and summary['scoped_glossary_rows']==269
assert not summary['registered_not_yet_built_folios'] and not summary['prepared_unregistered_folios']
assert not summary['pending_layout_repairs']
commands=['python review/english/verify_reviewed_english.py','python review/english/verify_expose_i_forms.py','python review/english/verify_expose_ii_forms.py','python review/english/verify_expose_iii_forms.py','python review/english/verify_expose_iv_forms.py','python review/english/build_english_candidates.py','python review/english/compile_candidates.py','python review/english/make_alignment_hints.py','python review/english/refresh_work_summary.py']
record=dict(scope='English reconstruction through printed296;68 accepted translation records;201 explicit source variants',copied_English_files=len(files),excluded_live_files=['contributions/**','__pycache__/**'],frozen=True,
 source_validation=dict(mathematical_units=9621,approved_difference_side_units=118,unexpected_difference_units=0,both_source_forms='ExposésI78–159,II160–221,III222–273 andIV274–296 separately materialized and checked',glossary_reference_pairs=269),
 builds=summary['builds'],reproduction_check=dict(commands=commands_run,all_four_generated_source_hashes_identical_to_compiled_sources=True,external_inputs_unchanged_during_check=True),
 visual_QA='Corrected outputs150–162 from the IV title through its complete bibliography and every new apparatus187–201 on400–404 were directly inspected. Original notes276/279/290 have their complete texts on the same output page as their calls. Diagrams, equation tags, local rules and source-approved analytic locator amendments199/200 are legible without clipping or overlap. Regional164 verifies only the separate Ab/fil rules after the296 macro renewal. No alternate-form pixel check was repeated; reading retains established margin diagnostics20/21/49/110.',
 source_amendments=['ASTRA-IV-REF-287-POSTFREEZE / EN-VAR-199','ASTRA-IV-REF-289-POSTFREEZE / EN-VAR-200'],
 author_claim_handling='The full source3.3.3 on295 remains unchanged in both English forms. Its exact derived-tensor counterexample and transfer disposition are separate audit records; no replacement theorem or artificial variant is inserted.',
 required_external_inputs=external_rows,generation_commands=commands,
 integration='Copy this complete staged review/english directory into the combined checkpoint and provide the named external inputs. Recompilation also needs the isolated TeX runtime and wrapper. Temporary verification links were removed. Copy the read-only stage to a new working directory before regeneration.',
 limitations='English after296, complete front/rear alignment, whole-volume semantic glossary and full-PDF visual verification remain unfinished. Live parallel contribution directories are excluded. No full-volume translation or global propagation claim is made.')
(DEST/'EN_FROZEN296_HANDOFF.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(DEST/'EN_FROZEN_HANDOFF_296.md').write_text('''# English through296 frozen handoff

The immutable snapshot contains68 accepted passage records and201 explicit
source variants through the complete ExposéIV bibliography on printed296.
All four forms compiled twice:404 pages for corrected/apparatus and master,
370 for diplomatic and reading. All final diagnostics are empty except the
established reading margin moves20/21/49/110.

The current-source check covers9,621 complete mathematical units,59 approved
paired lexical occurrences and zero unexpected differences. Both branches of
I,II,III andIV have separate exact comparisons. The scoped glossary contains269
reference pairs and makes no whole-volume semantic-completeness claim.

Corrected outputs150–162 and every new apparatus187–201 on400–404 were directly
viewed. The original notes276/279/290 remain complete with their calls. The
IV287/289 locator amendments are explicit variants199/200. The source author
claim3.3.3 on295 is retained in both layers with its separate counterexample
record. Regional164 checks only the local Ab/fil macro expansion. No clipping
or overlap was observed; no alternate-form pixel inspection is newly claimed.

All live contribution directories are excluded. Regeneration in the isolated
stage exactly reproduced all four TeX hashes used by the successful builds.
EN_FROZEN296_HANDOFF.json records the source dependencies, hashes, commands and
scope; the include list and manifest identify every payload file. The seal
records their hashes. Earlier checkpoints and live work remain unchanged.
The complete-volume delivery gate remains unmet.
''')
manifest=DEST/'EN_FROZEN296_MANIFEST.tsv';seal=DEST/'EN_FROZEN296_SEAL.json';include=DEST/'EN_FROZEN296_INCLUDE_LIST.txt'
names=sorted([str(p.relative_to(STAGE)) for p in DEST.rglob('*') if p.is_file()]+[str(p.relative_to(STAGE)) for p in [manifest,seal,include]])
include.write_text('\n'.join(names)+'\n')
payload=sorted(p for p in DEST.rglob('*') if p.is_file())
manifest.write_text('sha256\tbytes\tpath\n'+''.join(f'{sha(p)}\t{p.stat().st_size}\t{p.relative_to(STAGE)}\n' for p in payload))
seal_record=dict(boundary='printed1–296',manifest='review/english/EN_FROZEN296_MANIFEST.tsv',manifest_sha256=sha(manifest),manifest_payload_files=len(payload),total_staged_files=len(payload)+2,include_list='review/english/EN_FROZEN296_INCLUDE_LIST.txt',include_list_sha256=sha(include),immutable_snapshot=True)
seal.write_text(json.dumps(seal_record,indent=2)+'\n')
for p in STAGE.rglob('*'):
 if p.is_file():p.chmod(0o444)
for p in sorted((p for p in STAGE.rglob('*') if p.is_dir()),reverse=True):p.chmod(0o555)
STAGE.chmod(0o555)
receipt=dict(stage=STAGE.name,**seal_record,seal_sha256=sha(seal),frozen_assembly_reproduces_compiled_source_hashes=True)
(HERE/'EN_FROZEN296_SNAPSHOT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
