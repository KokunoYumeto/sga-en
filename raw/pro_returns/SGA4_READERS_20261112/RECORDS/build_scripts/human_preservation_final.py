"""Exact source/dossier and selected-body audit of the final human apparatus.

This reads the frozen inputs and masters; it never edits a language builder.
All public paths are relative to the output archive or its supplied sources.
"""
from pathlib import Path
import collections,csv,difflib,hashlib,json,re
from human_editorial_audit import calls,main_source
from human_source_crosswalk import alignment_key
from fr_core import FILES,EXP,strip_comments,explicit_pages,body,replace_sisi
from build_fr import quote_tex,raw_layer,restore_commented,DROOT,EROOT,AROOT
from build_en import literal_reading,page_markers
from en_common import fragment_blocks,group,sanitize,replace_spans
from en_one_model_review import selected

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'output/records'
NOTE_COMMANDS={r'\nde',r'\ndetext',r'\acorriger'}
INLINE=r'''\stepcounter{cnote}\textsuperscript{\arabic{cnote}}%
\textup{ [N.D.E.: This exercise does not seem to exist.]}'''
MASTERS={'FR':'fr/SGA4_FR_master_annote.tex','EN':'en/SGA4_EN_annotated_master.tex'}

def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text())
def note_calls(s):return [r for r in calls(s) if r['command'] in NOTE_COMMANDS]
def note_key(r):return (r['command'],re.sub(r'\s+','',strip_comments(r['arguments'][0])))

def labeled_blocks(s,pattern):
    mm=list(re.finditer(pattern,s));result={}
    for i,m in enumerate(mm):
        assert m.group(1) not in result,m.group(1)
        result[m.group(1)]=s[m.end():mm[i+1].start() if i+1<len(mm) else len(s)]
    return result

def wrapper_ranges(s,name):
    out=[]
    for m in re.finditer(re.escape(name)+r'(?![A-Za-z@])\s*\{',s):
        _,_,end,_=group(s,m.start()+len(name));out.append((m.start(),end))
    return out

def ordered_correspondence(a,b):
    """Map exact TeX reading keys from complete C notes to D notes in order."""
    found={};operations=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,[note_key(x) for x in a],[note_key(x) for x in b],autojunk=False).get_opcodes():
        operations.append({'operation':tag,'corrected_range':[i,j],'diplomatic_range':[k,l]})
        if tag=='equal':
            for x,y in zip(range(i,j),range(k,l)):found[x]=y
    return found,operations

def trace_source_notes(root,file,branch,original_ids):
    """Carry documentary note IDs through the actual source branch operation.

    The unique trace commands are inserted only into an in-memory copy, before
    each original active note call. They have no arguments in common with any
    branch selector. Removing these markers recovers the exact source reading.
    """
    raw=(root/file/(file+'.tex')).read_text();lo,hi=main_source(raw)
    source_calls=[r for r in note_calls(raw) if lo<=r['start']<hi]
    assert len(source_calls)==len(original_ids),(file,len(source_calls),len(original_ids))
    marked=replace_spans(raw,[(r['start'],r['start'],r'\HumanAuditMark{'+ident+'}') for r,ident in zip(source_calls,original_ids)])
    projected=restore_commented(replace_sisi(body(explicit_pages(marked,file)),branch),file,branch==0)
    ids=re.findall(r'\\HumanAuditMark\{([^}]+)\}',projected)
    plain=re.sub(r'\\HumanAuditMark\{[^}]+\}','',projected)
    expected=restore_commented(raw_layer(root,file,branch),file,branch==0)
    assert plain==expected,(file,branch,'trace failed to commute with projection')
    source_rows=[]
    for ident,r in zip(original_ids,source_calls):
        source_rows.append({'id':ident,'source':str((root/file/(file+'.tex')).relative_to(ROOT/'sources')),
            'source_line':r['line'],'command':r['command'],'argument':r['arguments'][0],
            'argument_sha256':digest(r['arguments'][0]),'source_ancestors':r['ancestors'],
            'context_before':raw[max(lo,r['start']-100):r['start']],
            'context_after':raw[r['end']:min(hi,r['end']+100)],
            'selected_in_this_form':ident in ids})
    return ids,source_rows

