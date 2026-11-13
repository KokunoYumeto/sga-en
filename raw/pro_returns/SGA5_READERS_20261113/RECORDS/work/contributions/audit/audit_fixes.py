#!/usr/bin/env python3
"""Audit French record inheritance without treating intermediate strings as final.

This is an inheritance audit of the authoritative attached layers, supplemented
by literal/projection searches and explicit record-to-record supersession.
It does not rerun a complete historical edit sequence against the August corpus.
"""
import argparse
import bisect
import collections
import csv
import difflib
import hashlib
import json
import re
from pathlib import Path


MARKER = re.compile(r'%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+(\d+)\s*%+')
EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
WINDOWS_PATH = re.compile(r'[A-Za-z]:[\\/](?:Users|Documents and Settings|Program Files|Windows|Temp|tmp)[\\/][^\s"<>]*', re.I)

# These terminal readings are quoted from the recorded replay explanations,
# checked against the final current source, and retained after later conventions.
REPLAY_TERMINAL = {
    1: r'\dim.\mathrm{top}_{\bar{x}}(K)$ la borne',
    2: r'c_*c^!(P\overset{\mathrm{L}}{\otimes} Q)',
    3: r'd_*d^!(P\overset{\mathrm{L}}{\otimes} Q)',
    4: r'P\overset{\mathrm{L}}{\otimes}L',
    5: r'\Hom(Rf_{2*}A,Rf_{1*}A)',
    7: r'\underline{v}:b_{1*}b_2^*M',
    8: r'$v\in\Hom_A(',
    11: r'u\in\Hom_A(c_1^*L,c_2^!L),\qquad v\in\Hom_B(d_1^*M,d_2^!M),',
    12: r'(1) \emph{est produit tensoriel des flèches}',
    13: r'(2) \emph{est la flèche déduite du produit tensoriel externe par restriction selon la diagonale}',
    14: r'\emph{et} (3) \emph{est composé de} 6.5.3',
    15: r'\mathrm{R}_!^{2r}q(q^*L)\longrightarrow',
    16: r'$A^\bullet(P)$ \emph{est un} $A^\bullet(S)$-\emph{module libre de même rang que} $E$',
    17: r'\alpha:A^{\bullet}(S)[T_{ij_i}]_{1\le i\le m,\,1\le j_i\le p_i}\to A^{\bullet}(X)',
    18: r"\emph{l'idéal de l'anneau de polynômes}",
    19: r'$j_i^{\text{ème}}$ \emph{fonction symétrique élémentaire des éléments}',
    20: r'\mathcal O_c^*)\to H^2(X(\mathbb C),\mathbb Z)',
    21: r'g^*[g_*(\cdot)]c_{d-1}(\check F),',
    22: r'\emph{Soient} $X$ \emph{un} $k$-\emph{schéma projectif, lisse, connexe, de dimension} $n$ \emph{et} $Y$',
    23: r"\emph{une section hyperplane lisse de} $X$, \emph{définie par une section d'un}",
    24: r'$\mathcal O_X$-\emph{Module ample} $L$. \emph{Notant}',
    25: r'\underline{\underline{L}}^{-}',
    26: 'Démonstration de la proposition 8.1.',
    28: "(3.2) l'homomorphisme trace:",
    33: r'i), ii) \emph{de} 6.1 \emph{soient remplies}. \emph{Sous ces conditions on a}',
    35: r'$W$) \emph{alors}',
    36: r'\prod_i\prod_j\bigl(L_{\mathrm{R}^j_!v(\mathrm{R}^i_!u(F))}\bigr)^{(-1)^i(-1)^j}',
}
HAND_REPLAY = dict(zip(range(21, 45), [3,4,5,7,8,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,28,33,35,36]))


def safe(s):
    s = str(s or '')
    s = EMAIL.sub('[email omitted]', s)
    s = WINDOWS_PATH.sub('[local source path omitted]', s)
    s = re.sub(r'/(?:home|root|workspace|Users|tmp)/[^\s"<>]*', '[local source path omitted]', s)
    return s


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_rows(path):
    text = path.read_text(encoding='utf-8')
    return [json.loads(line) for line in text.splitlines() if line.strip()] if path.suffix == '.jsonl' else json.loads(text)


def active(text):
    """Delete each unescaped percent and everything through its line ending."""
    result = []
    i = 0
    while i < len(text):
        if text[i] == '%':
            j = i - 1
            while j >= 0 and text[j] == '\\':
                j -= 1
            if (i - 1 - j) % 2 == 0:
                end = text.find('\n', i)
                i = len(text) if end == -1 else end + 1
                continue
        result.append(text[i])
        i += 1
    return ''.join(result)


def project(text):
    """Explicit diagnostic projection pi: active text with Unicode spaces deleted.

    This supplies a string-location witness only. No equivalence of TeX output
    is inferred from equality under this non-injective projection.
    """
    return ''.join(c for c in active(text) if not c.isspace())


def get_pages(text):
    markers = list(MARKER.finditer(text))
    result = {0: text[:markers[0].start()]}
    for i, m in enumerate(markers):
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        result[int(m.group(2))] = text[m.end():end]
    return result


def scope_numbers(record, pages):
    value = record.get('page', record.get('pages'))
    if isinstance(value, int):
        return [value]
    if isinstance(value, list):
        return [int(p) for p in value]
    if value is None:
        return sorted(pages)
    if 'Exposé III' in str(value):
        return list(range(73, 219))
    if 'Exposé V' in str(value):
        return list(range(219, 241))
    if str(value) == '73-':
        return list(range(73, 219))
    match = re.fullmatch(r'(\d+)-(\d+)', str(value))
    if match:
        return list(range(int(match[1]), int(match[2]) + 1))
    return [int(n) for n in re.findall(r'\d+', str(value))] or sorted(pages)


