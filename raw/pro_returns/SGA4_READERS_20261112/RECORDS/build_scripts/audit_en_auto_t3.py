"""Record the inspected automatic Tome III candidate review and final links."""
import collections,hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'output/records';SHARED=ROOT/'output/shared'

def main():
    original=json.loads((SHARED/'EN_T3_AUTOMATIC_REVIEW_INPUT.json').read_text())
    repairs={r['id']:r for r in json.loads((SHARED/'EN_T3_AUTO_REPAIR_PAIRS.json').read_text())}
    variants=json.loads((REC/'EN_VARIANTS.json').read_text())
    audits=json.loads((REC/'EN_SOURCE_AUDIT.json').read_text())
    canonical=json.loads((ROOT/'sources/fixes/MISPRINTS_4.json').read_text())
    master=(ROOT/'output/en/SGA4_EN_annotated_master.tex').read_bytes()
    rows=[]
    for prior in original:
        ident=prior['id'];source=canonical[int(ident[2:])-1]
        reviewed=repairs.get(ident)
        outcome=('explicit common English reading' if reviewed and reviewed['assessment'].lower().startswith('no')
                 else 'bounded English replacement supplied' if reviewed
                 else 'inspected automatic pair retained')
        current=[r for r in audits if r['id']==ident]
        linked=[dict(id=v['id'],source=v['source'],printed=v['printed'],corrected=v['corrected'],
                     expose=v['expose'],page=v['page']) for v in variants if ident in v['source'].split('; ')]
        rows.append(dict(id=ident,expose=source['expose'],page=source['page'],place=source['where'],
          canonical_printed=source['print'],canonical_corrected=source['correct'],
          review_outcome=outcome,
          review_method='Read the canonical French record and the English occurrence at the supplied folio, including neighboring repeated formulas. Candidate IDs were matched by their literal paired strings; historical EN-V numbering was not used as a location key.',
          prior_candidate_pairs=[dict(printed=v['printed'],corrected=v['corrected']) for v in prior.get('variants',[])],
          reviewed_input=reviewed,final_variant_links=linked,final_audit_rows=current,
          final_assessment_present=any(r['status'] in ['paired','represented by existing variant','no English impact'] for r in current)))
    payload=dict(master_sha256=hashlib.sha256(master).hexdigest(),reviewed_ids=len(rows),
      outcome_counts=dict(collections.Counter(r['review_outcome'] for r in rows)),
      all_final_assessments_present=all(r['final_assessment_present'] for r in rows),rows=rows)
    (REC/'EN_T3_AUTOMATIC_REVIEW.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print('Automatic T3 reviewed IDs:',len(rows),payload['outcome_counts'],
      'final assessments',sum(r['final_assessment_present'] for r in rows))

if __name__=='__main__':main()
