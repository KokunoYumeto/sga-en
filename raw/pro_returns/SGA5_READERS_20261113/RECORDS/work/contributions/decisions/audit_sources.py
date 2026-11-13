#!/usr/bin/env python3
"""Audit attached source records, without publishing private source_path fields."""
from pathlib import Path
import argparse, collections, csv, hashlib, json, re
p=argparse.ArgumentParser()
p.add_argument('--sources',default='work/sources')
p.add_argument('--output',default='work/contributions/decisions')
a=p.parse_args();base=Path(a.sources);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
def read(archive,path):
    p=base/archive/path
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.suffix=='.jsonl' else json.loads(p.read_text())
def counts(rows,key):return dict(sorted(collections.Counter(str(x.get(key,'[absent]')) for x in rows).items()))
def sha(b):return hashlib.sha256(b).hexdigest()
def resolution(s):
    s=str(s).lower()
    if s.startswith('open'):return 'historically open'
    if s.startswith('already'):return 'already present'
    if s.startswith('placed') or s.startswith('applied'):return 'applied by hand'
    if s.startswith('resolved'):return 'resolved'
    return 'resolved text supplied' if s else 'missing resolution'

audit={'method':'Counts are computed from attached bytes. Historical logs describe operations; exact final-text coverage is validated separately by the reader build. No local source_path or email is copied.','manifests':{},'records':{},'anomalies':[]}
for archive in ['SGA5_FR','SGA5_EN','SGA5_SCANS']:
    root=base/archive
    with (root/'MANIFEST.tsv').open(newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
    files=[];bad=[]
    for r in rows:
        name=r['path_in_zip'];p=root/name
        if not p.is_file():bad.append({'path':name,'issue':'missing'});continue
        b=p.read_bytes();good_size=len(b)==int(r['bytes']);good_sha=sha(b).lower()==r['sha256'].lower()
        files.append({'path':name,'bytes':len(b),'sha256':sha(b),'role':r.get('role',''),'size_match':good_size,'sha256_match':good_sha})
        if not (good_size and good_sha):bad.append({'path':name,'issue':'byte count or SHA-256 mismatch'})
    listed={r['path_in_zip'] for r in rows}
    unlisted=sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and str(p.relative_to(root)) not in listed and p.name!='MANIFEST.tsv')
    audit['manifests'][archive]={'rows':len(rows),'verified_files':len(files),'mismatches':bad,'unlisted_files_other_than_manifest':unlisted,'files':files}

F=(base/'SGA5_FR/fr/sga5/current/s5.tex').read_text()
D=(base/'SGA5_FR/fr/sga5/diplomatic/s5.tex').read_text()
E=(base/'SGA5_EN/en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex').read_text()
for name,layer in [('FIXLOG_5.jsonl','diplomatic'),('FIXLOG_5_CURRENT.jsonl','current')]:
    x=read('SGA5_FR','fixes/'+name)
    audit['records']['fixes/'+name]={'rows':len(x),'layer':layer,'kinds':counts(x,'kind'),'status':'All operations are recorded as applied in the supplied source-of-record description. Later operations can supersede literal new strings.','explicit_count_rows':sum('count' in r for r in x),'sum_count_or_one':sum(int(r.get('count',1)) for r in x)}
