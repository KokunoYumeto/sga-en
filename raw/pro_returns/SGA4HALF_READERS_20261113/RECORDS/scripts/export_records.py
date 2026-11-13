"""Assemble the decision registers from the four independent page allocations."""
from pathlib import Path
import csv,collections,json,re,hashlib
from edition_catalog import *
from tex_audit import variants,marker_rows,resolve

OUT=ROOT/'work/records';OUT.mkdir(parents=True,exist_ok=True)

def tsv(name,rows,fields=None):
    if fields is None:fields=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore');w.writeheader()
        for row in rows:
            w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})

sol=all_rows('decisions');own=all_rows('own_findings');pages=all_rows('pages');meta=all_rows('variants')
assert len(sol)==1247 and len({x['id'] for x in sol})==1247
assert {x['id'] for x in sol}=={f'S45-SOL-{i:04d}' for i in range(1,1248)}
assert len(pages)==314 and {str(x['printed_page']) for x in pages}==set(PAGE_ORDER)
assert all(x['checked_against_scan'] and x.get('reason') and x.get('start_fr') and x.get('start_en') for x in pages)
assert len(own)==len({x['id'] for x in own})
assert all(x['verdict'] in ['accepted','accepted with a corrected reading','rejected'] and x['reason'] and x['region'] and x['printed_reading'] for x in sol)

with (ROOT/'source/check/SOL_FINDINGS.tsv').open(newline='') as f:original={r['id']:r for r in csv.DictReader(f,delimiter='\t')}
for r in sol:
    r['original_kind']=original[r['id']]['kind']
    r['part']=PAGE_COMPONENT[r['printed_page']]['name']
    if r['kind']=='marker':r['forms_affected']='All French and English forms: original-page markers.'
tsv('SOL_FINDINGS_DECIDED.tsv',sorted(sol,key=lambda r:r['id']),['id','printed_page','pdf_page','part','verdict','printed_reading','image','region','change_made','forms_affected','reason','original_kind','kind','corrected_reading','codex_ids'])
tsv('CHECK_FINDINGS.tsv',sorted(own,key=lambda r:r['id']),['id','page','place','printed_reading','tex_reading','change','kind','reason'])

component_text={};occurrences=[]
for c in COMPONENTS:
    for lang in ['fr','en']:
        p=component_path(c,lang);s=p.read_text();component_text[lang,c['key']]=s
        markers=marker_rows(s)
        assert [r['page'] for r in markers]==c['pages'],(lang,c['key'],'page markers')
        for n,v in enumerate(variants(s),1):
            matches=[x for x in meta if x['id'] in v['source'].split(';') or x.get('source') in v['source'].split(';')]
            exact=[x for x in matches if str(x['page'])==v['page']]
            candidates=exact or matches
            if not candidates:raise ValueError(('variant without decision',lang,c['key'],v))
            m=candidates[0]
            v.update(language=lang,part=c['name'],component=c['key'],component_occurrence=n,
                     place=m.get('place',''),kind=m.get('kind','misprint_in_print'),reason=m['reason'],metadata_page=str(m['page']))
            assert v['printed']!=v['corrected'],('empty difference',v)
            occurrences.append(v)

misprints=[]
for n,v in enumerate([x for x in occurrences if x['language']=='fr'],1):
    m=dict(id=f'S45-MP-{n:04d}',printed_page=v['page'],part=v['part'],place=v['place'],
           printed_reading=v['printed'],correction=v['corrected'],source=v['source'],kind=v['kind'],reason=v['reason'],
           fr_occurrence=f"{v['component']}:{v['component_occurrence']}")
    english=[x for x in occurrences if x['language']=='en' and x['source']==v['source'] and x['page']==v['page']]
    m['english_occurrences']=';'.join(f"{e['component']}:{e['component_occurrence']}" for e in english)
    m['forms']='FR diplomatic keeps print; FR corrected/apparatus and reading correct; EN follows the same distinction when listed.'
    misprints.append(m)
tsv('MISPRINTS_45.tsv',misprints)
(OUT/'VARIANT_OCCURRENCES.json').write_text(json.dumps(occurrences,ensure_ascii=False,indent=2))

def associated_pages(value):
    result=set()
    for item in str(value).split(','):
        item=item.strip()
        if item in PAGE_RANK:result.add(item);continue
        match=re.fullmatch(r'(\d+)\s*[–—-]\s*(\d+)',item)
        if match:result.update(str(n) for n in range(int(match[1]),int(match[2])+1))
    return result

own_page_sets={r['id']:associated_pages(r['page']) for r in own}
master_markers={};relocations={}
for lang in ['fr','en']:
    master=ROOT/'deliverables'/lang.upper()/('SGA4HALF_'+lang.upper()+'_annotated_master.tex')
    if master.exists():master_markers[lang]={r['page']:r for r in marker_rows(master.read_text())}
    report=ROOT/f'work/build/prepare_report_{lang}.json'
    relocations[lang]={r['page']:r for r in json.loads(report.read_text()).get('marker_relocations',[])} if report.exists() else {}

