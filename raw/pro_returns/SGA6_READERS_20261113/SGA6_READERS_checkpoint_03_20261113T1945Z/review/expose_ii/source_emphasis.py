#!/usr/bin/env python3
"""Render inspected source emphasis as underlined words, preserving math bytes.

This local copy is used only after the Exposé II reviewer has individually
compared the emphasis groups on the specific folio being patched.
It does not choose new emphasis spans or alter mathematical font commands.
"""
import re

MATH = re.compile(
    r'\\begin\{(?:equation|align)\}.*?\\end\{(?:equation|align)\}'
    r'|(?<!\\)\\\[.*?(?<!\\)\\\]'
    r'|(?<!\\)\\\(.*?(?<!\\)\\\)'
    r'|(?<!\\)\$(?:[^$]|\\\$)*?(?<!\\)\$', re.S)
TOKEN = re.compile(
    MATH.pattern
    + r'|\\(?:SGAPrintPage|sgaStableTarget|SGAAuthorFootnote|SGAAuthorFootMark|SGAAuthorFootText|footnote|footnotetext|var)\{'
    + r'|(?<!\\)%[^\n]*(?:\n|$)', re.S)
ARG_COUNTS = {'SGAPrintPage': 1, 'sgaStableTarget': 1,
              'SGAAuthorFootnote': 2, 'SGAAuthorFootMark': 1,
              'SGAAuthorFootText': 2, 'footnote': 1,
              'footnotetext': 1, 'var': 3}


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
             'explicit_text_words_inside_math': []}

    def words(span):
        if not span.strip():
            return span
        lead = span[:len(span) - len(span.lstrip())]
        right = len(span.rstrip())
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
        return lead + r'\uline{' + span[len(lead):right] + '}' + tail

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
                if name == 'var':
                    pieces.append(r'\var{' + content(args[0]) + '}{' +
                                  content(args[1]) + '}{' + args[2] + '}')
                else:
                    pieces.append(body[m.start():j])
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
    expected_math = []
    for m in MATH.finditer(text):
        unit = m.group()
        replacements = []
        for start, end, body, replacement in changes:
            if m.start() <= start and end <= m.end():
                # The source also underlines lexical words placed in \text
                # within a display. These exact word-only replacements are
                # recorded; every other byte of that math unit is retained.
                if not re.search(r'\\text\{\s*$', text[m.start():start]) or not re.fullmatch(r"[A-Za-z ,.;:'-]+", body):
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
