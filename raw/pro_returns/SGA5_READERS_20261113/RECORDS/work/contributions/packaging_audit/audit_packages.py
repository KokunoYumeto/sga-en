#!/usr/bin/env python3
"""Inspect output archives without reproducing private matched values."""
from __future__ import annotations
import argparse
import ast
import collections
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

EMAIL = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
UNIX = re.compile(r"(?<![A-Za-z0-9_.])/(?:home|Users|workspace|root|tmp|mnt|var|opt|data|private|usr|etc)/[^\s\"'<>\[\]()]+")
WINDOWS = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/](?:Users|Documents(?: and Settings)?|Program Files|Windows|Temp|tmp|workspace|home)[\\/][^\s\"'<>\[\]()]+", re.I)
PATTERNS = [('email', EMAIL), ('absolute Unix path', UNIX), ('absolute Windows path', WINDOWS)]
NAIVE_DRIVE = re.compile(r'[A-Za-z]:\\')
TEXT_SUFFIXES = {'.tex','.py','.json','.jsonl','.tsv','.csv','.md','.txt','.log','.stdout','.aux','.out','.toc','.diff','.patch','.sty','.cls','.sh','.fls','.fdb_latexmk'}
RAW_DIRECTORIES = {'compile_check','runtime_check','flat_compile_check','compile_tmp','latex','__pycache__'}
ORIGINAL_ARCHIVES = {'SGA5_FR.zip','SGA5_EN.zip','SGA5_SCANS.zip'}
STANDARD_SHEBANGS = {'/' + 'usr/bin/env', '/' + 'usr/bin/python3'}


def sha(value):
    return hashlib.sha256(value.encode('utf-8') if isinstance(value, str) else value).hexdigest()


def declared_pattern_ranges(member, text):
    """Ignore only declared regex literals containing actual regex structure."""
    ranges = []
    def regex_literal(value):
        if not isinstance(value, str) or not any(token in value for token in ['(?:', '(?<!', '(?=', '(?!', '[^', '[A-Za-z', '[a-z', '[0-9', r'\s']):
            return False
        try:
            re.compile(value)
            return True
        except re.error:
            return False
    if member.endswith('.py'):
        try:
            tree = ast.parse(text)
        except SyntaxError:
            tree = None
        if tree is not None:
            lines = text.splitlines(keepends=True)
            offsets = [0]
            for line in lines:
                offsets.append(offsets[-1] + len(line))
            def coordinate(line, column):
                prefix = lines[line - 1].encode('utf-8')[:column].decode('utf-8')
                return offsets[line - 1] + len(prefix)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == 're' and node.func.attr in {'compile','sub','search','finditer','findall','match','fullmatch','split'} and node.args:
                    literal = node.args[0]
                    if isinstance(literal, ast.Constant) and regex_literal(literal.value):
                        ranges.append((coordinate(literal.lineno,literal.col_offset),coordinate(literal.end_lineno,literal.end_col_offset),'declared regular expression'))
                if isinstance(node, (ast.Assign, ast.AnnAssign)):
                    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                    names = [target.id.lower() for target in targets if isinstance(target, ast.Name)]
                    if any(name == 'patterns' or name.endswith('_patterns') for name in names) and isinstance(node.value, ast.Dict):
                        for literal in node.value.values:
                            if isinstance(literal, ast.Constant) and regex_literal(literal.value):
                                ranges.append((coordinate(literal.lineno,literal.col_offset),coordinate(literal.end_lineno,literal.end_col_offset),'declared regular-expression dictionary value'))
    if member.endswith(('.json','.jsonl')):
        for match in re.finditer(r'"(?:regular_expression|regex|pattern)"\s*:\s*("(?:\\.|[^"\\])*")',text):
            try:
                value = json.loads(match.group(1))
            except json.JSONDecodeError:
                continue
            if regex_literal(value):
                ranges.append((match.start(1),match.end(1),'declared regular expression'))
    return ranges