page_rows=[];decisions=[]
for p in sorted(pages,key=lambda r:PAGE_RANK[str(r['printed_page'])]):
    key=str(p['printed_page']);c=PAGE_COMPONENT[key]
    row=dict(printed_page=key,pdf_page=p['pdf_page'],checked_against_scan=True,
             sol_findings=sum(x['printed_page']==key for x in sol),own_findings=sum(key in x for x in own_page_sets.values()),
             number_of_findings=sum(x['printed_page']==key for x in sol)+sum(key in x for x in own_page_sets.values()),
             part=c['name'],image='scan/Number32.pdf',reason=p['reason'])
    for lang in ['fr','en']:
        s=component_text[lang,c['key']];marker=next(x for x in marker_rows(s) if x['page']==key)
        row['master_'+lang]='SGA4HALF_'+lang.upper()+'_annotated_master.tex'
        row['component_'+lang]=c[lang];row['component_line_'+lang]=marker['line'];row['start_'+lang]=marker['start']
        final=master_markers.get(lang,{}).get(key)
        row['master_line_'+lang]=final['line'] if final else ''
        row['master_marker_context_'+lang]=final['start'] if final else ''
        row['scan_boundary_anchor_'+lang]=p['start_'+lang]
        row['marker_placement_'+lang]=relocations[lang].get(key,{}).get('action','At the reviewed text boundary; margin marker uses the common presentation macro.')
    page_rows.append(row)
    decisions.append(dict(id='PAGE-'+key,page=key,kind='page boundary',decision='Exact original-page break retained in both languages',
                          evidence=p['reason'],fr_anchor=row['start_fr'],en_anchor=row['start_en'],source='Direct scan review; PAGES_CHECKED.tsv'))
tsv('PAGES_CHECKED.tsv',page_rows)
for d in sol:
    if d['kind']=='marker':decisions.append(dict(id=d['id'],page=d['printed_page'],kind='Sol page-cut report',decision=d['change_made'],evidence=d['reason'],source=d['id']))
    elif d['id'] in {'S45-SOL-0199','S45-SOL-0201','S45-SOL-0204','S45-SOL-0205'}:
        decisions.append(dict(id=d['id'],page=d['printed_page'],kind='Rejected presentation-only label renaming',decision=d['change_made'],evidence=d['reason'],source=d['id']))
for r in own:
    if any(k in (r['kind']+' '+r['reason']).lower() for k in ['notation','convention','derived','sheaf hom','ordinary hom','editorial correction rejected']):
        decisions.append(dict(id=r['id'],page=r['page'],kind='Notation/convention or rejected normalization',decision=r['change'],evidence=r['reason'],source=r['id']))
decisions += [
dict(id='POLICY-NOTE45',page='all',kind='Source convention',decision='Retain Miller layout, display/diagram form, label names, equivalent macros, script sheaf letters and Hom/hom convention unless the print makes a distinction they erase.',evidence='check/NOTE_45.txt and the explicit task instructions.',source='NOTE_45.txt'),
dict(id='POLICY-MBOX-7',page='256',kind='Codex diplomatic mbox',decision='Retain the mbox around cas in all French forms; it introduces no English content difference.',evidence='The sole mbox in the supplied diplomatic component7 surrounds cas in the complex-base sentence. The box is a line-breaking choice, not a print misprint and receives no apparatus.',source='fr/codex_dip/sga4.5-7.tex; fr/codex_corr/sga4.5-7.tex; NOTE_45.txt'),
dict(id='POLICY-CODEX-RANGE',page='66–312',kind='Source provenance discrepancy',decision='Compare the supplied Codex trees beyond65 as actual sources; do not assume equality with Miller.',evidence='The attached trees contain many later content repairs despite the prompt’s equality statement. Full component diffs and the decision-to-source checks use their actual contents.',source='fr/miller_src; fr/codex_dip; fr/codex_corr'),
dict(id='POLICY-CODEX-0011',page='28,32',kind='Duplicate historical identifier',decision='Keep the first SGA45-CORR-0011 identifier for the rejected Soient correction; denote the second historical row by SGA45-CORR-0011B for the norm subscript correction.',evidence='The attached dec.csv repeats SGA45-CORR-0011. The alias prevents two different decisions from sharing one apparatus source.',source='fr/codex_records/dec.csv'),
dict(id='GENERAL-CONTENTS',page='unnumbered',kind='Original matter restoration',decision='Retain the original general contents from PDFpage5 without inventing an original printed page number.',evidence='The page was visually inspected in addition to the314 numbered text pages.',source='S45-ASTRA-A-0032'),
]
tsv('DECISIONS.tsv',decisions,['id','page','kind','decision','evidence','fr_anchor','en_anchor','source'])

counts=collections.Counter((v['part'],v['language'],v['kind']) for v in occurrences)
lines=['# Apparatus counts','','Counts are per actual variant occurrence, not per distinct source identifier. Each occurrence has one entry in the corrected reader and annotated-master PDF; the diplomatic and reading PDFs have no apparatus entries. Transcription repairs are excluded.','','| Part | Language | Recorded kind | Diplomatic | Corrected with apparatus | Reading | Annotated master |','|---|---|---|---:|---:|---:|---:|']
for c in COMPONENTS:
    for (part,lang,kind),n in sorted(counts.items()):
        if part==c['name']:lines.append(f'| {part} | {lang.upper()} | {kind} | 0 | {n} | 0 | {n} |')
for lang in ['fr','en']:
    n=sum(x['language']==lang for x in occurrences);lines.append(f'| **Total** | **{lang.upper()}** | **All kinds** | **0** | **{n}** | **0** | **{n}** |')
(OUT/'APPARATUS_COUNTS.md').write_text('\n'.join(lines)+'\n')
summary=dict(pages=len(pages),sol_findings=len(sol),sol_verdicts=dict(collections.Counter(x['verdict'] for x in sol)),own_findings=len(own),
             fr_variant_occurrences=sum(x['language']=='fr' for x in occurrences),en_variant_occurrences=sum(x['language']=='en' for x in occurrences),
             misprint_rows=len(misprints),sol_original_kinds=dict(collections.Counter(x['original_kind'] for x in sol)),
             marker_checks_per_language=314,empty_variant_differences=0,variants_without_source=0,
             all_pages_visually_checked=True,all_sol_rows_have_reasons=True)
(OUT/'RECORDS_VALIDATION.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False))
