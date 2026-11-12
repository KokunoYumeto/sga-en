"""Deduplicated final English source dispositions, with per-part evidence.

This register keeps failed projection attempts as history. It does not turn
one successful occurrence into proof that a multipart correction is complete:
each inspected English part has its own placement evidence, the complete
French witness list remains visible, and final branch/source audits are
separate gates.
"""
from en_common import *
from en_extra import key
import hashlib,collections

SUCCESS={'paired','represented by existing variant'}
INPUTS=['EN_REVIEW_EXTRA45.json','EN_T3_EXACT_PAIRS.json','EN_T2_LATE_EXACT_PAIRS.json',
        'EN_T3_AUTO_REPAIR_PAIRS.json','EN_T1_T2_EXACT_PAIRS.json',
        'EN_ONE_MODEL_NO_IMPACT_PARTIAL.json','EN_ONE_MODEL_EXACT_PAIRS.json']

def match_key(text,exp,page):
    # Only the separately recorded printed-cardinal convention is composed
    # here. The complete inspected text and all other tokens remain visible.
    if exp=='I' and 136<=int(page)<=178:
        text=re.sub(r'\\Pi(?![A-Za-z@])',lambda m:r'\pi',text)
    return key(text)

def main():
    master=ROOT/'output/en/SGA4_EN_annotated_master.tex'
    variants=json.loads((RECORDS/'EN_VARIANTS.json').read_text())
    by_source=collections.defaultdict(list)
    for v in variants:
        for source in v['source'].split('; '):by_source[source].append(v)
    attempts=collections.defaultdict(list)
    for number,row in enumerate(json.loads((RECORDS/'EN_SOURCE_AUDIT.json').read_text()),1):
        attempts[row['id']].append(dict(row,audit_row=number))
    reviewed={}
    language=RECORDS/'EN_MISPRINT_LANGUAGE_ASSESSMENT.json'
    for r in json.loads(language.read_text()) if language.exists() else []:
        reviewed[r['id']]=dict(r,review_file='EN_MISPRINT_LANGUAGE_ASSESSMENT.json')
    for r in json.loads((RECORDS/'EN_MANUAL_PAIRS.json').read_text()):
        if reviewed.get(r['id'],{}).get('review_file')!='EN_MANUAL_PAIRS.json':
            reviewed[r['id']]=dict(id=r['id'],expose=EXPOSE[r['file']],page=r['page'],assessment='English-impact',review_file='EN_MANUAL_PAIRS.json',english_deltas=[])
        reviewed[r['id']]['english_deltas'].append(r)
    for name in INPUTS:
        for r in json.loads((ROOT/'output/shared'/name).read_text()):reviewed[r['id']]=dict(r,review_file=name)
    compositions={r['id']:r for r in json.loads((RECORDS/'EN_COMPOSED_REVIEW_READINGS.json').read_text())['records']}
    french=collections.defaultdict(list)
    ignored={'Adaptation to the existing E corrected spelling','Restoration of the documented printed reading'}
    for number,p in enumerate(json.loads((RECORDS/'FR_APPLIED_PATCHES.json').read_text()),1):
        if p.get('method') in ignored:continue
        for source in p.get('source',p.get('id','')).split('; '):
            if re.fullmatch(r'MP\d{4}|OM-(?:SOL|OPUS)-\d{4}',source):
                french[source].append(dict(ledger_row=number,printed=p['printed'],corrected=p['corrected'],method=p.get('method',''),source=p.get('source',p.get('id'))))
    canonical=json.loads((SOURCES/'fixes/MISPRINTS_4.json').read_text())
    items=[dict(id='MP%04d'%i,expose=p['expose'],page=p['page'],canonical_source='fixes/MISPRINTS_4.json#MP%04d'%i) for i,p in enumerate(canonical,1)]
    one=json.loads((ROOT/'output/shared/EN_ONE_MODEL_EXACT_PAIRS.json').read_text())
    items.extend(dict(id=r['id'],expose=r['expose'],page=r['page'],canonical_source='EN_ONE_MODEL_EXACT_PAIRS.json#'+r['id']) for r in one)
    records=[];missing_parts=[]
    for item in items:
        ident=item['id'];exp=item['expose'];page=item['page'];r=reviewed.get(ident)
        rows=attempts[ident];success=[x for x in rows if x['status'] in SUCCESS]
        noimpact=next((x for x in reversed(rows) if x['status']=='no English impact'),None)
        common=bool(r and r['assessment'].lower().startswith('no')) or bool(noimpact and not success)
        history=[dict(x,history_status='unsuccessful intermediate projection attempt; consult the explicit final disposition and per-part evidence below') for x in rows if x['status'] not in SUCCESS|{'no English impact'}]
        final=dict(item,disposition='no English impact' if common else 'English variants registered',variant_ids=[v['id'] for v in by_source[ident]],source_links=[dict(variant_id=v['id'],all_sources=v['source'],printed=v['printed'],corrected=v['corrected']) for v in by_source[ident]],final_french_witness_parts=french[ident],prior_unsuccessful_projection_history=history)
        if common:
            final.update(review_file=r.get('review_file') if r else 'EN_SOURCE_AUDIT.json',reason=(r or {}).get('reason',(noimpact or {}).get('method','')),unchanged_english_reading=(r or {}).get('english_reading') or (r or {}).get('english_context') or (r or {}).get('english_evidence',''),english_parts=[])
        else:
            inspected=[]
            if r:
                inspected=r.get('english_deltas',[r.get('english_delta',{})])
                inspected=[d for d in inspected if d and d.get('printed')!=d.get('corrected')]
            if not inspected:
                seen=set()
                for a in success:
                    k=(a['printed'],a['corrected'])
                    if k not in seen:inspected.append(dict(printed=k[0],corrected=k[1]));seen.add(k)
                final['coverage_basis']='All registered projections are enumerated and every final French witness is retained; multipart source completeness is an independent source-review gate.'
            else:final['coverage_basis']='Every separately reviewed English part is listed and matched to its own recorded placement attempt; independent literal branch audits are separate gates.'
            parts=[]
            for n,d in enumerate(inspected,1):
                old=d.get('pre_notation_printed',d['printed']);new=d.get('pre_notation_corrected',d['corrected'])
                exact=[a for a in success if match_key(a['printed'],exp,page)==match_key(old,exp,page) and match_key(a['corrected'],exp,page)==match_key(new,exp,page)]
                if not exact:
                    # The placement ledger retains the exact raw spelling in
                    # the matched English source, including equivalent one-
                    # token groups and already existing human punctuation.
                    exact=[a for a in success if match_key(old,exp,page) in match_key(a['printed'],exp,page) and match_key(new,exp,page) in match_key(a['corrected'],exp,page)]
                method_ids=set(re.findall(r'EN-V\d+',' '.join(a.get('method','') for a in exact)))
                for v in by_source[ident]:
                    if match_key(old,exp,page) in match_key(v['printed'],exp,page) and match_key(new,exp,page) in match_key(v['corrected'],exp,page):method_ids.add(v['id'])
                composed=compositions.get(ident)
                expected=composed['english_deltas'][n-1] if composed and n<=len(composed['english_deltas']) else d
                part=dict(part=n,review_file=r.get('review_file') if r else 'EN_SOURCE_AUDIT.json',reviewed_printed=d['printed'],reviewed_corrected=d['corrected'],expected_final_printed=expected['printed'],expected_final_corrected=expected['corrected'],placement_audit_rows=[a['audit_row'] for a in exact],placement_methods=[a['method'] for a in exact],variant_ids=sorted(method_ids),placement_evidence_found=bool(exact))
                if composed:part['composition_record']='EN_COMPOSED_REVIEW_READINGS.json#'+ident
                if not exact:missing_parts.append((ident,n))
                parts.append(part)
            final['english_parts']=parts
            final['every_reviewed_part_has_placement_evidence']=bool(parts) and all(p['placement_evidence_found'] for p in parts)
        records.append(final)
    payload=dict(master_sha256=hashlib.sha256(master.read_bytes()).hexdigest(),agreed_misprints=930,accepted_undisputed_one_model=338,record_count=len(records),method='Source disposition and per-part placement register. Prior unsuccessful attempts are retained as history. A source ID on one variant is not a multipart completion check.',independent_gates=['EN_REVIEWED_FINAL_BRANCH_AUDIT.json','Root review of all166 automatic TomeIII records','Final English one-model branch audit','Final structural page-marker and variant correspondence audit'],missing_part_evidence=missing_parts,records=records)
    (RECORDS/'EN_FINAL_DISPOSITIONS.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    table=[]
    for r in records:
        table.append(dict(id=r['id'],expose=r['expose'],page=r['page'],disposition=r['disposition'],english_parts=len(r['english_parts']),parts_with_placement_evidence=sum(p['placement_evidence_found'] for p in r['english_parts']),variant_ids='; '.join(r['variant_ids']),unsuccessful_attempts_retained_as_history=len(r['prior_unsuccessful_projection_history']),review_source=r.get('review_file',r['canonical_source']),reason=r.get('reason',r.get('coverage_basis',''))))
    write_tsv(RECORDS/'EN_FINAL_DISPOSITIONS.tsv',table,list(table[0]))
    print(json.dumps(dict(records=len(records),dispositions=dict(collections.Counter(r['disposition'] for r in records)),missing_part_evidence=missing_parts)))

if __name__=='__main__':main()
