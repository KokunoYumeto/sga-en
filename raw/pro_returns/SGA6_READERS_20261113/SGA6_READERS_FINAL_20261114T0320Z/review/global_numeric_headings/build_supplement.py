#!/usr/bin/env python3
"""Occurrence-scoped numeric-heading typography supplement; no frozen edits."""
from pathlib import Path
import json,re,sys,hashlib,collections,csv
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'review/english'))
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH,split
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def dump(name,v):(HERE/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def write_rows(name,rows):(HERE/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))

rows=json.loads((HERE/'rendered_source_inventory.json').read_text())
assert len(rows)==49
assert not (HERE/'post_review_patches.jsonl').exists(),'Do not rerun against an already installed supplement'
before={};references={}
for layer in ['current','diplomatic']:
    page_set={};refs=[]
    for start,end in [(1,17),(429,464),(519,563)]:
        ps,ref=load_reviewed_pages(end,layer,start=start)
        page_set.update({p:t for p,t in ps.items() if any(r['page']==p for r in rows)})
        refs.append(ref)
    before[layer]=page_set;references[layer]=refs
    print('loaded '+layer,flush=True)
dump('input_pages.json',before)
dump('input_reference_records.json',references)

source_page_records={}
for folder in ['early','expose_vii','expose_x']:
    path=ROOT/'review'/folder/'page_status.jsonl'
    for i,line in enumerate(path.read_text().splitlines(),1):
        r=json.loads(line)
        if r.get('page') in before['current']:
            assert r.get('fully_checked') is True or r.get('checked_against_scan') is True
            source_page_records[r['page']]=dict(record=f'review/{folder}/page_status.jsonl#{i}',sha256=sha(line),record_value=r)

native_en_path=ROOT/'review/english/DRAFT_SGA6_EN_annotated_master.tex'
native_en=native_en_path.read_text();en_pages=split(native_en)
en_sources={p:'review/english/DRAFT_SGA6_EN_annotated_master.tex' for p in range(1,18)}
en_hashes={p:sha(native_en) for p in range(1,18)}
for folder in ['review/english/contributions/expose_vii','review/english/contributions/exposes_viii_x/snapshots/x519_594']:
    for path in sorted((ROOT/folder).glob('EN_*_P*.tex')):
        txt=path.read_text()
        for p,t in split(txt).items():
            en_pages[p]=t;en_sources[p]=path.relative_to(ROOT).as_posix();en_hashes[p]=sha(txt)

note=ROOT/'conventions/NOTE_6.txt'
note_text=note.read_text()
rule='NOTE_6 separately accepts section titles as subsection* without their source rule and a new paragraph after a run-in numbered heading. Its ordinary paragraph-number weight is a pending volume convention; the now-decided ordinary weight applies to these numeric-only labels too. Their existing structural command and every numeric/punctuation byte are retained.'
findings=[];patches=[];english=[];occurrences=[]
for n,r in enumerate(rows,1):
    p=r['page'];label=r['label'];sid=f'ASTRA-NUMERIC-HEADING-{p}-{label.rstrip(".").replace(".","-")}'
    assert r['new'].replace(r'\normalfont ','',1)==r['old']
    changes={}
    for layer in before:
        t=before[layer][p];assert t.count(r['old'])==1,(sid,layer,t.count(r['old']))
        u=t.replace(r['old'],r['new'],1)
        assert MATH.findall(t)==MATH.findall(u),(sid,'changed mathematical units')
        assert re.findall(r'\\SGAAuthorFoot(?:note|Mark|Text)\{[^}]+\}',t)==re.findall(r'\\SGAAuthorFoot(?:note|Mark|Text)\{[^}]+\}',u)
        changes[layer]=dict(before_sha256=sha(t),after_single_occurrence_sha256=sha(u),count=1)
    observation=(f'The printed numeric label {label} is in ordinary typed weight, with no rule beneath its digits, before the recorded prose. Fresh bounded primary-image inspection covers this label and adjoining lines; the previous complete-page review and its actual witness-use status remain separately attributed.')
    region=f'Numeric paragraph label {label}; PDF clip points {r["clip_points"]}; derived crop {r["crop"]}'
    finding=dict(source_id=sid,page=p,kind='font_convention',verdict='confirmed and explicitly transported in both layers',printed_reading=f'ordinary-weight numeric paragraph label {label}',image=r['image'],region=region,
        reason=observation+' '+rule+' The insertion of normalfont is confined to the heading argument. Removing that one declaration recovers the exact previous source bytes; it changes no number, punctuation, mathematical unit, note, destination or paragraph boundary.',
        change={'old':r['old'],'new':r['new']},forms='French diplomatic and current; corresponding English heading argument',
        is_misprint=False,source_audit=source_page_records[p],fresh_bounded_view={'crop':r['crop'],'crop_sha256':r['crop_sha256'],'inspection_sheet':r['inspection_sheet'],'scope':'label and adjoining source lines only','personally_viewed':True})
    findings.append(finding)
    patches.append(dict(page=p,layer='both',old=r['old'],new=r['new'],expected_count=1,source_id=sid,reason=finding['reason'],kind='font_convention'))
    occurrence={**r,'source_id':sid,'status':'fresh bounded primary label/first-line inspection complete; historical full-page record separately attributed','source_audit':source_page_records[p],'branch_anchor_checks':changes}
    occurrences.append(occurrence)
    et=en_pages[p];assert et.count(r['old'])==1,(sid,'English exact occurrence',et.count(r['old']))
    pos=et.index(r['old']);matches=list(re.finditer(r'\\sgaStableTarget(?:Inline)?\{[^}]+\}',et[:pos]));nearest=matches[-1].group() if matches else ''
    anchor=nearest if nearest and et[pos-len(nearest):pos]==nearest else ''
    english.append(dict(source_id=sid,page=p,printed_label=label,English_old=r['old'],English_new=r['new'],stable_target=anchor,
        exact_old_anchor=anchor+r['old'],exact_new_anchor=anchor+r['new'],expected_count=1,
        scope_start=r'\SGAPrintPage{'+str(p)+'}',scope_end=r'\SGAPrintPage{'+str(p+1)+'}',
        source_file=en_sources[p],source_file_sha256=en_hashes[p],English_page_sha256=sha(et),
        source_image=r['image'],source_region=region,
        instruction='Apply this exact heading-argument font wrapper after the aggregate translation spans, preserving the stable target and folio boundary. It is the identical both-form source typography transport; no apparatus variant is created. Do not modify the sealed raw contribution.'))

