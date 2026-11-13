"""Record an independent English-propagation review; do not edit Arcata sources.

Run from the project root. Witnesses are manually selected after reading the
English page text against the scan-verified French correction record. This is
not a second visual audit of the full Arcata scan. The two extra checks that
needed scan consultation are identified in the supplement.
"""
from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path('work/rapport_cycle')
AR = Path('work/arcata')

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def pages(folder):
    result = {}
    for path in sorted(folder.glob('*.tex')):
        text = path.read_text()
        chunks = re.split(r'\\PrintPage\{([^}]+)\}', text)
        for page, body in zip(chunks[1::2], chunks[2::2]):
            assert page not in result, (folder, page)
            result[page] = (str(path), body)
    return result

coverage = list(csv.DictReader((AR/'ACCEPTED_FIX_COVERAGE.tsv').open(), delimiter='\t'))
decisions = {r['id']:r for r in map(json.loads,(AR/'decisions.jsonl').read_text().splitlines())}
witness = json.loads((ROOT/'arcata_noedit_witnesses.json').read_text())
selected = [r for r in coverage
    if r['en_status']=='reviewed existing translation; no additional edit required'
    and decisions[r['id']]['kind'] in {'word','missing','number','punctuation','extra'}]
# Preserve the reviewed cohort after the parent replaces its generic status for
# a finding. This makes a post-patch rerun verify the same 147 source records.
cohort_ids = {'S45-SOL-'+i for i in witness}
selected = [r for r in coverage if r['id'] in cohort_ids]
assert len(selected) == len(witness) == 147
fr = pages(AR/'fr')
en = pages(AR/'en')
overrides = {
    '0199': ('I:5-2-4','2.3.1'),
    '0201': ('I:5-2-5','2.3.2'),
    '0204': ('I:5-2-4','2.3.1'),
    '0205': ('I:5-2-6','2.3.3'),
}
records=[]
for row in selected:
    sid=row['id']; short=sid[-4:]; p=row['page']; d=decisions[sid]
    enpath,body=en[p]; frpath,frbody=fr[p]
    expected=witness[short]
    present=norm(expected) in norm(body)
    record={
        'id':sid,'printed_page':p,'kind':d['kind'],'final_source_verdict':d['verdict'],
        'printed_reading_checked':d['printed_reading'],
        'fr_source':frpath,'fr_page_sha256':hashlib.sha256(frbody.encode()).hexdigest(),
        'en_source':enpath,'en_page_sha256':hashlib.sha256(body.encode()).hexdigest(),
        'english_witness':expected,'witness_present':present,
        'status':'verified existing English conveys the accepted printed reading',
        'review_scope':'independent semantic propagation review; exact witness checked in final page chunk',
    }
    if short in overrides:
        label,display=overrides[short]
        record['status']='presentation-only verification: printed local number retained; label-renaming proposal rejected'
        record['required_label_display']={'label':label,'display':display}
        record['compiled_number_evidence']='work/rapport_cycle/records/arcata_global_number_verification.json'
    if short=='0021':
        if not present:
            assert 'For example, let $X$ be a space and' in norm(body)
            record['status']='missing English hypothesis; exact supplementary patch supplied'
        else:
            record['status']='supplementary normal-space hypothesis now present in final English'
        assert 'espace normal et' in norm(frbody)
        record['french_witness']='espace normal et'
    else:
        assert present, (sid,p,expected)
    records.append(record)

out=ROOT/'records/arcata_noedit_review.json'
out.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
fields=['id','printed_page','kind','status','english_witness','witness_present','en_source','en_page_sha256','fr_source','fr_page_sha256']
with (ROOT/'records/arcata_noedit_review.tsv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore')
    w.writeheader(); w.writerows(records)
summary={
    'reviewed_rows':len(records),
    'exact_english_witnesses_present':sum(r['witness_present'] for r in records),
    'missing_hypothesis_rows':[r['id'] for r in records if not r['witness_present']],
    'presentation_only_number_rows':['S45-SOL-'+i for i in overrides],
    'compiled_number_verification':'work/rapport_cycle/records/arcata_global_number_verification.json',
    'other_kinds_not_reaudited':{'symbol':20,'accent':13,'formula':11},
    'method':'Manual semantic comparison of the historical cohort of 147 word/missing/number/punctuation/extra rows previously assigned the generic no-English-edit status. Witnesses are checked against final source pages. Four label-renaming proposals were subsequently rejected as presentation-only; their printed numbers are retained and verified in both compiled languages. This review supplements, and does not repeat, the primary visual scan audit.',
    'root_patch_instructions':'work/rapport_cycle/records/arcata_review_supplement.json'
}
(ROOT/'records/arcata_noedit_review_status.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
