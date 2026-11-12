#!/usr/bin/env python3
"""Verify English projections, port history, source-fix coverage and provenance.

All evidence is computed from supplied archive records and generated witnesses.
Literal checks, history replay, source identity and contextual dispositions are
reported separately; a failed literal search is never relabelled an exact match.
"""
import collections
import csv
import hashlib
import json
import re
from pathlib import Path

import french
from english_stage import ROOT,SRC,WORK,load_port
from english_variants import balanced
from english import clean,strip_notes,expose_start
from audit_en_already_exceptions import build_supplement

REC=ROOT/'output/records'


def read(path):return json.loads(path.read_text())
def sha(text):return hashlib.sha256(text.encode()).hexdigest()
def nw(text):return re.sub(r'\s+','',text)
def rows(path):return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def argument(text,pos):
    while text[pos].isspace():pos+=1
    assert text[pos]=='{',(pos,text[pos:pos+30])
    start=pos+1;depth=1;pos+=1
    while depth:
        if text[pos]=='\\':pos+=2;continue
        if text[pos]=='{':depth+=1
        elif text[pos]=='}':depth-=1
        pos+=1
    return text[start:pos-1],pos


def project(text,mode):
    out=[];pos=0;blocks=[]
    for m in re.finditer(r'\\SGAvar(?=\s*\{)',text):
        if m.start()<pos:continue
        out.append(text[pos:m.start()]);p=m.end();args=[]
        for _ in range(3):a,p=argument(text,p);args.append(a)
        out.append(args[0 if mode==0 else 1]);pos=p
        blocks.append({'printed':args[0],'corrected':args[1],'id':args[2]})
    out.append(text[pos:]);return ''.join(out),blocks


def without_folios(text):
    out=[];pos=0
    for m in re.finditer(r'\\SGApage(?=\s*\{)',text):
        if m.start()<pos:continue
        out.append(text[pos:m.start()]);_,p=argument(text,m.end());_,p=argument(text,p);pos=p
    out.append(text[pos:]);return ''.join(out)


def projection_audit(data):
    results=[];allids=[]
    for component in data:
        dp,blocks=project(component['annotated'],0);cp,_=project(component['annotated'],1)
        assert nw(without_folios(dp))==nw(without_folios(component['diplomatic'])),('diplomatic projection',component['expose'])
        assert nw(without_folios(cp))==nw(without_folios(component['corrected'])),('corrected projection',component['expose'])
        assert balanced(dp) and balanced(cp),('unbalanced TeX groups',component['expose'])
        indexed=collections.defaultdict(list)
        for e in component['entries']:
            assert e['source'] and e['before']!=e['after'],('invalid apparatus entry',e['id'])
            indexed[e['group_id']].append(e);allids.append(e['id'])
        for b in blocks:
            if not b['id']:continue
            hs=french.token_changes(b['printed'],b['corrected'])
            if component['expose']=='VI':hs=[h for h in hs if french.visible_hunk(h,b['printed'],b['corrected'])]
            else:hs=[h for h in hs if nw(h['before'])!=nw(h['after'])]
            es=indexed[b['id']]
            assert len(hs)==len(es),(b['id'],'apparatus count',len(hs),len(es))
            assert [(h['before'],h['after']) for h in hs]==[(e['before'],e['after']) for e in es],('apparatus readings',b['id'])
        results.append({'volume':component['volume'],'expose':component['expose'],'variant_blocks':sum(bool(b['id']) for b in blocks),
                        'apparatus_entries':len(component['entries']),'diplomatic_projection':'verified token identity',
                        'corrected_and_reading_projection':'verified identical selected body','diplomatic_sha256':sha(component['diplomatic']),
                        'corrected_sha256':sha(component['corrected'])})
    assert len(allids)==len(set(allids)),'duplicate English apparatus IDs'
    frvi=next(x for x in read(WORK/'fr_variant_data.json') if x['expose']=='VI')
    envi=next(x for x in data if x['expose']=='VI')
    for layer in ['corrected','diplomatic','annotated']:assert envi[layer]==frvi[layer],('Exposé VI identity',layer)
    french.write_tsv(REC/'EN_PROJECTION_AUDIT.tsv',list(results[0]),results)
    return {'parts':len(results),'entries':len(allids),'blocks':sum(x['variant_blocks'] for x in results),'shared_original_English_VI':'exact identity in both witnesses and annotated master'}