after={layer:dict(ps) for layer,ps in before.items()};checks=[]
for layer in after:
    for patch in patches:
        p=patch['page'];t=after[layer][p];assert t.count(patch['old'])==1
        after[layer][p]=t.replace(patch['old'],patch['new'],1)
    for p,t in before[layer].items():
        u=after[layer][p]
        assert MATH.findall(t)==MATH.findall(u)
        assert u.replace(r'\normalfont ','')==t.replace(r'\normalfont ','')
        checks.append(dict(layer=layer,page=p,before_sha256=sha(t),after_sha256=sha(u),mathematical_units=len(MATH.findall(t)),math_units_identical=True,
            exact_inverse_identity='Removing only the inserted normalfont declarations restores the previous page exactly.'))

write_rows('own_findings.jsonl',findings)
write_rows('post_review_patches.jsonl',patches)
dump('occurrences.json',occurrences)
dump('english_correspondence.json',english)
write_rows('english_correspondence.jsonl',english)
dump('validation.json',dict(occurrences=49,both_layer_patch_records=49,branch_applications=98,source_pages=len(before['current']),
    by_expose={'0':19,'VII':7,'X':23},by_command=dict(collections.Counter(r['command'] for r in rows)),
    fresh_bounded_primary_views=49,new_full_page_certifications=0,English_exact_anchors=49,mathematical_unit_changes=0,author_note_label_changes=0,
    rule_source='conventions/NOTE_6.txt',rule_source_sha256=sha(note_text),rule=rule,checks=checks))
(HERE/'HANDOFF.md').write_text('''# Numeric-only structural heading supplement

All49 numbered heading occurrences have fresh bounded primary-image observations and exact current/diplomatic transports. There are19 in Exposé0, seven inVII and23 inX, on42 source pages. The49 records with layer=both make98 branch applications. The37 subsection and12 subsubsection commands are retained; only a normalfont declaration is inserted inside each numeric argument. All digits, stops, spacing outside that argument, source-folio markers, mathematical units and original notes are unchanged.

This closes the numeric-heading category missed by the earlier77 standalone textbf removals. The earlier sealed convention package remains unchanged. NOTE_6 accepts the structural paragraph break and the typesetting of named section titles. It separately identifies ordinary paragraph-number weight as a volume decision. The label-only commands in this supplement carry precisely those ordinary source numerals; their command name does not create a new source title.

Every label and its adjoining source lines was personally inspected in the49 saved crops displayed on nine contact sheets. This bounded check does not recertify the whole pages. Exact historical full-page and witness observations remain attributed in each occurrence. The interdigit and terminal stops retain their previously adjudicated readings, including the NOTE_6 restoration of faint interdigit stops; this supplement changes only font weight.

Apply post_review_patches.jsonl after review/global_conventions/post_review_patches.jsonl. The source IDs are occurrence-specific, and every local anchor count is1 in each branch. Validation proves an exact inverse: remove the inserted normalfont declarations and every source page returns byte for byte to its former state. All mathematical-unit lists are unchanged.

For English, english_correspondence.jsonl gives49 exact folio-scoped wrapper anchors and their existing source-file hashes. Existing immediately adjacent stable destinations are included where present; a label with no such native destination receives no new one. Apply these during aggregate typography transport, leaving all sealed contributions untouched. Every numeral and heading command is the same on the French and English sides, so the same local normalfont declaration suffices. No author-text correction or new apparatus variant is introduced. Final French and English rendering remains with the respective builders.
''')
print(json.dumps(dict(occurrences=49,patches=49,applications=98,source_pages=len(before['current']),English_anchors=len(english))),flush=True)
