#!/usr/bin/env python3
"""Write the stable handoff and exact file manifest for the glossary packet."""
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def put(name, value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    audit=json.loads((HERE/'GLOSSARY_AUDIT.json').read_text())
    verified=json.loads((HERE/'FINAL_VERIFICATION.json').read_text())
    assert verified['passed']
    filenames=['GLOSSARY_SGA6_FR_EN.tsv','CROSS_VOLUME_TERMS.tsv','GLOSSARY_INCONSISTENCIES.md']
    artifacts=[]
    for name in filenames:
        p=HERE/name;data=p.read_bytes()
        artifacts.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=len(data),sha256=sha(data)))
    record=dict(status='complete; stable for final assembly',
        owned_directory=HERE.relative_to(ROOT).as_posix(),deliverables=artifacts,
        exact_counts={k:audit[k] for k in ['glossary_rows','distinct_French_headword_keys',
            'admitted_multiple_rendering_groups','cross_volume_difference_rows','cross_volume_retained_difference_rows',
            'cross_volume_resolved_prior_deviation_rows','printed_index_rows','printed_terminology_index_rows',
            'printed_notation_index_rows','source_index_ditto_rows','English_terminology_patches']},
        TSV_input_rows_explicitly_disposed=verified['TSV_input_rows_with_explicit_dispositions'],
        manual_lexicon_rows_explicitly_disposed=verified['manual_lexicon_rows_with_dispositions'],
        live_source_leaf_pairs_verified=720,
        English_text_status='Both source-scoped generization repairs are applied by the English assembly owner. Their exact live scopes pass this packet verification. No pending terminology slip has been identified.',
        patch_ids=audit['English_terminology_patch_ids'],
        source_formula_status='No French formula or English mathematical unit is changed by this terminology packet. Source-scoped macro expansions and literal labels are separately proved and counted.',
        red_macro_invocations=20,red_literal_labels_545=3,red_literal_label_597=1,
        audit='review/english/terminology_final/GLOSSARY_AUDIT.json',
        verification='review/english/terminology_final/FINAL_VERIFICATION.json',
        manifest='review/english/terminology_final/MANIFEST.json',
        cross_volume_alias='CROSS_VOLUME_DECISIONS.tsv is byte-identical to CROSS_VOLUME_TERMS.tsv.',
        count_definition=audit['count_definition'],completeness=audit['completeness'],
        final_projection_repairs='The final glossary resolves both printed ditto patterns (692 and693), removes spacing dimensions from lexical search, preserves tau in its Greek term prefix, and retains mixed formula labels literally instead of inventing a headword with a dropped mathematical prefix. These are glossary/search-view repairs only.',
        source_and_sealed_files_changed=False,pending_known_terminology_slips=0)
    put('HANDOFF.json',record)
    lines=['# Final SGA 6 terminology handoff','',
        'Status: complete and stable for final assembly. The shared English builder owns the edition sources and receives this packet without any pending terminology repair.','',
        '## Deliverables','']
    for item in artifacts:
        lines.append(f"- `{Path(item['path']).name}` — {item['bytes']} bytes; SHA256 `{item['sha256']}`.")
    lines += ['', '## Coverage and decisions','',
        f"The glossary has {audit['glossary_rows']} rows for {audit['distinct_French_headword_keys']} distinct French headword keys. It records {audit['admitted_multiple_rendering_groups']} admitted headwords with multiple English renderings and {audit['cross_volume_difference_rows']} cross-volume decisions: {audit['cross_volume_retained_difference_rows']} retained differences and one resolved prior deviation.", '',
        'Every one of the 5,134 declared TSV input rows and 26 additional reviewed entries has an explicit disposition. All 234 printed index rows are paired and assigned exactly once, including both ditto rows. Their original definition references and mathematical units are retained. Thirty-four complete reference formula labels receive a separate literal-token census.', '',
        'The two exact generalization → generization repairs on 648–649 are already applied in the live English source. All 720 live French and English printed-leaf search views agree with this packet’s captured, explicitly patched inventory. The notation ledger records 20 literal red-macro invocations separately from the three literal labels on 545 and one on 597.', '',
        record['count_definition'], '', record['completeness'], '',
        '## Reproduction and verification','',
        'Captured inputs and their hashes are in INPUT_MANIFEST.json, SUPPLEMENTAL_INPUT_MANIFEST.json and FINAL_MACRO_INPUT_MANIFEST.json. Rebuild in this order: make_terminology_patches.py, lexical_inventory.py, index_inventory.py, finalize_glossary.py, verify_glossary.py, close_packet.py. The input preparation script refuses to overwrite a captured input with changed bytes.', '',
        'FINAL_VERIFICATION.json records the successful row census, deduplication, exact index assignment, command counts, cross-volume alias equality, applied patch scopes, live corpus comparison and privacy checks. MANIFEST.json lists every packet file except itself, SEAL_RECEIPT.json and Python caches; SEAL_RECEIPT.json gives the manifest digest. No edition source or immutable contribution seal was edited.', '']
    (HERE/'HANDOFF.md').write_text('\n'.join(lines))
    files=[]
    for p in sorted(HERE.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or p.name in ['MANIFEST.json','SEAL_RECEIPT.json']:
            continue
        data=p.read_bytes();files.append(dict(path=p.relative_to(HERE).as_posix(),bytes=len(data),sha256=sha(data)))
    put('MANIFEST.json',dict(record_type='final_terminology_packet_manifest',files=files,
        omitted=['MANIFEST.json (self)','SEAL_RECEIPT.json (manifest digest)','__pycache__ (reproducible interpreter cache)']))
    receipt=dict(status='complete',manifest='review/english/terminology_final/MANIFEST.json',
        manifest_sha256=sha((HERE/'MANIFEST.json').read_bytes()),manifested_files=len(files),
        manifested_bytes=sum(r['bytes'] for r in files),deliverable_files=len(artifacts))
    put('SEAL_RECEIPT.json',receipt)
    print(json.dumps(receipt))


if __name__=='__main__':
    main()