def summary(payload):
    counts=payload['counts'];checks=payload['checks'];masters=payload['masters']
    lines=['# Human editorial preservation audit','',
        '**Result: '+('PASS' if payload['passed'] else 'FAIL')+'.** '+str(sum(c['passed'] for c in checks))+' of '+str(len(checks))+' source, argument, projection and visibility checks passed.',
        '', 'The exact source arguments, source lines, per-record correspondences, selected body arguments and hashes are in [HUMAN_EDITORIAL_PRESERVATION_AUDIT.json](HUMAN_EDITORIAL_PRESERVATION_AUDIT.json). The complete original evidence is also retained separately in [HUMAN_ORIGINAL_SOURCE_RECORDS.json](HUMAN_ORIGINAL_SOURCE_RECORDS.json).',
        '', '## Paired human records','',
        '| Source scope | Records | Verified preservation route |','|---|---:|---|',
        '| Original French A71766d9 active outer `sisi` calls | 1,261 | Every original call and both raw arguments are retained, with a verified route in both language dossiers. |',
        '| Supplied D transmission | 1,258 | Every transmitted argument pair is reproduced exactly through the documented literal-TeX encoding in the French dossier. |',
        '| Released English body records | 1,171 | Every released argument pair is reproduced through the explicit folio-marker and literal-TeX encoding. |',
        '| Additional original-A records in the French supplement | 44 | Three calls flattened before D and 41 further pairs with changed transmitted argument bytes. |',
        '| Additional original-A records in the English supplement | 315 | Every original pair without two byte-identical raw arguments in a corresponding released English pair. |',
        '| Dedicated original proof rewrite | 1 per language | Complete commented printed proof and the Changement Yves replacement at Vbis, p. 138. |',
        '', 'The three original calls absent from the D paired-record inventory are `A-ORG-01-0016`, `A-ORG-17-0424` and `A-ORG-17-0496`. Their actual second arguments are the single TeX tokens `(`, `m` and `M`; the evidence preserves those exact tokens. The English crosswalk locates every original record in its native French-source line-range fragment. It records 946 pairs whose two original raw arguments occur in a corresponding released pair and 315 originals supplied separately. Twenty repeated configuration switches outside translated body fragments are explicitly excluded from the 1,171 body-record total.',
        '', '## Editorial notes and visibility','',
        '| Language and form | Raw `nde` / `ndetext` / `acorriger` calls | Hidden generated archive notices | Inline human note | Visible human notes |',
        '|---|---:|---:|---:|---:|',
        '| French diplomatic | 121 | 0 | 0 | 121 |',
        '| French corrected | 129 | 0 | 0 | 129 |',
        '| English diplomatic | 122 | 2 | 1 | 121 |',
        '| English corrected | 130 | 2 | 1 | 129 |',
        '| Both reading forms | — | — | 0 | 0 |',
        '', 'The original French source contains 127 direct editorial-note arguments and two actual `acorriger` arguments. The source definition `\\newcommand{\\acorriger}[1]{\\nde{#1}}` sends each of those two arguments unchanged to `nde`. Macro-definition templates are excluded from the invocation census. Both languages preserve all 129 original arguments in documentary dossiers visible in the diplomatic and corrected forms.',
        '', 'The English inline note is `A-NDE-04-010`, IV, p. 465: “This exercise does not seem to exist.” Its complete released marker and text remain byte-identical inside `SGAeditor`, which suppresses it in reading form. Five released English human-note arguments formerly inside `SGAArchiveOnly` are restored at X, pp. 46, 51, 52 and XVI, pp. 232, 246 without wording changes. Two VIII release-generated reference notices retain their always-hidden archive wrappers and are excluded from the visible human-note count.',
        '', '### Eight notes absent from the diplomatic body','',
        '| Original note | Exposé / page | Source scope | Retention in diplomatic and corrected forms |',
        '|---|---|---|---|']
    for r in payload['diplomatic_omissions']:
        lines.append('| `'+r['id']+'` | '+r['expose']+' / '+str(r['page'])+' | `'+r['original_pair']+'` | Exact original argument in both language dossiers. |')
    lines += ['', 'Seven notes occur only in corrected arguments of original human pairs. The eighth accompanies the proof rewrite at Vbis, p. 138. The audit carries unique note identifiers through the actual source branch selection in memory; removing the audit markers recovers the exact unmarked source projection. This identifies each omitted note and each retained note independently of note-text equality.',
        '', '## Supplied D/E note differences','',
        'Five note arguments already differ between the supplied D and E trees. The audit records their full before/after arguments, exact source lines, surrounding source context and hashes. The final diplomatic and corrected bodies preserve their respective supplied readings.',
        '', '| Original note | Supplied D → supplied E difference |','|---|---|',
        '| `A-NDE-14-003` | Reference `XIV.thm1.1` → `XIV.thm3.1`. |',
        '| `A-NDE-18-009` | `identication` → `identification`. |',
        '| `A-NDE-18-012` | `est tensorisant` → `en tensorisant`. |',
        '| `A-NDE-18-024` | `rappport` → `rapport`. |',
        '| `A-NDE-18-032` | Adds `que`; reference `1.5.10.2` → `1.5.10.4`. |',
        '', 'The corrected French body also omits the inactive source comment `%peu compréhensible` from `A-NDE-17-039`. Removing precisely that TeX comment and its terminating newline reproduces the final argument byte for byte; the complete original comment remains in the original-note dossier. Every other final French body note argument matches its selected supplied-source argument byte for byte. All 130 raw released-English note-call arguments match the corrected English body byte for byte.',
        '', '## Bibliography and dossier guards','',
        'Eight human-added XVIII bibliography entries are retained in a separately attributed diplomatic appendix in each language. French entries keep their exact original A texts and editorial ordinals 1, 2, 3, 6, 8, 9, 11, 13; only citation keys are explicitly namespaced. English entries reproduce their exact released-English wording and source record IDs. The full dossier files match their master spans after one documented metadata operation: removing an `addcontentsline` whose title exactly repeats the immediately preceding `chapter*` title. No argument bytes participate in that metadata operation.',
        '', 'The literal encoders expose TeX metacharacters, including the ASCII tilde, and add line-break opportunities. Complete raw UTF-8 arguments remain in the JSON evidence. The NDE macros, the inline-note guard and the dossier guards all suppress their editorial material in reading form.',
        '', '## Reproduction and frozen inputs','',
        'Run `python build_scripts/human_preservation_final.py` to regenerate this audit from the source trees, source-record manifests and frozen masters. It edits audit outputs only. Run `python build_scripts/audit_en_om_branches.py` for the 338-record English one-model branch audit.',
        '', '| Master | SHA256 |','|---|---|']
    for lang,r in masters.items():lines.append('| `'+r['path']+'` | `'+r['sha256']+'` |')
    lines += ['', 'The preservation audit contains source hashes for all 20 original French exposés and the released English master. Its source-record hash binds every exact argument and correspondence to the checked build.', '']
    return '\n'.join(lines)

