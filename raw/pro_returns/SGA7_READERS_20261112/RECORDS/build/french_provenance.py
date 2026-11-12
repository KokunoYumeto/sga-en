#!/usr/bin/env python3
"""Exact-span attribution shared by the French apparatus and baseline change log.

A citation must identify the actual changed span, not merely nearby context.
Historical citation repair changes metadata only. The immutable baseline and
ADOPT cohort make both the scope and the before/after audit reproducible.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import re
from pathlib import Path

def jsonread(path):
    return json.loads(path.read_text())


def lines(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def signature(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def contains(outer, inner):
    return outer[0] <= inner[0] and inner[1] <= outer[1]


def page_spans(text):
    markers = list(re.finditer(r'\\SGApage\{[^}]+\}\{([^}]+)\}', text))
    return {m[1]: (m.end(), markers[i + 1].start() if i + 1 < len(markers) else len(text))
            for i, m in enumerate(markers)}


def occurrences(text, quote, page):
    if not quote or page is None:
        return []
    start, end = page
    found = []
    while (at := text.find(quote, start, end)) >= 0:
        found.append(at)
        start = at + 1
    return found


class PositionSources:
    def __init__(self, source_root, decision_path, token_changes):
        self.by_page = collections.defaultdict(list)
        self.by_ref = {}
        self.quote_cache = {}
        self.token_changes = token_changes
        for vol in ['7I', '7II']:
            for layer in ['', '_CURRENT']:
                path = 'fixes/FIXLOG_' + vol + layer + '.jsonl'
                for i, r in enumerate(lines(source_root / path), 1):
                    self.add(vol, dict(r, source_row_sha256=signature(r), id=r.get('id', f'FIX-{vol}{"-C" if layer else "-D"}-{i:04}'),
                                       ref=f'{path}#{i}'), reversible=not layer)
            path = f'fixes/MISPRINTS_{vol}.json'
            for i, r in enumerate(jsonread(source_root / path)):
                self.add(vol, dict(r, source_row_sha256=signature(r), id=f'{vol}:{i}', old=r.get('tex_did', r.get('print', '')),
                                   new=r.get('correct', ''), ref=f'{path}#{i}', kind='printed misprint'))
        for r in jsonread(decision_path).get('patches', []):
            if r.get('language', 'FR') == 'FR':
                self.add(r['volume'], dict(r, source_row_sha256=signature(r), ref='OPEN_ITEMS_DECIDED.tsv#' + r['id'],
                                            kind='editorial decision'))

    def add(self, vol, record, reversible=False):
        record['old'] = record.get('old') or ''
        record['new'] = record.get('new') or ''
        record['record_old'] = record['old']; record['record_new'] = record['new']
        record['orientation'] = 'record old → record new'
        record['changes'] = self.token_changes(record['old'], record['new'])
        self.by_page[(vol, str(record['page']))].append(record)
        self.by_ref[record['ref']] = record
        if reversible and record['old'] != record['new']:
            reverse = dict(record, old=record['new'], new=record['old'],
                           orientation='record new → record old (diplomatic restoration)')
            reverse['changes'] = self.token_changes(reverse['old'], reverse['new'])
            self.by_page[(vol, str(record['page']))].append(reverse)

    def find_quote(self, component, layer, page, quote):
        key = (component['_context_id'], layer, page, quote)
        if key not in self.quote_cache:
            self.quote_cache[key] = occurrences(component[layer], quote, component['_pages'][layer].get(page))
        return self.quote_cache[key]

    def candidates(self, component, page, old_span, new_span):
        """Return supported records and reproducible positional evidence."""
        supported = []
        rejected = []
        for r in self.by_page[(component['volume'], str(page))]:
            if r.get('file') and r['file'] != component['file']:
                continue
            if not r['changes']:
                rejected.append((r['ref'], 'record old and new are identical'))
                continue
            old_hits = self.find_quote(component, 'diplomatic', str(page), r['old'])
            new_hits = self.find_quote(component, 'corrected', str(page), r['new'])
            best = None
            for i, change in enumerate(r['changes']):
                proof = None
                if len(old_hits) == 1 or len(new_hits) == 1:
                    for ro in old_hits:
                        for rn in new_hits:
                            changed_old = (ro + change['a0'], ro + change['a1'])
                            changed_new = (rn + change['b0'], rn + change['b1'])
                            exact = changed_old == old_span and changed_new == new_span
                            span_supports = contains(changed_old, old_span) and contains(changed_new, new_span)
                            whole = (contains((ro, ro + len(r['old'])), old_span) and
                                     contains((rn, rn + len(r['new'])), new_span) and
                                     r['old'][:old_span[0]-ro] == r['new'][:new_span[0]-rn] and
                                     r['old'][old_span[1]-ro:] == r['new'][new_span[1]-rn:])
                            if span_supports or whole:
                                p = dict(record=r['ref'], record_id=r['id'], strength=4 if exact or whole else 1,
                                         support='coincident changed spans' if exact else 'whole quote differs exactly at hunk' if whole else 'containing changed spans',
                                         record_old_quote=r['old'], record_new_quote=r['new'],
                                         record_old_quote_span=[ro, ro + len(r['old'])],
                                         record_new_quote_span=[rn, rn + len(r['new'])],
                                         record_change_index=i, record_changed_old_span=list(old_span if whole else changed_old),
                                         record_changed_new_span=list(new_span if whole else changed_new),
                                         changed_old=change['before'], changed_new=change['after'])
                                if proof is None or p['strength'] > proof['strength']:
                                    proof = p
                # Later independent edits can alter the surrounding quotation.
                # An exact changed atom still identifies the hunk if it occurs
                # in only one real change on this page. Any surviving whole
                # quotation must point to that same offset, never elsewhere.
                a = component['diplomatic'][slice(*old_span)]
                b = component['corrected'][slice(*new_span)]
                key = (str(page), a, b)
                unique_atom = (change['before'] == a and change['after'] == b and
                               len(component['_hunk_pairs'].get(key, [])) == 1)
                old_anchors = [x for x in old_hits if (x + change['a0'], x + change['a1']) == old_span]
                new_anchors = [x for x in new_hits if (x + change['b0'], x + change['b1']) == new_span]
                contradicted = (old_hits and not old_anchors) or (new_hits and not new_anchors)
                anchored = bool(old_anchors or new_anchors)
                if unique_atom and anchored and not contradicted:
                    atomic = dict(record=r['ref'], record_id=r['id'], strength=3 if anchored else 2,
                                  support='exact changed atom with surviving quote anchor' if anchored else 'unique exact changed atom',
                                  record_old_quote=r['old'], record_new_quote=r['new'],
                                  record_old_quote_spans=[[x, x + len(r['old'])] for x in old_anchors],
                                  record_new_quote_spans=[[x, x + len(r['new'])] for x in new_anchors],
                                  record_change_index=i, record_changed_old_span=list(old_span),
                                  record_changed_new_span=list(new_span), changed_old=a, changed_new=b,
                                  same_page_hunk_candidates=component['_hunk_pairs'][key],
                                  surviving_quote_contradiction=False)
                    if proof is None or atomic['strength'] > proof['strength']:
                        proof = atomic
                if proof is None:
                    continue
                proof['source_row_sha256'] = r['source_row_sha256']
                proof['record_orientation'] = r['orientation']
                proof['original_record_old'] = r['record_old']
                proof['original_record_new'] = r['record_new']
                if best is None or proof['strength'] > best['strength']:
                    best = proof
            if best:
                supported.append(best)
            else:
                rejected.append((r['ref'], 'no exact changed-span support at this hunk position; quoted context is absent, ambiguous, or points elsewhere'))
        chosen = {}
        for p in supported:
            if p['record'] not in chosen or p['strength'] > chosen[p['record']]['strength']:
                chosen[p['record']] = p
        return list(chosen.values()), [(ref, reason) for ref, reason in rejected if ref not in chosen]

    def citation(self, proofs):
        records = [self.by_ref[p['record']] for p in proofs]
        return dict(source='; '.join(dict.fromkeys(r['id'] for r in records)),
                    source_ref='; '.join(dict.fromkeys(r['ref'] for r in records)),
                    kind=records[0].get('kind', 'recorded correction'))



class AttributionSources(PositionSources):
    """Apply verified citations while holding the frozen text/ID scope fixed."""
    def __init__(self, source_root, record_root, token_changes):
        super().__init__(source_root, record_root / 'editorial_decisions.json', token_changes)
        self.record_root = record_root
        self.baseline = jsonread(record_root / 'FR_ATTRIBUTION_BASELINE.json')
        self.frozen = {scope: {r['id']: r for r in self.baseline[scope]}
                       for scope in ['apparatus', 'changes']}
        self.cohort = jsonread(record_root / 'FR_ADOPT_COHORT.json')
        self.adopt_ids = set(self.cohort['ids'])
        assert len(self.adopt_ids) == 531
        assert self.cohort['counts'] == {'7I': 197, '7II': 334}
        self.audit = []

    def context(self, scope, volume, expose, filename, before, after, hunks, before_ref, after_ref, comparison=''):
        pairs = collections.defaultdict(list)
        for h in hunks:
            pairs[(str(h['page']), h['before'], h['after'])].append(h['id'])
        return {'scope': scope, 'volume': volume, 'expose': expose, 'file': filename,
                'diplomatic': before, 'corrected': after, 'comparison': comparison,
                '_context_id': (scope, volume, filename, comparison), '_hunk_pairs': pairs,
                '_pages': {layer: page_spans(text) for layer, text in [('diplomatic', before), ('corrected', after)]},
                'witness_refs': before_ref + '; ' + after_ref}

    def match(self, context, identity, row, page, old_span, new_span):
        """Return source, source_ref, kind for one exact absolute witness hunk."""
        scope = context['scope']
        old = self.frozen[scope][identity]
        identity_fields = {k: v for k, v in row.items() if k not in ('source', 'source_ref', 'kind')}
        assert signature(identity_fields) == old['identity_sha256'], ('Changed text/ID scope', scope, identity)
        assert context['diplomatic'][slice(*old_span)] == row['before'], identity
        assert context['corrected'][slice(*new_span)] == row['after'], identity
        proofs, rejected = self.candidates(context, page, old_span, new_span)
        valid_by_ref = {p['record']: p for p in proofs}
        old_refs = [s.strip() for s in old.get('source_ref', '').split(';') if s.strip()]
        old_ids = [s.strip() for s in old['source'].split(';') if s.strip()]
        explicit = old['source'].startswith('ED-')
        original_adopt = identity in self.adopt_ids if scope == 'apparatus' else False
        original_collation = old['source'].startswith('COLLATION-')
        if explicit or scope == 'changes':
            retained = [p for p in proofs if p['record_id'] in old_ids]
        else:
            retained = [valid_by_ref[r] for r in old_refs if r in valid_by_ref]
        new = {k: old.get(k, '') for k in ('source', 'source_ref', 'kind')}
        if original_adopt:
            status = 'preserved original ADOPT witness decision'; selected = []
            assert old['source'] == 'ADOPT-' + identity
        elif original_collation:
            status = 'preserved original COLLATION witness decision'; selected = []
            new['source_ref'] = context['witness_refs']; new['kind'] = 'source-selection decision'
        elif explicit and retained:
            status = 'preserved explicit edition decision'; selected = retained
            if scope == 'changes':
                new['source_ref'] = '; '.join(p['record'] for p in selected)
                new['kind'] = 'editorial decision'
        elif retained:
            selected = retained
            new = self.citation(selected)
            old_claims = set(old_refs if scope == 'apparatus' else old_ids)
            verified_claims = {p['record'] if scope == 'apparatus' else p['record_id'] for p in selected}
            status = ('preserved supported historical citation' if old_claims == verified_claims
                      else 'removed unsupported co-citation')
        elif proofs:
            strength = max(p['strength'] for p in proofs)
            selected = [p for p in proofs if p['strength'] == strength]
            new = self.citation(selected)
            status = 'relinked to position-supported historical record'
        else:
            selected = []
            new = {'source': 'WITNESS-' + identity, 'source_ref': context['witness_refs'],
                   'kind': 'designated-witness attribution'}
            status = 'unsupported historical claim replaced by witness attribution'
        if not original_adopt and scope == 'apparatus':
            assert not new['source'].startswith('ADOPT-')
        unsupported = {r: reason for r, reason in rejected
                       if r in old_refs or (scope == 'changes' and self.by_ref[r]['id'] in old_ids)}
        if explicit and not retained:
            unsupported['OPEN_ITEMS_DECIDED.tsv#' + old['source']] = (
                'The editorial patch does not change this actual hunk; nearby patch context is not attribution evidence.')
        metadata_fields = ('source', 'source_ref', 'kind') if scope == 'apparatus' else ('source',)
        audit = {'scope': scope, 'id': identity, 'volume': context['volume'], 'expose': context['expose'],
                 'file': context['file'], 'page': str(page), 'comparison': context['comparison'],
                 'printed': row['before'], 'corrected': row['after'],
                 'old_source': old['source'], 'old_source_ref': old.get('source_ref', ''), 'old_kind': old.get('kind', ''),
                 'new_source': new['source'], 'new_source_ref': new['source_ref'], 'new_kind': new['kind'],
                 'original_adopt_cohort': original_adopt, 'status': status,
                 'old_witness_hunk_span': list(old_span), 'new_witness_hunk_span': list(new_span),
                 'witness_refs': context['witness_refs'], 'selected_evidence': selected,
                 'additional_supported_records': [p for p in proofs if p not in selected],
                 'unsupported_original_claims': unsupported,
                 'metadata_changed': any(old.get(k, '') != new[k] for k in metadata_fields)}
        if scope == 'apparatus':
            audit['group_id'] = row['group_id']
        else:
            audit['row_number'] = int(identity.split('-')[1])
            audit['place'] = row['place']
        self.audit.append(audit)
        return new['source'], new['source_ref'], new['kind']

    def finish(self, components, changes):
        scopes = {}
        for scope in ('apparatus', 'changes'):
            rows = [r for r in self.audit if r['scope'] == scope]
            assert [r['id'] for r in rows] == [r['id'] for r in self.baseline[scope]], ('Changed row order', scope)
            scopes[scope] = {'rows': len(rows), 'metadata_changed': sum(r['metadata_changed'] for r in rows),
                            'status_counts': dict(collections.Counter(r['status'] for r in rows)),
                            'witness_fallbacks_by_volume': dict(collections.Counter(r['volume'] for r in rows if r['new_source'].startswith('WITNESS-'))),
                            'selected_proof_support_counts': dict(collections.Counter(p['support'] for r in rows for p in r['selected_evidence']))}
        now_components = [{'volume': c['volume'], 'expose': c['expose'],
                           **{k + '_sha256': hashlib.sha256(c[k].encode()).hexdigest()
                              for k in ('diplomatic', 'corrected', 'annotated')}} for c in components]
        assert now_components == self.baseline['components'], 'Source projection or variant-group body changed'
        entries = [e for c in components for e in c['entries']]
        assert {e['id'] for e in entries if e['source'].startswith('ADOPT-')} == self.adopt_ids
        by_id = {r['id']: r for r in self.audit if r['scope'] == 'apparatus'}
        assert by_id['F7I-IX-212.1']['new_source'] == '7I:800'
        assert by_id['F7I-IX-212.1']['new_source_ref'] == 'fixes/FIXLOG_7I_CURRENT.jsonl#1005'
        assert by_id['F7I-VII-046.1']['new_source'] == 'ED-7I-356'
        assert all(by_id[f'F7II-XVIII-013.{i}']['new_source'] != 'ED-G52-notée' for i in range(2, 6))
        current = [r for r in self.audit if r['comparison'] == 'current']
        assert len(current) == 3 and all(r['old_source'] == r['new_source'] and r['selected_evidence'] for r in current)
        summary = {'purpose': 'Citation-only correction; no new textual correction, changed reading, renumbered entry, or changed review cohort.',
                   **scopes, 'entries': len(entries), 'variant_blocks': len({e['group_id'] for e in entries}),
                   'original_adopt_counts': self.cohort['counts'], 'original_adopt_cohort_unchanged': True,
                   'all_body_fields_entry_ids_group_ids_and_change_row_order_unchanged': True,
                   'source_record_indexing': 'FIXLOG references count JSONL records from 1; MISPRINTS references use the existing zero-based array indices. Editorial patches are identified by their exact decision ID.',
                   'offset_convention': 'Zero-based half-open character spans in the exact cleaned witness projections used by french.py (source comments removed; folio furniture replaced by SGApage anchors).',
                   'method': 'Same volume, file where recorded, and folio. Exact full quotations must place the hunk inside their actual old/new changed spans; alternatively an identical recorded changed atom must be unique among actual same-page hunks and have a surviving full-quotation anchor at that exact span. Every surviving quote must be consistent with the hunk. No nearby-context or quote-length scoring and no unanchored atom inference.',
                   'limits': 'Records using paraphrase, composite quotations, or surrounding text changed independently may fail this conservative exact check. A WITNESS identifier records that the paired designated witnesses support the existing reading, while the earlier individual historical citation is not established. It is a metadata fallback, not an emendation or a new ADOPT decision.',
                   'frozen_input_sha256': {name: hashlib.sha256((self.record_root / name).read_bytes()).hexdigest()
                                           for name in ('FR_ATTRIBUTION_BASELINE.json', 'FR_ADOPT_COHORT.json')}}
        (self.record_root / 'FR_ATTRIBUTION_AUDIT.json').write_text(json.dumps({'summary': summary, 'rows': self.audit}, ensure_ascii=False, indent=2) + '\n')
        fields = ['scope', 'id', 'volume', 'expose', 'page', 'comparison', 'printed', 'corrected',
                  'old_source', 'old_source_ref', 'new_source', 'new_source_ref', 'status', 'original_adopt_cohort']
        with (self.record_root / 'FR_ATTRIBUTION_CHANGES.tsv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n', extrasaction='ignore')
            writer.writeheader(); writer.writerows(r for r in self.audit if r['metadata_changed'])
        text = ['# French source-attribution audit', '',
                'This is a correction of citation metadata. All 2,824 apparatus entries, their 1,112 variant-group identifiers, every diplomatic and corrected body reading, and the order and before/after text of all 7,977 change-log rows are preserved. The original ADOPT review remains exactly 531 entries: 197 in Volume I and 334 in Volume II.', '',
                '## Results', '', '| Record set | Rows checked | Rows with changed citation metadata | New WITNESS fallbacks |', '|---|---:|---:|---:|']
        for scope, label in [('apparatus', 'French apparatus'), ('changes', 'CHANGES_FR')]:
            s = scopes[scope]
            text.append(f"| {label} | {s['rows']} | {s['metadata_changed']} | {sum(s['witness_fallbacks_by_volume'].values())} |")
        text += ['', 'The complete old-to-verified attribution changes are in `FR_ATTRIBUTION_CHANGES.tsv`. `FR_ATTRIBUTION_AUDIT.json` includes every checked row, exact witness offsets, selected source-record quotes and changed spans, record orientation, and hashes of the parsed source rows. `FR_ATTRIBUTION_BASELINE.json` freezes the earlier citation metadata and reading-identity hashes; it does not validate the earlier claims. `FR_ADOPT_COHORT.json` freezes the already reviewed textual cohort.', '',
                 '## Decision rules', '', summary['method'], '', summary['limits'], '',
                 'Existing genuine ADOPT and COLLATION witness decisions are retained even when an additional exact historical link can be found; those optional links appear separately in the audit. Supported historical citations are retained. Unsupported co-citations are removed. A historical claim with no supported citation receives a WITNESS identifier, whose explanation is explicitly about attribution and does not enlarge the textual-review scope.', '',
                 '## Targeted regressions', '',
                 '- F7I-IX-212.1, Reguliers → Réguliers at I:525, now cites 7I:800 at FIXLOG_7I_CURRENT.jsonl record 1005. The neighboring Ferrier correction at record 1006 is rejected because its changed span does not support this hunk.',
                 '- F7II-XVIII-013.2–.5 no longer cite ED-G52-notée: that decision changes notées → notée and does not support these quotation, spacing, and mathematical-accent changes. Each receives its own verified historical or paired-witness attribution.',
                 '- F7I-VII-046.1 retains ED-7I-356. The three current-layer CHANGES_FR rows retain ED-7I-356, ED-G52-notée, and ED-7II-1018, with exact changed-span evidence.', '',
                 '## Reproduction and indexing', '',
                 'Running `python build/french.py` regenerates both the apparatus and CHANGES_FR through the same matcher; `--data-only` omits reader construction. The two frozen input JSON files above must accompany the supplied source witnesses, correction logs, and editorial decisions. The rebuild checks the frozen identities and stops if body readings, entries, groups, or change-log order differ.', '',
                 summary['source_record_indexing'], '', summary['offset_convention'], '']
        (self.record_root / 'FR_ATTRIBUTION_AUDIT.md').write_text('\n'.join(text))
        return summary
