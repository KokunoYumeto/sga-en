"""Produce the shared decision register and deferred-port crosswalk.

All source references are paths inside the supplied archives. Run again after
the language builders to refresh their edition-decision counts.
"""
import collections,csv,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
csv.field_size_limit(100_000_000)
REC=ROOT/'output/records'
SHARED=ROOT/'output/shared'

def read(path):return json.loads((ROOT/path).read_text())
def write_tsv(path,rows,fields):
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow({k:str(v).replace('\t',' ').replace('\r','').replace('\n',r'\n') for k,v in row.items()})

def decisions():
    rows=[]
    for r in read('output/records/FR_EDITION_DECISIONS.json'):
        rows.append(dict(id=r['id'],page=r.get('page',''),place=r.get('file','edition'),
          printed=r.get('before',''),corrected=r.get('after',''),decision=r['decision'],
          reason=('Exact occurrence counts: '+json.dumps(r['counts'],sort_keys=True)) if r.get('counts') else '',
          source=r.get('source','method/GLOBAL_ISSUES_SGA.md')))
    variant_path=REC/'FR_VARIANTS.json'
    variants={r['id']:r for r in json.loads(variant_path.read_text())} if variant_path.exists() else {}
    changes_path=REC/'CHANGES_FR.tsv'
    changes={r['id']:r for r in csv.DictReader(changes_path.open(),delimiter='\t')} if changes_path.exists() else {}
    source_decisions=REC/'FR_SOURCE_DECISIONS.json'
    for r in json.loads(source_decisions.read_text()) if source_decisions.exists() else []:
        change=changes.get(r['variant'])
        variant=variants.get(r['variant']) or dict(place=change['place'],printed=change['before'],corrected=change['after'])
        decision=r['decision'] if not change else 'Record this exact source-comparison change in the generated corrected reader.'
        evidence='Exact paired source-of-record span; variant '+r['variant']+'.' if not change else 'Exact before/after span in CHANGES_FR.tsv; comparison '+change['comparison']+'; row '+change['id']+'.'
        rows.append(dict(id=r['id'],page=f"{r['expose']} {r['page']}",place=variant['place'],
          printed=variant['printed'],corrected=variant['corrected'],decision=decision,
          reason=evidence,source=r['source']))
    for r in read('output/shared/held_apparatus_decisions.json'):
        rows.append(dict(id=r['id'],page=f"t{r['tome']} {r['expose']} {r['page']}",place=r['place'],
          printed='',corrected='',decision=r['decision'],reason=r['reason'],source=r['source']+'; '+r['item']))
    rows.extend([
      dict(id='DEC-C293',page='t2 V 78',place='Proposition 8.2.6; target slice',
        printed=r'\Ss/V',corrected=r'\Ss/U',
        decision='Retain V in the diplomatic branch and U in both corrected branches; the released English U already has the accepted mathematical reading.',
        reason=r'C293 repairs the site-symbol s to \Ss. MP0355 independently records the printed denominator V as a misprint for U. With p^*:S→T, U∈S, V∈T and φ:V→p^*U, the induced inverse-image functor sends (W→U) to (V×_{p^*U}p^*W→V), so its source is S/U and its target T/V. The corresponding morphism of sites goes from T/V to S/U.',
        source='en/F_port_20261112/FINAL_4.json#C293; fixes/MISPRINTS_4.json#MP0355'),
      dict(id='DEC-MP-RECORD-SCOPE',page='all',place='930 agreed misprint records',printed='',corrected='',
        decision='Use the top-level print/correct/tex_did fields as the canonical agreed item. Nested model quotations provide location and reasoning evidence.',
        reason='Nested model readings sometimes concern neighboring formulas or a different span. They are not automatically additional authorized changes. Exact local source pairs record any adaptation to an existing human correction; independent source corrections remain intact.',
        source='fixes/MISPRINTS_4.json; build_scripts/review_t3.py; build_scripts/fr_manual.py'),
      dict(id='DEC-MP0582',page='t3 X 50',place='Proof of Corollary 2.4',printed='a corps des fractions',corrected='de corps des fractions',
        decision='Retain Orgogozo’s existing correction de and the unchanged human record sisi{a}{de}.',
        reason='The top-level and Opus proposal is à; Sol explicitly proposes de. Both de corps des fractions K and à corps des fractions K express the relation that K is the field of fractions of A. E already corrects the printed a through the human record, so no replacement of that correction is needed.',
        source='fixes/MISPRINTS_4.json#MP0582; fr/E_corrected_after_scan_check/10/10.tex'),
      dict(id='DEC-MP0831',page='t3 XVIII 495',place='Lemma 1.2.6',printed=r'\Psi(\lambda v):\varphi(\lambda)\Psi(v)',corrected=r'\Psi(\lambda v)=\Psi(v)\varphi(\lambda)',
        decision='Repair the colon to an equality; retain the independent factor order already corrected in E and its human record.',
        reason='The new agreed misprint concerns the colon. Applying it as a local delta preserves E’s pre-existing human factor-order correction.',
        source='fixes/MISPRINTS_4.json#MP0831; fr/E_corrected_after_scan_check/18/18.tex'),
      dict(id='DEC-MP0878',page='t3 XVIII 557',place='Proof involving (Var 3)',printed='Il est immédiatement, grâce à (Var 3)',corrected='Il est immédiatement clair, grâce à (Var 3)',
        decision='Retain the complete corrected construction already in E.',
        reason='The misprint is an incomplete construction after est. E supplies clair. The model alternative immédiat repairs the same omission without requiring replacement of the valid human correction immédiatement clair.',
        source='fixes/MISPRINTS_4.json#MP0878; fr/E_corrected_after_scan_check/18/18.tex'),
      dict(id='DEC-PORT-COUNTS',page='all',place='English port of 12 November 2026',printed='',corrected='',
        decision='Distinguish the 157 applied C records from the total 159 apply decisions.',
        reason='PORT_EN4_LOG has 583 decisions: 159 apply (157 C and H33,H39), 155 already (135 C,20 H), 269 not-applicable (257 C,12 H). FINAL_4 has 898 rows:549 final,293 app_check,56 not_in_current. The 293 deferred C records are listed separately from the 22 by-hand replays on disputed pages.',
        source='en/F_port_20261112/PORT_EN4_LOG.jsonl; en/F_port_20261112/FINAL_4.json'),
      dict(id='DEC-DISPUTE-BOUNDARY',page='443 supplied pages',place='643 unresolved items',printed='',corrected='',
        decision='Retain the agreed source text and carry every unresolved item into the corrected-form dossier; no scan-dependent choice is made.',
        reason='Accepted mathematical or linguistic judgments remain deferred for application when they lie on a supplied disputed page. Existing agreed source corrections and existing human editorial records remain.',
        source='api_pass_20261111/PAGES_FOR_APP_CHECK.json; output/records/DISPUTED_PLACES.tsv'),
      dict(id='DEC-PAGE-TOKEN-MAPPING',page='all',place='Text replacements spanning printed-page markers',printed='',corrected='',
        decision='Keep markers at their mapped unchanged-character boundary within an exact replacement.',
        reason='marker_projection.py removes marker tokens, constructs the explicit equal-character/boundary correspondence, and reinserts them at that boundary. A marker inside an unequal interior without such a boundary requires a reviewed placement. It is never appended arbitrarily to the end of a replacement.',
        source='build_scripts/marker_projection.py; api_pass_20261111/PAGES.json'),
      dict(id='DEC-EN-MACRON',page='all',place='Combining macron encoding in English source',
        printed='base character followed by U+0304',corrected=r'\bar{base character}',
        decision='Encode the same base character and its overbar by the corresponding TeX math accent.',
        reason='The replacement is restricted to the observed base-plus-combining-mark sequences; the base character is retained exactly. The build event ledger records every occurrence.',
        source='build_scripts/build_en.py; output/records/EN_BUILD_EVENTS.tsv'),
      dict(id='DEC-SHARED-UNICODE',page='appendices',place='Literal transcription of record text in bilingual appendices',
        printed='Recorded Unicode mathematical symbols and combining accents',corrected='The explicit TeX equivalents listed in shared_records.py',
        decision='Use the exact symbol dictionary and base-plus-accent mappings when printing the supplied record text; retain U+2972 and U+223F directly in the math font.',
        reason='The source strings remain in the machine-readable ledgers. Every replacement is specified character by character in tex() and MATH_CHARS; final compile logs are checked for missing characters.',
        source='build_scripts/shared_records.py; output/records/COMPILE_STATUS.json'),
    ])
    fr_change_decisions=REC/'FR_CHANGE_DECISIONS.json'
    for r in json.loads(fr_change_decisions.read_text()) if fr_change_decisions.exists() else []:
        rows.append(dict(id=r['id'],page=r.get('page','all'),place=r.get('place','French reader construction'),
          printed=r.get('before',''),corrected=r.get('after',''),decision=r['decision'],
          reason=r.get('reason','All 42 complete-body/source comparisons have exact forward, inverse and serialized-TSV reconstruction checks.'),
          source=r.get('source','build_scripts/fr_changes_audit.py; output/records/CHANGES_FR.tsv; output/records/FR_CHANGE_AUDIT.json')))
    by_id={r['id']:r for r in rows}
    en_decisions=REC/'EN_CHANGE_DECISIONS.json'
    for r in json.loads(en_decisions.read_text()) if en_decisions.exists() else []:
        if r['id'] in by_id:continue
        row=dict(id=r['id'],page=r.get('page','all'),place=r.get('place','English reader construction'),
          printed=r.get('before',''),corrected=r.get('after',''),decision=r['decision'],
          reason=r.get('reason','Complete-source comparison and reconstruction checks are in the English change-log audit.'),
          source=r.get('source','build_scripts/en_changes.py; output/records/CHANGES_EN.tsv'))
        rows.append(row);by_id[row['id']]=row
    notation=REC/'EN_NOTATION_DECISIONS.json'
    for r in json.loads(notation.read_text()) if notation.exists() else []:
        evidence='English occurrence evidence: '+json.dumps(r,ensure_ascii=False,sort_keys=True)
        if r['id'] in by_id:by_id[r['id']]['reason']+=' '+evidence
        else:
            row=dict(id=r['id'],page=r.get('scope','all'),place='English notation projection',
              printed=r.get('before',''),corrected=r.get('after',''),
              decision='Apply the recorded printed-notation mapping in both selected English bodies.',
              reason=evidence,source='method/GLOBAL_ISSUES_SGA.md; output/records/EN_NOTATION_DECISIONS.json')
            rows.append(row);by_id[row['id']]=row
    scope=REC/'OM_1326_SCOPE_DECISION.json'
    if scope.exists():
        r=json.loads(scope.read_text())
        rows.append(dict(id=r['id'],page=f"{r['expose']} {r['page']}",place=r['extended_scope'],
          printed=r['printed'],corrected=r['corrected'],decision=r['kind'],reason=r['proof'],source=r['source']))
    write_tsv(REC/'DECISIONS.tsv',rows,['id','page','place','printed','corrected','decision','reason','source'])
    return rows

def deferred():
    final=read('sources/en/F_port_20261112/FINAL_4.json')
    disputes=read('output/shared/disputes_index.json')
    bypage=collections.defaultdict(list)
    for r in disputes:bypage[(r['file'],int(r['page']))].append(r['id'])
    rows=[]
    for r in final:
        if r['status']!='app_check':continue
        rows.append(dict(id=r['id'],expose=r['expose'],page=r['page'],kind=r['kind'],
           before=r['old'],after=r['new'],status='deferred; no new English application',
           disputed_items='; '.join(bypage[(r['file'],int(r['page']))]),
           source='en/F_port_20261112/FINAL_4.json#'+r['id']))
    assert len(rows)==293,len(rows)
    write_tsv(REC/'EN_DEFERRED_FRENCH_FIXES.tsv',rows,['id','expose','page','kind','before','after','status','disputed_items','source'])
    return rows

if __name__=='__main__':
    print('Decision rows',len(decisions()),'deferred C records',len(deferred()))
