"""Extend the exact source change logs through the complete corrected readers.

Every stage uses literal UTF-8 byte ranges.  The aggregate tables retain the
five requested columns and include extraction, representation and assembly.
Original CRLF bytes inside TSV cells are read and written with newline=''.
"""
from __future__ import annotations
import argparse, collections, csv, difflib, json, re, sys
from pathlib import Path

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path('work/contributions/changes')))
import build_changes_fr as shared
from sga5_common import FOLIO, write_json

NAMES={'FR':'SGA5_FR_corrige_apparat.tex','EN':'SGA5_EN_corrected_apparatus.tex'}

def read_rows(path):
    with Path(path).open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))

def replay(data,rows):
    return shared.replay_tsv(data,rows)

def comparison(before,after,lang,stage,source_path,target_path,variants):
    old=before.decode('utf-8').splitlines(keepends=True)
    new=after.decode('utf-8').splitlines(keepends=True)
    oo=shared.line_byte_offsets(old);nn=shared.line_byte_offsets(new)
    pages=shared.folios_per_line(new)
    rows=[];decisions=[]
    for op,i,j,k,l in shared.complete_line_opcodes(old,new):
        if op=='equal':continue
        a=''.join(old[i:j]);b=''.join(new[k:l])
        ident=f'READERS-{lang}-{stage.upper()}-{len(rows)+1:04d}'
        ids=list(dict.fromkeys(re.findall(r'\}\{((?:FR|EN)-\d{4}|R98-\d{2})\}',b)))
        ids=[x for x in ids if x in variants]
        scope=sorted(set(pages[k:l] or (pages[min(k,len(pages)-1):min(k,len(pages)-1)+1] if pages else [0])))
        page=shared.compact_pages(scope)
        if stage=='extract':
            category='exact body slice; editorial preamble/front-matter and delimiter extraction'
            reason='Extract the exact recorded body substring without trimming. The removed preamble and editorial front matter are retained in these complete cells; the later assembly stage supplies the new credited front matter.'
        else:
            category='annotated variants; folio display; generated contents; front matter; apparatus; document assembly'
            reason='Record the exact assembly from the prepared corrected body to the complete corrected reader. Balanced variant calls retain both documented readings and select the corrected argument; wrapper code supplies title, credits, rights, generated contents, margin folios and apparatus. The independent master projection audit proves the body relationship.'
        sources=[f'READER_ASSEMBLY_DECISIONS.tsv:{ident}',source_path,target_path,'work/build/scripts/wrap_readers.py']
        sources += [f'work/build/prepared/{lang}_variants_ordered.json:{vid}' for vid in ids]
        if stage=='extract':sources.append(f'work/contributions/{"changes" if lang=="FR" else "changes_en"}/{lang}_REPRESENTATION_RULES.json')
        if lang=='EN' and stage=='assemble' and ('Editorial note.' in a or 'EN-INHERITED-0046-P43' in b):
            sources.append('work/build/prepared/EN_wrapper_editorial_extractions.json:EN-INHERITED-0046-P43')
            reason+=' The inherited p.43 editorial footnote is moved verbatim to the corrected-only unresolved appendix under its exact extraction/reinsertion ledger.'
        rows.append({'page':page,'place':f'{stage}:{lang} | id={ident} | old_bytes={oo[i]}:{oo[j]} | new_bytes={nn[k]}:{nn[l]} | old_lines_0based={i}:{j} | new_lines_0based={k}:{l} | category={category}',
                     'before':a,'after':b,'source':'; '.join(sources)})
        decisions.append({'id':ident,'language':lang,'stage':stage,'page':page,'operation':op,'source':source_path,'target':target_path,'reason':reason,'variant_ids':'; '.join(ids)})
    assert replay(before,rows)==after
    return rows,decisions,{'comparison':stage+':'+lang,'source':source_path,'target':target_path,'source_sha256':shared.sha(before),'target_sha256':shared.sha(after),'rows':len(rows),'exact_replay':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='work/contributions/reader_changes');a=ap.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    report={'coordinate_system':'Zero-based half-open UTF-8 byte ranges at each named stage. Before/after cells are complete. Apply all rows for a stage against its unchanged source, from greatest offset to least.','languages':{},'all_final_reader_reconstructions_exact':True}
    all_decisions=[]
    for lang in ['FR','EN']:
        source_dir=Path('work/contributions')/('changes' if lang=='FR' else 'changes_en')
        original_rows=read_rows(source_dir/f'CHANGES_{lang}.tsv')
        rep_rows=read_rows(source_dir/f'CHANGES_{lang}_REPRESENTATION.tsv')
        vars={v['id']:v for v in json.loads(Path(f'work/build/prepared/{lang}_variants_ordered.json').read_text())}
        prepared_path=Path(f'work/build/prepared/{lang}_corrected_body.tex')
        prepared=prepared_path.read_bytes()
        reader_path=Path('deliverables')/lang/NAMES[lang]
        reader=reader_path.read_bytes()
        if lang=='FR':
            source_path=Path('work/build/prepared/FR_current_source.tex')
            source=source_path.read_bytes()
            start=source.index(br'\begin{document}')+len(br'\begin{document}')
            end=source.rindex(br'\end{document}')
            beginnings={
                'baseline:o':Path('work/sources/SGA5_FR/fr_baseline_aug2026/sga5/o/s5.tex'),
                'baseline:c5':Path('work/sources/SGA5_FR/fr_baseline_aug2026/sga5/c5/s5.tex'),
                'baseline:c4':Path('work/sources/SGA5_FR/fr_baseline_aug2026/sga5/c4/s5.tex'),
                'current':Path('work/sources/SGA5_FR/fr/sga5/current/s5.tex')}
        else:
            source_path=Path('work/contributions/english/EN_corrected_flat.tex')
            source=source_path.read_bytes()
            text=source.decode('utf-8')
            align=json.loads(Path('work/contributions/english/EN_ALIGNMENT.json').read_text())
            pos=min(row['position_corrected'] for row in align)
            start=len(text[:pos].encode('utf-8'));end=source.rindex(br'\end{document}')
            beginnings={'release':Path('work/sources/SGA5_EN/en/release_source/sources/native/SGA5/SGA5_English_sync_workpass.tex')}
        raw=source[start:end]
        assert replay(raw,rep_rows)==prepared
        extraction,ed,ep=comparison(source,raw,lang,'extract',str(source_path),f'{lang}:exact-raw-body-slice',vars)
        assembly,ad,apf=comparison(prepared,reader,lang,'assemble',str(prepared_path),str(reader_path),vars)
        all_decisions+=ed+ad
        combined=original_rows+extraction+rep_rows+assembly
        shared.write_tsv(out/f'CHANGES_{lang}.tsv',combined,shared.FIELDS)
        shared.write_tsv(out/f'CHANGES_{lang}_READER_ASSEMBLY.tsv',extraction+assembly,shared.FIELDS)
        written=read_rows(out/f'CHANGES_{lang}.tsv')
        assert written==combined
        groups=collections.defaultdict(list)
        for row in written:groups[row['place'].split(' | ',1)[0]].append(row)
        proofs=[]
        for label,p in beginnings.items():
            data=p.read_bytes()
            stage1=replay(data,groups[label]);assert stage1==source
            stage2=replay(stage1,groups['extract:'+lang]);assert stage2==raw
            rep_label=rep_rows[0]['place'].split(' | ',1)[0]
            stage3=replay(stage2,groups[rep_label]);assert stage3==prepared
            stage4=replay(stage3,groups['assemble:'+lang]);assert stage4==reader
            proofs.append({'start':label,'source':str(p).replace('work/sources/',''),'source_sha256':shared.sha(data),'stage_order':[label,'extract:'+lang,rep_label,'assemble:'+lang],'final_reader':str(reader_path),'final_reader_sha256':shared.sha(stage4),'byte_exact':True})
        report['languages'][lang]={'source_change_rows':len(original_rows),'extraction_rows':len(extraction),'representation_rows':len(rep_rows),'assembly_rows':len(assembly),'complete_change_rows':len(combined),'raw_body_source_byte_range':[start,end],'raw_body_sha256':shared.sha(raw),'extraction':ep,'assembly':apf,'complete_chains':proofs}
    shared.write_tsv(out/'READER_ASSEMBLY_DECISIONS.tsv',all_decisions,list(all_decisions[0]))
    write_json(out/'COMPLETE_READER_CHANGELOG_RECONSTRUCTION.json',report)
    lines=['# Complete changes through the corrected readers','',
           'The root CHANGES_FR.tsv and CHANGES_EN.tsv include the full source comparisons, the exact body-extraction steps, all body-representation changes, and the complete assembly into the delivered corrected reader source. The five required columns are preserved. No before/after cell is abbreviated.','',
           'The stage label at the beginning of `place` identifies the source against which its byte ranges apply. These are consecutive maps, not one flat set of offsets. Start from the named original, apply its source-comparison group, then `extract`, `representation`, and `assemble` in the recorded order. Each stage and every complete chain was replayed from the written TSV with exact SHA-256 agreement.','',
           '| Language | Source changes | Body extraction | Representation | Reader assembly | Total rows |',
           '|---|---:|---:|---:|---:|---:|']
    for lang,v in report['languages'].items():lines.append(f"| {lang} | {v['source_change_rows']:,} | {v['extraction_rows']:,} | {v['representation_rows']:,} | {v['assembly_rows']:,} | {v['complete_change_rows']:,} |")
    lines += ['', 'The French table has four alternative starting branches: August `o`, `c5`, `c4`, and final supplied `current`. They share the later extraction, representation and assembly stages. The English table begins with the released source. Assembly includes the new front matter, exact rights and credits, generated contents, margin folios, variant macros, apparatus and document support code. These source-code assembly differences are not counted as new mathematical corrections.','',
              'Read these tables with a TSV parser that preserves embedded newlines, for example Python `csv.DictReader(..., delimiter="\\t")` on a file opened with `newline=""`. The original CRLF bytes inside quoted cells remain significant.','',
              '`COMPLETE_READER_CHANGELOG_RECONSTRUCTION.json` gives every chain, stage hash and final reader hash. `READER_ASSEMBLY_DECISIONS.tsv` gives each added extraction/assembly row an explicit decision and reason. The original stage reports and patches remain under the contributions directories.','']
    (out/'COMPLETE_READER_CHANGELOG_REPORT.md').write_text('\n'.join(lines))
    print(json.dumps({k:{x:v[x] for x in ['source_change_rows','extraction_rows','representation_rows','assembly_rows','complete_change_rows']} for k,v in report['languages'].items()}))

if __name__=='__main__':main()
