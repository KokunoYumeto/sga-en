#!/usr/bin/env python3
"""Reproduce and audit the supplied English source without claiming collation.

Invoke from the extracted archive root:
    python review/english/audit_build_english.py [--compile]

All recorded paths are archive-relative.  The source map records line origins;
candidate term counts are literal occurrences and do not assert translation
equivalence.  Compilation is a build check, not a check against the scan.
"""
from __future__ import annotations

import argparse
import bisect
import collections
import csv
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'review/english'
SOURCE = ROOT / 'en/sources/SGA6_English_current_buildable_source_20260823'
MAIN = SOURCE / '02f_SGA6_English_Master.tex'
RELEASE = ROOT / 'en/release_v2026-11-12/07_SGA6_EN_CURRENT_LAYERED_READER.tex'


def write_tsv(name, fields, rows):
    with (OUT / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def flatten():
    lines, origins, dependencies, inactive = [], [], [], []

    def visit(path, stack=()):
        rel = str(path.relative_to(ROOT))
        if path in stack:
            raise ValueError('Cyclic source inclusion: ' + rel)
        dependencies.append(rel)
        for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(True), 1):
            m = re.fullmatch(r'\s*\\(?:input|include)\{([^}]+)\}\s*(?:%[^\n]*)?\n?', line)
            if m:
                target = SOURCE / m.group(1)
                if not target.suffix:
                    target = target.with_suffix('.tex')
                if not target.exists():
                    raise FileNotFoundError('Active source missing: ' + str(target.relative_to(ROOT)))
                visit(target, stack + (path,))
            else:
                if '\\SGAArchiveOnly{\\input{' in line:
                    inactive.append({'source_file': rel, 'source_line': line_no,
                                     'tokens': line.rstrip('\n'),
                                     'reason': 'SGAArchiveOnly is defined to consume its argument without expansion.'})
                lines.append(line)
                origins.append({'flat_line': len(lines), 'source_file': rel, 'source_line': line_no})

    visit(MAIN)
    text = ''.join(lines)
    (OUT / 'SGA6_EN_native_flattened_UNVERIFIED.tex').write_text(text, encoding='utf-8')
    write_tsv('EN_SOURCE_MAP.tsv', ['flat_line', 'source_file', 'source_line'], origins)
    (OUT / 'EN_INPUT_GRAPH.json').write_text(json.dumps({'active_files':dependencies,'inactive_inputs':inactive}, ensure_ascii=False, indent=2)+'\n')
    return text, origins, dependencies, inactive


def inspect_release(flat):
    old = RELEASE.read_text(encoding='utf-8')
    before, after = old.splitlines(True), flat.splitlines(True)
    changes=[]
    for k,(tag,i,j,a,b) in enumerate(difflib.SequenceMatcher(None,before,after,autojunk=False).get_opcodes(),1):
        if tag == 'equal':
            continue
        changes.append({'id':f'EN-BASE-DIFF-{len(changes)+1:04d}','kind':tag,
                        'before_file':str(RELEASE.relative_to(ROOT)),
                        'before_lines':f'{i+1}-{j}','after_file':'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex',
                        'after_lines':f'{a+1}-{b}','before':''.join(before[i:j]),'after':''.join(after[a:b]),
                        'status':'mechanical comparison; editorial meaning requires review'})
    write_tsv('EN_NATIVE_VS_RELEASE.tsv',list(changes[0]) if changes else ['id','kind','before_file','before_lines','after_file','after_lines','before','after','status'],changes)
    return changes


def source_outline(flat, origins):
    rows=[]
    expose='front matter'
    target=''
    for n,line in enumerate(flat.splitlines(),1):
        m=re.search(r'\\sgaStableTarget(?:Inline)?\{([^}]+)\}',line)
        if m:
            target=m.group(1)
            em=re.match(r'sga6\.e(\d+)\.',target)
            if em:
                expose=em.group(1)
        if re.search(r'\\(?:sub)*section\*?\{',line):
            o=origins[n-1]
            rows.append({'expose':expose,'stable_target':target,'flat_line':n,
                         'source_file':o['source_file'],'source_line':o['source_line'],
                         'heading_tex':line.strip(),'printed_folio':'','status':'unmatched to printed-page boundary'})
    write_tsv('EN_OUTLINE.tsv',list(rows[0]),rows)
    return rows


def credentials():
    # Preserve complete attribution and source blocks; their wording is evidence.
    names=['en/repo_records/ATTRIBUTION.md','en/sources/SOURCES.md','en/repo_records/SOURCE_AUTHORITY.md']
    chunks=['# Required credit sources for the SGA 6 build\n\nThe following text is copied from the supplied records. It preserves the named contributions and their stated scopes.\n']
    for name in names:
        chunks.append('\n## '+name+'\n\n'+(ROOT/name).read_text())
    readme=(ROOT/'en/repo_records/README.md').read_text()
    for title in ['How it was made','Sources and credits']:
        m=re.search(r'(?ms)^## '+re.escape(title)+r'\n(.*?)(?=^## |\Z)',readme)
        chunks.append('\n## en/repo_records/README.md: '+title+'\n'+m.group(1))
    text='\n'.join(chunks)
    # Hard stop, rather than silently deleting any credit evidence.
    assert not re.search(r'[\w.+%-]+@[\w.-]+\.[A-Za-z]{2,}',text)
    assert not re.search(r'(?:/Users/|/home/|/workspace/|[A-Za-z]:\\\\)',text)
    (OUT/'CREDITS_REQUIRED.md').write_text(text,encoding='utf-8')


