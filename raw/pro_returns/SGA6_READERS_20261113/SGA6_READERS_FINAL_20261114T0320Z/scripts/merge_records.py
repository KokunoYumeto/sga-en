#!/usr/bin/env python3
"""Combine explicit reviews without promoting pending work to verified work."""
import collections
import csv
import difflib
import json
import re
from pathlib import Path
from intake import write_tsv, split_pages

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'records'

def jsonl(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()] if path.exists() else []

def jd(value):
    return json.dumps(value,ensure_ascii=False) if isinstance(value,(list,dict)) else value

def main():
    registry=json.loads((ROOT/'build/registry.json').read_text())
    byid={r['id']:r for r in registry}
    aliases={}
    for id in byid:
        aliases[id]=id
        aliases[id.replace(':entries#','#')]=id
    review=[];pages=[]
    for d in sorted((ROOT/'review').iterdir()):
        if not d.is_dir():continue
        for name in ['decisions.jsonl','own_findings.jsonl','convention_decisions.jsonl']:
            for r in jsonl(d/name):
                r['review_file']=(d/name).relative_to(ROOT).as_posix()
                review.append(r)
        for line,p in enumerate(jsonl(d/'page_status.jsonl'),1):
            p['_review_record']=(d/'page_status.jsonl').relative_to(ROOT).as_posix()+'#'+str(line)
            pages.append(p)
    decisions={};duplicates=[];review_groups=collections.defaultdict(list)
    for r in review:
        id=r.get('source_id',r.get('id',''))
        id=aliases.get(id,id)
        r['source_id']=id
        review_groups[id].append(r)
        if id in decisions and decisions[id]!=r:
            duplicates.append({'id':id,'earlier':decisions[id]['review_file'],'later':r['review_file']})
        decisions[id]=r
    resolved=[]
    for resolution in jsonl(ROOT/'review/merge_resolutions.jsonl'):
        id=resolution['source_id'];group=review_groups.get(id,[])
        actual=sorted({r['review_file'] for r in group})
        expected=sorted(resolution['review_files'])
        assert actual==expected,(id,actual,expected)
        selected=[r for r in group if r['review_file']==resolution['primary_review_file']]
        assert len(selected)==1,id
        row=selected[0].copy()
        row['verdict']=resolution.get('verdict',row['verdict'])
        row['reason']+=' '+resolution['resolution_reason']
        row['review_file']='; '.join(actual)
        row['image']='; '.join(dict.fromkeys(r.get('image','') for r in group if r.get('image')))
        decisions[id]=row
        resolved.append({'id':id,'primary_review_file':resolution['primary_review_file'],'verdict':row['verdict'],'resolution_reason':resolution['resolution_reason']})
    resolved_ids={r['id'] for r in resolved}
    unresolved=[d for d in duplicates if d['id'] not in resolved_ids]
    for duplicate in unresolved:
        decisions[duplicate['id']]['verdict']='pending_duplicate_resolution'
    from fr_source_links import apply_classification_supplements
    decisions=apply_classification_supplements(decisions)
    (REC/'REVIEW_IMPORT_DIAGNOSTICS.json').write_text(json.dumps({'duplicate_ids':duplicates,'resolved_duplicates':resolved,'unresolved_duplicate_ids':unresolved,'reviews_imported':len(review)},ensure_ascii=False,indent=2)+'\n')
    common_fields=['id','page','place','verdict','printed_reading','image','region','change','forms','reason','review_file','is_misprint','correction_status']
    types={'finding':[],'fixlog':[],'misprint':[],'replay':[],'manual':[],'hold_difference':[],'rejected_codex':[]}
    for entry in registry:
        id=entry['id'];d=decisions.get(id);data=entry['data']
        row={'id':id,'page':entry['page'],'place':data.get('where',data.get('expose',''))}
        if d:
            row.update({'page':d.get('page',row['page']),'place':d.get('where',row['place']),
              'verdict':d.get('verdict','pending_scan_review'),'printed_reading':d.get('printed_reading',''),
              'image':d.get('image',''),'region':d.get('region',''),'change':jd(d.get('change',d.get('correction',''))),
              'forms':jd(d.get('forms','')),'reason':d.get('reason',''),'review_file':d.get('review_file',''),
              'is_misprint':d.get('is_misprint',''),'correction_status':d.get('correction_status','')})
            if not row['image'] or not row['reason']:
                row['verdict']='pending_missing_evidence'
        else:
            row.update({'verdict':'pending_scan_review','printed_reading':'','image':'','region':'','change':'','forms':'','reason':'No independent image-read verdict has been entered in this checkpoint.','review_file':''})
        types[entry['type']].append(row)
    write_tsv(REC/'FINDINGS_DECIDED.tsv',types['finding']+types['fixlog'],common_fields)
    # Include explicit source-error dispositions, including decisions whose
    # original schema expressed the disposition in kind/type rather than the
    # later is_misprint Boolean. A font/reference tag or branch diff alone
    # supplies no source-error classification.
    additional_misprints=[]
    explicit_source_error_kinds={'misprint_in_print','misprint','misprint_correction',
      'mathematical_source_correction','substantive_mathematical_source_correction',
      'mathematical_source_error','substantive_mathematical_source_error',
      'bibliographic_source_correction','substantive_mathematical_misprint',
      'unresolved_mathematical_source_error'}
    classification=[]
    for id,d in decisions.items():
        if id in byid or d.get('is_misprint') is False or d.get('verdict','').startswith(('reverted','rejected')):continue
        kind=d.get('kind',d.get('type',d.get('record_type','')))
        basis='explicit is_misprint=true' if d.get('is_misprint') is True else ('explicit source-error disposition: '+kind if kind in explicit_source_error_kinds else '')
        if not basis:continue
        assert d.get('image') and d.get('reason'),id
        classification.append({'id':id,'page':d.get('page',''),'classification_basis':basis,'verdict':d.get('verdict',''),
          'correction_status':d.get('correction_status','See the explicit source decision; inclusion here does not alone assert a changed current reading.'),
          'review_file':d['review_file']})
        additional_misprints.append({'id':id,'page':d.get('page',''),'place':d.get('where',d.get('region',d.get('scope',''))),
          'verdict':d.get('verdict',''),'printed_reading':d.get('printed_reading',''),'image':d.get('image',''),
          'region':d.get('region',''),'change':jd(d.get('change',d.get('correction',''))),'forms':jd(d.get('forms','')),
          'reason':d.get('reason',''),'review_file':d.get('review_file',''),'is_misprint':True,
          'correction_status':d.get('correction_status','')})
    write_tsv(REC/'MISPRINTS_6_DECIDED.tsv',types['misprint']+additional_misprints,common_fields)
    (REC/'ADDITIONAL_MISPRINT_CLASSIFICATION.json').write_text(json.dumps({'method':'Explicit review-schema dispositions only; no classification inferred from typography or an observed branch difference. Historical alias counts and actual apparatus entry counts remain separate.','records':classification},ensure_ascii=False,indent=2)+'\n')
    # Keep the four previously resolved replay items separately; their earlier
    # resolved status never counts as a new independent verdict.
    replay_open={r['id'] for r in registry if r['type']=='replay' and not r['data'].get('resolved')}
    write_tsv(REC/'OPEN_ITEMS_DECIDED.tsv',[r for r in types['replay'] if r['id'] in replay_open]+types['manual'],common_fields)
    write_tsv(REC/'PRIOR_RESOLVED_REPLAY_REVIEW.tsv',[r for r in types['replay'] if r['id'] not in replay_open],common_fields)
    write_tsv(REC/'CODEX_DECIDED.tsv',types['rejected_codex']+types['hold_difference'],common_fields)
    own=[];conventions=[]
    for id,d in decisions.items():
        if id in byid:continue
        row={'id':id,'page':d.get('page',''),'place':d.get('where',d.get('region',d.get('scope',''))),'printed_reading':d.get('printed_reading',''),
          'tex_reading':d.get('tex',''),'change':jd(d.get('change',d.get('correction',''))),'kind':d.get('kind',d.get('type',d.get('record_type',''))),
          'verdict':d.get('verdict',''),'image':d.get('image',''),'region':d.get('region',''),'reason':d.get('reason',''),'review_file':d['review_file'],'evidence_refs':jd(d.get('evidence_refs','')),'evidence_mode':d.get('evidence_mode',''),
          'is_misprint':d.get('is_misprint',''),'correction_status':d.get('correction_status','')}
        if row['kind'] in ['convention','marker','boundary']:conventions.append(row)
        else:own.append(row)
    write_tsv(REC/'CHECK_FINDINGS.tsv',own,['id','page','place','printed_reading','tex_reading','change','kind','verdict','image','region','reason','review_file','is_misprint','correction_status'])
    write_tsv(REC/'DECISIONS.tsv',conventions,['id','page','place','printed_reading','change','kind','verdict','image','region','reason','review_file','evidence_refs','evidence_mode'])

    # One row for all720 primary scan leaves, including the rear catalogue.
    page_map={}
    for p in pages:
        pdf=p.get('pdf_page')
        if pdf is None and isinstance(p.get('page'),int):pdf=p['page']+14
        if pdf:
            previous=page_map.get(pdf,{})
            if p.get('supersedes') or not previous.get('supersedes'):
                page_map[pdf]=p
    front_labels=['cover','cover-verso','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
    page_rows=[]
    revised=ROOT/'build/FR_current_revised.tex'
    ftext=revised.read_text() if revised.exists() else ''
    master_paths={'FR_master_begin':('readers/fr/final/SGA6_FR_master_annote.tex' if (ROOT/'readers/fr/final/SGA6_FR_master_annote.tex').exists() else 'readers/fr/SGA6_FR_master_annote_DRAFT.tex'),
      'EN_master_begin':('review/english/final/SGA6_EN_annotated_master.tex' if (ROOT/'review/english/final/SGA6_EN_annotated_master.tex').exists() else 'review/english/DRAFT_SGA6_EN_annotated_master.tex')}
    starts={};inline_marker_locations=[]
    for column,rel in master_paths.items():
        path=ROOT/rel;body=path.read_text() if path.exists() else ''
        starts[column]={}
        for match in re.finditer(r'(?m)%+\s*scan idx\s+\d+\s*\|\s*folio\s+(\S+)\s*%+',body):
            line=body.count('\n',0,match.start())+1
            starts[column][match[1]]=rel+'#line='+str(line)
            line_start=body.rfind('\n',0,match.start())+1
            if match.start()!=line_start:
                inline_marker_locations.append({'master':rel,'folio':match[1],'line':line,'column':match.start()-line_start+1,
                  'basis':'The exact original marker is an inline TeX comment after preceding prose. Its actual line and column are recorded without moving or editing any source token.'})
    # Count each checker/hand-placed finding once, independently of its duplicate
    # FIXLOG and misprint-register rows; include the new independent findings.
    finding_counts=collections.Counter()
    for row in types['finding']+types['manual']+own:
        finding_counts[str(row['page'])]+=1
    page_schema_transports=[]
    for pdf in range(1,721):
        folio=front_labels[pdf-1] if pdf<=14 else pdf-14 if pdf<=714 else f'rear-{pdf}'
        p=page_map.get(pdf,{})
        checked=p.get('fully_checked',p.get('checked_against_scan',p.get('checked',False))) is True
        image=p.get('image',p.get('scan',''))
        if not image and p.get('main_scan_viewed') and p.get('pdf_page')==pdf:
            image='scan/SGA6_scan_360dpi.pdf#page='+str(pdf)
            page_schema_transports.append({'folio':folio,'pdf_page':pdf,'review_record':p['_review_record'],
              'recorded_main_scan_view':p['main_scan_viewed'],'exported_image':image,
              'basis':'The existing page review explicitly records the main scan view and its physical PDF page. Export its archive-relative image address; no new source-reading claim or verdict change.'})
        page_rows.append({'pdf_page':pdf,'folio':folio,'checked_against_scan':str(checked).lower(),'findings':finding_counts[str(folio)],
          'FR_master_begin':starts['FR_master_begin'].get(str(folio),''),
          'EN_master_begin':starts['EN_master_begin'].get(str(folio),''),'image':image,'review_record':p.get('_review_record',''),
          'region':p.get('region',p.get('regions',p.get('main_scan_viewed',''))),
          'status':p.get('status','fully compared' if checked else 'pending_scan_review'),
          'reason':p.get('reason',p.get('note',p.get('notes','No independent page comparison recorded.')))})
    write_tsv(REC/'PAGES_CHECKED.tsv',page_rows,['pdf_page','folio','checked_against_scan','findings','FR_master_begin','EN_master_begin','image','region','status','reason','review_record'])
    (REC/'PAGES_SCHEMA_TRANSPORT.json').write_text(json.dumps({'scope':'Export of explicitly recorded main-scan page addresses from the early page-status schema and exact inline marker locations. Original review records and final master bytes remain unchanged.','rows':page_schema_transports,'count':len(page_schema_transports),'inline_marker_locations':inline_marker_locations},ensure_ascii=False,indent=2)+'\n')

    # Exact diff hunks, preserving complete source text rather than a summary.
    if ftext:
        changes=[]
        for before_rel in ['fr/codex/ref_hold/main.tex','fr/sga6/current/main.tex']:
            before=(ROOT/before_rel).read_text().splitlines(keepends=True)
            after=ftext.splitlines(keepends=True)
            for tag,a,b,c,d in difflib.SequenceMatcher(None,before,after,autojunk=True).get_opcodes():
                if tag=='equal':continue
                prefix=''.join(after[:c]);marks=list(re.finditer(r'folio\s+([^%\n]+?)\s*%',prefix))
                label=marks[-1][1].strip() if marks else 'front'
                page=int(label) if label.isdigit() else label
                changes.append({'page':page,'place':f'after lines {c+1}–{d}','before':''.join(before[a:b]),'after':''.join(after[c:d]),
                  'source':before_rel,'provenance':'Exact source diff; see PATCH_APPLICATION_FR.json for reviewed edits.','status':'draft source comparison'})
        write_tsv(REC/'CHANGES_FR.tsv',changes,['page','place','before','after','source','provenance','status'])

    counts={}
    for kind,rs in types.items():
        counts[kind]={'total':len(rs),'decided':sum(not r['verdict'].startswith('pending') for r in rs),'pending':sum(r['verdict'].startswith('pending') for r in rs)}
    counts['pages']={'total':len(page_rows),'checked':sum(r['checked_against_scan']=='true' for r in page_rows),'unchecked':sum(r['checked_against_scan']!='true' for r in page_rows)}
    counts['own_findings']=len(own)
    counts['additional_explicit_misprint_decisions']=len(additional_misprints)
    counts['release_complete']=False
    (REC/'CHECKPOINT_STATUS.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(counts,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
