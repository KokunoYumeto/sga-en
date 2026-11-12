"""Exact, reversible French body and complete-source comparisons.

The existing source-labelled CHANGES_FR rows are retained. Additional rows cover
every unequal character through complete line hunks, including blank-only hunks.
No whitespace or mathematical notation is normalized by the differencer.

The body projection is explicitly the builder's book branch, second sisi leaf,
explicit PAGES markers, comment removal and corrected statement-label casing.
The complete-source comparison retains the original wrappers, both sisi leaves,
comments and line endings in an ordered, privacy-filtered source-file bundle.
It reconstructs the complete generated corrected TeX byte for byte, and its
inverse reconstructs the entire sanitized input bundle byte for byte.
"""
from pathlib import Path
import bisect,csv,difflib,hashlib,json,re
csv.field_size_limit(100_000_000)
from build_fr import AROOT,EROOT,FILES,EXP,PAGEBY,REC,FR,WORK,ROOT,raw_layer,uppercase_statement_labels
from fr_core import sanitize,strip_comments,tsv,writejson

COLS=['page','place','before','after','source','comparison','id','scope','kind',
      'before_offset_start','before_offset_end','after_offset_start','after_offset_end',
      'before_line_start','before_line_end','after_line_start','after_line_end']
DECISIONS=[
    {'id':'FR-CHANGE-PROJECTION','decision':'The selected-body comparison uses the builder book branch and corrected sisi leaves, preserves NDE arguments, supplies explicit PAGES.json markers, removes TeX comments with the documented control-word delimiter handling, and omits apparatus markers. Its complete line diff records all unequal spans, including blank-only differences. A separate complete-source comparison retains and accounts for every source comment and wrapper.'},
    {'id':'FR-CHANGE-SOURCE-BUNDLE','decision':'For each A71766d9/E baseline, concatenate the exact UTF-8 contents of the four tome controllers, four supplied configuration/style inputs and twenty exposé files in the recorded order, inside explicit ZIP-relative begin/end framing. Preserve source line endings. This is the declared input bundle for the complete-source comparison.'},
    {'id':'FR-CHANGE-PRIVACY','decision':'Before public comparison, replace only email addresses and local personal filesystem paths with the declared privacy placeholders. Keep original input-byte SHA256 values and privacy-filtered per-file SHA256 values. Reversible reconstruction is asserted for the privacy-filtered bundle, not for hidden personal data.'},
    {'id':'FR-TEX-MASTER-CONTROL','decision':'Construct one common annotated master with complete exposé-level diplomatic/corrected alternatives and the SGAForm selector; generated forms differ only by the selector value. The complete-source change register includes the selectors, duplicate branches, explicit folio markers and all marker definitions.'},
    {'id':'FR-TEX-FRONTMATTER','decision':'Generate the reader title, contributor and source credits, rights statement, form-specific preface and table of contents from the shared frontmatter and common French builder. Keep the complete credits on one page using a local small-font group.'},
    {'id':'FR-TEX-APPENDICES','decision':'Generate the source-labelled correction apparatus, all unresolved dispute items and all possible-misprint records only in the corrected form. Retain the separately attributed human transmission dossier and original-source supplement in diplomatic/corrected forms; retain the eight original editorial references additionally in diplomatic form.'},
]

