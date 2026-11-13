from pathlib import Path
import json,re,collections,difflib
P=Path(__file__).resolve().parent;S=P.parents[1]/'source'
def read(n):return [json.loads(l)for l in(P/n).read_text().splitlines()]
dec=read('decisions.jsonl');own=read('own_findings.jsonl');ps=read('pages.jsonl');vs=read('variants.jsonl')
for p in ps:p['findings']=sum(d['printed_page']==p['printed_page']for d in dec)+sum(d['page']==p['printed_page']for d in own)
(P/'pages.jsonl').write_text(''.join(json.dumps(p,ensure_ascii=False)+'\n'for p in ps))
changes=json.loads((P/'en_changes_5.json').read_text());ids={d['id']for d in changes}|{v['id']for v in vs if v.get('en_old')or v.get('embedded_en')}
already={632:'The English already has computations of duals.',638:'The English injectivity parenthesis already conveys the printed statement; English grammar requires its finite verb.',641:'The English already reads H^i(P,M)=0 for i>0.',643:'The English conjunction already expresses the second subordinate clause.',644:'The second degree-minus-one group already has coefficient G.',645:'The final degree-zero group already has coefficient G.',647:'The group above the isomorphism already has X-prime.',649:'The English has a single conjunction and.',650:'The English already has the subject of then stop.',651:'The English already has the compact-support subscript c.',653:'The English already restores the sentence and its subject using the latter.',654:'The English already reads defined by.',658:'All three English shifts already read[-1].',659:'French grammatical correction; English already has singular exact sequence.',661:'French article correction; English already says the exact sequence.',663:'The English pullback already has argument x.',665:'French spelling correction; English whence already conveys the printed reading.',666:'French preposition correction; English remedy that omission is already correct.',671:'The English homomorphism already begins k f_! f^!.',672:'The English sentence already has is before the functoriality.'}
coverage=[]
for d in dec:
 if not 154<=int(d['printed_page'])<=167:continue
 n=int(d['id'][-4:]);status='explicit English patch or printed/corrected variant' if d['id']in ids else already.get(n)
 assert status,d
 coverage.append(dict(id=d['id'],page=d['printed_page'],status=status))
for d in own:
 if not 154<=int(d['page'])<=167:continue
 status='explicit English patch or variant'if d['id']in ids else'No change: rejected suspected omission; arrow already present in both sources.'if d['id']=='S45-ASTRA-R-0046'else None
 assert status,d
 coverage.append(dict(id=d['id'],page=d['page'],status=status))
(P/'records/english_coverage_5.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
counts={}
for lang,name in [('fr','sga4.5-5.tex'),('en','sga4half_5_en.tex')]:
 t=(P/lang/name).read_text();markers=list(map(int,re.findall(r'\\PrintPage\{(\d+)\}',t)))
 assert markers==list(range(154,168)),(lang,markers)
 counts[lang+'_variants']=t.count(r'\var{')
 log=json.loads((P/f'records/{lang}_build_5.json').read_text());assert not any('unmatched'in x['status']or'ambiguous'in x['status'].lower()for x in log)
 before=S/'fr/miller_src'/name if lang=='fr' else S/'en/sources/components'/name
 (P/f'records/{lang}_annotated_5.diff').write_text(''.join(difflib.unified_diff(before.read_text().splitlines(True),t.splitlines(True),fromfile=str(before.relative_to(S)),tofile=f'{lang}/{name}')))
d=[x for x in dec if 154<=int(x['printed_page'])<=167]
status=dict(component=5,printed_pages=[154,167],pages_visually_checked=14,sol_decisions=len(d),verdicts=dict(collections.Counter(x['verdict']for x in d)),own_findings=sum(154<=int(x['page'])<=167 for x in own),own_rejected=1,**counts,page_markers=14,compile_status='awaiting root whole-book build',restored_matter='Complete four-entry local contents154; full adjunction identity and pairing sentence155; omitted degree-zero duality argument160.',notation_note='Ordinary/sheaf Hom distinctions156 and158 are verified print errors with apparatus. Total-degree asterisks restored at checked loci; complex degree bullets166 retained. Sol0656 supplies two separate projection-index variants. Two printed local-contents page numbers154 are corrected with separate variants.')
(P/'PART_V_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2));print(json.dumps(status,ensure_ascii=False,indent=2))
