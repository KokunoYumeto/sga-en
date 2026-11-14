#!/usr/bin/env python3
"""Assemble all exact sealed English spans, with separately recorded transports."""
from pathlib import Path
import csv, hashlib, json, re
from english_folio_joins import repair as repair_joins

EN = Path(__file__).resolve().parent
ROOT = EN.parents[1]
OUT = EN / 'aggregate'
PACKETS = [
    ('V_VI365_393', 'build/review_snapshots/english_v297_364_vi365_393_complete', r'\sgaStableTarget{sga6.e06.sec.4}'),
    ('VI394_415', 'build/review_snapshots/english_vi394_415_complete', r'\sgaStableTarget{sga6.e07.expose}'),
    ('VII', 'build/review_snapshots/english_vii_complete416_465', r'\sgaStableTarget{sga6.e08.expose}'),
    ('VIII', 'review/english/contributions/exposes_viii_x/snapshots/viii466_497', r'\sgaStableTarget{sga6.e09.expose}'),
    ('IX', 'review/english/contributions/exposes_viii_x/snapshots/ix498_518', r'\sgaStableTarget{sga6.e10.expose}'),
    ('X', 'review/english/contributions/exposes_viii_x/snapshots/x519_594', r'\sgaStableTarget{sga6.e12.expose}'),
    ('XII', 'build/review_snapshots/english_xii_complete595_615', r'\sgaStableTarget{sga6.e13.expose}'),
    ('XIII', 'build/review_snapshots/english_xiii_complete616_666', r'\sgaStableTarget{sga6.e14.expose}'),
    ('XIV_INDEX', 'build/review_snapshots/english_xiv_indexes_complete667_700', r'\end{document}'),
    ('FRONT_REAR', 'build/review_snapshots/english_front_rear_complete20', r'\end{document}'),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def put(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def verify_packet(folder):
    path = folder / 'MANIFEST.json'
    if path.exists():
        manifest = json.loads(path.read_text())
        files = manifest if isinstance(manifest, list) else manifest['files']
    else:
        path = folder / 'MANIFEST.tsv'
        files = list(csv.DictReader(path.open(), delimiter='\t'))
    for record in files:
        file = folder / record['path']
        assert file.is_file(), file
        assert sha(file.read_bytes()) == record['sha256'], file
    return dict(path=path.relative_to(ROOT).as_posix(), sha256=sha(path.read_bytes()), verified_files=len(files))


def main():
    OUT.mkdir(exist_ok=True)
    native = (EN / 'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
    spans = []
    variants = []
    packets = []
    superseded = set()
    for label, relative, end_anchor in PACKETS:
        folder = ROOT / relative
        manifest = verify_packet(folder)
        local = jsonl(folder / 'translation_spans.jsonl')
        for span in local:
            superseded.update(span.get('supersedes', []))
            span = dict(span, contribution=label, packet=relative)
            spans.append(span)
        local_variants = jsonl(folder / 'variants.jsonl')
        for variant in local_variants:
            variant = dict(variant, contribution=label, packet=relative)
            if not variant.get('scope_end'):
                variant['scope_end'] = end_anchor
                variant['aggregate_scope_transport'] = 'Bound the final local variant by the exact next native exposé target.'
            variants.append(variant)
        packets.append(dict(label=label, directory=relative, manifest=manifest,
                            spans=len(local), variants=len(local_variants)))
    prefix = [p for p in jsonl(EN / 'EN_TRANSLATION_PATCHES.jsonl')
              if p['status'].startswith('accepted') and p['id'] not in superseded]
    assert len(superseded) == 8
    source = native
    applications = []
    for span in prefix + spans:
        assert source.count(span['old']) == 1, (span['id'], source.count(span['old']))
        source = source.replace(span['old'], span['new'], 1)
        applications.append(dict(id=span['id'], packet=span.get('packet', 'review/english'),
                                 native_span_sha256=sha(span['old'].encode()),
                                 new_span_sha256=sha(span['new'].encode())))
    amendments = []
    amendment_file = EN / 'EN_AGGREGATE_TEXT_AMENDMENTS.jsonl'
    if amendment_file.exists():
        for amendment in jsonl(amendment_file):
            a = source.index(amendment['scope_start'])
            b = source.index(amendment['scope_end'], a)
            part = source[a:b]
            assert part.count(amendment['old']) == 1, amendment['id']
            source = source[:a] + part.replace(amendment['old'], amendment['new'], 1) + source[b:]
            amendments.append(amendment)
    (OUT / 'SGA6_EN_prejoin_current.tex').write_text(source)
    source, joins = repair_joins(source)
    put(OUT / 'FOLIO_JOIN_AUDIT.json', joins)
    variants = jsonl(EN / 'EN_VARIANTS.jsonl') + variants
    additional_variants = EN / 'EN_AGGREGATE_VARIANTS.jsonl'
    if additional_variants.exists():
        variants.extend(jsonl(additional_variants))
    assert len({v['id'] for v in variants}) == len(variants)
    variants.sort(key=lambda v: (source.index(v['scope_start']) if v.get('scope_start') else 0,
                                 source[source.index(v['scope_start']) if v.get('scope_start') else 0:].index(v['old'])))
    expected = list(range(1, 701))
    actual = [int(n) for n in re.findall(r'\\SGAPrintPage\{(\d+)\}', source)]
    assert actual == expected, (len(actual), set(expected) - set(actual), set(actual) - set(expected))
    strings = re.findall(r'\\SGAPrintPage\{([^}]+)\}', source)
    assert len(strings) == len(set(strings)) == 720
    raw_path = OUT / 'SGA6_EN_raw_current.tex'
    raw_path.write_text(source)
    (OUT / 'VARIANTS.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in variants))
    put(OUT / 'INPUT_CATALOG.json', dict(
        scope='Exact aggregate raw spans: all printed folios 1–700 and all 20 original front/rear leaves, with every contribution seal verified.',
        native_sha256=sha(native.encode()), raw_current_sha256=sha(source.encode()),
        packets=packets, superseded_front_patch_ids=sorted(superseded),
        applications=applications, English_only_amendments=amendments, variant_groups=len(variants),
        reviewed_numeric_folios=expected, reviewed_intervals=[[1, 700]],
        original_leaf_marker_keys=strings, unreviewed_numeric_folios=[],
        source_tex_environment_counts=dict(sorted(__import__('collections').Counter(re.findall(r'\\begin\{([^}]+)\}', source)).items())),
        folio_join_audit='review/english/aggregate/FOLIO_JOIN_AUDIT.json',
        full_English_transfer_complete=True))
    print(json.dumps(dict(applied_spans=len(applications), variants=len(variants),
                          reviewed_numeric_folios=len(expected), original_leaf_markers=len(strings),
                          remaining_folios=[])))


if __name__ == '__main__':
    main()
