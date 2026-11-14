#!/usr/bin/env python3
"""Compare and transport exact paragraph separators at original folio joins.

This removes only helper-added empty lines or restores an omitted separator.
Original folio comments, visible-marker calls and hyperlink targets stay in place.
The source-packet basis is the reviewed French text, not a new image reading.
"""
from pathlib import Path
import hashlib, json, re
from difflib import SequenceMatcher
from english_typography import MARK
from reviewed_french import load_reviewed_pages

EN = Path(__file__).resolve().parent
OUT = EN / 'aggregate'
ZERO = r'\\(?:SGAPrintPage|sgaStableTarget(?:Inline)?)\{[^{}]*\}'
COMMENT = re.compile(r'(?<!\\)%[^\n]*(?:\n|$)')


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def clean(body):
    # The first newline belongs to the preceding folio-comment line.
    if body.startswith('\n'):
        body = body[1:]
    # A line containing only a zero-width generated command is not an empty
    # TeX source line. Remove that whole line for separator classification.
    body = re.sub(r'(?m)^[ \t]*' + ZERO + r'[ \t]*(?:%[^\n]*)?\n', '', body)
    body = re.sub(ZERO, '', body)
    return COMMENT.sub('', body)


def is_break(left, right):
    left, right = clean(left), clean(right)
    tail = re.search(r'\s*$', left).group()
    head = re.match(r'\s*', right).group()
    return tail.count('\n') >= 2 or head.count('\n') >= 1


def squash_tail(body):
    # Retain every command/comment byte; remove empty lines only in the final
    # whitespace / nonprinting-target suffix.
    lines = body.splitlines(keepends=True)
    k = len(lines)
    while k:
        line = lines[k - 1]
        stripped = line.strip()
        if not stripped or stripped.startswith('%') or re.fullmatch(ZERO + r'[ \t]*(?:%[^\n]*)?', stripped):
            k -= 1
        else:
            break
    suffix = ''.join(line for line in lines[k:] if line.strip())
    prefix = ''.join(lines[:k])
    return prefix + suffix


def squash_head(body):
    # Keep the comment-line terminator, then all generated commands/comments,
    # but no empty helper separator before the first author token.
    first = '\n' if body.startswith('\n') else ''
    rest = body[len(first):]
    lines = rest.splitlines(keepends=True)
    k = 0
    while k < len(lines):
        stripped = lines[k].strip()
        if not stripped or stripped.startswith('%') or re.fullmatch(ZERO + r'[ \t]*(?:%[^\n]*)?', stripped):
            k += 1
        else:
            break
    return first + ''.join(line for line in lines[:k] if line.strip()) + ''.join(lines[k:])


