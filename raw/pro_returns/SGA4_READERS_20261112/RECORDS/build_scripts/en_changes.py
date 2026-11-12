"""Complete, replay-checked English comparisons against the released reader.

Both comparisons use UTF-8 text with LF line endings. The body comparison
selects the corrected branches, retains editorial-note text, removes TeX
comments, and supplies the same explicit page-marker alignment to the release.
The source comparison includes every generated-source change, including the
standalone preamble, paired selectors, front matter and documentary appendices.
"""
from en_common import *
from en_extra import selected_with_owners
import hashlib

DECISIONS=[
 dict(id='DEC-EN-CHANGE-LF',decision='For the exact-text comparisons only, decode UTF-8 and map CRLF/CR line endings to LF; report the original input byte checksum separately.'),
 dict(id='DEC-EN-STANDALONE',decision='Replace the omitted custom amsbook class by the system amsbook class, inline the supplied smfthm definitions, and retain the book branch of the twenty standalone exposé wrappers.'),
 dict(id='DEC-EN-MASTER-CONTROL',decision='One master selects diplomatic, corrected-with-apparatus and reading forms; variant markers, original-page margins and note visibility are controlled in the common preamble.'),
 dict(id='DEC-EN-FRONTMATTER',decision='Inline the credited bibliographic, contributor, rights and form-specific preface text supplied in the shared build records.'),
 dict(id='DEC-EN-HUMAN-DOSSIER',decision='Preserve every original released-English sisi pair, including typographic and identical alternatives, as attributed human records in diplomatic and corrected forms.'),
 dict(id='DEC-EN-AI-APPENDICES',decision='Inline the source-labelled correction apparatus, all643 unresolved dispute records, and the complete possible-misprint appendix in the corrected form only.'),
 dict(id='DEC-EN-COMPARISON-PROJECTION',decision='The body comparison selects the released second sisi readings and the generated corrected SGAvar readings, retains note contents, removes comments and apparatus marks, and uses the same explicit page-marker alignment. The separate complete-source comparison accounts for the selectors, comments, appendices and technical code.'),
 dict(id='DEC-EN-MP0664-HUMAN-PROJECTION',decision='The canonical MP0664 printed reference is2.1. The released human first leaf references XIV.subsec3.1 and would print3.1. Restore visible2.1 in the diplomatic body at the verified To prove clause, retain the corrected3.1, and preserve the complete original human pair unchanged in the attributed dossier.'),
 dict(id='DEC-EN-MP0777-HUMAN-PROJECTION',decision='Apply MP0777 to the complete fiber-product expression: the printed base and last factor are Z_1 and Z_1, while the corrected base and last factor are Z_1 and Z. The original tiny human subscript pair remains unchanged in the attributed human dossier.'),
 dict(id='DEC-EN-MP0801-HUMAN-PROJECTION',decision='The canonical opening bibliography delimiter is a square bracket in print and a parenthesis after correction. Preserve the original human square-bracket/deletion pair in the dossier, and set the corrected body delimiter to the recorded parenthesis.'),
 dict(id='DEC-EN-MP0820-HUMAN-PROJECTION',decision='Place the existing human empty/prime selector after f and before its shriek subscript so that the corrected prime belongs to f. The original human pair and its attribution remain unchanged in the dossier.'),
 dict(id='DEC-EN-HUMAN-CITED-REFERENCES',decision='The diplomatic body retains Orgogozo editorial notes, including eight citations to bibliography entries supplied only in his corrected leaves. Reproduce those eight exact released-English entries in a separately attributed diplomatic-only bibliography so that the retained human citations resolve. The original printed bibliography remains at its source location.'),
 dict(id='DEC-EN-AMSBOOK-TOC',decision='The installed standard amsbook class automatically puts starred chapters in the table of contents. Remove an immediately following explicit chapter ToC entry only when its title exactly equals that starred chapter, preventing duplicate generated headings.'),
 dict(id='DEC-EN-HUMAN-NOTE-VISIBILITY',decision='Unwrap the five explicitly reviewed English SGAArchiveOnly notes at X46/51/52 and XVI232/246, preserving every byte of each existing nde argument. The human notes become visible at their source locations in diplomatic and corrected forms, while the common nde selector omits them from reading form. Wrap the exact IV465 inline human note marker and text in SGAeditor so the printed surrounding footnote remains in every form and that editorial insertion is omitted in reading form. The two release-generated VIII archive notices remain guarded; all129 original French human-note arguments are preserved in the separate attributed documentary supplement.'),
 dict(id='DEC-EN-APPARATUS-MARK-LAYOUT',decision='Render each corrected-form variant mark as a small linked dagger, retaining its exact app:EN-V identifier target and the full source identifier in the corresponding apparatus or human dossier. Full inline identifiers widened nine formula or diagram locations beyond the physical page edge in PDF inspection. Compact marks retain every link while preserving the mathematical layout.'),
 dict(id='DEC-EN-XVII275-DIAGRAM-LAYOUT',decision='Enclose only XVII275 diagram(2) in a restricted horizontal math box inside its existing vertical center. In the corrected form, its linked annotations otherwise started a full-width paragraph inside the vertical box and pushed the adjoining condition beyond the page edge. Every diagram token, variant link, condition and equation tag is retained; this changes only the TeX box dimensions.'),
]

