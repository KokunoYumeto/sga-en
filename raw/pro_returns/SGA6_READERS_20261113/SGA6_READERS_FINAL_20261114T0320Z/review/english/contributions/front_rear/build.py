#!/usr/bin/env python3
"""Build the complete original front and rear matter from reviewed page packets.

New-edition credits are inserted separately by the common English generator.
The two exact native replacements here contain only the original printed work.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,re,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'review/english'))
from verify_reviewed_english import MATH

FRONT=['cover','cover-verso','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
REAR=[f'rear-{n}' for n in range(715,721)]
KEYS=FRONT+REAR
COPIED=['cover-verso','II']+REAR
MARKER=re.compile(r'%%%%%%%%%%\s+scan idx\s+(\d+)\s*\|\s*folio\s+([^\s]+)\s+%%%%%%%%%%')

def sha(text):return hashlib.sha256(text.encode()).hexdigest()
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def jsonl(path,rows):path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
def target_ids(text):return re.findall(r'\\sgaStableTarget(?:Inline)?\{([^}]+)\}',text)

def page(key):
    packet=HERE/'source_packets'/key
    original=(packet/'current.tex').read_text()
    match=MARKER.match(original)
    assert match and match.group(2)==key,key
    units=json.loads((packet/'units.json').read_text())
    text=(HERE/'translations'/f'{key}.tex').read_text()
    used=Counter(int(n) for n in re.findall(r'@@M(\d+)@@',text))
    assert used==Counter(range(len(units))),(key,used,len(units))
    text=re.sub(r'@@M(\d+)@@',lambda m:units[int(m.group(1))],text)
    assert r'\end{document}' not in text,key
    if key in COPIED:
        # These English-language publisher texts and multilingual bibliographic
        # titles are literal source copies, with only the page marker removed.
        copied=original[match.end()+1:].replace(r'\end{document}','')
        assert copied==text,(key,'copied publisher content differs')
    visible=r'\SGAPrintPage{'+key+'}%\n'
    if '@@PAGE_MARK@@' in text:
        assert key=='VIII' and text.count('@@PAGE_MARK@@')==1
        text=text.replace('@@PAGE_MARK@@',visible)
    else:text=visible+text
    assert '@@' not in text,key
    return match.group()+'\n'+text

def records():
    native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
    pieces={k:page(k) for k in KEYS}
    front=''.join(pieces[k] for k in FRONT)
    rear=''.join(pieces[k] for k in REAR)
    a=native.index(r'\begin{document}')+len(r'\begin{document}')
    b=native.index(r'\sgaStableTarget{sga6.e00.expose}',a)
    old_front=native[a:b]
    assert target_ids(old_front)==target_ids(front)==[
        'sga6.front.preface','sga6.front.introduction','sga6.front.table-of-contents']
    assert native.count(r'\end{document}')==1
    front='\n'+front
    (HERE/'EN_ORIGINAL_FRONTMATTER.tex').write_text(front)
    (HERE/'EN_ORIGINAL_REARMATTER.tex').write_text(rear)
    patches=[
        dict(id='EN-CONTRIB-ORIGINAL-FRONT',page='front:cover–XII',old=old_front,new=front,
             status='accepted: complete original front matter compared paragraph by paragraph with reviewed French',
             source='review/front; review/front_amendments; review/publisher_notice_recovery',
             reason='Restore all 14 physical front leaves, source page breaks, complete author Preface and Introduction, full contents and original publisher material. Retain the three native stable targets. Eight previous partial front patches are superseded by this exact complete native-span replacement.',
             supersedes=['EN-INTRO-001','EN-INTRO-002','EN-TOC-I','EN-TOC-III','EN-TOC-IV','EN-TOC-VI','EN-TOC-VII','EN-TOC-IX']),
        dict(id='EN-CONTRIB-ORIGINAL-REAR',page='rear:715–720',old=r'\end{document}',new=rear+r'\end{document}',
             status='accepted: all six rear physical leaves transferred literally from reviewed source',
             source='review/backmatter',
             reason='Insert the two blank leaves, all 188 publisher catalogue entries in their bibliographic languages, and both ISBN lines after the source700 index. The unchanged unique document terminator follows the insertion.')]
    for p in patches:
        p['native_span_sha256']=sha(p['old']);p['new_span_sha256']=sha(p['new'])
        assert native.count(p['old'])==1,p['id']
    jsonl(HERE/'translation_spans.jsonl',patches)
    decisions={}
    for folder in ['front','backmatter','publisher_notice_recovery','front_amendments']:
        for name in ['decisions.jsonl','own_findings.jsonl']:
            path=ROOT/'review'/folder/name
            if path.exists():
                for line in path.read_text().splitlines():
                    if line.strip():
                        row=json.loads(line);decisions[row['source_id']]=row
    d=decisions['ASTRA-FM-008']
    v=dict(id='EN-FRONT-001',page='VIII',old='Lecture Notes in Mathematics',
           printed='Lectures Notes in Mathematics',corrected='Lecture Notes in Mathematics',
           source=d['source_id'],scan_image=d['image'],scan_region=d['region'],reason=d['reason'],
           scope_start=MARKER.match(pieces['VIII']).group(),scope_end=MARKER.match(pieces['IX']).group())
    assert pieces['VIII'].count(v['old'])==1
    jsonl(HERE/'variants.jsonl',[v])
    ledger=[];checks=[];branch_hashes={}
    for layer,keyname in [('current','corrected'),('diplomatic','printed')]:
        text=front+rear
        x=text.index(v['scope_start']);y=text.index(v['scope_end'],x)
        part=text[x:y];assert part.count(v['old'])==1
        text=text[:x]+part.replace(v['old'],v[keyname],1)+text[y:]
        branch_hashes[layer]=sha(text)
        marks=list(MARKER.finditer(text))
        assert [m.group(2) for m in marks]==KEYS
        assert re.findall(r'\\SGAPrintPage\{([^}]+)\}',text)==KEYS
        en={m.group(2):text[m.end():marks[i+1].start() if i+1<len(marks) else len(text)] for i,m in enumerate(marks)}
        for key in KEYS:
            source=(HERE/'source_packets'/key/f'{layer}.tex').read_text()
            fu=Counter(MATH.findall(source));eu=Counter(MATH.findall(en[key]))
            assert fu==eu,(key,layer,list((fu-eu).elements()),list((eu-fu).elements()))
            match=MARKER.match(source)
            check=dict(page=key,layer=layer,pdf_page=int(match.group(1))+1,
                       French_math_units=sum(fu.values()),English_math_units=sum(eu.values()),
                       unexpected_difference_units=0,source_sha256=sha(source),English_sha256=sha(en[key]))
            checks.append(check)
            ledger.append(dict(record_type='page_transfer_inventory',**check,
                decision=('Literal copied publisher material, retaining original bibliographic languages.' if key in COPIED else 'Complete manual paragraph-by-paragraph English translation of the reviewed source; formulas inserted as exact literal units.'),
                image_review_attribution='Original source observations and regions are the attributed French front/backmatter audit; this translation record makes no new image-read claim.'))
    for sid,d in decisions.items():
        if str(d.get('page','')) in KEYS or sid=='ASTRA-FRONT-NOTICE-1971-RESTORATION':
            ledger.append(dict(record_type='attributed_French_disposition',source_id=sid,
                source_record=d,English_variant=v['id'] if sid=='ASTRA-FM-008' else '',
                English_disposition='Source spelling differences have the same ordinary English rendering and produce no English variant; source math, page breaks and copied publisher strings are preserved. See the explicit page records and spelling map.'))
    spelling_map=[
      ('ASTRA-FM-001','V','régigé / rédigé','written up'),
      ('ASTRA-FM-002','VII','extrêment / extrêmement','extremely'),
      ('ASTRA-FM-003','VII','coéfficients / coefficients','coefficients'),
      ('ASTRA-FM-004a','VII','Algébrique / Algébrique','Algebraic Geometry; withdrawn misprint attribution, acute retained'),
      ('ASTRA-FM-004b','VII','Algèbrique / Algébrique','Algebraic Geometry'),
      ('ASTRA-FM-005','VIII','Algèbrique / Algébrique','Algebraic Geometry'),
      ('ASTRA-FM-006','VIII','inflence / influence','influence'),
      ('ASTRA-FM-007','VIII','cites / cités','cited'),
      ('ASTRA-FM-009','XI','Fibre / Fibré','Bundle')]
    # Validate the id/page mapping against the authoritative front records.
    for sid,page_id,reading,rendering in spelling_map:
        assert str(decisions[sid]['page'])==page_id,(sid,decisions[sid]['page'],page_id)
        ledger.append(dict(record_type='source_spelling_without_English_variant',source_id=sid,page=page_id,
                           source_readings=reading,English_both_branches=rendering,English_variant=None))
    ledger.extend([
        dict(record_type='source_variant',page='VIII',source_id='ASTRA-FM-008',English_variant=v['id'],printed=v['printed'],corrected=v['corrected'],reason=v['reason']),
        dict(record_type='restored_passage',page='VII',source_id='EN-INTRO-001',decision='The complete R. Hartshorne, Residues and Duality, Lecture Notes in Mathematics no.20, Springer reference is restored.'),
        dict(record_type='corrected_sense',page='VIII',source_id='EN-INTRO-002',decision='The source says the first proof does not yet appear in the literature, including Borel–Serre and the present seminar. The inherited exceptive apart from wording is replaced by including.'),
        dict(record_type='source_content_retention',page='IX',decision='Retain the historical future to appear of the Serre article, the full Jouanolou attribution and VI1.1 full stop, both participating authors, and all siglum explanations.'),
        dict(record_type='bibliographic_copy',page='rear-717–rear-719',entries=188,decision='Every catalogue line, entry number, title, author, volume description and printed price is copied literally; bibliographic languages remain those of the original.'),
        dict(record_type='publisher_restitution',page='cover-verso',source_id='ASTRA-FRONT-NOTICE-1971-RESTORATION',decision='The identical English notice is copied from the reviewed French restitution. The new-edition preface must identify the matching Springer1971 LNM228 template and state that hidden physical strokes in the SGA6 copy were not recovered.'),
        dict(record_type='author_history',page='XI–XII',decision='The contents mark ExposéXI Not written up and do not invent an English body; all original exposé titles, authors and starting folios are retained.'),
    ])
    jsonl(HERE/'transfer.jsonl',ledger)
    joins=[]
    for keys in [FRONT,REAR]:
        for before,after in zip(keys,keys[1:]):
            joins.append(dict(before=before,after=after,source_tail=(HERE/'source_packets'/before/'current.tex').read_text()[-220:],
                              English_tail=pieces[before][-220:],English_head=pieces[after][:250],
                              decision=('The split com-/plexe is rendered com-/plex across the same physical boundary; the visible page label follows the completed word.' if after=='VIII' else 'The projective-morphism paragraph continues without an inserted blank line.' if after=='IX' else 'Explicit source leaf/section boundary retained; source blanks carry a marker but have no visible page label.')))
    dump(HERE/'folio_joins.json',joins)
    dump(HERE/'literal_math_verification.json',dict(scope=KEYS,checks=checks,
          method='Exact complete mathematical-unit multisets; no normalization or deleted commands.',
          branch_sha256s=branch_hashes,unexpected_difference_units=0,
          exact_variants=1,ordered_markers=KEYS,
          copied_publisher_pages=COPIED,limitation='This exact check supplements the manual full prose comparison; final PDF layout and global glossary integration are separate.'))
    print(json.dumps(dict(pages=len(KEYS),translation_spans=len(patches),variants=1,
                         transfer_records=len(ledger),math_units_each_branch=sum(c['French_math_units'] for c in checks if c['layer']=='current'),
                         unexpected_math=0,stable_targets=3,joins=len(joins))))

if __name__=='__main__':records()
