#!/usr/bin/env python3
"""Audit the captured220 classifications and emit metadata-only supplements."""
from pathlib import Path
import collections,csv,hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
INPUT=HERE/'input_snapshots'
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def put(name,value):(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def jsonl(name,rows):(HERE/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
cache={}
def decision(path,sid):
    if path not in cache:
        cache[path]=[(i,json.loads(line),digest(line)) for i,line in enumerate((ROOT/path).read_text().splitlines(),1) if line.strip()]
    found=[r for r in cache[path] if r[1].get('source_id',r[1].get('id'))==sid]
    assert len(found)==1,(path,sid,len(found))
    return found[0]
classified=json.loads((INPUT/'ADDITIONAL_MISPRINT_CLASSIFICATION.json').read_text())['records']
assert len(classified)==220
table=list(csv.DictReader((INPUT/'MISPRINTS_6_DECIDED.tsv').open(),delimiter='\t'))
bytable=collections.defaultdict(list)
for r in table:bytable[r['id']].append(r)
variants=json.loads((INPUT/'FR_VARIANTS.json').read_text())
byvariant=collections.defaultdict(list)
for r in variants:
    for sid in r['source']:byvariant[sid].append(r)
checked=[];issues=[];originals={}
for entry in classified:
    sid=entry['id'];path=entry['review_file'];line,d,sha=decision(path,sid);originals[sid]=dict(path=path,line=line,sha256=sha,record=d)
    for key in ['image','reason','region','printed_reading']:
        if not d.get(key):issues.append(dict(source_id=sid,issue='missing source '+key))
    if d.get('is_misprint') is False or str(d.get('verdict','')).startswith(('reverted','rejected','pending')):
        issues.append(dict(source_id=sid,issue='excluded disposition included'))
    if len(bytable[sid])!=1:issues.append(dict(source_id=sid,issue='TSV multiplicity',count=len(bytable[sid])))
    if bytable[sid]:
        for key in ['verdict','printed_reading','image','region','reason']:
            if bytable[sid][0][key]!=str(d.get(key,'')):issues.append(dict(source_id=sid,issue='TSV/source mismatch',field=key))
    if str(entry['page'])!=str(d.get('page')):issues.append(dict(source_id=sid,issue='classification/source page mismatch'))
    refs=re.findall(r'(scan/[^;\s]+\.(?:pdf|djvu))#page=(\d+)',str(d.get('image','')))
    for rel,page in refs:
        limit=720 if rel.endswith('.pdf') else 711
        if not (ROOT/rel).exists() or not 1<=int(page)<=limit:issues.append(dict(source_id=sid,issue='invalid scan reference',reference=rel+'#page='+page))
    checked.append(dict(source_id=sid,page=entry['page'],original_decision_path=path,original_decision_line=line,original_decision_sha256=sha,source_evidence_fields_present=all(d.get(k) for k in ['image','reason','region','printed_reading']),matching_tsv_rows=len(bytable[sid]),direct_final_variant_ids=[v['id'] for v in byvariant[sid]],classification_basis=entry['classification_basis'],verdict=d['verdict']))
assert not issues,issues

# This list is entered only after reading each complete source reason and its
# actual final literal pair. It is not derived from a branch difference.
selected={
 'ASTRA-EARLY-0004':('misprint_in_print','The existing decision identifies the printed r and the required déduit through the actual associated-graded projection map; this is an accepted lexical source correction.'),
 'ASTRA-EARLY-0011':('reference_misprint','The existing decision identifies the representation-ring theorem1.1 on26–27 and the different numbered proposition1.3 on32; the accepted source locator correction is missing from the table.'),
 'ASTRA-EARLY-0012':('mathematical_source_correction','Coefficient extraction in(1+t)^(n−1) lambda_t gives lambda^(n−i); the recorded n=1 value independently contradicts the printed exponent. This is an established source formula correction.'),
 'ASTRA-EARLY-0013':('mathematical_source_correction','The same quantified assertion includes the component formula with(j−1)! and the positive-degree multiplication map; the accepted bound repair is a source-domain correction.'),
 'ASTRA-EARLY-0014':('mathematical_source_correction','The defined C-tilde target and the explicit coefficientwise pullback [n,1+sum a_i]→[n,1+sum f-star(a_i)] establish the two omitted target tildes as source corrections.'),
 'ASTRA-EARLY-0015':('reference_misprint','The recorded direct comparison identifies example1 as the definition of K(G) from representations; the printed example2 locator is explicitly corrected.'),
 'ASTRA-EARLY-0016':('mathematical_source_correction','The recorded restriction j^! sends the global gamma(Y) to the local gamma(D), so the two global arguments are explicitly corrected to Y. The unrelated surplus parenthesis has its own inherited MISPRINTS row and does not classify this argument correction.'),
 'ASTRA-EARLY-0017':('mathematical_source_correction','The support-filtration definition and localization map identify the stated condition with membership in K(X)^i, hence filtration at least i; the accepted reversed inequality is a source error.'),
 'ASTRA-EARLY-0018':('mathematical_source_correction','The actual C-tilde lambda-homomorphism and its associated-graded map have the recorded A-tilde target; the omitted target tilde is explicitly corrected.'),
 'ASTRA-EARLY-0019':('reference_misprint','Taking associated-graded classes in(iii) gives exactly(iii bis), while(ii) gives(ii bis); the recorded map proves the accepted first numeral repair.'),
 'ASTRA-EARLY-0020':('mathematical_source_correction','The recorded pushforward computation is i_*i^*(delta)=i_*(1)delta=xi-prime delta on X. It forces the accepted annihilating factor in the stated operation.'),
 'ASTRA-EARLY-0021':('mathematical_source_correction','The defined Grothendieck-group pushforward has lower shriek and supplies the argument of ch_X. The recorded Chow-valued left star stays unchanged; the single right-hand symbol is explicitly corrected.'),
 'ASTRA-EARLY-TYPE-016':('misprint_in_print','The exact same KÜnneth/Künneth pair is explicitly classified misprint_in_print in check/findings/findings_071_075.json#34 and is already in MISPRINTS#115 for75. The same image-backed decision expressly extends that orthographic correction to70; its generic typography_observation field must not hide the separate70 occurrence.'),
 'ASTRA-EARLY-0022':('mathematical_source_correction','The source explicitly defines G→f_*(G) and then derives R^p f_*; the recorded underlying sheaf functor has the omitted lower star. This is the accepted source functor-name repair.'),
 'ASTRA-V-SLASH-PRODUCT-360':('mathematical_source_correction','The recorded calculation differentiates ab and multiplies by(ab)^−1, forcing the entire product denominator. The supplied x=y=1 computation gives2/(1+t), whereas the successively evaluated ungrouped slash gives2(1+t). Classify this accepted formula-delimiter omission from that explicit calculation; do not extend it to the four records expressly declared notation conventions.'),
 'ASTRA-V-POLYNOMES-361':('misprint_in_print','The decision records two bare-o source spellings and expressly supplies the missing circumflex in the same noun polynôme. The coefficient maps are unchanged. Both final literal accent corrections belong to this source-error record.'),
 'ASTRA-V-COEFFICIENT-363':('mathematical_source_correction','The recorded Phi definition requires(-1)^(k−1) coefficient extraction. At k=2 the unsigned coefficient is−X² while Phi²(1+Xt)=X²; the accepted sign restoration is a source error independent of its accompanying denominator grouping.'),
 'ASTRA-X-0064':('reference_misprint','The source decision gives the exact Pic-tau specialization of Proposition2.4.4 yielding the claimed Pic-tau→Pic-N inclusion; the printed2.3.4 locator is explicitly corrected.'),
 'ASTRA-X-0106':('reference_misprint','The source decision identifies Corollary1.1.4 and the exact additive generator map used in7.4. The accepted missing internal stop in1.14 is a source locator error.'),
 'ASTRA-X-0117':('misprint_in_print','The recorded restricted object is the feminine cohomology class, with exact pullbacks to the two fibers; the accepted tel→telle repair is a source agreement error.'),
 'ASTRA-X-0118':('reference_misprint','The recorded cycle-class homomorphism proves the implication from the conjecture7.12.5, while the printed7.11.5 is the quotient construction. The accepted locator repair is a source error.'),
 'ASTRA-X-0119':('misprint_in_print','The decision records the source singular inverse, its plural antecedent images and the same page’s correctly plural parallel expression. The accepted final-s repair is a source agreement error.')
}
assert len(selected)==22
missing={}
for v in variants:
    for d in v['source_decisions']:
        sid=d['source_id']
        if sid.startswith('ASTRA') and sid not in bytable:missing.setdefault(sid,d)
assert len(missing)==77 and set(selected)<=set(missing)
supplement=[]
for sid,(kind,why) in selected.items():
    path=missing[sid]['review_file'];line,d,sha=decision(path,sid)
    assert d.get('is_misprint') is not False and not d['verdict'].startswith(('reverted','rejected','pending'))
    assert d.get('image') and d.get('reason') and d.get('region')
    refs=[path+'#'+str(line),str(d['image'])]
    for key in ['witness','witness_image']:
        if d.get(key):refs.append(str(d[key]))
    refs.extend(d.get('additional_evidence',[]))
    if sid=='ASTRA-EARLY-TYPE-016':refs.extend(['check/findings/findings_071_075.json#34','fixes/MISPRINTS_6.json#115'])
    pairs=[{k:v[k] for k in ['id','page','printed','corrected','source','sha256_printed','sha256_corrected']} for v in byvariant[sid]]
    r=dict(record_type='supplemental_source_error_classification',source_id=sid,page=d['page'],is_misprint=True,source_error_kind=kind,classification_basis='Independent explicit classification of the existing accepted source correction after reading its full image-backed decision and exact final literal pair; the original generic metadata did not express this source-error category.',reason=why,original_decision_path=path,original_decision_line=line,original_decision_sha256=sha,original_kind=d.get('kind',''),original_record_type=d.get('record_type',''),original_verdict=d['verdict'],image=d['image'],region=d['region'],underlying_source_reason=d['reason'],evidence_refs=refs,final_literal_variants=pairs,correction_status='Accepted paired correction already present in final literals; this supplement changes classification metadata only.',scope='No source reading,patch,current/diplomatic text,or frozen checkpoint is changed.')
    supplement.append(r);originals[sid]=dict(path=path,line=line,sha256=sha,record=d)
jsonl('SUPPLEMENTAL_SOURCE_ERROR_CLASSIFICATIONS.jsonl',supplement)
excluded=[]
notation={'ASTRA-V-SUBSTITUTION-325','ASTRA-V-SUBSTITUTION-326','ASTRA-V-UNIT-DENOMINATOR-327','ASTRA-V-SLASH-329'}
for sid,d in missing.items():
    if sid in selected:continue
    if sid in notation:
        why='The source record explicitly declares a notation/substitution grouping convention and proves the same substitution map and inverse. Preserve that stated classification; a current/diplomatic difference alone does not promote it to a source error.'
    elif sid=='ASTRA-X-0015':
        why='The source prints an ellipsis placeholder and the decision expressly supplies a reference completion. Its projection-formula specialization is verified, but the decision does not assert an erroneous printed locator. Retain the declared reference-completion category.'
    else:
        assert d.get('kind') in ['font','font_convention'],(sid,d.get('kind'))
        why='The source record supplies an occurrence-scoped glyph/notation transport, with the identical object or functor identified, or an accompanying both-form glyph restoration. It does not assert a source error for this record. Separately classified omitted rules remain under their own explicit source-error IDs.'
    excluded.append(dict(source_id=sid,page=d['page'],source_kind=d.get('kind'),decision='Not added to the source-error table by this audit',reason=why,original_decision_path=d['review_file'],source_reason=d['reason'],final_variant_ids=[v['id'] for v in byvariant[sid]]))
assert len(excluded)==55
put('EXCLUDED_BRANCH_DIFFERENCES.json',excluded)
bad=next(v for v in variants if v['id']=='FRV0485')
right=next(v for v in variants if v['id']=='FRV0495')
assert bad['printed']==right['printed']=='3' and bad['corrected']==right['corrected']=='4'
assert bad['source']==right['source']==['ASTRA-VI-FLAG-BASIS-REFERENCE-397']
sourcepath='review/expose_vi/own_findings.jsonl';line,d,sha=decision(sourcepath,'ASTRA-VI-FLAG-NOTATION-REFERENCE-397')
anomaly=dict(record_type='final_variant_source_attribution_discrepancy',variant='FRV0485',page=397,diplomatic_page_offset=811,printed_context='(notation de3.5)',corrected_context='(notation de4.5)',existing_source=bad['source'],required_source=['ASTRA-VI-FLAG-NOTATION-REFERENCE-397'],reason='The first digit correction is in the notation reference3.5→4.5, whose exact map keeps the canonical kernels F_i and sends them to xi_i. The BASIS source refers to the later corollary3.4→4.4 at offset2238, correctly attached toFRV0495. Both literal digit changes are already correct; only the first source attribution needs amendment.',original_decision_path=sourcepath,original_decision_line=line,original_decision_sha256=sha,image=d['image'],source_reason=d['reason'],comparison_variant=dict(id='FRV0495',diplomatic_page_offset=right['diplomatic_page_offset'],source=right['source']),scope='Metadata only; no source/text change proposed.')
put('FINAL_VARIANT_ATTRIBUTION_DISCREPANCIES.json',[anomaly])
put('SOURCE_DECISION_SNAPSHOT.json',originals)
direct=sum(bool(byvariant[r['id']]) for r in classified)
unlinked=[r for r in classified if not byvariant[r['id']]]
summary=dict(scope='Captured220 additional classifications,all944 MISPRINTS table rows for lookup,and970 final literal variants; selected source-reason audit',input_manifest='review/final_classification_audit/INPUT_MANIFEST.json',existing_classification_count=220,metadata_checks=dict(missing_source_records=0,missing_image_reason_region_or_reading=0,invalid_primary_scan_reference=0,False_reverted_rejected_pending_inclusions=0,missing_or_duplicate_tsv_rows=0,source_tsv_field_mismatches=0),direct_final_variant_links=direct,unlinked_existing_records=dict(total=len(unlinked),historical_Codex_ids=sum(r['id'].startswith('fixes/RECONCILE_CODEX_6.json#') for r in unlinked),retained_unresolved_source_errors=[r['id'] for r in unlinked if 'unresolved' in r['verdict']],incorrect_direct_attribution=['ASTRA-VI-FLAG-NOTATION-REFERENCE-397']),own_source_ids_present_in_variants_but_missing_from_tsv=77,verified_supplemental_source_errors=22,excluded_branch_difference_records=55,excluded_breakdown=dict(glyph_or_font_records=50,explicit_notation_conventions=4,declared_reference_completion=1),supplemental_file='review/final_classification_audit/SUPPLEMENTAL_SOURCE_ERROR_CLASSIFICATIONS.jsonl',final_variant_attribution_discrepancies=1,decisions=checked,limitations=['This is a classification/evidence-link audit,not a fresh image collation or a new proof audit of all220 mathematical passages.','The22 supplemental decisions were read individually with their exact final pairs; the50 glyph records and five other non-error classifications were also read before exclusion.','Historical Codex IDs remain separate historical records; the audit does not assert that220 rows are220 unique source loci or220 apparatus entries.','Three explicitly unresolved source errors retain the author body and correctly have no paired literal variant; inclusion in the source-error table does not assert an applied emendation.','No source records,source patches,body text,shared merger code,or frozen English packet were edited.'])
put('AUDIT_REPORT.json',summary)
(HERE/'AUDIT_REPORT.md').write_text('''# Additional source-error classification audit

The captured220 additional classification records all have a unique original decision,nonempty printed reading,image,region and reason,and exactly one matching row in the captured944-row `MISPRINTS_6_DECIDED.tsv`. Their pages and source-evidence fields agree. No included record is explicitly false,reverted,rejected or pending. The recorded primary/witness scan references exist and their page indices are in range. This validates metadata and evidence links; it does not claim a new scan reading or a fresh proof of every passage.

The final970-variant inventory exposed77 own-source IDs absent from the misprint table. Reading their decisions and actual final pairs established22 omitted source-error classifications:14 early records,three in V and five in X. `SUPPLEMENTAL_SOURCE_ERROR_CLASSIFICATIONS.jsonl` gives an explicit classification,original decision path/line/hash,source image and region,full existing reason,exact final variant pairs and the audit’s reason for each. These records change classification metadata only. The underlying accepted readings and patches remain untouched.

Fifty glyph/notation-transport records,four explicitly declared V slash-notation conventions and the declared X524 reference completion remain excluded. Their dispositions are recorded individually in `EXCLUDED_BRANCH_DIFFERENCES.json`. The360 denominator omission is classified from its separately recorded product-rule calculation and explicit coefficient counterexample; this does not promote the four records expressly marked notation conventions. The p70 KÜnneth occurrence is linked to the identical p75 reading already explicitly classified as a source misprint.

One source-attribution discrepancy needs a metadata correction. FRV0485 at397,offset811,is the first digit of `(notation de3.5)`→`4.5`; it currently cites `ASTRA-VI-FLAG-BASIS-REFERENCE-397` but must cite `ASTRA-VI-FLAG-NOTATION-REFERENCE-397`. The later FRV0495 at offset2238 is `(corollaire3.4)`→`4.4` and correctly cites the BASIS record. The literal body corrections are already correct. The exact discrepancy,source reason and evidence are saved in `FINAL_VARIANT_ATTRIBUTION_DISCREPANCIES.json`.

Of the original220 classifications,109 are directly named in final variants. The111 remaining records comprise107 historical Codex IDs,three explicitly unresolved source errors whose author text remains unchanged,and the397 attribution discrepancy. These are record counts,not counts of unique printed errors or apparatus entries. The historical Codex rows retain their original evidence; this bounded audit does not claim a new exhaustive alias-to-variant correspondence for all107.

The original220 inputs are preserved under `input_snapshots` with SHA-256 values in `INPUT_MANIFEST.json`. `SOURCE_DECISION_SNAPSHOT.json` preserves the exact source decision records used. No source text,frozen checkpoint,shared merger code or sealed English contribution was edited.
''')
print(json.dumps({k:summary[k] for k in ['existing_classification_count','metadata_checks','direct_final_variant_links','unlinked_existing_records','verified_supplemental_source_errors','excluded_branch_difference_records','final_variant_attribution_discrepancies']},ensure_ascii=False,indent=2))