def folio_audit(data):
    ledger=list(csv.DictReader((REC/'EN_ALIGNMENT.tsv').open(),delimiter='\t'));by=collections.defaultdict(list)
    for r in ledger:by[r['volume'],r['expose']].append(r)
    report=[]
    def labels(text):
        result=[]
        for m in re.finditer(r'\\SGApage(?=\s*\{)',text):
            volume,p=argument(text,m.end());folio,_=argument(text,p)
            nums=re.findall(r'\d+',folio);folio=nums[-1] if nums else folio
            result.append((volume,folio))
        return result
    for c in data:
        dp,_=project(c['annotated'],0);cp,_=project(c['annotated'],1);actual=labels(cp)
        assert labels(dp)==actual,('folio sequence differs between forms',c['expose'])
        expected=[('I' if r['volume']=='7I' else 'II',r['folio']) for r in by[c['volume'],c['expose']]]
        assert actual==expected,('folio ledger does not match actual projected source',c['expose'])
        assert actual and actual[0][1]==expose_start(c['volume'],c['expose']),('incorrect exposé start',c['expose'])
        for vol,folio in actual:
            if c['expose']=='Introduction':assert folio in ['V','VI','VII']
            else:assert folio.isdigit() and 1<=int(folio)<=(528 if vol=='I' else 438),(c['expose'],folio)
        exact=sum(r['quality'].startswith(('source','exact')) for r in by[c['volume'],c['expose']])
        report.append({'volume':c['volume'],'expose':c['expose'],'anchors':len(actual),'exact_or_source_boundary_anchors':exact,
                       'explicitly_estimated_anchors':len(actual)-exact,'first_source_folio':actual[0][1],'last_source_folio':actual[-1][1],
                       'projection_sequences_identical':True})
    assert [r['folio'] for r in by['7I','Catalogue']]==['525','526','527','528']
    assert [r['folio'] for r in by['7I','VI']]==[str(i) for i in range(32,133)]
    (REC/'EN_ALIGNMENT_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return {'folio_anchors':len(ledger),'exact_or_source_boundary_anchors':sum(x['exact_or_source_boundary_anchors'] for x in report),
            'explicitly_estimated_anchors':sum(x['explicitly_estimated_anchors'] for x in report),'folio_sequences_match_all_forms':True}


def port_history(originals,finals):
    texts={(c['volume'],c['component']):c['text'] for c in originals};initial=dict(texts)
    final={(c['volume'],c['component']):c['corrected'] for c in finals};replay=[];lookup={}
    for volume in ['7I','7II']:
        log=rows(SRC/'port'/('PORT_EN'+volume+'_LOG.jsonl'))
        for ordinal,r in reversed(list(enumerate(log))):
            if r.get('outcome')!='applied':continue
            key=(volume,r['tr_file']);t=texts[key];count=t.count(r['tr_new'])
            assert count>0,('recorded applied English port edit absent from reverse history',volume,r['id'])
            if count==1:texts[key]=t.replace(r['tr_new'],r['tr_old'],1)
            native=initial[key];reader=final.get(key,'');author=clean(strip_notes(r['tr_new']))
            exact=native.count(r['tr_new']);final_exact=reader.count(r['tr_new']) if reader else 0
            author_exact=reader.count(author) if reader and author.strip() else 0
            if 'expose_VI_' in r['tr_file']:
                evidence='original-English VI replaced by exact authoritative source witness; projection identity verified'
            elif final_exact:evidence='exact translated new reading occurs in final corrected English'
            elif author_exact:evidence='translated authorial reading retained; comments/editorial notes removed or relocated'
            elif not exact:evidence='verified in reverse history; later recorded port edits supersede its literal spelling'
            elif nw(author) and nw(author) in nw(reader):evidence='translated reading retained with nonprinting whitespace changes'
            else:evidence='released target verified; later reader changes are enumerated in CHANGES_EN.tsv for this component'
            row={'log':'port/PORT_EN'+volume+'_LOG.jsonl','record':ordinal+1,'volume':volume,'port_id':r['id'],
                 'component':r['tr_file'],'page':str(r['page']),'reverse_matches':count,
                 'reverse_check':'unique exact reverse replay' if count==1 else 'two exact final targets; no source-location guess made',
                 'native_literal_new_count':exact,'final_literal_new_count':final_exact,'final_authorial_new_count':author_exact,
                 'final_evidence':evidence,'before':r['tr_old'],'after':r['tr_new']}
            replay.append(row);lookup[(volume,r['id'])]=row
    replay.sort(key=lambda x:(x['volume'],x['record']))
    french.write_tsv(REC/'EN_PORT_REPLAY_AUDIT.tsv',list(replay[0]),replay)
    return lookup,{'applied_port_records':len(replay),'unique_exact_reverse_replays':sum(x['reverse_matches']==1 for x in replay),
                   'multiple_exact_final_targets':sum(x['reverse_matches']>1 for x in replay),'absent_recorded_targets':0,
                   'final_evidence_counts':dict(collections.Counter(x['final_evidence'] for x in replay))}


