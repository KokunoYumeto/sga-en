#!/usr/bin/env python3
"""Render inspected source emphasis as underlined words, preserving math bytes.

The caller supplies explicitly reconstructed intervals and exact plain-word
exceptions.  The final source convention record preserves edge punctuation,
literal mathematics, existing direct rules and original author-note labels.
This formatter chooses no new emphasis scope.  Source-specific plain terms
are carried by SGAPlainWords wrappers inserted by an audited occurrence map.
"""
import re

MATH = re.compile(
    r'\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}.*?'
    r'\\end\{(?:equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}'
    r'|(?<!\\)\\\[.*?(?<!\\)\\\]'
    r'|(?<!\\)\\\(.*?(?<!\\)\\\)'
    r'|(?<!\\)\$(?:[^$]|\\\$)*?(?<!\\)\$', re.S)
TOKEN = re.compile(
    MATH.pattern
    + r'|\\(?:SGAPrintPage|sgaStableTarget|sgaStableTargetInline|SGAAuthorFootnote|SGAAuthorFootMark|SGAAuthorFootText|footnote|footnotetext|var|uline|SGAPlainWords|emph)\{'
    + r'|(?<!\\)%[^\n]*(?:\n|$)', re.S)
ARG_COUNTS = {'SGAPrintPage': 1, 'sgaStableTarget': 1, 'sgaStableTargetInline': 1,
              'SGAAuthorFootnote': 2, 'SGAAuthorFootMark': 1,
              'SGAAuthorFootText': 2, 'footnote': 1,
              'footnotetext': 1, 'var': 3, 'uline': 1,
              'SGAPlainWords': 1, 'emph': 1}


def braced(text, start):
    assert text[start] == '{'
    depth = 1
    i = start + 1
    while depth:
        if i >= len(text):
            raise ValueError('Unclosed emphasis/control argument')
        if text[i] == '\\':
            i += 2
            continue
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1
    return text[start + 1:i - 1], i


def underline_words(text):
    stats = {'inspected_emphasis_groups': 0, 'underlined_word_spans': 0,
             'explicit_text_words_inside_math': [], 'plain_occurrence_wrappers': [],
             'preserved_direct_uline_groups': 0, 'punctuation_only_spans': []}

    def words(span):
        if not span.strip():
            return span
        # The directly reviewed convention leaves only edge punctuation plain;
        # punctuation internal to a lexical span stays in that same span.
        edge = ' \t\r\n.,;:!?()[]«»~'
        left = 0
        right = len(span)
        while left < right and span[left] in edge:
            left += 1
        while right > left and span[right - 1] in edge:
            i = right - 2
            escapes = 0
            while i >= left and span[i] == '\\':
                escapes += 1
                i -= 1
            if escapes % 2:
                break
            right -= 1
        if left == right or not re.search(r'[A-Za-zÀ-ÿ]', span[left:right]):
            stats['punctuation_only_spans'].append(span)
            return span
        # A TeX control-space is the two-character token backslash + space.
        # Moving that space outside the closing brace turns the brace into
        # an escaped literal, leaving the underline argument unclosed.
        slash_count = 0
        i = right - 1
        while i >= 0 and span[i] == '\\':
            slash_count += 1
            i -= 1
        if slash_count % 2 and right < len(span):
            right += 1
        tail = span[right:]
        stats['underlined_word_spans'] += 1
        return span[:left] + r'\uline{' + span[left:right] + '}' + tail

    def content(body):
        pieces = []
        pos = 0
        while True:
            m = TOKEN.search(body, pos)
            if m is None:
                pieces.append(words(body[pos:]))
                break
            pieces.append(words(body[pos:m.start()]))
            command = re.fullmatch(r'\\([A-Za-z]+)\{', m.group())
            if command:
                name = command.group(1)
                j = m.end() - 1
                args = []
                for _ in range(ARG_COUNTS[name]):
                    arg, j = braced(body, j)
                    args.append(arg)
                if name == 'SGAPlainWords':
                    pieces.append(args[0])
                    stats['plain_occurrence_wrappers'].append(args[0])
                elif name == 'emph':
                    raise ValueError('Nested emphasis lacks an exact plain or ruled occurrence map')
                elif name == 'var':
                    pieces.append(r'\var{' + content(args[0]) + '}{' +
                                  content(args[1]) + '}{' + args[2] + '}')
                else:
                    pieces.append(body[m.start():j])
                    if name == 'uline':
                        stats['preserved_direct_uline_groups'] += 1
                pos = j
            else:
                pieces.append(m.group())
                pos = m.end()
        return ''.join(pieces)

    out = []
    changes = []
    pos = 0
    while True:
        start = text.find(r'\emph{', pos)
        if start < 0:
            out.append(text[pos:])
            break
        out.append(text[pos:start])
        body, end = braced(text, start + 5)
        replacement = content(body)
        out.append(replacement)
        changes.append((start, end, body, replacement))
        stats['inspected_emphasis_groups'] += 1
        pos = end
    result = ''.join(out)
    if r'\SGAPlainWords{' in result:
        raise ValueError('A plain occurrence wrapper lies outside its inspected emphasis group')
    expected_math = []
    for m in MATH.finditer(text):
        unit = m.group()
        replacements = []
        for start, end, body, replacement in changes:
            if m.start() <= start and end <= m.end():
                # The source also underlines lexical words placed in \text
                # within a display. These exact word-only replacements are
                # recorded; every other byte of that math unit is retained.
                if not re.search(r'\\text\{\s*$', text[m.start():start]) or not re.fullmatch(r"[A-Za-zÀ-ÿ ,.;:'-]+", body):
                    raise ValueError('Unreviewed emphasis command inside mathematics')
                replacements.append((start - m.start(), end - m.start(), replacement))
                stats['explicit_text_words_inside_math'].append({
                    'before': text[start:end], 'after': replacement})
        for start, end, replacement in reversed(replacements):
            unit = unit[:start] + replacement + unit[end:]
        expected_math.append(unit)
    if expected_math != [m.group() for m in MATH.finditer(result)]:
        raise ValueError('Emphasis rendering changed a literal mathematical unit')
    return result, stats