def sha(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()

def lines_and_offsets(text):
    lines=text.splitlines(keepends=True);offsets=[0]
    for line in lines:offsets.append(offsets[-1]+len(line))
    assert offsets[-1]==len(text)
    return lines,offsets

def replay(before,rows,reverse=False):
    out=[];cursor=0
    for row in rows:
        pre='after' if reverse else 'before';post='before' if reverse else 'after'
        a=int(row[pre+'_offset_start']);b=int(row[pre+'_offset_end'])
        assert cursor<=a<=b<=len(before),(row['id'],'offset order')
        assert before[a:b]==row[pre],(row['id'],'recorded input span differs')
        out.extend([before[cursor:a],row[post]]);cursor=b
    out.append(before[cursor:]);return ''.join(out)

def compare(before,after,label,scope,file,legacy):
    assert sanitize(before)==before and sanitize(after)==after
    aa,apos=lines_and_offsets(before);bb,bpos=lines_and_offsets(after)
    marks=[(m.start(),m.group(1),m.group(2)) for m in re.finditer(r'\\SGApageno\{(\d)\}\{(\d+)\}',after)]
    markoffsets=[x[0] for x in marks]
    rows=[]
    for tag,a,b,c,d in difflib.SequenceMatcher(None,aa,bb,autojunk=True).get_opcodes():
        if tag=='equal':continue
        old=before[apos[a]:apos[b]];new=after[bpos[c]:bpos[d]]
        n=len(rows)+1;comparison=label+':'+scope
        if scope=='complete-body':
            ident=f'FR-FULLBODY-{label}-{file}-{n:04d}'
            sources=legacy.get((label,file,old,new))
            # The old labelled diff omitted only all-blank unequal hunks.
            assert sources or (not old.strip() and not new.strip()),(ident,'unattributed nonblank body hunk',old[:80],new[:80])
            source='; '.join(sorted(sources)) if sources else 'FR-CHANGE-PROJECTION'
            idx=bisect.bisect_right(markoffsets,bpos[c])-1
            page=(marks[idx][1]+':'+marks[idx][2]) if idx>=0 else str(PAGEBY[file][0]['tome'])+':'+str(PAGEBY[file][0]['folio'])
            place=f'Exposé {EXP[file]}; complete selected body; target line {c+1}'
        else:
            ident=f'FR-FULLSOURCE-{label}-{n:05d}'
            source='; '.join(['FR-CHANGE-SOURCE-BUNDLE','FR-CHANGE-PRIVACY','FR-TEX-STANDALONE','FR-TEX-MASTER-CONTROL','FR-TEX-FRONTMATTER','FR-TEX-APPENDICES','FR-ORG-REFERENCES','FR-ORG-ORIGINAL-SUPPLEMENT','FR-ORG-ORIGINAL-NOTES','FR-TEX-LITERAL-QUOTES','FR-TEX-STARRED-TOC'])
            page='complete source';place=f'{label} ordered input bundle to entire corrected standalone reader; target line {c+1}'
        rows.append(dict(page=page,place=place,before=old,after=new,source=source,comparison=comparison,id=ident,scope=scope,kind=tag,
                         before_offset_start=apos[a],before_offset_end=apos[b],after_offset_start=bpos[c],after_offset_end=bpos[d],
                         before_line_start=a+1,before_line_end=b,after_line_start=c+1,after_line_end=d))
    forward=replay(before,rows);inverse=replay(after,rows,True)
    assert forward==after and inverse==before
    audit={'comparison':label+':'+scope,'file':file,'hunks':len(rows),'before_characters':len(before),'after_characters':len(after),
           'before_utf8_bytes':len(before.encode()),'after_utf8_bytes':len(after.encode()),'before_sha256':sha(before),'after_sha256':sha(after),
           'reconstructed_sha256':sha(forward),'inverse_reconstructed_sha256':sha(inverse),
           'exact_reconstruction':True,'exact_inverse_reconstruction':True,'row_ids':[r['id'] for r in rows]}
    return rows,audit

def source_bundle(root,label):
    names=['fichiers-configuration-latex/'+n for n in ['paquets.tex','numerotation.tex','macros.tex','smfthm.sty']]
    names+=['tomes/SGA4.tex']+[f'{f}/{f}.tex' for f in FILES]+['tomes/tome1.tex','tomes/tome2.tex','tomes/tome3.tex']
    chunks=[];files=[]
    for name in names:
        path=root/name;raw=path.read_bytes();text=raw.decode('utf-8');clean=sanitize(text);rel=path.relative_to(ROOT/'sources').as_posix()
        chunks.extend(['% FR-CHANGE-INPUT-BEGIN '+rel+'\n',clean,'\n% FR-CHANGE-INPUT-END '+rel+'\n'])
        files.append({'path':rel,'original_bytes':len(raw),'original_bytes_sha256':hashlib.sha256(raw).hexdigest(),
                      'privacy_filtered_utf8_sha256':sha(clean),'privacy_filtered_characters':len(clean),'privacy_filter_changed':clean!=text,
                      'line_endings':{'CRLF':text.count('\r\n'),'bare_CR':text.count('\r')-text.count('\r\n'),'LF_total':text.count('\n')}})
    bundle=''.join(chunks);folder=REC/'change_baselines';folder.mkdir(exist_ok=True)
    target=folder/f'FR_{label}_source_bundle.txt';target.write_bytes(bundle.encode('utf-8'))
    return bundle,files,target.relative_to(ROOT/'output').as_posix()

def build():
    path=REC/'CHANGES_FR.tsv'
    with path.open(newline='',encoding='utf-8') as h:original=list(csv.DictReader(h,delimiter='\t'))
    original=[r for r in original if r['comparison'] in ['E','A71766d9']]
    legacy={}
    for r in original:
        m=re.fullmatch(r'CHANGE-(E|A71766d9)-(\d{2}(?:bis)?)-\d+',r['id'])
        if m:legacy.setdefault((m.group(1),m.group(2),r['before'],r['after']),set()).update(r['source'].split('; '))
    layers=json.loads((WORK/'corrected_layers.json').read_text())
    complete=[];audits=[];inputs=[];contexts=[]
    for label,root in [('E',EROOT),('A71766d9',AROOT)]:
        for f in FILES:
            before=sanitize(strip_comments(raw_layer(root,f,1)))
            after=sanitize(strip_comments(uppercase_statement_labels(layers['corr'][f])))
            rows,audit=compare(before,after,label,'complete-body',f,legacy)
            complete.extend(rows);audits.append(audit);contexts.append((before,after,audit))
        before,files,baseline=source_bundle(root,label)
        target=FR/'SGA4_FR_corrige_apparat.tex';after=target.read_bytes().decode('utf-8')
        rows,audit=compare(before,after,label,'complete-generated-source','all',legacy)
        audit.update({'baseline_file':baseline,'target_file':target.relative_to(ROOT/'output').as_posix()})
        complete.extend(rows);audits.append(audit);contexts.append((before,after,audit));inputs.append({'comparison':label,'files':files,'baseline_file':baseline})
    allrows=original+complete;tsv(path,allrows,COLS)
    with path.open(newline='',encoding='utf-8') as h:stored={r['id']:r for r in csv.DictReader(h,delimiter='\t')}
    assert len(stored)==len(allrows)
    for before,after,audit in contexts:
        rr=[stored[i] for i in audit['row_ids']]
        assert replay(before,rr)==after and replay(after,rr,True)==before,audit['comparison']
        audit['serialized_tsv_forward_and_inverse_verified']=True
    writejson(REC/'FR_CHANGE_AUDIT.json',{'scope':'Complete source and complete selected body; two baselines, twenty exposés each.',
              'source_byte_policy':'Original UTF-8 decoded byte content and original line endings are retained in the complete-source baseline. Privacy filtering is explicitly recorded. No other raw-source normalization is performed.',
              'body_projection_decision':'FR-CHANGE-PROJECTION','legacy_labelled_rows':len(original),'complete_comparison_rows':len(complete),'total_rows':len(allrows),
              'change_tsv_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'inputs':inputs,'comparisons':audits})
    writejson(REC/'FR_CHANGE_DECISIONS.json',DECISIONS)
    print(json.dumps({'legacy_rows':len(original),'complete_rows':len(complete),'comparisons':len(audits),'all_forward_and_inverse_checks_passed':True},indent=2),flush=True)

if __name__=='__main__':build()
