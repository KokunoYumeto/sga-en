#!/usr/bin/env python3
"""Freeze the exact terminology-audit inputs without changing shared sources."""
from pathlib import Path
import csv, hashlib, json, shutil

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SNAP = HERE / 'input_snapshots'

def main():
    catalog = json.loads((ROOT/'review/english/aggregate/INPUT_CATALOG.json').read_text())
    paths = [
        'review/english/aggregate/INPUT_CATALOG.json',
        'review/english/aggregate/SGA6_EN_raw_current.tex',
        'build/FR_current_revised.tex',
        'review/english/GLOSSARY_SGA6_REVIEWED_001_296.tsv',
        'review/english/GLOSSARY_SGA6_CANDIDATES.tsv',
        'review/english/CROSS_VOLUME_TERMS_CANDIDATE.tsv',
        'review/english/CROSS_VOLUME_TERM_CANDIDATES.tsv',
        'review/english/GLOSSARY_INCONSISTENCIES_CANDIDATE.md',
    ]
    paths += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'en/glossaries').iterdir()) if p.is_file()]
    paths += [str(Path(p['directory'])/'terms.tsv') for p in catalog['packets']]
    records = []
    for relative in paths:
        source = ROOT/relative
        assert source.is_file(), relative
        target = SNAP/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        if target.exists():
            assert target.read_bytes() == data, ('Existing audit snapshot differs; do not overwrite',relative)
        else:
            target.write_bytes(data)
        row = dict(source=relative, snapshot=str(target.relative_to(ROOT)),
                   bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        if target.suffix == '.tsv':
            rows=list(csv.reader(target.open(),delimiter='\t'))
            row.update(data_rows=len(rows)-1,fields=rows[0])
        records.append(row)
    manifest=dict(record_type='terminology_audit_input_manifest',
        scope='All 720 original leaf markers in the reviewed French and integrated English current bodies; exact sealed terminology inventories and supplied reference glossaries.',
        files=records,
        caution='Input term inventories supply attestations and lexical candidates with different count definitions. This audit recalculates its own counts; historical counts are not summed.')
    (HERE/'INPUT_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(files=len(records),term_inventory_rows=sum(r.get('data_rows',0) for r in records if r['source'].endswith('/terms.tsv')),prefix_rows=269)))

if __name__=='__main__':main()