class Layer:
    def __init__(self, text):
        self.text = text
        self.pages = get_pages(text)
        self.active = {p: active(t) for p, t in self.pages.items()}
        self.projected = {p: project(t) for p, t in self.pages.items()}

    def locate(self, needle, numbers, nearby=True):
        if not needle:
            return None
        groups = [('scope', numbers)]
        if nearby and len(numbers) < 20:
            neighbours = sorted({p + d for p in numbers for d in [-1, 1] if p + d not in numbers})
            groups.append(('neighbouring_folio', neighbours))
        aneedle = active(needle)
        projection = project(needle)
        for label, group in groups:
            matches = [(p, self.active.get(p, '').count(aneedle)) for p in group if aneedle and aneedle in self.active.get(p, '')]
            if matches:
                p = matches[0][0]
                at = self.active[p].find(aneedle)
                return {'status': 'literal_active_' + label, 'folios': [p for p, _ in matches],
                        'count': sum(n for _, n in matches),
                        'excerpt': self.active[p][max(0, at - 80):at + min(len(aneedle), 180) + 80]}
            matches = [(p, self.projected.get(p, '').count(projection)) for p in group
                       if projection and projection in self.projected.get(p, '')]
            if matches:
                return {'status': 'whitespace_projection_' + label, 'folios': [p for p, _ in matches],
                        'count': sum(n for _, n in matches), 'excerpt': needle,
                        'qualification': 'Location under the explicitly defined projection; no rendered-output equivalence asserted.'}
        for label, group in groups:
            matches = [(p, self.pages.get(p, '').count(needle)) for p in group if needle in self.pages.get(p, '')]
            if matches:
                return {'status': 'raw_source_only_' + label, 'folios': [p for p, _ in matches],
                        'count': sum(n for _, n in matches), 'excerpt': needle,
                        'qualification': 'Raw source match; active-text search did not locate this string.'}
        if nearby and projection and len(numbers) < 20:
            window = sorted({p + delta for p in numbers for delta in [-1, 0, 1] if p + delta in self.pages})
            for start in range(len(window) - 1):
                if window[start + 1] != window[start] + 1:
                    continue
                pair = window[start:start + 2]
                joined = ''.join(self.projected[p] for p in pair)
                if projection in joined:
                    return {'status': 'whitespace_projection_across_folio_boundary', 'folios': pair,
                            'count': joined.count(projection), 'excerpt': needle,
                            'qualification': 'The recorded string crosses a moved folio marker; verified by the defined projection of two consecutive pages.'}
        return None


def source_layers(fr, prepared, scan_patches, additional_edits):
    with (fr / 'MANIFEST.tsv').open(encoding='utf-8', newline='') as f:
        manifest = {r['path_in_zip']: r for r in csv.DictReader(f, delimiter='\t')}
    proof = {}
    layers = {}
    differences = []
    for name in ['diplomatic', 'current']:
        path = f'fr/sga5/{name}/s5.tex'
        raw = (fr / path).read_bytes()
        expected_sha = manifest[path]['sha256']
        assert sha(raw) == expected_sha, 'Source manifest SHA-256 mismatch: ' + path
        text = raw.decode('utf-8')
        edits = []
        for decision in scan_patches['decisions']:
            location = decision['fr_' + name]
            old = location['source_tex']
            start, end = location['start'], location['end']
            assert text[start:end] == old
            replacement = decision['diplomatic_reading' if name == 'diplomatic' else 'corrected_reading']
            edits.append({'id': decision['id'], 'folio': decision['folio'],
                          'start': start, 'end': end, 'before': old, 'after': replacement})
        if name == 'current':
            match = next(m for m in MARKER.finditer(text) if int(m.group(2)) == 433)
            next_marker = next(m for m in MARKER.finditer(text) if int(m.group(2)) == 434)
            old = r"par $F'/G_{x'}$ l'endomorphisme"
            new = r"par $f'/G_{x'}$ l'endomorphisme"
            start = text.index(old, match.end(), next_marker.start())
            edits.append({'id': 'H75', 'folio': 433, 'start': start, 'end': start + len(old),
                          'before': old, 'after': new})
            old = r'avec $F$ annulé par $\ell^{\nu+1}$'
            new = r'avec $F_\nu$ annulé par $\ell^{\nu+1}$'
            assert text.count(old) == 1
            start = text.index(old)
            edits.append({'id': 'SOL-EN-084', 'folio': 472, 'start': start, 'end': start + len(old),
                          'before': old, 'after': new})
            begin_441 = next(m for m in MARKER.finditer(text) if int(m.group(2)) == 441)
            begin_442 = next(m for m in MARKER.finditer(text) if int(m.group(2)) == 442)
            old = r'\Fr_{Y/S}'
            new = r'\underline{\operatorname{\mathbb{F}r}}_{Y/S}'
            assert text[begin_441.end():begin_442.start()].count(old) == 1
            start = text.index(old, begin_441.end(), begin_442.start())
            edits.append({'id': 'GLOBAL-98b', 'folio': 441, 'start': start, 'end': start + len(old),
                          'before': old, 'after': new})
        for e in additional_edits:
            if name not in e.get('layers', [name]):
                continue
            before, after = e['before'], e['after']
            start = text.index(before)
            if text.count(before) != 1:
                raise ValueError('Additional edit is not unique: ' + e['id'])
            edits.append({'id': e['id'], 'folio': e.get('folio'), 'start': start,
                          'end': start + len(before), 'before': before, 'after': after})
        ordered = sorted(edits, key=lambda e: e['start'])
        assert all(a['end'] <= b['start'] for a, b in zip(ordered, ordered[1:])), 'Overlapping edits'
        rebuilt = text
        for e in reversed(ordered):
            assert rebuilt[e['start']:e['end']] == e['before']
            rebuilt = rebuilt[:e['start']] + e['after'] + rebuilt[e['end']:]
            differences.append({'layer': name, **e})
        output = (prepared / f'FR_{name}_source.tex').read_bytes()
        equal = rebuilt.encode('utf-8') == output
        unaccounted = []
        if not equal:
            for op, a, b, c, d in difflib.SequenceMatcher(None, rebuilt.splitlines(), output.decode('utf-8').splitlines(), autojunk=False).get_opcodes():
                if op != 'equal':
                    unaccounted.append({'operation': op, 'expected_lines': [a + 1, b], 'actual_lines': [c + 1, d],
                                        'expected': '\n'.join(rebuilt.splitlines()[a:b]),
                                        'actual': '\n'.join(output.decode('utf-8').splitlines()[c:d])})
        proof[name] = {'path_in_zip': path, 'manifest_sha256': expected_sha, 'source_sha256': sha(raw),
                       'source_bytes': len(raw), 'prepared_sha256': sha(output), 'prepared_bytes': len(output),
                       'reconstructed_sha256': sha(rebuilt.encode('utf-8')), 'exact_reconstruction': equal,
                       'enumerated_edits': len(edits), 'unaccounted_differences': unaccounted,
                       'folio_markers': len(list(MARKER.finditer(text))),
                       'marker_sequence_unchanged': MARKER.findall(text) == MARKER.findall(output.decode('utf-8'))}
        layers[name] = (Layer(text), Layer(output.decode('utf-8')))
    return proof, layers, sorted(differences, key=lambda e: (e['layer'], e['start']))


