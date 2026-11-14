#!/usr/bin/env python3
"""Record the explicitly inferred reconstruction of the clipped X549 line."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'review/english'))
from reviewed_french import load_reviewed_pages

SOURCE = 'ASTRA-X-0071'
OLD = r'\(\cl^{\bullet}(E)-n\), où \(E\) est un'
NEW = r'\(\cl^{\bullet}(\underline{E})-\underline{n}\), où \(\underline{E}\) est un'
REASON = (
    'The lower halves of the final line are clipped in primary PDF563, native '
    'witness560 and the SLMath facsimile; none of the three underline strokes '
    'has been recovered physically. The complete adjacent page550 visibly '
    'binds the same underlined O_X-module E of underlined rank section n, '
    'uses underlined E twice in5.3.3, and then explicitly writes plain '
    'E=cl^bullet(underlined E). The identity of the sheaf across the page break '
    'and the class map E↦[E] identify the two damaged E tokens as the sheaf '
    'input and its binder. The rank homomorphism sends [E] to n. On the '
    'constant-rank subobjects of the finite decomposition used on550, '
    'n↦[O_X^n] gives the standard rank-section map, and '
    'epsilon([E]−[O_X^n])=n−n=0. The standard wedge basis trivializes '
    'det(O_X^n), so det([E]−[O_X^n])=det(E). These are the exact maps in '
    'the continuation and5.3.3. Restore the three rules in both layers as '
    'a declared reconstruction from the neighbouring notation and mathematics. '
    'The historical unresolved observation and its image limitations remain '
    'preserved; this amendment decides the reading without asserting that a '
    'lost stroke was seen. No source-misprint variant is introduced.'
)


def append_once(path, row, key='source_id'):
    previous = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    same = [item for item in previous if item.get(key) == row.get(key)]
    if same:
        assert same == [row], (path.name, row.get(key))
        return
    with path.open('a') as stream:
        stream.write(json.dumps(row, ensure_ascii=False) + '\n')


def main():
    existing = (HERE / 'patches.jsonl').read_text()
    already = any(json.loads(line).get('source_id') == SOURCE for line in existing.splitlines())
    before = {}
    for layer in ['diplomatic', 'current']:
        pages, record = load_reviewed_pages(550, layer, start=549)
        assert pages[549].count(NEW if already else OLD) == 1
        before[layer] = dict(page_sha256=hashlib.sha256(pages[549].encode()).hexdigest(),
                             reference=record)

    finding = dict(record_type='own', page=549, source_id=SOURCE,
        verdict='amended', where='last body line, the clipped lower rules of E,n,E',
        printed_reading=NEW, tex=OLD, change=NEW,
        kind='damaged_print_restoration', reason=REASON,
        image='scan/SGA6_scan_360dpi.pdf#page=563',
        region='complete primary549 and550; native549 lower line and550 opening',
        forms='French diplomatic and corrected; English in both source branches',
        is_misprint=False, reconstruction_basis='neighbouring text and exact class/rank maps',
        physical_strokes_recovered=False,
        supersedes='review/expose_x/own_findings.jsonl#ASTRA-X-0071',
        proof_packet='review/expose_x_amendments/damaged_notation_549.json')
    append_once(HERE / 'own_findings.jsonl', finding)
    append_once(HERE / 'patches.jsonl', dict(page=549, layer='both', old=OLD,
        new=NEW, source_id=SOURCE, reason=REASON, expected_count=1))
    append_once(ROOT / 'review/merge_resolutions.jsonl', dict(source_id=SOURCE,
        review_files=['review/expose_x/own_findings.jsonl',
                      'review/expose_x_amendments/own_findings.jsonl'],
        primary_review_file='review/expose_x_amendments/own_findings.jsonl',
        verdict='amended', resolution_reason=REASON))
    append_once(HERE / 'page_status.jsonl', dict(page=549, pdf_page=563,
        checked_against_scan=True, fully_checked=True,
        status='fully compared; clipped notation explicitly reconstructed',
        image='scan/SGA6_scan_360dpi.pdf#page=563',
        region='complete primary549 and550; native549 lower line and550 opening',
        witness_pages=[560, 561], findings=4,
        supersedes='review/expose_x/page_status.jsonl#549',
        reason=REASON, source_id=SOURCE, physical_strokes_recovered=False), key='page')

    viewed = ['build/publisher_recovery/sga6_549.png',
              'build/publisher_recovery/sga6_550.png',
              'review/expose_x/images/w549_2.png',
              'review/expose_x/images/w550_1.png']
    packet = dict(source_id=SOURCE, page=549, status='decided inferred reconstruction',
        reason=REASON, exact_old=OLD, exact_new=NEW,
        physical_strokes_recovered=False,
        root_directly_viewed=[dict(path=p, sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in viewed],
        independent_audit='review/english/contributions/exposes_viii_x/X549_independent_damaged_notation_audit.json',
        historical_record_preserved='review/expose_x/own_findings.jsonl#ASTRA-X-0071',
        maps=[
            'identity on the locally free O_X-module bound across the549/550 source break',
            'class map: E↦[E]=cl^bullet(E)',
            'rank map: epsilon([E])=n',
            'standard rank-section map: n↦[O_X^n], on the constant-rank subobjects used on550',
            'epsilon([E]−[O_X^n])=0',
            'det([E]−[O_X^n])=det(E), by the standard exterior basis of O_X^n'],
        additional_source_note='The printed upper-case N in5.3.3 is independently retained in diplomatic and corrected to n in current by the existing550 source decision.')
    for layer in ['diplomatic', 'current']:
        pages, record = load_reviewed_pages(550, layer, start=549)
        assert pages[549].count(NEW) == 1 and OLD not in pages[549]
        packet[layer + '_verification'] = dict(new_anchor_count=1,
            page_sha256=hashlib.sha256(pages[549].encode()).hexdigest(),
            amendment=[r for r in record['applied_patches'] if r['source_id'] == SOURCE])
    (HERE / 'damaged_notation_549.json').write_text(json.dumps(packet, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(source_id=SOURCE, both_exact_replays=True,
                         source_misprint_variant=False), ensure_ascii=False))


if __name__ == '__main__':
    main()
