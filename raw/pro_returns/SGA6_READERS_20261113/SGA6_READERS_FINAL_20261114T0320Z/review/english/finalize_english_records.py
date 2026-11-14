#!/usr/bin/env python3
"""Write exhaustive final-reader differences and the attributed transfer ledger."""
from pathlib import Path
from collections import Counter
from bisect import bisect_right
from difflib import SequenceMatcher
import csv,hashlib,json,re

EN=Path(__file__).resolve().parent
ROOT=EN.parents[1]
OUT=EN/'final'
AGG=EN/'aggregate'


def sha(text):return hashlib.sha256(text.encode()).hexdigest()
def rows(path):return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def check_privacy(text):
    assert not re.search(r'(?:/(?:workspace|Users|home|usr|opt|tmp|root|mnt)/|[A-Z]:\\(?:Users|Documents|Temp|Windows|Program Files)\\)',text)
    assert not re.search(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}',text,re.I)


def main():
    catalog=json.loads((AGG/'INPUT_CATALOG.json').read_text())
    baseline=ROOT/'en/release_v2026-11-12/07_SGA6_EN_CURRENT_LAYERED_READER.tex'
    final=OUT/'SGA6_EN_corrected_apparatus.tex'
    before=baseline.read_bytes().decode('utf-8');after=final.read_bytes().decode('utf-8')
    check_privacy(before);check_privacy(after)
    old_lines=before.splitlines(keepends=True);new_lines=after.splitlines(keepends=True)
    # The released file uses CRLF. Align complete lines after the explicit
    # reversible newline projection, but retain the original bytes in every
    # raw hunk, including equal-content blocks whose line endings change.
    old_projected=[line[:-2]+'\n' if line.endswith('\r\n') else line for line in old_lines]
    endings=['CRLF' if line.endswith('\r\n') else 'LF' if line.endswith('\n') else 'none' for line in old_lines]
    ending_runs=[]
    for i,kind in enumerate(endings):
        if ending_runs and ending_runs[-1]['kind']==kind:ending_runs[-1]['end_line']=i+1
        else:ending_runs.append(dict(start_line=i+1,end_line=i+1,kind=kind))
    restored_projection=''.join(line[:-1]+'\r\n' if kind=='CRLF' else line for line,kind in zip(old_projected,endings))
    assert restored_projection==before
    aligned=SequenceMatcher(None,old_projected,new_lines,autojunk=False).get_opcodes()
    opcodes=[]
    for tag,a,b,c,d in aligned:
        if tag=='equal':
            for delta in range(0,b-a,200):
                n=min(200,b-a-delta)
                if old_lines[a+delta:a+delta+n]!=new_lines[c+delta:c+delta+n]:
                    opcodes.append(('line_endings',a+delta,a+delta+n,c+delta,c+delta+n))
        else:opcodes.append((tag,a,b,c,d))
    hunks=[]
    marker_lines=[];marker_pages=[]
    for n,line in enumerate(new_lines):
        match=re.search(r'%{10}\s+scan idx\s+\d+\s*\|\s*folio\s+(\S+)\s+%{10}',line)
        if match:marker_lines.append(n);marker_pages.append(match[1])
    apparatus_line=next(n for n,line in enumerate(new_lines) if line.strip()==r'\section*{Apparatus}')
    for tag,a,b,c,d in opcodes:
        k=bisect_right(marker_lines,c)-1
        page=marker_pages[k] if k>=0 else 'new edition matter / preamble'
        if c>=apparatus_line:page='new apparatus'
        involved=[marker_pages[i] for i,line in enumerate(marker_lines) if c<=line<d]
        if involved:page=', '.join(dict.fromkeys(([page] if k>=0 else [])+involved))
        hunks.append(dict(change_id=f'EN-RAW-{len(hunks)+1:05d}',scope='exact_final_reader_TeX',
            difference_class='line_ending_transport' if tag=='line_endings' else 'literal_source_change',
            page=page,place=f'Final corrected-reader lines {c+1}–{d}; released-reader lines {a+1}–{b}',
            before=''.join(old_lines[a:b]),after=''.join(new_lines[c:d]),
            source='Exact released English compared with final SGA6_EN_corrected_apparatus.tex; complete source-linked passage and correction records are in TRANSFER_LEDGER.jsonl and VARIANTS.jsonl.',
            before_start_line=a+1,before_end_line=b,after_start_line=c+1,after_end_line=d,
            old_start0=a,old_end0=b,new_start0=c,new_end0=d))
    reconstructed=list(old_lines)
    for row in reversed(hunks):
        assert ''.join(reconstructed[row['old_start0']:row['old_end0']])==row['before']
        reconstructed[row['old_start0']:row['old_end0']]=row['after'].splitlines(keepends=True)
    assert ''.join(reconstructed)==after
    reverse=list(new_lines)
    for row in reversed(hunks):
        assert ''.join(reverse[row['new_start0']:row['new_end0']])==row['after']
        reverse[row['new_start0']:row['new_end0']]=row['before'].splitlines(keepends=True)
    assert ''.join(reverse)==before

    superseded=set(catalog['superseded_front_patch_ids'])
    spans=[dict(r,packet='review/english/EN_TRANSLATION_PATCHES.jsonl') for r in rows(EN/'EN_TRANSLATION_PATCHES.jsonl')
           if r['status'].startswith('accepted') and r['id'] not in superseded]
    for packet in catalog['packets']:
        spans.extend(dict(r,packet=packet['directory']+'/translation_spans.jsonl')
                     for r in rows(ROOT/packet['directory']/'translation_spans.jsonl'))
    assert len(spans)==len(catalog['applications'])==142
    described=[]
    for span in spans:
        page=span.get('page')
        if page is None:page=f"{span['first_folio']}–{span['last_folio']}"
        described.append(dict(change_id=span['id'],scope='reviewed_translation_span_from_native_source',
            page=page,place=span.get('place','Complete source-aligned passage; '+span['id']),
            before=span['old'],after=span['new'],source=span['packet']+'; '+span.get('source','')+'; '+span.get('reason','')))
    for record in rows(EN/'EN_AGGREGATE_TEXT_AMENDMENTS.jsonl'):
        described.append(dict(change_id=record['id'],scope='English_translation_correction',
            page=record.get('page','53'),place=record.get('place',record['id']),
            before=record['old'],after=record['new'],source=record['source']+'; '+record.get('reason','')))
    fields=['change_id','scope','difference_class','page','place','before','after','source','before_start_line','before_end_line','after_start_line','after_end_line']
    with (OUT/'CHANGES_EN.tsv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore')
        writer.writeheader();writer.writerows(hunks+described)
    save(OUT/'CHANGES_EN_RAW_HUNKS.json',hunks)
    save(OUT/'CHANGES_EN_LINE_ENDING_PROJECTION.json',dict(
        original_sha256=sha(before),LF_projection_sha256=sha(''.join(old_projected)),
        line_ending_runs=ending_runs,exact_inverse_pass=True,
        definition='For alignment only, replace each recorded CRLF line ending by LF. Reattach CR before LF at precisely the recorded original line numbers to recover the original released bytes. Raw hunk before/after fields retain actual original and final line endings, so no literal difference is omitted.'))
    save(OUT/'CHANGES_EN_RECONSTRUCTION.json',dict(
        baseline=baseline.relative_to(ROOT).as_posix(),baseline_sha256=sha(before),
        final_reader=final.relative_to(ROOT).as_posix(),final_reader_sha256=sha(after),
        baseline_lines=len(old_lines),final_lines=len(new_lines),raw_hunks=len(hunks),
        line_ending_only_hunks=sum(r['difference_class']=='line_ending_transport' for r in hunks),
        literal_source_change_hunks=sum(r['difference_class']=='literal_source_change' for r in hunks),
        changed_released_lines=sum(r['old_end0']-r['old_start0'] for r in hunks),
        changed_final_lines=sum(r['new_end0']-r['new_start0'] for r in hunks),
        forward_exact_reconstruction=True,reverse_exact_reconstruction=True,
        additional_reviewed_translation_span_rows=len(spans),additional_English_only_correction_rows=len(described)-len(spans),
        scope='The raw-hunk rows include every literal difference, including all generated preamble, form-switch, edition-credit, source-folio, typography, apparatus and editorial material. They perform no author-text projection. Separately labelled reviewed-translation rows compare the exact native source spans and are not falsely presented as an independent released-source baseline.',
        privacy_check='No email address or local absolute path in either exact TeX input.'))

    transfers=[];input_files=[]
    def collect(path,kind):
        relative=path.relative_to(ROOT).as_posix();digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if path.suffix=='.tsv':
            with path.open(newline='') as f:local=list(csv.DictReader(f,delimiter='\t'))
        else:local=rows(path)
        for n,r in enumerate(local,1):
            transfers.append(dict(aggregate_transfer_id=f'EN-TRANSFER-{len(transfers)+1:05d}',
                scope=kind,input=relative,input_sha256=digest,input_row=n,record=r))
        input_files.append(dict(path=relative,sha256=digest,rows=len(local),scope=kind))
    collect(EN/'EN_EARLY_CURRENT_TRANSFER_001_077.tsv','source_correction_transfer_1_77')
    for path in sorted(EN.glob('EN_EXPOSE_*_TRANSFER_*.jsonl')):
        collect(path,'source_correction_and_typography_transfer_78_296')
    for packet in catalog['packets']:
        collect(ROOT/packet['directory']/'transfer.jsonl','sealed_contribution_transfer')
    for name in ['EN_AGGREGATE_VARIANTS.jsonl','EN_AGGREGATE_TEXT_AMENDMENTS.jsonl','EN_AGGREGATE_MACRO_TRANSPORTS.jsonl','EN_AGGREGATE_BUILD_REPAIRS.jsonl','EN_AGGREGATE_RENDERING_REPAIRS.jsonl']:
        collect(EN/name,'final_aggregate_adjudication_or_transport')
    ledger=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in transfers)
    check_privacy(ledger)
    (OUT/'TRANSFER_LEDGER.jsonl').write_text(ledger)
    (OUT/'VARIANTS.jsonl').write_bytes((AGG/'VARIANTS.jsonl').read_bytes())
    save(OUT/'TRANSFER_LEDGER_STATUS.json',dict(rows=len(transfers),input_files=input_files,
        definition='One attributed row for every row of each named original correction-transfer ledger, plus every final aggregate correction/transport row. Row types and historical frozen source hashes are retained exactly; final source wrapper and macro checks are separate linked audits.',
        final_French_source_states='review/english/aggregate/FRENCH_SOURCE_STATES.json',
        final_literal_math_check='review/english/aggregate/LITERAL_MATH_VERIFICATION.json',
        final_typography_check='review/english/aggregate/TYPOGRAPHY_TRANSPORT.json'))
    print(json.dumps(dict(raw_change_hunks=len(hunks),translation_spans=len(spans),
        English_only_corrections=len(described)-len(spans),transfer_rows=len(transfers),
        forward_and_reverse_reconstruction=True)))


if __name__=='__main__':main()