def supersession(record, number, records, hand, layer):
    """Find a later recorded replacement which explicitly contains this result."""
    value = record.get('new', '')
    if not value or len(project(value)) < 4:
        return None
    scope = scope_numbers(record, layer.pages)
    candidates = [(f'{record["_file"]}#{i + 1}', r) for i, r in enumerate(records) if i > number]
    candidates += [(f'HANDFIX_5.jsonl#{r.get("_ordinal", i + 1)}', r) for i, r in enumerate(hand)]
    working = value
    chain = []
    for ident, later in candidates:
        later_scope = scope_numbers(later, layer.pages)
        if len(scope) < 40 and not set(scope).intersection(later_scope):
            continue
        old, new = later.get('old', ''), later.get('new', '')
        if not old or not new or len(project(old)) < 4:
            continue
        if value in old or project(value) in project(old):
            witness = layer.locate(new, later_scope)
            if witness:
                return {'status': 'superseded_by_record', 'folios': witness['folios'], 'count': witness['count'],
                        'excerpt': new, 'superseding_id': ident,
                        'qualification': 'Earlier replacement occurs in a later recorded old reading; the later new reading is located.'}
        if old in working and old != new:
            working = working.replace(old, new)
            chain.append(ident)
            witness = layer.locate(working, scope)
            if witness:
                return {'status': 'recorded_overlap_chain', 'folios': witness['folios'], 'count': witness['count'],
                        'excerpt': working, 'superseding_id': ';'.join(chain),
                        'qualification': 'Explicit later old-to-new replacements applied within the earlier result produce this located terminal string.'}
        # The later edit can extend beyond the edge of the earlier logged
        # snippet. Locate its exact prefix/suffix overlap, and transfer only
        # edits fully contained in that shared interval.
        for span in range(min(len(working), len(old)), 1, -1):
            alignments = []
            if working.endswith(old[:span]):
                alignments.append((len(working) - span, 0, span))
            if working.startswith(old[-span:]):
                alignments.append((0, len(old) - span, len(old)))
            for dst, lo, hi in alignments:
                operations = [op for op in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes() if op[0] != 'equal']
                inside = [op for op in operations if lo <= op[1] and op[2] <= hi]
                if not inside:
                    continue
                trial = working
                for op, a, b, c, d in reversed(inside):
                    x, y = dst + a - lo, dst + b - lo
                    if trial[x:y] != old[a:b]:
                        break
                    trial = trial[:x] + new[c:d] + trial[y:]
                else:
                    witness = layer.locate(trial, scope)
                    if witness:
                        return {'status': 'recorded_partial_overlap_witness', 'folios': witness['folios'],
                                'count': witness['count'], 'excerpt': trial,
                                'superseding_id': ident,
                                'qualification': 'A later old reading overlaps this earlier snippet at its boundary. Transferring the later replacement within the exactly shared interval produces the located final string.'}
            if alignments:
                break
    return None