def main():
    checks=[]
    def check(name,passed,evidence=None):
        checks.append({'check':name,'passed':bool(passed),'evidence':evidence})
    masters={lang:(ROOT/'output'/path).read_text() for lang,path in MASTERS.items()}
    master_meta={lang:{'path':path,'sha256':digest(masters[lang])} for lang,path in MASTERS.items()}
    source=read('output/records/HUMAN_ORIGINAL_SOURCE_RECORDS.json')
    original=source['original_source_records'];original_notes=source['original_NDE_records']
    transmitted=read('work_fr/initial_layers.json')['org']
    released_records=read('output/records/EN_HUMAN_RECORDS.json')
    release=(ROOT/'sources/en/C_release_20261112/04_SGA4_EN_COMPLETE_READER.tex').read_text()
    frblocks=labeled_blocks(masters['FR'],r'\\textbf\{(ORG-[0-9bis]+-\d{4}) -- [^}]+\}')
    enblocks=labeled_blocks(masters['EN'],r'\\textbf\{(EN-ORG-\d{4})\}')
    originals_blocks={lang:labeled_blocks(s,r'\\textbf\{(A-ORG-[0-9bis]+-\d{4})\}') for lang,s in masters.items()}
    note_blocks={lang:labeled_blocks(s,r'\\textbf\{(A-(?:NDE|ACORRIGER)-[0-9bis]+-\d{3})\}') for lang,s in masters.items()}
    quote={'FR':quote_tex,'EN':literal_reading}
    transmitted_rows=[]
    for r in transmitted:
        block=frblocks.get(r['id'],'')
        expected=[r'\textit{Lecture imprimée consignée dans D :} '+quote_tex(r['printed'])+r'\par',
                  r'\textit{Lecture éditoriale transmise dans D :} '+quote_tex(r['corrected'])+r'\par']
        transmitted_rows.append({'id':r['id'],'expose':r['expose'],'page':r['page'],
            'source':f"fr/D_diplomatic_after_scan_check/{r['file']}/{r['file']}.tex",
            'printed':r['printed'],'corrected':r['corrected'],
            'argument_sha256':[digest(r[k]) for k in ['printed','corrected']],
            'dossier_exact_encoded_arguments':[x in block for x in expected]})
    en_rows=[]
    for r in released_records:
        block=enblocks.get(r['id'],'')
        expected=[r'\noindent Original first reading: '+literal_reading(r['printed'])+r'\par',
                  r'\noindent Original second reading: '+literal_reading(r['corrected'])+r'\par']
        en_rows.append({'id':r['id'],'expose':r['expose'],'page':r['page'],
            'source':'en/C_release_20261112/04_SGA4_EN_COMPLETE_READER.tex',
            'printed':r['printed'],'corrected':r['corrected'],
            'argument_sha256':[digest(r[k]) for k in ['printed','corrected']],
            'dossier_exact_encoded_arguments':[x in block for x in expected]})
    check('All 1,258 D-transmitted argument pairs are encoded exactly in the French dossier',len(transmitted_rows)==1258 and all(all(r['dossier_exact_encoded_arguments']) for r in transmitted_rows))
    check('All 1,171 released-English argument pairs are encoded exactly in the English dossier',len(en_rows)==1171 and all(all(r['dossier_exact_encoded_arguments']) for r in en_rows))
    original_rows=[];byd={r['id']:r for r in transmitted_rows};bye={r['id']:r for r in en_rows}
    raw_sources={f:(ROOT/f'sources/fr/A_orgogozo_snapshot_71766d9/{f}/{f}.tex').read_text() for f in FILES}
    for r in original:
        row=dict(r);raw=raw_sources[r['file']];line=sum(len(x) for x in raw.splitlines(keepends=True)[:r['source_line']-1])
        row['exact_original_call_at_source_line']=r['raw_call'] in raw[line:line+len(r['raw_call'])+250]
        row['preservation']={}
        for lang in ['FR','EN']:
            if r['id'] in source['supplement_'+lang+'_ids']:
                block=originals_blocks[lang].get(r['id'],'')
                labels=['Premier argument original : ','Second argument original : '] if lang=='FR' else ['Original first argument: ','Original second argument: ']
                ok=[r'\noindent '+label+quote[lang](r[k])+r'\par' in block for label,k in zip(labels,['printed','corrected'])]
                row['preservation'][lang]={'route':'exact-original documentary supplement','record_id':r['id'],'arguments_verified':ok}
            elif lang=='FR':
                ref=byd.get(r['D_transmission_id']);ok=bool(ref) and all(r['D_arguments_exact']) and all(ref['dossier_exact_encoded_arguments'])
                row['preservation'][lang]={'route':'byte-identical D transmission in human dossier','record_id':r['D_transmission_id'],'arguments_verified':[ok,ok]}
            else:
                ids=r['released_english_record_ids'];ok=bool(ids) and all(r['released_english_arguments_exact']) and all(all(bye[i]['dossier_exact_encoded_arguments']) for i in ids)
                row['preservation'][lang]={'route':'byte-identical released pair, with explicit page-marker encoding in human dossier','record_ids':ids,'arguments_verified':[ok,ok]}
        original_rows.append(row)
    check('All 1,261 original A pairs have exact source evidence and an explicit verified route in both languages',len(original_rows)==1261 and all(r['exact_original_call_at_source_line'] and all(all(x['arguments_verified']) for x in r['preservation'].values()) for r in original_rows))
    # Whole included supplements also verify their form guards. The French
    # assembler removes only redundant ToC metadata immediately after chapter*.
    supplement_checks=[]
    toc=re.compile(r'(\\chapter\*\{([^{}]+)\})(\s*)\\addcontentsline\{toc\}\{chapter\}\{\2\}')
    for lang in ['FR','EN']:
        for stem in ['HUMAN_ORIGINAL_SUPPLEMENT','HUMAN_ORIGINAL_NOTES']:
            path=f'shared/{stem}_{lang}.tex';s=(ROOT/'output'/path).read_text()
            inserted=toc.sub(lambda m:m.group(1)+m.group(3),s)
            guard=r'\ifnum\SGAForm=2\relax\else' if lang=='FR' else r'\ifSGAreading\else'
            item={'file':path,'sha256':digest(s),'entire_guarded_supplement_present':inserted in masters[lang],
                  'D_C_guard_and_closing_fi':s.startswith(guard) and s.rstrip().endswith(r'\fi')}
            supplement_checks.append(item)
    check('Four complete source supplements and their D/C-only visibility guards are included',all(r['entire_guarded_supplement_present'] and r['D_C_guard_and_closing_fi'] for r in supplement_checks),supplement_checks)
    rewrite=source['dedicated_original_rewrite'];rewrite_checks={}
    for lang,s in masters.items():
        at=s.index(r'\textbf{'+rewrite['id']+r'}');block=s[at:s.index(r'\fi',at)]
        rewrite_checks[lang]={k:quote[lang](rewrite[k]) in block for k in ['printed_commented_source','editorial_rewrite_source']}
    check('The complete original commented proof and Changement Yves rewrite are retained in both dossiers',all(all(r.values()) for r in rewrite_checks.values()),rewrite_checks)
    # Fresh source D extraction checks the 1,258 dossier records independently.
    frbody=masters['FR'].split(r'\backmatter',1)[0]
    parts={e:(a,b) for e,a,b in re.findall(r'% BEGIN EXPOSE (\w+)\s*\n\\ifnum\\SGAForm=0\s*\n(.*?)\n\\else\s*\n(.*?)\n\\fi\s*\n',frbody,re.S)}
    check('Twenty independent French exposé branches found',len(parts)==20)
    fr_actual={'D':[],'C':[]};fr_source_note_rows=[];fresh_d=[]
    fr_trace_ids={'D':[],'C':[]};fr_trace_sources={'D':[],'C':[]}
    for f in FILES:
        for side,k,root in [('D',0,DROOT),('C',1,EROOT)]:
            t=restore_commented(raw_layer(root,f,k,fresh_d if side=='D' else None),f,k==0)
            before=note_calls(t);after=note_calls(parts[EXP[f]][k]);fr_actual[side].extend(after)
            strict_note_projection=len(before)==len(after) and all(a['command']==b['command'] and
                (a['arguments']==b['arguments'] or strip_comments(a['arguments'][0])==b['arguments'][0]) for a,b in zip(before,after))
            check(f'French {EXP[f]} {side} note count and exact TeX-reading projection',strict_note_projection)
            for n,(a,b) in enumerate(zip(before,after),1):
                fr_source_note_rows.append({'file':f,'form':side,'index_in_expose':n,'command':a['command'],
                    'source_argument':a['arguments'][0],'final_argument':b['arguments'][0],
                    'raw_argument_equal':a['arguments']==b['arguments'],
                    'exact_inactive_comment_projection_equal':strip_comments(a['arguments'][0])==b['arguments'][0],
                    'projection_rule':'identity' if a['arguments']==b['arguments'] else 'Remove only inactive TeX percent-comment text and its terminating newline; every other byte is identical.'})
            ids,rows=trace_source_notes(root,f,k,[r['id'] for r in original_notes if r['file']==f])
            fr_trace_ids[side].extend(ids);fr_trace_sources[side].extend(rows)
            check(f'French {EXP[f]} {side} source-position note trace commutes with branch projection',len(ids)==len(after))
    check('Fresh D source extraction equals every transmitted French dossier pair',len(fresh_d)==1258 and [(r['id'],r['printed'],r['corrected']) for r in fresh_d]==[(r['id'],r['printed'],r['corrected']) for r in transmitted])
    # Reproduce the explicit released-page-marker transform, then compare every
    # released human pair. This is an encoding crosswalk, not a count argument.
    paged=page_markers(release);encoded_pairs=[]
    for f in fragment_blocks(paged):
        encoded_pairs.extend([r for r in calls(f['text']) if r['command']==r'\sisi' and not r['ancestors']])
    check('Every released-English pair maps exactly through explicit page-marker encoding',len(encoded_pairs)==1171 and [r['arguments'] for r in encoded_pairs]==[[r['printed'],r['corrected']] for r in released_records])
    # Every released English note is matched by exact argument bytes in source
    # order. Five archive wrappers change visibility; no note wording changes.
    source_en=[];fragments=fragment_blocks(release)
    for f in fragments:
        for r in note_calls(f['text']):source_en.append({'fragment':f['name'],'file':f['file'],'call':r})
    enbody=masters['EN'][masters['EN'].index(r'\mainmatter'):masters['EN'].index(r'\backmatter')]
    en_selected={side:selected(enbody,flag) for side,flag in [('D',False),('C',True)]}
    en_actual={side:note_calls(t) for side,t in en_selected.items()}
    check('Every 130 released English note-call argument is byte-identical in final C body',len(source_en)==len(en_actual['C'])==130 and [(r['call']['command'],r['call']['arguments']) for r in source_en]==[(r['command'],r['arguments']) for r in en_actual['C']])
    en_map,en_ops=ordered_correspondence(en_actual['C'],en_actual['D'])
    check('Every shared English D/C note argument is byte-identical across the two selected bodies',all(en_actual['C'][c]['arguments']==en_actual['D'][d]['arguments'] for c,d in en_map.items()))
    check('French corrected source-position note IDs agree with the complete original note crosswalk',fr_trace_ids['C']==[r['id'] for r in original_notes])
    dpos={ident:i for i,ident in enumerate(fr_trace_ids['D'])}
    fr_map={i:dpos[ident] for i,ident in enumerate(fr_trace_ids['C']) if ident in dpos}
    fr_ops=[{'id':ident,'corrected_index':i,'diplomatic_index':fr_map.get(i),
             'same_argument_reading':note_key(fr_actual['C'][i])==note_key(fr_actual['D'][fr_map[i]]) if i in fr_map else None}
            for i,ident in enumerate(fr_trace_ids['C'])]
    check('D/C note correspondence removes exactly eight corrected-reading notes in each language',len(fr_map)==121 and len(en_map)==122 and len(fr_actual['C'])-len(fr_map)==len(en_actual['C'])-len(en_map)==8,
          {'FR_operations':fr_ops,'EN_operations':en_ops})
    byfrag=collections.defaultdict(list)
    for i,r in enumerate(source_en):byfrag[r['fragment']].append(i)
    a_byfrag=collections.defaultdict(list)
    for i,r in enumerate(original_notes):
        if r['id']!='A-NDE-04-010':a_byfrag[r['english_fragment']].append(i)
    original_to_en={};extra_en=[];fragment_crosswalk=[]
    for fragment,indices in byfrag.items():
        original_indices=a_byfrag.get(fragment,[])
        if original_indices:
            check('Original-to-English note fragment correspondence '+fragment,len(original_indices)==len(indices))
            for ai,ei in zip(original_indices,indices):original_to_en[ai]=ei
        else:extra_en.extend(indices)
        fragment_crosswalk.append({'fragment':fragment,'original_note_ids':[original_notes[i]['id'] for i in original_indices],
            'released_note_indices':[i+1 for i in indices]})
    archive={side:wrapper_ranges(t,r'\SGAArchiveOnly') for side,t in en_selected.items()}
    hidden={side:[i for i,r in enumerate(en_actual[side]) if any(a<=r['start']<b for a,b in archive[side])] for side in ['D','C']}
    check('Exactly two release-generated VIII notes remain archive-only',len(extra_en)==2 and set(extra_en)==set(hidden['C']) and len(hidden['D'])==2 and all(source_en[i]['file']=='08' for i in extra_en))
    fresh_A_notes=[]
    for f in FILES:
        raw=raw_sources[f];lo,hi=main_source(raw)
        fresh_A_notes.extend(r for r in note_calls(raw) if lo<=r['start']<hi)
    check('Every original 129 note argument matches the untouched A source exactly',len(fresh_A_notes)==129 and
          [(r['command'],r['arguments'][0]) for r in fresh_A_notes]==[(r['command'],r['argument']) for r in original_notes])
    original_note_rows=[];omissions=[]
    fr_transmissions={side:{r['id']:r for r in rows} for side,rows in fr_trace_sources.items()}
    for i,r in enumerate(original_notes):
        item=dict(r);item['documentary_preservation']={lang:quote[lang](r['argument'])+r'\par' in note_blocks[lang].get(r['id'],'') for lang in ['FR','EN']}
        fc=fr_actual['C'][i];fd=fr_actual['D'][fr_map[i]] if i in fr_map else None
        item['FR_body']={'corrected_argument':fc['arguments'][0],'corrected_command':fc['command'],
            'corrected_sha256':digest(fc['arguments'][0]),'diplomatic_argument':fd['arguments'][0] if fd else None,
            'diplomatic_visible':fd is not None,'corrected_visible':True,
            'original_argument_equal_in_corrected_body':r['argument']==fc['arguments'][0]}
        item['FR_supplied_transmissions']={side:fr_transmissions[side][r['id']] for side in ['D','C']}
        if r['id']=='A-NDE-04-010':
            item['EN_body']={'representation':'inline editorial note in the existing printed footnote','released_span':INLINE,
                'guarded_final_span':r'\SGAeditor{'+INLINE+'}','diplomatic_visible':True,'corrected_visible':True,'reading_visible':False}
        else:
            ei=original_to_en[i];ec=en_actual['C'][ei];ed=en_actual['D'][en_map[ei]] if ei in en_map else None
            item['EN_body']={'released_argument':source_en[ei]['call']['arguments'][0],
                'released_command':source_en[ei]['call']['command'],'released_fragment':source_en[ei]['fragment'],
                'corrected_argument':ec['arguments'][0],'corrected_sha256':digest(ec['arguments'][0]),
                'diplomatic_argument':ed['arguments'][0] if ed else None,
                'diplomatic_visible':ed is not None,'corrected_visible':ei not in hidden['C'],
                'released_argument_exact':source_en[ei]['call']['arguments']==ec['arguments'],
                'correspondence_basis':'Same native-source fragment and preserved note order; exact released English argument retained. Original French argument is separately preserved verbatim.'}
        if fd is None:
            reason='Note belongs to the corrected argument of the original human pair.' if r['enclosing_original_pair'] else 'Note belongs to the Changement Yves rewrite of the proof at Vbis138.'
            omissions.append({'id':r['id'],'expose':r['expose'],'page':r['page'],'original_argument':r['argument'],
                'reason':reason,'original_pair':r['enclosing_original_pair'] or rewrite['id'],
                'original_argument_retained_in_D_C_dossiers':item['documentary_preservation'],
                'English_also_corrected_only':not item['EN_body']['diplomatic_visible']})
        original_note_rows.append(item)
    check('All 129 exact original human-note arguments are present in both D/C documentary dossiers',len(original_note_rows)==129 and all(all(r['documentary_preservation'].values()) for r in original_note_rows))
    check('All 129 original human notes have French and English corrected-body counterparts',len(original_to_en)==128 and all(r['EN_body']['corrected_visible'] for r in original_note_rows))
    check('Eight diplomatic omissions are retained as source evidence in both language dossiers',len(omissions)==8 and all(all(r['original_argument_retained_in_D_C_dossiers'].values()) and r['English_also_corrected_only'] for r in omissions))
    expected_omissions={r['id'] for r in original_notes if r['enclosing_original_pair']}
    expected_omissions.add('A-NDE-05bis-016')
    check('The eight missing D-body notes are precisely the seven corrected-side human-pair notes and Vbis rewrite note',
          {r['id'] for r in omissions}==expected_omissions)
    transmitted_note_differences=[]
    for r in original_notes:
        d=fr_transmissions['D'][r['id']];c=fr_transmissions['C'][r['id']]
        if d['argument']!=c['argument']:
            transmitted_note_differences.append({'id':r['id'],'expose':r['expose'],'page':r['page'],
                'D_source':d,'E_source':c,'attribution':'Argument difference already present between the supplied D and E source trees; the final readers preserve their respective transmitted arguments. The exact original A argument is retained independently in both documentary dossiers.',
                'original_A_argument':r['argument'],
                'exact_diff':list(difflib.unified_diff(d['argument'].splitlines(),c['argument'].splitlines(),fromfile='supplied D argument',tofile='supplied E argument',lineterm=''))})
    inline={'original_human_note_id':'A-NDE-04-010','expose':'IV','page':465,
        'source':'en/C_release_20261112/04_SGA4_EN_COMPLETE_READER.tex',
        'fragment':'SGA4_IV_LINES_6788_7070_English.texfrag','released_original_span':INLINE,
        'final_guarded_span':r'\SGAeditor{'+INLINE+'}',
        'exact_released_payload_preserved':release.count(INLINE)==1 and enbody.count(r'\SGAeditor{'+INLINE+'}')==1,
        'macro_definition':r'\long\def\SGAeditor#1{\ifSGAreading\else#1\fi}',
        'visible_counts':{'diplomatic':1,'corrected':1,'reading':0}}
    check('Inline IV465 note retains its exact text and its reading-form guard',inline['exact_released_payload_preserved'] and inline['macro_definition'] in masters['EN'],inline)
    restores=read('output/records/EN_ARCHIVED_HUMAN_NOTES.json')
    for r in restores:
        check('Five-source-note visibility restoration '+r['id'],release.count(r['old_wrapper'])==1 and enbody.count(r['new_wrapper'])==1 and r['old_wrapper'] not in enbody)
    check('Both acorriger arguments expand to NDE in each language',all(r'\newcommand{\acorriger}[1]{\nde{#1}}' in s for s in masters.values()) and sum(r['command']==r'\acorriger' for r in original_notes)==2)
    selectors={
      'FR':{r'\nde':r'\long\def\nde#1{\ifnum\SGAForm=2\relax\else',r'\ndetext':r'\long\def\ndetext#1{\ifnum\SGAForm=2\relax\else',r'\ndemark':r'\def\ndemark{\ifnum\SGAForm=2\relax\else'},
      'EN':{r'\nde':r'\def\nde#1{\ifSGAreading\else',r'\ndetext':r'\def\ndetext#1{\ifSGAreading\else',r'\ndemark':r'\def\ndemark{\ifSGAreading\else'}}
    check('NDE, ndetext and ndemark definitions suppress reading-form editorial notes',all(prefix in masters[lang] for lang,defs in selectors.items() for prefix in defs.values()),selectors)
    # The active bibliography entries are checked against their own credited
    # source language; the two language renderings are not conflated.
    frrefs=read('output/records/ORGOGOZO_EDITORIAL_REFERENCES_FR.json')
    enrefs=read('output/records/EN_EDITORIAL_REFERENCE_RECORDS.json')
    bib=[]
    source_bib=raw_layer(AROOT,'18',1)
    for r in frrefs:
        exact=r'\setcounter{enumiv}{'+str(r['original_editorial_number']-1)+'}\n'+r'\bibitem{'+r['global_key']+'} '+r['text']
        item=dict(r,language='FR',source_entry_present=r'\bibitem{'+r['original_key']+'}' in source_bib and r['text'] in source_bib,final_exact_entry_present=exact in masters['FR'])
        bib.append(item)
    for r in enrefs:
        h=next(h for h in released_records if h['id']==r['human_source'])
        bib.append(dict(r,language='EN',source_entry_present=r['entry'] in h['corrected'],final_exact_entry_present=r['entry'] in masters['EN']))
    check('Eight human editorial bibliography entries per language retain exact source text',len(frrefs)==len(enrefs)==8 and all(r['source_entry_present'] and r['final_exact_entry_present'] for r in bib),[{'language':r['language'],'key':r.get('global_key',r.get('key'))} for r in bib])
    # The dedicated English human rewrite has a released-source correction
    # branch plus explicit restored printed translation. Both full variant
    # arguments are visible in its human dossier.
    rewrites=[r for r in read('output/records/EN_VARIANTS.json') if r['kind']=='human editorial rewrite']
    en_rewrite=[]
    for r in rewrites:
        at=masters['EN'].index(r'\textbf{'+r['source']+'}');block=masters['EN'][at:masters['EN'].find(r'\endgroup',at)]
        encoded=[literal_reading(r[k])+r'\par' in block for k in ['printed','corrected']]
        a=release.index('We may suppose that $p>n+1$. Write');b=release.index('\nUsing \\hyperref[Vbis.prop3.3.1]',a)
        released_rewrite=release[a:b]
        actual_without_page_marker=re.sub(r'\\SGApage\{[^}]+\}\{[^}]+\}\{[^}]+\}','',r['corrected'])
        en_rewrite.append(dict(r,dossier_exact_encoded_arguments=encoded,
            released_original_editorial_rewrite=released_rewrite,
            released_original_sha256=digest(released_rewrite),
            released_rewrite_argument_exact_after_explicit_page_marker=actual_without_page_marker==released_rewrite))
    check('Dedicated English human rewrite has both full arguments preserved in its dossier',len(en_rewrite)==1 and all(all(r['dossier_exact_encoded_arguments']) for r in en_rewrite))
    check('Dedicated English corrected rewrite retains every released source byte apart from its added folio marker',len(en_rewrite)==1 and all(r['released_rewrite_argument_exact_after_explicit_page_marker'] for r in en_rewrite))
    counts={'original_A_active_outer_pairs':1261,'FR_D_transmitted_pairs':1258,'EN_released_body_pairs':1171,
        'excluded_repeated_English_configuration_switches':20,'FR_original_pair_supplement':44,
        'EN_original_pair_supplement':315,'original_A_direct_note_arguments':127,'original_A_acorriger_arguments':2,
        'original_note_dossiers_per_language':129,'original_proof_rewrite_records_per_language':1,
        'FR':{'diplomatic':{'raw_note_calls':len(fr_actual['D']),'visible_human_notes':len(fr_actual['D'])},
              'corrected':{'raw_note_calls':len(fr_actual['C']),'visible_human_notes':len(fr_actual['C'])},'reading':{'visible_human_notes':0}},
        'EN':{'diplomatic':{'raw_note_calls':len(en_actual['D']),'archive_only_generated_calls':len(hidden['D']),'inline_human_notes':1,'visible_human_notes':len(en_actual['D'])-len(hidden['D'])+1},
              'corrected':{'raw_note_calls':len(en_actual['C']),'archive_only_generated_calls':len(hidden['C']),'inline_human_notes':1,'visible_human_notes':len(en_actual['C'])-len(hidden['C'])+1},'reading':{'visible_human_notes':0}}}
    check('Visible body human-note census agrees after explicit wrappers and inline note are counted',counts['FR']['diplomatic']['visible_human_notes']==counts['EN']['diplomatic']['visible_human_notes']==121 and counts['FR']['corrected']['visible_human_notes']==counts['EN']['corrected']['visible_human_notes']==129,counts)
    csv.field_size_limit(100_000_000)
    judged=list(csv.DictReader((REC/'ONE_MODEL_MISPRINTS_JUDGED.tsv').open(),delimiter='\t'))
    existing_human=[r for r in judged if r['verdict']=='accept' and r['application']=='preserve-human-apparatus']
    linked='\n'.join(r['source'] for r in read('output/records/FR_VARIANTS.json')+read('output/records/EN_VARIANTS.json'))
    new_human_links=set(r['id'] for r in existing_human)&set(re.findall(r'OM-(?:OPUS|SOL)-\d{4}',linked))
    check('The 53 accepted findings in existing human apparatus create no new OM variant',len(existing_human)==53 and not new_human_links,{'records':len(existing_human),'new_variant_source_ids':sorted(new_human_links)})
    payload={'passed':all(r['passed'] for r in checks),'masters':master_meta,'counts':counts,'checks':checks,
        'source_record':'records/HUMAN_ORIGINAL_SOURCE_RECORDS.json','source_record_sha256':digest((REC/'HUMAN_ORIGINAL_SOURCE_RECORDS.json').read_text()),
        'original_source_hashes':{f'fr/A_orgogozo_snapshot_71766d9/{f}/{f}.tex':digest(s) for f,s in raw_sources.items()},
        'released_English_source_sha256':digest(release),
        'scope_note':'The 1,261 original active outer sisi calls, 1,258 D-transmitted records and 1,171 released-English body records have different documented scopes. Three A calls were collapsed before D; 41 other A pairs have changed D argument bytes. The French supplement reproduces those 44 originals. Every A pair is linked to its native English line-range fragment; 946 pairs have both raw arguments present in a corresponding released pair and 315 originals are reproduced in the English supplement. Twenty repeated English configuration switches are outside source body fragments and are excluded. All original raw arguments and hashes are retained; no translation equivalence is inferred from record counts.',
        'encoding_policy':'Literal dossiers encode TeX metacharacters, math glyphs, line breaks and break opportunities through quote_tex or literal_reading. Complete original UTF-8 arguments and their hashes remain in the JSON evidence. Explicit pageoriginale-to-SGApage correspondence is checked independently for every released English pair. Source-body NDE comparison records exact raw bytes and separately checks removal of inactive TeX percent-comment text and its terminating newline; every other byte is identical. The one changed final French body argument loses only an inactive source comment, whose exact text is retained in the original-note dossier.',
        'original_pairs':original_rows,'transmitted_FR_pairs':transmitted_rows,'released_EN_pairs':en_rows,
        'original_notes':original_note_rows,'FR_source_to_body_note_arguments':fr_source_note_rows,
        'FR_D_E_transmitted_note_differences':transmitted_note_differences,
        'FR_note_projection_proof':'A unique audit-only marker is inserted before each source note call in memory. Explicit-page encoding, book-body extraction, sisi selection and the dedicated commented-proof projection are applied. Removing the markers gives exactly the unmarked source projection. The surviving marker IDs therefore specify the selected source-to-body note correspondence, including supplied D/E argument differences; raw argument equality across D and E is never assumed.',
        'note_fragment_crosswalk':fragment_crosswalk,'diplomatic_omissions':omissions,
        'inline_English_note':inline,'restored_English_archive_notes':restores,
        'remaining_archive_only_generated_English_notes':[{'fragment':source_en[i]['fragment'],'argument':source_en[i]['call']['arguments'][0]} for i in extra_en],
        'dedicated_original_rewrite':dict(rewrite,preservation_checks=rewrite_checks),
        'dedicated_English_rewrite':en_rewrite,'bibliography_provenance':bib,
        'accepted_findings_preserved_in_existing_human_apparatus':existing_human}
    (REC/'HUMAN_EDITORIAL_PRESERVATION_AUDIT.json').write_text(sanitize(json.dumps(payload,ensure_ascii=False,indent=2))+'\n')
    (REC/'HUMAN_EDITORIAL_PRESERVATION_AUDIT.md').write_text(summary(payload))
    missing=[r['check'] for r in checks if not r['passed']]
    print('Human preservation checks',sum(r['passed'] for r in checks),'/',len(checks),'passed',payload['passed'])
    for r in missing:print('FAIL',r)
    print('Masters',master_meta);print('Visible notes FR/EN',counts['FR'],counts['EN'])
    return payload

if __name__=='__main__':main()
