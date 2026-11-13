#!/usr/bin/env python3
"""Rebuild the SGA 5 readers from the three original ZIPs and reviewed records.

Run from the extracted records project root, preserving its work/ layout.
The default mode validates inputs and writes a plan without running builders.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import time
import zipfile
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
from audit_packages import PATTERNS

ARCHIVES = ['SGA5_FR.zip', 'SGA5_EN.zip', 'SGA5_SCANS.zip']
REVIEWED_INPUTS = [
    'upload/PROMPT(20261112-230204).md',
    'work/contributions/decisions/frontmatter_FR.tex',
    'work/contributions/decisions/frontmatter_EN.tex',
    'work/contributions/english/manual_prose_variants.json',
    'work/contributions/english/EN_PROJECTION_REVIEW_DECIDED.json',
    'work/contributions/english/EN_PROJECTION_REVIEW_DECIDED.tsv',
    'work/contributions/validation_fr/folio248_token_boundary_probe.tex',
    'work/contributions/validation_fr/folio248_probe_input.json',
]
MODULE_DEPENDENCIES = [
    'work/build/scripts/sga5_common.py',
    'work/contributions/english/project_glyphs.py',
    'work/contributions/english/project_internal_hom.py',
    'work/contributions/english/editorial_note_relocation.py',
    'work/contributions/validation_en/apply_resolved_sources.py',
    'work/contributions/validation_fr/resolve_fr_sources.py',
    'work/contributions/validation_fr/audit_fr_master.py',
    'work/contributions/validation_en/audit_english_master.py',
    'work/contributions/packaging_audit/audit_packages.py',
]
TEX_PACKAGES = ['article.cls','fontenc.sty','inputenc.sty','babel.sty','french.ldf','english.ldf','lmodern.sty',
                'geometry.sty','microtype.sty','amsmath.sty','amssymb.sty','mathtools.sty','mathrsfs.sty',
                'enumitem.sty','amsthm.sty','tikz-cd.sty','graphicx.sty','hyperref.sty','ulem.sty',
                'xcolor.sty','marginnote.sty','fvextra.sty','xparse.sty','needspace.sty']


def step(identifier, script, *arguments, checks=None):
    return {'id': identifier, 'command': ['python', script, *arguments], 'checks': checks or []}


def build_steps():
    stages = [
        step('source_record_audit','work/contributions/decisions/audit_sources.py'),
        step('open_decisions','work/contributions/decisions/decide_records.py'),
        step('unresolved_notes','work/contributions/decisions/make_unresolved_notes.py'),
        step('scan_decisions','work/contributions/scans/decide_places98.py','--sources','work/sources','--output','work/contributions/scans'),
        # prepare_french owns its exact source resolver. Do not run the resolver
        # again on its already-resolved ledger, which would lose legacy history.
        step('prepare_french','work/build/scripts/prepare_french.py'),
        step('english_candidate_inventory','work/contributions/english/prepare_english.py'),
        step('finalize_english','work/contributions/english/finalize_english.py'),
        # Alignment consumes the bilingual index pairs; glossary consumes both
        # index pairs and the terminology inventory. This order avoids a cycle.
        step('index_glossary_pairs','work/contributions/decisions/extract_index_glossary.py'),
        step('body_terminology','work/contributions/decisions/curate_terminology.py'),
        step('english_alignment','work/contributions/english/alignment_english.py'),
        step('glossary_additions','work/contributions/english/collect_glossary_additions.py'),
        step('english_glossary','work/contributions/english/build_glossary.py'),
        step('english_port_audit','work/contributions/english/audit_english_port.py',checks=[
            ['work/contributions/english/EN_PORT_AUDIT_SUMMARY.json',['unresolved'],0],
            ['work/contributions/english/EN_PORT_AUDIT_SUMMARY.json',['byte_exact_variant_replay'],True]]),
        # English master preparation internally audits, resolves exact source
        # labels, and audits again before returning.
        step('prepare_english_master','work/build/scripts/prepare_english_master.py'),
        step('wrap_french','work/build/scripts/wrap_readers.py','FR'),
        step('wrap_english','work/build/scripts/wrap_readers.py','EN'),
        step('glossary_and_note_audit','work/contributions/english/audit_glossary_and_notes.py',checks=[
            ['work/contributions/english/GLOSSARY_COVERAGE_AUDIT.json',['passed'],True],
            ['work/contributions/english/READER_UNRESOLVED_NOTES_AUDIT.json',['passed'],True]]),
        step('french_fix_inheritance','work/contributions/audit/audit_fixes.py',checks=[
            ['work/contributions/audit/AUDIT_FR.json',['validation','all_prepared_layers_reconstruct_exactly'],True],
            ['work/contributions/audit/AUDIT_FR.json',['validation','unresolved_terminal_searches'],[]]]),
        step('french_token_probe','work/contributions/packaging_audit/run_token_probe.py'),
        step('french_master_and_credits','work/contributions/validation_fr/audit_fr_master.py',checks=[
            ['work/contributions/validation_fr/INDEPENDENT_FR_MASTER_AUDIT.json',['pass'],True],
            ['work/contributions/validation_fr/READERS_CREDITS_AUDIT.json',['pass'],True]]),
        step('english_master_audit','work/contributions/validation_en/audit_english_master.py',checks=[
            ['work/contributions/validation_en/INDEPENDENT_EN_MASTER_AUDIT.json',['passed'],True]]),
        step('french_source_changes','work/contributions/changes/build_changes_fr.py'),
        step('english_source_changes','work/contributions/changes_en/build_changes_en.py',
             '--en','work/sources/SGA5_EN','--english','work/contributions/english',
             '--prepared','work/build/prepared','--output','work/contributions/changes_en'),
        step('complete_reader_changes','work/build/scripts/complete_reader_changes.py',checks=[
            ['work/contributions/reader_changes/COMPLETE_READER_CHANGELOG_RECONSTRUCTION.json',['all_final_reader_reconstructions_exact'],True]]),
    ]
    readers = [
        ('FR','SGA5_FR_diplomatique'),('FR','SGA5_FR_corrige_apparat'),('FR','SGA5_FR_texte_de_lecture'),
        ('EN','SGA5_EN_diplomatic'),('EN','SGA5_EN_corrected_apparatus'),('EN','SGA5_EN_reading'),
        ('FR','SGA5_FR_master_annotated'),('EN','SGA5_EN_master_annotated')]
    for language, name in readers:
        stages.append(step('compile_' + name,'work/build/scripts/compile_readers.py',f'deliverables/{language}/{name}.tex',
                           checks=[[f'deliverables/records/build_outputs/{name}.json',['success'],True],
                                   [f'deliverables/records/build_outputs/{name}.json',['error_count'],0]]))
    stages += [step('finalize_records','work/build/scripts/finalize_records.py'),
               step('package_deliverables','work/build/scripts/package_deliverables.py'),
               step('final_archive_privacy','work/contributions/packaging_audit/audit_packages.py',
                    'deliverables/SGA5_READERS_FR.zip','deliverables/SGA5_READERS_EN.zip','deliverables/SGA5_READERS_RECORDS.zip',
                    '--report-stem','FINAL_PACKAGE_PRIVACY')]
    return stages


def sha(data):
    return hashlib.sha256(data).hexdigest()


def clean(text):
    for label, pattern in PATTERNS:
        text = pattern.sub('[email omitted]' if label == 'email' else '[machine path omitted]',text)
    return text


def json_write(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def safe_member(name):
    path = PurePosixPath(name)
    return not path.is_absolute() and '..' not in path.parts and '\\' not in name and not (path.parts and ':' in path.parts[0])


def verify_archives(directory, extract=False):
    verified = []
    for archive_name in ARCHIVES:
        archive_path = directory / archive_name
        raw = archive_path.read_bytes()
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            members = archive.infolist()
            names = [m.filename for m in members]
            if len(names) != len(set(names)):
                raise ValueError('Duplicate ZIP member in '+archive_name)
            for info in members:
                if not safe_member(info.filename) or stat.S_ISLNK(info.external_attr >> 16):
                    raise ValueError('Unsafe archive member in '+archive_name)
            manifest_raw = archive.read('MANIFEST.tsv')
            rows = list(csv.DictReader(io.StringIO(manifest_raw.decode('utf-8')),delimiter='\t'))
            checked = []
            for row in rows:
                name = row['path_in_zip']
                if not safe_member(name):
                    raise ValueError('Unsafe manifest member in '+archive_name)
                data = archive.read(name)
                if len(data) != int(row['bytes']) or sha(data) != row['sha256']:
                    raise ValueError('Manifest verification failed: '+archive_name+':'+name)
                checked.append({'path_in_zip':name,'bytes':len(data),'sha256':sha(data)})
            destination = Path('work/sources') / archive_path.stem
            # Never overwrite a modified original source. Existing members
            # must match the attached archive exactly before reuse.
            for info in members:
                if info.is_dir():
                    continue
                dest = destination / info.filename
                data = archive.read(info)
                if dest.exists() and dest.read_bytes() != data:
                    raise ValueError('Existing original source differs: '+archive_name+':'+info.filename)
                if extract and not dest.exists():
                    dest.parent.mkdir(parents=True,exist_ok=True)
                    dest.write_bytes(data)
            verified.append({'archive':archive_name,'archive_bytes':len(raw),'archive_sha256':sha(raw),
                             'manifest_sha256':sha(manifest_raw),'manifest_rows':len(rows),
                             'all_manifest_members_verified':True,'extraction_requested':extract,'members':checked})
    return verified


def preflight(stages, require_tex):
    paths = sorted(set(REVIEWED_INPUTS + MODULE_DEPENDENCIES + [s['command'][1] for s in stages]))
    files = [{'path':name,'exists':Path(name).is_file(),
              'sha256':sha(Path(name).read_bytes()) if Path(name).is_file() else None} for name in paths]
    tools = {name:bool(shutil.which(name)) for name in ['patch','pdftotext','pdfinfo','pdftex','pdflatex','kpsewhich']}
    try:
        import PIL
        pillow = PIL.__version__
    except ImportError:
        pillow = None
    packages = {}
    if tools['kpsewhich']:
        for name in TEX_PACKAGES:
            run = subprocess.run(['kpsewhich',name],capture_output=True,text=True)
            packages[name] = run.returncode == 0 and bool(run.stdout.strip())
    missing_files = [r['path'] for r in files if not r['exists']]
    missing_tools = [name for name, present in tools.items() if not present and (require_tex or name in ['patch','pdftotext'])]
    missing_packages = [name for name in TEX_PACKAGES if not packages.get(name,False)] if require_tex else []
    return {'files':files,'missing_files':missing_files,'tools_available':tools,'Pillow_version':pillow,
            'TeX_packages':packages,'missing_tools':missing_tools,'missing_TeX_packages':missing_packages,
            'ready':not missing_files and not missing_tools and pillow is not None and not missing_packages}


def import_tex_environment(path):
    # Argument passing keeps the path outside shell-code interpolation.
    run = subprocess.run(['bash','-c','source "$1" && env -0','bash',str(path)],capture_output=True)
    if run.returncode:
        raise RuntimeError('Requested TeX environment could not be loaded')
    for entry in run.stdout.split(b'\0'):
        if b'=' in entry:
            key,value = entry.split(b'=',1)
            os.environ[key.decode()] = value.decode()


def check_results(checks):
    for path, keys, expected in checks:
        value = json.loads(Path(path).read_text())
        for key in keys:
            value = value[key]
        if value != expected:
            raise RuntimeError('Required result failed: '+path+':'+'.'.join(keys))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root',type=Path,default=Path('.'))
    parser.add_argument('--archives',type=Path,default=Path('upload'))
    parser.add_argument('--mode',choices=['plan','verify','build'],default='plan')
    parser.add_argument('--tex-env',type=Path)
    parser.add_argument('--output',type=Path,default=Path('work/contributions/packaging_audit/rebuild_outputs'))
    parser.add_argument('--stop-after',help='Run through this exact stage ID only; no completed-final-build claim is made.')
    parser.add_argument('--checkpoints',action='store_true',help='Create checkpoint ZIPs after each of the six ordinary readers compiles.')
    args = parser.parse_args()
    os.chdir(args.project_root)
    if args.tex_env:
        import_tex_environment(args.tex_env)
    stages = build_steps()
    if args.stop_after and args.stop_after not in {s['id'] for s in stages}:
        raise ValueError('Unknown stop-after stage')
    inputs = verify_archives(args.archives,extract=args.mode=='build')
    requirements = preflight(stages,require_tex=args.mode=='build')
    report = {'mode':args.mode,'layout':'Project root contains upload/, work/sources/, work/contributions/, work/build/, deliverables/.',
              'source_archives':inputs,'preflight':requirements,'stages':stages,
              'reviewed_input_policy':'Retain the supplied reviewed front-matter fragments, 43-record manual prose catalogue, projection-review dispositions, and attached prompt. Visual/editorial judgments are replayed from their recorded decisions.',
              'source_resolver_policy':'French preparation performs its own exact resolver once. English master preparation performs its own audit/apply/audit sequence. Do not add a second standalone resolver call.',
              'PDF_reproducibility':'Source bytes and semantic audits are checked; byte-identical PDFs require the same TeX engine/package/font versions in addition to the fixed SOURCE_DATE_EPOCH used by compile_readers.py.',
              'executed_stages':[],'completed_full_rebuild':False}
    json_write(args.output/'REBUILD_PLAN.json',report)
    if args.mode != 'build':
        print(json.dumps({'mode':args.mode,'archives_verified':3,'manifest_members':sum(r['manifest_rows'] for r in inputs),
                          'stages':len(stages),'missing_files':requirements['missing_files'],'build_executed':False},indent=2))
        return
    if not requirements['ready']:
        raise RuntimeError('Rebuild preflight failed; inspect REBUILD_PLAN.json for exact missing inputs or dependencies')
    completed_readers = []
    for ordinal, stage in enumerate(stages,1):
        command = [sys.executable,*stage['command'][1:]]
        started = time.monotonic()
        env = os.environ.copy()
        env['PYTHONDONTWRITEBYTECODE']='1'
        run = subprocess.run(command,capture_output=True,text=True,env=env)
        result = {'id':stage['id'],'command':stage['command'],'exit_code':run.returncode,
                  'elapsed_seconds':round(time.monotonic()-started,3),
                  'stdout':clean(run.stdout),'stderr':clean(run.stderr)}
        json_write(args.output/'steps'/f'{ordinal:02d}_{stage["id"]}.json',result)
        report['executed_stages'].append({k:v for k,v in result.items() if k not in ['stdout','stderr']})
        json_write(args.output/'REBUILD_PLAN.json',report)
        if run.returncode:
            raise RuntimeError('Rebuild stopped at '+stage['id']+'; inspect its screened step report')
        check_results(stage['checks'])
        if stage['id'].startswith('compile_') and 'master_annotated' not in stage['id']:
            completed_readers.append(stage['command'][2])
            if args.checkpoints:
                subprocess.run([sys.executable,'work/build/scripts/checkpoint.py',str(len(completed_readers)),
                                '--finished',*completed_readers],check=True,env=env,capture_output=True)
        print(json.dumps({'stage':stage['id'],'exit_code':0}),flush=True)
        if args.stop_after == stage['id']:
            report['stopped_after_requested_stage']=stage['id']
            json_write(args.output/'REBUILD_PLAN.json',report)
            return
    report['completed_full_rebuild']=True
    json_write(args.output/'REBUILD_PLAN.json',report)


if __name__=='__main__':
    main()