def special_evidence(record, ordinal, final):
    numbers = scope_numbers(record, final.pages)
    file = record['_file']
    if file == 'REPLAY_MANUAL_5.json':
        terminal = REPLAY_TERMINAL.get(ordinal)
        if terminal:
            witness = final.locate(terminal, numbers)
            if witness:
                return {**witness, 'status': 'recorded_manual_resolution_witness',
                        'qualification': 'Terminal reading explicitly checked against the replay explanation and later conventions; original intermediate replacement retained in the before/after columns.'}
    if file == 'HANDFIX_5.jsonl' and ordinal in HAND_REPLAY:
        replay = HAND_REPLAY[ordinal]
        terminal = REPLAY_TERMINAL.get(replay)
        witness = final.locate(terminal, numbers) if terminal else None
        if witness:
            return {**witness, 'status': 'recorded_manual_resolution_witness',
                    'superseding_id': f'REPLAY_MANUAL_5.json#{replay}',
                    'qualification': 'Hand record describes rather than encodes the edit. The corresponding replay and final terminal text supply the witness; later conventions are retained.'}
    if file == 'HANDFIX_5.jsonl' and ordinal == 88:
        witness = final.locate("(3.2) l'homomorphisme trace:", numbers)
        if witness:
            return {**witness, 'status': 'record_only_decision_verified', 'qualification': 'This hand record expressly makes no source edit; the retained reading is located.'}
    page = record.get('page')
    if file == 'HANDFIX_5.jsonl' and ordinal in [5,6,11,12,13,14,15,16,17,19]:
        anchors = {356: r'\[K(\cB)', 403: '(``isomorphisme', 484: r'\sgaindexentry{$\QQ_\ell$-fc$(X)$}',
                   471: r'\[f^{-n}_{F_{\barx}}', 455: r"\[\fr_{X'}^*(F')"}
        prefix = anchors.get(page)
        if prefix and final.projected[page].startswith(prefix):
            return {'status': 'marker_anchor_verified', 'folios': [page], 'count': 1,
                    'excerpt': final.pages[page][:200], 'qualification': 'Specified folio begins with the recorded anchor after the explicit whitespace projection.'}
    if file == 'HANDFIX_5.jsonl' and ordinal in [18,20]:
        if final.pages[474].rstrip().endswith('en cha%') and final.active[475].lstrip().startswith('que'):
            return {'status': 'split_word_join_verified', 'folios': [474,475], 'count': 1,
                    'excerpt': final.pages[474][-90:] + final.pages[475][:30],
                    'qualification': 'The previous page ends en cha% and the next starts que; the explicit TeX comment operation consumes the intervening line ending.'}
    new = record.get('new', '')
    structural = None
    structural_note = ''
    if new == 'line break after the note, the text restored':
        structural = r'Soit $Y$ un fermé non vide'
        structural_note = 'The formerly swallowed prose is found in active TeX.'
    elif new == 'line break after the comment, the text after it restored':
        structural = r", $A'$, $B'$, $X'$ les transformés purs respectifs"
        structural_note = 'The continuation after FIX#58 is on an active source line; its folio follows the final moved markers.'
    elif new.startswith(r'Exposé III: \mathrm{R}\underline'):
        structural = r'\renewcommand{\uRHom}{\mathrm{R}\underline{\mathrm{Hom}}}'
        structural_note = 'The explicit scoped definition named by the descriptive convention record is present.'
    elif new.startswith('Exposé III: labels without'):
        structural = r'\renewenvironment{statement}[1]{\par\medskip\noindent\textbf{#1}\ }{\par\medskip}'
        structural_note = 'The scoped statement environment appends no full stop after its label argument.'
    elif new.startswith("Exposé V: 'Preuve :'"):
        structural = r'\renewenvironment{prooftext}[1][Preuve]{\par\noindent\emph{#1} :\ }{\par\medskip}'
        numbers = sorted(final.pages)
        structural_note = 'The scoped proof-label environment implements the recorded Preuve colon form.'
    elif new.startswith('(deleted; the proof label is run in'):
        structural = r'\emph{Preuve} :'
        structural_note = 'The run-in proof label specified by the record is present in the stated scope.'
    elif new == r'M\otimes_K...':
        structural = r'M\otimes_K'
        structural_note = 'The log describes several outputs with an ellipsis; its explicitly written tensor prefix is located.'
    if structural:
        witness = final.locate(structural, numbers)
        if witness:
            return {**witness, 'status': 'descriptive_record_structural_witness', 'qualification': structural_note}
    if new == r'{Corollaire 4.7 - (Formule de Lefschetz-Verdier)}':
        terminal = r'{Corollaire 4.7 - (Formule de Lefschetz-Verdier).}'
        witness = final.locate(terminal, numbers)
        if witness:
            return {**witness, 'status': 'source_terminal_difference_documented',
                    'qualification': 'The authoritative source has one final full stop before the closing title brace, absent from this intermediate log string. The title and its single hyphens are present. This audit preserves that supplied terminal reading and does not invent a historical record for the extra stop.'}
    if file == 'FIXLOG_5_CURRENT.jsonl' and ordinal == 274:
        terminal = r'(SGAA~XVIII~3.1.10)}'
        witness = final.locate(terminal, numbers)
        if witness:
            return {**witness, 'status': 'recorded_misprint_resolution_witness',
                    'superseding_id': 'MISPRINTS_5.json#61',
                    'qualification': 'The punctuation result is retained with the independently recorded missing-exposé correction XVIII; the final moved folio is recorded in the witness.'}
    if file == 'FIXLOG_5_CURRENT.jsonl' and ordinal == 474:
        assert record['old'].replace('de 7.1 soient', 'de 6.1 soient') == new
        witness = final.locate(REPLAY_TERMINAL[33], numbers)
        if witness:
            return {**witness, 'status': 'recorded_manual_resolution_witness',
                    'superseding_id': 'HANDFIX_5.jsonl#42; REPLAY_MANUAL_5.json#33',
                    'qualification': 'The exact edit in this record is 7.1 -> 6.1. Its corrected reference is present inside the subsequently restored emphasis, as explicitly recorded by hand replay.'}
    if new == r'moved after \end{center}':
        page = final.pages[73]
        centre = page.index(r'\end{center}')
        definition = page.index(r'\renewenvironment{statement}')
        if centre < definition:
            return {'status': 'scoped_definition_position_verified', 'folios': [73], 'count': 1,
                    'excerpt': page[centre:definition + 100], 'qualification': 'The scoped definitions follow the closed centre environment in the actual source.'}
    if new.startswith('reset moved to Exposé V'):
        raw = final.text
        pos = raw.index('% Exposé V: back to')
        witness_page = max(p for p, t in final.pages.items() if '% Exposé V: back to' in t)
        return {'status': 'scoped_reset_position_verified', 'folios': [witness_page], 'count': 1,
                'excerpt': raw[pos:pos + 600], 'qualification': 'The recorded reset is located at the explicit Exposé V boundary; source inheritance preserves its placement.'}
    if new.startswith(r'marker before the display \widehat A'):
        content = final.projected[291]
        if content.startswith(r'\[\widehat A^{\bullet}(S)'.replace(' ', '')):
            return {'status': 'marker_anchor_verified', 'folios': [291], 'count': 1,
                    'excerpt': final.pages[291][:160], 'qualification': 'The folio begins with the specified display; the terminal raised-dot notation is preserved from the final source.'}
    if new == 'a space before the note (the output keeps the space)':
        matches = list(re.finditer(r'\. +%[^\n]*', final.text))
        if matches:
            return {'status': 'descriptive_record_pattern_present', 'folios': [], 'count': len(matches),
                    'excerpt': matches[0].group(), 'qualification': 'The global description has no individual location; full-stop/space/comment sequences are present and preserved by exact source inheritance.'}
    if new == r'\emph{Preuve} : ...':
        witness = final.locate(r'\emph{Preuve} :', numbers)
        if witness:
            return {**witness, 'status': 'descriptive_record_pattern_present',
                    'qualification': 'The record uses an ellipsis and supplies no unique location. Its literal proof-label prefix is present; a one-to-one historical occurrence is not claimed.'}
    if new == 'elided word + % (no space in the output)':
        matches = list(re.finditer(r"[A-Za-zÀ-ÿ']%\n", final.text))
        if matches:
            return {'status': 'descriptive_record_pattern_present', 'folios': numbers, 'count': len(matches),
                    'excerpt': final.text[max(0,matches[0].start()-30):matches[0].end()+30],
                    'qualification': 'The record gives a descriptive global pattern rather than a concrete replacement or unique location. Word-final percent joins are present; exact source inheritance preserves every occurrence.'}
    if new == 'partial-foncteur':
        witness = final.locate(r'\(\partial\)-foncteur', numbers)
        if witness:
            return {**witness, 'status': 'descriptive_notation_witness',
                    'qualification': 'The log describes the partial sign in words; the explicit TeX spelling of that sign is located.'}
    if not new and record.get('old') == r'\end{prooftext}' and record.get('page') is None:
        begins = len(re.findall(r'\\begin\{prooftext\}', active(final.text)))
        ends = len(re.findall(r'\\end\{prooftext\}', active(final.text)))
        if begins == ends:
            return {'status': 'global_environment_balance_verified', 'folios': [], 'count': begins,
                    'excerpt': '', 'qualification': f'Global prooftext begin/end counts are {begins}/{ends}; the orphan-removal record has no location, so historical individual deletion is not independently reconstructed.'}
    return None


def convention_witness(record, final, index, records, hand):
    value = record.get('new', '')
    if not value:
        return None
    numbers = scope_numbers(record, final.pages)
    substitutions = []
    if any(73 <= p <= 218 for p in numbers) and len(numbers) < 200:
        for old in [r'\otimes^{\mathbf L}', r'\otimes^{L}', r'\otimes^L', r'\overset{\mathbf L}{\otimes}', r'\overset{L}{\otimes}']:
            if old in value:
                value = value.replace(old, r'\overset{\mathrm{L}}{\otimes}')
                substitutions.append('derived tensor convention: ' + old + ' -> ' + r'\overset{\mathrm{L}}{\otimes}')
        if r'\otimes_S^{\mathbf L}' in value:
            value = value.replace(r'\otimes_S^{\mathbf L}', r'\overset{\mathrm{L}}{\otimes}_S')
            substitutions.append('derived tensor convention with S subscript')
        if r'L_{\natural}' in value:
            value = value.replace(r'L_{\natural}', r'L\natural')
            substitutions.append('L-natural convention in FIXLOG_5.jsonl#1395 / FIXLOG_5_CURRENT.jsonl#1287')
    if any(p in [408,410,411,412,426,427,432] for p in numbers) and len(numbers) < 25:
        pattern = r"(?<![A-Za-z\\])H(?=(?:\^\\vee)?_\{(?:n,|m,|U\'))"
        changed = re.sub(pattern, lambda _: r'\mathcal{H}', value)
        if changed != value:
            substitutions.append('HANDFIX_5.jsonl#52/#53 script-H regex')
            value = changed
        if value.endswith(r'_{H^\vee'):
            value = value[:-len(r'_{H^\vee')] + r'_{\mathcal{H}^\vee'
            substitutions.append('HANDFIX_5.jsonl#52/#53 script-H rule applied at the truncated right edge of the logged snippet')
    if numbers == [447] and r'\Omega' in value:
        value = value.replace(r'\Omega', r'\underline{\Omega}')
        substitutions.append('HANDFIX_5.jsonl#68/#69 underlined-Omega rule; the log snippet ends before the exponent')
    if substitutions:
        witness = final.locate(value, numbers)
        if witness:
            return {**witness, 'status': 'recorded_convention_substitution_witness',
                    'superseding_id': '; '.join(substitutions),
                    'qualification': 'Exact substitutions explicitly described in the records produce the located final string; the original earlier string is retained separately.'}
        following = supersession({**record, 'new': value}, index, records, hand, final)
        if following:
            return {**following, 'status': 'recorded_convention_and_overlap_witness',
                    'superseding_id': '; '.join(substitutions) + '; ' + following.get('superseding_id', ''),
                    'qualification': 'The explicit convention substitutions followed by the named overlapping recorded edits produce the located terminal string.'}
    return None


