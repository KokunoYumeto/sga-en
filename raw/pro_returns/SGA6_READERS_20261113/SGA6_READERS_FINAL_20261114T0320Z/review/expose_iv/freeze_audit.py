"""Audit saved IV decisions and exact patches; never assign image verdicts."""
from collections import Counter
from pathlib import Path
import hashlib,json,re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def rows(path):return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
def js(path):return json.loads(path.read_text())
def save(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def pageno(row):
    p=row.get('page')
    return int(p) if isinstance(p,(str,int)) and str(p).isdigit() else -1
def canonical(s):return s.replace(':entries#','#')

records=rows(HERE/'decisions.jsonl');own=rows(HERE/'own_findings.jsonl')
patches=rows(HERE/'patches.jsonl');pages=rows(HERE/'page_status.jsonl')
ids={r['source_id'] for r in records};allids=ids|{r['source_id'] for r in own}
errors=[]
for name,data,key in [('decisions',records,'source_id'),('own',own,'source_id'),('pages',pages,'page')]:
    if len({r[key] for r in data})!=len(data):errors.append({'duplicate_keys':name})
if sorted(r['page'] for r in pages)!=list(range(274,297)):errors.append('Page range is not exactly274–296.')
if not all(r.get('fully_checked') for r in pages):errors.append('Incomplete saved page status.')
for row in records+own:
    for field in ['page','source_id','verdict','printed_reading','image','region','reason','change','forms','record_type']:
        if field not in row:errors.append({'missing_field':field,'source_id':row.get('source_id')})

registry=js(ROOT/'build/registry.json');groups={}
for row in registry:
    if 274<=pageno(row)<=296:
        sid=canonical(row['id']);groups.setdefault(sid.split('#')[0],[]).append(sid)
entries=js(ROOT/'fixes/RECONCILE_CODEX_6.json')['entries']
codex_indices=[i for i,r in enumerate(entries,1) if r.get('expose')=='IV']
groups['fixes/RECONCILE_CODEX_6.json']=[f'fixes/RECONCILE_CODEX_6.json#{i}' for i in codex_indices]
coverage={}
for group,wanted in sorted(groups.items()):
    wanted=sorted(set(wanted));missing=[x for x in wanted if x not in ids]
    coverage[group]={'expected':len(wanted),'decided':len(wanted)-len(missing),'missing':missing,'source_ids':wanted}
    if missing:errors.append({'missing_group':group,'source_ids':missing})

codex_lines=(ROOT/'fr/codex/sga6_fr_r1_fr.tex').read_text().splitlines()
start=next(i for i,s in enumerate(codex_lines,1) if s.startswith(r'\section*{Exposé IV.'))
end=next(i for i,s in enumerate(codex_lines,1) if i>start and s.startswith(r'\section*{Exposé V.'))
hold=js(ROOT/'fr/codex/HOLD_VS_CORR.json')
hold_iv=[f'fr/codex/HOLD_VS_CORR.json#{i}' for i,r in enumerate(hold,1) if r['corr_lines'][0]<end and r['corr_lines'][-1]>=start]
if any(x not in ids for x in hold_iv):errors.append({'undecided_HOLD':hold_iv})

# Identify any earlier owner patches affecting the same printed folios.
other=[]
for path in (ROOT/'review').glob('*/patches.jsonl'):
    if path.parent==HERE:continue
    for row in rows(path):
        if 274<=pageno(row)<=296:other.append({'path':str(path.relative_to(ROOT)),**row})
if other:errors.append({'other_owner_patches_require_explicit_composition':other})

applied=0;render_counts={};residual={}
allowed={'uline','underline','SGAAuthorFootnote','SGAAuthorFootMark','SGAAuthorFootText','mathrm','textsubscript'}
for page in range(274,297):
    for layer in ['diplomatic','current']:
        before=(ROOT/f'build/page_packets/{page}/{layer}.tex').read_text();text=before
        for patch in patches:
            if patch['page']!=page or patch['layer'] not in ['both',layer]:continue
            expected=patch.get('expected_count',1);actual=text.count(patch['old'])
            if actual!=expected:
                errors.append({'blocked_patch':patch['source_id'],'page':page,'layer':layer,'expected':expected,'found':actual});continue
            text=text.replace(patch['old'],patch['new']);applied+=1
        pre=set(re.findall(r'\\([A-Za-z@]+)',before));post=set(re.findall(r'\\([A-Za-z@]+)',text))
        unknown=sorted(post-pre-allowed)
        if unknown:errors.append({'new_control_review':unknown,'page':page,'layer':layer})
        if re.search(r'\\(?:Ob[A-Z]|simeq[A-Za-z])',text):errors.append({'joined_control':page,'layer':layer})
        # Exposé V setup after the last bibliography is unprinted on296.
        body=text.split('% Expose V macros')[0]
        residual[f'{page}:{layer}']={
          'emph':body.count(r'\emph{'),'mathcal_O':len(re.findall(r'\\mathcal\s*(?:O|\{O\})',body)),
          'automatic_footnotes':len(re.findall(r'\\(?:footnote|footnotemark|footnotetext)\b',body))}
        if any(residual[f'{page}:{layer}'].values()):errors.append({'residual_review':page,'layer':layer,**residual[f'{page}:{layer}']})
        render_counts[f'{page}:{layer}']={'raised_K':body.count(r'K^{\bullet}'),'author_note_helpers':body.count(r'\SGAAuthorFootnote')}
        if page==288 and 'f^*(a)f^*(y)' in body:errors.append({'288_action_reversal_missing':layer})
        if page==295:
            first=r'\(x\in K_{\bullet}(X/S)\)' if layer=='current' else r'\(x\in K_{\bullet}(X)\)'
            if first not in body or r'\(a\in K_{\bullet}(S)\)' not in body:errors.append({'295_projection_domains':layer})
for patch in patches:
    if patch['source_id'] not in allids:errors.append({'patch_without_decision':patch['source_id']})

claim=js(HERE/'author_claim_issue_295.json')
identifications={name:js(HERE/name) for name in ['identification_278.json','identification_288.json','identification_295.json']}
if claim['source_id']!='ASTRA-IV-AUTHOR-CLAIM-295' or not claim['textual_action'].startswith('No patch to 3.3.3.'):
    errors.append('Author-claim source retention changed.')
if any(p['source_id']=='ASTRA-IV-AUTHOR-CLAIM-295' for p in patches):errors.append('Unexpected textual patch to retained author claim.')
private=re.compile(r'(?:/workspace/|/home/|/Users/|[A-Za-z]:\\+(?:Users|workspace|home|Temp|Documents and Settings)\\|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,})')
for row in records+own+patches+pages+[claim]+list(identifications.values()):
    if private.search(json.dumps(row,ensure_ascii=False)):errors.append({'private_reference':row.get('source_id',row.get('page'))})

audit={
 'scope':'Exposé IV, printed folios274–296 including bibliography',
 'main_scan':'scan/SGA6_scan_360dpi.pdf; physical page=folio+14',
 'witness':'scan/SGA6_witness_300dpi.djvu; physical page=folio+11; native regional checks as explicitly recorded, not a complete second-scan collation claim',
 'fully_checked_pages':sorted(r['page'] for r in pages),
 'witness_used_on_folios':sorted({r['page'] for r in pages if r.get('witness_viewed')}),
 'counts':{'source_decisions':len(records),'own_observations':len(own),'patches':len(patches),'fully_checked_pages':len(pages),
   'source_record_types':dict(Counter(r['record_type'] for r in records)),
   'patch_layers':dict(Counter(r['layer'] for r in patches)),
   'source_verdicts':dict(Counter(r['verdict'] for r in records)),
   'own_verdicts':dict(Counter(r['verdict'] for r in own))},
 'source_coverage':coverage,
 'hold_scope':{'corrected_tree':'fr/codex/sga6_fr_r1_fr.tex','first_IV_line':start,'first_V_line':end,'applicable_ids':hold_iv},
 'codex_entries':codex_indices,
 'codex_originally_rejected_entries':[i for i in codex_indices if entries[i-1].get('status')=='rejected'],
 'cumulative_validation':{'layer_applications':applied,'blocked':sum('blocked_patch' in e for e in errors if isinstance(e,dict)),'other_owner_patches':other},
 'source_readings_unresolved':[],
 'author_claim_issues':[{'source_id':claim['source_id'],'page':295,'source_status':'decided and retained','textual_emendation':None,'packet':'review/expose_iv/author_claim_issue_295.json'}],
 'identification_packets':[f'review/expose_iv/{name}' for name in identifications],
 'implementation_scope_followup':{'page296_unprinted_macro_rows':['fixes/FIXLOG_6.jsonl#339','fixes/FIXLOG_6.jsonl#340','fixes/FIXLOG_6_CURRENT.jsonl#304','fixes/FIXLOG_6_CURRENT.jsonl#305'],'meaning':'These rows are decided as code-scope resets; no Id/Ob glyph is printed on296. Later usages require their own image checks; first id use317.'},
 'notes':[
  'All23 full-page records were entered only after direct main-image comparison. The script validates coverage and composition and creates no image verdict.',
  'The checker row nominally283 concerning et l’homomorphisme canonique is recorded at its actual folio284; the nominal287 last display is recorded at actual286.',
  'Regional consultations of III231,247–248 and256 support exact mathematical identifications and the author-claim packet; no additional page is marked fully checked.',
  'The frozen II178 post-checkpoint05 reference amendment is separate in review/expose_ii_amendments; it is outside this IV manifest.',
  'The first IV295 projection domain receives /S in current; the second coefficient remains K_•(S). The separate first external tensor pairing is retained with an author-claim issue, not rewritten.'
 ],
 'residual_format_checks':residual,'mechanical_symbol_counts_for_validation_only':render_counts,'errors':errors}
save('coverage_audit.json',audit)
if errors:
    print(json.dumps({'errors':errors},ensure_ascii=False));raise SystemExit(1)
files=sorted(p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='frozen_manifest.tsv')
manifest=['path\tbytes\tsha256']
for path in files:manifest.append(f'{path.relative_to(ROOT)}\t{path.stat().st_size}\t{hashlib.sha256(path.read_bytes()).hexdigest()}')
(HERE/'frozen_manifest.tsv').write_text('\n'.join(manifest)+'\n')
print(json.dumps({'audit_passed':True,'counts':audit['counts'],'layer_applications':applied,'manifest_files':len(files),'manifest_bytes':sum(p.stat().st_size for p in files)},ensure_ascii=False))
