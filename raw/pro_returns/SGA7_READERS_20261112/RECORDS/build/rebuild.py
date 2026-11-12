#!/usr/bin/env python3
"""Rebuild the SGA 7 readers from the three original archives and this record set.

Place the original SGA7_*.zip files in upload/. Run this script from the
unpacked records archive. Frozen editorial resolutions are deliberate inputs;
they are not replaced by fresh heuristic decisions during a rebuild.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / 'output' / 'records'


def run(name, *args):
    print('Running', name, *args, flush=True)
    subprocess.run([sys.executable, str(ROOT / 'build' / name), *args],
                   cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compile', action='store_true', help='Also build all six PDFs with installed TeX Live')
    parser.add_argument('--local-tex', action='store_true', help='Use a previously prepared workspace TeX configuration')
    args = parser.parse_args()
    RECORDS.mkdir(parents=True, exist_ok=True)
    (ROOT / 'work').mkdir(exist_ok=True)
    # Required records are at the root of the delivered records ZIP; the live
    # workspace keeps them together under output/records.
    for p in ROOT.iterdir():
        if p.is_file() and p.suffix in {'.json', '.tsv', '.md'}:
            target = RECORDS / p.name
            if not target.exists():
                shutil.copy2(p, target)
    archives = sorted((ROOT / 'upload').glob('SGA7_*.zip'))
    if len(archives) != 3:
        raise SystemExit('Put the three original SGA7 source archives in upload/ before rebuilding.')
    for script in ['verify_inputs.py', 'editorial_decisions.py', 'french.py',
                   'audit_fr.py', 'audit_exceptions.py', 'english_stage.py',
                   'english_variants.py']:
        run(script)
    # These scripts preserve or regenerate the explicit editorial decisions
    # from their frozen paired-source evidence.
    for script in ['glossary_en_resolutions.py', 'audit_en_nonlocal.py',
                   'audit_en_port_witnesses.py', 'audit_en_nonmath_i.py',
                   'nonmath_i_review.py', 'glossary_nonmath_audit.py',
                   'glossary_font_audit.py']:
        if (ROOT / 'build' / script).exists():
            run(script)
    run('english.py')
    for script in ['audit_en_nonmath_i.py', 'glossary_font_audit.py', 'glossary_nonmath_audit.py']:
        if (ROOT / 'build' / script).exists():
            run(script, '--reports-only')
    for script in ['glossary.py', 'english_audit.py', 'audit_frontmatter.py']:
        if (ROOT / 'build' / script).exists():
            run(script)
    if args.compile:
        for lang in ['fr', 'en']:
            for p in sorted((ROOT / 'output' / lang).glob('*.tex')):
                if 'master' in p.name:
                    continue
                options = [] if args.local_tex else ['--system-tex']
                run('compile_reader.py', str(p.relative_to(ROOT)), *options)
        run('master_pdfs.py')
        run('english_pdf_audit.py')
    run('english_attribution_audit.py', *([] if args.compile else ['--source-only']))
    run('edition_report.py')
    if (ROOT / 'build' / 'final_audit.py').exists():
        run('final_audit.py', *(['--require-pdfs'] if args.compile else []))
    run('write_readme.py')
    run('package.py', *([] if args.compile else ['--allow-incomplete']))


if __name__ == '__main__':
    main()
