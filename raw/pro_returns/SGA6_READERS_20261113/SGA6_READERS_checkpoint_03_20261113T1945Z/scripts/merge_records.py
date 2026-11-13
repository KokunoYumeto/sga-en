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
        for name in ['decisions.jsonl','own_findings.jsonl']:
            for r in jsonl(d/name):
                r['review_file']=(d/name).relative_to(ROOT).as_posix()
                review.append(r)
        pages.extend(jsonl(d/'page_status.jsonl'))
    decisions={};duplicates=[]
    for r in review:
        id=r.get('source_id',r.get('id',''))
        id=aliases.get(id,id)
        r['source_id']=id
        if id in decisions and decisions[id]!=r:
            duplicates.append({'id':id,'earlier':decisions[id]['review_file'],'later':r['review_file']})
        decisions[id]=r
    (REC/'REVIEW_IMPORT_DIAGNOSTICS.json').write_text(json.dumps({'duplicate_ids':duplicates,'reviews_imported':len(review)},ensure_ascii=False,indent=2)+'\n')
    common_fields=['id','page','place','verdict','printed_reading','image','region','change','forms','reason','review_file']
    types={'finding':[],'fixlog':[],'misprint':[],'replay':[],'manual':[],'hold_difference':[],'rejected_codex':[]}
    for entry in registry:
        id=entry['id'];d=decisions.get(id);data=entry['data']
        row={'id':id,'page':entry['page'],'place':data.get('where',data.get('expose',''))}
        if d:
            row.update({'page':d.get('page',row['page']),'place':d.get('where',row['place']),
              'verdict':d.get('verdict','pending_scan_review'),'printed_reading':d.get('printed_reading',''),
              'image':d.get('image',''),'region':d.get('region',''),'change':jd(d.get('change',d.get('correction',''))),
              'forms':jd(d.get('forms','')),'reason':d.get('reason',''),'review_file':d.get('review_file','')})
            if not row['image'] or not row['reason']:
                row['verdict']='pending_missing_evidence'
        else:
            row.update({'verdict':'pending_scan_review','printed_reading':'','image':'','region':'','change':'','forms':'','reason':'No independent image-read verdict has been entered in this checkpoint.','review_file':''})
        types[entry['type']].append(row)
    write_tsv(REC/'FINDINGS_DECIDED.tsv',types['finding']+types['fixlog'],common_fields)
    write_tsv(REC/'MISPRINTS_6_DECIDED.tsv',types['misprint'],common_fields)
    # Keep the four previously resolved replay items separately; their earlier
    # resolved status never counts as a new independent verdict.
    replay_open={r['id'] for r in registry if r['type']=='replay' and not r['data'].get('resolved')}
    write_tsv(REC/'OPEN_ITEMS_DECIDED.tsv',[r for r in types['replay'] if r['id'] in replay_open]+types['manual'],common_fields)
    write_tsv(REC/'PRIOR_RESOLVED_REPLAY_REVIEW.tsv',[r for r in types['replay'] if r['id'] not in replay_open],common_fields)
    write_tsv(REC/'CODEX_DECIDED.tsv',types['rejected_codex']+types['hold_difference'],common_fields)
    own=[];conventions=[]
    for id,d in decisions.items():
        if id in byid:continue
        row={'id':id,'page':d.get('page',''),'place':d.get('where',d.get('region','')),'printed_reading':d.get('printed_reading',''),
          'tex_reading':d.get('tex',''),'change':jd(d.get('change',d.get('correction',''))),'kind':d.get('kind',d.get('type',d.get('record_type',''))),
          'verdict':d.get('verdict',''),'image':d.get('image',''),'region':d.get('region',''),'reason':d.get('reason',''),'review_file':d['review_file']}
        if row['kind'] in ['convention','marker','boundary']:conventions.append(row)
        else:own.append(row)
    write_tsv(REC/'CHECK_FINDINGS.tsv',own,['id','page','place','printed_reading','tex_reading','change','kind','verdict','image','region','reason','review_file'])
    write_tsv(REC/'DECISIONS.tsv',conventions,['id','page','place','printed_reading','change','kind','verdict','image','region','reason','review_file'])

    # One row for every primary scan front-matter page and every folio 1–700.
    page_map={}
    for p in pages:
        pdf=p.get('pdf_page')
        if pdf is None and isinstance(p.get('page'),int):pdf=p['page']+14
        if pdf:page_map[pdf]=p
    front_labels=['cover','cover-verso','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
    page_rows=[]
    revised=ROOT/'build/FR_current_revised.tex'
    ftext=revised.read_text() if revised.exists() else ''
    master_paths={'FR_master_begin':'readers/fr/SGA6_FR_master_annote_DRAFT.tex',
      'EN_master_begin':'review/english/DRAFT_SGA6_EN_annotated_master.tex'}
    starts={}
    for column,rel in master_paths.items():
        path=ROOT/rel;body=path.read_text() if path.exists() else ''
        starts[column]={}
        for match in re.finditer(r'(?m)^%+\s*scan idx\s+\d+\s*\|\s*folio\s+(\S+)\s*%+',body):
            starts[column][match[1]]=rel+'#line='+str(body.count('\n',0,match.start())+1)
    # Count each checker/hand-placed finding once, independently of its duplicate
    # FIXLOG and misprint-register rows; include the new independent findings.
    finding_counts=collections.Counter()
    for row in types['finding']+types['manual']+own:
        finding_counts[str(row['page'])]+=1
    for pdf in range(1,715):
        folio=front_labels[pdf-1] if pdf<=14 else pdf-14
        p=page_map.get(pdf,{})
        checked=p.get('fully_checked',p.get('checked_against_scan',p.get('checked',False))) is True
        page_rows.append({'pdf_page':pdf,'folio':folio,'checked_against_scan':str(checked).lower(),'findings':finding_counts[str(folio)],
          'FR_master_begin':starts['FR_master_begin'].get(str(folio),''),
          'EN_master_begin':starts['EN_master_begin'].get(str(folio),''),'image':p.get('image',p.get('scan','')),
          'region':p.get('region',p.get('regions',p.get('main_scan_viewed',''))),
          'status':p.get('status','fully compared' if checked else 'pending_scan_review'),
          'reason':p.get('reason',p.get('note',p.get('notes','No independent page comparison recorded.')))})
    write_tsv(REC/'PAGES_CHECKED.tsv',page_rows,['pdf_page','folio','checked_against_scan','findings','FR_master_begin','EN_master_begin','image','region','status','reason'])

    # Exact diff hunks, preserving complete source text rather than a summary.
    if ftext:
        changes=[]
        for before_rel in ['fr/codex/ref_hold/main.tex','fr/sga6/current/main.tex']:
            before=(ROOT/before_rel).read_text().splitlines(keepends=True)
            after=ftext.splitlines(keepends=True)
            for tag,a,b,c,d in difflib.SequenceMatcher(None,before,after,autojunk=True).get_opcodes():
                if tag=='equal':continue
                prefix=''.join(after[:c]);marks=list(re.finditer(r'folio\s+(\d+)\s*%',prefix))
                page=int(marks[-1][1]) if marks else 'front'
                changes.append({'page':page,'place':f'after lines {c+1}–{d}','before':''.join(before[a:b]),'after':''.join(after[c:d]),
                  'source':before_rel,'provenance':'Exact source diff; see PATCH_APPLICATION_FR.json for reviewed edits.','status':'draft source comparison'})
        write_tsv(REC/'CHANGES_FR.tsv',changes,['page','place','before','after','source','provenance','status'])

    counts={}
    for kind,rs in types.items():
        counts[kind]={'total':len(rs),'decided':sum(not r['verdict'].startswith('pending') for r in rs),'pending':sum(r['verdict'].startswith('pending') for r in rs)}
    counts['pages']={'total':len(page_rows),'checked':sum(r['checked_against_scan']=='true' for r in page_rows),'unchecked':sum(r['checked_against_scan']!='true' for r in page_rows)}
    counts['own_findings']=len(own)
    counts['release_complete']=False
    (REC/'CHECKPOINT_STATUS.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(counts,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
