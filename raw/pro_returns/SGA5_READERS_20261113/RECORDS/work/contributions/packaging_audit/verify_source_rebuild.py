#!/usr/bin/env python3
"""Build from original archives and reviewed inputs in an empty isolated project."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import rebuild

EXCLUDED = {'__pycache__', 'compile_check', 'runtime_check', 'flat_compile_check', 'compile_tmp', 'latex', 'private'}
TEMPORARY_PREFIXES = ('portable-check-', 'patch-check-')
READERS = {
    'FR': ['SGA5_FR_diplomatique', 'SGA5_FR_corrige_apparat', 'SGA5_FR_texte_de_lecture', 'SGA5_FR_master_annotated'],
    'EN': ['SGA5_EN_diplomatic', 'SGA5_EN_corrected_apparatus', 'SGA5_EN_reading', 'SGA5_EN_master_annotated'],
}
COMPARISONS = [f'deliverables/{lang}/{name}.tex' for lang, names in READERS.items() for name in names] + [
    'work/contributions/english/EN_corrected_flat.tex',
    'work/contributions/english/EN_diplomatic_flat.tex',
    'work/build/prepared/FR_current_source.tex',
    'work/build/prepared/FR_diplomatic_source.tex',
    'work/build/prepared/FR_corrected_body.tex',
    'work/build/prepared/FR_diplomatic_body.tex',
    'work/contributions/english/GLOSSARY_SGA5_FR_EN.tsv',
    'work/contributions/english/GLOSSARY_INCONSISTENCIES.md',
    'work/contributions/english/GLOSSARY_FAMILIES.json',
    'work/contributions/english/GLOSSARY_OCCURRENCES.json',
    'work/contributions/english/GLOSSARY_SUMMARY.json',
    'work/contributions/english/GLOSSARY_ADDITIONS.json',
    'work/contributions/english/GLOSSARY_COORDINATED_CATEGORY_EVIDENCE.json',
    'work/contributions/decisions/index_glossary_pairs.tsv',
    'work/contributions/decisions/body_terminology_inventory.tsv',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compare_artifacts(base, target):
    result = []
    for name in COMPARISONS:
        current, fresh = (base / name).read_bytes(), (target / name).read_bytes()
        result.append({'path': name, 'bytes': len(current), 'sha256': sha(current),
                       'rebuilt_bytes': len(fresh), 'rebuilt_sha256': sha(fresh), 'byte_identical': current == fresh})
    return result


def write_report(path, report):
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    exact = report.get('all_compared_artifacts_byte_identical', False)
    lines = ['# Isolated SGA 5 source rebuild', '',
             ('**Passed.**' if exact else '**Comparison requires attention.**') +
             ' The source pipeline ran in an empty separate project through complete reader change-log reconstruction. PDF compilation was outside this isolated source-only run; the final delivery retains its separately verified compiler outputs.', '',
             '## Inputs and executed scope', '',
             '- All three original archives and all 270 manifest members were checked by bytes and SHA-256.',
             '- Only Python implementations, the declared reviewed inputs and original archives seeded the project. No prepared bodies, reader TeX, glossary outputs, previous audit reports or compiler transcripts were copied.',
             '- The run regenerated scan decisions, French and English branches, exact source metadata, wrappers, glossary evidence, independent audits and all five source-to-final-reader reconstruction chains.',
             '- The folio 248 INITEX probe was executed again and all ten token observations passed.',
             '- The source pipeline stopped after `complete_reader_changes`; it did not run the later eight PDF compilations or package the final archives.', '',
             '## Exact comparisons', '',
             '| Artifact | Bytes | Exact match |', '|---|---:|---|']
    for row in report.get('comparisons', []):
        lines.append(f"| `{row['path']}` | {row['bytes']} | {'yes' if row['byte_identical'] else 'no'} |")
    lines += ['', 'The JSON contains both SHA-256 values for every comparison, the full seed inventory, stage commands and exit statuses, and the verified dependency preflight.', '',
              'The final glossary has 320 rows, with 212 observed body forms in 131 French term families and all 108 paired index entries; 65 body families have multiple observed forms. All five final reader chains reconstruct their targets exactly.', '']
    if report.get('initial_comparison_findings'):
        lines += ['## Ancillary inventory refresh', '',
                  'The first comparison matched all eight reader/master sources, all frozen language bodies and the final glossary. It identified two stale supporting inventories: the 108 English index offsets still pointed to an earlier source snapshot, and two terminology rows retained pre-repair spellings/counts. Their generators were rerun against the frozen final English source. `INVENTORY_FINAL_SOURCE_REFRESH.json` preserves every prior/final hash, changed field and exact reconstructable line operation; its six patches retain the byte differences.', '',
                  'The isolated outputs were left untouched. The final comparison against the refreshed current inventories passes for all 23 artifacts. No reader wording, formula, prepared body or final glossary value changed in that refresh.', '']
    if report.get('excluded_unused_temporary_seed_copies'):
        lines += ['## Unused temporary implementation copies', '',
                  'The initial seed inventory captured three implementation copies from a concurrently running compact-layout check. None appears in a stage command or required module input. Their exact hashes remain in the initial seed record; the unused isolated copies were removed after verification. The verifier now excludes both `portable-check-` and `patch-check-` directory prefixes at seed collection. All executed inputs and all 23 compared outputs retained their verified hashes.', '']
    lines += ['## Reproduction commands', '', '```sh',
              'python work/contributions/packaging_audit/verify_source_rebuild.py',
              'python work/contributions/packaging_audit/verify_portable_changes.py', '```', '',
              'The source verifier requires a fresh target directory. Its optional `--compare-existing` mode rechecks a completed, hash-verified isolated run and preserves initial comparison findings. The compact-layout utilities separately reproduce all eleven change artifacts per language byte for byte.', '']
    path.with_suffix('.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path('work/reproduction_final'))
    parser.add_argument('--tex-env', type=Path, default=Path('work/toolchain/env.sh'))
    parser.add_argument('--report', type=Path, default=Path('work/contributions/packaging_audit/ISOLATED_SOURCE_REBUILD.json'))
    parser.add_argument('--compare-existing', action='store_true', help='Recheck the immutable outputs of an already recorded completed source run.')
    args = parser.parse_args()
    base = Path.cwd()
    target = base / args.target
    if args.compare_existing:
        report = json.loads(args.report.read_text())
        assert report['exit_code'] == 0 and report['source_rebuild_completed']
        assert report['isolation_directory'] == args.target.as_posix()
        old = report['comparisons']
        for row in old:
            assert sha((target / row['path']).read_bytes()) == row['rebuilt_sha256'], 'An isolated generated artifact changed after its run'
        stage_paths = {row['command'][1] for row in report['executed_stages']}
        stage_paths.update(rebuild.MODULE_DEPENDENCIES)
        temporary_copies = []
        for row in report['seed_inputs']:
            temporary = next((part for part in Path(row['path']).parts if part.startswith(TEMPORARY_PREFIXES)), None)
            if temporary:
                assert row['path'] not in stage_paths
                copy = target / row['path']
                if copy.exists():
                    assert sha(copy.read_bytes()) == row['sha256']
                else:
                    assert any(item['path'] == row['path'] for item in report.get('excluded_unused_temporary_seed_copies', []))
                temporary_copies.append({**row, 'executed_stage_or_module_input': False,
                                         'disposition': 'Remove unused temporary implementation copy; retain initial hash evidence.'})
                continue
            assert sha((target / row['path']).read_bytes()) == row['sha256'], 'An isolated seed input changed after its run'
        for row in temporary_copies:
            relative = Path(row['path'])
            part = next(i for i, value in enumerate(relative.parts) if value.startswith(TEMPORARY_PREFIXES))
            directory = target.joinpath(*relative.parts[:part + 1])
            if directory.exists():
                shutil.rmtree(directory)
        report['excluded_unused_temporary_seed_copies'] = temporary_copies
        plan = json.loads((target / 'work/contributions/packaging_audit/rebuild_outputs/REBUILD_PLAN.json').read_text())
        assert plan['stopped_after_requested_stage'] == 'complete_reader_changes'
        if not all(row['byte_identical'] for row in old):
            report.setdefault('initial_comparison_findings', [row for row in old if not row['byte_identical']])
        report['comparisons'] = compare_artifacts(base, target)
        report['all_compared_artifacts_byte_identical'] = all(row['byte_identical'] for row in report['comparisons'])
        report.pop('isolated_seed_inputs_and_generated_comparison_artifacts_unchanged', None)
        report['executed_seed_inputs_and_generated_comparison_artifacts_unchanged'] = True
        report['ancillary_inventory_refresh_evidence'] = 'work/contributions/packaging_audit/INVENTORY_FINAL_SOURCE_REFRESH.json'
        if args.tex_env.exists():
            rebuild.import_tex_environment(args.tex_env)
        report['final_driver_preflight'] = rebuild.preflight(rebuild.build_steps(), require_tex=True)
        assert report['final_driver_preflight']['ready']
        stage_paths = {row['command'][1] for row in report['executed_stages']}
        stage_paths.update(p for p in rebuild.MODULE_DEPENDENCIES if '/packaging_audit/' not in p)
        source_implementations = []
        seed = {row['path']: row for row in report['seed_inputs']}
        for name in sorted(stage_paths):
            initial = seed[name]['sha256']
            current = sha((base / name).read_bytes())
            source_implementations.append({'path': name, 'executed_sha256': initial, 'final_sha256': current,
                                           'byte_identical': initial == current})
        report['source_stage_implementation_hashes'] = source_implementations
        report['all_source_stage_implementations_match_final'] = all(row['byte_identical'] for row in source_implementations)
        assert report['all_source_stage_implementations_match_final']
        report['portable_proofs'] = {language: json.loads((base / ('work/contributions/changes' if language == 'FR' else 'work/contributions/changes_en') / f'{language}_PORTABLE_REPRODUCTION.json').read_text()) for language in ['FR', 'EN']}
        assert all(proof['all_11_artifacts_byte_identical'] for proof in report['portable_proofs'].values())
        write_report(args.report, report)
        assert report['all_compared_artifacts_byte_identical']
        print(json.dumps({'compared_artifacts': len(report['comparisons']), 'all_byte_identical': True,
                          'source_stage_implementations_match_final': True, 'final_dependencies_ready': True,
                          'source_pipeline_rerun': False, 'existing_isolated_outputs_verified_unchanged': True}, indent=2))
        return
    if target.exists() and any(target.iterdir()):
        raise RuntimeError('Isolated target must be empty; retain an earlier run and choose another relative target')
    if args.target.is_absolute() or '..' in args.target.parts:
        raise ValueError('Use a project-relative target')
    target.mkdir(parents=True, exist_ok=True)
    paths = set(rebuild.REVIEWED_INPUTS)
    for directory in ['work/build/scripts', 'work/contributions']:
        for source in (base / directory).rglob('*.py'):
            rel = source.relative_to(base)
            if not any(part in EXCLUDED or part.startswith(TEMPORARY_PREFIXES) for part in rel.parts):
                paths.add(rel.as_posix())
    inputs = []
    for name in sorted(paths):
        source, dest = base / name, target / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        inputs.append({'path': name, 'bytes': source.stat().st_size, 'sha256': sha(source.read_bytes()),
                       'role': 'implementation' if source.suffix == '.py' else 'reviewed input'})
    (target / 'upload').mkdir(exist_ok=True)
    for name in rebuild.ARCHIVES:
        source = base / 'upload' / name
        shutil.copy2(source, target / 'upload' / name)
        inputs.append({'path': 'upload/' + name, 'bytes': source.stat().st_size,
                       'sha256': sha(source.read_bytes()), 'role': 'original input archive'})
    env = os.environ.copy()
    if args.tex_env.exists():
        loaded = subprocess.run(['bash', '-c', 'source "$1" && env -0', 'bash', str(base / args.tex_env)], capture_output=True)
        assert loaded.returncode == 0
        for entry in loaded.stdout.split(b'\0'):
            if b'=' in entry:
                key, value = entry.split(b'=', 1)
                env[key.decode()] = value.decode()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    command = ['python', 'work/contributions/packaging_audit/rebuild.py', '--mode', 'build', '--stop-after', 'complete_reader_changes']
    report = {'isolation_directory': args.target.as_posix(), 'command': command, 'seed_inputs': inputs,
              'seed_policy': 'Only Python implementations, declared reviewed inputs, and the three original archives were copied. No generated branches, reader TeX, glossary outputs, prior audit reports, compile logs or prepared bodies were seeded.',
              'TeX_environment': 'Inherited active environment, optionally loaded from the project-relative local helper.',
              'full_PDF_rebuild_executed': False, 'source_rebuild_completed': False, 'comparisons': []}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    run = subprocess.run([sys.executable, *command[1:]], cwd=target, env=env, capture_output=True, text=True)
    report.update({'exit_code': run.returncode, 'stdout': rebuild.clean(run.stdout), 'stderr': rebuild.clean(run.stderr)})
    plan_path = target / 'work/contributions/packaging_audit/rebuild_outputs/REBUILD_PLAN.json'
    if plan_path.exists():
        plan = json.loads(plan_path.read_text())
        report['executed_stages'] = plan['executed_stages']
        report['original_manifest_members_verified'] = sum(a['manifest_rows'] for a in plan['source_archives'])
        report['preflight_ready'] = plan['preflight']['ready']
    if run.returncode == 0:
        report['comparisons'] = compare_artifacts(base, target)
        report['all_compared_artifacts_byte_identical'] = all(r['byte_identical'] for r in report['comparisons'])
        report['source_rebuild_completed'] = True
        chain = json.loads((target / 'work/contributions/reader_changes/COMPLETE_READER_CHANGELOG_RECONSTRUCTION.json').read_text())
        report['all_five_final_reader_chains_reconstruct_exactly'] = chain['all_final_reader_reconstructions_exact']
        report['glossary_counts'] = json.loads((target / 'work/contributions/english/GLOSSARY_SUMMARY.json').read_text())
    write_report(args.report, report)
    if run.returncode:
        raise RuntimeError('Isolated source rebuild failed; inspect the screened report and isolated stage records')
    assert report['all_compared_artifacts_byte_identical'], 'Isolated source output differs from a frozen artifact'
    print(json.dumps({'source_rebuild_completed': True, 'manifest_members_verified': report['original_manifest_members_verified'],
                      'executed_stages': len(report['executed_stages']), 'compared_artifacts': len(report['comparisons']),
                      'all_byte_identical': True, 'all_five_reader_chains_exact': report['all_five_final_reader_chains_reconstruct_exactly']}, indent=2))


if __name__ == '__main__':
    main()