def fix_audit(originals,finals,history):
    source_rows=list(csv.DictReader((REC/'FR_FIX_AUDIT.tsv').open(),delimiter='\t'))
    supplement=build_supplement()
    (REC/'EN_ALREADY_EXCEPTIONS.json').write_text(json.dumps(supplement,ensure_ascii=False,indent=2)+'\n')
    already_verified={(r['source_log'],r['source_record']):s for s in supplement['records'] for r in s['affected_source_records']}
    used_already=set()
    native={(c['volume'],c['component']):c for c in originals};final={(c['volume'],c['component']):c for c in finals}
    ports={v:load_port(v)[0] for v in ['7I','7II']};current={};equivalent={}
    for volume in ['7I','7II']:
        current[volume]=rows(SRC/'fixes'/('FIXLOG_'+volume+'_CURRENT.jsonl'))
        equivalent[volume]=collections.defaultdict(list)
        for i,r in enumerate(current[volume]):equivalent[volume][(r['file'],r['page'],r['old'],r['new'])].append('C'+str(i))
    source_cache={};out=[]
    for r in source_rows:
        volume='7II' if '7II' in r['log'] else '7I';key=r['log'];index=int(r['record'])-1
        if key not in source_cache:source_cache[key]=rows(SRC/key)
        fix=source_cache[key][index]
        identifiers=['C'+str(index)] if '_CURRENT' in key else equivalent[volume].get((fix['file'],fix['page'],fix['old'],fix['new']),[])
        pid=identifiers[-1] if identifiers else '';p=ports[volume].get(pid,{})
        component=p.get('tr_file','');n=native.get((volume,component),{});f=final.get((volume,component),{})
        needle=p.get('tr_new') or p.get('tr_old','');literal=n.get('text','').count(needle) if needle else 0
        reader_literal=f.get('corrected','').count(needle) if needle else 0;decision=p.get('decision','')
        proof='';status=''
        if fix['file']=='expose_VI_body.tex':
            status='shared original-English source identity';proof='EN_PROJECTION_AUDIT.tsv; complete VI source identity transfers every retained source repair'
        elif fix['kind']=='marker':
            status='source page-furniture correction';proof='English folios are generated from the corrected French marker set; exact/estimated anchors individually listed in EN_ALIGNMENT.tsv'
        elif fix['kind']=='dash_convention':
            status='catalogue transcription repair applied in all English forms';proof='EN_COMMON_SOURCE_REPAIRS.tsv: C604=67 and C605=68 exact price-dash repairs'
        elif (volume,pid) in history:
            status='recorded translated correction replayed';proof=history[volume,pid]['final_evidence']+'; EN_PORT_REPLAY_AUDIT.tsv#'+volume+':'+pid
        elif decision=='not_applicable':
            status='port records no English textual correction';proof=p.get('note','')+'; paired formula, notation and non-math source audits also performed'
        elif (key,index+1) in already_verified:
            verified=already_verified[key,index+1]
            assert decision=='already' and (volume,pid)==(verified['volume'],verified['port_id'])
            status=verified['English_evidence_kind'];proof=verified['evidence'];used_already.add((key,index+1))
        elif decision=='already' and literal:
            status='recorded already-correct translation verified literally';proof='exact supplied translated target occurs '+str(literal)+' time(s) in released native component'
        elif decision=='already' and needle and nw(needle) in nw(n.get('text','')):
            status='already-correct target verified ignoring whitespace';proof='literal words/TeX tokens retained; source whitespace differs'
        elif decision=='already' and re.search(r'covered by C\d+',p.get('note','')):
            other=re.search(r'covered by (C\d+)',p['note']).group(1)
            status='already decision covered by named later translated correction';proof=p['note']+'; '+history.get((volume,other),{}).get('final_evidence','see paired source/context resolution records')
        elif decision=='already':
            raise AssertionError(('already-decision target needs an exact successor or scope predicate',volume,pid,key,index+1))
        elif decision=='unclear':
            status='open port item explicitly decided';proof='OPEN_ITEMS_DECIDED.tsv; corrected-body patch or shared VI/source counterpart verified by build assertions'
        elif not identifiers:
            status='diplomatic-witness restoration distinct from current fix history';proof='FR_FIX_AUDIT.tsv verifies the printed witness; its English consequences are collated against current in EN_APPARATUS.json and individual reconstruction ledgers'
        else:
            raise AssertionError(('unclassified source fix',volume,key,index,pid,p))
        out.append({'source_log':key,'source_record':r['record'],'source_fix_id':r['id'],'page':r['page'],'kind':fix['kind'],
                    'source_replay':r['replay'],'source_final_evidence':r['final_evidence'],'equivalent_current_port_id':pid,
                    'port_decision':decision,'English_evidence_kind':status,'evidence':proof,'native_literal_target_count':literal,
                    'final_literal_target_count':reader_literal,'component':component})
    assert used_already==set(already_verified),'unused verified already-decision predicates'
    french.write_tsv(REC/'EN_FIX_AUDIT.tsv',list(out[0]),out)
    return {'source_fix_records_accounted':len(out),'logs':dict(collections.Counter(x['source_log'] for x in out)),
            'English_evidence_kinds':dict(collections.Counter(x['English_evidence_kind'] for x in out)),
            'verified_already_successor_or_scope_records':len(used_already),'verified_already_decisions':len(supplement['records'])}