def scan_text(member, text, kind='text'):
    findings = []
    ignored = []
    declarations = declared_pattern_ranges(member, text)
    for label, pattern in PATTERNS:
        hits = []
        for match in pattern.finditer(text):
            exempt = next((reason for start,end,reason in declarations if start <= match.start() and match.end() <= end),None)
            if label == 'absolute Unix path' and match.group() in STANDARD_SHEBANGS and text.startswith('#!' + match.group()) and match.start() == 2:
                exempt = 'exact standard interpreter shebang'
            if exempt:
                ignored.append({'member':member,'representation':kind,'kind':exempt,'line_1based':text.count('\n',0,match.start())+1,'value_sha256':sha(match.group())})
            else:
                hits.append(match)
        if hits:
            findings.append({'member': member, 'representation': kind, 'kind': label, 'count': len(hits),
                             'lines_1based': sorted({text.count('\n', 0, m.start()) + 1 for m in hits}),
                             'match_sha256_counts': dict(collections.Counter(sha(m.group()) for m in hits)),
                             'values_omitted': True})
    return findings, ignored


def inspect_archive(path):
    findings, ignored, raw, members, pdf_failures, original_inputs = [], [], [], [], [], []
    naive_count = 0
    archive_data = path.read_bytes()
    with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
        unsafe = [i.filename for i in archive.infolist() if PurePosixPath(i.filename).is_absolute()
                  or '..' in PurePosixPath(i.filename).parts or '\\' in i.filename
                  or (PurePosixPath(i.filename).parts and ':' in PurePosixPath(i.filename).parts[0])]
        for info in archive.infolist():
            if info.is_dir():
                continue
            name = info.filename
            parts = PurePosixPath(name).parts
            suffix = PurePosixPath(name).suffix.lower()
            data = archive.read(info)
            members.append({'path_in_zip': name, 'bytes': len(data), 'sha256': sha(data)})
            if PurePosixPath(name).name in ORIGINAL_ARCHIVES or any(parts[i:i+2] == ('work','sources') for i in range(len(parts)-1)):
                original_inputs.append({'path_in_zip':name,'bytes':len(data),'reason':'original private input archive or extracted originals must remain external'})
            is_raw = bool(set(parts).intersection(RAW_DIRECTORIES)) or suffix in {'.stdout','.aux','.toc','.out','.fls','.fdb_latexmk'}
            if is_raw:
                raw.append({'path_in_zip': name, 'bytes': len(data), 'reason': 'execution-directory or compiler intermediate artifact'})
            if suffix in TEXT_SUFFIXES:
                text = data.decode('utf-8', errors='replace')
                found, exempt = scan_text(name, text)
                findings += found
                ignored += exempt
                naive_count += len(NAIVE_DRIVE.findall(text))
            elif suffix == '.pdf':
                result = subprocess.run(['pdftotext','-','-'],input=data,capture_output=True)
                if result.returncode:
                    pdf_failures.append(name)
                else:
                    found, exempt = scan_text(name, result.stdout.decode('utf-8', errors='replace'), 'extracted PDF text')
                    findings += found
                    ignored += exempt
                # This catches plain PDF metadata values even when they are
                # absent from text extraction; decompressed page content is
                # covered by pdftotext above.
                found, exempt = scan_text(name, data.decode('latin-1'), 'PDF raw metadata/string scan')
                findings += found
                ignored += exempt
    return {'archive': path.name, 'archive_bytes': len(archive_data), 'archive_sha256': sha(archive_data),
            'members': len(members), 'unsafe_member_names': unsafe, 'privacy_findings': findings,
            'private_match_count': sum(f['count'] for f in findings), 'members_with_privacy_findings': len({f['member'] for f in findings}),
            'raw_compile_artifacts': raw, 'raw_compile_artifact_count': len(raw),
            'prohibited_original_inputs': original_inputs, 'prohibited_original_input_count': len(original_inputs),
            'pdf_text_extraction_failures': pdf_failures, 'naive_drive_prefix_candidates': naive_count,
            'strict_windows_path_matches': sum(f['count'] for f in findings if f['kind'] == 'absolute Windows path'),
            'explicit_nonprivate_exceptions': ignored,
            'archive_inventory': members}


