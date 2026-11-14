#!/usr/bin/env python3
"""Record inspected XIV author-note labels without creating source variants."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'review/english'))
from reviewed_french import load_reviewed_pages

READINGS = [
    (667, r'$D(X)$\footnote{cf. note de la page 23.}}',
     r'$D(X)$\SGAAuthorFootMark{*}}' + '\n' + r'\SGAAuthorFootText{*}{cf. note de la page 23.}',
     'The section1 heading carries the explicit (*) call after D(X), and the foot carries the same label. The separate mark/text transport preserves that call and the exact short note.', [2]),
    (671, r'\footnote{La formule, ainsi que la variante signalée dans 3.3',
     r'\SGAAuthorFootnote{*}{La formule, ainsi que la variante signalée dans 3.3',
     'The explicit (*) call follows A^i(X) in3.2, and the note has the same label. The unfinished Cf. is printed and remains unfinished.', [1, 2]),
    (675, r'\sgastandalonefootnotetext{xiv-jouanolou}{Elle est donc établie grâce à P. JOUANOLOU pour $X$ lisse quasi-projectif sur un corps (cf. note p.5).}',
     r'\SGAAuthorFootText{*}{Elle est donc établie grâce à P. JOUANOLOU pour $X$ lisse quasi-projectif sur un corps (cf. note p.5).}',
     'The original footnote has label (*) and no visible body call on the full page. Preserve it as an unanchored labelled footnote; no call is supplied.', [1, 2]),
    (677, r'\footnote{cf. note de la page 23.\newline (**)}',
     r'\SGAAuthorFootnote{*}{cf. note de la page 23.\newline (**)}',
     'The body call after actuelle and the first foot label are (*). The separately printed orphan (**) below the note remains explicit on its own line, with no invented body call or note text.', [1, 2]),
    (679, r'\footnote{Cf. IX 3.4, 2.2.}',
     r'\SGAAuthorFootnote{*}{Cf. IX 3.4, 2.2.}',
     'The call after tout entier and the original note both carry (*). Preserve the exact two locators and their punctuation.', [2]),
    (686, r'\footnote{Ajouté en octobre 1968. Les problèmes soulevés ici ont été résolus dans le cadre de la \uline{cohomologie de Hodge} par L. ILLUSIE; cf. [13]}',
     r'\SGAAuthorFootnote{*}{Ajouté en octobre 1968. Les problèmes soulevés ici ont été résolus dans le cadre de la \uline{cohomologie de Hodge} par L. ILLUSIE; cf. [13]}',
     'The call after7.1 and the foot label are (*). Preserve the date, author, underlined cohomologie de Hodge and final locator without adding a full stop.', [1, 2]),
    (688, r'\noindent{\footnotesize (*) Ajouté en février 1969}',
     r'\SGAAuthorFootText{*}{Ajouté en février 1969}',
     'The two existing (*) labels on bibliography items16 and17 remain literal. The shared original note at the foot is transported to a labelled footnote with its printed text and no added terminal punctuation.', [1, 2]),
]


def main():
    patches = []
    findings = []
    packet = []
    for page, old, new, observation, crops in READINGS:
        sid = f'ASTRA-XIV-NOTE-{page}-POSTFREEZE'
        reason = ('The coordinator personally inspected the cited primary image crops. '
                  + observation + ' This is an identity transport of the same original note, applied to both source layers; it introduces no source-misprint variant.')
        patches.append(dict(page=page, layer='both', old=old, new=new,
                            source_id=sid, reason=reason, expected_count=1))
        findings.append(dict(record_type='own', page=page, source_id=sid,
                             verdict='amended', kind='author_note', is_misprint=False,
                             where='original author-note call and printed foot',
                             printed_reading=observation, tex=old, change=new,
                             reason=reason, image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}',
                             region='full upper/lower primary crops as indexed in author_notes.json',
                             forms='French diplomatic and corrected; English both branches'))
        images = [f'review/late/images/p{page}_{crop}.png' for crop in crops]
        packet.append(dict(page=page, source_id=sid, observation=observation,
                           directly_viewed=[dict(path=p, sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in images]))
    for name, rows in [('patches.jsonl', patches), ('own_findings.jsonl', findings)]:
        target = HERE/name
        text = ''.join(json.dumps(row, ensure_ascii=False)+'\n' for row in rows)
        if target.exists():
            existing = [json.loads(line) for line in target.read_text().splitlines() if line.strip()]
            by_id = {row['source_id']: row for row in existing}
            assert len(by_id) == len(existing), target.name
            for row in rows:
                assert by_id.get(row['source_id']) == row, (target.name, row['source_id'])
        else:
            target.write_text(text)
    for item in packet:
        item['verification'] = {}
        for layer in ['diplomatic', 'current']:
            pages, record = load_reviewed_pages(item['page'], layer, start=item['page'])
            replay = [r for r in record['applied_patches'] if r['source_id'] == item['source_id']]
            assert len(replay) == 1
            item['verification'][layer] = dict(exact_replays=1, page_sha256=hashlib.sha256(pages[item['page']].encode()).hexdigest())
    (HERE/'author_notes.json').write_text(json.dumps(packet, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(notes=len(packet), exact_branch_replays=2*len(packet), source_variants=0)))


if __name__ == '__main__':
    main()