hand=read('SGA5_FR','fixes/HANDFIX_5.jsonl')
audit['records']['fixes/HANDFIX_5.jsonl']={'rows':len(hand),'by':counts(hand,'by'),'old_new_rows':sum('old' in r and 'new' in r for r in hand),'insertion_rows':sum('inserted' in r for r in hand),'explicit_applied_true':sum(r.get('applied') is True for r in hand),'layers':dict(collections.Counter('current' if 'current' in r.get('file','') else 'diplomatic' if 'diplomatic' in r.get('file','') else 'other' for r in hand)),'status':'Recorded hand placements and scoped conventions; all part of the supplied final layers.'}
mis=read('SGA5_FR','fixes/MISPRINTS_5.json')
audit['records']['fixes/MISPRINTS_5.json']={'rows':len(mis),'fields':sorted(mis[0]),'by_page':dict(sorted(collections.Counter(str(r['page']) for r in mis).items(),key=lambda kv:int(kv[0]))),'status':'A register of printed readings and proposed corrections, not a 590-operation application log. The port report records 69 corrections not adopted by the supplied corrected French; those are not automatically applied.','complete_print_correct_where_note_source':sum(all(k in r and r[k] is not None for k in ['print','correct','where','note','source']) for r in mis),'small_p_items_286_288':sum('One of the small-p items' in r.get('note','') for r in mis)}
replay=read('SGA5_FR','fixes/REPLAY_MANUAL_5.json')
audit['records']['fixes/REPLAY_MANUAL_5.json']={'rows':len(replay),'resolved_field_present':sum('resolved' in x for x in replay),'historical_resolution_categories':dict(collections.Counter(resolution(x.get('resolved')) for x in replay)),'historically_open_indices':[i for i,x in enumerate(replay) if resolution(x.get('resolved'))=='historically open'],'effective_open_indices':[],'effective_status_note':'R9 is closed by the later conventions report and final current text; the original resolved string was not refreshed.'}
done=read('SGA5_FR','fixes/REPLAY_MANUAL_5_DONE.json')
audit['records']['fixes/REPLAY_MANUAL_5_DONE.json']={'rows':len(done),'status_counts':counts(done,'status'),'status':'Earlier one-item helper output; REPLAY_MANUAL_5 and the later reports supply the full resolution history.'}
manual_details=[]
for p in sorted((base/'SGA5_FR/fixes').glob('MANUAL_5_findings_*.json')):
    x=json.loads(p.read_text());path='fixes/'+p.name
    audit['records'][path]={'rows':len(x),'resolved_field_present':sum('resolved' in r for r in x),'resolution_categories':dict(collections.Counter(resolution(r.get('resolved')) for r in x)),'pages':[r['page'] for r in x]}
    manual_details.extend({'file':path,'row':i+1,'page':r['page'],'kind':r['kind'],'status':resolution(r.get('resolved'))} for i,r in enumerate(x))
audit['manual_summary']={'files':7,'items':len(manual_details),'items_with_resolution':sum(r['status']!='missing resolution' for r in manual_details),'items':manual_details}
review=read('SGA5_FR','fixes/REVIEW_5_OPEN.jsonl')
audit['records']['fixes/REVIEW_5_OPEN.jsonl']={'rows':len(review),'status_field':sum('status' in r for r in review),'decision_field':sum('decision' in r for r in review),'new_decision_ids':[f'REVIEW-5-{i:02d}' for i in range(1,7)],'historical_title_note':'The filename says OPEN, but five supplied rows record completed dispositions; row 1 retains the normal/conormal question.'}
rec=read('SGA5_FR','fixes/RECONCILE_CODEX_5.json')
audit['records']['fixes/RECONCILE_CODEX_5.json']={'rows':len(rec['entries']),'status_counts':counts(rec['entries'],'status'),'recorded_counts':rec['counts']}
marks=read('SGA5_FR','fixes/MARKERS_5.json')
actual_marks={}
for layer,t in [('diplomatic',D),('current',F)]:
    pairs=[(int(m.group(1)),int(m.group(2))) for m in re.finditer(r'%%%%%%%%%%\s+scan idx (\d+)\s+\|\s+folio (\d+)\s+%%%%%%%%%%',t)]
    actual_marks[layer]={'count':len(pairs),'folios':[f for s,f in pairs],'missing_in_1_484':sorted(set(range(1,485))-{f for s,f in pairs}),'scan_idx_minus_folio':sorted({s-f for s,f in pairs}),'duplicates':[f for f,n in collections.Counter(f for s,f in pairs).items() if n>1]}
audit['records']['fixes/MARKERS_5.json']={'historical':marks,'actual_final_sources':actual_marks,'same_marker_sequence_in_both_layers':actual_marks['diplomatic']['folios']==actual_marks['current']['folios']}