def repair(source, french=None):
    if french is None:
        french, _ = load_reviewed_pages(700, 'current', start=1)
    diplomatic, _ = load_reviewed_pages(700, 'diplomatic', start=1)
    marks = list(MARK.finditer(source))
    parts = [source[m.end():marks[i + 1].start() if i + 1 < len(marks) else len(source)]
             for i, m in enumerate(marks)]
    original_parts = list(parts)
    numeric = {int(m[1]):i for i,m in enumerate(marks) if m[1].isdigit()}
    records = []
    for page in range(1, 700):
        i, j = numeric[page], numeric[page + 1]
        assert j == i + 1
        left, right = parts[i], parts[j]
        before = is_break(left, right)
        desired = is_break(french[page], french[page + 1])
        assert desired == is_break(diplomatic[page], diplomatic[page+1]), page
        decision = 'Reviewed French paragraph separator transported to the same author-text boundary.'
        if page == 84:
            desired = False
            decision = ('Root direct primary98-bottom/99-top inspection: folio85 opening continues 1.1.3; '
                        'the blank padding of the unprinted local macro block is not an author paragraph.')
        if page in [689, 690]:
            records.append(dict(left_folio=page,right_folio=page+1,
                status='Source-certified blank folio690; no paragraph transport across the blank leaf.',
                changed=False,source_left_sha256=sha(french[page]),source_right_sha256=sha(french[page+1])))
            continue
        if before != desired:
            if desired:
                left = left.rstrip('\n') + '\n\n'
            else:
                left = squash_tail(left)
                right = squash_head(right)
            assert is_break(left, right) == desired, (page, desired, repr(left[-150:]), repr(right[:150]))
            assert re.sub(r'\s+', '', parts[i]+parts[j]) == re.sub(r'\s+', '', left+right)
        records.append(dict(left_folio=page,right_folio=page+1,
            source_paragraph_break=desired,English_before_break=before,English_after_break=is_break(left,right),
            changed=before!=desired,status=decision,
            source_left_sha256=sha(french[page]),source_right_sha256=sha(french[page+1]),
            source_left_tail=french[page][-240:],source_right_head=french[page+1][:240],
            English_left_before=parts[i][-300:],English_right_before=parts[j][:300],
            English_left_after=left[-300:],English_right_after=right[:300]))
        parts[i],parts[j]=left,right
    rebuilt = source[:marks[0].start()] + ''.join(m.group()+part for m,part in zip(marks,parts))
    assert re.sub(r'\s+', '', source) == re.sub(r'\s+', '', rebuilt)
    # The source527 comment is inside equation1.3.9, but its visible folio call
    # is correctly after the closing command. Its extra helper blank below
    # that call also separates 'where' from the displayed formula.
    old = '\\end{equation}\n\\SGAPrintPage{527}%\n\nwhere '
    new = '\\end{equation}\n\\SGAPrintPage{527}%\nwhere '
    assert rebuilt.count(old) == 1
    rebuilt = rebuilt.replace(old,new,1)
    special = dict(id='EN-JOIN-527-VISIBLE',old=old,new=new,
        source='Reviewed folio527 begins end{equation}, immediately followed by où, with no blank paragraph separator.',
        printed_content_unchanged=True,visible_folio_outside_math=True)
    final_marks=list(MARK.finditer(rebuilt))
    final_parts=[rebuilt[m.end():final_marks[i+1].start() if i+1<len(final_marks) else len(rebuilt)]
                 for i,m in enumerate(final_marks)]
    edits=[]
    for i,(old,new) in enumerate(zip(original_parts,final_parts)):
        if old==new:
            continue
        for tag,a,b,c,d in SequenceMatcher(None,old,new,autojunk=False).get_opcodes():
            if tag=='equal':
                continue
            assert not old[a:b].strip() and not new[c:d].strip()
            edits.append(dict(folio=marks[i][1],old_start=marks[i].end()+a,
                new_start=final_marks[i].end()+c,old=old[a:b],new=new[c:d]))
    forward=source
    for edit in reversed(edits):
        a=edit['old_start'];b=a+len(edit['old'])
        assert forward[a:b]==edit['old']
        forward=forward[:a]+edit['new']+forward[b:]
    assert forward==rebuilt
    reverse=rebuilt
    for edit in reversed(edits):
        a=edit['new_start'];b=a+len(edit['new'])
        assert reverse[a:b]==edit['new']
        reverse=reverse[:a]+edit['old']+reverse[b:]
    assert reverse==source
    report = dict(method='Exact comment-aware source separator comparison; only empty newline separators change.',
        source_basis='Current reviewed French loader; all 699 numeric adjacent boundaries recorded, with source-certified blank690 handled explicitly.',
        source_before_sha256=sha(source),source_after_sha256=sha(rebuilt),
        numeric_join_records=len(records),changed_boundaries=sum(r['changed'] for r in records),
        nonwhitespace_tokens_identical=True,both_French_branch_separator_patterns_identical=True,
        exact_whitespace_edits=edits,forward_and_reverse_reconstruction_pass=True,
        records=records,special_visible_marker_transport=[special],
        limitation='Paragraph-boundary transport from already reviewed source packets; no new scan-reading claim and no alteration of words, symbols, notes, targets or folio markers.')
    return rebuilt,report


if __name__ == '__main__':
    original=(OUT/'SGA6_EN_raw_current.tex').read_text()
    result,report=repair(original)
    (OUT/'FOLIO_JOIN_PROPOSAL.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (OUT/'SGA6_EN_joined_proposal.tex').write_text(result)
    print(json.dumps({k:report[k] for k in ['numeric_join_records','changed_boundaries','nonwhitespace_tokens_identical']}))
    for r in report['records']:
        if r['changed']:
            print(r['left_folio'], 'paragraph' if r['source_paragraph_break'] else 'continuation',
                  repr(clean(r['English_left_before'])[-60:]),repr(clean(r['English_right_after'])[:70]))
