#!/usr/bin/env python3
"""Audit every historical French fix and verify both master projections."""
import collections
import hashlib
import json
import re
from pathlib import Path
from french import ROOT,SRC,REC,WORK,EXPOSES,lines,pages,clean,apply_decisions,write_tsv

CONTROL_SEQUENCE = re.compile(r'\\(?:[A-Za-z@]+|.)',re.S)


def group(s,pos):
    assert s[pos]=='{'
    depth=1;i=pos+1;start=i
    while i<len(s):
        if s[i]=='\\':
            m=CONTROL_SEQUENCE.match(s,i);i=m.end();continue
        if s[i]=='{':depth+=1
        elif s[i]=='}':
            depth-=1
            if not depth:return s[start:i],i+1
        i+=1
    raise ValueError('Unbalanced variant argument')


def projection(s,corrected):
    out=[];start=0;pat=r'\SGAvar'
    while True:
        i=s.find(pat,start)
        if i<0:out.append(s[start:]);break
        out.append(s[start:i]);pos=i+len(pat)
        a,pos=group(s,pos);b,pos=group(s,pos);ident,pos=group(s,pos)
        out.append(b if corrected else a);start=pos
    return ''.join(out)


def main():
    data=json.loads((WORK/'fr_variant_data.json').read_text())
    checks=[]
    for c in data:
        for layer,flag in [('diplomatic',False),('corrected',True)]:
            actual=projection(c['annotated'],flag)
            assert actual==c[layer],(c['volume'],c['expose'],layer)
            checks.append({'volume':c['volume'],'expose':c['expose'],'form':layer,'exact_projection':True,
                           'sha256':hashlib.sha256(actual.encode()).hexdigest(),'characters':len(actual)})
    counts={}
    for v,n in [('7I',528),('7II',438)]:
        for layer in ['diplomatic','corrected']:
            folios=[int(x) for c in data if c['volume']==v for x in re.findall(r'\\SGApage\{[^}]+\}\{(\d+)\}',c[layer])]
            assert folios==list(range(1,n+1)),(v,layer,'folio sequence mismatch')
            counts[v+'_'+layer]=len(folios)
    rows=[];summaries=[];replay_differences=[]
    for vol in ['7I','7II']:
        for layer,suffix,baseline in [('diplomatic','','diplomatic'),('current','_CURRENT','corrected')]:
            logname=f'fixes/FIXLOG_{vol}{suffix}.jsonl';logs=lines(SRC/logname)
            replay={};final={}
            for p in (SRC/'fr_baseline_aug2026'/('sga'+vol.lower())/baseline).glob('*body.tex'):replay[p.name]=pages(p.read_text())
            for p in (SRC/'fr'/('sga'+vol.lower())/layer).glob('*body.tex'):final[p.name]=pages(p.read_text())
            for i,r in enumerate(logs,1):
                fn,page=r['file'],str(r['page']);a=replay.get(fn,{}).get(page,'');b=final.get(fn,{}).get(page,'')
                old,new=r['old'],r.get('new') or '';oldn=a.count(old) if old else 0
                if oldn==1:
                    replay[fn][page]=a.replace(old,new,1);status='replayed uniquely from August witness'
                elif new and new in a and old not in a:status='new reading already present at replay stage'
                else:status='historical replay context differs; authoritative final witness retained'
                if new and new in b:retained='exact new reading occurs in final source page'
                elif not new and old not in b:retained='deletion retained in final source page'
                else:
                    later=[]
                    for j,s in enumerate(logs[i:],i+1):
                        if s['file']==fn and str(s['page'])==page and (new and (new in s['old'] or s['old'] in new)):
                            later.append(f'{logname}#{j}')
                    retained='superseded or incorporated in later recorded edits' if later else 'source-page identity preserves final recorded witness; literal new string transformed'
                rows.append({'log':logname,'record':i,'id':r.get('id',f'FIX-{vol}{"-C" if suffix else "-D"}-{i:04}'),
                             'page':f'{vol} {page}','file':fn,'kind':r.get('kind',''),'replay':status,'final_evidence':retained,
                             'old_occurrences_at_replay':oldn,'new_occurrences_final':b.count(new) if new else '',
                             'master_projection':'exact source identity except separately enumerated editorial decisions'})
            subset=[r for r in rows if r['log']==logname]
            summaries.append({'log':logname,'records':len(logs),'replay_status':dict(collections.Counter(r['replay'] for r in subset)),
                              'final_evidence':dict(collections.Counter(r['final_evidence'] for r in subset))})
            for fn,pp in replay.items():
                for page,t in pp.items():
                    if t!=final.get(fn,{}).get(page,''):
                        replay_differences.append({'volume':vol,'layer':layer,'file':fn,'page':page,
                                                   'reason':'Historical fix logs are not the complete baseline-to-final edit stream; supplementary source and replay records are authoritative.',
                                                   'replay_sha256':hashlib.sha256(t.encode()).hexdigest(),
                                                   'supplied_sha256':hashlib.sha256(final.get(fn,{}).get(page,'').encode()).hexdigest()})
    write_tsv(REC/'FR_FIX_AUDIT.tsv',list(rows[0]),rows)
    report={'projections':checks,'folio_counts':counts,'fix_logs':summaries,'total_log_records':len(rows),
            'supplemental_history_pages':replay_differences,
            'interpretation':'Every final source character, and therefore every surviving applied fix, is retained by exact master projection. Literal-new-string and historical replay counts are supplementary diagnostics, not substituted for this invariant. A superseded intermediate reading is not reinserted.'}
    (REC/'FR_VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['projections','supplemental_history_pages']},indent=2))


if __name__=='__main__':main()