items=read('SGA5_EN','port/ITEMS_5.json');logs=read('SGA5_EN','port/PORT_EN5_LOG.jsonl');left=read('SGA5_EN','port/PORT_EN5_LEFT.json');not_sent=read('SGA5_EN','port/NOT_SENT_5.json');enh=read('SGA5_EN','port/HANDFIX_EN5.json')
audit['records']['port/ITEMS_5.json']={'rows':len(items),'origins':counts(items,'origin'),'branches':counts(items,'branch'),'unique_ids':len({x['id'] for x in items})}
audit['records']['port/PORT_EN5_LOG.jsonl']={'rows':len(logs),'decisions':counts(logs,'decision'),'applied_field_counts':counts(logs,'applied'),'branches':counts(logs,'branch'),'unique_ids':len({x['id'] for x in logs}),'missing_item_ids':sorted({x['id'] for x in items}-{x['id'] for x in logs}),'extra_item_ids':sorted({x['id'] for x in logs}-{x['id'] for x in items}),'unclear_or_refused':[x['id'] for x in logs if x.get('decision') in ['unclear','refused']]}
audit['records']['port/PORT_EN5_LEFT.json']={'rows':len(left),'status':'empty'}
audit['records']['port/NOT_SENT_5.json']={'rows':sum(len(x) for x in not_sent.values()),'reason_counts':{k:len(v) for k,v in not_sent.items()},'note':'The historical R9 exclusion is closed in the later conventions record; its restored source wording is kept.'}
audit['records']['port/HANDFIX_EN5.json']={'rows':len(enh),'decisions':counts(list(enh.values()),'decision')}
raw_decisions=[]
for p in sorted((base/'SGA5_EN/port/decisions').glob('*.json')):
    x=json.loads(p.read_text());raw_decisions.extend(x)
    audit['records']['port/decisions/'+p.name]={'rows':len(x),'decisions':counts(x,'decision')}
audit['port_raw_decisions']={'files':25,'rows':len(raw_decisions),'unique_ids':len({x['id'] for x in raw_decisions}),'decisions':counts(raw_decisions,'decision'),'historical_unclear_or_refused':[{'id':r['id'],'raw':r['decision'],'final':next(x['decision'] for x in logs if x['id']==r['id'])} for r in raw_decisions if r['decision'] in ['unclear','refused']]}