def glossary_candidates(flat, origins):
    fr=(ROOT/'fr/sga6/current/main.tex').read_text()
    # Body occurrences only. Keep raw TeX and exact Unicode case; no silent
    # canonicalization of mathematical symbols, inflections or accented text.
    fr_body=fr.split('\\begin{document}',1)[1]
    en_body=flat.split('\\begin{document}',1)[1]
    en_start_lines=flat[:flat.index('\\begin{document}')+len('\\begin{document}')].count('\n')
    en_offsets=[0]+[m.end() for m in re.finditer('\n',en_body)]
    fr_markers=list(re.finditer(r'%%%%%%%%%%\s+scan idx\s+\d+\s*\|\s*folio\s+(\d+)\s+%%%%%%%%%%',fr_body))
    keys=collections.defaultdict(list)
    for p in sorted((ROOT/'en/glossaries').glob('*.tsv')):
        rows=list(csv.DictReader(p.open(encoding='utf-8'),delimiter='\t'))
        for i,row in enumerate(rows,2):
            f=row.get('french_term_or_notation',row.get('French term or notation',row.get('french','')))
            e=row.get('english_rendering',row.get('English rendering',row.get('english','')))
            if f and e:
                keys[(f,e)].append({'volume':p.stem.replace('GLOSSARY_','').replace('_FR_EN',''),
                                   'source':str(p.relative_to(ROOT))+'#'+str(i)})
    records=[]
    for (f,e),refs in sorted(keys.items()):
        # Boundary guards prevent counting 'Spec' inside another word/command.
        def find(t,term):
            left=r'(?<![A-Za-zÀ-ÿ])' if term[0].isalpha() else ''
            right=r'(?![A-Za-zÀ-ÿ])' if term[-1].isalpha() else ''
            return list(re.finditer(left+re.escape(term)+right,t))
        fm=find(fr_body,f)
        em=find(en_body,e)
        if not fm:
            continue
        fi=fm[0].start(); pindex=bisect.bisect_right([m.start() for m in fr_markers],fi)-1
        folio=fr_markers[pindex].group(1) if pindex>=0 else 'front matter'
        first_en=''
        if em:
            el=bisect.bisect_right(en_offsets,em[0].start())+en_start_lines
            origin=origins[el-1]
            first_en=f"{origin['source_file']}#{origin['source_line']}"
        records.append({'french_term_or_notation':f,'english_rendering':e,
                        'english_literal_count':len(em),'french_literal_count':len(fm),
                        'first_french_folio':folio,'first_english_place':first_en,
                        'reference_volumes':'; '.join(sorted({x['volume'] for x in refs})),
                        'reference_sources':'; '.join(x['source'] for x in refs),
                        'status':'candidate; French and English occurrences have not been paired',
                        'method':'exact case-sensitive literal occurrence with alphabetic boundaries in TeX body; includes formula operands, comments and headings; excludes preamble'})
    write_tsv('GLOSSARY_SGA6_CANDIDATES.tsv',list(records[0]),records)
    groups=collections.defaultdict(list)
    for r in records:
        if r['english_literal_count']:
            groups[r['french_term_or_notation']].append(r)
    cross=[]
    for f,rs in sorted(groups.items()):
        if len({r['english_rendering'] for r in rs})<2:
            continue
        cross.append({'french_term_or_notation':f,
                      'attested_english_candidates':'; '.join(r['english_rendering'] for r in rs),
                      'counts':'; '.join(str(r['english_literal_count']) for r in rs),
                      'reference_volumes':'; '.join(sorted({r['reference_volumes'] for r in rs})),
                      'status':'requires paired-context adjudication; counts alone do not establish inconsistent translation'})
    write_tsv('CROSS_VOLUME_TERM_CANDIDATES.tsv',list(cross[0]),cross)
    return len(records),len(cross)


def compile_native():
    name='SGA6_EN_native_flattened_UNVERIFIED'
    statuses=[]
    for attempt in range(1,3):
        p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=OUT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        # Do not retain raw TeX transcripts: TeX package-loading paths are local.
        console=p.stdout
        errors=[l for l in console.splitlines() if l.startswith('!')]
        warnings=[l for l in console.splitlines() if 'Warning:' in l or 'Overfull \\' in l or 'Underfull \\' in l]
        output=next((l for l in console.splitlines() if l.startswith('Output written on ')),'')
        statuses.append({'run':attempt,'exit_code':p.returncode,'errors':errors,'warning_lines':warnings,'output':output})
        if p.returncode:
            break
    (OUT/'EN_NATIVE_BUILD_STATUS.json').write_text(json.dumps(statuses,ensure_ascii=False,indent=2)+'\n')
    return statuses


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--compile',action='store_true'); args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    flat,origins,deps,inactive=flatten()
    diff=inspect_release(flat)
    outline=source_outline(flat,origins)
    credentials()
    candidates,cross=glossary_candidates(flat,origins)
    status={'source_files':len(deps),'flattened_characters':len(flat),'flattened_lines':len(origins),
            'flattened_sha256_utf8':sha(flat),'release_diff_hunks':len(diff),'headings':len(outline),
            'glossary_candidates':candidates,'cross_volume_candidates':cross,
            'scan_collated':False,'complete_translation_audit':False,'verified_English_diplomatic_layer':False}
    if args.compile:
        status['build']=compile_native()
    (OUT/'EN_AUDIT_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(status,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
