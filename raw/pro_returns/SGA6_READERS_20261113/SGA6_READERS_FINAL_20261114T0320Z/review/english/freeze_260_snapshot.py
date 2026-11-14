#!/usr/bin/env python3
"""Freeze compiled260 without discarding the live261–265 continuation."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
STAGE=ROOT.parent/'sga6_checkpoint09_english260_stage';DEST=STAGE/'review/english'
assert not STAGE.exists(),'Never overwrite an existing checkpoint.'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
builds=json.loads((HERE/'EN_CANDIDATE_BUILD_STATUS.json').read_text())
assert set(builds)=={'corrected_apparatus','diplomatic','reading','annotated_master'}
for form,b in builds.items():
 assert b['compiled_printed_markers']==list(range(1,261))
 assert len(b['runs'])==2 and all(r['exit_code']==0 for r in b['runs'])
 assert b['source_unchanged_during_compile']
 assert sha(HERE/f'DRAFT_SGA6_EN_{form}.tex')==b['source_sha256']
 assert sha(HERE/f'DRAFT_SGA6_EN_{form}.pdf')==b['pdf_sha256']
excluded={'EN_EXPOSE_III_P261_265.tex','register_261_265.py','EN_EXPOSE_III_TRANSFER_261_265.jsonl'}
files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in excluded]
DEST.mkdir(parents=True)
for p in files:
 out=DEST/p.relative_to(HERE);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
assert all(sha(p)==sha(DEST/p.relative_to(HERE)) for p in files)
changes=[]
for name,keep in [
 ('EN_TRANSLATION_PATCHES.jsonl',lambda x:not re.fullmatch(r'\d+[–-]\d+',str(x.get('page',''))) or int(re.split('[–-]',x['page'])[1])<=260),
 ('EN_VARIANTS.jsonl',lambda x:x['page']<=260)]:
 path=DEST/name;old=path.read_text();rows=[json.loads(x) for x in old.splitlines()];kept=[x for x in rows if keep(x)]
 path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in kept));changes.append(dict(path=name,action='Filter accepted records to the compiled260 prefix.',removed_ids=[x['id'] for x in rows if not keep(x)]))
 assert len(kept)==(60 if 'TRANSLATION' in name else 174)
path=DEST/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';pairs=json.loads(path.read_text());path.write_text(json.dumps([x for x in pairs if x['page']<=260],ensure_ascii=False,indent=2)+'\n')
path=DEST/'EN_AUTHOR_NOTE_MARKS.tsv';lines=path.read_text().splitlines();removed=[l for l in lines if l.split('\t',1)[0].isdigit() and int(l.split('\t',1)[0])>260];path.write_text('\n'.join(l for l in lines if l not in removed)+'\n')
changes.append(dict(path='EN_AUTHOR_NOTE_MARKS.tsv',action='Remove the two unbuilt263 author-note rows.',removed_rows=len(removed)))
path=DEST/'README_EN_WORK.md';s=path.read_text();s=s.replace('Live261–265 is also registered with192 exact local\nmathematical units and two additional variants; that later chunk is not yet\nincluded in the generated sources or PDFs.','This snapshot excludes the live261–265 continuation, whose raw chunk and\nshared registry rows were explicitly omitted before sealing.')
s=s.replace('The separately registered261–265 chunk\nhas192 identical mathematical units per branch. ','')
path.write_text(s)
path=DEST/'EN_PARALLEL_TRANSFER_HANDOFF.md';s=path.read_text().replace('Live261–265 is already registered and has passed its\nlocal two-branch comparison. Frozen checkpoints remain untouched.','At snapshot creation, the separate live workspace had also registered261–265;\nthat unbuilt continuation is excluded here. Frozen checkpoints remain untouched.');path.write_text(s)

previous=json.loads((ROOT.parent/'sga6_checkpoint08_english240_stage/review/english/EN_FROZEN240_HANDOFF.json').read_text())
external={x['path'] for x in previous['required_external_inputs']}
external.update(f'build/page_packets/{n}/{layer}.tex' for n in range(241,261) for layer in ['current','diplomatic'])
external.update('review/expose_iii/'+name for name in ['external_sga4_242.json','author_claim_244_245.json','projection_amplitude_248.json','truncation_reference_255.json','author_claim_256_257.json'])
external_rows=[dict(path=x,sha256=sha(ROOT/x)) for x in sorted(external)]

# Only for exact regeneration checks, expose the unchanged external inputs.
# These links are removed before the immutable English directory is sealed.
links=[]
for name in ['en','fr','build']:
 p=STAGE/name;p.symlink_to(ROOT/name,target_is_directory=True);links.append(p)
for p in (ROOT/'review').iterdir():
 if p.is_dir() and p.name!='english':
  out=STAGE/'review'/p.name;out.symlink_to(p,target_is_directory=True);links.append(out)
commands_run=[]
for name in ['verify_reviewed_english.py','build_english_candidates.py','refresh_work_summary.py']:
 p=subprocess.run([sys.executable,str(DEST/name)],cwd=STAGE,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 commands_run.append(dict(command=f'python review/english/{name}',exit_code=p.returncode,output=p.stdout.strip()))
 assert p.returncode==0,commands_run[-1]
for form,b in builds.items():assert sha(DEST/f'DRAFT_SGA6_EN_{form}.tex')==b['source_sha256'],form
for x in external_rows:assert sha(ROOT/x['path'])==x['sha256'],x['path']
for p in links:p.unlink()
for p in DEST.rglob('__pycache__'):shutil.rmtree(p)
summary=json.loads((DEST/'EN_WORK_SUMMARY.json').read_text())
assert summary['translation_patch_count']==60 and summary['variant_count']==174
assert summary['mathematical_units']==8609 and summary['scoped_glossary_rows']==260
assert not summary['registered_not_yet_built_folios'] and not summary['prepared_unregistered_folios']
assert not summary['pending_layout_repairs']
commands=['python review/english/verify_reviewed_english.py','python review/english/verify_expose_i_forms.py','python review/english/verify_expose_ii_forms.py','python review/english/verify_expose_iii_forms.py','python review/english/build_english_candidates.py','python review/english/compile_candidates.py','python review/english/make_alignment_hints.py','python review/english/refresh_work_summary.py']
record=dict(scope='English reconstruction through printed260;60 accepted translation records;174 explicit source variants',copied_English_files=len(files),excluded_live_files=sorted(excluded)+['__pycache__/**'],staged_changes=changes,frozen=True,
 source_validation=dict(mathematical_units=8609,approved_difference_side_units=118,unexpected_difference_units=0,both_source_forms='ExposéI78–159, ExposéII160–221 and ExposéIII222–260 separately materialized and checked',glossary_reference_pairs=260),
 builds=summary['builds'],reproduction_check=dict(commands=commands_run,all_four_generated_source_hashes_identical_to_compiled_sources=True,external_inputs_unchanged_during_check=True),
 visual_QA='Direct inspection of corrected outputs134–144 through the final260 words direct sums of sheaves, plus every new apparatus entry162–174 on398–400. All new original-note calls/text pairs share their output page; diagrams, truncation labels and exact symbol transport are legible. No clipping or overlap observed. Later text on144 is inherited. Alternate-form pixels were not rechecked; the reading margin diagnostics20/21/49/110 remain at the established221 locations.',
 required_external_inputs=external_rows,generation_commands=commands,
 integration='Copy this entire staged review/english directory into the combined checkpoint and provide the named external inputs. The isolated TeX runtime and wrapper are required for recompilation. The temporary verification links were removed. Copy the read-only stage to a separate working directory before regeneration.',
 limitations='English after260, the whole-volume semantic glossary, complete front-matter alignment and full-PDF visual inspection remain unfinished. The live261–265 source is excluded from this coherent build boundary. No full-volume translation or global propagation claim is made.')
(DEST/'EN_FROZEN260_HANDOFF.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(DEST/'EN_FROZEN_HANDOFF_260.md').write_text('''# English through260 frozen handoff

This immutable snapshot contains60 accepted translation records and174 explicit
source variants through printed260. All four forms compiled twice successfully:
400 pages for corrected/apparatus and master,372 for diplomatic and reading.
The only final diagnostics are the existing reading margin moves20/21/49/110.

The current-source check covers8,609 mathematical units,59 approved paired
lexical occurrences and zero unexpected differences. Both source branches of
I,II and reconstructed III have separate exact checks. The scoped glossary has
260 reference pairs, without a semantic-completeness claim.

Corrected outputs134–144 through the final260 words “direct sums of sheaves”
and all new apparatus entries162–174 on398–400 were directly viewed. Every new
original note is complete and shares the output page of its call. No clipping
or overlap was observed. Later text on144 is inherited. No alternate-form pixel
comparison was repeated at this boundary.

The live261–265 continuation is excluded: its raw chunk, registration script,
ledger, variants175–176 and author-note rows were omitted or filtered. The
frozen source was regenerated from the filtered registries, and all four TeX
hashes exactly match the sources of the successful PDFs. The frozen global
comparison still returns8,609 units with zero unexpected differences.

EN_FROZEN260_HANDOFF.json records exact hashes, external dependencies, commands,
scope and staging actions. EN_FROZEN260_INCLUDE_LIST.txt lists every file;
EN_FROZEN260_MANIFEST.tsv hashes all payload files; EN_FROZEN260_SEAL.json hashes
the manifest. Earlier stages and the live continuation remain unchanged.
The whole-volume completion gate remains unmet.
''')
manifest=DEST/'EN_FROZEN260_MANIFEST.tsv';seal=DEST/'EN_FROZEN260_SEAL.json';include=DEST/'EN_FROZEN260_INCLUDE_LIST.txt'
names=sorted([str(p.relative_to(STAGE)) for p in DEST.rglob('*') if p.is_file()]+[str(p.relative_to(STAGE)) for p in [manifest,seal,include]])
include.write_text('\n'.join(names)+'\n')
payload=sorted(p for p in DEST.rglob('*') if p.is_file())
manifest.write_text('sha256\tbytes\tpath\n'+''.join(f'{sha(p)}\t{p.stat().st_size}\t{p.relative_to(STAGE)}\n' for p in payload))
seal_record=dict(boundary='printed1–260',manifest='review/english/EN_FROZEN260_MANIFEST.tsv',manifest_sha256=sha(manifest),manifest_payload_files=len(payload),total_staged_files=len(payload)+2,include_list='review/english/EN_FROZEN260_INCLUDE_LIST.txt',include_list_sha256=sha(include),immutable_snapshot=True)
seal.write_text(json.dumps(seal_record,indent=2)+'\n')
for p in STAGE.rglob('*'):
 if p.is_file():p.chmod(0o444)
for p in sorted((p for p in STAGE.rglob('*') if p.is_dir()),reverse=True):p.chmod(0o555)
STAGE.chmod(0o555)
receipt=dict(stage=STAGE.name,**seal_record,seal_sha256=sha(seal),frozen_assembly_reproduces_compiled_source_hashes=True)
(HERE/'EN_FROZEN260_SNAPSHOT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