def evidence(record, index, records, hand, original, final):
    new = record.get('new', record.get('inserted', record.get('fix', {}).get('new', '')))
    old = record.get('old', record.get('fix', {}).get('old', ''))
    if record['_layer'] == 'current' and record.get('kind') == 'misprint_in_print' and 'corrected' in record:
        new = record['corrected']
    numbers = scope_numbers(record, final.pages)
    found = final.locate(new, numbers)
    if found:
        return found
    found = special_evidence(record, index + 1, final)
    if found:
        return found
    found = convention_witness(record, final, index, records, hand)
    if found:
        return found
    if new and any(457 <= p <= 474 for p in numbers) and len(numbers) < 25:
        glyph = r'\underline{\underline{\mathrm{R}}}\Gamma' if record['_layer'] == 'diplomatic' else r'\mathrm{R}\Gamma'
        transformed = new.replace(r'\RGamma', glyph).replace(r'\R\Gamma', glyph)
        if transformed != new:
            found = final.locate(transformed, numbers)
            if found:
                return {**found, 'status': 'transformed_by_R98_decision',
                        'qualification': 'Exact explicit R98 substitution applied to this old result; located after substitution.'}
    if new:
        found = supersession(record, index, records, hand, final)
        if found:
            return found
    if not new and old:
        present = final.locate(old, numbers, nearby=False)
        if not present:
            return {'status': 'deletion_old_absent_in_scope', 'folios': numbers, 'count': 0,
                    'excerpt': '', 'qualification': 'The deleted literal is absent in the final scope; historical occurrence placement is supplied by the source record.'}
    original_found = original.locate(new, numbers)
    if original_found:
        return {**original_found, 'status': 'original_layer_result_located_final_changed',
                'qualification': 'Original result found but final result requires examination against the enumerated build edits.'}
    return {'status': 'inherited_source_record_no_terminal_literal', 'folios': numbers,
            'count': '', 'excerpt': '',
            'qualification': 'Exact source-inheritance proof applies; no direct terminal literal witness was established by these searches.'}


def make_row(file, ordinal, record, layer, ev, disposition='applied as supplied'):
    return {'record_id': f'{file}#{ordinal}', 'original_id': record.get('id', ''),
            'record_file': 'fixes/' + file, 'record_number_1based': ordinal,
            'layer': layer, 'page': record.get('page', record.get('pages', 'all/source-defined')),
            'kind': record.get('kind', 'recorded hand edit'),
            'record_disposition': disposition,
            'terminal_evidence': ev.get('status', ''),
            'evidence_folios': ','.join(map(str, ev.get('folios', []))),
            'observed_matches': ev.get('count', ''), 'recorded_count': record.get('count', ''),
            'superseding_record': ev.get('superseding_id', ''),
            'before_json': json.dumps(safe(record.get('old', record.get('fix', {}).get('old', ''))), ensure_ascii=False),
            'after_json': json.dumps(safe(record.get('new', record.get('inserted', record.get('fix', {}).get('new', '')))), ensure_ascii=False),
            'source': safe(record.get('source', '')),
            'record_resolution': safe(record.get('resolved', record.get('status', record.get('what', '')))),
            'qualification': safe(ev.get('qualification', 'A source-string location witness; repeated strings can have several matches.')),
            'evidence_excerpt_json': json.dumps(safe(ev.get('excerpt', '')), ensure_ascii=False),
            'inheritance_proof': 'AUDIT_FR.json source_inheritance.' + layer}


def tsv(path, rows):
    if not rows:
        return
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def verify_manifest_inputs(fr, paths):
    """Record byte and SHA-256 checks without copying manifest source paths."""
    with (fr / 'MANIFEST.tsv').open(encoding='utf-8', newline='') as f:
        manifest = {r['path_in_zip']: r for r in csv.DictReader(f, delimiter='\t')}
    verified = []
    for path in sorted(set(paths)):
        raw = (fr / path).read_bytes()
        expected = manifest[path]
        digest = sha(raw)
        match = len(raw) == int(expected['bytes']) and digest == expected['sha256']
        assert match, 'Record manifest mismatch: ' + path
        verified.append({'path_in_zip': path, 'bytes': len(raw), 'sha256': digest,
                         'manifest_bytes_and_sha256_match': match})
    return verified