def sha(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()

def select_sisi(text):
    edits=[]
    for m in active_matches(r'\\sisi\b',text):
        if any(a<=m.start()<b for a,b,_ in edits):continue
        line=text[text.rfind('\n',0,m.start())+1:m.start()]
        if re.search(r'\\(?:def|newcommand|renewcommand|providecommand)',line):continue
        try:
            _,_,j,_=group(text,m.end());c,_,end,_=group(text,j)
        except ValueError:continue
        c=select_sisi(c)
        if c and c[0].isalpha() and re.search(r'\\[A-Za-z@]+$',text[:m.start()]):c=' '+c
        if end<len(text) and text[end].isalpha():
            if re.search(r'\\[A-Za-z]+$',c) or (not c and re.search(r'\\[A-Za-z]+$',text[:m.start()])):c+=' '
        edits.append((m.start(),end,c))
    return replace_spans(text,edits)

def apply_mapped(text,owners,edits):
    out=[];tags=[];cursor=0
    for a,b,replacement in sorted(edits):
        if a<cursor:continue
        out.append(text[cursor:a]);tags.extend(owners[cursor:a]);out.append(replacement);tags.extend(['']*len(replacement));cursor=b
    out.append(text[cursor:]);tags.extend(owners[cursor:]);return ''.join(out),tags

def body(text,generated=False):
    a=text.index(r'\mainmatter')+len(r'\mainmatter');b=text.index(r'\backmatter',a)
    text=text[a:b]
    if generated:
        # Quiet Xy-pic selectors append all their original entry marks. Bind
        # those exact entry IDs to the diagram text for the change provenance.
        edits=[]
        for m in active_matches(r'\\SGAquietvar\b',text):
            try:
                _,_,j,_=group(text,m.end());_,_,j,_=group(text,j);ident,start,end,_=group(text,j)
            except ValueError:continue
            if ident!='diagram':continue
            ids=re.match(r'(?:\\SGAvariantmark\{EN-V\d+\})+',text[end:])
            if ids:edits.append((start,end,'{'+','.join(re.findall(r'EN-V\d+',ids.group()))+'}'))
        text=replace_spans(text,edits)
        text,owners=selected_with_owners(text,True)
    else:
        text=select_sisi(text);owners=['']*len(text)
    edits=[]
    for m in active_matches(r'\\SGAvariantmark\b',text):
        try:_,_,end,_=group(text,m.end());edits.append((m.start(),end,''))
        except ValueError:pass
    for m in re.finditer(r'(?<!\\)%[^\n]*',text):edits.append((m.start(),m.end(),''))
    text,owners=apply_mapped(text,owners,edits)
    return sanitize(text),owners

def compare(before,after,comparison,variants,events,owners=None):
    al=before.splitlines(keepends=True);bl=after.splitlines(keepends=True)
    ao=[0];bo=[0]
    for x in al:ao.append(ao[-1]+len(x))
    for x in bl:bo.append(bo[-1]+len(x))
    byid={v['id']:v for v in variants}
    rows=[];replay=[];cursor=0
    markers=[(m.start(),m.group(1),m.group(2),m.group(3)) for m in re.finditer(r'\\SGApage\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}',after)]
    offsets=[p[0] for p in markers]
    main=after.find(r'\mainmatter');back=after.find(r'\backmatter')
    for tag,a,b,c,d in difflib.SequenceMatcher(None,al,bl,autojunk=True).get_opcodes():
        if tag=='equal':continue
        old=''.join(al[a:b]);new=''.join(bl[c:d]);pos=bo[c]
        idx=bisect.bisect_right(offsets,pos)-1
        loc=markers[idx] if idx>=0 else None
        page=(loc[1]+':'+loc[3]) if loc else 'frontmatter'
        place=('Exposé '+loc[2]) if loc else 'Standalone preamble / front matter'
        sources=set()
        if comparison=='complete generated source' and back>=0 and pos>=back:
            page='backmatter';place='Human dossier and source-labelled AI appendices'
            sources.update(['DEC-EN-HUMAN-DOSSIER','DEC-EN-AI-APPENDICES'])
        elif comparison=='complete generated source' and main>=0 and pos<main:
            sources.update(['DEC-EN-STANDALONE','DEC-EN-MASTER-CONTROL','DEC-EN-FRONTMATTER'])
        else:
            ids=set(re.findall(r'EN-V\d+',old+new))
            if owners is not None:
                for owner in set(owners[bo[c]:bo[d]]):ids.update(owner.split(','))
            for ident in ids:
                if ident in byid:sources.update(byid[ident]['source'].split('; '))
            if re.search(r'\\begin\{enonce\*\}',old+new):sources.add('FR-ED93-LABELS')
            if r'\Pi' in old and r'\pi' in new:sources.add('FR-ED93-PI')
            if r'\mathsf{e}' in old and r'\mathcal{C}' in new:sources.add('FR-ED93-CHAMP')
            for e in events:
                ep=str(e['page'])
                if loc and ep not in ['all',loc[3]] and loc[3] not in ep.split(','):continue
                ea=e['after'];eb=e['before']
                if (len(ea)>8 and ea in new) or (len(eb)>8 and eb in old):sources.update(e['source'].split('; '))
            if r'\SGApage' in old+new:sources.add('PAGES.json; DEC-EN-MASTER-CONTROL')
            if not sources:sources.add('DEC-EN-MASTER-CONTROL' if comparison=='complete generated source' else 'DEC-EN-COMPARISON-PROJECTION')
        rows.append(dict(page=page,place=place,before=old,after=new,source='; '.join(sorted(sources)),kind=tag,comparison=comparison,before_line_start=a+1,before_line_end=b,after_line_start=c+1,after_line_end=d))
        replay.extend(al[cursor:a]);replay.append(new);cursor=b
    replay.extend(al[cursor:]);reconstructed=''.join(replay)
    assert reconstructed==after,comparison
    return rows,dict(comparison=comparison,hunks=len(rows),before_characters=len(before),after_characters=len(after),before_sha256=sha(before),after_sha256=sha(after),reconstructed_sha256=sha(reconstructed),exact_reconstruction=True)

def build(master,variants,events):
    from build_en import page_markers,strip_standalone_preambles
    original=RELEASE.read_text()
    marked=page_markers(original)
    # Remove the same standalone wrappers before selecting the body; the full
    # raw-source comparison below retains these deletions explicitly.
    before,_=body(strip_standalone_preambles(marked),False)
    after,owners=body(master,True)
    rows,audit1=compare(before,after,'selected corrected body',variants,events,owners)
    generated='% Generated from SGA4_EN_annotated_master.tex.\n\\def\\SGAform{1}\n'+master
    rawrows,audit2=compare(sanitize(original),generated,'complete generated source',variants,events)
    rows+=rawrows
    for i,row in enumerate(rows,1):row['id']='EN-CHANGE-%05d'%i
    write_tsv(RECORDS/'CHANGES_EN.tsv',rows,['page','place','before','after','source','kind','comparison','id','before_line_start','before_line_end','after_line_start','after_line_end'])
    (RECORDS/'EN_CHANGE_AUDIT.json').write_text(json.dumps(dict(released_file='en/C_release_20261112/04_SGA4_EN_COMPLETE_READER.tex',released_original_bytes_sha256=hashlib.sha256(RELEASE.read_bytes()).hexdigest(),newline_policy='UTF-8 decoded text, CRLF/CR to LF; complete source reconstruction equals the final corrected reader bytes.',comparisons=[audit1,audit2]),ensure_ascii=False,indent=2)+'\n')
    (RECORDS/'EN_CHANGE_DECISIONS.json').write_text(json.dumps(DECISIONS,ensure_ascii=False,indent=2)+'\n')
    return [audit1,audit2]

if __name__=='__main__':
    master=(ROOT/'output/en/SGA4_EN_annotated_master.tex').read_text()
    variants=json.loads((RECORDS/'EN_VARIANTS.json').read_text())
    events=list(csv.DictReader((RECORDS/'EN_BUILD_EVENTS.tsv').open(),delimiter='\t'))
    print(json.dumps(build(master,variants,events),indent=2))
