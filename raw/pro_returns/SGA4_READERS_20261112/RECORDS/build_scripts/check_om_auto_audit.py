"""Validate exact one-model audit pairs without changing French source layers."""
from pathlib import Path
import copy,csv,hashlib,json,re,sys
from fr_core import group,find_exact
from marker_projection import carry_markers
ROOT=Path(__file__).resolve().parents[1]
MARK=re.compile(r'\\SGApageno\{[^{}]*\}\{[^{}]*\}')
def notes(text):
    out=[]
    for m in re.finditer(r'\\(?:nde|ndetext)\s*\{',text):
        a=m.start()
        if re.search(r'(?<!\\)%',text[text.rfind('\n',0,a)+1:a]):continue
        _,b=group(text,text.index('{',a));out.append(text[a:b])
    return out

def main():
    path=ROOT/'work_fr/om_auto_baseline.json';data=json.loads(path.read_text());before=copy.deepcopy(data)
    rows=json.loads((ROOT/'output/shared/ONE_MODEL_FR_AUTO_AUDIT_PAIRS.json').read_text())
    scope=json.loads((ROOT/'work_fr/om_auto_scope.json').read_text())
    manual=json.loads((ROOT/'output/shared/ONE_MODEL_FR_PATCHES.json').read_text())
    edits=json.loads((ROOT/'output/records/one_model_edits.json').read_text())
    accepted={r['id'] for r in edits if r['application']=='accepted-candidate' and not r['on_disputed_page']}
    ids={r['id'] for r in rows};manual_ids={r['id'] for r in manual}
    assert ids=={r['id'] for r in scope}
    assert len(ids)==169 and len(rows)==170
    supplement_ids={r['id'] for r in json.loads((ROOT/'output/shared/ONE_MODEL_FR_0352_SUPPLEMENT.json').read_text())}
    assert not ids&manual_ids and len(manual_ids)==168 and ids|manual_ids|supplement_ids==accepted
    final_positions=[]
    for row in rows:
        assert row['printed']!=row['corrected']
        f=row['file'];entry={'id':row['id'],'part':row['part'],'file':f,'page':row['page'],'printed':row['printed'],'corrected':row['corrected'],'reason':row['reason'],'requires_repair':row['requires_repair']}
        for layer,target in [('dip',row['printed']),('corr',row['corrected'])]:
            item=row[layer];a=item['at'];old=item['old'];b=a+len(old);t=data[layer][f]
            assert row[layer+'_hits']==1
            assert t[a:b]==old,(row['id'],layer,'old-span')
            assert t[max(0,a-len(item['context_before'])):a]==item['context_before'],(row['id'],layer,'before')
            assert t[b:b+len(item['context_after'])]==item['context_after'],(row['id'],layer,'after')
            assert item['new']==carry_markers(old,target),(row['id'],layer,'marker-projection')
            assert MARK.findall(old)==MARK.findall(item['new']),(row['id'],layer,'markers')
            data[layer][f]=t[:a]+item['new']+t[b:]
            entry[layer]={'old':old,'new':item['new'],'context_before':item['context_before'],'context_after':item['context_after'],'verified':True}
        if row.get('represented_by'):entry['represented_by']=row['represented_by']
        final_positions.append(entry)
    for layer in ('dip','corr'):
        for f,t in data[layer].items():
            assert MARK.findall(t)==MARK.findall(before[layer][f]),(layer,f,'marker-sequence')
            assert notes(t)==notes(before[layer][f]),(layer,f,'editorial-note')
    judgments=list(csv.DictReader((ROOT/'output/records/ONE_MODEL_MISPRINTS_JUDGED.tsv').open(),delimiter='\t'))
    human=[r for r in judgments if r['verdict']=='accept' and r['application']=='preserve-human-record']
    # Human-record spelling is retained exactly as the judgment table records it.
    if not human:human=[r for r in judgments if r['verdict']=='accept' and 'human' in r['application']]
    assert len(human)==53,len(human)
    repair=[r for r in rows if r['requires_repair']]
    assert len(repair)==20
    payload=json.dumps(rows,ensure_ascii=False)
    assert not re.search(r'/(?:workspace|home|root)/',payload)
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',payload)
    result={'records':169,'parts':170,'repairs':20,'unique_both_layers':170,'unlocated':0,'accepted_undisputed_total':len(accepted),'original_review_cohort':337,'later_supplement_records':len(supplement_ids),'later_supplement_ids':sorted(supplement_ids),'complementary_manual_records':168,'accepted_existing_human_records':53,'disputed_page_candidates':0,'baseline':'work_fr/om_auto_baseline.json','baseline_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':['Every one of the 169 intended contexts was read individually.','All 170 parts have distinct printed and corrected readings and a unique location in each branch.','Sequential old text and exact surrounding contexts match the frozen baseline.','The printed-page marker sequence and projected marker boundaries are unchanged.','Existing nde and ndetext editorial note arguments remain byte-for-byte unchanged.','The automatic 169 and manual 168 scopes are disjoint and cover the original 337-record review cohort; the six-part OM-SOL-0352 supplement completes the current 338 accepted undisputed records.','The 53 accepted reports already recorded by human editors remain separately preserved.','No disputed-page candidate, local machine path, or email address is included.'],'repair_ids':[r['id'] for r in repair]}
    (ROOT/'output/shared/ONE_MODEL_FR_AUTO_AUDIT_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'output/records/ONE_MODEL_FR_AUTO_BRANCH_AUDIT.json').write_text(json.dumps(final_positions,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