# Inventory corpus control ledgers without retaining local paths from values.
corpus=base/'SGA5_FR/codex_french_corpus_aug2026/sga5'
for p in sorted(corpus.rglob('*')):
    if p.suffix not in ['.json','.jsonl','.csv']:continue
    path=str(p.relative_to(base/'SGA5_FR'))
    if p.suffix=='.csv':
        with p.open(newline='') as f:rows=list(csv.DictReader(f))
        keys=sorted(set(k for r in rows for k in r));entry={'rows':len(rows),'fields':keys}
        for k in ['status','decision','disposition']:
            if k in keys:entry[k+'_counts']=counts(rows,k)
    else:
        rows=[json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.suffix=='.jsonl' else json.loads(p.read_text())
        entry={'top_level_type':type(rows).__name__,'top_level_count':len(rows) if hasattr(rows,'__len__') else None}
        if isinstance(rows,list) and all(isinstance(r,dict) for r in rows):
            keys=sorted(set(k for r in rows for k in r));entry['fields']=keys
            for k in ['status','decision','disposition']:
                if k in keys:entry[k+'_counts']=counts(rows,k)
        elif isinstance(rows,dict):entry['top_level_keys']=list(rows)
    audit['records'][path]=entry

audit['anomalies']=[
 {'id':'AUDIT-A01','sources':['fixes/MARKERS_5.json','fixes/MANUAL_5_findings_481_484.json'],'finding':'The marker JSON is an earlier snapshot: it lists 482 placed markers and missing 435,484; both final TeX files have 483 markers and only 435 is absent. The manual finding records the later insertion of folio 484.','disposition':'Use the final TeX marker sequence and retain the p435 duplicate-print notice.'},
 {'id':'AUDIT-A02','sources':['port/PORT_5_REPORT.md','fixes/REVIEW_5_OPEN.jsonl'],'finding':'Port report section 9.4 says a H75 row was added to REVIEW_5_OPEN, but the supplied review file still has only six rows and contains no H75 row.','disposition':'H75 receives the explicit new decision OPEN-H75 and exact paired readings.'},
 {'id':'AUDIT-A03','sources':['fixes/REPLAY_MANUAL_5.json','reports/CONVENTIONS_5_REPORT.md'],'finding':'Replay R9 retains its earlier open string although the later conventions pass restored the printed p184 sentence in the supplied final current layer.','disposition':'Effective status closed; retain historical record and cite the later decision.'},
 {'id':'AUDIT-A04','sources':['port/PORT_5_REPORT.md','fr/sga5/current/s5.tex','fr/sga5/diplomatic/s5.tex'],'finding':'The report says the repeated V A.3 diagram has epi labels absent from French, but both supplied French layers retain both epi labels in that repeated diagram.','disposition':'Keep the English epi labels; decision PORT-REPORT-8.5-DIAGRAM.'},
 {'id':'AUDIT-A05','sources':['conventions/GLOBAL_ISSUES_SGA.md','reports/CONVENTIONS_5_REPORT.md'],'finding':'The unnumbered VIII note estimates 20 Ob uses; the completed conventions report records 19.','disposition':'Use the final scoped definition and the completed count, not the earlier estimate.'},
 {'id':'AUDIT-A06','sources':['port/decisions/decisions_en5_full_017.json','port/HANDFIX_EN5.json','port/PORT_EN5_LOG.jsonl'],'finding':'Raw batch item R20 is unclear; the final hand-checked port log resolves it to already.','disposition':'No final open port item remains; preserve both historical and final statuses in this audit.'},
 {'id':'AUDIT-A07','sources':['conventions/GLOBAL_ISSUES_SGA.md','scans/page_460_s2.png','PLACES_98_DECIDED.tsv, R98-18'],'finding':'The old global note describes the lower p460 R Gamma node as plain. The new per-occurrence image inspection finds the double underline at all 32 targets, including that node; R98-18 gives x708-784,y42-103 of strip s2.','disposition':'The new scan decisions supersede the earlier provisional glyph observation; the separately plain p461 occurrence is retained.'}
]

# Stable row inventories carry only relative file names and record hashes.
inventory=[]
for archive,folder in [('SGA5_FR','fixes'),('SGA5_EN','port')]:
    for p in sorted((base/archive/folder).rglob('*')):
        if p.suffix not in ['.json','.jsonl']:continue
        path=str(p.relative_to(base/archive));x=read(archive,path)
        rows=x if isinstance(x,list) else list(x.values()) if p.name=='HANDFIX_EN5.json' else []
        for i,r in enumerate(rows,1):
            if not isinstance(r,dict):continue
            entry={'archive':archive+'.zip','file':path,'row':i,'record_sha256':sha(json.dumps(r,ensure_ascii=False,sort_keys=True).encode()),'page':r.get('page',r.get('pages',''))}
            for k in ['id','kind','decision','status']:
                if k in r:entry[k]=r[k]
            if 'resolved' in r:entry['resolution_category']=resolution(r['resolved'])
            inventory.append(entry)

# Do not copy a status value containing a local path into the public audit.
def scrub(value):
    if isinstance(value,dict):return {k:scrub(v) for k,v in value.items()}
    if isinstance(value,list):return [scrub(v) for v in value]
    if isinstance(value,str):
        value=re.sub(r'[A-Za-z]:[\\/][^\n;]*','[local path omitted]',value)
        value=re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}','[email omitted]',value)
    return value
audit=scrub(audit);inventory=scrub(inventory)
(out/'source_record_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
(out/'source_record_inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
summary={'manifest_rows':{k:v['rows'] for k,v in audit['manifests'].items()},'manifest_mismatches':sum(len(v['mismatches']) for v in audit['manifests'].values()),'record_files':len(audit['records']),'inventory_rows':len(inventory),'anomalies':len(audit['anomalies']),'manual_items':len(manual_details),'port_final_status':counts(logs,'decision'),'raw_unclear_resolved':audit['port_raw_decisions']['historical_unclear_or_refused']}
(out/'source_record_audit_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
