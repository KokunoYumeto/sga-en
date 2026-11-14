"""Audit the completed II records and hash them without assigning scan verdicts.

The canonical JSONL records contain the personally entered image decisions.
This script checks their coverage, exact patch composition, private references,
and preservation of the separately documented author-claim issue.
"""
from collections import Counter
from pathlib import Path
import hashlib,json,re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
def js(path):return json.loads(path.read_text())
def save(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def numpage(row):
    p=row.get('page')
    return int(p) if isinstance(p,(str,int)) and str(p).isdigit() else -1
def canonical(s):return s.replace(':entries#','#')

records=rows(HERE/'decisions.jsonl');own=rows(HERE/'own_findings.jsonl')
patches=rows(HERE/'patches.jsonl');pages=rows(HERE/'page_status.jsonl')
ids={r['source_id'] for r in records};allids=ids|{r['source_id'] for r in own}
errors=[]
for name,rs,key in [('decisions',records,'source_id'),('own',own,'source_id'),('pages',pages,'page')]:
    if len({r[key] for r in rs})!=len(rs):errors.append({'duplicate_keys':name})
if sorted(p['page'] for p in pages)!=list(range(160,222)):
    errors.append('The saved page range is not exactly160–221.')
if not all(p.get('fully_checked') for p in pages):errors.append('Incomplete page record.')

registry=js(ROOT/'build/registry.json')
groups={}
for row in registry:
    if 160<=numpage(row)<=221:
        sid=canonical(row['id']);group=sid.split('#')[0]
        groups.setdefault(group,[]).append(sid)
entries=js(ROOT/'fixes/RECONCILE_CODEX_6.json')['entries']
codex_ids={r['id'] for r in entries if r.get('expose')=='II'}
groups['fixes/RECONCILE_CODEX_6.json']=[f'fixes/RECONCILE_CODEX_6.json#{i}' for i,r in enumerate(entries,1) if r['id'] in codex_ids]
coverage={}
for group,wanted in sorted(groups.items()):
    wanted=sorted(set(wanted));missing=[s for s in wanted if s not in ids]
    coverage[group]={'expected':len(wanted),'decided':len(wanted)-len(missing),'missing':missing,'source_ids':wanted}
    if missing:errors.append({'missing_group':group,'source_ids':missing})

# HOLD line spans refer to the supplied corrected Codex tree. No II span lies
# between the exact II heading and the following III heading.
codex_lines=(ROOT/'fr/codex/sga6_fr_r1_fr.tex').read_text().splitlines()
start=next(i for i,s in enumerate(codex_lines,1) if s.startswith(r'\section*{Exposé II.'))
end=next(i for i,s in enumerate(codex_lines,1) if i>start and s.startswith(r'\section*{Exposé III.'))
hold=js(ROOT/'fr/codex/HOLD_VS_CORR.json')
hold_ii=[f'fr/codex/HOLD_VS_CORR.json#{i}' for i,r in enumerate(hold,1) if r['corr_lines'][0]<end and r['corr_lines'][-1]>=start]
if hold_ii:errors.append({'unexpected_II_HOLD_records':hold_ii})

middle=rows(ROOT/'review/middle/patches.jsonl')
applied=0;already=[]
controls={'uline','underline','phi','SGAAuthorFootnote','SGAAuthorFootMark','SGAAuthorFootText','simeq','operatorname'}
for page in range(160,222):
    for layer in ('diplomatic','current'):
        text=(ROOT/f'build/page_packets/{page}/{layer}.tex').read_text();before=text
        for owner,ps in [('middle',middle),('expose_ii',patches)]:
            for p in ps:
                if p['page']!=page or p['layer'] not in ('both',layer):continue
                expected=p.get('expected_count',1);found=text.count(p['old'])
                if found==0 and text.count(p['new'])==expected:
                    already.append({'page':page,'layer':layer,'source_id':p['source_id']});continue
                if found!=expected:
                    errors.append({'blocked_patch':p['source_id'],'owner':owner,'page':page,'layer':layer,'expected':expected,'found':found});continue
                text=text.replace(p['old'],p['new']);applied+=1
        pre=set(re.findall(r'\\([A-Za-z@]+)',before));post=set(re.findall(r'\\([A-Za-z@]+)',text))
        unexpected=sorted(post-pre-controls)
        if unexpected:errors.append({'unexpected_controls':unexpected,'page':page,'layer':layer})
        if re.search(r'\\(?:Ob[A-Z]|simeq[A-Za-z])',text):errors.append({'joined_control':page,'layer':layer})
        if page==181 and text.count(r'\underline{\underline{R}}\Gamma_S')!=2:errors.append({'181_R_count':layer})
        if page==190 and (r'QE^n\simeq E^n' not in text or "E'{}^n" in text):errors.append({'190_unpriming':layer})
for p in patches:
    if p['source_id'] not in allids:errors.append({'patch_without_decision':p['source_id']})

claim=js(HERE/'author_claim_issue_206.json')
if claim.get('source_reading_status')!='decided and retained' or claim.get('textual_change')!='None; no replacement theorem proposed.':
    errors.append('Author-claim packet lost its decided/retained and no-emendation status.')
for row in records+own+patches+pages+[claim]:
    value=json.dumps(row,ensure_ascii=False)
    # A TeX morphism such as Gamma_S:\Coh is not a Windows drive path.
    if re.search(r'(?:/workspace/|/home/|/Users/|[A-Za-z]:\\+(?:Users|workspace|home|Temp|Documents and Settings)\\|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,})',value):
        errors.append({'private_reference':row.get('source_id',row.get('page'))})

audit={
 'scope':'Exposé II with both appendices and bibliography, printed folios160–221',
 'main_scan':'scan/SGA6_scan_360dpi.pdf; physical PDF page=folio+14',
 'witness':'scan/SGA6_witness_300dpi.djvu; physical page=folio+11; use is regional as recorded, not a full second-scan collation claim',
 'fully_checked_pages':sorted(p['page'] for p in pages),
 'witness_used_on_folios':sorted({p['page'] for p in pages if p.get('witness_viewed')}|{numpage(p) for p in records+own if 'SGA6_witness_300dpi.djvu' in p.get('image','') and 160<=numpage(p)<=221}),
 'counts':{'source_decisions':len(records),'own_observations':len(own),'patches':len(patches),'fully_checked_pages':len(pages),
    'source_record_types':dict(Counter(r['record_type'] for r in records)),
    'patch_layers':dict(Counter(r['layer'] for r in patches)),
    'source_verdicts':dict(Counter(r['verdict'] for r in records)),
    'own_verdicts':dict(Counter(r['verdict'] for r in own))},
 'source_coverage':coverage,
 'hold_scope':{'corrected_tree':'fr/codex/sga6_fr_r1_fr.tex','first_II_line':start,'first_III_line':end,'applicable_ids':hold_ii,'neighboring_diff_ids':[35,36]},
 'codex_rejected_entries':[i for i,r in enumerate(entries,1) if r['id'] in codex_ids and r.get('status')=='rejected'],
 'cumulative_validation':{'scope':[160,221],'layer_applications':applied,'already_present_exact':already,'blocked':sum('blocked_patch' in x for x in errors if isinstance(x,dict))},
 'source_readings_unresolved':[],
 'author_claim_issues':[{'source_id':claim['source_id'],'page':206,'source_status':'decided and retained','textual_emendation':None,'packet':'review/expose_ii/author_claim_issue_206.json','continuation_page':207}],
 'notes':['The page_status file is keyed by folio, not promised to be sorted; all62 page keys are present exactly once.',
          'String-valued page keys in the six historical macro FIXLOG rows are explicitly included.',
          'The native page-marker naming in NOTE_6 places III at221, but printed221 is the final II bibliography page; III starts222.',
          'External EGAIII locator verification on196 is retrieved text evidence, separately documented; it is not claimed as image evidence.'],
 'errors':errors}
save('coverage_audit.json',audit)
if errors:
    print(json.dumps({'errors':errors},ensure_ascii=False));raise SystemExit(1)
files=sorted(p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='frozen_manifest.tsv')
manifest=['path\tbytes\tsha256']
for p in files:manifest.append(f'{p.relative_to(ROOT)}\t{p.stat().st_size}\t{hashlib.sha256(p.read_bytes()).hexdigest()}')
(HERE/'frozen_manifest.tsv').write_text('\n'.join(manifest)+'\n')
print(json.dumps({'frozen':True,'counts':audit['counts'],'manifest_files':len(files),'cumulative_validation':audit['cumulative_validation'],'coverage_errors':0},ensure_ascii=False))
