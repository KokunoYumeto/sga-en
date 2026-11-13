"""Exact relocation of one inherited English editorial footnote.

The source bodies stay frozen. The reader wrapper removes this non-authorial
footnote from the body and preserves its full payload in the corrected-only
unresolved-notes appendix. The ledger permits exact reversal of the extraction.
"""
from __future__ import annotations
import hashlib
import re

DECISION = 'EN-INHERITED-0046-P43'
EVIDENCE = 'en/evidence/controls/standalone/sga5/controls/REMOVED_READER_PROSE_SGA5_001_002.texfrag'
SOURCE = 'en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex'
NOTE_PREFIX = r'\footnote{\emph{Editorial note.} The ordinary-induction line is not unambiguously legible in the printed source.'


def digest(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def group_end(s, begin):
    assert s[begin] == '{'
    depth, i = 1, begin + 1
    while i < len(s):
        if s[i] == '\\':
            m = re.match(r'\\(?:[A-Za-z@]+|.)', s[i:], re.S)
            assert m
            i += m.end()
            continue
        if s[i] == '%':
            end = s.find('\n', i)
            i = len(s) if end < 0 else end + 1
            continue
        depth += (s[i] == '{') - (s[i] == '}')
        i += 1
        if depth == 0:
            return i
    raise AssertionError('Unclosed editorial footnote')


def locate_note(s):
    assert s.count(NOTE_PREFIX) == 1, 'Expected exactly one inherited p43 editorial footnote'
    start = s.index(NOTE_PREFIX)
    brace = start + len(r'\footnote')
    end = group_end(s, brace)
    return start, end, s[brace + 1:end - 1]


def mask_editorial_note(s):
    """Keep all offsets while excluding inherited editorial prose from counts."""
    start, end, _ = locate_note(s)
    return s[:start] + ''.join('\n' if c == '\n' else ' ' for c in s[start:end]) + s[end:]


def relocate_en_note(s):
    start, end, payload = locate_note(s)
    removed = s[start:end]
    body = s[:start] + s[end:]
    assert body[:start] + removed + body[start:] == s
    before_ids = re.findall(r'\}\{((?:EN)-\d{4}|R98-\d{2})\}', s)
    after_ids = re.findall(r'\}\{((?:EN)-\d{4}|R98-\d{2})\}', body)
    before_markers = re.findall(r'%{5,}[ \t]*scan idx[ \t]+\d+[ \t]*\|[ \t]*folio[ \t]+\d+[ \t]*%+', s)
    after_markers = re.findall(r'%{5,}[ \t]*scan idx[ \t]+\d+[ \t]*\|[ \t]*folio[ \t]+\d+[ \t]*%+', body)
    assert before_ids == after_ids and len(before_ids) == 879
    assert before_markers == after_markers and len(before_markers) == 793
    remaining = []
    for pattern in [r'Editorial note', r'French-control reading', r'without claiming that the scan',
                    r'This edition retains', r'needs the scan']:
        for m in re.finditer(pattern, body, re.I):
            remaining.append({'pattern': pattern, 'offset': m.start(), 'context': body[max(0, m.start() - 50):m.end() + 90]})
    assert not remaining, remaining
    appendix = '\n'.join([
        r'\section*{Inherited English editorial note}',
        r'\begingroup\small',
        r'\medskip\noindent\textbf{' + DECISION + r' (folio 43; Exposé I, 4.6).}\par',
        r'This inherited editorial footnote is preserved here in full. Its source record is SGA5-READER-PROSE-002. The supplied body readings remain unchanged; the additional proposed readings require the unavailable scan.\par',
        r'\begin{quote}',
        payload,
        r'\end{quote}',
        r'\noindent\textit{Sources: }\nolinkurl{' + EVIDENCE + r'}; \texttt{MISPRINTS\_5:0054}; \texttt{MISPRINTS\_5:0055}. Status: needs the scan.',
        r'\endgroup',
        r'\clearpage',
        '',
    ])
    ledger = {
        'id': DECISION, 'page': 43, 'place': 'Exposé I, 4.6',
        'kind': 'wrapper-level editorial-note relocation',
        'body_before_sha256': digest(s), 'body_after_sha256': digest(body),
        'start_before': start, 'end_before': end, 'start_after': start,
        'before': removed, 'after': '', 'payload': payload,
        'payload_preserved_exactly_once_in_appendix': appendix.count(payload) == 1,
        'exact_reverse_replay': True,
        'source': EVIDENCE + ':SGA5-READER-PROSE-002; ' + SOURCE + '; MISPRINTS_5:0054; MISPRINTS_5:0055',
        'disposition': 'Retain supplied mathematical readings. Move this inherited English-only editorial note from all reader bodies to the corrected-only unresolved appendix; needs the scan.',
        'master_call_ids_before': before_ids, 'master_call_ids_after': after_ids,
        'master_calls_unchanged': True, 'master_call_count': len(after_ids),
        'folio_markers_unchanged': True, 'folio_marker_count': len(after_markers),
        'remaining_matching_editorial_prose': remaining,
        'shared_unresolved_notes': 30, 'additional_inherited_English_notes': 1,
        'unresolved_English_notes_total': 31,
    }
    return body, appendix, ledger