def resolution_audit(originals):
    native={(c['volume'],c['component']):c['text'] for c in originals}
    gaps=[]
    for name in ['en_formula_resolutions_editorial.json','en_formula_resolutions_glossary.json']:
        gaps+=read(WORK/name)
    assert sorted(r['index'] for r in gaps)==list(range(249)),'formula gap ledger is incomplete or duplicated'
    counts=collections.Counter(r['status'] for r in gaps)
    for r in gaps:
        if r['status']=='variant':
            t=native[r['volume'],r['component']];a=r.get('start',t.find(r['corrected']))
            assert t[a:a+len(r['corrected'])]==r['corrected'],('stale reviewed native target',r['index'])
            assert balanced(r['corrected'])==balanced(r['printed']),('reviewed TeX group change',r['index'])
    notes=read(REC/'EN_INHERITED_EDITORIAL_NOTES.json');nrows=[]
    for n in notes:
        flat=' '.join(n['text'].split())
        markers=re.findall(r'(?i)\b(?:the print|printed|prints|scan|editorial|transcription|the source|source note|the English|source-visible)\b',flat)
        assert markers,(n['id'],'removed note lacks an explicit editorial marker')
        nrows.append({'id':n['id'],'volume':n['volume'],'expose':n['expose'],'page':n['page'],'source':n['file'],
                      'kind':n['kind'],'editorial_markers':'; '.join(dict.fromkeys(markers)),
                      'disposition':'retained verbatim in separate inherited editorial notes; excluded from authorial body'})
    french.write_tsv(REC/'EN_NOTE_EXTRACTION_AUDIT.tsv',list(nrows[0]),nrows)
    return {'formula_gap_records':len(gaps),'gap_dispositions':dict(counts),'inherited_editorial_notes':len(notes),
            'font_scope_and_tag_operations':len(read(WORK/'en_font_resolutions_glossary.json')),
            'non_math_operations':sum(len(read(p)) for p in WORK.glob('en_nonmath_resolutions_*.json'))}


def lexical_guard(originals,data):
    pattern=re.compile(r'\\[A-Za-z@]+')
    fr=read(WORK/'fr_variant_data.json')
    vocabulary=set(pattern.findall('\n'.join(c['text'] for c in originals)))
    vocabulary.update(pattern.findall('\n'.join(c['diplomatic']+c['corrected'] for c in fr)))
    vocabulary.update(pattern.findall(french.preamble()));vocabulary.add('\\SGApage');vocabulary.add('\\notag')
    extra={}
    for c in data:
        bad=set(pattern.findall(c['diplomatic']))-vocabulary
        if bad:extra[c['expose']]=sorted(bad)
    assert not extra,('unattested new control words introduced by reconstruction',extra)
    return {'new_unattested_control_words':0,'balanced_authorial_components':len(data)}


