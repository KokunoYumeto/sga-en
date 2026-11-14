#!/usr/bin/env python3
"""Index existing retention decisions without adding a source or math verdict."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SPECS=[
 ('expose_ii','ASTRA-II-AUTHOR-CLAIM-206',[206],'Corollary 2.3: general Hom-sheaf softness and restriction assertion','review/expose_ii/author_claim_issue_206.json'),
 ('expose_ii','ASTRA-II-AUTHOR-CLAIM-207',[207],'Corollary 2.3: proof specializations continuing the preceding assertion','review/expose_ii/author_claim_issue_206.json'),
 ('expose_iii','ASTRA-III-AUTHOR-CLAIM-244',[244,245],'Proposition 3.5(a): cohomology interval and its proof','review/expose_iii/author_claim_244_245.json'),
 ('expose_iii','ASTRA-III-STALK-CLAIM-244',[244,245],'Product-stalk equalities and ensuing derived comparison','review/expose_iii/author_claim_244_245.json'),
 ('expose_iii','ASTRA-III-AUTHOR-CLAIM-256',[256,257],'Proposition 4.7(a): cohomology bound and boundedness; proof reference',None),
 ('expose_iv','ASTRA-IV-AUTHOR-CLAIM-295',[295],'3.3.3: first category pairing and its first induced group map','review/expose_iv/author_claim_issue_295.json'),
 ('expose_v','ASTRA-V-AUTHOR-CLAIM-336',[336],'Proposition 4.12: printed finite-tail filtration formula','review/expose_v/author_claim_issue_336.json'),
 ('expose_v','ASTRA-V-AUTHOR-CLAIM-337',[337],'Remarks 4.13 and a cited proof step of Corollary 4.14','review/expose_v/author_claim_issue_337.json'),
 ('expose_v','ASTRA-V-AUTHOR-CLAIM-338',[338],'Corollary 4.15: intermediate equality; stated identification separately verified','review/expose_v/author_claim_issue_338.json'),
 ('expose_v','ASTRA-V-AUTHOR-CLAIM-339',[338,339],'Full-domain injectivity sentence; restricted argument and divisibility lemma separately verified','review/expose_v/author_claim_issue_339.json'),
 ('expose_v','ASTRA-V-UNIT-CLAIM-341',[341],'Prose after 5.5.1 concerning absence of a unit; unitization separately verified','review/expose_v/identification_341.json'),
 ('expose_v','ASTRA-V-AUTHOR-CLAIM-343',[343],'Proposition 5.7 and its final augmentation/filtration transport','review/expose_v/author_claim_issue_343.json'),
 ('expose_v','ASTRA-V-LOCAL-CALCULATION-343',[343],'Second proof display: literal sign and prime calculation','review/expose_v/author_claim_issue_343.json'),
 ('expose_v','ASTRA-V-LAMBDA-EVALUATION-352',[352],'Full-series evaluation notation in the proof; finite Corollary 6.6.2 separately verified','review/expose_v/identification_352.json'),
 ('expose_v','ASTRA-V-COEFFICIENT-355',[354,355],'6.9 proof coefficient shorthand; leading-degree interpretation and conclusion separately verified','review/expose_v/identification_355.json'),
 ('expose_v','ASTRA-V-AUTHOR-CLAIM-355',[355],'Proposition 6.10 statement','review/expose_v/author_claim_issue_355.json'),
 ('expose_v','ASTRA-V-AUTHOR-CLAIM-CONTINUATION-356',[356],'Final 6.10 specialization and filtration-compatibility assertion','review/expose_v/author_claim_issue_355.json'),
]


def main():
    rows=[]
    for folder,sid,loci,label,proof in SPECS:
        path=ROOT/'review'/folder/'own_findings.jsonl'
        matches=[]
        for number,line in enumerate(path.read_text().splitlines(),1):
            record=json.loads(line)
            if record.get('source_id')==sid:
                matches.append((number,line,record))
        assert len(matches)==1,sid
        number,line,record=matches[0]
        assert record.get('kind') in ['author_claim','author_claim_issue'],sid
        assert 'retain' in ' '.join(str(record.get(k,'')) for k in ['verdict','change','tex']).lower(),sid
        if proof:
            assert (ROOT/proof).is_file(),proof
        rows.append(dict(source_id=sid,loci=loci,scope_label=label,
            original_decision=path.relative_to(ROOT).as_posix()+f'#{number}',
            original_decision_line_sha256=hashlib.sha256(line.encode()).hexdigest(),
            proof_packet=proof,verdict=record['verdict'],
            printed_reading=record['printed_reading'],editorial_disposition=record['change'],
            original_reason_verbatim=record['reason'],image=record.get('image'),
            supplemental_images=record.get('supplemental_images',[]),region=record.get('region'),
            new_scan_claim=False,new_mathematical_claim=False))
    packet=dict(record_type='additional_retained_passage_index',
        scope='Existing author-claim and proof-step retention decisions in II, III, IV and V, additional to the selected final-disposition examples on 431,443,464–465 and590–592. This bounded index does not claim to enumerate every possible defect in the book.',
        records=len(rows),distinct_decision_ids=len({r['source_id'] for r in rows}),
        coverage_loci=sorted({p for r in rows for p in r['loci']}),
        source_text_changed=False,source_verdicts_changed=False,
        interpretation='Retained statements and retained proof steps have distinct scopes. Several records explicitly verify a stated conclusion independently while identifying a defect only in an intermediate equality, domain, coefficient shorthand or evaluation. The original reasons below preserve those distinctions.',
        entries=rows)
    (HERE/'ADDITIONAL_RETAINED_PASSAGES.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
    (HERE/'ADDITIONAL_RETAINED_PASSAGES.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    lines=['# Additional retained source passages','',packet['scope'],'',packet['interpretation'],'',
        '| Printed loci | Scope | Existing decision | Proof packet |','|---|---|---|---|']
    for row in rows:
        lines.append('| '+', '.join(map(str,row['loci']))+' | '+row['scope_label']+' | `'+row['original_decision']+'` | '+('`'+row['proof_packet']+'`' if row['proof_packet'] else 'Complete calculation in the cited decision row')+' |')
    lines+=['','The JSON and JSONL preserve the source IDs, original verdicts, original reasons verbatim, image references, exact source-row hashes and separate proof-packet paths. This index adds no mathematical verdict and changes no source passage.','']
    (HERE/'ADDITIONAL_RETAINED_PASSAGES.md').write_text('\n'.join(lines))
    print(json.dumps(dict(records=len(rows),coverage_loci=packet['coverage_loci'],path='review/final_readme_audit/ADDITIONAL_RETAINED_PASSAGES.json')))


if __name__=='__main__':
    main()
