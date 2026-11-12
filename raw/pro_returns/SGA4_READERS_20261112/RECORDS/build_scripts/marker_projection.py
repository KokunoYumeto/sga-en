"""Carry printed-page markers across an exact, source-backed replacement.

The character map is SequenceMatcher's explicit equal-span correspondence. A
marker inside an unequal span must sit on its boundary; otherwise the caller
must supply a reviewed placement. Nothing moves to the end of a long quotation.
"""
import difflib,re
MARKER=re.compile(r'\\SGApageno\{\d\}\{\d+\}')

def carry_markers(old,new):
    if MARKER.search(new):return new
    pieces=[];marks=[];last=0;length=0
    for match in MARKER.finditer(old):
        part=old[last:match.start()];pieces.append(part);length+=len(part)
        marks.append((length,match.group()));last=match.end()
    if not marks:return new
    pieces.append(old[last:]);plain=''.join(pieces)
    codes=difflib.SequenceMatcher(None,plain,new,autojunk=False).get_opcodes()
    located=[]
    for offset,marker in marks:
        choices=[]
        for tag,a,b,c,d in codes:
            if tag=='equal' and a<=offset<=b:choices.append(c+offset-a)
        if choices:target=choices[-1]
        else:
            boundaries=[j for tag,a,b,c,d in codes for i,j in [(a,c),(b,d)] if i==offset]
            if not boundaries:raise ValueError('Page marker lies inside a changed span; explicit placement required')
            target=boundaries[-1]
        located.append((target,marker))
    for target,marker in reversed(located):new=new[:target]+marker+new[target:]
    return new