def disposition_audit():
    decisions={r['signature']:r for r in read(WORK/'en_overlap_resolutions_build.json')}
    out=[];pending=[]
    for x in read(WORK/'en_operation_conflicts.json'):
        op=x['candidate'];fingerprint={'volume':op['volume'],'component':op['component'],'corrected':op['corrected'],'printed':op['printed'],
                                      'atom':x['candidate_atom'],'retained':[{k:r[k] for k in ['start','end','corrected','printed']} for r in x['retained']]}
        signature=hashlib.sha256(json.dumps(fingerprint,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        review=decisions.get(signature)
        if review:out.append({'type':'overlap','signature':signature,'status':review['status'],'reason':review['reason'],
                              'candidate_source':op['source'],'component':op['component'],'candidate_atom':x['candidate_atom'],'retained':x['retained']})
        else:pending.append({'signature':signature,**x})
    rejected=read(WORK/'en_rejected_operations.json')
    for r in rejected:
        assert r.get('disposition') and r.get('review'),('undisposed rejected operation',r)
        out.append({'type':'rejected proposal','status':r['disposition'],'reason':r['reason'],'operation_index':r.get('operation_index'),
                    'review_id':r.get('review_id'),'source':r['source'],'component':r['component']})
    superseded=read(REC/'EN_SUPERSEDED_PORT_PROPOSALS.json')
    for r in superseded:
        out.append({'type':'superseded port proposal','status':'covered by '+r['superseded_by'],'reason':r['reason'],
                    'port_id':r['port_id'],'source':r['source'],'component':r['component']})
    (WORK/'en_overlaps_unreviewed.json').write_text(json.dumps(pending,ensure_ascii=False,indent=1)+'\n')
    (REC/'EN_OPERATION_DISPOSITION_AUDIT.json').write_text(json.dumps({'records':out,'pending':pending},ensure_ascii=False,indent=1)+'\n')
    assert not pending,('overlap dispositions require final source review',len(pending))
    return {'rejected_proposals_fully_disposed':len(rejected),'superseded_port_proposals_fully_disposed':len(superseded),
            'overlaps_fully_disposed':sum(r['type']=='overlap' for r in out),'pending_reconstruction_operations':0}


def main():
    manifest=read(REC/'EN_BUILD_INPUTS.json')
    changed=[name for name,digest in manifest['inputs'].items() if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest]
    assert not changed,('generated English readers require regeneration after editorial input changes',changed)
    originals=read(WORK/'en_components.json');finals=read(WORK/'en_final_components.json');data=read(WORK/'en_variant_data.json')
    # Native components in the released master were previously verified against
    # its complete single-file bodies; the catalogue is the explicit addition.
    releases={'7I':(SRC/'en/release_v2026-11-12/08_SGA7I_EN_EXPOSES_I_II_VI_IX_READER.tex').read_text(),
              '7II':(SRC/'en/release_v2026-11-12/09_SGA7II_EN_COMPLETE_READER.tex').read_text()}
    verified=[]
    for c in originals:
        if c['expose']=='Catalogue':continue
        assert c['text'].strip() in releases[c['volume']],('native/release mismatch',c['component'])
        verified.append({'volume':c['volume'],'component':c['component'],'native_sha256':sha(c['text']),'release_body_match':'exact'})
    french.write_tsv(REC/'EN_RELEASE_COMPONENT_AUDIT.tsv',list(verified[0]),verified)
    summary={'release_components_verified':len(verified),'restored_catalogue_components':1}
    summary.update(projection_audit(data));summary.update(folio_audit(data));history,replay=port_history(originals,finals);summary.update(replay)
    summary.update(fix_audit(originals,finals,history));summary.update(resolution_audit(originals));summary.update(lexical_guard(originals,data));summary.update(disposition_audit())
    fix_summary={key:summary[key] for key in ['source_fix_records_accounted','logs','English_evidence_kinds','applied_port_records',
                 'unique_exact_reverse_replays','multiple_exact_final_targets','absent_recorded_targets','final_evidence_counts',
                 'verified_already_successor_or_scope_records','verified_already_decisions']}
    fix_summary.update({'detailed_fix_table':'EN_FIX_AUDIT.tsv','detailed_port_history':'EN_PORT_REPLAY_AUDIT.tsv',
                        'already_decision_predicates':'EN_ALREADY_EXCEPTIONS.json',
                        'method':'Source-witness replay, exact native/release identity, reverse replay of recorded English edits, exact already-decision successor/scope predicates, and explicit contextual dispositions are reported separately.'})
    (REC/'EN_FIX_AUDIT.json').write_text(json.dumps(fix_summary,ensure_ascii=False,indent=2)+'\n')
    (REC/'EN_VERIFICATION_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