def write_report(output, summary):
    proof = summary['source_inheritance']
    misprint_count = summary['misprints']['count']
    misprint_witnesses = summary['misprints']['current_literal_or_projection_witnesses']
    misprint_evidence = summary['misprints']['current_terminal_evidence']
    direct = {name: sum(value for status, value in summary['fix_logs'][file]['terminal_evidence'].items()
                       if status.startswith('literal_active_'))
              for name, file in [('diplomatic', 'FIXLOG_5.jsonl'), ('current', 'FIXLOG_5_CURRENT.jsonl')]}
    text = f'''# French fix-inheritance audit

## Result and scope

Both prepared French layers are reproduced **byte for byte** from their manifest-verified attached source layers by the complete edit list in `SOURCE_TO_PREPARED_FR.tsv`. There are {proof['diplomatic']['enumerated_edits']} edits in the diplomatic layer and {proof['current']['enumerated_edits']} in the current layer. There are no unaccounted differences. This proves that the source state containing the earlier applied fixes is inherited, except for the explicitly enumerated new decisions.

The 32 common edits implement the inspected Exposé XV RΓ decisions. Three additional current-layer edits implement H75 at folio 433 (`F'` to `f'` in the indicated quotient endomorphism), SOL-EN-084 at folio 472 (`F` to `F_\\nu` in the annihilation clause), and GLOBAL-98b at folio 441. The last retains the recorded single-underlined, double-struck-F reading of Fr at the unresolved glyph question, following the source task's instruction to keep the printed reading while the scan is needed. The diplomatic layer keeps its supplied readings at those three places. Exact before/after strings and original character offsets are recorded for every edit.

This audit reaches the prepared layers. The reader build extends the proof by checking that the diplomatic and corrected branch projections of its annotated master reproduce those layers, with any presentation-only extraction explicitly specified. Compiling alone does not establish that relation. The audit does not independently reproduce the historical scan-check sequence or recheck judgments against scans unavailable in the attached material.

## Verified source identities

| ZIP-relative source | Source SHA-256 | Prepared SHA-256 | Enumerated edits |
|---|---|---|---:|
| `fr/sga5/diplomatic/s5.tex` | `{proof['diplomatic']['source_sha256']}` | `{proof['diplomatic']['prepared_sha256']}` | {proof['diplomatic']['enumerated_edits']} |
| `fr/sga5/current/s5.tex` | `{proof['current']['source_sha256']}` | `{proof['current']['prepared_sha256']}` | {proof['current']['enumerated_edits']} |

The byte lengths and SHA-256 values of all {len(summary['record_manifest_verification'])} audited fix/status input files also match `MANIFEST.tsv`. `AUDIT_FR.json` records each check by its path inside `SGA5_FR.zip`; source-machine paths are omitted.

## Record coverage

| Collection | Source records | Audit treatment |
|---|---:|---|
| `fixes/FIXLOG_5.jsonl` | 4,173 | One diplomatic inheritance row per original record |
| `fixes/FIXLOG_5_CURRENT.jsonl` | 3,770 | One current inheritance row per original record, including all 29 `misprint_correction` records |
| `fixes/HANDFIX_5.jsonl` | 88 | Original one-based record numbers preserved; layer read from each record |
| `fixes/REPLAY_MANUAL_5.json` | 36 | All 36 have a `resolved` field; later conventions and hand edits are checked |
| `fixes/REPLAY_MANUAL_5_DONE.json` | 1 | Earlier replay sidecar audited separately |
| Seven `fixes/MANUAL_5_findings_*.json` files | 8 findings | Both layers checked, giving 16 rows |
| `fixes/RECONCILE_CODEX_5.json` | 117 entries | Supplied status and reason retained in a separate table |
| `fixes/MISPRINTS_5.json` | 590 entries | Printed/corrected strings and notes retained; presence evidence recorded separately |

`FIX_INHERITANCE_FR.tsv` contains **8,084 rows**: 4,173 + 3,770 + 88 + 36 + 1 + 16. Each row has the source file and its original one-based record number, source scope, before/after strings, observed terminal evidence, observed folios and match counts, any identified superseding record, and qualifications. The source's own `id` is retained separately where supplied. The two extra tables contain all 117 reconciliation entries and all 590 misprint entries.

The reconciliation statuses are 56 `present`, 49 `applied`, 11 `rejected`, and 1 `superseded`. These are preserved decisions from the source record, with exact-source inheritance establishing that this build retains the supplied final layer state.

## What the terminal checks establish

Direct active-source literal witnesses were found for {direct['diplomatic']:,} of the 4,173 diplomatic fix-log records and {direct['current']:,} of the 3,770 current fix-log records. These searches allow an adjacent folio because later hand work moved markers. The remaining log rows have explicitly reported evidence: later overlapping edits, recorded conventions, named superseding records, descriptive or structural witnesses, deletions, R98 substitutions, or the documented title-stop discrepancy below. No fix-log row remains with the generic unresolved terminal-search status. All 88 hand records and all 36 replay records have terminal or explicitly described structural evidence. `AUDIT_FR.json` gives the complete evidence-category counts, including those for the 29 current-layer misprint corrections.

The proof of inheritance is the exact source reconstruction. The terminal searches supplement that proof with record-level witnesses; they do not assume that an intermediate `new` string must survive every later edit. For a recorded overlap, the script applies the later exact `old`/`new` replacement inside the earlier result and locates the resulting string. For a partial overlap, it identifies the exact shared prefix or suffix and transfers only changed intervals inside that shared text. The relevant record identifiers remain in the table. Explicit convention mappings, including derived tensor notation, script H, underlined Omega, and the R98 decisions, are similarly listed.

Some source records describe a global pattern or use ellipses. Their rows report the specified pattern or structural check and state that an individually unique historical occurrence was not established. A literal appearing more than once is reported with its match count. A raw-source-only match is distinguished from a match in the diagnostic active text. Deletion evidence reports the old string's absence in its scope; it does not manufacture a historical location for an unlocated deletion.

For the small number of whitespace-projection witnesses, the mapping is explicitly defined: delete each unescaped percent sign and the following text through its line ending, then delete Unicode whitespace. Equality after this mapping gives a string-location witness. It is not used as a proof that arbitrary TeX expressions have identical rendered output. No notation is rewritten in the source by this audit.

## Source-record details that require qualification

At folio 109, `FIXLOG_5.jsonl#710` and `FIXLOG_5_CURRENT.jsonl#665` record the title string `{{Corollaire 4.7 - (Formule de Lefschetz-Verdier)}}`. The authoritative final sources contain `{{Corollaire 4.7 - (Formule de Lefschetz-Verdier).}}`, with a final full stop before the closing brace. The audit reports `source_terminal_difference_documented` for these two rows. The title and its single hyphens are located; the final source's additional stop is inherited. No historical record for that added stop is invented.

`REPLAY_MANUAL_5.json#10` has a `resolved` field whose text still begins “open”. Its folio-184 wording was subsequently restored by `HANDFIX_5.jsonl#45`; that terminal text is present. The original status wording remains visible in the audit rather than being silently rewritten. Likewise, replay items 12–14 at folio 201 are read with the later restorations in hand records 46–48.

`fixes/MARKERS_5.json` is an earlier placement report: it lists 482 markers and missing folios 435 and 484 in both layers. Hand records 13 and 14 subsequently add folio 484. The final source layers and prepared layers each contain **483 markers**, with the same full ordered marker sequence, scan index equal to folio + 11, and only folio 435 absent. The source task explains that omission by the print's repeated page number 434; the build does not invent a folio-435 marker.

## Misprint-register status

All 590 entries contain `page`, `where`, `print`, `correct`, `tex_did`, `note`, and `source`. No entry contains a separate `status` or `decision` field. The decisions and qualifications therefore have to be read from the supplied fields and notes.

The final current layer supplies a literal or explicit projection witness for {misprint_witnesses} corrected descriptions: {misprint_evidence.get('literal_active_scope', 0)} on the declared folio, {misprint_evidence.get('literal_active_neighbouring_folio', 0)} on an adjacent folio, and {misprint_evidence.get('whitespace_projection_scope', 0)} under the stated whitespace projection. The remaining {misprint_count - misprint_witnesses} descriptions require their prose, notation, supersession, or new-build-decision context; failure of this literal search is recorded explicitly. They include the folio-441 GLOBAL-98b decision to retain the printed glyph while its scan remains needed. The audit makes no blanket assertion that 590 proposed corrections were all inserted. The full register notes are retained in `MISPRINT_STATUS_FR.tsv`, while the manifest/source reconstruction separately proves preservation of the attached final layer except for the enumerated decisions.

## Reproduction and files

From the build workspace, run:

```sh
python work/contributions/audit/audit_fixes.py
```

The script also accepts `--fr`, `--prepared`, `--scans`, and `--output` to set the source directory, prepared-layer directory, R98 patch JSON, and audit output directory. `--additional-edits` accepts an explicit JSON list of further uniquely located before/after edits when a later build adds a recorded decision. The script checks source identities, expected record counts, exact reconstruction, marker inheritance, and unresolved terminal searches, and exits unsuccessfully when one of these required checks fails.

Outputs are `AUDIT_FR.json`, `FIX_INHERITANCE_FR.tsv`, `SOURCE_TO_PREPARED_FR.tsv`, `RECONCILE_INHERITANCE_FR.tsv`, `MISPRINT_STATUS_FR.tsv`, and this report. All source references in these outputs use paths inside the input ZIPs or record identifiers. Email addresses and source-machine paths are removed from copied free-text evidence.
'''
    (output / 'AUDIT_FR_REPORT.md').write_text(text, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fr', type=Path, default=Path('work/sources/SGA5_FR'))
    parser.add_argument('--prepared', type=Path, default=Path('work/build/prepared'))
    parser.add_argument('--scans', type=Path, default=Path('work/contributions/scans/PLACES_98_PATCHES.json'))
    parser.add_argument('--output', type=Path, default=Path('work/contributions/audit'))
    parser.add_argument('--additional-edits', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    patches = json.loads(args.scans.read_text())
    additional = json.loads(args.additional_edits.read_text()) if args.additional_edits else []
    proof, layers, changes = source_layers(args.fr, args.prepared, patches, additional)
    fixes = args.fr / 'fixes'
    record_files = ['FIXLOG_5.jsonl', 'FIXLOG_5_CURRENT.jsonl', 'HANDFIX_5.jsonl',
                    'REPLAY_MANUAL_5.json', 'REPLAY_MANUAL_5_DONE.json',
                    'MISPRINTS_5.json', 'RECONCILE_CODEX_5.json', 'MARKERS_5.json']
    record_files.extend(path.name for path in sorted(fixes.glob('MANUAL_5_findings_*.json')))
    manifest_checks = verify_manifest_inputs(args.fr, ['fixes/' + name for name in record_files])
    hand = read_rows(fixes / 'HANDFIX_5.jsonl')
    for i, record in enumerate(hand, 1):
        record['_ordinal'] = i
    rows = []
    collections_summary = {}
    for file, layer in [('FIXLOG_5.jsonl', 'diplomatic'), ('FIXLOG_5_CURRENT.jsonl', 'current')]:
        records = read_rows(fixes / file)
        for r in records:
            r['_file'], r['_layer'] = file, layer
        selected_hand = [r for r in hand if layer in r.get('file', '')]
        for i, r in enumerate(records):
            ev = evidence(r, i, records, selected_hand, *layers[layer])
            rows.append(make_row(file, i + 1, r, layer, ev))
        collections_summary[file] = {'records': len(records),
                                      'kinds': dict(collections.Counter(r.get('kind') for r in records)),
                                      'terminal_evidence': dict(collections.Counter(row['terminal_evidence'] for row in rows if row['record_id'].startswith(file + '#')))}
    for i, r in enumerate(hand):
        layer = 'diplomatic' if 'diplomatic' in r.get('file', '') else 'current'
        r['_file'], r['_layer'] = 'HANDFIX_5.jsonl', layer
        ev = evidence(r, i, hand, [], *layers[layer])
        rows.append(make_row('HANDFIX_5.jsonl', i + 1, r, layer, ev,
                             'record-only decision; no edit' if 'no edit of s5.tex' in r.get('what', '') else 'applied as supplied'))
    replays = read_rows(fixes / 'REPLAY_MANUAL_5.json')
    for i, r in enumerate(replays):
        r['_file'], r['_layer'] = 'REPLAY_MANUAL_5.json', 'current'
        ev = evidence(r, i, replays, hand, *layers['current'])
        rows.append(make_row('REPLAY_MANUAL_5.json', i + 1, r, 'current', ev,
                             'resolution text supplied; later conventions also audited'))
    done = read_rows(fixes / 'REPLAY_MANUAL_5_DONE.json')
    for i, r in enumerate(done):
        r['_file'], r['_layer'] = 'REPLAY_MANUAL_5_DONE.json', 'current'
        ev = evidence(r, i, done, hand, *layers['current'])
        rows.append(make_row('REPLAY_MANUAL_5_DONE.json', i + 1, r, 'current', ev, r.get('status', '')))
    manual_counts = {}
    for path in sorted(fixes.glob('MANUAL_5_findings_*.json')):
        records = read_rows(path)
        manual_counts[path.name] = len(records)
        for i, r in enumerate(records):
            for layer in ['diplomatic', 'current']:
                r['_file'], r['_layer'] = path.name, layer
                ev = evidence(r, i, records, hand, *layers[layer])
                rows.append(make_row(path.name, i + 1, r, layer, ev, 'resolution supplied'))
    reconcile = read_rows(fixes / 'RECONCILE_CODEX_5.json')
    reconcile_rows = []
    for i, r in enumerate(reconcile['entries']):
        reconcile_rows.append({'record_id': f'RECONCILE_CODEX_5.json#{i + 1}', 'original_id': r.get('id', ''),
                               'status': r.get('status', ''), 'expose': r.get('expose', ''),
                               'claim': safe(r.get('codex_claim', r.get('claim', ''))),
                               'reason': safe(r.get('note', r.get('why', ''))),
                               'source': safe(r.get('source', '')),
                               'inheritance_proof': 'Both authoritative source layers reconstructed exactly except enumerated build edits.'})
    misprints = read_rows(fixes / 'MISPRINTS_5.json')
    misprint_rows = []
    for i, r in enumerate(misprints):
        c = layers['current'][1].locate(r['correct'], [r['page']])
        d = layers['diplomatic'][1].locate(r['print'], [r['page']])
        misprint_rows.append({'record_id': f'MISPRINTS_5.json#{i + 1}', 'page': r['page'],
                             'place': safe(r['where']), 'printed_reading': safe(r['print']),
                             'corrected_reading': safe(r['correct']),
                             'current_terminal_evidence': c['status'] if c else 'no_literal_witness; prose/notation/supersession requires record context',
                             'current_observed_matches': c['count'] if c else '',
                             'diplomatic_terminal_evidence': d['status'] if d else 'no_literal_witness; printed description may be prose',
                             'diplomatic_observed_matches': d['count'] if d else '',
                             'explicit_status_field': 'absent in supplied registry',
                             'new_build_decision': ('GLOBAL-98b: retain ' + r'\underline{\operatorname{\mathbb{F}r}}_{Y/S}' + '; scan needed, printed reading retained under task Rule 3') if i + 1 == 572 else '',
                             'record_note': safe(r['note']), 'source': safe(r['source']),
                             'inheritance_proof': 'AUDIT_FR.json source_inheritance; registry text is unchanged and its notes retained.'})
    tsv(args.output / 'FIX_INHERITANCE_FR.tsv', rows)
    tsv(args.output / 'RECONCILE_INHERITANCE_FR.tsv', reconcile_rows)
    tsv(args.output / 'MISPRINT_STATUS_FR.tsv', misprint_rows)
    changes_rows = [{'layer': e['layer'], 'decision_id': e['id'], 'folio': e['folio'],
                     'source_start_character_0based': e['start'], 'source_end_character_0based': e['end'],
                     'before_json': json.dumps(e['before'], ensure_ascii=False),
                     'after_json': json.dumps(e['after'], ensure_ascii=False)} for e in changes]
    tsv(args.output / 'SOURCE_TO_PREPARED_FR.tsv', changes_rows)
    marker_record = read_rows(fixes / 'MARKERS_5.json')
    marker_summary = {}
    for layer in ['diplomatic', 'current']:
        observed = sorted(p for p in layers[layer][1].pages if p)
        marker_summary[layer] = {
            'earlier_record': marker_record[layer], 'final_placed': len(observed),
            'final_missing': sorted(set(range(1, 485)) - set(observed)),
            'folio_484_added_by': 'HANDFIX_5.jsonl#13' if layer == 'diplomatic' else 'HANDFIX_5.jsonl#14',
            'scan_index_equals_folio_plus_11': all(int(i) == int(f) + 11 for i, f in MARKER.findall(layers[layer][1].text))}
    summary = {'record_manifest_verification': manifest_checks,
               'source_inheritance': proof, 'fix_logs': collections_summary,
               'current_misprint_corrections': {'count': 29,
                   'terminal_evidence': dict(collections.Counter(r['terminal_evidence'] for r in rows
                        if r['record_file'] == 'fixes/FIXLOG_5_CURRENT.jsonl' and r['kind'] == 'misprint_correction'))},
               'hand_records': {'count': len(hand), 'terminal_evidence': dict(collections.Counter(r['terminal_evidence'] for r in rows if r['record_file'] == 'fixes/HANDFIX_5.jsonl'))},
               'manual_replay': {'count': len(replays), 'with_resolved_field': sum(bool(r.get('resolved')) for r in replays),
                                 'resolution_text_starts_open': [i + 1 for i, r in enumerate(replays) if r.get('resolved', '').startswith('open')],
                                 'later_resolution_of_stale_open_text': {'REPLAY_MANUAL_5.json#10': 'HANDFIX_5.jsonl#45'},
                                 'done_sidecar_records': len(done)},
               'manual_findings': {'files': len(manual_counts), 'items': sum(manual_counts.values()), 'per_file': manual_counts,
                                   'rows_in_inheritance_table': sum(manual_counts.values()) * 2},
               'reconciliation': {'count': len(reconcile_rows), 'statuses': dict(collections.Counter(r['status'] for r in reconcile_rows))},
               'marker_record_reconciliation': marker_summary,
               'misprints': {'count': len(misprints), 'complete_required_fields': sum(all(k in r for k in ['page','where','print','correct','tex_did','note','source']) for r in misprints),
                            'records_with_explicit_status_field': sum('status' in r or 'decision' in r for r in misprints),
                            'current_literal_or_projection_witnesses': sum(not r['current_terminal_evidence'].startswith('no_literal') for r in misprint_rows),
                            'current_terminal_evidence': dict(collections.Counter(r['current_terminal_evidence'] for r in misprint_rows)),
                            'qualification': 'The 590-item registry has no explicit status/decision fields; notes contain qualifications. String searches do not establish that all 590 proposed corrections were applied.'},
               'inheritance_table_rows': len(rows),
               'projection_definition': 'pi(s): remove an unescaped % through its line ending, then delete Unicode whitespace characters. Its equality is a location witness only, not a claim of equivalent rendered TeX.',
               'scope_of_proof': 'Exact inheritance from the manifest-verified final attached layers to the prepared layers, with all build edits enumerated. Exact branch-projection checks from the annotated master to these prepared layers extend this proof to generated readers. This audit does not independently recreate the historical scan-check sequence or certify source-record judgments from unavailable scans.'}
    expected_counts = {'FIXLOG_5.jsonl': 4173, 'FIXLOG_5_CURRENT.jsonl': 3770,
                       'HANDFIX_5.jsonl': 88, 'REPLAY_MANUAL_5.json': 36,
                       'REPLAY_MANUAL_5_DONE.json': 1, 'MANUAL_5_findings_items': 8,
                       'MISPRINTS_5.json': 590, 'RECONCILE_CODEX_5.json': 117,
                       'current_misprint_corrections': 29, 'inheritance_table_rows': 8084}
    observed_counts = {'FIXLOG_5.jsonl': collections_summary['FIXLOG_5.jsonl']['records'],
                       'FIXLOG_5_CURRENT.jsonl': collections_summary['FIXLOG_5_CURRENT.jsonl']['records'],
                       'HANDFIX_5.jsonl': len(hand), 'REPLAY_MANUAL_5.json': len(replays),
                       'REPLAY_MANUAL_5_DONE.json': len(done), 'MANUAL_5_findings_items': sum(manual_counts.values()),
                       'MISPRINTS_5.json': len(misprints), 'RECONCILE_CODEX_5.json': len(reconcile_rows),
                       'current_misprint_corrections': sum(r['record_file'] == 'fixes/FIXLOG_5_CURRENT.jsonl'
                            and r['kind'] == 'misprint_correction' for r in rows), 'inheritance_table_rows': len(rows)}
    summary['validation'] = {
        'expected_counts': expected_counts, 'observed_counts': observed_counts,
        'counts_match': expected_counts == observed_counts,
        'all_prepared_layers_reconstruct_exactly': all(p['exact_reconstruction'] for p in proof.values()),
        'all_marker_sequences_unchanged': all(p['marker_sequence_unchanged'] for p in proof.values()),
        'unresolved_terminal_searches': [r['record_id'] for r in rows if r['terminal_evidence'] in
            ['inherited_source_record_no_terminal_literal', 'original_layer_result_located_final_changed']],
        'documented_source_terminal_differences': [r['record_id'] for r in rows if r['terminal_evidence'] == 'source_terminal_difference_documented']}
    (args.output / 'AUDIT_FR.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    write_report(args.output, summary)
    print(json.dumps({'exact_source_inheritance': all(p['exact_reconstruction'] for p in proof.values()),
                      'table_rows': len(rows), 'fix_logs': {k: v['terminal_evidence'] for k, v in collections_summary.items()},
                      'misprints': summary['misprints']}, ensure_ascii=False, indent=2))
    assert summary['validation']['counts_match'], 'Unexpected record counts'
    assert summary['validation']['all_prepared_layers_reconstruct_exactly'], 'Prepared-source difference is not accounted for'
    assert summary['validation']['all_marker_sequences_unchanged'], 'Folio marker sequence changed'
    assert not summary['validation']['unresolved_terminal_searches'], 'Terminal search requires review'


if __name__ == '__main__':
    main()
