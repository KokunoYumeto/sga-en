#!/usr/bin/env python3
"""Create an immutable numbered checkpoint; never includes an older ZIP.

Inputs remain in the user's four supplied archives. This checkpoint retains
derived text, exact review records and reproducible scripts. It is deliberately
not named as a completed reader release while the release gate remains false.
"""
import argparse
import collections
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPOSES=[('0',1,77),('I',78,159),('II',160,221),('III',222,273),('IV',274,296),('V',297,364),('VI',365,415),('VII',416,465),('VIII',466,497),('IX',498,518),('X',519,594),('XII',595,615),('XIII',616,666),('XIV',667,690),('Indices',691,700)]

def exposure(page):
    try:n=int(page)
    except (ValueError,TypeError):return 'Front matter'
    return next((name for name,a,b in EXPOSES if a<=n<=b),'Other')

def make_docs():
    rec=ROOT/'records';status=json.loads((rec/'CHECKPOINT_STATUS.json').read_text())
    variants=json.loads((rec/'FR_VARIANTS.json').read_text()) if (rec/'FR_VARIANTS.json').exists() else []
    counts=collections.Counter(exposure(v['page']) for v in variants)
    lines=['# Apparatus counts — unfinished checkpoint','',
      'These are generated entry counts, not counts of independently approved corrections. The source-to-scan decision links remain under review.',
      '', '| Exposé | FR diplomatic | FR apparatus | FR reading |', '|---|---:|---:|---:|']
    for name in ['Front matter']+[e[0] for e in EXPOSES]:
        lines.append(f'| {name} | 0 | {counts[name]} | 0 |')
    lines.extend(['','French kind: layered-text variant. Classification and scan-decision linkage are incomplete.',
      'English counts are in review/english/EN_CANDIDATE_STATUS.json and EN_VARIANTS.jsonl; only individually aligned English variants are entered.',''])
    (rec/'APPARATUS_COUNTS.md').write_text('\n'.join(lines))
    compile_rows=[]
    for f in sorted(rec.glob('COMPILE_*.json')):
        d=json.loads(f.read_text());compile_rows.append(d)
    english=ROOT/'review/english/EN_CANDIDATE_BUILD_STATUS.json'
    enbuild=json.loads(english.read_text()) if english.exists() else {}
    text=['# SGA 6 reader checkpoint','',
      '**Status: incomplete. This is a resumable checkpoint, not the requested final six-reader release.**','',
      '## Verification recorded at this checkpoint','',
      f"{status['pages']['checked']} of {status['pages']['total']} primary front-matter/numbered pages have an independent full-page comparison recorded. {status['pages']['unchecked']} remain unchecked or incomplete.",'',
      '| Record class | Total | Decided | Pending |','|---|---:|---:|---:|']
    for k in ['finding','fixlog','misprint','replay','manual','hold_difference','rejected_codex']:
        r=status[k];text.append(f"| {k} | {r['total']} | {r['decided']} | {r['pending']} |")
    text.extend(['',f"Own findings recorded: {status['own_findings']}.",'',
      'In PAGES_CHECKED.tsv, findings counts checker and hand-placed findings plus new independent findings, without recounting their FIXLOG or misprint aliases. The two master-begin columns locate actual source markers; absent English alignment is left blank.',
      '',
      'A row marked pending is an explicit absence of an independent verdict. No prior checker confidence, successful hash check, OCR extraction, diff, or LaTeX build is counted as a new scan review.',
      '', '## Contents and construction','',
      '- `scripts/`: source integrity, exact patching, annotated French generation, record merging, compilation and checkpoint scripts.',
      '- `readers/fr/`: three unfinished French forms and their common annotated master; PDFs are included only after successful compilation.',
      '- `review/english/`: flattened native source, provenance map, page-aligned retranslation chunks, exact translation edits, individually sourced variants, candidate glossary material, four unfinished English TeX files and available PDFs.',
      '- `review/front/`, `review/early/`, `review/expose_i/`, `review/late/`, `review/xiii/`, `review/middle/`, and any subsequent exposé directories: explicit image-read decisions and exact-anchor patch files. Original supplied layers are not overwritten.',
      '- `records/`: exhaustive decision queues with actual statuses, input hashes, page checks, literal changes, annotation data and compile diagnostics.',
      '', 'The French generator applies reviewed patches to the two supplied layers, verifies every exact anchor count, and computes page-local TeX-atom differences. Math spans and macro arguments stay intact. Both alternatives are stored in each `SGAvar` call. The three French forms differ only in the `SGAform` switch. The intermediate representation reconstructs each patched input text exactly before documented typesetting transports.',
      '', 'The French apparatus currently prints exact LaTeX alternatives for auditability. Many inherited differences still require scan-decision links. This apparatus is a working apparatus, not the final readable adjudicated apparatus.',
      '', 'The English generator uses its own common annotated master. Reviewed English replacements are logged passage by passage. French spelling corrections that have no effect on the English produce no English variant. Unchecked inherited English remains explicitly unverified.',
      '', '## Front matter, boundaries and printed matter','',
      'The main scan has 720 PDF pages. Printed folio F is PDF page F+14. The witness has 711 DjVu pages; its folio F is physical page F+11, directly verified. Front-matter offsets differ: main PDF3 is witness1; main PDF11 is witness9; main PDF13 is witness10 because the blank main PDF12 is absent from the witness.',
      '', 'The source title/credits page, Preface, Introduction and contents have been compared. Front breaks include com-/plexe across VII/VIII and the beginning of IX at «d’un morphisme projectif d’espaces analytiques complexes». New transcription restores the cover, publisher title and colophon in French. The inside-cover publisher notice is partly hidden by an attached label and has no counterpart in the witness; its covered text remains unresolved and is visibly marked incomplete in the working transcription. Institutional stamps, barcodes, handwritten prices and attached labels are copy-specific marks and are not transcribed as the printed work. Publisher logos are non-textual decoration.',
      '', 'The publisher catalogue after folio700 (main PDF715–720) remains to be inspected/transcribed. The English transfer of the newly restored publisher matter also remains pending. No claim of complete printed-matter coverage is made.',
      '', '## Notation and typesetting','',
      'The reviews use occurrence-specific glyph readings. Raised dots, lower dots, primes, asterisks, underlines, plain/script/double-struck letters and author footnote marks are retained where observed. No global replacement of a mathematical letter is inferred from its role. The exact notation convention decisions requested for the rest of the volume remain open.',
      '', 'Technical transports in the French generator: a TikZ-CD diagram scanned as a macro argument uses `ampersand replacement=\\&`, with each original column delimiter mapped to `\\&` and its count checked; heading underline boxes are preserved inside a maximum-width box to prevent clipping; footnote hyperlink generation is disabled to avoid inherited missing PDF destinations. These operations retain the displayed source text; they do not decide a reading.',
      '', '## Compilation','',
      '| French file | Exit | PDF pages | Errors | Warnings |','|---|---:|---:|---:|---:|'])
    for d in compile_rows:
        text.append(f"| {Path(d['file']).name} | {d['exit_code']} | {d.get('pdf_pages','—')} | {len(d.get('errors',[]))} | {d.get('warning_count',0)} |")
    text.extend(['','Full path-free French diagnostics are the corresponding `records/COMPILE_*.json` files. English compile results:','',
      '```json',json.dumps(enbuild,ensure_ascii=False,indent=2),'```','',
      'Compilation and selected visual layout checks do not establish the correctness of unchecked source pages.',
      '', '## Restore and reproduce','',
      '1. Extract the four original archives into one working directory, preserving their internal paths; retain each root manifest under a distinct archive-derived name.',
      '2. Extract this checkpoint over that directory. It contains no original archives and no nested checkpoints.',
      '3. Run `python scripts/intake.py --archives <the four archive files>` from the working directory. This revalidates every manifest hash and recreates review packets.',
      '4. Retain the saved review JSONL files as the authoritative inputs to the build. The accompanying observation scripts document the recorded image readings; they do not perform new automatic verdicts. They were applied cumulatively during review and need not be rerun to rebuild the books.',
      '5. Run `python scripts/build_french.py`, `python scripts/merge_records.py`, and the English audit/generation scripts. Compile with a complete standard TeX Live installation. The optional isolated-tree wrapper falls back to the installed TeX environment when its local package tree is absent.',
      '6. Continue the pending scan collation, exact English alignment/translation review, rejected-Codex decisions, conventions and glossary. The final release gate must require zero pending page/finding decisions, complete English transfer, sourced apparatus entries and error-free compiled readers.',
      '', '## Material omitted from this checkpoint','',
      'The four supplied source ZIPs and their extracted source trees are reproducible inputs and remain in the original attachments. Downloaded TeX/DjVu runtime packages, raw engine transcripts with runtime paths, caches, generated image strips and prior checkpoint ZIPs are omitted. Image evidence is specified by original archive-relative scan, page and region; review scripts reproduce crops. Previous checkpoint files are never replaced or nested.',
      '', 'No final release ZIPs have been designated complete.', ''])
    (ROOT/'README.md').write_text('\n'.join(text))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--number',type=int,required=True);args=parser.parse_args()
    make_docs()
    dest=ROOT.parent/f'SGA6_READERS_checkpoint_{args.number:02d}.zip'
    if dest.exists():raise SystemExit('Checkpoint already exists; choose the next number.')
    selected=[]
    for base in ['scripts','records','readers','review']:
        for p in (ROOT/base).rglob('*'):
            if not p.is_file():continue
            if any(part in ['__pycache__','images','build','rendered'] for part in p.relative_to(ROOT).parts):continue
            if p.name.startswith('TEMP_') or p.suffix in ['.log','.aux','.out','.toc','.png','.ppm','.jpg','.zip','.pyc']:continue
            if p.suffix not in ['.py','.json','.jsonl','.tsv','.csv','.tex','.md','.pdf','.txt']:continue
            selected.append(p)
    selected.append(ROOT/'README.md')
    files=[];private=[]
    forbidden=re.compile(r'(?:[A-Z]:\\(?:Users|work|home)\\|/(?:workspace/scratch|home/agent|root/\.codex)/[^\s]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})')
    for p in sorted(selected):
        b=p.read_bytes();rel=p.relative_to(ROOT).as_posix()
        if p.suffix!='.pdf':
            s=b.decode('utf-8')
            if forbidden.search(s):private.append(rel)
        files.append((rel,b))
    if private:raise SystemExit('Privacy scan requires review in: '+', '.join(private))
    manifest='path\tbytes\tsha256\n'+''.join(f'{name}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}\n' for name,data in files)
    with zipfile.ZipFile(dest,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in files:z.writestr(name,data)
        z.writestr('CHECKPOINT_MANIFEST.tsv',manifest)
    print(json.dumps({'checkpoint':dest.name,'bytes':dest.stat().st_size,'files':len(files)+1,'status':'incomplete checkpoint'},ensure_ascii=False))

if __name__=='__main__':main()