def regression_cases():
    maths = [r'f:\mathcal{C}\to\mathcal{D}', r'A:\cC\longrightarrow\cD', r'\Tr_A:\uRHom_A(E,E)', r'V:\operatorname{Vect}']
    assert all(not any(pattern.search(value) for _, pattern in PATTERNS) for value in maths)
    assert all(NAIVE_DRIVE.search(value) for value in maths)
    # Keep fixture values out of reports and avoid literal private-looking
    # values in source code; the report contains classifications only.
    windows = 'C:' + chr(92) + 'Users' + chr(92) + 'fixture' + chr(92) + 'sample.tex'
    unix = '/' + 'workspace' + '/' + 'fixture' + '/sample.log'
    email = 'fixture' + chr(64) + 'example.invalid'
    assert WINDOWS.search(windows) and UNIX.search(unix) and EMAIL.search(email)
    return {'mathematical_drive_prefix_examples': maths, 'mathematical_examples_preserved': len(maths),
            'synthetic_windows_path_detected': True, 'synthetic_unix_path_detected': True, 'synthetic_email_detected': True,
            'qualification': 'A bare letter-colon-backslash is insufficient evidence of a machine path; known filesystem directory context is required.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('archives', nargs='+', type=Path)
    parser.add_argument('--output', type=Path, default=Path('work/contributions/packaging_audit'))
    parser.add_argument('--report-stem', default='CHECKPOINT_PRIVACY')
    parser.add_argument('--allow-findings', action='store_true', help='Write diagnostic results without a failing exit status.')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    results = [inspect_archive(path) for path in args.archives]
    result = {'archive_audits': results, 'privacy_detector_regressions': regression_cases(),
              'scope': 'All recognized textual members and PDF extracted text/raw string metadata; matched private values are hashed, never copied into this report.',
              'packaging_rule': 'Exclude original input archives/extracted originals, raw execution directories, compiler intermediates, raw stdout and caches. Retain only screened public compile logs, structured summaries, and the screened minimal folio248 INITEX proof log.'}
    (args.output / (args.report_stem + '_AUDIT.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    lines = ['# Checkpoint privacy and execution-artifact audit', '',
             '| Archive | Members | Members with private values | Private matches | Raw compile artifacts |',
             '|---|---:|---:|---:|---:|']
    for row in results:
        lines.append(f"| `{row['archive']}` | {row['members']} | {row['members_with_privacy_findings']} | {row['private_match_count']} | {row['raw_compile_artifact_count']} |")
    lines += ['', 'The JSON report records archive SHA-256 values, member hashes, finding categories, and line numbers. It deliberately omits matched private values.', '',
              '## Required exclusions', '',
              'Exclude `compile_check/`, `runtime_check/`, `flat_compile_check/`, `compile_tmp/`, raw LaTeX build directories, `.stdout`, `.aux`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, and `__pycache__/`. Keep the screened `deliverables/records/build_outputs/` logs and summaries after testing their complete contents.', '',
              '## Mathematical expressions and path detection', '',
              'A broad drive-prefix pattern such as a single letter followed by colon and backslash also matches mathematical expressions. The regression cases preserve `f:\\mathcal{C}\\to\\mathcal{D}`, `A:\\cC\\longrightarrow\\cD`, and corresponding trace/vector examples. A Windows-path finding requires a known filesystem directory immediately after the drive prefix. Unix paths require an explicit absolute filesystem root; relative archive/build references remain intact.', '',
              'Avoid any broad drive-path substitution after a more precise redactor: it can erase mathematical text in diagnostics. The scanner requires known-directory Windows-root context. Its only explicit path-like exceptions are exact standard interpreter shebangs and declared regular-expression literals that contain regex structure rather than an actual private file value. Every exception is listed by member, line, category, and hash. Sanitization must never rewrite mathematical reader content.', '']
    for row in results:
        if row['raw_compile_artifacts']:
            lines += ['## Raw artifacts in '+row['archive'], '']
            lines += ['- `'+entry['path_in_zip']+'`' for entry in row['raw_compile_artifacts']]
            lines += ['']
    (args.output / (args.report_stem + '_REPORT.md')).write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps([{'archive':r['archive'],'members':r['members'],'private_members':r['members_with_privacy_findings'],
                       'private_matches':r['private_match_count'],'raw_compile_artifacts':r['raw_compile_artifact_count'],
                       'prohibited_original_inputs':r['prohibited_original_input_count'],
                       'naive_drive_prefix_candidates':r['naive_drive_prefix_candidates']} for r in results],indent=2))
    if not args.allow_findings and any(r['privacy_findings'] or r['raw_compile_artifacts'] or r['unsafe_member_names'] or r['pdf_text_extraction_failures'] or r['prohibited_original_inputs'] for r in results):
        raise SystemExit(1)


if __name__=='__main__':
    main()
